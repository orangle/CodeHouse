#-*- coding: utf-8 -*-
#log_test1.py   python2.7.x
#author: orangleliu       2014-07-19
'''
两个文件中都有log配置
执行的时候怎么写log文件
'''


import logging
logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', filename='test1.log')
logger = logging.getLogger('test1')
logger.setLevel(logging.DEBUG)

def fun_test1():
    logger.info("test1-log")
