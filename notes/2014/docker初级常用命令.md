docker 初级常用命令
===============

>之前有一段时间看了看docker，这两个月还工作还没继续往下看。 但是呢后面一段时间需要学习一些linux常用软件的安装还有些运维支持，所以需要经常搭建linux虚拟环境，为了不至于总要初始化环境还有容易做些集群实验，用docker正合适。简要的记录写常用的命令，快速熟悉简单的操作。

* docker run  在一个**新**的容器中运行命令<br>
    1 docker run [dockerfile/ubuntu](镜像) [/bin/echo 'orangleliu'](命令)<br>
    2 docker run -t -i dockerfile/ubuntu /bin/bash<br>
        * -t 打开一个终端<br>
        * -i  可以交互的连接<br>
    3 docker run -d dockerfile/ubuntu /bin/echo "you are lzz"<br>
        * -d 后台运行，守护进程<br>
    4 docker run -d -P training/webapp python app.py<br>
        * -P 把web应用在容器中使用的端口映射到host上<br>
    5 docker run -d -p 5000:5000 training/webapp python app.py<br>
        * -p 把容器内的5000端口 映射到host的5000端口<br>
* docker images  列出本地镜像<br>
* docker ps 查看正在运行的容器<br>
* docker logs container_name 查看某个后台运行的容器的日志<br>
    1 docker logs -f container_name  类似于tail -f 可以实时打印最新日志<br>
* docker stop container_name 停止容器的运行<br>
* docker rm  container_name  删除一个或多个容器<br>
* docker rmi  image_name  删除一个或者多个镜像<br>
* docker port container_name 5000 查看某个容器内部5000端口，映射到host对应的端口<br>
* cocker top container_name 查看某个容器内部的进程<br>
* docker inspect container_name 查看容器的状态<br>

查看所有命令 docker --help  , 查看二级命令的帮助 docker run --help

###[docker file 使用](https://docs.docker.com/userguide/dockerimages/)
使用dockerfile可以实现一些自动化的安装

[dockerfile 训练教程](https://docs.docker.com/userguide/level1/)

###连接容器
例如我们启动了一个web 或者数据库服务，然后需要在不停服务的情况下调整配置参数，就需要一个通道[进入到这个正在运行的容器中](https://docs.docker.com/userguide/dockerlinks/)。

###[管理容器中的数据](https://docs.docker.com/userguide/dockervolumes/)


###一些理解
* 可以自己搭建私有仓库，可以自己制作image
* container自己没有内核，是依赖于host的内核
* 现在是分层的，一个image包含了多层，多个文件





