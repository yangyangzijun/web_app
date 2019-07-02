from werkzeug.utils import secure_filename
from flask import Flask, session,render_template, jsonify, request,redirect,escape,url_for
import time
import os
import base64
import psutil, time,json
import pymysql
import json
from redis import StrictRedis
from user import User,Goods

redis = StrictRedis(host='127.0.0.1', port=6379, db=0, password='')
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='web_db',
    charset='utf8'
)
from flask_cors import *



app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
CORS(app, supports_credentials=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
    if request.method=='POST':
        request_data = json.loads(request.data.decode('utf-8'))
        goods_name=request_data['goods_name']
        goods_nums = request_data['goods_nums']
        goods_price  = request_data['goods_price']
        goods_type = request_data['goods_type']
        goods = Goods(goods_name,goods_nums,goods_price,goods_type)
        if goods.add_sql()==0:
            return jsonify({'mess': 'error'})
        else:
            return jsonify({'mess': 'ok'})
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
        
        return  render_template('login.html')
    elif request.method=="POST":
        request_data = json.loads(request.data.decode('utf-8'))
        username = request_data['username']
        passwd = request_data['passwd']
        u = User(username,passwd)
        
        if u.test_password() == 1:
            session['username'] = u.username
            return jsonify({'mess':'ok'})
        elif u.test_password()==-1:
            return jsonify({'mess':'error'})
        else:
            return jsonify({'mess':'密码错误'})
            
        
@app.route('/logout')

def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
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
        
        if redis.hget('user', username) is not None:
            return jsonify({'mess':'用户名已存在'})
        if u.regist()==0:
            return jsonify({'mess': 'error'})
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
@cross_origin()
def js_test():
    

    return render_template('error.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
   



    

        
