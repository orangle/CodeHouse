#coding:utf-8
import sys
import os

from twisted.internet import reactor, ssl
from twisted.python import log
from twunnel import local_proxy_server, logger, proxy_server, remote_proxy_server

log.startLogging(sys.stdout)

configuration = \
{
    "LOGGER":
    {
        "LEVEL": 3
    }
}

logger.configure(configuration)

port_REMOTE_PROXY_SERVER = None

def start_REMOTE_PROXY_SERVER():
    global port_REMOTE_PROXY_SERVER

    configuration = \
    {
        "PROXY_SERVERS": [],
        "REMOTE_PROXY_SERVER":
        {
            "TYPE": "SSL",
            "ADDRESS": "45.78.37.246", #主机的ip, local proxy 连接这个地址
            "PORT": 9998,           #本地proxy链接使用的端口，自定义
            "CERTIFICATE":
            {
                "FILE": "C.pem",  #ssl_ca_generate.py 生成的证书
                "KEY":
                {
                    "FILE": "CK.pem" #ssl_ca_generate.py 生成的证书
                }
            },
            "ACCOUNTS":
            [
                {
                    "NAME": "lzz",     #local proxy 使用的用户名密码，自定义
                    "PASSWORD": "lzzlovesj"
                }
            ]
        }
    }

    port_REMOTE_PROXY_SERVER = remote_proxy_server.createPort(configuration)
    port_REMOTE_PROXY_SERVER.startListening()

def stop_REMOTE_PROXY_SERVER():
    global port_REMOTE_PROXY_SERVER
    port_REMOTE_PROXY_SERVER.stopListening()

reactor.callLater(0, start_REMOTE_PROXY_SERVER)
reactor.run()
