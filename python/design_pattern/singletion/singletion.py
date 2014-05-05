#!/usr/bin/env python
# -*- coding: utf-8 -*-
#orangleliu  @2014-05-05
'''
单例的几种写法
'''

#看了篇文章 说了singletion的几个坏处，并使用导入的方式来实现一个实例
'''
具体说说单例的几个不好的地方
The core problem of a singleton is the global, shared state

The second biggest problem is that, invariably, if you think something
needs to be a singleton today, tomorrow you'll wish you had two of
them.
'''
class Foo():
    pass

foo = Foo()

