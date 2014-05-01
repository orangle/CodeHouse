#-*- coding: utf-8 -*-
__author__ = 'orangleliu'
__edate__ = '2014-05-01'
__pythonv__='python2.7.x'

'''
获取百度 蓝汛 网易股价
通过对网页分析获得页面信息
'''

import urllib
import re

gupiaos = ['CCIH']
regex = '<li id="zxj" class="light">(.+?)</li>'
pattern = re.compile(regex)


for gupiao in gupiaos :
    url_head = r'http://quote.eastmoney.com/us/CCIH.html?StockCode='
    url = url_head + gupiao

    htmlfile = urllib.urlopen(url)
    html = htmlfile.read()

    #因为是使用js获取的，所以直接抓页面行不通
    stock = re.findall(pattern, html)
    print stock


