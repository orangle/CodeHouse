#coding:utf-8
from twisted.internet import defer, reactor
from twisted.application import service, internet
from mrpc import JSONRPCServerFactory, Handler, exportRPC


class Example(Handler):
    def __init__(self, who):
        self.who = who

    @exportRPC("add")
    @defer.inlineCallbacks
    def _add(self, x, y):
        yield
        defer.returnValue(x+y)

    @exportRPC()
    def login(self, **kwargs):
        return self.who

factory = JSONRPCServerFactory(seperator="")
factory.addHandler(Example('foo'), namespace='')

#application = service.Application("Example JSON-RPC Server")
#jsonrpcServer = internet.TCPServer(7080, factory)
#jsonrpcServer.setServiceParent(application)
reactor.listenTCP(9344, factory)
print "start"
reactor.run()
