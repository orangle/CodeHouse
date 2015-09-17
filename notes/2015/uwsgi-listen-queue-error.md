# 【uwsgi】 listen queue of socket (fd: 3) 错误分析


> 现在django的应用基本都是使用uwsgi来部署，类似下面 `listen queue of socket "127.0.0.1:9001" (fd: 3)` 的错误出现过2次，下面说下这两次错误出现的解决的过程。

## 出错场景

错误日志截取

```
Tue Jun  2 17:33:27 2015 - *** uWSGI listen queue of socket "127.0.0.1:9001" (fd: 3) full !!! (101/100) ***
Tue Jun  2 17:33:28 2015 - *** uWSGI listen queue of socket "127.0.0.1:9001" (fd: 3) full !!! (101/100) ***
```

* 第一次是因为联通机房防火墙配置错了，限制了服务器output，也就是外部发包给服务器没有问题，但是服务器返回包给外部的时候非常慢，几乎不可用，这个时候uwsgi日志中就出现了大量的错误

* 第二次是并发量剧增之后，活动链接保持在6000左右的时候，大量出现这个错误。

## 分析
以这个错误为基础，查询了下相关资料，应该是系统级别参数的问题，具体可以参考 [linux man page listen(2)](http://linux.die.net/man/2/listen). 

lzz注： 简单的理解就是每个监听的socket，在没有accept之前，等待处理的socket队列长度，linux(至少在centos6.6中)默认是128，在我这个编译的uwsgi中默认是100，也就是说没有调整系统参数之前，最高也就是128。

那么怎样才能把队列的长度调整变长呢？
* 必须调整系统参数，使其生效
* 必须调整uwsgi配置，然后重启应用

## 操作
### 修改系统参数
这里直接修改配置文件了，重启后仍然有效。

修改/etc/sysctl.conf文件,添加或者修改这几个参数值

```
#对于一个经常处理新连接的高负载 web服务环境来说，默认的 128 太小了
net.core.somaxconn = 262144
​#表示SYN队列的长度，默认为1024，加大队列长度为8192，可以容纳更多等待连接的网络连接数
net.ipv4.tcp_max_syn_backlog = 8192
#网卡设备将请求放入队列的长度
net.core.netdev_max_backlog = 65536
```

修改完成之后要记得 `sysctl -p` 重新加载参数

### uwsgi调整
不管是配置，还是命令行加一个选项，例如 .ini 文件中添加如下配置

```
listen=1024
```

之后重启应用，重新加载配置。

## 小结
通过修改配置，这种错误基本没有出现过了，系统的吞吐量和并发数都大大提高了。所以系统特性和调优对于提高整个服务质量非常重要。

## 参考

* [somaxconn - That pesky limit.](https://derrickpetzold.com/#!/p/somaxconn/)
* [listen(2) - Linux man page](http://linux.die.net/man/2/listen)











