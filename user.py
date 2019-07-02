import pymysql
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='web_db',
    charset='utf8'
)
class User:
    username = ''
    passwd = ''
    sex = ''
    def __init__(self,name=None,pswd=None,sex=None):
        self.username = name
        self.passwd = pswd
        self.sex=sex
    def test_password(self):
       
        try:
            cursor = db.cursor()
            cursor.execute(f"select password from user where username ='{self.username}'")
            data = cursor.fetchall()
            cursor.close()
           
            print(data)
            
            if self.passwd == str(data[0][0]):
                return 1
            else:
                return 0
        except:
            return -1
            
    def regist(self):
        try:
            
            cursor = db.cursor()
            cursor.execute(f"insert into user values (NULL,'{self.username}','{self.passwd}','{self.sex}')")
            db.commit()
            cursor.close()
            return 1
        except:
            return 0
class Goods:
    id=None
    goods_name = None
    goods_nums = None
    price = None
    type = None
    def __init__(self,name = None,nums= 0,price = 99999,type = None):
        self.goods_name=name
        self.id=None
        self.type=type
        self.goods_nums=int(nums)
        self.price=int(price)
    def add_sql(self):
        try:
            
        
            cursor = db.cursor()
           
            cursor.execute(f"insert into goods values (NULL,'{self.goods_name}',{self.goods_nums},{self.price},'{self.type}')")
            db.commit()
            cursor.close()
            return 1
        except:
            return 0
        
        
    
            
        
        
