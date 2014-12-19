#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-17
#template_jijia2
'''
模板的简单使用和熟悉
'''
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    '''
    测试下jinja2 模板常用的变量表示方式
    '''
    mydict = {"name": "orangleliu"}
    mylist =  ["apple", "orange", "banana"]
    class myobj:
        def sayhello(self):
            return "yes I am a method!"
    #这里使用了一个 flask-bootstrap 来做为模板基本风格
    return render_template('index.html', mydict=mydict, mylist=mylist,\
                    myobj=myobj)

if __name__=="__main__":
    app.run(debug=True)
