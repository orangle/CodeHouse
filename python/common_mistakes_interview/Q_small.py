#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu  @2014-06-25
'''
一些比较简短的问题和回答
'''

#say('Hello')('World')
def say(a):
    def hello(b):
        return a+" "+b
    return hello

print  say('Hello')('World')


say1 = lambda x: lambda y: x + " " + y
print say1('Hello')('World')

print '*'*50
