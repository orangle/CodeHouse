#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: spl_5.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-13 16:21:39
############################
'''
这里是对前面一个例子的优化，当我们一次访问太多的url的时候可能会导致网络不好使，或者对方封IP
为了让同一时间执行url访问得到限制，需要添加一个控制器，defer一次生成玩之后，同时只能执行指定
数目的defer
'''
from twisted.internet import defer, reactor
from twisted.web.client import getPage

maxRun = 2

urls = [
        'http://www.baidu.com',
        'http://www.google.com',
        'http://www.github.com'
    ]

def listCallback(results):
    print len(results) 

def finish(ign):
    reactor.stop()

def test():
    deferreds = []
    sem = defer.DeferredSemaphore(maxRun)
    for url in urls:
        d = sem.run(getPage, url)
        deferreds.append(d)
    dl = defer.DeferredList(deferreds)
    dl.addCallback(listCallback)
    dl.addCallback(finish)

test()
reactor.run()

