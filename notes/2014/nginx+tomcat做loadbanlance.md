nginx tomcat做负载均衡
==================

>之前使用nginx做过web反向代理，没有做过负载均衡，今天有个同学需要做tomcat的负载均衡，我也研究下。

一共是2个机器，一个物理机(win7)上面部署2个tomcat，使用不同的端口启动。vm中的虚拟机放(centos)nginx，给tomcat做负载均衡.

* inux ip: 192.168.37.129
* win ip:  192.168.37.1

首先保证两个主机可以互ping，响应的端口开放。

* nginx上使用80
* tomcat1 使用8081  tomcat2使用8080
* nginx，tomcat的安装和启动不在说了，特别是windows下很简单，遇到困难百度下就可以了。
* [windows安装启动个tomcat](http://www.360doc.com/content/10/1215/14/58597_78364548.shtml) 还有 [一个系统启动多个tomcat](http://www.linuxidc.com/Linux/2012-10/72248.htm)  为了区分每个tomcat的不同，把首页的html加上些标志。
* nginx版本1.4  tomcat 版本6.0
* 2个tomcat实例可以正常启动，nginx实例也能正常使用，win上的浏览器中可以正常访问3个网页
    * http://192.168.37.1:8081/
    * http://192.168.37.1:8080/
    * http://192.168.37.129/

然后开始配置nginx:

[root@localhost conf]# cat /etc/nginx/nginx.conf

    #user  nobody;
    worker_processes  1;
    events {
        worker_connections  1024;
    }

    http {
        include       mime.types;
        default_type  application/octet-stream;

        upstream localhost{
            server 192.168.37.1:8080 weight=2;
            server 192.168.37.1:8081 weight=1;
            #ip_hash;
        }

        sendfile        on;
        keepalive_timeout  65;

        server {
            listen       80;
            server_name  localhost;

            location / {
                proxy_connect_timeout  3;
                #proxy_redirect        off;
                proxy_send_timeout     30;
                proxy_read_timeout     30;
                proxy_pass      http://localhost;
            }

            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   html;
            }
        }
    }

这怎么重启nginx都没生效，最后发现是因为启动的配置文件不对，可以通过 nginx -c /etc/nginx/nginx.conf 来指定陪配置文件的路径。
当然这里是最简单的轮询，没有其他策略，实验来说基本成功。


