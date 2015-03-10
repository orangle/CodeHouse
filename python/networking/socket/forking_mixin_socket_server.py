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


class RequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = "%s: %s"%(current_process_id, data)
        print "Server sending response [%s]"%response
        self.request.send(response)
        return 

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass 


def main():
    import time
    try:
        option = sys.argv[1]
    except:
        option = ""

    if option == "server":
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
    else:
        clients = []
        for i in range(5):
            client = ForkedClient(SERVER_HOST, SERVER_PORT)
            client.run()
            clients.append(client)
            time.sleep(1)

        for c in clients:
            c.shutdown()

if __name__ == "__main__":
    main()

