--添加路径
--require模块的时候也要使用局部变量的形式
--
package.path = package.path .. ";../?.lua"
local ip = require "ip"

print(ip.test_ip(12))
