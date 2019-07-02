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

cursor.execute(f"delete from goods where goods_name='sjj'")
db.commit()
cursor.close()
db.commit()
cursor.close()
cursor.close()
data = cursor.fetchall()


print('6'.)


