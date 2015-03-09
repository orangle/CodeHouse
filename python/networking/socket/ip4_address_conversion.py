#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: ip4_address_conversion.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-03-09 19:01:39
############################
'''
ip4地址 转化为 16进制，10进制
'''
import socket
import struct
from binascii import hexlify, unhexlify

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def ip4hex(addr):
    packed_ip = socket.inet_aton(addr)
    return hexlify(packed_ip)

def hex4ip(addr):
    upack_addr = unhexlify(addr)
    return socket.inet_ntoa(upack_addr)

if __name__ == "__main__":
    addr = "127.0.0.1"
    intip = ip2int(addr)
    print intip 
    print int2ip(intip)
    
    hexip = ip4hex(addr)
    print hexip
    print hex4ip(hexip)

