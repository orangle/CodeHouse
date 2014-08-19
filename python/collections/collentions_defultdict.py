#-*- coding: utf-8 -*-
#collections_defaultdict.py   python2.7.x
#author: orangleliu       2014-04-20
'''
how use defaultdict
'''
import collections as coll

def default_factory():
    return 'default value'

d = coll.defaultdict(default_factory, foo='bar')
print 'd:',d
print 'foo=>', d['foo']
print 'foo=>', d['bar']   #key为'bar'的元素不存在，会有一个默认值

'''
刚开始不太懂这个default的好处，后来从别人的blog中发现一种好处，
就是指定了默认类型以后就不需要总是判断key的存在与否问题，就可以直接使用
特别是list set这种集合类型作为一个字段的元素的时候
'''
dict_set = coll.defaultdict(set)
dict_set['key'].add('000')
dict_set['key'].add('111')
print dict_set


dict_set1 = {}
#如果不知道这个字段中key有没有，需要先判断
if 'key' not in dict_set1:
    dict_set1['key'] = set()
dict_set1['key'].add('111')
dict_set1['key'].add('000')
print dict_set1



ss = '1111222233334444'
dict_int = coll.defaultdict(int)
for s in ss:
    dict_int[s] += 1
print dict_int

'''
官方文档的这个例子就能看到这种写法的简洁了
https://docs.python.org/2/library/collections.html#collections.defaultdict
>>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
>>> d = defaultdict(list)
>>> for k, v in s:
...     d[k].append(v)
...
>>> d.items()
[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
'''
