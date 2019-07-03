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

cursor.execute(f"select * from goods")
db.commit()
cursor.close()
db.commit()
cursor.close()
cursor.close()
data = cursor.fetchall()


print((data))



res={}
li = []
res[data[0][0]]={'num':data[0][2],'weight':65}
for l in data:
    res={'goods_name':l[1],'goods_nums':l[2],'goods_price':l[3],'goods_type':l[4]}
    li.append(res)
res['mess']= 'ok'
print(li)


