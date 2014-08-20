#!/usr/bin/python
# -*- coding: utf-8 -*-
# python2.7x
# gevent_urllib2.py
# author: orangelliu
# date: 2014-08-20

import gevent.monkey
gevent.monkey.patch_socket()

import gevent
import urllib2
import json
import threading

def fetch(pid):
	response = urllib2.urlopen('http://www.orangleliu.info')
	result = response.read()
	btypes = len(result)

	print 'process %s : %s'%(pid, btypes)

def synchronous():
	for i in range(10):
		fetch(i)

def asynchonous():
	threads = []
	for i in range(10):
		threads.append(gevent.spawn(fetch,i))
	gevent.joinall(threads)

def mulithread():
	threads = []
	for i in range(10):
		th = threading.Thread(target=fetch, args=(i,))
		threads.append(th)

	for thread in threads:
		thread.start()

	for thread in threads:
		threading.Thread.join(thread)

import time
print 'sync....'
ss = time.time()
synchronous()
print 'sync time is %s'%(time.time()-ss)

print 'async...'
sa = time.time()
asynchonous()
print 'async time is %s'%(time.time()-sa)

print 'thread...'
sm = time.time()
mulithread()
print 'thread time is %s'%(time.time()-sm)


