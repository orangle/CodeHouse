#!/usr/bin/python
# -*- coding: utf-8 -*-
# python2.7x
# author: orangelliu
# date: 2014-08-20

'''
线程本地变量  初始值定义之后，在线程中可以保持隔离性
为了做对比，分别和全局变量，gevent线程对比

全局变量
'''
from time import sleep
from random import random
from threading import Thread, local

#如果使用全局变量呢
def bar1():
    global v
    print 'calledddddd from %s'%v

def foo1():
    global v
    v = v + '.....'
    bar1()

class T1(Thread):
    def run(self):
        global v
        sleep(random())
        v =self.getName()
        sleep(1)
        foo1()

T1().start()
T1().start()
