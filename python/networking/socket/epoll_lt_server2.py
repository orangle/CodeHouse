#coding:utf-8
#增加了监听队列长队，对客户端的tcp设置了TCP_CORK
#rps 100左右 无错误

import socket, select

EOL1 = '\n\n'
EOL2 = '\n\r\n'

response = "HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 2016 18:05:30 GMT\r\n"
response += "Content-Type: text/palin\r\nContent-Length: 13\r\n\r\n"
response += "Hello, world\n"

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ss.bind(('0.0.0.0', 9999))
ss.listen(100)  #增加backlog长度
ss.setblocking(0)
#实时应用可以开启
#ss.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

epoll = select.epoll()
epoll.register(ss.fileno(), select.EPOLLIN)

try:
    connections = {}; requests = {}; responses = {}
    while True:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == ss.fileno():
                connection, address = ss.accept()
                connection.setblocking(0)
                epoll.register(connection.fileno(), select.EPOLLIN)
                requests[connection.fileno()] = ''
                connections[connection.fileno()] = connection
                responses[connection.fileno()] = response
            elif event & select.EPOLLIN:
                requests[fileno] += connections[fileno].recv(1024)
                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                    epoll.modify(fileno, select.EPOLLOUT)
                    connections[fileno].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 1)
                    print '-'*40 + '\n' + requests[fileno].decode()[:-2]
            elif event & select.EPOLLOUT:
                bytesw = connections[fileno].send(responses[fileno])
                if bytesw > 0: print bytesw
                responses[fileno] = responses[fileno][bytesw:]
                if len(responses[fileno]) == 0:
                    connections[fileno].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                    epoll.modify(fileno, 0)
                    connections[fileno].shutdown(socket.SHUT_RDWR)
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
finally:
    epoll.unregister(ss.fileno())
    epoll.close()
    ss.close()
