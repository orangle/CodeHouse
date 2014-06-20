#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python27.x    return_exception.py
#orangleliu#gmail.com   @2014-06-20

'''
异常处理中return 不同位置的测试
'''

def test1():
    '''
    在异常中return
    '''
    l = []
    try:
        l[1]
        return 'normal'
    except Exception as e:
        return 'exception:'+str(e)

def test2():
    '''
    return放在所有处理之后，异常中赋值
    '''
    l = []
    res = 'normal'
    try:
        l[1]
    except Exception as e:
        res = 'exception:'+str(e)
    return res


if __name__ == '__main__':
    print 'test1----'+test1()
    print 'test2----'+test2()
