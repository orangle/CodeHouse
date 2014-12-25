#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-19
#req.py
'''
client, 一个客户端可以连接多个服务端，多个服务端部署在一个端口上
'''

import zmq
import random
import time

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.bind("tcp://*:8888")

time.sleep(1)

for i in range(9):
    a, b = random.randint(0,100), random.randint(0,100)
    print 'num:  %s + %s'%(a, b)
    socket.send_multipart([str(a),str(b)])
    rep = socket.recv()
    print ' = %s'%rep



