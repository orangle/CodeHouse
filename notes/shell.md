Shell 编程要点  --if判断
=================

####IF 判断

之前也写过简单的shell脚本，也不是转职运维，和系统相关的工作比较少，所以不怎么熟练。
最近由于系统总是出现各种乱七八糟的问题，也没有人来协助，只好自己写shell脚本了，都是些基础的脚本，但由于shell的语法和通常的高级语言有些不一样，所以还是要系统的看下常用的部分。 if语句就是很重要的一个。

基本结构：  if语句块需要使用if结束

if condition
then
    statements
elif condition
    then statements
else
    statements
fi

tips：写法上需要注意的是
if后面的判断条件 方括号和之间的判断语句左右各要有一个空格（错了好几次了）


#####判断字符是否相等

#!/bin/bash
system=`uname -s`

if [ $system = "Linux" ]    #方括号内部两边有空格,等号两边也需要空格
then
    echo "Linux"
else
    echo "Other system"
fi


常用类型的判断写法(类比字符串)

1 字符串判断
str1 = str2　　　　　  当两个串有相同内容、长度时为真
str1 != str2　　　　　 当串str1和str2不等时为真
-n str1　　　　　　　 当串的长度大于0时为真(串非空)
-z str1　　　　　　　 当串的长度为0时为真(空串)
str1　　　　　　　　 当串str1为非空时为真

2 数字的判断
int1 -eq int2　　　　两数相等为真
int1 -ne int2　　　　两数不等为真
int1 -gt int2　　　　int1大于int2为真
int1 -ge int2　　　　int1大于等于int2为真
int1 -lt int2　　　　int1小于int2为真
int1 -le int2　　　　int1小于等于int2为真

3 文件的判断
-r file　　　　　用户可读为真
-w file　　　　　用户可写为真
-x file　　　　　用户可执行为真
-f file　　　　　文件为正规文件为真
-d file　　　　　文件为目录为真
-c file　　　　　文件为字符特殊文件为真
-b file　　　　　文件为块特殊文件为真
-s file　　　　　文件大小非0时为真
-t file　　　　　当文件描述符(默认为1)指定的设备为终端时为真

4 复杂逻辑判断
-a 　 　　　　　 与
-o　　　　　　   或
!　　　　　　　非

tips:
* -eq -ne -lt -nt只能用于整数，不适用于字符串，字符串等于用赋值号=
* =放在别的地方是赋值,放在if [ ] 里就是字符串等于,shell里面没有==的,那是c语言的等于
* 整数条件表达式，大于，小于，shell里没有> 和< ,会被当作尖括号，只有-ge,-gt,-le,lt



[参考文章](http://rfyiamcool.blog.51cto.com/1030776/738624)



















":"  符号在判断中表示true 也表示什么也不做
清空一个文件的内容

    : > comment.sh.bak
    #类似于
    cat /dev/null > comment.sh.bak







