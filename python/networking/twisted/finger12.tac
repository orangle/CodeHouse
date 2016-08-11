#coding:utf-8
# But let's try and fix setting away messages, shall we?
from twisted.application import internet, service
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
        return defer.succeed(self.users.get(user, "No such user"))


# 用来设置用户的状态
class FingerSetterProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.lines = []

    def lineReceived(self, line):
        # 输入2行，一个用户名，一个是状态
        self.lines.append(line)

    def connectionLost(self, reason):
        user = self.lines[0]
        status = self.lines[1]
        self.factory.setUser(user, status)

class FingerSetterFactory(protocol.ServerFactory):
    protocol = FingerSetterProtocol

    def __init__(self, fingerFactory):
        self.fingerFactory = fingerFactory

    def setUser(self, user, status):
        self.fingerFactory.users[user] = status

ff = FingerFactory(sweet='Happy and well')
fsf = FingerSetterFactory(ff)

application = service.Application('finger', uid=1, gid=1)
serviceCollection = service.IServiceCollection(application)

internet.TCPServer(8879,ff).setServiceParent(serviceCollection)
internet.TCPServer(8888,fsf).setServiceParent(serviceCollection)


'''
(pylearn)liuzhizhi@lzz-rmbp|twisted # sudo twistd -ny finger12.tac

pylearn)liuzhizhi@lzz-rmbp|twisted # telnet localhost 8888
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
lzz
yes
^C^]
telnet> q
Connection closed.

(pylearn)liuzhizhi@lzz-rmbp|twisted # telnet localhost 8879
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
lzz
yes
Connection closed by foreign host.
'''
