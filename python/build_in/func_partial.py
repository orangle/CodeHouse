#coding:utf-8

from functools import partial

env = 'test'

def echo_test(name):
    print 'test'

def echo_pro(name):
    print 'Hi %s'%name

if env == 'production':
    echo = partial(echo_pro)
else:
    echo = partial(echo_test)

echo('lzz')

def add(x,y):
    return x+y

add10 = partial(add, y=10)

print 'args', add10.args
print 'keywords', add10.keywords
print 'func name', add10.func.func_name
print add10(10)

add10and9 = partial(add,10,y=9)
print 'args', add10and9.args
print 'keywords', add10and9.keywords
print 'func name', add10and9.func.func_name
print add10and9()
