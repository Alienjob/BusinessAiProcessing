import os
import yaml
import consul
import requests
from io import StringIO

def getProfileSuffix(profile: str):
    if profile is None or len(profile) < 1 or profile.lower() == 'production':
        return ''
    if profile.lower() == 'development':
        return ',dev'
    return ',' + profile

class Environment:

    def __init__(self, name: str):
        try:
            self.profile = getProfileSuffix(os.environ['PYTHON_PROFILE'])
        except KeyError:
            self.profile = ''
        self.values = None
        self.consul = None
        self.name = name

    def __getConsul(self):
        if self.consul is None:
            try:
                consulPort = os.environ['CONSUL_PORT']
            except KeyError:
                consulPort = 8500
            try:
                consulHost = os.environ['CONSUL_HOST']
            except KeyError:
                consulHost = 'consul'
            self.consul = consul.Consul(host=consulHost, port=consulPort, scheme='http')
        return self.consul

    def __getProfileConsul(self):
        consulPath = 'config/' + self.name + self.profile + "/data"
        try:
            result = self.__getConsul().kv.get(consulPath)
            if result is None or result[1] is None:
                return None
            return result[1]['Value']
        except requests.exceptions.ConnectionError:
            print("Consul connection error ")
            return None

    def __getConfigFileName(self):
        fileName = self.name
        if len(self.profile) > 0:
            fileName = fileName + self.profile
        return fileName.replace(',', '_') + ".yaml"

    def __getValues(self):
        if self.values is None:
            try:
                consulConfig = self.__getProfileConsul()
                if consulConfig is None:
                    with open(self.__getConfigFileName(), 'r') as file:
                        self.values = yaml.safe_load(file)
                else:
                    self.values = yaml.safe_load(consulConfig)
            except FileNotFoundError:
                print(f"Error: Configuration file not found at {self.__getConfigFileName()}")
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")
        return self.values

    def get(self, name: str, defaultValue = None):
        i = 1
        try:
            path = name.split('.')
            result = self.__getValues()[path[0]]
            while i < len(path):
                if result is None:
                    return defaultValue
                result = result[path[i]]
                i = i + 1
            return result
        except KeyError:
            return defaultValue

    def __saveValues(self):
        stringToSave = StringIO()
        yaml.dump(self.__getValues(), stringToSave, default_flow_style = False)
        consulPath = 'config/' + self.name + self.profile + "/data"
        try:
            self.__getConsul().kv.put(consulPath, stringToSave.getvalue())
        except requests.exceptions.ConnectionError:
            with open(self.__getConfigFileName(), 'w') as file:
                file.write(stringToSave.getvalue())

    def set(self, name: str, value):
        path = name.split('.')
        item = self.__getValues()
        if item is None:
            item = dict()
            self.values = item
        for i in range(len(path) - 1):
            element = item[path[i]]
            if element is None:
                element = dict()
                item[path[i]] = element
            item = element
        item[path[len(path) - 1]] = value
        self.__saveValues()
