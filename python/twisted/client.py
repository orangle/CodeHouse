#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: mandela_ssl_client.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-01-21 20:13:16
############################
import json
import os 

from twisted.internet import  reactor
from twisted.internet.protocol import ClientFactory, Protocol

class Ap(Protocol):
    def connectionMade(self):
        self.messageCount = 0
        pid = os.getpid()
        self.factory.n += 1
        self.name = "Client %s"%self.factory.n
        data = {"No":self.name,"func":"login","user":"u-%s"%pid,"para":{"mac":"2c:67:fb:aa:2b:1f","hostname":"TH-NC-1205-92","tqisfull":0}}
        self.transport.write(json.dumps(data))
        reactor.callLater(0.5, self.sendMessage, "Message %d"%self.messageCount)

    def connectionLost(self, reason):
        #print "connection lost"
        pass

    def dataReceived(self, data):
        print data

    def sendMessage(self, msg):
        if self.factory.stop:
            self.transport.loseConnection()
        else:
            self.messageCount += 1
            reactor.callLater(0.5, self.sendMessage, "Message %d"%self.messageCount)
       
class ApFactory(ClientFactory):
    protocol = Ap

    def __init__(self):
        self.n = 0
        self.stop = False

    def stopTest(self):
        self.stop = True

    def clientConnectionFailed(self, connector, reason):
        print "connection failed, bye"

    def clientConnectionLost(self, connector, reason):
        print "connection lost, bye!"

if __name__ == '__main__':
    '''
    模拟多个客户端并发连接twisted服务端,多线程模拟多个reactor来并发连接服务器端
    '''
    factory = ApFactory()
    num = 100
    for i in range(num):
        reactor.connectTCP('localhost', 9344, factory)

    reactor.callLater(10, factory.stopTest)
    reactor.run()

