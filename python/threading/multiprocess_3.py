# -*- coding: utf-8 -*-
#multiprocess_3.py   python2.7.x
#orangleliu@gmail.com    2014-12-29
'''
多进程同时启动，然后对任务消费，最后等待结果，结果收集完毕才退出
类似Pool的功能
'''

import multiprocessing
import time

class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.tq = task_queue
        self.rq = result_queue

    def run(self):
        #一直做任务，指导任务为空的时候退出
        proc_name = self.name
        while True:
            next_task = self.tq.get()
            if next_task is None:
                print '%s: Exiting'%proc_name
                self.tq.task_done()
                break
            print '%s: %s'%(proc_name, next_task)
            ans = next_task()
            self.tq.task_done()
            self.rq.put(ans)
        return

class Task(object):
    def __init__(self, a ,b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)
        return '%s + %s = %s'%(self.a, self.b, self.a+self.b)

    def __str__(self):
        return '%s + %s'%(self.a, self.b)

if __name__ == "__main__":
    #任务队列 和 结果队列
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    #根据主机core数目 生成消费队列
    num_con = multiprocessing.cpu_count()*2
    conss = [Consumer(tasks, results) for i in xrange(num_con)]
    for w in conss:
        w.start()

    num_jobs = 100
    for i in xrange(num_jobs):
        tasks.put(Task(i, i))

    #添加NOne任务，可以让消费者停止
    for i in xrange(num_con):
        tasks.put(None)

    tasks.join()

    while num_jobs:
        print results.get()
        num_jobs -= 1




