# -*- coding: utf-8 -*-
#threading1.py   python2.7.x
#orangleliu@gmail.com    2014-07-05
'''
简单的生产者消费者模型
see video:https://www.youtube.com/watch?v=i1SW4q9yUEs
'''

import threading, time, random
import Queue


class Producer :
    '''生产食物'''
    def __init__(self):
        self.food = ['!A','B','C','Apple','Orange','Banana']
        self.nextTime = 0

    def run(self):
        global q
        while (time.clock()<10):
            if (self.nextTime < time.clock()):
                f = self.food[random.randrange(len(self.food))]
                q.put(f)
                print "Add %s"%f
                self.nextTime += random.random()

class Customer:
    '''
    消费掉食物
    '''
    def __init__(self):
        self.nextTime = 0

    def run(self):
        global q
        while(time.clock() < 10):
            if (self.nextTime < time.clock() and not q.empty()):
                f = q.get()
                print "Remove %s"%f
                self.nextTime += random.random()*2


if __name__ ==  "__main__":
    q = Queue.Queue(10)

    p = Producer()
    c = Customer()

    pt =  threading.Thread(target=p.run, args=())
    ct =  threading.Thread(target=c.run, args=())
    pt.start()
    ct.start()


