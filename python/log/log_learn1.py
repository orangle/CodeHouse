#-*- coding: utf-8 -*-
#log_learn1.py   python2.7.x
#author: orangleliu       date:2014-11-26

'''
比较简单的单个文件中log使用
'''

import logging

#1 没什么格式 简单记录
#logging.basicConfig(level=logging.INFO)
#loger = logging.getLogger(__name__)

#2 添加一些日志配置 handler，格式和输出方式（了解有哪些handler）
'''
loger = logging.getLogger(__name__)
loger.setLevel(logging.DEBUG) #基本无用,日志全部输出到log中，级别是info

handler = logging.FileHandler("learn1.log")
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
handler.setFormatter(formatter)

loger.addHandler(handler)
'''



#http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
#有关模块中使用logger的问题很经典
#最好使用JSON or YAML来配置log



#-----------测试数据------------

loger.info("Start reading database")

try:
    c = 2/0
except ZeroDivisionError:
    #使用 exc_info=True参数来记录异常堆栈信息
    loger.error("print is failed", exc_info=True)

a = 1 + 2
loger.debug("1 + 2 : %s"%a)
loger.error("nothing is error")

loger.info("End reading database")
