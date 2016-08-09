from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols import basic 
import json

user_tasks = {}

class WifiProtocol(Protocol):
    MAX_LENGTH = 999999

    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        print "Client: %s length: %s"%(data, len(data))
        data_dic = json.loads(data)
        client = data_dic.get("user", "nobody")
        res = "You login times is "
        num = user_tasks.get(client, 0) + 1
        user_tasks[client] = num
        self.transport.write(res+str(num))

if __name__ == '__main__':
    from twisted.internet import ssl
    factory = Factory()
    factory.protocol = WifiProtocol
    reactor.listenSSL(9344, factory,
                      ssl.DefaultOpenSSLContextFactory(
            'keys/privkey.pem', 'keys/CAcert.pem'))
    print 'tserver start ok 9344'
    reactor.run()
