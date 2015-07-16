# -*- coding: utf-8 -*-
#orangleliu
#2015-07-15

'''
在非阻塞这个名字出现的时候，我们经常会想到的就是 select模型

可能在socket 网络io模型中使用的最多，其实也可以做事件的调度
'''

import time
import gevent
from gevent import select

start = time.time()
tic = lambda: 'at %1.1f seconds '%(time.time() - start)

def gr1():
    print 'start polling 1 %s'%tic()
    select.select([], [], [], 2)
    print 'end polling  1 %s'%tic()

def gr2():
    print 'start polling  2 %s'%tic()
    select.select([], [], [], 2)
    print 'end polling 2 %s'%tic()

def gr3():
    print 'sleep 2, %s'%tic()
    gevent.sleep(2)

gevent.joinall([
    gevent.spawn(gr1),
    gevent.spawn(gr2),
    gevent.spawn(gr3)
])
