# -*- coding: utf-8 -*-
#python2.7x
#send_email_by_sendmail.py
#author: orangleliu
#date: 2014-08-15
'''
用的是sendmail命令的方式

这个时候邮件还不定可以发出来，hostname配置可能需要更改
'''

from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def get_sh_res():
    p = Popen(['/Application/2.0/nirvana/logs/log.sh'], stdout=PIPE)
    return str(p.communicate()[0])

def mail_send(sender, recevier):
    print "get email info..."
    msg = MIMEText(get_sh_res())
    msg["From"] = sender
    msg["To"] = recevier
    msg["Subject"] = "Yestoday interface log results"
    p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    res = p.communicate(msg.as_string())
    print 'mail sended ...'

if __name__ == "__main__":
    s = "957748332@qq.com"
    r = "zhizhi.liu@chinacache.com"
    mail_send(s, r)






