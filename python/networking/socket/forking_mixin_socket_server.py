#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: forking_mixin_socket_server.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-09 21:38:36
############################

import os
import sys
import socket
import threading
import SocketServer

SERVER_HOST = "localhost"
SERVER_PORT = 8888
BUF_SIZE = 1024
ECHO_MSG = "HELLO ORANGLELIU!"

class RequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = "pid-->%s: %s"%(current_process_id, data)
        print "Server sending response [%s]"%response
        self.request.send(response)
        return

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

def main():
    import time

    server = ForkingServer((SERVER_HOST, SERVER_PORT),
                RequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "server loop pid: %s"%os.getpid()
    time.sleep(300)
    server.shutdown()
    server.socket.close()

if __name__ == "__main__":
    main()

