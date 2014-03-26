#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x      django_orm_use.py   zhizhi.liu@2014-03-21

import sys,os
#pro_dir = ''  #可以自己用绝对路径定义,目的是工程目录下
pro_dir = os.getcwd()  #如果放在project目录，就不需要在配置绝对路径了
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] ='nirvana.settings'  #项目的settings

from django.core.management import setup_environ
import settings    #导入settings
setup_environ(settings)  #设置settings


#===============调用代码部分================
from userManage.models import UserProfile

print UserProfile.objects.all().count()



