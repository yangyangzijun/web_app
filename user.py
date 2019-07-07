import pymysql
db = pymysql.connect(
    host='192.168.43.68',
    port=3306,
    user='root',
    passwd='',
    db='web_db',
    charset='utf8'
)
def cal_sub(s):
    print(s[0:-1])
    
    cursor = db.cursor()
    cursor.execute(f"select sum(price*num) from orders,goods where goods.goods_id = orders.goods_id and orders.order_id in ({s[0:-1]})")
    cursor.close()
    return cursor.fetchall()[0][0]
    
class User:
    username = ''
    passwd = ''
    sex = ''
    def __init__(self,name=None,pswd=None,sex=None):
        self.username = name
        self.passwd = pswd
        self.sex=sex
    def add_order(self,order_id):
        try:  # test pswd
            cursor = db.cursor()
            cursor.execute(f"update orders set num=num+1 where order_id = {order_id}")
            db.commit()
            cursor.close()
            return 1
        except:
            return 0

    def remove_order(self, order_id):
        try:  # test pswd
            cursor = db.cursor()
            cursor.execute(f"delete from orders where order_id = '{order_id}' ")
            cursor.close()
            return 1
        except:
            return -1

    def reduce_order(self, order_id):
        try:  # test pswd
            cursor = db.cursor()
           
            cursor.execute(f"update orders set num=num-1 where order_id = {order_id}")
            db.commit()
            cursor.close()
            return 1
        except:
            return 0

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

    def create_order(self, goods_id):
        try:  # test pswd
            cursor = db.cursor()
            cursor.execute(f"select user_id from user where username ='{self.username}' ")
            data1 = cursor.fetchall()
          
            
            cursor.close()
            user_id = data1[0][0]
            
            o = Order(user_id=user_id, goods_id=goods_id)
            o.update()
            return 1
        except:
            return -1


class Goods:
    id=None
    goods_name = None
    goods_nums = None
    price = None
    type = None
    photo = None
    def __init__(self,name = None,nums= 0,price = 99999,type = None,photo = None):
        self.goods_name=name
        self.id=None
        self.type=type
        self.goods_nums=int(nums)
        self.price=int(price)
        self.photo = photo
    def add_sql(self):
        try:
            cursor = db.cursor()
            cursor.execute(f"insert into goods values (NULL,'{self.goods_name}',{self.goods_nums},{self.price},'{self.type}','{ self.photo}')")
            db.commit()
            cursor.close()
            return 1
        except:
            return 0

    def del_sql(self):
        try:
            cursor = db.cursor()
            cursor.execute(f"delete from goods where goods_name='{self.goods_name}'")
            db.commit()
            cursor.close()
            return 1
        except:
            return 0
class Order:
    order_id=None
    goods_id=None
    user_id=None
    def __init__(self,order_id=None,goods_id=None,user_id=None):
        self.goods_id=goods_id
        self.order_id=order_id
        self.user_id=user_id
    def update(self):
        cursor = db.cursor()
        cursor.execute(f"select * from orders where user_id = {self.user_id} and goods_id = {self.goods_id}")
        data = cursor.fetchall()
        print(789)
        if len(data) == 0:
            
            cursor.execute(f"insert into orders (user_id,goods_id) values ('{self.user_id}','{self.goods_id}')")
        else:
            cursor.execute(f"update orders set  num = num + 1 where user_id = {self.user_id} and  goods_id = {self.goods_id}")
        
        db.commit()
        cursor.close()

   
        












            
        
    
            
        
        
