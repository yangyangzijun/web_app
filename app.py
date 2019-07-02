from werkzeug.utils import secure_filename
from flask import Flask, session,render_template, jsonify, request,redirect,escape,url_for
import time
import os
import base64
import psutil, time,json
import pymysql
import json
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
@app.route('/',methods=['GET'])
def index():
    if 'username' in session:
        return session['username']
    else:
        return 'false'
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="GET":
        
        return  render_template('login.html')
    elif request.method=="POST":
        request_data=request.data.decode('utf-8')
        username = json.loads(request_data)['username']
        passwd = json.loads(request_data)['passwd']
        try:
            cursor = db.cursor()
            cursor.execute(f"select password from user where username ='{username}'")
            data=cursor.fetchall()
            cursor.close()
            if passwd==str(data[0][0]):
                session['username'] = username
                return jsonify({'mess': 'ok'})
            else:
                return jsonify({ 'mess': '密码错误'})
        except:
            return jsonify({'mess': '用户名不存在'})
            
        
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
        try:
            cursor = db.cursor()
            cursor.execute(f"insert into user values (NULL,'{username}','{password}','{sex}')")
            db.commit()
            cursor.close()
            
            return  jsonify({'mess':'ok'})
        except:
            return  jsonify({'mess':'error'})
            
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
    

    
    cursor = db.cursor()
    cursor.execute(f"select * from user_table")
    cursor.close()
    cursor.close()
    data = cursor.fetchall()
    res = {}
    res['data'] = data
    
    return "successCallback" + "(" + json.dumps(res) + ")"
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
   



    

        
