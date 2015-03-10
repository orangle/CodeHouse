#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: test_client.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-10 16:15:19
#License: MIT
############################

import socket
import os
import sys


SERVER_HOST = "localhost"
SERVER_PORT = 8888
BUF_SIZE = 1024
ECHO_MSG = "HELLO ORANGLELIU!"

class ForkedClient(object):
    '''
    用来测试服务端的，多个客户端同时连接服务端
    '''
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        current_process = os.getpid()
        print "PID %s client send msg to server: %s"%(current_process, ECHO_MSG)
        data_len = self.sock.send(ECHO_MSG)
        print "Msg length is %s"%data_len

        data = self.sock.recv(BUF_SIZE)
        print "PID %s reveced: %s"%(current_process, data)

    def shutdown(self):
        self.sock.close()


if __name__ == "__main__":
        clients = []
        for i in range(5):
            client = ForkedClient(SERVER_HOST, SERVER_PORT)
            client.run()
            clients.append(client)
            time.sleep(1)

        for c in clients:
            c.shutdown()
