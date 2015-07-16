# -*- coding: utf-8 -*-
import gevent;
from gevent.pool import Pool;
#from gevent import socket;
from gevent import monkey; monkey.patch_socket();

import urllib2;
import time;

start = time.time();

urls = [
"http://www.google.com/",
"http://baidu.com",
"http://orangleliu.info"
];

def grab(url):
    resp = urllib2.urlopen(url);
    return url, resp.read();

pool = Pool(12);

for url, content in pool.imap_unordered(grab, urls):
    print "<"+ str(len(content)) + ">", url;

print "Done in " + str(time.time() - start);
