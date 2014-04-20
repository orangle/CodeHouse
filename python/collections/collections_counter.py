#-*- coding: utf-8 -*-
#collections_counter.py   python2.7.x
#author: orangleliu       2014-04-20
'''
对于一个集合元素中相同的元素的统计
'''

from collections import Counter


#统计一个元素出现的次数
li = [1,1,1,2,2,'2','2','r','r','r']
a  = Counter(li)
print u'统计每个元素出现的次数',a
#统计有哪些元素在list中
print u'统计出现了多少个元素',len(set(li))
print u'top2统计',a.most_common(2)



