#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#config_parser.py  @2014-07-25
#author: orangleliu
'''
使用 ConfigParser 模块来解析和写入配置文件，主要支持的文件类型有键值对风格的配置和json格式的配置
简单的配置应该可以应付的了
'''

import ConfigParser

config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read('conf.cfg')

#str
print config.get('mysqld', 'user')
#int
print config.getint('mysqld', 'old_passwords')
#list  一种解析方法
users = config.get('mysqld', 'users')
for i in  users.strip().split(','):
    print i

#list 另外一种解析方法,放到section里面
names = config.items("names")
for key, name in names:
    print key, name

print config.sections()
print config.has_section('default')



