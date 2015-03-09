#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: local_machine_info.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-09 18:31:41
############################

import socket

def local_machine_info():
    '''
    get some info of local machine 
    '''
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    print "The local machine's host name is %s, ip is %s"%(host_name, ip)

def get_remote_machine_info():
    '''
    get remote machine info by hostname
    '''
    remote_host = "python.org"
    try:
        ip = socket.gethostbyname(remote_host)
        print "host %s , its ip is %s"%(remote_host, ip)
    except Exception as e:
        print str(e)

if __name__ == "__main__":
    local_machine_info()
    get_remote_machine_info()
