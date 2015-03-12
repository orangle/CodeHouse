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

使用coroutine + task 并行
'''

import trollius as asyncio
from trollius import From

@asyncio.coroutine
def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print  "Task %s:  factorial (%s)"%(name, i)
        yield From(asyncio.sleep(1))
        f *= i
    print "Task %s, result: %s"%(name, f)

loop = asyncio.get_event_loop()
tasks = [
    asyncio.async(factorial("A", 2)),
    asyncio.async(factorial("B", 5)),
    asyncio.async(factorial("C", 6))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

