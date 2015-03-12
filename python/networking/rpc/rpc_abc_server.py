#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: rpc_abc.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-12 15:56:04
#License: MIT
############################

import SimpleXMLRPCServer
import os 

def ls(directory):
    try:
        return os.listdir(directory)
    except OSError:
        return "error"

if __name__ == "__main__":
    s = SimpleXMLRPCServer.SimpleXMLRPCServer(('127.0.0.1', 8888))
    s.register_function(ls)
    print "rpc server.. start.."
    s.serve_forever()



