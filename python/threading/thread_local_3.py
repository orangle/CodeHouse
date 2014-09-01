#!/usr/bin/python
# -*- coding: utf-8 -*-
# python2.7x
# author: orangelliu
# date: 2014-08-20

'''
线程本地变量  初始值定义之后，在线程中可以保持隔离性
为了做对比，分别和全局变量，gevent线程对比

gevent 协程
'''

import gevent
from gevent.local import local

data = local()

def bar():
    print 'called from %s'%data.v

def foo(v):
    data.v = v
    data.v = str(data.v) + '.......'
    bar()

g1 = gevent.spawn(foo, '1')
g2 = gevent.spawn(foo, '2')

gevent.joinall([g1, g2])


