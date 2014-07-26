#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#property.py  @2014-07-26
#author: orangleliu

class Person(object):
    def __init__(self, name):
        self._name = name 
    
    def getName(self):
        print 'fetch....'
        return self._name
    
    def setName(self, value):
        print 'change...'
        self._name = value
    
    def delName(self):
        print 'remove....'
        del self._name
        
    #也可以使用装饰器的方式
    name = property(getName, setName, delName, "name property docs")
    
bob = Person('Bob')
print bob.name
print Person.name.__doc__
bob.name = 'bob'
print bob.name
del bob.name
#print bob.name

'''
并没有想象中的那么好使

#类没有继承object的情况下
fetch....
Bob
name property docs
bob
set del 就没有使用啊

#类继承object的情况下
Bob
name property docs
change...
fetch....
bob
remove....
'''