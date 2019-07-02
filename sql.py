import pymysql
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='web_db',
    charset='utf8'
)
username = '11111'
password = 'dd'
sex= 's'
cursor = db.cursor()
cursor = db.cursor()

cursor.execute(f"insert into goods values (NULL,'sjj','10','100','ol')")
db.commit()
cursor.close()
db.commit()
cursor.close()
cursor.close()
data = cursor.fetchall()
print(data)

print(int('5')+6)


