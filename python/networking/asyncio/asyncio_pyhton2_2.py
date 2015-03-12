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

定时执行
'''

import trollius as asyncio
from trollius import From
import datetime

def display_date(end_time, loop):
    print datetime.datetime.now().__str__()
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

#创建一个事件
loop = asyncio.get_event_loop()

#事件的开始
end_time = loop.time() + 10.0
loop.call_soon(display_date, end_time, loop)

#事件的结束 stop ->close
loop.run_forever()
loop.close()
