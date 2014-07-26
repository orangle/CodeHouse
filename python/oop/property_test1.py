#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#property.py  @2014-07-26
#author: orangleliu

class GetSquare(object):
    def __init__(self, num):
        self.value = num
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, num):
        self._value = num**2
        
'''
从上面可以看到set属性值的时候作了一些属性的某人动作，有时候很有必要
'''

g = GetSquare(4)
print g.value

g.value = 10 
print g.value