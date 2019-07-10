from werkzeug.utils import secure_filename
from flask import Flask, session,render_template, jsonify, request,redirect,escape,url_for
import os
from user import *
from red import *

import redis
re = redis.Redis(host='192.168.43.68', port=6379)

from flask_cors import *



app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
@app.route('/get_shop_num', methods=['GET', 'POST'])
def  shop_num():
    if 'username' in session:
        name = session["username"]
        s= f'select sum(orders.num) from user,orders where user.user_id= orders.user_id and username = "{ name }"'
        data = op_sql(s)
        print(data[0][0])
        return jsonify({"mess": "ok","num":str(data[0][0])})
    else:
        return jsonify({"mess":"请登录"})
@app.route('/get_test', methods=['GET', 'POST'])
def  mulp():
    if request.method == "POST":
        request_data = json.loads(request.data.decode('utf-8'))
        print(request_data['goods_id'])
        data=op_sql(f"select username,evalute,star_class,checked_orders.num from user,checked_orders where goods_id = {request_data['goods_id']} and checked_orders.user_id = user. user_id and checked_orders.received=2;")
        li = []
        for l in data:
            res = {'username': l[0], 'evalute': l[1], 'star_class': l[2], 'num': l[3]}
            li.append(res)
        result = {}
        result['data'] = li
        result['mess'] = 'ok'
        return jsonify(result)

@app.route('/pingjia', methods=['GET', 'POST'])
def  get_mess_with_pingjia():
    request_data = json.loads(request.data.decode('utf-8'))
    try:
        data = op_sql(
            f"select evalute,star_class  from checked_orders  where order_id  = {request_data['order_id']}")
        return jsonify({"mess": "ok", "data": data[0][0],"star_class":data[0][1]})
    except:
        return jsonify({"mess": "error", })
    pass
@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == "POST":
        if 'username' in session:
            request_data = json.loads(request.data.decode('utf-8'))
            try:
                op_sql(f"update checked_orders set evalute='{request_data['content']}',star_class ='{request_data['xingji']}',received = 2 where order_id= '{request_data['order_id']}'")
            except:
                print("添加出错")
            return jsonify({'mess': 'ok'})
        else:
            return jsonify({'mess': '请先登录'})

@app.route('/checked_orders',methods=['POST','GET'])
def checked_orders():
    if request.method=="GET":
        return render_template('checked_orders.html')
    else:
        data = json.loads(request.data.decode('utf-8'))
        data = data['order_id']
        s = f"update  checked_orders set received =1 where order_id  = {data} "
        try :
            op_sql(s)
            return  jsonify({"mess":"ok"})
        except:
            return  jsonify({"mess":"error"})

            
@app.route('/eva',methods=['POST','GET'])
def eva():
    return jsonify({'s':'s'})
        
@app.route('/pay',methods=['POST','GET'])
def pay():
    if "user_id" in session:
        a=session["user_id"]
        data = op_sql(f"select checked_orders.order_id,goods.main_pic_addr,goods"
                     f".goods_name,goods.price,checked_orders.num,checked_orders.received from checked_orders,"
                     f"user,goods where  user.user_id=checked_orders.user_id and checked_"
                     f"orders.goods_id=goods.goods_id  and user.user_id='{a }'")
        li = []
        for l in data:
            res = {'orders_id': l[0], 'main_pic_addr': 'static/' + l[1], 'goods_name': l[2], 'goods_price': l[3],
                   'order_num': l[4],'received':l[5]}
            li.append(res)
        result = {}
        result['data'] = li
        result['mess'] = 'ok'
        return jsonify(result)
        
    else:
        pass
@app.route('/cal_sub', methods=['POST', 'GET'])
def cal_su():
    if request.method=="GET":
        return render_template('lop.html')
    else:
        data = json.loads(request.data.decode('utf-8'))
        data = data['data']
        s=''
        for l in  data:
            
            s +=str(l)+','
        id = str(time.time() * 1000000)[0:-2]
        print(id)

        re.set(id,s[0:-1],600)
        return jsonify({"mess": buy(int(cal_sub(s)),id)})
      
      
