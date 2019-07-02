import pymysql
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='web_db',
    charset='utf8'
)
username = 'ddd'
password = 'dd'
sex= 's'
cursor = db.cursor()
cursor.execute(f"select password from user where username ='{username}'")
db.commit()
cursor.close()
cursor.close()
data = cursor.fetchall()
print(data)


