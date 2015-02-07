#-*- coding: utf-8 -*-
#author: orangleliu  date: 2014-12-25
#python2.7.x

'''
对目标主机进行端口扫描
参考 http://codereview.stackexchange.com/questions/38452/python-port-scanner
对比 http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python
'''

#This module makes available standard errno system symbols
from errno import ECONNREFUSED
from functools import partial
from multiprocessing import Pool
import socket

NUM_CORES = 4*2

def ping(host, port):
    try:
        sock = socket.socket()
        sock.connect((host, port))
        print(str(port) + " Open")
        return port
    except socket.error as err:
        if err.errno == ECONNREFUSED:
            return False
        print "some error: %s"%str(err)

def scan_ports(host):
    p = Pool(NUM_CORES)
    ping_host = partial(ping, host)
    return filter(bool, p.map(ping_host, range(1, 65536)))

def main(host=None):
    if host is None:
        host = "127.0.0.1"

    print("\nScanning ports on " + host + " ...")
    ports = list(scan_ports(host))
    print("\nDone.")

    print(str(len(ports)) + " ports available.")
    print(ports)

if __name__ == "__main__":
    #add some commond options
    main()













