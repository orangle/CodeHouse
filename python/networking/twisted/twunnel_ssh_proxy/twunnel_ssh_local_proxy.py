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

def start_LOCAL_PROXY_SERVER():
    global port_LOCAL_PROXY_SERVER

    configuration = \
    {
        "PROXY_SERVERS": [],
        "LOCAL_PROXY_SERVER":
        {
            "TYPE": "SOCKS5",
            "ADDRESS": "127.0.0.1",
            "PORT": 1081  #本地应用设置的代理端口
        },
        "REMOTE_PROXY_SERVERS":
        [
            {
                "TYPE": "SSH",
                "ADDRESS": "45.78.37.246", #远程是开启了ssh的一个服务器
                "PORT": 2222,  #一般为端口22
                "KEY":
                {
                    "FINGERPRINT": ""
                },
                "ACCOUNT":
                {
                    "NAME": "lzz",  #ssh 账户
                    "PASSWORD": "123456", #ssh密码
                    "KEYS":
                    [
                        {
                            "PUBLIC":
                            {
                                "FILE": "KP.pem", #generate.py 生成的key
                                "PASSPHRASE": ""
                            },
                            "PRIVATE":
                            {
                                "FILE": "KP.pem",
                                "PASSPHRASE": ""
                            }
                        }
                    ],
                    "CONNECTIONS": 2
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
