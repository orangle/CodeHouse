#coding:utf-8
#monkey_pache.py

'''
python monkey patch

在运行的时候改变对象的属性
A MonkeyPatch is a piece of Python code which extends or modifies other code at runtime (typically at startup)
'''

import json

try:
    json.sayHello()   #没有这个属性
except Exception,e:
    print e.message
    pass 
    
def sayHello():
    print 'Hello json'
    
json.sayHello = sayHello #有了这个属性
json.sayHello()
