关于linux web服务器的内核参数调整和安全防御

- 修改的配置文件 /etc/sysctl.conf
- 修改后生效 sysctl -p
- 检测好用否

**主要是这个文件的配置**

**高并发**

    #---基本调优---  防止简单的攻击
    #提高整个系统的文件限制
    fs.file-max = 51200
    #开启SYN Cookies,当出现SYN等待队列溢出时,启用cookies来处理,可防范少量SYN攻击,默认为0,表示关闭；
    net.ipv4.tcp_syncookies = 1
    #表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；
    net.ipv4.tcp_tw_reuse = 1
    #表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭；
    #为了对NAT设备更友好，建议设置为0。
    net.ipv4.tcp_tw_recycle = 0
    #修改系統默认的 TIMEOUT 时间
    net.ipv4.tcp_fin_timeout = 30

    #TCP发送keepalive探测以确定该连接已经断开的次数。
    #(注意:保持连接仅在SO_KEEPALIVE套接字选项被打开是才发送.
    #次数默认不需要修改,当然根据情形也可以适当地缩短此值.设置为5比较合适)
    net.ipv4.tcp_keepalive_probes = 5

    #探测消息发送的频率，乘以tcp_keepalive_probes就得到对于从开始探测以来没有响应的连接杀除的时间。
    #默认值为75秒，也就是没有活动的连接将在大约11分钟以后将被丢弃。
    #(对于普通应用来说,这个值有一些偏大,可以根据需要改小.特别是web类服务器需要改小该值,15是个比较合适的值)
    net.ipv4.tcp_keepalive_intvl = 15

    #---流量特别大才有效果---
    #表示当keepalive起用的时候，TCP发送keepalive消息的频度。缺省是2小时，改为20分钟
    net.ipv4.tcp_keepalive_time = 1200
    #表示用于向外连接的端口范围。缺省情况下很小：32768到61000，改为10000到65000。
    #（注意：这里不要将最低值设的太低，否则可能会占用掉正常的端口！）
    net.ipv4.ip_local_port_range = 10000 65000
    #表示SYN队列的长度，默认为1024，加大队列长度为8192，可以容纳更多等待连接的网络连接数
    net.ipv4.tcp_max_syn_backlog = 8192
    #表示系统同时保持TIME_WAIT的最大数量，如果超过这个数字，TIME_WAIT将立刻被清除并打印警告信息
    net.ipv4.tcp_max_tw_buckets = 5000
    #额外的，对于内核版本新于**3.7.1**的，我们可以开启tcp_fastopen：
    #net.ipv4.tcp_fastopen = 3

    #在内核内存中netfilter可以同时处理的“任务”（连接跟踪条目）跟iptables有关
    net.ipv4.ip_conntrack_max = 655360
    #跟踪的连接超时结束时间
    net.ipv4.netfilter.ip_conntrack_tcp_timeout_established = 180

    #定义了系统中每一个端口最大的监听队列的长度
    #对于一个经常处理新连接的高负载 web服务环境来说，默认的 128 太小了
    net.core.somaxconn = 262144

    # increase TCP max buffer size settable using setsockopt()
    net.core.rmem_max = 67108864
    net.core.wmem_max = 67108864
    # increase Linux autotuning TCP buffer limit
    net.ipv4.tcp_rmem = 4096 87380 67108864
    net.ipv4.tcp_wmem = 4096 65536 67108864
    # increase the length of the processor input queue
    net.core.netdev_max_backlog = 250000
    # recommended for hosts with jumbo frames enabled
    net.ipv4.tcp_mtu_probing=1

**参考模板**

    # 避免放大攻击
    net.ipv4.icmp_echo_ignore_broadcasts = 1

    # 开启恶意icmp错误消息保护
    net.ipv4.icmp_ignore_bogus_error_responses = 1

    # 开启SYN洪水攻击保护
    net.ipv4.tcp_syncookies = 1

    # 开启并记录欺骗，源路由和重定向包
    net.ipv4.conf.all.log_martians = 1
    net.ipv4.conf.default.log_martians = 1

    # 处理无源路由的包
    net.ipv4.conf.all.accept_source_route = 0
    net.ipv4.conf.default.accept_source_route = 0

    # 开启反向路径过滤
    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.conf.default.rp_filter = 1

    # 确保无人能修改路由表
    net.ipv4.conf.all.accept_redirects = 0
    net.ipv4.conf.default.accept_redirects = 0
    net.ipv4.conf.all.secure_redirects = 0
    net.ipv4.conf.default.secure_redirects = 0

    # 不充当路由器
    net.ipv4.ip_forward = 0
    net.ipv4.conf.all.send_redirects = 0
    net.ipv4.conf.default.send_redirects = 0

    # 开启execshild
    kernel.exec-shield = 1
    kernel.randomize_va_space = 1

    # IPv6设置
    net.ipv6.conf.default.router_solicitations = 0
    net.ipv6.conf.default.accept_ra_rtr_pref = 0
    net.ipv6.conf.default.accept_ra_pinfo = 0
    net.ipv6.conf.default.accept_ra_defrtr = 0
    net.ipv6.conf.default.autoconf = 0
    net.ipv6.conf.default.dad_transmits = 0
    net.ipv6.conf.default.max_addresses = 1

    # 优化LB使用的端口

    # 增加系统文件描述符限制
    fs.file-max = 65535

    # 允许更多的PIDs (减少滚动翻转问题); may break some programs 32768
    kernel.pid_max = 65536

    # 增加系统IP端口限制
    net.ipv4.ip_local_port_range = 2000 65000

    # 增加TCP最大缓冲区大小
    net.ipv4.tcp_rmem = 4096 87380 8388608
    net.ipv4.tcp_wmem = 4096 87380 8388608

    # 增加Linux自动调整TCP缓冲区限制
    # 最小，默认和最大可使用的字节数
    # 最大值不低于4MB，如果你使用非常高的BDP路径可以设置得更高

    # Tcp窗口等
    net.core.rmem_max = 8388608
    net.core.wmem_max = 8388608
    net.core.netdev_max_backlog = 5000
    net.ipv4.tcp_window_scaling = 1

** 参考 **
http://blog.csdn.net/largetalk/article/details/16863689

