#coding:utf-8
#orangleliu py2.7
#recv_signal.py

import signal
import time
import sys
import os

def handle_int(sig, frame):
    print "get signal: %s, I will quit"%sig
    sys.exit(0)

def handle_hup(sig, frame):
    print "get signal: %s"%sig


if __name__ == "__main__":
    signal.signal(2, handle_int)
    signal.signal(1, handle_hup)
    print "My pid is %s"%os.getpid()
    while True:
        time.sleep(3)
