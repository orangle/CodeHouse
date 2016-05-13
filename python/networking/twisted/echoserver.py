#coding:utf-8
#orangleliu
#echoserver.py

from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocal(self, addr):
        return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()
