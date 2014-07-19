#-*- coding: utf-8 -*-
#log_test2.py   python2.7.x
#author: orangleliu       2014-07-19

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', filename='test2.log')
logger = logging.getLogger('test2')
logger.setLevel(logging.DEBUG)

from log_test1 import fun_test1

def fun_test2():
    fun_test1()
    logger.info("test2-log")


if __name__ == "__main__":
    fun_test2()
