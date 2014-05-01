#-*- coding: utf-8 -*-
__author__ = 'orangleliu'
__edate__ = '2014-05-01'

'''
获取多个网站的title,需要解决中文乱码问题
'''

import urllib
import re
import sys

urls = [r'http://www.baidu.com',
           r'http://www.souhu.com',
           r'http://www.google.com']

regex = '<title>(.+?)</title>'
pattern = re.compile(regex)

for url in urls:
    html = urllib.urlopen(url)
    #set code
    html_text = html.read().decode('utf-8', errors='ignore')
    title = re.findall(pattern, html_text)[0]
    print title
