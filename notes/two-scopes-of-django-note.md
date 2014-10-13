Settings and Requirements Files
=======================

> Two Scoops of Django 读书笔记，基于django1.5，第五章 settings和requements 最佳实践

#####some Tips
*  All settings files need to be version-controlled.
*  Don't Repeat Yourself. 应该是继承基本的配置文件，而不是从一个文件粘贴到另一个文件
*  Keep secret keys safe.  密码不应该放在版本控制中


#####案例
开发环境的配置可以使用local_settings.py，针对开发环境配置一些信息，不要放到svn中。我们把开发，测试，生产环境的配置分开，让他们都继承一个基础的配置文件，这个基础的配置文件是放在svn中的。

文件的结构：

    settings
        |___ base.py
        |___ local.py
        |___ test.py
        |___ __init__.py

base.py 是基础的配置，其他都是不同环境下的配置
怎么使用呢，只要在执行命令的时候加上 --settings=..  选项就行了
eg

    python manage.py runserver --settings=nirvana.settings.local

base.py中类似django自动生成的settings.py中的内容。local.py中可以这样写。

    #-*- coding: utf-8 -*-

    from .base import *

    DEBUG = TEMPLATE_DEBUG = True
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nirvana',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '3306',
    }
    }
    INSTALLED_APPS  += ('debug_toolbar',)

在多人开发的环境中，每个人都有自己不同的配置，共享一个dev.py 是不行的。







