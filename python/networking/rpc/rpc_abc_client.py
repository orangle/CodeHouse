#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: rpc_abc_client.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-12 16:05:10
#License: MIT
############################

import xmlrpclib
x = xmlrpclib.ServerProxy("http://localhost:8888")
print x.ls('.')





