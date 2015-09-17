django 利用多线程增加异步任务
========================

>看到django异步大家的反应应该是celery这种消息队列组件，现在用的最多的最推荐的也是这种方式。然而我这需求就是
请求来了，执行一个小程序，但是又不能确定这个小程序啥时候执行完，响应又要及时，丢给队列处理当然可以，但是
为了简单，决定直接起个线程跑跑。 （当然这只是实验，应用规模也很小，如果并发高，会有很多问题）

从view.py中截取了这段代码:

    @login_required
    def search_area(request):
        prints = PrintThread()
        prints.start()

        return retrieve(request, 'Area', 'areasearche.html', [{'name':'areaname', 'mode': 'contains'}])

    ##通过thread 实现django中
    import threading
    import time
    class PrintThread(threading.Thread):
        def run(self):
            print "start.... %s"%(self.getName(),)
            for i in range(30):
                time.sleep(1)
                print i
            print "end.... %s"%(self.getName(),)

从执行的结果来看是可以完成需求的，

    start.... Thread-7
    0
    1
    2
    [24/Oct/2014 15:09:30] "GET /media/js/hawk.js HTTP/1.1" 304 0
    3
    ...
    26
    27
    28
    29
    end.... Thread-7

对于定时延迟任务，还有高并发的异步任务还用mq来的方面。
