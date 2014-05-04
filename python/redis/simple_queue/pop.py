# -*- coding: utf-8 -*-
#pop.py   python2.7.x
#orangleliu@gmail.com    2014-05-04
'''
模拟任务队列从redis中取出
python pop.py
'''

import sys
from redis import Redis

redis = Redis(host="localhost", port=6379)
while 1:
    res = redis.rpop('time_queue')
    if res== None:
        pass
    else:
        print str(res)


