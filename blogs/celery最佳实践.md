Celery最佳实践
============

>[orangleliu](http://blog.csdn.net/orangleliu) 翻译  [原文点击查看](https://denibertovic.com/posts/celery-best-practices/)

 如果你的工作和 [Django](https://www.djangoproject.com/) 相关, 并且有时候需要执行一些长时间的后台任务。可能你已经使用了某种任务队列，[Celery](http://www.celeryproject.org/)就是Python（和Django）世界中时下解决类似问题最受欢迎的项目。

当在某些项目使用Celery作为任务队列之后，我总结了一些最佳实践，决定把它们些下来。然而，这里也有一些对自己应该做的却没做的反思，还有一些celery提供但是没有充分利用的功能。

###No.1  不要使用关系型数据库来作为AMQP的代理

让我来解释下我为什么觉得这是错的。

关系型数据库不像RabbitMQ一样专门作为AMQP代理而设计。它会在某个时间点挂掉，可能在生产中没法那么基于 传输/用户。

我猜测人们使用关系型数据库的最大原因是，已经有了一个数据库为web应用工作，为啥不复用呢。配置非常简单并且你不需要在担心其他的组件（像RabbitMQ）

假设这样的场景：你有4个后台工作的进程，你把这些任务放到数据库中。这意味着有四个进程相当频繁地去数据库轮询，检查是否有新的任务，这还不包括这4个进程本身也是多个进程。在某些时刻你会发现你的任务进程很慢，有些任务还没处理就有更多的任务进来了，你就自然的增加worker来处理任务。大量的worker为了获取新任务轮询数据库，导致数据库突然变慢，磁盘IO达到瓶颈，你的web应用也会受此影响变得越来越慢，因为这些worker正在对数据库进行基本的DDOS 攻击。

当你有一个像RabbitMQ这样的AMQP代理的时候，这些情况就不会发生了，因为这些队列是存在于内存当中，所以也不会伤害到你的硬盘。这些worker不需要频繁的轮询，因为队列会把新的任务推送给worker，如果AMQP因为某些原因不能工作了，至少不会影响到web应用的所有使用。

我不得不说你也不应该在开发环境中使用关系型数据库来作为代理，像Docker和预先建立好的镜像都能给你一个沙盒中的RabbitMQ环境使用。

###NO.2 使用多个Queues（队列），不要只是使用默认的那个（default）
Celery的启动是相当的简单，它会启动一个默认的队列，除非你定义了别的队列否则它就会把所有的任务放到这一个队列中去。最常见的就是像下面这样。

    @app.task()
    def my_taskA(a, b, c):
        print("doing something here...")

    @app.task()
    def my_taskB(x, y):
        print("doing something here...")

两个任务会放到同一个队列中去(如果没有在celeryconfig.py中配置).我能清楚的看到有哪些事发生，因为你那些可人的后台任务上仅仅有那么一个 装饰器。这里我关心的是，也许 taskA 和 taskB做的是完全不同的两件事情，也许其中一个要比另外一个重要的多，那为什么要把它们扔到一个篮子里呢？虽然一个worker可以处理这两个任务，设想某个时间有大量的taskB，然而更重要的 taskA却没有得到worker的足够重视？这种情况下增加了worker以后，所有的worker还是会平等的对待这两种任务，在大量taskB的情况下，taskA还是无法得到应得的重视。 这就把我们带到了下一个要点中。

###NO.3 使用优先级wokers

解决上面问题办法就是把taskA放到一个队列中去，taskB放到另一个队列中去，分配x个workers去处理Q1队列，有于Q2队列有更多的任务需要处理，其他的workers都分配给Q2队列。这种方式你能保证taskB有足够多的workers去，同时维持几个高优先级的队列给taskA，当taskA任务来的时候不需要等待很久就可以被处理掉。

所以，手工的定义队列

    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('for_task_A', Exchange('for_task_A'), routing_key='for_task_A'),
        Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),
    )

你的routes 会决定不同的任务分配到不同的队列

    CELERY_ROUTES = {
        'my_taskA': {'queue': 'for_task_A', 'routing_key': 'for_task_A'},
        'my_taskB': {'queue': 'for_task_B', 'routing_key': 'for_task_B'},
    }

然后你可以为每个任务启动不同的workers

    celery worker -E -l INFO -n workerA -Q for_task_A
    celery worker -E -l INFO -n workerB -Q for_task_B

###No.4 使用Celery's的错误处理机制

我见过最多就是，任务根本就没有错误处理的概念。如果一个任务失败了就是失败了。在某些情况下这样处理是不错的，然而我见过最多的是一些第三方API的错误，网络原因，或者资源不可用等造成的。最简单的处理这种错误的办法就是对任务进行重试。因为有一些第三方的API是因为服务或者网络的出了问题，但是很快就可以恢复，我们为什么不试一试呢？

    @app.task(bind=True, default_retry_delay=300, max_retries=5)
    def my_task_A():
        try:
            print("doing stuff here...")
        except SomeNetworkException as e:
            print("maybe do some clenup here....")
            self.retry(e)

我比较喜欢就是给每个任务定义一个重试的间隔和重试的次数(分别是default_retry_delay和max_retries参数)。这是最基本的错误处理方式也是我见过最多的。当然Celery还提供了很多种处理处理但是我把celery的文档地址留给你。

###No.5 使用Flower

[Flower](http://celery.readthedocs.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor) 是一个非常棒的工具，它可以用来监控celery的任务和workers。它是基于web的，所以你可以看到任务进程，详情，worker状态，启动新的workers等。可以通过前面的链接查看它所有的功能。

###No.6 只有真正需要才追踪task的结果

task状态指的是task执行的结果是成功还是失败。它对于后续的某些分析是有用的。需要注意的一个问题是退出结果并不是任务执行的结果，那些信息更类似于对数据的某些影响（例如更新用户的朋友列表）

项目中我见过最多的是不关心这些任务执行时候的状态，有些只是用默认的sqlite数据库在保存这些信息，更好一点的是花时间保存在常规的数据库中（例如postgres 或者其他数据库）

为什么无缘无故的增加web应用数据库的负担呢？使用CELERY_IGNORE_RESULT = True配置在你的celeryconfig.py配置文件中来丢弃这些执行状态。


###No.7 不要通过数据库或者ORM对象的方式来执行任务

在一次本地的Python小聚会上发表这个分享之后有几个人建议我把这一条添加到最佳实践的列表中。这个建议是关于什么的呢？不要通过数据库对象（例如你的User model）来执行后台任务，因为对象序列话是包含了一些陈旧的数据。你要作的是把Userid放在任务中，然后任务执行的时候会从数据中获取最新的用户对象。
