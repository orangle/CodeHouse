#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu@gmail.com 2014-12-12
#psutiltest.py
'''
照着教程简单学习下psutil的使用，windows下试试
'''
import psutil
import datetime

#查看cpu的信息
print u"CPU 个数 %s"%psutil.cpu_count()
print u"物理CPU个数 %s"%psutil.cpu_count(logical=False)
print u"CPU uptimes"
print psutil.cpu_times()
print ""

#查看内存信息
print u"系统总内存 %s M"%(psutil.TOTAL_PHYMEM/1024/1024)
print u"系统可用内存 %s M"%(psutil.avail_phymem()/1024/1024)
mem_rate = int(psutil.avail_phymem())/float(psutil.TOTAL_PHYMEM)
print u"系统内存可用率 %s %%"%int(mem_rate*100)

#系统启动时间
print u"系统启动时间 %s"%datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

#系统用户
users_count = len(psutil.users())
users_list = ",".join([ u.name for u in psutil.users()])
print u"当前有%s个用户，分别是%s"%(users_count, users_list)

#网卡，可以得到网卡属性，连接数，当前流量等信息
net = psutil.net_io_counters()
bytes_sent = '{0:.2f} kb'.format(net.bytes_recv / 1024)
bytes_rcvd = '{0:.2f} kb'.format(net.bytes_sent / 1024)
print u"网卡接收流量 %s 网卡发送流量 %s"%(bytes_rcvd, bytes_sent)

#进程  进程的各种详细参数
#磁盘 磁盘的使用量等等



