#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python27.x    scope_rules.py
#orangleliu#gmail.com   @2014-06-25

'''
作用域错误使用的一些情况
大部分都是因为使用了全局变量引起的
'''

x=10
def foo():
    x += 1  #使用全局变量的时候特别注意这种写法
    print x
'''
这是因为，在一个作用域里面给一个变量赋值的时候，
Python自动认为这个变量是这个作用域的本地变量，并屏蔽作用域外的同名的变量。
'''
#foo()   #报错 UnboundLocalError: local variable 'x' referenced before assignment

def foo1():
    print x,'foo1'
    y = x + 1
    print y,'foo1'

foo1()  #从这里就可以发现第一处的错误是原因是 局部变量和全局变量重名，在没有 x=x+1
           # 等号右边的x是在局部变量中查找，全局的x这时是被屏蔽的，所以报错没有声明变量x

def foo2():
    global x
    x += 1
    print x,'foo2'

foo2()  #通过对x进行全局声明也可以解决foo出现的问题。







