#coding: utf-8
__author__= 'orangleliu'
__version__ = '0.1'

'''
filename: soaplib_test.py
createdate: 2014-05-10
comment: webservice 简单学习

这是官网的一个demo  调试看看
参考链接：
http://soaplib.github.io/soaplib/2_0/pages/helloworld.html#declaring-a-soaplib-service
http://www.cnblogs.com/grok/archive/2012/04/29/2476177.html

http://www.cnblogs.com/lm3515/archive/2010/10/29/1864456.html
http://www.cnblogs.com/macroxu-1982/archive/2009/12/23/1630415.html
http://192.168.100.109:8000/webservices/SOAProvider/plsql/cux_ccih_yz/?wsdl

服务启动之后可以在浏览器： http://localhost:7789/?wsdl
得到一个xml文件，具体怎么解读还需要查看资料

需要研究下怎么手动写一个http客户端来请求webservice
'''
import soaplib
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array


class HelloWorldService(DefinitionBase):
    @soap(String,Integer,_returns=Array(String))
    def say_hello(self,name,times):
        results = []
        for i in range(0,times):
            results.append('Hello, %s'%name)
        return results

if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([HelloWorldService], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('localhost', 7789, wsgi_application)
        print 'soap server starting......'
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"


