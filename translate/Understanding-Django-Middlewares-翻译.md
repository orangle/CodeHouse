> 原文来自 [Understanding Django Middlewares](http://agiliq.com/blog/2015/07/understanding-django-middlewares/), 这篇文章从整体上介绍了django中中间件定义，作用，和怎么样自己写中间件  --orangleliu。

注：middleware 和中间件在下面文章中含义相同，不完全翻译了

假设你已经阅读了 [ Django官方文档middleware部分 ](https://docs.djangoproject.com/en/1.8/topics/http/middleware/). 下面会尽可能详尽的介绍文档中提到的知识，但是还是希望你熟悉 `middleware` 基本的概念。


这篇文章中我们将讨论下面内容：

* 什么是 middleware
* 什么时候使用 middleware
* 我们写 middleware 必须要记住的东西
* 写一些 middlewares 来理解中间件的工作过程和要点

## 什么是 middleware
Middlewares 是修改 Django **request** 或者 **response** 对象的钩子. 下面是[Django 文档](https://docs.djangoproject.com/en/1.8/topics/http/middleware/)中的一段描述。

```
Middleware is a framework of hooks into Django’s request/response processing. It’s a light, low-level “plugin” system for globally altering Django’s input or output.
```

## 什么时候使用 middleware

如果你想修改请求，例如被传送到view中的**HttpRequest**对象。 或者你想修改view返回的**HttpResponse**对象，这些都可以通过中间件来实现。

可能你还想在view执行之前做一些操作，这种情况就可以用 middleware来实现。

Django 提供了一些默认的 middleware，例如：
`AuthenticationMiddleware`


大家可能频繁在view使用`request.user`吧。 Django想在每个view执行之前把user设置为request的属性，于是就用了一个中间件来实现这个目标。所以Django提供了可以修改request 对象的中间件 `AuthenticationMiddleware `。

Django 这样修改request对象的：

```
https://github.com/django/django/blob/master/django/contrib/auth/middleware.py#L22
```

例如你有一个应用，它的用户是不同时区的人们。你想让他们在访问任何页面的时候都能显示正确的时区，想让所有的views中都能得到用户自己的timezone信息。 这种情况下可以用session来解决，所以你可以像下面添加一个 middleware：


```
class TimezoneMiddleware(object):
    def process_request(self, request):
        # Assuming user has a OneToOneField to a model called Profile
        # And Profile stores the timezone of the User.
        request.session['timezone'] = request.user.profile.timezone
```  


TimezoneMiddleware 是依赖于 request.user的，request.user 是通过`AuthenticationMiddleware`来设置的。 所以在
`settings.MIDDLEWARE_CLASSES`配置中，TimezoneMiddleware 一定要在 AuthenticationMiddleware 之后。 

下面的例子可以得到关于中间件顺序的更多体会。

## 使用middleware时应该记住的东西
* middlewares 的顺序非常重要
* 一个middleware只需要继承 object 类
* 一个middleware可以实现一些方法并且不需要实现所有的方法
* 一个middleware可以实现 **process_request（方法）** 但是不可以实现 **process_response（方法）** 和 process_view 方法。 这些都很常见，Django提供了很多middlewares可以做到。
* 一个middleware可以实现 **process_response** 方法，但是不需要实现 **process_request** 方法

AuthenticationMiddleware 只实现了对请求的处理，并没有处理响应. [参照文档]((https://github.com/django/django/blob/master/django/contrib/auth/middleware.py#L14))

GZipMiddleware 只实现了对响应的处理，并没有实现对请求和view的处理 [参见文档](https://github.com/django/django/blob/master/django/middleware/gzip.py#L9)

## 写一些 middlewares

首先确认下你有一个Django项目，需要一个url和一个view，并且可以进入这个view。下面我们会对request.user做几个测试，确认权限设置好了，并可以在view中正确打印 request.user 的信息。

在任意一个app中创建middleware.py文件。

我有一个叫做books的app，所以文件的位置是 `books/middleware.py
`

```
class BookMiddleware(object):
    def process_request(self, request):
        print "Middleware executed"
```

MIDDLEWARE_CLASSES 中添加这个中间件

```
MIDDLEWARE_CLASSES = (
    'books.middleware.BookMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
```

对任意的一个url发送请求, 下面的信息将会打印在runserver的控制台。


```
Middleware executed
```

修改 `BookMiddleware.process_request` 如下

```
class BookMiddleware(object):
    def process_request(self, request):
        print "Middleware executed"
        print request.user
```

再次访问一个url，将会引起一个错误。

```
'WSGIRequest' object has no attribute 'user'
```

这是因为request对象还没有设置user属性呢。

现在我们改变下 middlewares的顺序，`BookMiddleware ` 放在 `AuthenticationMiddleware ` 之后。

```
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'books.middleware.BookMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
```

访问一个url，runserver控制台打印如下

```
Middleware executed
<username>
```

这说明middlewares处理request的顺序跟 settings.MIDDLEWARE_CLASSES 中列出的顺序是一致的。

你可以进一步证实，middleware.py添加另外一个middleware

```
class AnotherMiddleware(object):
    def process_request(self, request):
        print "Another middleware executed"
```    
    
把它也加到 `MIDDLEWARE_CLASSES`

```
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'books.middleware.BookMiddleware',
    'books.middleware.AnotherMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
```

现在的输出是：

```
Middleware executed
<username>
Another middleware executed
```

在process_request方法中返回HttpResponse，把BookMiddleware改成下面这样:

```
class BookMiddleware(object):
    def process_request(self, request):
        print "Middleware executed"
        print request.user
        return HttpResponse("some response")
```
        
尝试下任何一个url，会得到如下输出：

```
Middleware executed
<username>
```

你会注意到下面2个事情：

* 不管你访问哪个url，自己写的view 处理方法都不执行了，只有 "some response"这样一种响应。
* AnotherMiddleware.process_request 不在被执行


所以如果 Middleware的process_request方法中返回了HttpResponse对象，那么它之后的中间件将被略过， view中的处理方法也被略过。
所以在实际的项目中很少会这么干（不过也有些项目会，例如做代理） 

注释掉 `"return HttpResponse("some response")"`，两个 middleware 才能正常的处理请求。


## 使用 process_response
给这两个middleware添加 process_response方法

```
class AnotherMiddleware(object):
    def process_request(self, request):
        print "Another middleware executed"

    def process_response(self, request, response):
        print "AnotherMiddleware process_response executed"
        return response

class BookMiddleware(object):
    def process_request(self, request):
        print "Middleware executed"
        print request.user
        return HttpResponse("some response")
        #self._start = time.time()

    def process_response(self, request, response):
        print "BookMiddleware process_response executed"
        return response
```

访问一些url，得到如下的输出

```
Middleware executed
<username>
Another middleware executed
AnotherMiddleware process_response executed
BookMiddleware process_response executed
```

`AnotherMiddleware.process_response()` 在 `BookMiddleware.process_response()` 之前执行 而 `AnotherMiddleware.process_request()` 在 `BookMiddleware.process_request()`之后执行. 所以`process_response()` 执行的顺序跟 process_request正好相反. `process_response()` 执行的顺序是从最后一个中间件执行，到倒数第二个，然后直到第一个中间件.

## process_view
Django 按顺序执行中间件 `process_view()` 的方法，从上到下。 类似process_request()方法执行的顺序。

所以如果任何一个 `process_view()` 返回了HttpResponse对象，那么在它后面`process_view()`将会被省略，不会被执行。

