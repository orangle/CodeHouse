#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#python2.7x
#authror: zhizhi.liu
'''
监控80,53端口是否正常
'''

import subprocess
import shlex
import urllib2
from os import system
from datetime import datetime

URL = "http://127.0.0.1"
CMD = "dig @127.0.0.1 m.baidu.com +short"

def moniter80():
    code = urllib2.urlopen(URL).code
    if int(code) == 200:
        return True
    else:
        return False

def moniter53():
    proc=subprocess.Popen(shlex.split(CMD),stdout=subprocess.PIPE)
    out,err=proc.communicate()
    if "124.88.61.42" in out.strip() :
        return True
    else:
        return False

def sendmails(content):
    mailadds = [
            "lzz@i-erya.com",]
    subject = "Alarm of XinJiang-lianTong %s"%datetime.strftime(datetime.now(),\
                 "%Y-%m-%d %H:%M:%S")
    sendcmd = '''echo "{0}" |mail -s "{1}" {2}'''.format(content, subject,\
                 ",".join(mailadds))
    system(sendcmd)

def moniter():
    m80 = moniter80()
    m53 = moniter53()
    res = ""
    if not (m80 and m53):
        res += "http server is {0} \n".format("ok" if m80 else "down",)
        res += "dns server is {0}".format("ok" if m53 else "down",)
        print res
        sendmails(res)
    else:
        print "service is ok"

if __name__ == "__main__":
    moniter()
