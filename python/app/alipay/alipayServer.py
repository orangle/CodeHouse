#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-16
#alipayServer
'''
模拟接收支付宝充值请求和返回交易信息处理
'''
import hashlib
import threading
import urllib, urllib2
import time

from flask import Flask
from flask import request
app = Flask(__name__)

partner_g = "2088601262123456"
notify_id_g = "alicc20141212sssdfe"
key_g = "zc7nunumgwfmiisnc5nnnwy9gxxffsdfd2"
input_charset_g = "UTF-8"

@app.route("/cooperate/gateway.do", methods=['POST', 'GET'])
def gateway():
    '''
    接收用户发来的交易信息
    '''
    if request.method == "POST":
        params = {}
        params["retusn_url"] = request.form.get("return_url", "")
        params["notify_url"] = request.form.get("notify_url", "")
        params["sign_type"] = request.form.get("sign_type", "")
        params["sign"] = request.form.get("sign", "")
        params["out_trade_no"] = request.form.get("out_trade_no", "")
        params["extra_common_param"] = request.form.get("extra_common_param", "")
        params["service"] = request.form.get("service", "")
        params["paymethod"] = request.form.get("paymethod", "")
        params["total_fee"] = request.form.get("total_fee", 0)
        params["partner"] = request.form.get("partner", "")

        for i, j in params.items():
            print "POST=> %s  %s"%(i, j)

        notf = NotifyTread(params)
        notf.start()
        return "OK!"
    else:
        return "Not ok!"

@app.route("/trade/notify_query.do")
def notify_query():
    '''
    当通知用户交易结果的时候，用户通过这个url校验是否支付宝已经发出校验信息
    '''
    spartner = request.args.get("partner")
    notify_id = request.args.get("notify_id")
    print spartner, partner_g
    print spartner==partner_g
    print notify_id==notify_id_g

    if spartner==partner_g and notify_id==notify_id_g:
        return "true"
    else:
        return "false"

def notify_tran(params):
    '''
    异步的通知支付结果
    '''
    #需要签名的参数，这里只是把需要的参数做签名，实际可能要更多
    '''
    notify_id           #通过和支付宝交互，再次校验id是否正确
    notify_type         #支付宝
    trade_no
    out_trade_no        请求中
    total_fee              请求中
    trade_status
    buyer_email
    buyer_id
    gmt_payment
    gmt_close
    extra_common_param  请求中

    不需要签名
    sign
    sign_type
    '''
    sign_params = {}
    sign_params["notify_id"] = notify_id_g
    sign_params["notify_type"] = "trade_status_sync"
    sign_params["trade_no"] = "2014040311001004370000361525"
    sign_params["trade_status"] = "TRADE_SUCCESS" #"TRADE_FINISHED"
    sign_params["buyer_email"] = "orangleliu@gmail.com"
    sign_params["buyer_id"] = "2088002007013600"
    sign_params["gmt_payment"] = "2014-10-22 20:49:50"
    sign_params["gmt_close"] = "2014-11-22 20:49:50"
    sign_params["extra_common_param"] = params.get("extra_common_param")
    sign_params["out_trade_no"] = params.get("out_trade_no")
    sign_params["total_fee"] = params.get("total_fee")

    sign_params["sign"] = md5Sign(sign_params)
    sign_params["sign_type"] = params.get("sign_params")
    notify_url = params.get("notify_url")
    #urllib2 回调给用户
    encoded_args = urllib.urlencode(sign_params)
    print "notify_params:  %s"%encoded_args
    print "notify_url : %s"%notify_url
    reps = urllib2.urlopen(notify_url, encoded_args)
    print "notify_result: %s"%reps.read()

def md5Sign(params):
    names = params.keys()
    names.sort()
    s=u""
    for name in names:
        s=u"%s&%s=%s"%(s,name,params[name])
    s=s[1:]+key_g
    md5=hashlib.md5()
    md5.update(s.encode(input_charset_g))
    return md5.hexdigest()

class NotifyTread(threading.Thread):
    def __init__(self, params):
        threading.Thread.__init__(self)
        self.params = params

    def run(self):
        time.sleep(3)
        print "start notify............"
        try:
            notify_tran(self.params)
        except Exception as e:
            print "notify error ......"
        print "end notify.............."

if __name__ == '__main__':
    app.run(debug=True, port=8080)
