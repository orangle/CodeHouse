awk 学习笔记
==========

最近添加了几个功能的日志，但是呢，这个日志就是输出，一般自己也发现不了问题，于是想写一些简单的监控脚本来看看日志的大致情况，
比如有没有error，每天有多少error报出来。 想到了以前运维的同时分享awk，于是想简单的学习下。


####入门
最简单的输入某些列 使用$4 这种来表示  __$0__是输出整列

    [root]/root/test$ps -ef|grep uwsgi|awk '{print $1,$5}'
    root Jul24
    root Jul24
    root Jul24
    root Jul24
    root Jul24
    root Jul24
    root Jul24
    root Jul24
    root Jul24
    root 18:49

格式化输出：

    [root]/root/test$ps -ef|grep uwsgi|awk '{printf "%-2s and %-4s \n",$1,$5}'
    root and Jul24
    root and Jul24
    root and Jul24
    root and Jul24
    root and Jul24
    root and Jul24
    root and Jul24
    root and Jul24
    root and Jul24
    root and 18:51

####过滤 判断
判断符号 !=, >, <, >=, <=,==

    [root]/root/test$ps -ef|grep uwsgi|awk '$2=="20596"'
    root     20596 20560  0 Jul24 ?        00:00:19 uwsgi -x uwsgi.xml
    #使用表头(就是取第一行) NR
    [root]/root/test$ps -ef|grep uwsgi|awk '$2=="20596" || NR==1 {print $7}'
    00:00:01
    00:00:19

内建变量：
    $0 --->  当前记录（这个变量中存放着整个行的内容）
    $1~$n --->   当前记录的第n个字段，字段间由FS分隔
    FS--->  输入字段分隔符 默认是空格或Tab
    NF--->  当前记录中的字段个数，就是有多少列
    NR--->  已经读出的记录数，就是行号，从1开始，如果有多个文件话，这个值也是不断累加中。
    FNR---> 当前记录数，与NR不同的是，这个值会是各个文件自己的行号
    RS--->  输入的记录分隔符， 默认为换行符
    OFS---> 输出字段分隔符， 默认也是空格
    ORS---> 输出的记录分隔符，默认为换行符
    FILENAME--->    当前输入文件的名字

取出特定的列并显示行号：

    [root]/root/test$ps -ef|grep uwsgi|awk '$2=="20596" || NR==1 {printf "No %s, %s \n",NR,$7}'
    No 1, 00:00:01
    No 6, 00:00:19

指定分割符：

    [root]/root/test$awk  'BEGIN{FS=":"} {print $1,$3,$6}' /etc/passwd
    root 0 /root
    bin 1 /bin
    daemon 2 /sbin
    adm 3 /var/adm
    #也可以写成
    awk  -F: '{print $1,$3,$6}' /etc/passwd

多个分隔符的写法： awk -F '[;:]'

####使用正则

    $cat test.log
    2014-07-21 20:00:53,379 - charge - INFO - 30748 - contract_no=chuangfu-MIDS-1306
    2014-07-21 20:00:53,406 - charge - INFO - 30748 - contract_no=chuangfu-MIDS-1306
    2014-07-21 20:00:53,431 - charge - INFO - 30748 - contract_no=chuangfu-MIDS-1306
    2014-07-21 20:00:53,543 - charge - INFO - 30748 - contract_no=vvvgame-CCDL-1307
    2014-07-24 16:00:34,356 - charge - INFO - 18338 - contract_no=sennheiser-CC-1405
    2014-07-24 16:00:34,394 - charge - INFO - 18338 - contract_no=sennheiser-CC-1405
    2014-07-24 16:04:24,431 - charge - INFO - 19081 - contract_no=sennheiser-CC-1405
    2014-07-24 16:04:24,479 - charge - INFO - 19081 - contract_no=sennheiser-CC-1405
    2014-07-24 16:07:20,349 - charge - INFO - 19081 - contract_no=sennheiser-CC-1405
    2014-07-24 16:07:20,390 - charge - INFO - 19081 - contract_no=sennheiser-CC-1405
    [root]/Application/2.0/nirvana/logs$awk '$10 ~ /MIDS/ {print NR,$1,$2}' test.log
    1 2014-07-21 20:00:53,379
    2 2014-07-21 20:00:53,406
    3 2014-07-21 20:00:53,431

这里 ~是模式的开始，如果是对模式取反 使用!~， //是正则表达式
把结果放到文件中直接使用重定向就行了。

__使用if else对文件分组重定向__

    $awk '{if($10 ~ /MIDS/) print > "mids.txt";else if($6 ~ /CCDL/) print > "ccdl.txt"; else print > "cc.txt"}' test.log

####Demo  小案例

    #计算log文件的大小
    $ls -l *.log|awk '{sum+=$5} END {print sum}'
    102610686
    #打印99乘法表
    $seq 9 | sed 'H;g' | awk -v RS='' '{for(i=1;i<=NF;i++)printf("%dx%d=%d%s", i, NR, i*NR, i==NR?"\n":"\t")}'
    1x1=1
    1x2=2   2x2=4
    1x3=3   2x3=6   3x3=9
    1x4=4   2x4=8   3x4=12  4x4=16
    1x5=5   2x5=10  3x5=15  4x5=20  5x5=25
    1x6=6   2x6=12  3x6=18  4x6=24  5x6=30  6x6=36
    1x7=7   2x7=14  3x7=21  4x7=28  5x7=35  6x7=42  7x7=49
    1x8=8   2x8=16  3x8=24  4x8=32  5x8=40  6x8=48  7x8=56  8x8=64
    1x9=9   2x9=18  3x9=27  4x9=36  5x9=45  6x9=54  7x9=63  8x9=72  9x9=81


####怎么写脚本，后面在学习
>引用
>[AWK简明教程](http://coolshell.cn/articles/9070.html)
