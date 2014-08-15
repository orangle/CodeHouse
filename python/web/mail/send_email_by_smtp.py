#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#send_email_by_sendmail.py
#author: orangleliu
#date: 2014-08-15
'''
linux 下使用本地的smtp服务来发送邮件
前提要开启smtp服务，检查的方法
#ps -ef|grep sendmail
#telnet localhost 25
'''
import smtplib
from email.mime.text import MIMEText
from subprocess import Popen, PIPE


def get_sh_res():
    p = Popen(['/Application/2.0/nirvana/logs/log.sh'], stdout=PIPE)
    return str(p.communicate()[0])

def mail_send(sender, recevier):
    msg = MIMEText(get_sh_res())
    msg["From"] = sender
    msg["To"] = recevier
    msg["Subject"] = "Yestoday interface log results"
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [recevier], msg.as_string())
    s.quit()
    print 'send mail finished...'

if __name__ == "__main__":
    s = "zhizhi.liu@chinacache.com"
    r =  s
    mail_send(s, r)







