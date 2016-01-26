#coding:utf-8
#py2 some_examples_about_metaclass
#metaclass 集成type类，并且参数有些变化
'''
type 就是个 metaclass
元类主要用于类工厂 批量制造一些特殊的类

'''

class MClass(type):
    def __init__(self, name, bases, attrs):
        print name
        print bases
        print attrs
        print attrs.items()

class RClass(object):
    __metaclass__ = MClass
    age = 20

if __name__ == "__main__":
    print RClass
