#-*- coding: utf-8 -*-
#doctest1.py   python2.7.x
#author: orangleliu       2014-07-12

'''
执行这个文件的方式
可以在__main__中这样调用
python  doctest1.py #直接执行没有显示测试过程
python  doctest1.py  -v #执行并显示测试过程
也可以通过python的命令行参数来调用
python -m doctest doctest1.py    # 如果成功没有什么显示
python -m doctest -v doctest1.py  #会显示执行过程和结果，比较人性化一点
'''

##注意>>> 后面需要跟着一个空格才行
"""
>>> print 'a'
a
"""

def test(a,b):
    '''
    >>> test(3+4)
    7

    >>> test(2, 3)
    5
    '''
    print a+b

if __name__ == "__main__":
    import doctest
    doctest.testmod()
