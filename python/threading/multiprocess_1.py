# -*- coding: utf-8 -*-
#multiprocess_1.py   python2.7.x
#orangleliu@gmail.com    2014-05-04
'''
多进程的简单使用
对月python 对进程的使用是十分必要的，因为gil的问题
'''

from multiprocessing import Process
import os
import time

def info(title):
    '''
    打印pid
    '''
    print title
    print 'module_name:', __name__
    if hasattr(os, 'getppid'):
        print 'parent process', os.getppid()
    time.sleep(1)
    print 'process is', os.getpid(), 'end \n\t'

def f(name):
    info('function f')
    print 'hello , ', name

if __name__=='__main__':
    info('main line')
    p = Process(target=f, args=('oranglelliu',))
    p.start()
    #p.join()
    print "main process end"
