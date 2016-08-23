#coding:utf-8
#url https://ruslanspivak.com/lsbaws-part2/

def app(environ, start_response):
    status = "200 OK"
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world from a simple WSGI application!\n']
