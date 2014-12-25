#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-16
#server1.py
'''
zeromq hello boy!
zeromq4.0
'''
import zmq

adss = "tcp://*:8888"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(adss)

cs = socket.recv()
print cs
socket.send(cs + "oh boy")
