#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: spl_6.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-13 16:44:08
############################
'''
还是调度问题，不一次产生所有的defer，而是产生一部分然后在消费一部分
'''

from twisted.internet import defer, reactor, task 
from twisted.web.client import getPage

urls = [
        'http://www.orangleliu.info',
        'http://cafe.orangleliu.info',
        'http://www.baidu.com'
    ]

maxRun = 2

def pageCallback(results):
    print len(results)
    return results

def doWork():
    for url in urls:
        d = getPage(url)
        d.addCallback(pageCallback)
        yield d

def finish(ign):
    reactor.stop()

def test():
    deferreds = []
    coop = task.Cooperator()
    work = doWork()
    for i in xrange(maxRun):
        d = coop.coiterate(work)
        deferreds.append(d)
    dl = defer.DeferredList(deferreds)
    dl.addCallback(finish)

test()
reactor.run()

