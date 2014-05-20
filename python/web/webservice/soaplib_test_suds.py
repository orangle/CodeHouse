#coding: utf-8
__author__= 'orangleliu'
__version__ = '0.1'

'''
filename: soaplib_test_suds.py
create date: 2014-05-12
debug sudus访问soaplib服务端的内容 来看看怎么用soap xml写http请求
参考文章：https://mail.python.org/pipermail/soap/2011-July/000494.html
'''

import logging
from suds.client import Client

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    hello_client = Client('http://localhost:7789/?wsdl', cache=None)
    result = hello_client.service.say_hello("Dave", 5)
    print result


'''
DEBUG:suds.client:sending to (http://localhost:7789/?wsdl)
message:
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="tns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <ns0:Body>
      <ns1:say_hello>
         <ns1:name>Dave</ns1:name>
         <ns1:times>5</ns1:times>
      </ns1:say_hello>
   </ns0:Body>
</SOAP-ENV:Envelope>
DEBUG:suds.client:headers = {'SOAPAction': u'"say_hello"', 'Content-Type': 'text/xml; charset=utf-8'}
DEBUG:suds.client:http succeeded:
<?xml version='1.0' encoding='utf-8'?>
<senv:Envelope xmlns:wsa="http://schemas.xmlsoap.org/ws/2003/03/addressing" xmlns:tns="tns" xmlns:plink="http://schemas.xmlsoap.org/ws/2003/05/partner-link/" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:senc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s12env="http://www.w3.org/2003/05/soap-envelope/" xmlns:s12enc="http://www.w3.org/2003/05/soap-encoding/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:senv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"><senv:Body><tns:say_helloResponse><tns:say_helloResult><tns:string>Hello, Dave</tns:string><tns:string>Hello, Dave</tns:string><tns:string>Hello, Dave</tns:string><tns:string>Hello, Dave</tns:string><tns:string>Hello, Dave</tns:string></tns:say_helloResult></tns:say_helloResponse></senv:Body></senv:Envelope>
(stringArray){
   string[] =
      "Hello, Dave",
      "Hello, Dave",
      "Hello, Dave",
      "Hello, Dave",
      "Hello, Dave",
 }
'''
