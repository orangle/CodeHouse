# -*- coding: utf-8 -*-
#python2.7x
#tar.py
#orangleliu  2015-02-14
#解压tar.gz  文件, 指定目录
#todo  结果显示友好，解压到文件所在目录

import os
import sys
import tarfile
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("filename", help="the file will be extracted")
parser.add_argument("-d", "--directory", help="extract directory", action="store", default='./')
args = parser.parse_args()
filename = args.filename
directory = args.directory

try:
    if not tarfile.is_tarfile(filename):
        print u"This is not a tarfile"
        sys.exit(1)
except IOError, err:
    print u"%s"%str(err)
    sys.exit(1)

try:
    tar = tarfile.open(filename, 'r:gz')
    for item in tar:
        tar.extract(item, directory)
    print u"done success....%s解压到%s目录下"%(filename,directory)
except:
    print u"some error, stop"
