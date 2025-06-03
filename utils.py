# coding=utf-8

import consul

__consul = None
__db_url = None
__db_schema = ""
__application_name = ""
__consul_available = True

dbConnectionError = "База данных недоступна:"
consulConnectionError = "Consul not connected"
dbURL = "postgresql://postgres:postgres@localhost:5432/postgres"

def __getConsulProvider():
    global __consul
    if __consul is None:
        __consul = consul.Consul(host='192.168.0.10', port=18500, scheme='http')
    return __consul


# Параметры подключения к базе данных
def getDbUrl() -> str:
    global __db_url
    global __consul_available
    if __db_url is not None:
        return __db_url
    try:
        if __consul_available:
            result = __getConsulProvider().kv.get('business_ai.dbUrl')[1]
            if result is None:
                __getConsulProvider().kv.put('business_ai.dbUrl', str(dbURL))
                __db_url = dbURL
            else:
                __db_url = result['Value'].decode('UTF-8')
            return __db_url
        else:
            __db_url = dbURL
            return __db_url
    except Exception as e:
        __db_url = dbURL
        print(consulConnectionError + f" {e}")
        __consul_available = False
        return __db_url


def getDbSchema() -> str:
    global __db_schema
    global __consul_available
    if __db_schema != "":
        return __db_schema
    try:
        if __consul_available:
            result = __getConsulProvider().kv.get('business_ai.dbSchema')[1]
            if result is None:
                __getConsulProvider().kv.put('business_ai.dbSchema', "business_ai")
                __db_schema = "business_ai"
            else:
                __db_schema = result['Value'].decode('UTF-8')
            return __db_schema
        else:
            __db_schema = "business_ai"
            return __db_schema
    except Exception as e:
        print(consulConnectionError + f" {e}")
        __consul_available = False
        __db_schema = "business_ai"
        return __db_schema


def getBusinessDbSchema() -> str:
    global __db_schema
    global __consul_available
    if __db_schema != "":
        return __db_schema
    try:
        if __consul_available:
            result = __getConsulProvider().kv.get('business_ai.businessDbSchema')[1]
            if result is None:
                __getConsulProvider().kv.put('business_ai.businessDbSchema', "business_ai")
                __db_schema = "business_ai"
            else:
                __db_schema = result['Value'].decode('UTF-8')
            return __db_schema
        else:
            __db_schema = "business_ai"
            return __db_schema
    except Exception as e:
        print(consulConnectionError + f" {e}")
        __consul_available = False
        __db_schema = "business_ai"
        return __db_schema


def getApplicationName() -> str:
    global __application_name
    global __consul_available
    if __application_name != "":
        return __application_name
    try:
        if __consul_available:
            result = __getConsulProvider().kv.get('business_ai.applicationName')[1]
            if result is None:
                __getConsulProvider().kv.put('business_ai.applicationName', "business-ai")
                __application_name = "business-ai"
            else:
                __application_name = result['Value'].decode('UTF-8')
            return __application_name
        else:
            __application_name = "business-ai"
            return __application_name
    except Exception as e:
        print(consulConnectionError + f" {e}")
        __application_name = "business-ai"
        __consul_available = False
        return __application_name

def getPublicationsInterval() -> int:
    global __consul_available
    try:
        if __consul_available:
            result = __getConsulProvider().kv.get('business_ai.publicationsInterval')[1]
            if result is None:
                result = 345600000
                __getConsulProvider().kv.put('business_ai.publicationsInterval', str(result))
            else:
                result = int(result['Value'].decode('UTF-8'))
            return result
        else:
            return 345600000
    except Exception as e:
        print(consulConnectionError + f" {e}")
        __consul_available = False
        return 345600000
