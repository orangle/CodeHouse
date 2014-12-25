#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-19
#rep.py
'''
server
'''

import os
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:8888")

print "Worker id is %s"%os.getpid()

while True:
    a, b = socket.recv_multipart()
    print "server get is %s %s"%(a, b)
    socket.send( str(int(a)+int(b)))
