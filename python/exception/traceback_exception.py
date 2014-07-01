#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu  @2014-07-01
'''
traceback  简单使用
'''

import  traceback,sys

try:
    print a
except Exception as e:
    exc_type, exc_value, exc_tb = sys.exc_info()
    #traceback.print_exception(exc_type, exc_value, exc_tb)    #没有返回值，直接打印
    ex = traceback.format_exception(exc_type, exc_value, exc_tb)  #有返回值，返回一个list，可以后续做处理
    print 'Exception_str %s'%ex
