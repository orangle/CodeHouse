#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#atuo_deploy_by_fabric.py

'''
使用fabric自动部署现有的django项目

fab  -f filename op
'''

from fabric.api import *
from datetime import datetime

PRODUCT_DIR = r"/Application/2.0/"
BACKUP_NAME = "nirvana"+datetime.strftime(datetime.now(), '%m%d')

env.hosts =["192.168.100.235"]
env.user = "root"
env.password = "xxxxx"

def get_codes():
    #get resource codes
    with cd(PRODUCT_DIR):
        run("rm -f nirvana-0.0.1.tar.gz")
        run(r"wget http://192.168.100.230:8080/job/nirvana/lastSuccessfulBuild/artifact/dist/nirvana-0.0.1.tar.gz")
        run("tar zxvf nirvana-0.0.1.tar.gz")

def stop_server():
    with cd(PRODUCT_DIR+"/nirvana"):
        print u"关闭当前服务"
        run("killall -9 uwsgi")
        run("ps -ef|grep celery|grep -v grep|awk '{print $2}'|xargs kill -9")

def backup_codes():
    with cd(PRODUCT_DIR):
        try:
            run('mv nirvana '+BACKUP_NAME)
        except:
            print u"当前没有nirvana目录"

        run('ls -al')
        run('mv nirvana-0.0.1 nirvana')

def install_project():
    with cd(PRODUCT_DIR):
        print u'开始备份数据'
        run("cp ./"+BACKUP_NAME+"/settings.py ./nirvana")
        run("cp -r ./"+BACKUP_NAME+"/logs ./nirvana/")
        run("mkdir nirvana/statics/typeface")
        run("mv ./"+BACKUP_NAME+"/statics/typeface/simsun.ttc ./nirvana/statics/typeface/")

def sync_db():
    with cd(PRODUCT_DIR+"/nirvana"):
        run("python manage.py syncdb")

def start_server():
    with cd(PRODUCT_DIR+"/nirvana"):
        print u'启动nirvana服务'
        run("uwsgi -x uwsgi.xml")
        run("nohup python manage.py celeryd -l info&")
        #产看进程是否启动
        run("ps -ef|grep uwsgi")
        run("ps -ef|grep celery")

def deploy_nirvana():
    get_codes()
    stop_server()
    backup_codes()
    install_project()
    sync_db()
    start_server()

def restart_nirnava():
    stop_server()
    start_server()






