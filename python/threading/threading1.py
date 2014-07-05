# -*- coding: utf-8 -*-
#threading1.py   python2.7.x
#orangleliu@gmail.com    2014-07-05
'''
多线程的使用
threading  is old and outdate
better choice is threading

see video:https://www.youtube.com/watch?v=i1SW4q9yUEs
'''
import threading, random

def Splitter(words):
    str_list = words.split()
    new_list = []
    while (str_list):
        new_list.append(str_list.pop(random.randrange(0, len(str_list))))
    print (' '.join(new_list))

if __name__ == '__main__':
    sentance = "This is new day, do you like shijian ? ok ok ok ok "
    numOfThreads = 5
    threadList = []

    for i in range(numOfThreads):
        t = threading.Thread(target=Splitter, args=(sentance,))
        t.start()
        threadList.append(t)

    print ("Thread count is "+str(threading.activeCount()))
    print ('Exiting ...')


