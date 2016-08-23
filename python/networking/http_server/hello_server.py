#coding:utf-8
#url https://ruslanspivak.com/lsbaws-part1/

import socket

HOST, PORT = "127.0.0.1", 8888

lsocks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
lsocks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsocks.bind((HOST, PORT))
lsocks.listen(10)

while True:
    clientfd, client_addr = lsocks.accept()
    request = clientfd.recv(1024)
    print client_addr, request

    response = """\
HTTP/1.1 200 OK

Hello Girl!
"""
    clientfd.sendall(response)
    clientfd.close()



