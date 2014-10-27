lua 小知识点
=============

####调试：
1  可以在执行文件的时候添加一个 -i 参数，文件执行完毕进入调试交互模式

	[root]/root/lua$lua -i test.lua
	Lua 5.2.0  Copyright (C) 1994-2011 Lua.org, PUC-Rio
	> print (twice(2))
	4
	>
	[root]/root/lua$cat test.lua
	function twice(x)
		return 2*x
	end

从这里可以看到，执行之后函数已经在命名空间中，不需要导入就可以直接调试


2  使用函数dofile 在交互模式中引入文件，然后调试

	[root]/root/lua$lua
	Lua 5.2.0  Copyright (C) 1994-2011 Lua.org, PUC-Rio
	> dofile("test.lua")
	> print (twice(4))
	8
	>

####规范：
* 标识符是有字母，数字，下划线组成，不能用数字开头，不能使用保留字作为标识符。
* 避免使用 _VER ，下划线开头，多个大写字母这种标识符，lua中有特殊用途。
* lua区分大小写，大小写不同当作不同的变量


####注释
1 行注释： --xxxx
2 快注释： --[[
                         xxxx
                --]]

####变量声明
全局变量：
没有声明的变量访问结果是 nil

	> print (b)
	nil
	> b = 10
	> print (b)
	10

全局变量的删除：

	b = nil


#### 程序解释器

*   源码文件的第一行如果是使用**#**号开头就会忽略，这个和linux其他脚本语言类似，用来指定文件的执行解释器
*   lua  \[options\] [filename]  常用的几个选项

1  -e  后面直接输入代码

	[root]/root/lua$lua -e 'print ("orangleliu")'
	orangleliu

2  -l  用来加载文件库
3  -i  执行完文件进入交互模式

####类型和值

#####基础的数据类型有8种

	inl  空
	boolean  布尔
	number 数字
	string 字符串
	userdata  自定义类型
	function 函数
	thread 线程
	table 表

要查看某个变量的类型使用 type() 函数

nil 是全局变量的默认值，也相当于 ”无效值“
boolean nil为**假**， 数字0和空字符串为**真**

字符串类型是不可变的（有点类似python中的字符串）
字符串可以使用单引号或者双引号来表示
如果是包含一段字符串呢，可以使用 [[]] 来包括， 类似python中的 三个引号

.. 是lua中的字符连接符：

	> print ('nihao'..'lllll')
	nihaolllll

字符串墙转为数字： tonumber


数字转换成字符串： tostring










