#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2015-3-5
'''
python3中异步模块为asyncio，已经非常好用
要想在python2中使用，需要trollius来代替

replace asyncio with trollius (or use import trollius as asyncio)
replace yield from ... with yield From(...)
replace yield from [] with yield From(None)
in coroutines, replace return res with raise Return(res)

启动一个程序，每个1秒在控制台打印下hello baby，同时在控制台可以输入数字，显示这个数字的888倍是啥
'''
import sys
import time

import trollius as asyncio
from trollius import From

def process_input():
    text = sys.stdin.readline()
    n = int(text.strip())
    print "%s  %s*888=%s"%(n, n, n*888)

@asyncio.coroutine
def print_hello():
    while True:
        print "niu, hello baby %s"%(int(time()),)
        yield From(asyncio.sleep(1))

def main():
    loop = asyncio.get_event_loop()
    loop.add_reader(sys.stdin, process_input)
    loop.run_until_complete(print_hello())

if __name__ == "__main__":
    main()
