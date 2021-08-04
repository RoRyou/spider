import time
from selenium import webdriver
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import mysql.connector
import psycopg2
import pandas as pd
URL = "https://www.douyu.com/110/"



pg_host = "192.168.2.154"
pg_port = "5432"
pg_user = "cy_t15_read"
pg_password = "e7xwzt3CxJoxYNZ8"
pg_database = "db_ana_t15"
pg_table = "public.spider_dy"


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
    for i in range(1, 5):
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
        values.append(name)
        values.append(word)
    values = str(values).replace('[','(').replace(']',')')
    return values

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get(URL)

    time.sleep(random.randint(5, 10))

    scrollScreen()
    commentsList_ = getText()
    browser.close()

    #ETL
    data = removeLabel(commentsList_)

    values = genValues(data)

    sql = f"insert into spider_dy(username,comment)values {values}"
    print(sql)
    print(data)
    print(len(data))

#     #sql
#     gpcon(pg_host, pg_port, pg_user, pg_password, pg_database, pg_sql)
# pg_sql = f"insert into spider_dy(username,comment)values {valuse}"
# gpcon(pg_host, pg_port, pg_user, pg_password, pg_database, pg_sql)


text = ['德拉诺什： 难道不是吗', '主播天问： 常乃超的原型确实是功德林的', '舌 七两牛肉二两面： 承认了', 'gutyyijp： 这个牙真实', '脑残喷子的野爹： 送走']


def genValues(texts):
    values = []
    for text in texts:
        nameword = text.split('：')
        name = nameword[0]
        word = nameword[1]
        values.append(name)
        values.append(word)
    values = str(values).replace('[','(').replace(']',')')
    return values


c = genValues(text)
print(c)
