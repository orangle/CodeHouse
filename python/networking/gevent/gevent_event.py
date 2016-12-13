# -*- coding: utf-8 -*-
#orangleliu
#2015-07-16
import gevent
from gevent.event import Event

'''
也就是说wait可以手动把协程切走
set 把权限在交给wait的函数
主要用来做手动的切换
'''

evt = Event()

def setter():
    print "set start"
    gevent.sleep(3)
    print "ok set end"
    #这个set的作用是交出运行权，否则的话 wait就一直阻塞
    evt.set()


def waiter():
    print 'wait start'
    #这个把自己的权限切出去
    #wait阻塞在这里 等待set动作来激活wait，1秒之后还没有set来激活就直接执行了哈
    evt.wait(timeout=1)
    print 'wait end'


def main():
    gevent.joinall([
        gevent.spawn(setter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
        gevent.spawn(waiter)
    ])

if __name__ == '__main__':
    main()
