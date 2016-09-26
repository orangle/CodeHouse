-- lua 字符串匹配相关api使用
local string = string
local math = math

local ts = "You name is Lzz"
local ts1 = "#mac,ip,iface,in,out,total,first_date,last_date"

-- 字符串长度
local len = string.len(ts)
print("ts length is "..len)

-- 复制字符串
print(string.rep("*", 60))

-- 大写
print(string.lower(ts))

-- 小写
print(string.upper(ts))

-- 反转
print("ts reverse:"..string.reverse(ts))

-- 子串 正负值
-- 从第5个开始取到最后
print("ts sub 5:"..string.sub(ts, 5))
-- from 1 to 3，contain 1 and 3
print("ts sub 1～3:"..string.sub(ts, 1, 3))
--
print("ts sub -3:"..string.sub(ts, -3))

--format
print(string.format("%s %q", "Hello", "Lua user!")) --string quote
print(string.format("%c%c%c", 76,117,97))  --char
print(string.format("%f, %g", math.pi, math.pi)) --float
print(string.format("%o, %x, %X", -100,-100,-100)) -- octal, hex, hex

-- match: find gmatch gsub match
-- find 可以结合sub来提取字符串
local i, j = string.find(ts1, "#")
print("find "..tostring(i).." "..tostring(j))
print(string.find(ts, "#"))

--match 返回的是字串
print("match "..string.match(ts1, "#"))
print(string.match("today is 2016-09-25", "%d+-%d+-%d+"))

--gsub 替换匹配到的所有字符串
print("gsub "..string.gsub(ts, "z", "HHH"))
print("gsub "..string.gsub(ts, "z", "HHH", 1)) --just once

--gmatch 返回一个迭代器


--[[
匹配元字符

%a 字母
%c 控制字符
%d 数字
%l 小写字母
%p 标点
%s 空白字符
%u 大写字母
%w 字母和数字
%x 十六进制
%z 内部表示为0的字符

换成大写是它们的补集 %A 表示非字母

%b()
%b[]
%b{}
%b<>
自动匹配括号内的字符

. 任何字符
%  转译字符
%% 表示%
+  一次或多次
*  0次或多次 贪婪
-  0次或多次 非贪婪
?  出现0次或者一次
^  开头
$  结尾
()
[]
--]]
