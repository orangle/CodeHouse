#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: select_server.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-04-02 16:14:41
#License: MIT
############################
'''
使用select模型，处理并发连接
'''

import select 
import socket
import sys
import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_addr = ("localhost", 8889)
print >>sys.stderr, 'startup server %s on port %s'%server_addr
server.bind(server_addr)

server.listen(10)

inputs = [ server ]
outputs = []
message_queues = {}

while inputs:
    print >>sys.stderr,'\n waiting for next event'
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    #对于几种不同状态socket的处理
    for s in readable:

        if s is server:
            connection, client_addr = s.accept()
            print >>sys.stderr, 'new connection from', client_addr
            connection.setblocking(0)
            inputs.append(connection)
            #每个连接给一个存放消息的地方，多次连续发送保证数据都能接收到
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print >>sys.stderr, "receved {%s} from %s "%(data,\
                        s.getpeername())
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print >>sys.stderr, 'closeing', s.getpeername() , 'after reading no data'
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
    
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print >>sys.stderr, 'output queue for ',s.getpeername(), 'is empty'
            outputs.remove(s)
        except Exception as e:
            print >>sys.stderr, str(e)
        else:
            print >>sys.stderr, 'sending {%s} to %s'%(next_msg, s.getpeername())
            s.send(next_msg)

    for s in exceptional:
        print >>sys.stderr, "error", s.getpeername()
        inputs.remove(s)
        if s in outputs:
            outputs.remove()
        s.close()

        del message_queues[s]
    


             



    
        





