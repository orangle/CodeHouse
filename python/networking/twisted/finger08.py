# coding:utf-8
# https://twistedmatrix.com/documents/current/core/howto/tutorial/intro.html
# Read username, output from non-empty factory, drop connections
# Use deferreds, to minimize synchronicity assumptions

from twisted.internet import protocol, reactor, defer
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

    def __init__(self, **kwargs):
        self.users = kwargs

    def getUser(self, user):
        """这里的user get是内存操作，马上就能得到结果，可以不用 defer
        但是如果是远程调用的操作，defer就会完成异步的调用
        """
        return defer.succeed(self.users.get(user, "No such user"))

reactor.listenTCP(8879, FingerFactory(moshez='Happy and well'))
reactor.run()
