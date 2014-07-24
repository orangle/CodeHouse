#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#linecache_test.py
#author: orangleliu
'''
官网的解释就是可以得到文件的任意一行，并且这方法是经过优化的，使用了缓存。
'''

import linecache
filename = './test.txt'

##获取所有的行
f = linecache.getlines(filename)
print f

##获取任意一行
context = linecache.getline(filename, 1)
print context

#当文件的内容改变的时候
#需要  check 或者是update 下，才能获取新的文件
linecache.checkcache(filename)
#或者
linecache.updatecache(filename)

#使用完了要清空缓存
linecache.clearcache()
