# -*- coding: utf-8 -*-
#python2.7x  else_exception.py
#orangleliu   @2014-03-28
'''
异常处理中else的用法

如果发生异常进行异常处理
没有发生异常就执行else操作
'''

def else_test():
    try:
        #10/0
        10/1
    except:
        print  'some exception hanppened'
        raise
    else:
        print "nothing hanppend"

if __name__=="__main__":
    else_test()
