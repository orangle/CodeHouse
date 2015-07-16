# -*- coding: utf-8 -*-
# python2.7x
# author: orangelliu
# date: 2015-07-08

import sys
import gevent
from gevent import monkey
#patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import urllib2

url='http://baidu.com'
#sys.stdout = open('res.log', 'w')

def print_head(url, j, i):
  data=urllib2.urlopen(url).read()
  print '第%s轮第%s次处理结果 %s: %s bytes: %r' %(j,i,url,len(data),data[:10])

for j in range(10):
    print "第%s轮攻击开始"%j
    jobs=[gevent.spawn(print_head,url,j,i) for i in range(10)]
    gevent.joinall(jobs)

