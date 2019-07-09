import pymysql
from flask import session
from  user import *
db = pymysql.connect(
    host='192.168.43.68',
    port=3306,
    user='root',
    passwd='',
    db='web_db',
    charset='utf8'
)




li=[]
li.append(154)
li.append(153)
s=""
for l in li:
    s +=str(l)+','
print(s[:-1])
cal_sub(s)