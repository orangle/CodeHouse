#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#send_simple_email.py  @2014-07-30
#author: orangleliu

'''
使用python写邮件 simple
使用126 的邮箱服务
'''

import smtplib
from email.mime.text import MIMEText

SMTPserver = 'smtp.126.com'
sender = 'liuzhizhi123@126.com'
mailto_list = [sender]
password = "xxxx"

message = 'I send a message by Python. 你好'
msg = MIMEText(message)

msg['Subject'] = 'Test Email by Python'
msg['From'] = sender
msg['To'] = ";".join(mailto_list)

mailserver = smtplib.SMTP(SMTPserver, 25)
mailserver.login(sender, password)
mailserver.sendmail(sender, [sender], msg.as_string())
mailserver.quit()
print 'send email success'
