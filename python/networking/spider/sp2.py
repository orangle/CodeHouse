#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: sp2.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-10 16:31:00
############################
'''
twisted 基础爬虫，直接并发问题挺多
主要还是请求的定制，应答的处理
'''

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol 

class ResponseHandler(Protocol):
    def __init__(self, finished):
        self.finished = finished 
        #self.remaining = 1024 * 100

    def dataReceived(self, bytes):
        #if self.remaining:
        #    display = bytes[:self.remaining]
        #    print 'length:%s'%len(display)
        #    self.remaining -= len(display)
        print "length:%s"%len(bytes)

    def connectionLost(self, reason):
        print 'Finished receiving body: ', reason.getErrorMessage()
        self.finished.callback(None)

def rResponse(rep):
    print "Response code ",rep.code
    de = Deferred()
    rep.deliverBody(ResponseHandler(de))
    return de

def rShutDown(ingored):
    reactor.stop()

agent = Agent(reactor)
d = agent.request(
        'GET',
        'http://blog.csdn.net/orangleliu',
        Headers({'User-Agent': ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"]}),
        None)
d.addCallback(rResponse)
d.addBoth(rShutDown)
reactor.run()


