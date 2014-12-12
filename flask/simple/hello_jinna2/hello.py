#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: hello.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2014-12-12 17:54:11
############################
'''
.html files is in tmplates 文件夹,跟hello.py
同一级目录
'''
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
 
