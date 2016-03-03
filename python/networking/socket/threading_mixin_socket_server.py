#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: threading_mixin_server.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-10 15:14:09
#License: MIT
############################
'''
使用SocketServer的多线程模式，socket 服务器端
'''

import os
import socket
import threading
import SocketServer

SERVER_HOST = "localhost"
SERVRR_PORT = 8888
BUFF_SIZE = 1024

class RequestHander(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUFF_SIZE)
        cur_pid = os.getpid()
        cur_thread_name = threading.currentThread().getName()
        print "client msg: %s"%data
        response = "server: pid-->%s thread-->%s"%(cur_pid, cur_thread_name)
        self.request.sendall(response)
        return

class ThreadTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    import time
    server = ThreadTCPServer((SERVER_HOST, SERVRR_PORT), RequestHander)
    ip, port = server.server_address
    print ip, port
    server_thread = threading.Thread(target=server.serve_forever)
   # server_thread.setDaemon(True)
    server_thread.start()
    print "server starting port 8888..."

    time.sleep(300)
    server.socker.close()
