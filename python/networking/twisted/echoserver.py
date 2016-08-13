#coding:utf-8
#orangleliu
#echoserver.py
import sys

from twisted.internet import protocol, reactor
from twisted.python import log

log.startLogging(sys.stdout)

class Echo(protocol.Protocol):
    def connectionMade(self):
        host = self.transport.getPeer().host
        port = self.transport.getPeer().port
        log.msg("conn client:%s prot:%s"%(host, port))

    def dataReceived(self, data):
        log.msg("client: %s"%data)
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    protocol = Echo

reactor.listenTCP(8000, EchoFactory())
reactor.run()
