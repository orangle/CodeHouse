#coding:utf-8
#orangleliu py2.7
#thread_signal.py

import signal
import threading
import os
import time

def usr1_handler(num, frame):
    print "received signal %s %s"%(num, threading.currentThread())

signal.signal(signal.SIGUSR1, usr1_handler)

def thread_get_signal():
    #如果在子线程中设置signal的handler 会报错
    #ValueError: signal only works in main thread
    #signal.signal(signal.SIGUSR2, usr1_handler)

    print "waiting for signal in", threading.currentThread()
    #sleep 进程直到接收到信号
    signal.pause()
    print "waiting done"

receiver = threading.Thread(target=thread_get_signal, name="receiver")
receiver.start()
time.sleep(0.1)

def send_signal():
    print "sending signal in ", threading.currentThread()
    os.kill(os.getpid(), signal.SIGUSR1)

sender = threading.Thread(target=send_signal, name="sender")
sender.start()
sender.join()

print 'pid', os.getpid()
#这里是为了让程序结束，唤醒pause
signal.alarm(2)
receiver.join()