@app.route('/get_details',methods=['GET','POST'])
def get_details():
    if(request.method == 'GET'):
        data = {}
        data['data'] =  request.args.get("goods_id")
        return render_template('goodsDetails.html',**data)
    else:
        data = json.loads(request.data.decode('utf-8'))
        data1=op_sql(f"select * from goods where goods_id = '{data['goods_id']}'")
        data2=op_sql(f"select pic_addr from pics where goods_id = '{data['goods_id']}'")
        
        res = {'goods_id': data1[0][0],'goods_name': data1[0][1] ,'price':data1[0][3],'type':data1[0][4]}
        rr=[]
        for l in data2:
            rr.append('static/'+l[0])
        res["photo"] = rr
        print(res['photo'])
        return jsonify(res)
    
    


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
CORS(app, supports_credentials=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/remove",methods= ['GET','POST'])
def remove():
    if 'username' in session:
        u = User(name=session['username'])
        request_data = json.loads(request.data.decode('utf-8'))
        u.remove_order(request_data['order_id'])
        return jsonify({'mess': 'ok'})
    else:
        return jsonify({'mess': '请先登录'})
@app.route('/shoopping_cart',methods=['GET','POST'])
def shoopping_cart():
    if request.method=="POST":
        if 'username' in session:
            u=User(name=session['username'])
            request_data = json.loads(request.data.decode('utf-8'))
            if request_data['op'] == 'minus':
                if u.reduce_order(request_data['order_id'])==1:
                    return jsonify({'mess':'ok'})
                else:
                    return jsonify({'mess':'error'})
            elif request_data['op'] == 'plus':
                if u.add_order(request_data['order_id'])==1:
                    return jsonify({'mess':'ok'})
                else:
                    return jsonify({'mess':'error'})
                
        else:
            return jsonify({'mess':'请先登录'})

@app.route('/test',methods=['GET','POST'])
def test():
    if request.method=='GET':
        return render_template('admin.html')
    else:
        if 'username' in session:
            cursor = db.cursor()
            cursor.execute(
                f"select orders.order_id,goods.main_pic_addr,goods.goods_name,goods.price,orders.num from orders,user,goods where"
                f" user.user_id=orders.user_id and orders.goods_id=goods.goods_id  and user.username='{session['username']}'")
            cursor.close()
            data = cursor.fetchall()
            li = []
            for l in data:
                res = {'orders_id': l[0], 'main_pic_addr': 'static/' + l[1], 'goods_name': l[2], 'goods_price': l[3],
                       'order_num': l[4]}
                li.append(res)
            result = {}
            result['data'] = li
            result['mess'] = 'ok'
            return jsonify(result)
        else:
            return jsonify({'mess': '请先登录'})
        
    
@app.route('/create_order',methods=['GET','POST'])

def create_order():
    if request.method=="POST":
        if 'username' in session:
            print(session['username'])
            u=User(name=session['username'])
            request_data = json.loads(request.data.decode('utf-8'))
            u.create_order(request_data['goods_id'])
            return jsonify({"mess":"ok"})
        else:
            return jsonify({'mess':'请先登录'})

    
@app.route('/list_goods',methods=['GET','POST'])
def list_goods():
    cursor = db.cursor()
    cursor.execute(f"select * from goods")
    cursor.close()
    data = cursor.fetchall()
    
    res = {}
    li = []
    for l in data:
        res = {'goods_id'   : l[0], 'goods_name': l[1], 'goods_nums': l[2], 'goods_price': l[3], 'goods_type': l[4],
               'goods_photo': 'static/' + str(l[5])}
        li.append(res)
    
    result = {}
    result['data']=li
    result['mess']='ok'
    return jsonify(result)

@app.route('/add_goods_photo',methods=['GET','POST'])
def add_goods_photo():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(request.form['goods_name'])
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        token = (new_filename)
        
        
        return jsonify({"errno": 0, "errmsg": "上传成功", "token": token})
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})


