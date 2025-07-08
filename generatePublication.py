# coding=utf-8
import argparse
from businessAiProcessing import generatePublication

argParser = argparse.ArgumentParser(description="Запуск формирования публикации для указанной организации")
argParser.add_argument("orgName")

commandLine = argParser.parse_args()

generatePublication(commandLine.orgName)