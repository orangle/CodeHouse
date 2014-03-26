#!/usr/bin/env python
# -*- coding: utf-8 -*-
# observer_simple.py

# Date: 2014-03-16
# CopyRight: orangleliu@gmail.com
# Lisence: BSD
# tips:简单实现观察者模式


class Subject(object):
    '''
    Subject has three methods:
    add_observer
    delete_observer
    notify
    '''
    def __init__(self):
        self.observers_list = []

    def add_observer(self, obs):
        if obs is not self.observers_list:
            self.observers_list.append(obs)

    def delete_observer(self, obs):
        try:
            self.observers_list.remove(obs)
        except ValueError:
            pass

    def notify(self):
        for obs in self.observers_list:
            obs.notify()

class Observer(object):
    def __init__(self, name):
        self.name = name

    def notify(self):
        print "%s accept the infomation" %self.name

if __name__=='__main__':
    ob1 = Observer('Java')
    ob2 = Observer('Python')

    sub = Subject()
    sub.add_observer(ob1)
    sub.add_observer(ob2)
    print 'Tow users'
    sub.notify()
    print 'One user'
    sub.delete_observer(ob1)
    sub.notify()

'''
console:

PS D:\code\python\python_abc\design_pattern> python .\observer_simple.py
Tow users
Java accept the infomation
Python accept the infomation
One user
Python accept the infomation

quote:
    https://github.com/jfcalvo/patterns/blob/master/python/observer.py
    http://code.activestate.com/recipes/131499-observer-pattern/
'''



