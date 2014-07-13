在Python和IPython中使用Docker
========================


现在Docker是地球上最炙手可热的项目之一，就意味着人民实际上不仅仅是因为这个才喜欢它。
话虽如此，我非常喜欢使用容器，服务发现以及所有被创造出的新趣的点子和领域来切换工作作为范例。
这个文章中我会简要介绍使用python中的docker-py模块来操作Docker 容器，这里会使用我喜爱的编程工具IPython。

##安装docker-py
首先需要docker-py。注意这里的案例中我将会使用Ubuntu Trusty 14.04版本。

    $ pip install docker-py

##IPyhton
我真的很喜欢用IPython来探索Python。 它像是一共高级的python Shell，但是可以做的更多。

    $ sudo apt-get install ipython
    SNIP!
    $ ipython
    Python 2.7.6 (default, Mar 22 2014, 22:59:56)
    Type "copyright", "credits" or "license" for more information.

    IPython 1.2.1 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]:


##安装 docker
如果没有安装Docker，那首先安装docker

    $ sudo apt-get install docker.io

然后把 docker.io 起个别名 docker

    $ alias docker='docker.io'
    $ docker version
    Client version: 0.9.1
    Go version (client): go1.2.1
    Git commit (client): 3600720
    Server version: 0.9.1
    Git commit (server): 3600720
    Go version (server): go1.2.1
    Last stable version: 0.11.1, please update docker

Docker现在应该有个socket开启，我们可以用来连接。

    $ ls /var/run/docker.sock
    /var/run/docker.sock

##Pull 镜像
让我们下载 busybox镜像

    $ docker pull busybox
    Pulling repository busybox
    71e18d715071: Download complete
    98b9fdab1cb6: Download complete
    1277aa3f93b3: Download complete
    6e0a2595b580: Download complete
    511136ea3c5a: Download complete
    b6c0d171b362: Download complete
    8464f9ac64e8: Download complete
    9798716626f6: Download complete
    fc1343e2fca0: Download complete
    f3c823ac7aa6: Download complete

现在我们准备使用 docker-py 了。

##使用 docker-py
现在我们有了docker-py , IPython, Docker 和 busybox 镜像，我们就能建立一些容器。
如果你不是很熟悉IPython，可以参照这个教程学习（http://ipython.org/ipython-doc/stable/interactive/tutorial.html），
IPython是十分强大的。

首先启动一个IPython ，导入docker模块。

    $ ipython
    Python 2.7.6 (default, Mar 22 2014, 22:59:56)
    Type "copyright", "credits" or "license" for more information.

    IPython 1.2.1 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]: import docker

然后我们建立一个连接到Docker

    In [2]: c = docker.Client(base_url='unix://var/run/docker.sock',
       ...:                   version='1.9',
       ...:                   timeout=10)

现在我们已经连接到Docker。

IPython使用tab键来补全的。 如果 输入 “c.” 然后按下tab键，IPython会显示Docker连接对象所有的方法和属性。

    In [3]: c.
    c.adapters                      c.headers                       c.pull
    c.attach                        c.history                       c.push
    c.attach_socket                 c.hooks                         c.put
    c.auth                          c.images                        c.remove_container
    c.base_url                      c.import_image                  c.remove_image
    c.build                         c.info                          c.request
    c.cert                          c.insert                        c.resolve_redirects
    c.close                         c.inspect_container             c.restart
    c.commit                        c.inspect_image                 c.search
    c.containers                    c.kill                          c.send
    c.cookies                       c.login                         c.start
    c.copy                          c.logs                          c.stop
    c.create_container              c.max_redirects                 c.stream
    c.create_container_from_config  c.mount                         c.tag
    c.delete                        c.options                       c.top
    c.diff                          c.params                        c.trust_env
    c.events                        c.patch                         c.verify
    c.export                        c.port                          c.version
    c.get                           c.post                          c.wait
    c.get_adapter                   c.prepare_request
    c.head                          c.proxies

让我们来看下c.images   我输入一个 "?"在c.之后，ipython 会提供这个对象的详细信息。

    In [5]: c.images?
    Type:       instancemethod
    String Form:<bound method Client.images of <docker.client.Client object at 0x7f3acc731790>>
    File:       /usr/local/lib/python2.7/dist-packages/docker/client.py
    Definition: c.images(self, name=None, quiet=False, all=False, viz=False)
    Docstring:  <no docstring>

