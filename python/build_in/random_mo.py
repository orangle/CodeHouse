#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu  @2014-05-24
'''
random使用方法
'''

import  random

#0-1之间的浮点数
print random.random()

#某两个数之间的浮点数
print random.uniform(1, 20)

#比较常用的： 求某个连续区间的整数随机数
print random.randint(1, 100)

#去某个步长一定的序列的整数随机数
#0 2 4...100 之间的随机整数
print random.randrange(0, 101, 2)


#一串字符串中任意随机元素（例如一个生成验证码）
print random.choice('1234567890abcdefghijklmnopqrstuvwsyz')

#从序列中任意选取多个，更适合做 几位的验证码
print random.sample([1,2,3,4,5,6,7,8,9,0],4)

#随机排序
items = [1, 2, 3, 4, 5, 6, 7]
random.shuffle(items)
print items
