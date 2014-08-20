#coding: utf-8
#author: orangelliu
#date: 2014-08-20

from gevent import pywsgi
def hello_world(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    yield '<h1>Orangleliu</h1>'

sever = pywsgi.WSGIServer(
        ('0.0.0.0', 8080), hello_world)

sever.serve_forever()
