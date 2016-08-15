#coding:utf-8
import sys
import os


from twisted.application import service
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

port_LOCAL_PROXY_SERVER = None
port_REMOTE_PROXY_SERVER = None

def start_LOCAL_PROXY_SERVER():
    global port_LOCAL_PROXY_SERVER

    configuration = \
    {
        "PROXY_SERVERS": [],
        "LOCAL_PROXY_SERVER":
        {
            "TYPE": "SOCKS5",
            "ADDRESS": "127.0.0.1", #应用程序配置的sock5代理地址
            "PORT": 1081  #应用程序配置的socks5代理端口
        },
        "REMOTE_PROXY_SERVERS":
        [
            {
                "TYPE": "SSL",
                "ADDRESS": "45.78.37.246", #远程代理的地址
                "PORT": 9998,  #远程代理的端口
                "CERTIFICATE":
                {
                    "AUTHORITY":
                    {
                        "FILE": "CA.pem" #ssl_ca_generate.py 生成的证书
                    }
                },
                "ACCOUNT":
                {
                    "NAME": "lzz",  #跟远程代理的配置一致
                    "PASSWORD": "lzzlovesj"
                }
            }
        ]
    }

    port_LOCAL_PROXY_SERVER = local_proxy_server.createPort(configuration)
    port_LOCAL_PROXY_SERVER.startListening()

def stop_LOCAL_PROXY_SERVER():
    global port_LOCAL_PROXY_SERVER
    port_LOCAL_PROXY_SERVER.stopListening()

reactor.callLater(0, start_LOCAL_PROXY_SERVER)
reactor.run()
