#!/usr/bin/python
'''
Meta class学习和使用

class自身也是对象，用来生成对象实例
The main purpose of a metaclass is to change the class automatically, when it’s created.
#type 就是一个元类


'''

type('Foo', (), {})

print ''.__class__
print ''.__class__.__class__

''' 
大部分情况下都不会用到，一般是提供Api的时候才需要使用元类的设计
主要作用就是在创建类的时候自动做一些工作，由一般的类编程框架可以使用的类

改变类行为的几种方法：
1 装饰器
2 python monkey patch
3 metaclass 

'''