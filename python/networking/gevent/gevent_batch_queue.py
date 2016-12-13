# -*- coding: utf-8 -*-
# python2.7x
# author: orangelliu
# date: 2016-11-02
"""
模型
30s一次周期
一个线程获取数据，扔到queue中，其他线程做任务（io类型的任务, 出错了重试)

一个生产者 多个消费者的模型，收到关闭新信号生产者停止，然后给queue投毒
"""

import sys
import time
import logging
import gevent
from gevent.queue import Queue
from gevent import monkey

monkey.patch_all()

import urllib2

logger = logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 生产者产生的内容, 消费者就是抓取这些网页
plist = [
    'http://blog.csdn.net/orangleliu/article/details/52851122',
    'http://blog.csdn.net/orangleliu/article/details/52692999',
    'http://blog.csdn.net/orangleliu/article/details/52636842',
    'http://blog.csdn.net/orangleliu/article/details/52575369',
    'http://blog.csdn.net/orangleliu/article/details/52397384',
    'http://blog.csdn.net/orangleliu/article/details/52243749',
    'http://blog.csdn.net/orangleliu/article/details/52229817',
    'http://blog.csdn.net/orangleliu/article/details/52038092',
    'http://blog.csdn.net/orangleliu/article/details/51994513',
    'http://blog.csdn.net/orangleliu/article/details/51944758'
]

stop = False
tasks = Queue()
worknum = 3


def worker(name):
    # queue 不为空取值，取到了结束flag，自动结束
    print 'worker start ...'
    while not stop:
        t = tasks.get()
        if t == '##stop':
            break
        print 'worker {0} get {1}'.format(name, t)
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            r = opener.open(t)
            print 'worker {0}'.format(name) + r.read()[:40]
        except Exception as e:
            logger.error('worker urllib2 error', exc_info=True)
        gevent.sleep(0)
    print "worker exit"


def get_sms():
    global plist
    # lasttime = 0
    while not stop:
        # 采取自己计算时间的方法
        now = time.time()
        # if now - lasttime < 10:
        #     # 0.05 时候 cpu 的消耗在0.2左右
        #     gevent.sleep(10)
        #     continue

        print now, 'put tasks to queues, size', tasks.qsize()
        # lasttime = now
        for p in plist:
            tasks.put(p)
        gevent.sleep(30)
    else:
        print 'put stop flag to queue'
        for i in range(worknum):
            tasks.put_nowait('##stop')
        gevent.sleep(0)


gevent.joinall([gevent.spawn(worker, i) for i in range(worknum)] + [gevent.spawn(get_sms)])
