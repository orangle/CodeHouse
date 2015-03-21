--添加路径
package.path = package.path .. ";../?.lua"
local ip = require "ip"

print(ip.test_ip(12))
