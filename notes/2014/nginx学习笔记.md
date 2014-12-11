nginx 学习笔记
==========

>看视频学习笔记，先看一遍，做笔记，然后在实验一遍，主要是代理，反向代理和负载均衡的配置。

常用的web服务器：
* apache 模块丰富，资源消耗比较大，并发不够
* lighttpd 内存低，cup低，性能高
* websphere java容易，企业使用
* IIS 图形化管理，功能服务，操作系统绑定

nginx 一些知识：
* 使用epoll网络I/O模型
*

###源码安装
下载，解压，配置，编译，安装

    yum -y install gcc gcc-c++ autoconf automake
    yum -y install zlib zlib-dev openssl openssl-devel pcre-devel

zib: 压缩  openssl：ssl协议 pcre：地址重写

需要注意的是最好是自定义配置，特别是要求比较高的时候，不要使用默认配置。

    ./configure
        --sbin-path=/usr/local/nginx/nginx
        --conf-path=/usr/local/nginx/nginx.conf
        --pid-path=/usr/local/nginx/nginx.pid
        --with-http_ssl_module
        --with-pcre=../pcre-4.4
        --with-zlib=../zlib-1.1.3

[参数请参看文档](http://nginx.org/en/docs/configure.html)

    #tar -zxvf nginx.tar.gz
    #cd nginx
    #./configure \
        --prefix=usr \
        --sbin-path=/usr/sbin/nginx \
        --conf-path=/etc/nginx/nginx.conf \
        --error-log-paht=/var/log/nginx/error.log \
        --pid-path=/var/run/nginx/nginx.pid \
        --lock-path=/var/lock/nginx.lock \
        --user=nginx \
        --group=nginx \
        --with-http_ssl_module \
        --with-http_flv_module \
        --with-http_gzip_static_module \
        --http-log-path=/var/log/nginx/access.log \
        --http-proxy-temp-path=/var/tmp/nginx/proxy
    #make && make install

###服务操作
检查配置文件：
/usr/sbin/nginx -t -c /etc/nginx/nginx.conf


### 负载均衡的配置




