django-orm 聚合函数的使用
====================

>orm对于普通的单表条件查询和多表的关联查询支持力度还可以，基本可以满足不是很复杂的业务场景，对于聚合函数也有一些支持，之前基本都没有用过，大部分都是使用raw sql来写的，今天把orm的聚合方法学习下，对于简单的聚合还是用orm自身来解决吧。

一下笔记是基于django1.6

##[django中提供的聚合方法](https://docs.djangoproject.com/en/1.6/ref/models/querysets/#aggregation-functions)
* Avg 求平均值，数字类型的字段支持
* Count 统计个数， 可以增加dictinct选项 一般和annotate一起使用
* Max 最大值
* Mix  最小值
* StdDev 计算给出字段的标准差
* Sum 计算字段的和
* Variance 计算字段的方差

##[聚合方法的使用](https://docs.djangoproject.com/en/1.6/topics/db/aggregation/)
[文档地址](https://docs.djangoproject.com/en/1.6/topics/db/aggregation/)

模型参见文档,这些查询都是可以和filter，order_by等一起使用的
>  from django.db import models
    class Author(models.Model):
        name = models.CharField(max_length=100)
        age = models.IntegerField()

    class Publisher(models.Model):
        name = models.CharField(max_length=300)
        num_awards = models.IntegerField()

    class Book(models.Model):
        name = models.CharField(max_length=300)
        pages = models.IntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        rating = models.FloatField()
        authors = models.ManyToManyField(Author)
        publisher = models.ForeignKey(Publisher)
        pubdate = models.DateField()

    class Store(models.Model):
        name = models.CharField(max_length=300)
        books = models.ManyToManyField(Book)
        registered_users = models.PositiveIntegerField()

查询例子

    #得到所有书的总量
    Book.objects.count()
    #求平均值，最大值，最小值用法基本相似
    from django.db.models import Avg
    Book.objects.all().aggregate(Avg('price'))
    {'price__avg': 34.35}  #返回值是一个字典类型，key的名字好像不是很友好

    #计算每个出版社，出版书的数目
    from django.db.models import Count
    pubs = Publisher.objects.annotate(num_books=Count('book'))
    #计算所有出版社出版书数目最多的5个出版社
    pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
    pubs[0].num_books
    1323

    #返回值别名
    Book.objects.aggregate(average_price=Avg('price'))  #添加了一个average_price来作为返回值的key
    {'average_price': 34.35}

    #连表查询  跟filter中很相似使用 __来关联到其他表
    Store.objects.aggregate(min_price=Min('books__price'), max_price=Max('books__price'))

    #也可以把聚合和计数同时使用
    #计算每个作者平均出版书的数目
    from django.db.models import Count, Avg
    Book.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))

以上只是对文档的理解，具体使用还需要具体看业务需求。











