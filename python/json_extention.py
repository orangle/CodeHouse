﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
#json_extention
#2014-03-16
#copyright: orangleliu
#license: BSD

'''
python中dumps方法很好用，可以直接把我们的dict直接序列化为json对象
但是有的时候我们加了一些自定义的类就没法序列化了，这个时候需要
自定义一些序列化方法

参考：
http://docs.python.org/2.7/library/json.html

例如:
In [3]: from datetime import  datetime

In [4]: json_1 = {'num':1112, 'date':datetime.now()}

In [5]: import json

In [6]: json.dumps(json_1)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
D:\devsofts\python2.7\lib\site-packages\django\core\management\commands\shell.py
c in <module>()
----> 1 json.dumps(json_1)

TypeError: datetime.datetime(2014, 3, 16, 13, 47, 37, 353000) is not JSON serial
izable
'''

from datetime import datetime
import json

class DateEncoder(json.JSONEncoder ):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)

json_1 = {'num':1112, 'date':datetime.now()}
print json.dumps(json_1, cls=DateEncoder)

'''
输出结果：

PS D:\code\python\python_abc> python .\json_extention.py
{"date": "2014-03-16 13:56:39.003000", "num": 1112}
'''

#我们自定义一个类试试
class User(object):
   def __init__(self, name):
        self.name = name

class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.name
        return json.JSONEncoder.default(self, obj)

json_2 = {'user':User('orangle')}
print json.dumps(json_2, cls=UserEncoder)

'''
PS D:\code\python\python_abc> python .\json_extention.py
{"date": "2014-03-16 14:01:46.738000", "num": 1112}
{"user": "orangle"}

'''



