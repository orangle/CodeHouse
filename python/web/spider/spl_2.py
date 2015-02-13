#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: spl_2.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-11 16:34:55
############################

'''
twisted spider learn 2
这里相比1，在获取网页的时候增加了callback
把更多的过程异步话
'''

from twisted.internet import defer, reactor
from twisted.web.client import getPage

def pageCallback(result):
    data = {
            'length': len(result),
            'content': result[:100]
        }
    return data

def listCallback(result):
    for issuccess, data in result:
        if issuccess:
            print "Success %s"%(data)

def finish(ing):
    reactor.stop()

def test():
    d1 = getPage('http://www.orangleliu.info')
    d1.addCallback(pageCallback)
    d2 = getPage('http://blog.csdn.net/orangleliu')
    d2.addCallback(pageCallback)

    d3 = defer.DeferredList([d1, d2])
    d3.addCallback(listCallback)
    d3.addCallback(finish)

test()
reactor.run()


