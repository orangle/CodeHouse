#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#python2.7x
#authror: zhizhi.liu
'''
删除指定目录下的.pyc 文件
'''

import sys
import os
import os.path


def deletefile(dirname):
    for root, dirs, files in os.walk(dirname):
        pyc_files = filter(lambda filename: filename.endswith(".pyc"), files)
        for pyc_file in pyc_files:
            full_path = os.path.join(root, pyc_file)
            print "Removing PYC file:", full_path
            os.remove(full_path)


if __name__ == "__main__":
    try:
        dirname = sys.argv[1]
    except:
        dirname = ""
    if dirname == "":
        print "please input a directory name"
    elif not os.path.isdir(dirname):
        print "error, it is not a right directory!"
    else:
        deletefile(dirname)
