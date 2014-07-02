#--*-- coding:utf-8 --*--
#sorted_use.py   python2.7x
#orangleliu@gmail.com      2014-07-02
'''
python中集合类型的排序操作，主要使用sorted 内置方法
'''

##最基础的排序
l1 = [1,3,2,4,7,5]
print  "list  sorted"
print l1
print sorted(l1)

##sorted a tuple list, order by a elemtent of each tuple
t1 = [(1,3),(1,2),(7,6),(1,5)]
print 'list of tuples sorted '
print t1
print sorted(t1, key=lambda x:x[1])

##sorted objects order by object's one attribute
class Cup(object):
    def  __init__(self, name, big, height):
        self.big = big
        self.height = height
        self.name = name

    def __repr__(self):
        return str((self.name, self.big, self.height))

    def get_height(self):
        return int(self.height)

cup_list = [Cup('Appple',100,'112'),Cup('Orange',999, '1232'), Cup('Orange',101,'1132')]
print 'Object sorted'
print cup_list
print sorted(cup_list, key=lambda x:x.big)


######比较高级的是使用操作方法
from operator import itemgetter, attrgetter, methodcaller
'''
itemgetter: 迭代一个集合元素的index(适合元组list这种)
attrgetter:  迭代中一个object元素的attribute 名称
这两种方式都支持多级比较，当第一级相同的时候比较第二级

methodcaller: 对一个迭代元素处理之后排序
'''
print "sorted(t1, key=itemgetter(0))"
print sorted(t1, key=itemgetter(0))

print "sorted(cup_list, key=attrgetter('height')"
print sorted(cup_list, key=attrgetter('height'))

print "sorted(cup_list, key=attrgetter('name', 'big')"
print sorted(cup_list, key=attrgetter('name', 'big'))

#根据元素的一个方法来进行返回值的比较
print "sorted(cup_list, key=methodcaller('get_height'))"
print sorted(cup_list, key=methodcaller('get_height'))

#求倒序增加 reverse为True
print sorted(l1, reverse=True)


###使用自定义的比较函数



