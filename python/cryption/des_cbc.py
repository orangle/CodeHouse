#coding:utf-8
#用跟lua des对比，学习ffi等知识

from Crypto.Cipher import DES

iv = "npr^(dg2"
key = "a)q7unz9"
mode = DES.MODE_CBC
cipher = DES.new(key, mode, iv)
