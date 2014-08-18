#!/usr/bin/python
# -*- coding: utf-8 -*-
#python2.7x
#itertools_use.py
#author: orangleliu

'''
itertools模块提供了很多集合数据类型的方法的封装
这些方法都是经过优化，一般来说要比自己实现或者build-in 方法效率要高一些
https://docs.python.org/2/library/itertools.html
'''
from itertools import *

##1  chain() 合并iterators
me = chain([1,2,3], [ i for i in range(5,7)], list('abc'))
#for i in me:
#    print i

#合并的是iterator，即使类型不同也可以合并
me1 = chain((1,3), ['a','b'],{1:'cc'})
#for i in me1:
#    print i

##2  imap，类似map的用法，但是如果两个iterator长度不同会补充默认值None，不会异常
#map(lambda x,y: (x+y), [1,2],[9,10,10])  #异常
for i in imap(lambda x,y: (x+y), [1,2],[9,10,10]):
    print i

#模块中有很多i开头，类似build-in模块中的方法，使用上大同小异，但是返回值和处理会有区别，需要好好查下文档


