#coding:utf-8
#python epoll level-triggered example

'''
rps 20 会有错
水平触发是多次通知，所以个请求的数据接受或者是发送可以在多个时间中进行，因为一次
时间没有操作完，还会继续通知
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
ss.setblocking(0) #默认是阻塞方式，这里一定要设置下

epoll = select.epoll()
epoll.register(ss.fileno(), select.EPOLLIN)

try:
    connections = {}; requests = {}; responses = {}
    while True:
        events = epoll.poll(1) #1秒以内如果有时间发生，会立刻返回
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
                    print '-'*40 + '\n' + requests[fileno].decode()[:-2]
            elif event & select.EPOLLOUT:
                bytesw = connections[fileno].send(responses[fileno])
                if bytesw > 0: print bytesw
                responses[fileno] = responses[fileno][bytesw:]
                if len(responses[fileno]) == 0:
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
