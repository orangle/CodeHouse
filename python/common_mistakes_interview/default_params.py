#-*- coding: utf-8 -*-
#author: orangleliu  @2014-06-25
#python2.7x
'''
python程序中常见的错误

##默认参数为可变数据类型
'''

def foo(bar=[]):
    bar.append('baz')
    return bar

print foo()
print foo()
print foo()
'''
['baz']
['baz', 'baz']
['baz', 'baz', 'baz']
问题是这个默认参数的值是一个可变对象，那我们用一个不可变的试试就知道了，例如字符串
'''

def foo1(bar="?"):
    return bar + "?"

print foo1()
print foo1()
print foo1()
'''
这就没有问题
'''

###############解决方案是给出一个不可变值，然后在程序内部判断
def foo_test(bar=None):
    if bar==None:
        bar = []
    bar.append("baz")
    return bar

print foo_test()
print foo_test()
print foo_test()
'''
['baz']
['baz']
['baz']
 这样就正常了
'''




