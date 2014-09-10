logging 模块学习
=============

>开始学习编程的时候总是喜欢用print来打印出调试信息，后来会用了debug，在开发的时候总是用调试来解决问题，但是一旦部署之后我们想要及时发现问题就没法用print或者debug的方法来监控应用了。所以l不管是什么系统，log总是一个非常重要的模块，怎么样使用logging记录发生的问题，用log来监控系统的正常与否十分重要。 Java中经常使用Log4j等第三方jar来完成，Python 是集成在标准库中，简单实用。

陆陆续续用过挺长时间logging模块，也曾经简单的学习过，这次决定系统的看一下常用的功能。


参考的资料是python docs上的几篇文章
>[logging -Logging facility for Python](https://docs.python.org/2/library/logging.html)
>[Logging HOWTO](https://docs.python.org/2.7/howto/logging.html#logging-basic-tutorial)
>[Logging Cookbook](https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook)

###简单使用

常用的几个日志级别从低到高分别是  DEBUG, INFO,WARNING,ERROR


