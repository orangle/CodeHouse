linux命令学习-netstat
===============

>linux很多服务都与网络相关，当服务调不通或者是启动端口被占用，或者是又是被防火墙挡住的时候，就需要查询网络相关的问题，netstat命令之前只会用一两个参数这里，好好学习一番。

常用的几个选项：
* -a (all)显示所有选项，默认不显示LISTEN相关
* -t (tcp)仅显示tcp相关选项
* -u (udp)仅显示udp相关选项
* -n 拒绝显示别名，能显示数字的全部转化成数字
* -l 仅列出有在 Listen (监听) 的服務状态
* -c 每隔一个固定时间，执行该netstat命令
* -s 显示网络的统计信息
* -p 列出程序的pid，很有用
* -r 显示路由表
* -e 显示其他拓展信息

使用案例：

1 查看所有tcp端口

    $ netstat -at
2 查看所有在监听的tcp端口

    $ netstat -lt
3 找出ssh 服务的端口

    $ netstat -alpt|grep ssh
4 显示网卡以及网卡信息

    $ netstat -ie
5 查看所有路由表中tcp连接

    # netstat -ant
6 只查看监听的连接，以及pid信息（常用）

   # netstat -tnlp
7 每秒查看一次tcp连接

    # netstat -ct
8 查看某个服务是否运行

    netstat -alpnt|grep ssh

再有常用的在添加。






