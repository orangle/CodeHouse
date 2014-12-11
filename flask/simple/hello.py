#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-25
#hello.py
'''
单个文件的flask小项目
'''
from flask import Flask
app = Flask(__name__)

#访问根目录，显示你好
@app.route("/")
def index():
    return '<h1> Hi  Flask</h1>'

#路由中可以自动正则匹配出值，对于restful应用很友好
@app.route("/user/<name>")
def user(name):
    return 'Hello %s'%name

if __name__ == '__main__':
    #开发时候使用debug模式，方面调试
    app.run(debug=True)

'''
(flask) PS D:\CodeHouse\flask\simple> python hello.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader

'''
