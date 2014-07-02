#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7.x  custom_exception.py
#orangleliu   @2014-03-26

'''
自定义exception ，并且捕获
多级的异常，查看抛出情况
'''

class NewException(Exception):
    def __str__(self):
        return u"自己定义的一个异常"


def ex_test1():
    r = "jian.shi"
    try:
        r = "orengleliu"
        print '2'+2+[]               #在异常发生行之前的变量在异常发生之后仍然可以取到
        r = 'default value'
    except Exception as e:
        print r
        r = 'some exception happened'
        return r   #可以吧异常内处理的结果提前返回给上一级,异常就不会raise了！！！
        raise NewException()
    return r

def ex_test2():
    r = ''
    try:
        r = ex_test1()
    except NewException:
         print 'ex_test1 has exception'
    print r


if __name__=='__main__':
    ex_test2()
