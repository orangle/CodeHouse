#coding: utf-8
__author__= 'orangleliu'
__version__ = '0.1'

'''
filename: soaplib_ad.py
createdate: 2014-05-10
comment: webservice 复杂的接受数据的返回数据
传入参数为一个类的集合
返回数据为一类

这是官网的一个demo  调试看看
参考链接：
http://soaplib.github.io/soaplib/2_0/pages/helloworld.html#declaring-a-soaplib-service
http://www.cnblogs.com/grok/archive/2012/04/29/2476177.html

直接执行pyhton文件就可以把webservice启动了
服务启动之后可以在浏览器： http://localhost:7789/?wsdl
'''
import soaplib
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
from soaplib.core.model.clazz import ClassModel

class ResInfo(ClassModel):
    __namespace__ = "resinfo"
    confirmation_id = Integer
    status = String
    detail = String
    
class Confirmation(ClassModel):
    __namespace__ = "comfirmation"
    confirmation_id = Integer
    invoice_type = String
    return_type = String
    fee_detail_id = Integer 
    charge_id = Integer
    invoice_no = String 
    invoice_date = String  #yyyy-mm-dd 
    company = String 
    original_invoice = String  #多个用-分割
    bill_id = Integer


class InvoiceReturnService(DefinitionBase):
    @soap(Array(Confirmation),_returns=ResInfo)
    def invoice_return(self, confirmation_list):
        try:
            print confirmation_list
            res = ResInfo()
            res.confirmation_id = 1
            res.status = 'Y'
            res.detail = u'正常'
        except Exception,e:
            print str(e)
            res = ResInfo()
            res.confirmation_id = 0
            res.status = 'N'
            res.detail = str(e)
        return res

if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([InvoiceReturnService], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('localhost', 7789, wsgi_application)
        print 'soap server starting......'
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"
