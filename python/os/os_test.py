#-*- coding: utf-8 -*-
#python2.7x
#author: orangleliu  @2014-05-24
'''
os模块的简单使用 wini7下
'''

import os


#执行shell命令
print os.system('dir')

#获取某些环境变量的值,os.environ得到的是一个字典，可以进行增删改查等操作
print os.environ.get('path')

#等到当前的工作目录
print  os.getcwd()

#获取当前系统时间
print os.times()

#win下可以获得当前的进程ID
print os.getpid()

#列出某个路径下的所有“目录”
print os.listdir('e:')

'''
Create a directory named path with numeric mode mode.
os.mkdir(path)

Recursive directory creation function.
os.makedirs(path)

Remove (delete) the file path.
os.remove(path)

Remove directories recursively.
os.removedirs(path)

Rename the file or directory src to dst.
os.rename(src, dst)
'''







