redis 数据类型以及常用操作
====================

##5种类型(基本都是自己实现或者是根据c语言改进)
* string

字符串对象的编码可以是 int， raw， embstr

* list

列表对象的编码可以是 ziplist 或者 linkedlist

* hash
* set
* zset

##常用操作
**type**
用来判判断值的类型

    redis 127.0.0.1:6379> rpush num 2,4,5
    (integer) 1
    redis 127.0.0.1:6379> type num
    list

**object encoding**
用来查看对象的编码

    redis 127.0.0.1:6379> object encoding num
    "ziplist"

**del**
删除记录

    redis 127.0.0.1:6379> set name "orangleliu"
    OK
    redis 127.0.0.1:6379> get name
    "orangleliu"
    redis 127.0.0.1:6379> del name
    (integer) 1
    redis 127.0.0.1:6379> get name
    (nil)

**object refcount**
查看当前对象的引用次数

    redis 127.0.0.1:6379> set A 1
    OK
    redis 127.0.0.1:6379> object refcount A
    (integer) 1

**object idletime**
查看数据被命令访问最后一次的时间(空转时长)，这是最大内存参数的时候，这些数据优先回收

    redis 127.0.0.1:6379> set A 100
    OK
    redis 127.0.0.1:6379> object idletime A
    (integer) 0
    redis 127.0.0.1:6379> object idletime A
    (integer) 20

**dbsize**
查看整个库所有的记录数

    redis 127.0.0.1:6379> dbsize
    (integer) 8

** exists**
查看某个键是否存在

    redis 127.0.0.1:6379> exists blog  #存在
    (integer) 1
    redis 127.0.0.1:6379> exists heihei  #不存在
    (integer) 0

**flushdb**
清空数据库中的所有记录

    redis 127.0.0.1:6379> flushdb
    OK
    redis 127.0.0.1:6379> dbsize
    (integer) 0

**info**
查看数据库的状态信息

    redis 127.0.0.1:6379> info
    # Server
    redis_version:2.6.12
    redis_git_sha1:00000000
    redis_git_dirty:0
    redis_mode:standalone
    os:Windows
    arch_bits:32
    multiplexing_api:winsock_IOCP
    gcc_version:0.0.0
    process_id:1796
    run_id:0f55154e68cb081183058963e2423a97353c6abe
    tcp_port:6379
    uptime_in_seconds:15937
    uptime_in_days:0
    hz:0
    lru_clock:0

    # Clients
    connected_clients:1
    client_longest_output_list:0
    client_biggest_input_buf:0
    blocked_clients:0

    # Memory
    used_memory:545928
    used_memory_human:533.13K
    used_memory_rss:545928
    used_memory_peak:546368
    used_memory_peak_human:533.56K
    used_memory_lua:23552
    mem_fragmentation_ratio:1.00
    mem_allocator:libc

    # Persistence
    loading:0
    rdb_changes_since_last_save:-2
    rdb_bgsave_in_progress:0
    rdb_last_save_time:1409134834
    rdb_last_bgsave_status:ok
    rdb_last_bgsave_time_sec:0
    rdb_current_bgsave_time_sec:-1
    aof_enabled:0
    aof_rewrite_in_progress:0
    aof_rewrite_scheduled:0
    aof_last_rewrite_time_sec:-1
    aof_current_rewrite_time_sec:-1
    aof_last_bgrewrite_status:ok

    # Stats
    total_connections_received:2
    total_commands_processed:73
    instantaneous_ops_per_sec:0
    rejected_connections:0
    expired_keys:0
    evicted_keys:0
    keyspace_hits:20
    keyspace_misses:5
    pubsub_channels:0
    pubsub_patterns:0
    latest_fork_usec:0

    # Replication
    role:master
    connected_slaves:0

    # CPU
    used_cpu_sys:0.05
    used_cpu_user:0.02
    used_cpu_sys_children:0.00
    used_cpu_user_children:0.00

    # Keyspace




####字符串操作
**插入**

    redis 127.0.0.1:6379> set name "orangleliu"
    OK

**查询**

    redis 127.0.0.1:6379> get name
    "orangleliu"

**字符拼接**

    redis 127.0.0.1:6379> append  name " hello!"
    (integer) 17
    redis 127.0.0.1:6379> get name
    "orangleliu hello!"

**字符串转数字类型加减**

    redis 127.0.0.1:6379> set age 20
    OK
    redis 127.0.0.1:6379> incrbyfloat age 2.0  #取出转换为浮点数相加在变成字符类型
    "22"
    redis 127.0.0.1:6379> incrby age 3   #整数相加
    (integer) 25
    redis 127.0.0.1:6379> decrby age 20  #整数相减
    (integer) 5

**取字符串长度**

    redis 127.0.0.1:6379> set blog "chinacache"
    OK
    redis 127.0.0.1:6379> strlen blog
    (integer) 10

**指定索引插入和取出字符**

    redis 127.0.0.1:6379> setrange blog 1 "llll"
    (integer) 10
    redis 127.0.0.1:6379> get blog
    "cllllcache"   #可以看到字符串索引是重0开始的
    redis 127.0.0.1:6379> getrange blog 0 0  #必须要输入两个开始和结束的索引
    "c"
    redis 127.0.0.1:6379> getrange blog 0 1
    "cl"

#### 列表对象




##数据实现管理等

####切换数据库
默认情况下客户端连接的是redis 0号数据库

    redis 127.0.0.1:6379> set name "orangleliu"
    OK
    redis 127.0.0.1:6379> get name
    "orangleliu"
    redis 127.0.0.1:6379> select 1  #切换到数据库1
    OK
    redis 127.0.0.1:6379[1]> get name  #获取不到0数据库中的记录
    (nil)
    redis 127.0.0.1:6379[1]> select 0   #切换回到数据库 0
    OK
    redis 127.0.0.1:6379> get name
    "orangleliu"

####设置记录的有效期
可以设置一条记录的生存期，时间单位是秒或者是毫秒

    redis 127.0.0.1:6379> set name "orangleliu"
    OK
    redis 127.0.0.1:6379> expire name 5
    (integer) 1
    redis 127.0.0.1:6379> get name  #5s以后
    (nil)

当然还可以设置在某个时间点之前有效，expireat


