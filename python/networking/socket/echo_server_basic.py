#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: echo_server_basic.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-09 19:37:56
############################
'''
比较标准的入门级echo server
阻塞，同步
'''

import socket
import argparse

host = "127.0.0.1"
buff_data = 2048
backlog = 5

def echo_server(port):
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #设置端口重用
    #ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    #ss.settimeout(60)
    server_info = (host, port)
    ss.bind(server_info)
    ss.listen(backlog)
    print "Server starting.... port is %s"%port
    while 1:
        client, addr = ss.accept()
        print "client comming: %s %s"%(addr[0], addr[1])
        client.settimeout(30)

        try:
            data = client.recv(buff_data)
            if data:
                print "Data: %s"%data
                client.send("Server: %s"%data)
        except socket.timeout:
            print "socket timeout"
            client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scoket echo server")
    parser.add_argument("--port", action="store", dest="port", type=int, required=False)
    arg = parser.parse_args()
    port = arg.port or 8888
    echo_server(port)


