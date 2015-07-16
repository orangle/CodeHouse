# -*- coding: utf-8 -*-
#orangleliu
#2015-07-15

#最基础的例子，gevent是通过yield来进行 阻塞时自动切换的

import gevent

def f1():
    print 'runing f1 start'
    #gevent.sleep(0)
    print 'runing f1 end'

def f2():
    print 'runing f2 start'
    #gevent.sleep(0)
    print 'runing f2 end'

gevent.joinall([
    gevent.spawn(f1),
    gevent.spawn(f2)
])

'''
上面的例子就是用 sleep来模拟阻塞，如果没有这个明确的sleep
gevent不会自动切换

如果某些阻塞gevent无法自动识别，我们可以自己添加一个sleep来
让他自动切换出去
'''
