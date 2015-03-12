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

使用coroutine
'''

import trollius as asyncio
from trollius import From
import datetime

@asyncio.coroutine
def display_date(loop):
    end_time = loop.time() + 10
    while True:
        print datetime.datetime.now()
        if (loop.time() + 1.0) >=end_time:
            break
        yield From(asyncio.sleep(1))

loop = asyncio.get_event_loop()
loop.run_until_complete(display_date(loop))
loop.close()
