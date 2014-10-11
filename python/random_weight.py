#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#random_weight.py 
#author: orangleliu@gmail.com 2014-10-11

'''
每个元素都有权重，然后根据权重随机取值

输入 {"A":2, "B":2, "C":4, "D":10, "E": 20}
输出一个值
'''
import random
import collections as coll

data = {"A":2, "B":2, "C":4, "D":6, "E": 11}

#第一种 根据元素权重值 "A"*2 ..等，把每个元素取权重个元素放到一个数组中，然后最数组下标取随机数得到权重
def list_method():
    all_data = []
    for v, w in data.items():
        temp = []
        for i in range(w):
            temp.append(v)
        all_data.extend(temp)
        
    n = random.randint(0,len(all_data)-1)
    return all_data[n]
    
#第二种 也是要计算出权重总和，取出一个随机数，遍历所有元素，把权重相加sum，当sum大于等于随机数字的时候停止，取出当前的元组
def iter_method():
    total = sum(data.values())
    rad = random.randint(1,total)
    
    cur_total = 0
    res = ""
    for k, v in data.items():
        cur_total += v
        if rad<= cur_total:
            res = k 
            break
    return res
    
    
def test(method):
    dict_num = coll.defaultdict(int)
    for i in range(100):
        dict_num[eval(method)] += 1
    for i,j in dict_num.items():
        print i, j    
    
if __name__ == "__main__":
    test("list_method()")
    print "-"*50
    test("iter_method()")
    