@app.route('/add_goods',methods=['GET','POST'])
def add_goods():
    if request.method=="GET":
        return  render_template('add_goods.html')
    else:
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
        goods_name = request.form['goods_name']
        goods_nums = int(request.form['goods_nums'])
        goods_price = int(request.form['goods_price'])
        goods_type = request.form['goods_type']
        pic_list = []
        pic_num = int(request.form['length'])
        for l in range(0,pic_num):
            pic_list.append(request.files[str(l)])
        
        #main_pic_addr = request.form['myfile'].filename
        try:
            if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
                fname = secure_filename(f.filename)
                ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
                unix_time = int(time.time())
                new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
                f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
                goods = Goods(goods_name, goods_nums, goods_price, goods_type, new_filename)
                flag = goods.add_sql()
                print(flag)
                if flag==0:
                    return jsonify({'mess': 'error'})
                else:
                    print((pic_list[0].filename))
                    try:
                        
                        for l in pic_list:
                            
                            fname = secure_filename(l.filename)
                            ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
                            unix_time = int(time.time()*100000)
                            new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
                            l.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
                            op_sql(f"insert into pics(goods_id,pic_addr) v"
                                   f"alue ('{flag}','{new_filename}')")
                        return jsonify({'mess': 'ok'})
                    except:
                        return  jsonify({'mess':'次要图片上传错误'})
            else:
                return jsonify({"errno": 1001, "errmsg": "上传失败"})
        except:
            return jsonify({"errno": 1001, "errmsg": "文件类型错误"})


    
    
@app.route('/del_goods',methods=['GET','POST'])
def del_goods():
    if request.method=="GET":
        return  render_template('del_goods.html')
    if request.method=='POST':
        request_data = json.loads(request.data.decode('utf-8'))
        goods_name=request_data['goods_name']
        goods = Goods(goods_name)
        if goods.del_sql()==0:
            return jsonify({'mess': 'error'})
        else:
            return jsonify({'mess': 'ok'})
        
@app.route('/check_login',methods=['GET','POST'])
def check_login():
    if 'username' in session:
        return jsonify({'mess':'ok','username':session['username']})
    else:
        return jsonify({'mess':'error'})
    
@app.route('/',methods=['GET'])
def index():
    if request.method=='GET':
        return  render_template('home.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="GET":
        
        return  render_template('login (1).html')
    elif request.method=="POST":
        request_data = json.loads(request.data.decode('utf-8'))
        username = request_data['username']
        passwd = request_data['passwd']
        u = User(username,passwd)
        
        if u.test_password() == 1:
            session['username'] = u.username
            
            return jsonify({'mess':'ok'})
        elif u.test_password()==-1:
            print(session["user_id"])
            return jsonify({'mess':'error'})
        else:
            return jsonify({'mess':'密码错误'})
            
        
@app.route('/logout')

def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop("user_id",None)
    return redirect(url_for('index'))
@app.route('/regrist',methods=['POST',"GET"])

def regeist():
    # remove the username from the session if it's there
    if request.method=="GET":
        return render_template('register.html')
    if request.method =="POST":
        request_data = json.loads(request.data.decode('utf-8'))
        username = request_data['username']
        password = request_data['passwd']
        sex = request_data['sex']
        u = User(username,password,sex)
        
        if u.regist()==0:
            return jsonify({'mess': '用户名已存在'})
        else:
           
            return jsonify({'mess':'ok'})
      
            
@app.route('/admin',methods=['POST',"GET"])

def admin():
    
        cursor = db.cursor()
        cursor.execute(f"select * from user_table")
        cursor.close()
        cursor.close()
        data = cursor.fetchall()
        res={}
        res['data']=data
      
        return render_template('admin.html',res=res)
@app.route('/to',methods=['GET','POST'])
def po():
    return "pl"
@app.route('/js_test',methods=['POST',"GET"])
def js_test():
    data  = request.form
    d = {}
    for l in data:
        d[str(l)]=data[str(l)]
  
    check(d)
    print(d["out_trade_no"])
    s = re.get(d["out_trade_no"]).decode('utf-8')
   
    try :
        a=f'insert into checked_orders  (user_id,goods_id,num)  (select user_id,goods_id,num from orders where order_id in ({ s } ))'
        op_sql(  a)
        b=f'delete from orders where order_id in ({ s }) '
        op_sql(b)
        print('ok')
    except:
        print('error')
    
    
    

    return "success"
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
   



    

    
