#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: spl_1.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-11 15:46:57
############################

'''
twisted spider startup 1
print the page length
refer: technicae.cogitat.io
'''

from twisted.internet import defer, reactor
from twisted.web.client import getPage

def listCallback(result):
    for x,y in result:
        if x==True:
            print "page length is %s"%len(y) 

def finish(ign):
    reactor.stop()

def test():
    d1 = getPage('http://www.orangleliu.info/')
    d2 = getPage('http://blog.csdn.net/orangleliu/')
    d3 = defer.DeferredList([d1, d2])
    d3.addCallback(listCallback)
    d3.addCallback(finish)

test()
reactor.run()

