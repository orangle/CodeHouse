面试常见问题（偏理论）
==================


###Q1
Q: What are some drawbacks of the Python language? <br/>
python语言的缺点有哪些？

一般的回答会包括这*两点*

* 全局解释锁（GIL）<br>
>CPython (the most common Python implementation) is not fully thread safe.
>In order to support multi-threaded Python programs, CPython provides a
>global lock that must be held by the current thread before it can safely
>access Python objects. As a result, no matter how many threads or processors
>are present, only one thread is ever being executed at any given time.
>In comparison, it is worth noting that the PyPy implementation – discussed
>in more detail later in this post – provides a stackless mode that supports
>micro-threads for massive concurrency.

* 执行速度
>Python can be slower than compiled languages since it is interpreted.

