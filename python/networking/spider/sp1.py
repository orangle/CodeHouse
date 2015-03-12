#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: sp1.py
#Author: orangleliu
#Mail: orangleliu@gmail.com
#Created Time: 2015-02-09 20:21:24
############################
'''
simple spider use twisted
https://gist.github.com/hemanth/5272451
'''
import re
from twisted.web.client import getPage
from twisted.python.util import println
from twisted.python import log
from twisted.internet import defer, task
from bs4 import BeautifulSoup

def parallel(iterable, count, callable, *args, **named):
    coop = task.Cooperator()
    work = (callable(elem, *args, **named) for elem in iterable)
    return defer.DeferredList([coop.coiterate(work) for i in xrange(count)])

def union(p, q):
    for e in p:
        if e not in q:
            print e
            q.append(e)

def extract_links(html):
    soup = BeautifulSoup(html)
    soup.prettify()
    urls = [str(anchor["href"]) for anchor in soup.findAll('a', \
            attrs={'href':re.compile("^http://")}) if anchor["href"]]
    return urls 

def crawl_page(url, urllist):
    d = getPage(url)
    d.addCallback(extract_links)
    d.addCallback(union, urllist)
    d.addCallback(log.err)
    return d 

def crawler(urls):
    urls = list(urls)

def main(reactor, *args):
    urls = list(args)
    print "grab url %s"%urls
    return parallel(urls, len(urls), crawl_page, urls)

if __name__ == '__main__':
    import sys
    task.react(main, ["http://www.orangleliu.info",\
            "http://blog.csdn.net/orangleliu"])
