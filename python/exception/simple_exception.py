#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python27.x    simple_exception.py
#orangleliu#gmail.com   @2014-03-26

'''
简单的程序中经常是直接抛出异常，打印或者是直接跳过的比较多，
这个时候的异常只是打扰了我们的程序运行，我们只想把它显示出来
或者直接跳过去
'''

#异常的产生
#print '2'+2
'''
Traceback (most recent call last):
  File ".\simple_exception.py", line 13, in <module>
    print '2'+2
TypeError: cannot concatenate 'str' and 'int' objects
'''

#异常跳过,能保持正常运行，但是错误部分跳过
try:
    print '2'+2
except:
    pass
#print   'ok'
'''
PS D:\CodeHouse\python\exception> python .\simple_exception.py
ok
'''

#抛出异常，继续运行, 如果捕获的异常类型不正确也会直接中断执行
#使用Exception可以捕获所有的异常，但是会有隐患
try:
    print '2'+2
except Exception:
    print 'Oops some error happened!'
print 'Execute this line'
'''
PS D:\CodeHouse\python\exception> python .\simple_exception.py
Oops some error happened!
Execute this line
'''


