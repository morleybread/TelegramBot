import os

import yaml
import mysql

# 装载配置

with open("setup.cfg", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    MysqlData = data["mysql"]
    TelegramBotId = data["telegrambotid"]


def getMysqlConfig():
    if os.environ.get('ENV') == 'dev':
        MysqlData["password"]='root'

    mydb = mysql.connector.connect(
        host=MysqlData["host"],
        user=MysqlData["user"],

        password=MysqlData["password"],
        database="telegramdata",
    )
    return mydb


def getTelegramId():
    return TelegramBotId
