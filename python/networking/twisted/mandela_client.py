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

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.policies import TimeoutMixin
#from twisted.internet import ssl

class Ap(Protocol, TimeoutMixin):
    def connectionMade(self):
        print "I made a connection"
        pid = os.getpid()
        data = {"func":"login","user":"u-%s"%pid,"para":{"mac":"2c:67:fb:aa:2b:1f","hostname":"TH-NC-1205-92","tqisfull":0}}
        #data ={"func":"startup","para":{"mac":"00:50:56:c0:00:08", "hostname":"BJ-1111-2222", "dtype":"wifi", "sversion":"1.1", "fversion":"33.4",
        #         "ssid": "eryawifi"}}
        self.transport.write(json.dumps(data))
        #self.transport.loseConnection()
        self.setTimeout(1);

    def dataReceived(self, data):
        print "Server said:", data

    def timeoutConnection(self):
        print "timeout"
        self.transport.abortConnection()

class ApFactory(ClientFactory):
    protocol = Ap

    def clientConnectionFailed(self, connector, reason):
        print "connection failed, bye"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "connection lost, bye!"
        reactor.stop()

    def buildProtocol(self, addr):
        return self.protocol()


if __name__ == '__main__':
    '''
    factory = ApFactory()
    reactor.connectSSL('localhost', 9344, factory, ssl.ClientContextFactory())
    reactor.run()
    '''
    reactor.connectTCP("localhost", 9344 , ApFactory())
    reactor.run()



