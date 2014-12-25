# -*- coding: utf-8 -*-
#multiprocess_4.py   python2.7.x
#orangleliu@gmail.com    2014-12-25
'''
多进程Pool的使用
Pool.apply
Pool.map
Pool.apply_async
Pool.map_async
'''

import multiprocessing as mp
import random
import string


def get_string(lnum):
    newstr =str(lnum)*3
    return newstr

if __name__ == "__main__":
    pool = mp.Pool(processes=4)
    results = [pool.apply(get_string, args=(x,)) for x in range(1,7)]
    print results


