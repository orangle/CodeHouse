#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu  @2014-06-25

##下面函数执行的结果是什么
def fa():
    x = 1
    def fb():
        print x+1
    fb()

fa()
print '*'*50

y = 1
def fc():
    x=x+1

print fc()

#可以参见 scope_rules.py 里面的方法