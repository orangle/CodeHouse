#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: t_orderdict.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-11 11:53:14
#License: MIT
############################
'''
顺序不变的dict
'''

d = {}
d["a"] = "a"
d["b"] = "b"
d["c"] = "c"
print d 

from collections import OrderedDict
import json 

d = OrderedDict()
d["a"] = "a"
d["b"] = "b"
d["c"] = "c"
print d 
print json.dumps(d)
