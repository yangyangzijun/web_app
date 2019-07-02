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
CORS(app, supports_credentials=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
   



    

        
