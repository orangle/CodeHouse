#coding:utf-8
#python epoll edge-triggered example

'''
rps 20多 会有错
边缘触发对于一个读写只有一次通知，所以一次读写要在一个事件通知中完成，或者自己协调逻辑，否则
可能会造成程序错误
'''

import socket, select

EOL1 = '\n\n'
EOL2 = '\n\r\n'

response = "HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 2016 18:05:30 GMT\r\n"
response += "Content-Type: text/palin\r\nContent-Length: 13\r\n\r\n"
response += "Hello, world\n"

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ss.bind(('0.0.0.0', 9999))
ss.listen(1)
ss.setblocking(0)

epoll = select.epoll()
epoll.register(ss.fileno(), select.EPOLLIN|select.EPOLLET)

try:
    connections = {}; requests = {}; responses = {}
    while True:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == ss.fileno():
                try:
                    while True:
                        connection, address = ss.accept()
                        connection.setblocking(0)
                        epoll.register(connection.fileno(), select.EPOLLIN|select.EPOLLET)
                        requests[connection.fileno()] = ''
                        connections[connection.fileno()] = connection
                        responses[connection.fileno()] = response
                except socket.error:
                    pass

            elif event & select.EPOLLIN:
                try:
                    while True:
                        requests[fileno] += connections[fileno].recv(1024)
                except socket.error:
                    pass

                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                    epoll.modify(fileno, select.EPOLLOUT|select.EPOLLET)
                    print '-'*40 + '\n' + requests[fileno].decode()[:-2]
            elif event & select.EPOLLOUT:
                try:
                    while len(responses[fileno]) > 0:
                        bytesw = connections[fileno].send(responses[fileno])
                        responses[fileno] = responses[fileno][bytesw:]
                except socket.error:
                    pass

                if len(responses[fileno]) == 0:
                    epoll.modify(fileno, select.EPOLLET)
                    connections[fileno].shutdown(socket.SHUT_RDWR)
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
finally:
    epoll.unregister(ss.fileno())
    epoll.close()
    ss.close()
