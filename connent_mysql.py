import pymysql


db = pymysql.connect(
    host='192.168.43.68',
    port=3306,
    user='root',
    passwd='',
    db='web_db',
    charset='utf8'
)



cursor = db.cursor()
cursor.execute("select * from goods ")
print(cursor.fetchall())