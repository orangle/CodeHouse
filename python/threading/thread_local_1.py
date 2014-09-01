#!/usr/bin/python
# -*- coding: utf-8 -*-
# python2.7x
# author: orangelliu
# date: 2014-08-20

'''
线程本地变量  初始值定义之后，在线程中可以保持隔离性
为了做对比，分别和全局变量，gevent线程对比

线程局部变量
'''

from time import sleep
from random import random
from threading import Thread, local

data = local()

def bar():
    print 'called from %s'%data.v

def foo():
    data.v = str(data.v) + '.......'
    bar()

class T(Thread):
    def run(self):
        sleep(random())
        data.v = self.getName()
        sleep(1)
        foo()

T().start()
T().start()



