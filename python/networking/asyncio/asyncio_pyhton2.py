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
'''

import trollius as asyncio
from trollius import From


def hello_word(loop):
    print "Hello world"
    loop.stop()

loop = asyncio.get_event_loop()

loop.call_soon(hello_word, loop)
loop.run_forever()
loop.close()

