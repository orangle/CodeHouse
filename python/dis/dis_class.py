#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#dis_class.py
#author: orangleliu
#date: 2014-08-09

class Person(object):

    name = 'Jack'

    def __init__(self, age):
        self.age = age

    def show():
        print self.name, self.age

import dis
dis.dis(Person)
