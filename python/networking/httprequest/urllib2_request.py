#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-16
#urllib2_request.py
'''
使用urllib2 请求数据的几种不同情况
urllib2 在多线程或者是协程中使用需要注意
'''
import urllib2
import urllib
import json

'''
#简单的获取页面信息
resp = urllib2.urlopen("http://orangleliu.info")
print resp.code
print "url: %s"%resp.geturl()
print u"header -----------------"
print resp.info()

print "-"*30

#post请求， 自定义header请求，json请求
query = {"wd": "cc", "ie": "utf-8"}
query_args = urllib.urlencode(query)
#post
#resp = urllib2.urlopen("http://baidu.com", query_args)
#get
resp = urllib2.urlopen("http://baidu.com/?%s"%query_args)

print u"带有参数的请求"
print "Dict encode : %s"%query_args
print resp.code
print resp.geturl()
print "-"*30

#更复杂的需要用Request对象来构建
query = {"wd": "cc", "ie": "utf-8"}
#get
request = urllib2.Request("http://baidu.com/?" + urllib.urlencode(query))
#post
#request.add_data(urllib.urlencode(query))
request.add_header("(iPhone; CPU iPhone OS 7_1_2 like Mac OS X) \
    AppleWebKit/537.51.2 (KHTML, like Gecko)", "http://orangleliu.info")
print request.get_method()
resp = urllib2.urlopen(request)
print resp.code
'''

#使用urllib2 发送json数据
json_datas = {"1": [1,3,4]}
req = urllib2.Request('http://baidu.com/')
req.add_header('Content-Type', 'application/json')
resp = urllib2.urlopen(req, json.dumps(json_datas))
print resp.code






