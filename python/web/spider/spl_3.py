#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: spl_3.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-13 14:54:28
############################
'''
对twisted 获取网页的方法进行封装，使得回调中有更多可以利用的参数
'''

from twisted.internet import defer, reactor
from twisted.web.client import getPage

def pageCallback(result, url):
    data = {
            'length': len(result),
            'content' : result[:10],
            'url':url}
    return data 

def getPageData(url):
    d = getPage(url)
    d.addCallback(pageCallback, url)
    return d

def listCallback(result):
    for isSuccess, data in result:
        if isSuccess:
            print "success: %s"%str(data)

def finish(ign):
    reactor.stop()

def test():
    urls = ["http://www.orangleliu.info",
        "http://blog.csdn.net/orangleliu" ]
    i = 1
    dl = []
    for url in urls:
        exec("d%s = getPageData('%s')"%(i, url))
        dl.append(eval("d%s"%i))
        i += 1

    d = defer.DeferredList(dl)
    d.addCallback(listCallback)
    d.addCallback(finish)

test()
reactor.run()






    

