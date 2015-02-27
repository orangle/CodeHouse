# -*- coding: utf-8 -*-
#author: orangleliu@gmail.com
#python2.7.x
'''
为了模拟的更像，需要添加请求头，访问频度控制，在一定情况下还需要用代理
尽可能的真实的再现浏览器的访问状态
TODO: 
1 抓取文章的url，存储到json中，序列化到文件中，频度为大于一个月
2 代理抓取，存到一个文件里，然后每天更新一次这个文件
3 使用代理访问博客

'''
import re
import time 
import random
import sys
from urlparse import urljoin
from urllib import urlencode
import requests

header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Encoding": "gzip,deflate,sdch",
          "Accept-Language": "zh-CN,zh;q=0.8",
          "Host": "blog.csdn.net",
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"}

def capture_all_articles(domain="http://blog.csdn.net", blog="orangleliu"):
    '''
    根据博客的地址，抓取所有文章的url
    '''
    base_url = urljoin(domain, blog)
    param = {"viewmode":"contents"}
    url = "%s?%s"%(base_url, urlencode(param))
    url_re = re.compile('''<span class="link_title"><a href="(.+?)"''')
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        urls = url_re.findall(r.text)
    else:
        print "error..."
        sys.exit(1)
    return urls
    
def page_view(url, domain="http://blog.csdn.net",num=None):
    '''
    针对某一个文章进行访问
    '''
    num = num or 0
    url = urljoin(domain, url)
    r = requests.get(url, headers=header)
    print r.reason,url,num
    
def main():
    #30到1分钟刷新一次，一共刷新30次
    urls = capture_all_articles()
    NUM = 100
    for i in xrange(NUM):
        url = random.choice(urls)
        page_view(url,num=i+1)
        seds = random.randint(20, 40)
        print "sleep %s s"%seds
        time.sleep(seds)
        
main()
