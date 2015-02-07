# -*- coding: utf-8 -*-
#multiprocess_2.py   python2.7.x
#orangleliu@gmail.com    2014-05-04
'''
一次执行多个进程，保持进程的顺序（多用一个key就行了）
'''

import multiprocessing as mp
import random
import string

output = mp.Queue()

def get_string(lnum, output):
    newstr =str(lnum)*3
    output.put((lnum, newstr))


if __name__ == "__main__":
    #在windows下必须有__name__ 这个分装，否则会报错
    processes = [mp.Process(target=get_string, args=(x, output)) for x in range(10)]
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    
    res = [output.get() for p in processes ]
    print res
    res.sort()
    print [ i[1] for i in res ]