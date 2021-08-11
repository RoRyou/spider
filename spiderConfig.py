URL = "https://www.douyu.com/606118"

NUMMIN = 15 #每XX分钟一次

DURATION = NUMMIN*60
TIMESPLIT = 30

pg_host = "192.168.2.154"
pg_port = "5432"
pg_user = "cy_t15_read"
pg_password = "e7xwzt3CxJoxYNZ8"
pg_database = "db_ana_t15"
pg_table = "public.spider_dy"


def retURL():
    return URL


def retIntTime():
    return NUMMIN


def dbconfig():
    return pg_host, pg_port, pg_user, pg_password, pg_database, pg_table


def retDuration():
    return DURATION

def retTimeSplit():
    return TIMESPLIT
