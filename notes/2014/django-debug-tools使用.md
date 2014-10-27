django-debug-tools 使用
=================

>用django开发很快也很容易，但是很多时候我们的经验并不是很足，就会给自己挖下很多坑，不管是性能问题，还是开发语言使用技巧问题都会给应用的稳定带来危害， 开发之后的调试和调优就显得很重要，今天就尝试使用django-debug-toolbar来给我们的开发增加更多的调试和监控。之前只是听说过，没有具体应用过。


我这里是python1.6。  1.7的配置有点小改动，具体看[文档]((http://django-debug-toolbar.readthedocs.org/en/1.2/installation.html))。
##安装
使用pip安装

    pip install django-debug-toolbar

[参考地址](http://django-debug-toolbar.readthedocs.org/en/1.2/installation.html)

##配置
###基本配置
修改settings.py 中的配置

添加app，INSTALLED_APPS添加

    INSTALLED_APPS = (
        # ...
        'django.contrib.staticfiles',
        # ...
        # If you're using Django 1.7.x or later
        'debug_toolbar.apps.DebugToolbarConfig',
        # If you're using Django 1.6.x or earlier
        'debug_toolbar',
    )

还要设置成debug模式

    DEBUG = True

文档中说这种配置方式使用runserver 可以，但是其他方式启动可能需要就要更多的配置了。
[详细参照](http://django-debug-toolbar.readthedocs.org/en/1.2/installation.html#explicit-setup)

还有一些高级的自定义配置 [configuration.](http://django-debug-toolbar.readthedocs.org/en/1.2/configuration.html)

[更多更详细的配置](http://django-debug-toolbar.readthedocs.org/en/1.2/index.html)

##使用
这里我们就使用默认的配置

启动django的开发服务器。 进入项目中

* 发现浏览的又上方有个图标,如下图：
![django-debug](/images/django_debug1.png "django")

* 点击图标可以看到debug的一些选项如下图。
![django-debug](/images/django_debug2.png "django")

* 我们来查看下sql的执行（下图），可以看到sql的执行总时间，多少条，每个sql的执行时间，sql语句等等。 还是很详细的。
![django-debug](/images/django_debug3.png "django")

##小结
从试用的角度来看，debug-tool还是很强大的，给我们的开发和调试带来很多的方面。

大家可以尝试下。




