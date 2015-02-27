#--*-- coding:utf-8 --*--
#parse_commond_lines.py   python2.7x
'''
解析命令行  参数  显示help信息
作为一个命令行工具的模板
常用的
--help  帮助
-v  版本
-n  名字
-list  数组
'''
import argparse
VERSION = 1.0

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name",help ="input name of something", type=str)
parser.add_argument("-m", "--mulname",help ="input names of something", type=str,nargs = '*')
parser.add_argument("-v","--version", help ="the version of this tools", action="store_true")  #是个选项，不需要跟参数
args = parser.parse_args()

if args.version:
    print VERSION
elif args.name:
    print "name is %s"%args.name
elif args.mulname:
    print args.mulname
