# -*- coding: utf-8 -*-
#orangleliu
#2015-07-16

import time

import gevent
from gevent import Timeout

s = time.time()

def wait(pid):
    print 'wait start {0}'.format(pid)
    gevent.sleep(2)
    print 'wait end {0}'.format(pid)

timer = Timeout(3).start()
thread1 = gevent.spawn(wait, 1)

try:
    thread1.join(timeout=timer)
except Timeout:
    print 'thread 1 time out'

timer = Timeout.start_new(1)
thread2 = gevent.spawn(wait, 2)

try:
    thread2.get(timeout=timer)
except Timeout:
    print 'thread 2 time out'

try:
    gevent.with_timeout(1, wait, 3)
except Timeout:
    print 'thread 3 time out'

print time.time() - s
