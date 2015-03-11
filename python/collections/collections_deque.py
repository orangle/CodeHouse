#-*- coding: utf-8 -*-
#collections_deque.py   python2.7.x
#author: orangleliu       2014-04-20
'''
some demo of python deque module
if you have many  insert and pop op, deque is better than list
基本的用法其实和list差不多的
'''

from collections import deque

#保持list长度
d = deque(maxlen=2)
for i in range(10):
    d.append(i)
    print d 


print '*'*20


import heapq
#保持list中top n
nums = [4,5,6,9,23,45,23]
print "nums",nums 
print "top 3"
print heapq.nlargest(3, nums)
print heapq.nsmallest(3, nums)

nums.append(100)
nums.append(1)

print "\nnums",nums 
print "top 3"
print heapq.nlargest(3, nums)
print heapq.nsmallest(3, nums)

sutdents = [
    {"name":"xiaoming", "age": 20}, 
    {"name":"xiaowang", "age":10}
]
print "\nstudent",sutdents
ss = heapq.nsmallest(2, sutdents, key=lambda s:s["age"])
print ss
