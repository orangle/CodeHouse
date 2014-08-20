#coding: utf-8

from __future__ import print_function
import sys

urls = ['www.baidu.com','www.sohu.com',
        'www.sina.com','www.google.com',
        'www.orangleliu.info']
import gevent
from gevent import monkey 

monkey.patch_all()

from urllib2 import urlopen

def print_head(url):
    print ('start %s'%url)
    data = urlopen(url).read()
    print ('%s:%s bytes: %s'%(url, len(data), data[:50]))

jobs = [gevent.spawn(print_head, 'http://'+url) for url in urls]

#gevent.wait(jobs)
gevent.joinall(jobs, timeout=2)

