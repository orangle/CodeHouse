#--*-- coding:utf-8 --*--
#dict_use.py   python2.7x
'''
关于字典的常用操作
'''

#统计list中，各个元素出现的次数
'''
In [43]: a = ['1','2','1','3','1','2']

In [44]: d = {}

In [45]: for i in a:
   ....:     d[i] = d.get(i,0)+1
   ....:

In [46]: d
Out[46]: {'1': 3, '2': 2, '3': 1}
'''

'''
In [47]: a = ['1','2','1','3','1','2']

In [48]: from collections import  defaultdict

In [49]: d = defaultdict(int)

In [50]: for i in a:
   ....:     d[i] += 1
   ....:

In [51]: d
Out[51]: defaultdict(<type 'int'>, {'1': 3, '3': 1, '2': 2})
'''

#------------------------------------------------------------------------------
#怎么样group 字典




