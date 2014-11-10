# -*- encoding=utf-8 -*-
'''
author: orangleliu

python 弱引用的小实验
'''

import weakref
import gc

class NewObj(object):
    def my_method(self):
        print "called me "

obj = NewObj()
r = weakref.ref(obj)
gc.collect()
print  r() is obj

obj = 1
gc.collect()  #
print  r() is None, r()

print '*******************'
obj = NewObj()
s = obj
gc.collect()
print s is obj

obj = 1
gc.collect()
print s is None, s
