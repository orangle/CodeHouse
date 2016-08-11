#coding:utf-8
'''
延迟执行
'''

from twisted.internet import reactor, defer

def add(x, y):
    d = defer.Deferred()
    reactor.callLater(2, d.callback, x+y)
    return d

def calback(value):
    print "callback value", value

d = add(1, 2)
d.addCallback(calback)

reactor.callLater(4, reactor.stop)
reactor.run()
