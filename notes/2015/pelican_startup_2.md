Title:  Pelican入门(二)
Date: 2015-01-25
Modified: 2015-01-25
Category: pelican
Tags: pelican, publishing
Slug: pelican_startup_2
Authors: orangleliu

>之前是搭建了一个简单的博客，但是没有图片，没有具体的栏目分类
这次来研究下

## 一 导航栏
之前是直接把.md扔到的content文件夹下，结果导航栏，显示的是Category信息。
![menu](/images/pelican_2_1.png)

现在这么改成

```
D:.
├─articles
│      how_make_gitcafe_pages.md
│      pelican_startup_1.md
│      pelican_startup_2.md
│
└─pages
        about.md
```

可以在pelicanconf.py 中定义menu

```
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

MENUITEMS = (
    ('Home', '/'),
    ('About', '/pages/about.html'),
)
```
![menu](/images/pelican_2_2.png)

##二 图片
图文并茂才能更好的理解，图片怎么加到博客中呢？（这里说的是本地加载，如果直接使用其他存储服务直接放url连接就好了）

在content目录下建立一个 images目录

```
content
├── images
│   └── xxx.png
```
然后在 pelicanconf.py 中添加

```
STATIC_PATHS = ['images']
```

在文章中这样添加

```
![aimage](/images/xxx.png)
```

##三 footer
原来的footer 不太好看，这块应该怎么定制呢？ [可供参考的文章](http://mygeekdaddy.net/2015/01/09/never-change-your-pelican-footer-again/) 不过他说的是用模板引擎的情况，有点不太一样，我想就是直接默认的主题修改下footer

![之前的底页](/images/pelican_2_3.png)

文档也看了，google也查了，没发现直接配置footer.html的方法，都是通过主题来控制，这个等使用其他主题的时候再看把。

##四 小结
其实pelican的资源非常丰富，插件，主题，还有已经开源的博客，我们都可以参考和学习。



