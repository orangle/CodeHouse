#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu  @2014-06-25
'''
问题1：

下面代码片段：
>>> # INITIALIZING AN ARRAY -- METHOD 1
...
>>> x = [[1,2,3,4]] * 3
>>> x
[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
>>>
>>>
>>> # INITIALIZING AN ARRAY -- METHOD 2
...
>>> y = [[1,2,3,4] for _ in range(3)]
>>> y
[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
>>>
>>> # WHICH METHOD SHOULD YOU USE AND WHY?

比较两种不同方式生成的list有什么不同，并给出证明

'''

x =  [[1,2,3,4]] * 3
x[0][3] = 100
for i in x :
    print id(i), i

print '*'*80
y = [[1,2,3,4] for _ in range(3)]
y[0][3] = 100
for i in y:
    print id(i),i

######比较* 和 使用列表解析生成对象的不同########






