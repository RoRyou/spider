# coding=gbk

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
import _thread
import threading

from work.project.spider import spiderConfig

# PARAMETER
URL = spiderConfig.retURL()
NUMMIN = spiderConfig.retIntTime()
DURATION = spiderConfig.retDuration()

pg_host, pg_port, pg_user, pg_password, pg_database, pg_table = spiderConfig.dbconfig()
TIMESPLIT = spiderConfig.retTimeSplit()


def inputStartEndTime():
    try:
        strStart = input("请输入开始日期(格式为Y-M-D)：")
        strEnd = input("请输入截止日期(格式为Y-M-D)：")
        startDate = datetime.datetime.strptime(strStart, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(strEnd, '%Y-%m-%d')

        # if startDate == localTime().date():
        #     startDate = localTime()

        lTime = localTime()

        if startDate < lTime:
            print("Error:开始日期小于当前时间")
        elif endDate < lTime:
            print("Error:截止日期小于当前时间")
        elif endDate < startDate:
            print("Error:截止日期小于开始日期")
        else:
            return startDate, endDate
    except IOError:
        print("Error: 开始时间输入有误")


def localTime():
    lTime = datetime.datetime.now()
    lTime = lTime.strftime('%Y-%m-%d %H:%M:%S')
    lTime = datetime.datetime.strptime(lTime, '%Y-%m-%d %H:%M:%S')
    return lTime


def gpcon(host, port, user, password, database, sql):
    conn_string = "host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password
    gpconn = psycopg2.connect(conn_string)

    curs = gpconn.cursor()

    curs.execute(sql)

    gpconn.commit()

    curs.close()
    gpconn.close()


def removeLabel(commentList):
    comtext = []
    for line in commentList:
        if re.search('\n', line) is not None:
            text = line.split('\n')[1]
            comtext.append(text)
        else:
            comtext.append(line)
    return comtext


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


# 定时
def regularTime():
    # NUMMIN,Type = regularType(REGULARTYPE)
    if datetime.datetime.now().minute % NUMMIN == 0:  # NUMMIN
        return True
    else:
        return False


def getData():
    try:
        browser = webdriver.Firefox()
        browser.get(URL)

        for i in range(1, random.randint(2, 4)):
            time.sleep(random.randint(1, 3))
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        time.sleep(DURATION)  # 60

        comments = browser.find_elements(By.CLASS_NAME, 'Barrage-notice--normalBarrage')
        commentsList_ = []
        for comment in comments:
            commentsList_.append(comment.text)

        browser.close()

        data = removeLabel(commentsList_)
        data = list(set(data))
        print('采集完毕')
        print(len(data))


    except:
        print("ERROR:数据采集问题")

    try:
        if len(data) == 0:
            print("无评论")

        else:
            values = genValues(data)

            sql = f"insert into spider_dy(username,comment,washtime,url)values {values}"
            print(sql)

            # sql
            gpcon(pg_host, pg_port, pg_user, pg_password, pg_database, sql)
    except:
        print("ERROR：数据加载问题")


def localcheck(startDate, endDate):
    if localTime() <= startDate:
        return 0  # 时间未开始
    elif (localTime() >= startDate) & (localTime() <= endDate):
        return 1  # 开始
    else:
        return 2  # 结束


def mainf():
    while True:
        if localTime().second % TIMESPLIT == 0:
            print(localTime())

        time.sleep(1)

        # 每10分钟开始执行
        if regularTime() is True:
            if localTime().second % TIMESPLIT == 0:
                print(localTime())
            print("程序开始执行")
            print('预计采集', NUMMIN, '秒数据')
            getData()


exitflag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name + '\n')

        threadPro(self.name, self.counter)
        print("结束线程：" + self.name + '\n')
        print(localTime())


def threadPro(threadName, counter):
    while counter:
        if exitflag:
            threadName.exit()
        getData()
        # print("%s:%s"%(threadName,localTime()))
        counter -= 1

#threadflag = 1
def threadLine(threadNum):
    threadflag = 1

    while threadflag:
        if (localTime().minute % NUMMIN == 0)&(localTime().second == 0):
            print(localTime())
            time.sleep(1)
            threadName = 'thread' + str(threadNum)
            threadName = myThread(threadNum, threadName, 1)

            threadName.start()

            threadflag = 0


if __name__ == '__main__':
    # 时间输入检测
    # try:
    #     startDate, endDate = inputStartEndTime()
    #
    # except:
    #     print("ERROR:时间有误")
    # else:
    #     print("时间输入无误，开始执行程序")

    startDate = localTime() + datetime.timedelta(seconds=10)
    endDate = startDate+ datetime.timedelta(hours=2)
    print(startDate, endDate)

    # if startDate == localTime().date():
    #     startDate = localTime() + datetime.timedelta(seconds=10)

    # 时间范围检测
    threadNum = 1
    while 1:
        if localTime().second % TIMESPLIT == 0:
            print(localTime())
            time.sleep(1)
        else:
            pass

        if localcheck(startDate, endDate) == 0:
            pass
        elif localcheck(startDate, endDate) == 1:

            threadLine(threadNum)
            threadNum += 1
        elif localcheck(startDate, endDate) == 2:
            break
