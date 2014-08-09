#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#dis_func.py
#author: orangleliu
#date: 2014-08-09

def sayhi():
    print 'Hello world'

if __name__ == '__main__':
    import dis
    dis.dis(sayhi)
