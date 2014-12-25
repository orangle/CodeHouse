#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-19
#clent1.py

import zmq

adss = "tcp://127.0.0.1:8888"
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(adss)

socket.send("hello ..")
print socket.recv()
