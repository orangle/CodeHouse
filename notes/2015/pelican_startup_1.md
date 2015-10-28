Title:  Pelican入门(一)
Date: 2015-01-25
Modified: 2015-01-25
Category: pelican
Tags: pelican, publishing
Slug: pelican_startup_1
Authors: orangleliu

>听说这个静态博客很好用，最近又在协助“蟒周刊”翻译，于是先学习下基本的用法

[office site](http://docs.getpelican.com/en/3.5.0/)   You can startup for here.

##安装环境
我的os是win7， pelican v3.5.0.

```
pip install pelican markdown
```

不管你是用系统的python环境还是 virtualenv 都需要安装必要的组件。根据包依赖应该会装这些packages
**pelican, feedgenerator, jinja2, blinker, unidecode, markupsafe**
[这里有更详细的清单](http://docs.getpelican.com/en/3.5.0/install.html)

##建立项目
-  建立一个文件夹用来创建项目

```
D:\code>mkdir ptest
D:\code>cd ptest
```

-  建立一个初始的项目框架
```
D:\code\ptest>pelican-quickstart
```
我这里报错了  **ImportError: No module named html_parser**
本地的python版本是2.7.5  32bit，可能是一些兼容问题吧，于是直接修改了出错文件的代码

文件是 D:\devsofts\python2.7\lib\site-packages\pelican\readers.py，修改了下面一行
```
#from six.moves.html_parser import HTMLParser
from HTMLParser import HTMLParser
```

再次执行 D:\code\ptest>pelican-quickstart，会以问题的形式给出很多配置项，根据实际情况回答就行了。
得到如下的文件目录

```
D:\code\ptest>tree /f
文件夹 PATH 列表
卷序列号为 0002-FA2E
D:.
│  develop_server.sh
│  fabfile.py
│  Makefile
│  pelicanconf.py
│  publishconf.py
│
├─content
└─output
```
对于刚才问答形式的配置，还可以在这些配置文件中更改。

- 写文章

这里只是简单的一个例子，更多的定制和内置组件，[请参考](http://docs.getpelican.com/en/3.5.0/content.html)
pelican支持.rst, .md, .html 等文件,以及对应的格式， 还可以添加主题，插件，图片等等一些博客元素，文档中都有说明。

在content中添加一个 test.md文件
```
Title: HI baby！
Date: 2015-01-25 10:20
Modified: 2015-01-25 10:20
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: Orangleliu
Summary: Short version for index and feeds

##第一篇测试
 - markdown语法

```

目录结构现在是这样子
```
D:\code\ptest>tree /f
文件夹 PATH 列表
卷序列号为 0002-FA2E
D:.
│  develop_server.sh
│  fabfile.py
│  Makefile
│  pelicanconf.py
│  publishconf.py
│
├─content
│      test.md
│
└─output
```

- 生成html
使用命令,也可以通过命令指定其他的静态文件生成路径
```
D:\code\ptest>pelican content/
```

在output目录中就生成了如下的文件
```
└─output
    │  archives.html
    │  authors.html
    │  categories.html
    │  index.html
    │  my-super-post.html
    │  tags.html
    │
    ├─author
    │      orangleliu.html
    │
    ├─category
    │      python.html
    │
    ├─tag
    │      pelican.html
    │      publishing.html
    │
    └─theme
        ├─css
        │      main.css
        │      pygment.css
        │      reset.css
        │      typogrify.css
        │      wide.css
        │
        └─images
            └─icons
                    aboutme.png
                    ...
```

##本地查看
```
    D:\code\ptest>cd output

    D:\code\ptest\output>python -m SimpleHTTPServer
    Serving HTTP on 0.0.0.0 port 8000 ...
```
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)就可以在本地查看生成的博客了。
这样无论在github，还是gitcafe，还是自己的vps都可以快速的搭建博客了。
