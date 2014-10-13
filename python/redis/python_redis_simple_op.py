#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#author: orangleliu  2014-10-13

'''
use python connected python, some simple operation
'''

import redis

#connect redis
def get_conn():
    conn = redis.Redis("localhost")
    return conn

#key-value  string
def string_op():
    conn = get_conn()
    conn.set("name", "orangleliu")
    print "The name is %s"%conn.get("name")

#string_op()
def int_op():
    #you can increase value by 1 or decrease by 1
    conn = get_conn()
    conn.set("count", 100)
    conn.incr("count")
    print "The count was increased: %s"%conn.get("count")
    conn.decr("count")
    print "The count was decrease %s"%conn.get("count")

    #if we increase a key which is not in the database, what is happen?
    conn.incr("sum")
    print "sum is not init :%s"%conn.get("sum") #you will find the default value is 0

#int_op()
def list_op():
    conn = get_conn()
    conn.rpush("l1", "orange")
    conn.rpush("l1", "apple")
    print "The len of l1 is %s"%conn.llen("l1")
    print "The index 1 of l1 is %s"%conn.lindex("l1", 1)

#list_op()
def set_op():
    conn = get_conn()
    conn.sadd('s1', 'apple')
    conn.sadd('s1', 'orange')
    conn.sadd('s1', 'orange')
    print "The element of the s1 is %s"%conn.smembers('s1')

set_op()


