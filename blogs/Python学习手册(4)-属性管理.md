属性管理-特性
========

>一般开发这不必关心属性的实现，对工具的构建这来说，了解这一块对API的灵活性有帮助。
大多数情况下，属性位于对象自身之中，或者继承自对象所派生自的一个类。  ----python学习手册

###property
>property(fget=None, fset=None, fdel=None, doc=None) -> property attribute
fget is a function to be used for getting an attribute value, and likewisefset is a function for setting, and fdel a function for del'ing, an attribute.
可以使用函数的方式也可以使用装饰器的方式来使用

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    #python2.7x
    #property.py  @2014-07-26
    #author: orangleliu

    class Person(object):
        def __init__(self, name):
            self._name = name

        def getName(self):
            print 'fetch....'
            return self._name

        def setName(self, value):
            print 'change...'
            self._name = value

        def delName(self):
            print 'remove....'
            del self._name

        #也可以使用装饰器的方式
        name = property(getName, setName, delName, "name property docs")

    bob = Person('Bob')
    print bob.name
    print Person.name.__doc__
    bob.name = 'bob'
    print bob.name
    del bob.name
    #print bob.name

    '''
    并没有想象中的那么好使

    #类没有继承object的情况下
    fetch....
    Bob
    name property docs
    bob
    set del 就没有使用啊

    #类继承object的情况下
    Bob
    name property docs
    change...
    fetch....
    bob
    remove....
    '''

__书中的例子并没有继承object,  使用2.7的版本和书中结果不一致。 需要继承object才能达到预期的结果__

####添加属性的默认操作
这里使用装饰的方式， 只要value赋值就进行一个默认的操作，可以看到我们使用属性的方式就可以默认调用函数来处理属性。
g.value 而不是 g.valueXX()

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    #python2.7x
    #property.py  @2014-07-26
    #author: orangleliu

    class GetSquare(object):
        def __init__(self, num):
            self.value = num

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, num):
            self._value = num**2

    '''
    从上面可以看到set属性值的时候作了一些属性的某人动作，有时候很有必要
    '''

    g = GetSquare(4)
    print g.value

    g.value = 10
    print g.value


###描述符
>描述符作为独立的类创建， 并且她们就方法函数一样分配给类属性。和任何其他的类属性一样，它们可以通过子类和实力继承。通过为描述符自身提供一个self，以及提供客户类的实例，都可以提供访问拦截方法。
特性的应用领域相对狭窄，描述符提供了一种更为通用的解决方案。








