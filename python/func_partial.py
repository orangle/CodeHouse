#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#partial.py
#authror: orangleliu

'''
functools 中Partial可以用来改变一个方法默认参数
1 改变原有默认值参数的默认值
2 给原来没有默认值的参数增加默认值
'''
def foo(a,b=0) :
    '''
    int add'
    '''
    print a + b

#user default argument
foo(1)

#change default argument once
foo(1,1)

#change function's default argument, and you can use the function with new argument
import functools

foo1 = functools.partial(foo, b=5)  #change "b" default argument
foo1(1)

foo2 = functools.partial(foo, a=10) #give "a" default argument
foo2()

'''
foo2 is a partial object,it only has three read-only attributes
i will list them
'''
print foo2.func
print foo2.args
print foo2.keywords
print dir(foo2)

##默认情况下partial对象是没有 __name__ __doc__ 属性，使用update_wrapper 从原始方法中添加属性到partial 对象中
print foo2.__doc__
'''
执行结果：
partial(func, *args, **keywords) - new function with partial application
    of the given arguments and keywords.
'''

functools.update_wrapper(foo2, foo)
print foo2.__doc__
'''
修改为foo的文档信息了
'''
