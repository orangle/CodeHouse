#coding:utf-8
"""
local proxy
client -tcp-> LISTEN_PORT (twisted)-> RMOTE(SERVER_ADDR)

testing step

WINDOW1
>>> python echoserver.py

WINDOW2
>>> python tcp_proxy.py


WINDOW3

liuzhizhi@lzz-rmbp|githouse # telnet localhost 8001
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
echo
echo
Connection closed by foreign host.
"""

LISTEN_PORT = 8001
SERVER_PORT = 8000
SERVER_ADDR = "localhost"

import sys
from twisted.internet import protocol, reactor
from twisted.python import log


log.startLogging(sys.stdout)

# Adapted from http://stackoverflow.com/a/15645169/221061
class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None
        self.port = None
        self.host = None

    def connectionMade(self):
        self.host = self.transport.getPeer().host
        self.port = self.transport.getPeer().port
        log.msg("conn client:%s prot:%s"%(self.host, self.port))
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self
        reactor.connectTCP(SERVER_ADDR, SERVER_PORT, factory)

    # Client => Proxy
    def dataReceived(self, data):
        log.msg("%s:%s to server->%s"%(self.host, self.port, data))
        if self.client:
            self.client.write(data)
        else:
            self.buffer = data

    # Proxy => Client
    def write(self, data):
        self.transport.write(data)


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    # Server => Proxy
    def dataReceived(self, data):
        self.factory.server.write(data)

    # Proxy => Server
    def write(self, data):
        if data:
            self.transport.write(data)


def main():
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()
