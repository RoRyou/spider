import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import mysql.connector
import psycopg2
import pandas as pd
import datetime

URL = "https://www.douyu.com/22222"
NUMMIN = 10
pg_host = "192.168.2.154"
pg_port = "5432"
pg_user = "cy_t15_read"
pg_password = "e7xwzt3CxJoxYNZ8"
pg_database = "db_ana_t15"
pg_table = "public.spider_dy"


# REGULARTYPE = 10  # 每0（一直执行，一天做一次结算），10，30，60 分钟执行一次


def gpcon(host, port, user, password, database, sql):
    conn_string = "host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password
    gpconn = psycopg2.connect(conn_string)

    curs = gpconn.cursor()

    curs.execute(sql)

    gpconn.commit()

    curs.close()
    gpconn.close()


def getText():
    comments = browser.find_elements(By.CLASS_NAME, 'Barrage-notice--normalBarrage')
    commentsList_ = []
    for comment in comments:
        commentsList_.append(comment.text)
    return commentsList_


def removeLabel(commentList):
    comtext = []
    for line in commentList:
        if re.search('\n', line) is not None:
            text = line.split('\n')[1]
            comtext.append(text)
        else:
            comtext.append(line)
    return comtext


def scrollScreen():
    for i in range(1, random.randint(2, 4)):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(random.randint(1, 3))


def getData():
    comments = browser.find_elements(By.CLASS_NAME, 'Barrage-notice--normalBarrage')
    return comments


def genValues(texts):
    values = []
    for text in texts:
        nameword = text.split('：')
        name = nameword[0]
        word = nameword[1]
        washtime = str(datetime.datetime.now())
        values.append([name, word, washtime, URL])

    values = str(values).replace('[', '(').replace(']', ')')
    values = values[1:-1]
    return values


def regularTime():
    # NUMMIN,Type = regularType(REGULARTYPE)
    if (datetime.datetime.now().minute % 10 == 00) & (datetime.datetime.now().second == 00):
        return True
    else:
        return False


# # 设定时间进行定时
# #返回3个值，
# def regularType(REGULARTYPE):
#     if REGULARTYPE == 0:
#         NUMMIN = 24 * 60
#         Type= 0
#         return NUMMIN,Type
#     elif REGULARTYPE == 10:
#         NUMMIN = 10
#         Type = 10
#         return NUMMIN,Type
#     elif REGULARTYPE == 30:
#         NUMMIN = 30
#         Type = 30
#         return NUMMIN, Type
#     elif REGULARTYPE == 60:
#         NUMMIN = 60
#         Type = 60
#         return NUMMIN, Type

def checkEndTime():
    enddate = datetime.datetime.strptime(strEnd, '%Y-%m-%d')
    if enddate > datetime.datetime.now():
        return True
    else:

        return False


if __name__ == '__main__':

    strEnd = input("请输入截止时间(格式为Y-M-D):")

    if checkEndTime() is False:
        print("截止时间小于当前时间，已中断")


    elif checkEndTime() is True:
        print("程序开始执行")
        while True:

            if regularTime() is True:

                print(datetime.datetime.now())
                print('预计采集', NUMMIN, '分钟数据')
                browser = webdriver.Firefox()
                browser.get(URL)

                scrollScreen()

                time.sleep(NUMMIN * 60)

                commentsList_ = getText()
                browser.close()

                data = removeLabel(commentsList_)
                print('采集完毕')
                print(len(data))

                if len(data) == 0:
                    print("无评论")

                else:
                    values = genValues(data)

                    sql = f"insert into spider_dy(username,comment,washtime,url)values {values}"
                    print(sql)

                    # sql
                    gpcon(pg_host, pg_port, pg_user, pg_password, pg_database, sql)

                print(datetime.datetime.now())

            elif checkEndTime() is False:
                print("截止时间小于当前时间，已中断")
                break
