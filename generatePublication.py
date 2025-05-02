# coding=utf-8

import utils
import string
import argparse
import psycopg2 as ps

def generatePublication(organizationId: string, promptId: string):
    try:
        conn = ps.connect(utils.getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT kind, fcontent FROM " + utils.getDbSchema() +
                           ".prompts WHERE id = '" + promptId)
            for r in cursor.fetchall():
                if r[0] == 0:

    except Exception as e:
        print(utils.dbConnectionError, e)


argParser = argparse.ArgumentParser(description="Запуск формирования новости")
argParser.add_argument("-organizationId", dest="organizationId", required=True)
argParser.add_argument("-promptId", dest="promptId")

commandLine = argParser.parse_args()

generatePublication(commandLine.organizationId, commandLine.promptId)
