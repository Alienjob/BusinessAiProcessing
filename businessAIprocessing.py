# coding=utf-8

import string
import consul
import psycopg2 as ps

__consul = None
__db_url = None
__db_schema = ""
__application_name = ""
__consul_available = True
__active_community_status = 1

dbConnectionError = "База данных недоступна:"
consulConnectionError = "Consul not connected"
dbURL = "postgresql://postgres:postgres@localhost:5432/postgres"

def __getConsulProvider():
    global __consul
    if __consul is None:
        __consul = consul.Consul(host='192.168.0.10', port=18500, scheme='http')
    return __consul


# Параметры подключения к базе данных
def getDbUrl() -> string:
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
    except Exception:
        __db_url = dbURL
        print(consulConnectionError)
        __consul_available = False
        return __db_url


def getDbSchema() -> string:
    global __db_schema
    global __consul_available
    if __db_schema != "":
        return __db_schema
    try:
        if __consul_available:
            result = __getConsulProvider().kv.get('business_ai.dbSchema')[1]
            if result is None:
                __getConsulProvider().kv.put('business_ai.dbSchema', "application")
                __db_schema = "application"
            else:
                __db_schema = result['Value'].decode('UTF-8')
            return __db_schema
        else:
            __db_schema = "application"
            return __db_schema
    except Exception:
        print(consulConnectionError)
        __consul_available = False
        __db_schema = "application"
        return __db_schema


def getBusinessDbSchema() -> string:
    global __db_schema
    global __consul_available
    if __db_schema != "":
        return __db_schema
    try:
        if __consul_available:
            result = __getConsulProvider().kv.get('business_ai.businessDbSchema')[1]
            if result is None:
                __getConsulProvider().kv.put('business_ai.businessDbSchema', "business")
                __db_schema = "business"
            else:
                __db_schema = result['Value'].decode('UTF-8')
            return __db_schema
        else:
            __db_schema = "business"
            return __db_schema
    except Exception:
        print(consulConnectionError)
        __consul_available = False
        __db_schema = "business"
        return __db_schema


def getApplicationName() -> string:
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
    except Exception:
        print(consulConnectionError)
        __consul_available = False
        __application_name = "business-ai"
        return __application_name

def generatePublication(organization: string):
    print("Generate publication for {}", organization)
    try:
        conn = ps.connect(getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT fname FROM " + getDbSchema() +
                           ".community WHERE fapp = '" + getApplicationName() +
                           "' AND status = " + str(__active_community_status))
            for community in cursor.fetchall():
                processClientRequests(community)
                generatePublication(community)
    except Exception as e:
        print(dbConnectionError, e)

def processClientRequests(organization: string):
    print("Process client requests for {}", organization)

def businessAiProcessing():
    global __active_community_status
    try:
        conn = ps.connect(getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT fname FROM " + getDbSchema() +
                           ".community WHERE fapp = '" + getApplicationName() +
                           "' AND status = " + str(__active_community_status))
            for community in cursor.fetchall():
                with conn.cursor() as orgCursor:
                    orgCursor.execute("SELECT id FROM " + getBusinessDbSchema() )
                processClientRequests(community)
                generatePublication(community)
    except Exception as e:
        print(dbConnectionError, e)

businessAiProcessing()
