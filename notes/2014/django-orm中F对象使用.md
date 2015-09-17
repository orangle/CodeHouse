django-orm中F对象的使用
===================

##前言
django文档中有一节是 [Query-related classes](https://docs.djangoproject.com/en/1.7/ref/models/queries/#prefetch-objects),说
的是关联查询，1.7新加上去的，这里的关联是字段的关联，而不是表之间的关联。

表关联中主要用的是3个对象 F(), Q(), 和Prefetch()，其中Prefetch是1.7新加入的，其他两个是之前版本就有的。之前有个需求是比较一张表里的两个时间字段，[用到过F这个对象](http://blog.csdn.net/orangleliu/article/details/22273003)，今天再看djangocon的ppt时候又发现了一些新的用法，于是查询了下文档，小结一下。

##概念
> class F<br>
>F()是代表模型字段的值，也就是说对于一些特殊的字段的操作，我们不需要用python把数据先取到内存中，然后操作，在存储到db中了。

##场景
几个常用的情景

###[字段+1(加减乘除运算)](https://docs.djangoproject.com/en/1.7/ref/models/queries/#f-expressions)
例如我们有个统计点击量的字段，每次更新的操作其实就是把字段的值加1.

一般我们的做法是把这条记录取出来，把相应字段加+1，然后在save，类似下面的代码：

    # Tintin filed a news story!
    reporter = Reporters.objects.get(name='Tintin')
    reporter.stories_filed += 1
    reporter.save()

当我们使用了F()之后呢？ 只需要一行代码

    Reporters.objects.filter(name='Tintin').update(stories_filed=F('stories_filed') + 1)

不仅代码量少了，而且这是直接在数据中操作，效率也变高了，特别是并发的情况，减少了同时操作带来的隐患。

###[字段比较](https://docs.djangoproject.com/en/1.7/topics/db/queries/#using-f-expressions-in-filters)
例如一个合同有两个日期，一个叫做终止日期，一个叫做结束日期，现在要筛选出终止日期小于结束日期的合同。

    from django.db.models import F
    from contracts.models import Contracts
    contracts = Contracts.objects.filter(contract_stop_time__lt=F('end_time'))

如果没有F对象，就没法直接使用rom来查询。

##小结
现在时发现这两类用法，如果还有新的用法或者拓展，在更新。




