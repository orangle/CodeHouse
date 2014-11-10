docker 初级常用命令
===============

>之前有一段时间看了看docker，这两个月还工作还没继续往下看。 但是呢后面一段时间需要学习一些linux常用软件的安装还有些运维支持，所以需要经常搭建linux虚拟环境，为了不至于总要初始化环境还有容易做些集群实验，用docker正合适。简要的记录写常用的命令，快速熟悉简单的操作。

* docker run  在一个**新**的容器中运行命令
    1 docker run [dockerfile/ubuntu](镜像) [/bin/echo 'orangleliu'](命令)
    2 docker run -t -i dockerfile/ubuntu /bin/bash
        * -t 打开一个终端
        * -i  可以交互的连接

    3 docker run -d dockerfile/ubuntu /bin/echo "you are lzz"
        * -d 后台运行，守护进程
    4 docker run -d -P training/webapp python app.py
        * -P 把web应用在容器中使用的端口映射到host上
    5 docker run -d -p 5000:5000 training/webapp python app.py
        * -p 把容器内的5000端口 映射到host的5000端口


* docker images  列出本地镜像
* docker ps 查看正在运行的容器
* docker logs container_name 查看某个后台运行的容器的日志
    1 docker logs -f container_name  类似于tail -f 可以实时打印最新日志

* docker stop container_name 停止容器的运行
* docker rm  container_name  删除一个或多个容器
* docker rmi  image_name  删除一个或者多个镜像
* docker port container_name 5000 查看某个容器内部5000端口，映射到host对应的端口
* cocker top container_name 查看某个容器内部的进程
* docker inspect container_name 查看容器的状态

查看所有命令 docker --help  , 查看二级命令的帮助 docker run --help
