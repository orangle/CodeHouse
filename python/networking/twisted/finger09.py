# coding:utf-8
# Read username, output from factory interfacing to OS, drop connections

from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import basic

class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        d = self.factory.getUser(user)

        def onError(err):
            return 'Internal error in server'
        d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(message + '\r\n')
            self.transport.loseConnection()
        d.addCallback(writeResponse)

class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol

    def getUser(self, user):
        """给出一个命令行，获取名字
        """
        return utils.getProcessOutput("finger", [user])

reactor.listenTCP(8879, FingerFactory())
reactor.run()
