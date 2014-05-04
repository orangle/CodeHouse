# -*- coding: utf-8 -*-
#push.py   python2.7.x
#orangleliu@gmail.com    2014-05-04
'''
模拟任务队列写入到redis中
使用方式
python  push.py  1
'''
import time
from redis import Redis
import sys

redis = Redis(host='localhost', port=6379)
while 1:
    now = time.strftime("%Y-%m-%d %H:%M:%S") + ' | ' +sys.argv[1]
    print now
    redis.lpush('time_queue', now)
    time.sleep(2)
