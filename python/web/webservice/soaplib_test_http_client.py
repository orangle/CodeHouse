#coding: utf-8
__author__= 'orangleliu'
__version__ = '0.1'

'''
filename:  soaplib_test_http_client.py
create date: 2014-05-12
测试怎么样使用http来调用webservice,还没有解决，
不成功 总是返回找不到方法，很奇怪，也没有soap的文档。。。。。
'''

import httplib, urllib, urllib2, time
import pprint
import xml.dom.minidom as dm

soap_host = '127.0.0.1'
soap_port = 7789

soap_body = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
soap:encodingStyle="http://www.w3.org/2001/12/soap-encoding">
  <soap:Body>
    <tns:say_hello xmlns:tns="http://localhost:7789/">
        <tns:name>orangleliu</tns:name>
        <tns:times>10</tns:times>
    </tns:say_hello>
  </soap:Body>
</soap:Envelope>
'''

req_header = { 'Content-Type' : 'text/xml; charset=utf-8' }
conn = httplib.HTTPConnection(soap_host, soap_port, timeout=10)
conn.request('POST', '/', soap_body.encode('utf-8'), req_header)
response = conn.getresponse()
data = response.read()
conn.close()

#格式化打印xml文档
xml = dm.parseString(data)
print xml.toprettyxml()







