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

服务启动之后可以在浏览器： http://localhost:8001/?wsdl
得到一个xml文件，具体怎么解读还需要查看资料
'''
import soaplib
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import  wsgi
from soaplib.core.model.clazz import Array

class HelloWorldService(DefinitionBase):
    @soap(String, Integer, _returns=Array(String))
    def say_hello(self, name, times):
        results = []
        for i in range(0, times):
            results.append("Hello, %s" %name)
        return results

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_app = soaplib.core.Application([HelloWorldService], 'tns')
        wsgi_app = wsgi.Application(soap_app)

        server = make_server('localhost', 8001, wsgi_app)
        print u'soap service start...'
        server.serve_forever()
    except ImportError:
        pass



