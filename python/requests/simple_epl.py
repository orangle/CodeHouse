# -*- coding: utf-8 -*-
#author: orangleliu@gmail.com

import requests

#just hit a page
def hitpage():
    url = "http://orangleliu.info"
    r = requests.get(url)
    print "url: %s"%r.url
    print "content: %s ..."%r.content[:10]  #网页内容，二进制
    print "encoding: %s"%r.encoding
    print "text: %s ..."%r.text[:10]  #这里是经过自动编码过的内容
    print "raw: %s ..."%r.raw.read()[:10] #原始内容
    print "headers: %s"%r.headers.get("server")
    print "status_code: %s"%r.status_code
    print "cookies: %s"%dict(r.cookies)
    print "redirect: %s"%"Yes" if r.is_redirect else "No"
    
hitpage()