#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: spl_4.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-13 15:36:02
############################
'''
加上异常处理，算是比较完整的小案例
'''
from twisted.internet import defer, reactor
from twisted.web.client import getPage

urls = [
    'http://www.orangleliu.info',
    'http://blog.csdn.net/orangleliu',
    'http://cafe.orangleliu.info',
    'http://www.so.com.cn']

def pageCallback(result, url):
    data = {
            'length': len(result),
            'content': result[:20],
            'url': url,
            }
    return data 

def pageErrback(error, url):
    return {
        'msg': error.getErrorMessage(),
        'err': error,
        'url': url
        }

def getPageData(url):
    d = getPage(url, timeout=15)
    d.addCallback(pageCallback, url)
    d.addErrback(pageErrback, url)
    return d 

def listCallback(result):
    for ignore, data in result:
        if data.has_key('err'):
            print "failed--> %s"%str(data)
        else:
            print "successed--> %s"%str(data)

def finish(ign):
    reactor.stop()

def test():
    defereds = []
    for url in urls:
        d = getPageData(url)
        defereds.append(d)
    dl = defer.DeferredList(defereds, consumeErrors=1)
    dl.addCallback(listCallback)
    dl.addCallback(finish)

test()
reactor.run()








