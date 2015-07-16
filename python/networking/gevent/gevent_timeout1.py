# -*- coding: utf-8 -*-
#orangleliu
#2015-07-16

import gevent
from gevent import Timeout

timeout = Timeout(5)
timeout.start()


def wait():
    print 'wait start'
    gevent.sleep(4)
    print 'wait end'

try:
    gevent.spawn(wait).join()
except Timeout:
    print 'timeout'
