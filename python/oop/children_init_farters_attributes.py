#-*- coding: utf-8 -*-
#children_init_farters_attributes.py   python2.7.x
#author: orangleliu       2014-04-18
'''
子类初始化父类的属性, 子类中覆盖了父类的属性
'''

class Farter(object):
    farter_attr = 288

    def print_attr(self):
        print  self.farter_attr+2000


class Child1(Farter):

    def __init__(self, farter_attr):
        self.farter_attr = farter_attr

    def get_farter_attr(self):
        #不初始化父类，直接打印
        self.print_attr()
        print self.farter_attr


if __name__=='__main__':
    #子类属性会覆盖父类原来的属性，调用父类方法的时候会使用子类新的属性
    Child1(100).get_farter_attr()