获取busybox 镜像。

    In [6]: c.images(name="busybox")
    Out[6]:
    [{u'Created': 1401402591,
      u'Id': u'71e18d715071d6ba89a041d1e696b3d201e82a7525fbd35e2763b8e066a3e4de',
      u'ParentId': u'8464f9ac64e87252a91be3fbb99cee20cda3188de5365bec7975881f389be343',
      u'RepoTags': [u'busybox:buildroot-2013.08.1'],
      u'Size': 0,
      u'VirtualSize': 2489301},
     {u'Created': 1401402590,
      u'Id': u'1277aa3f93b3da774690bc4f0d8bf257ff372e23310b4a5d3803c180c0d64cd5',
      u'ParentId': u'f3c823ac7aa6ef78d83f19167d5e2592d2c7f208058bc70bf5629d4bb4ab996c',
      u'RepoTags': [u'busybox:ubuntu-14.04'],
      u'Size': 0,
      u'VirtualSize': 5609404},
     {u'Created': 1401402589,
      u'Id': u'6e0a2595b5807b4f8c109f3c6c5c3d59c9873a5650b51a4480b61428427ab5d8',
      u'ParentId': u'fc1343e2fca04a455f803ba66d1865739e0243aca6c9d5fd55f4f73f1e28456e',
      u'RepoTags': [u'busybox:ubuntu-12.04'],
      u'Size': 0,
      u'VirtualSize': 5454693},
     {u'Created': 1401402587,
      u'Id': u'98b9fdab1cb6e25411eea5c44241561326c336d3e0efae86e0239a1fe56fbfd4',
      u'ParentId': u'9798716626f6ae4e6b7f28451c0a1a603dc534fe5d9dd3900150114f89386216',
      u'RepoTags': [u'busybox:buildroot-2014.02', u'busybox:latest'],
      u'Size': 0,
      u'VirtualSize': 2433303}]

建立一个容器。 注意我添加一个可以将要运行的命令，这里用的是"env"命令。

    In [8]: c.create_container(image="busybox", command="env")
    Out[8]:
    {u'Id': u'584459a09e6d4180757cb5c10ac354ca46a32bf8e122fa3fb71566108f330c87',
     u'Warnings': None}

使用ID来启动这个容器

    In [9]: c.start(container="584459a09e6d4180757cb5c10ac354ca46a32bf8e122fa3fb71566108f330c87")

我们可以检查日志，应该可以看到当容器创建的时候 ，我们配置的"env"命令的输出。

    In [11]: c.logs(container="584459a09e6d4180757cb5c10ac354ca46a32bf8e122fa3fb71566108f330c87")
    Out[11]: 'HOME=/\nPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\nHOSTNAME=584459a09e6d\n'

如果使用docker命令行，使用同样的命令行选项运行一个容器，应该可以看到类似的信息。

    $ docker run busybox env
    HOME=/
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    HOSTNAME=ce3ad38a52bf

据我所知，docker-py没有运行选项，我们只能创建一个容器然后启动它。

以下是一个案例：

    In [17]: busybox = c.create_container(image="busybox", command="echo hi")

    In [18]: busybox?
    Type:       dict
    String Form:{u'Id': u'34ede853ee0e95887ea333523d559efae7dcbe6ae7147aa971c544133a72e254', u'Warnings': None}
    Length:     2
    Docstring:
    dict() -> new empty dictionary
    dict(mapping) -> new dictionary initialized from a mapping object's
        (key, value) pairs
    dict(iterable) -> new dictionary initialized as if via:
        d = {}
        for k, v in iterable:
            d[k] = v
    dict(**kwargs) -> new dictionary initialized with the name=value pairs
        in the keyword argument list.  For example:  dict(one=1, two=2)

    In [19]: c.start(busybox.get("Id"))

    In [20]: c.logs(busybox.get("Id"))
    Out[20]: 'hi\n'

如果你还没有使用过busybox镜像，我建议你使用下。我也建议debain下的jessie镜像，它只有120MB，比Ubuntu镜像要小。

##总结
Docker是一个吸引人的新系统，可以用来建立有趣的新技术应用，特别是云服务相关的。使用IPython我们探索了怎么使用
docker-py模块来创建docker 容器。 现在使用python，我们可以结合docker和容易 创造出很多新的点子。


#原文
原文地址：http://serverascode.com/2014/06/05/docker-python.html
