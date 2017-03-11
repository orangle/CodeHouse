local first = ARGV[1]
local last = ARGV[2]
redis.call('SET', 'name', first..last)

return "save ok"

--[[
 # redis-cli --eval test.lua  , orangle liu
"save ok"

# redis-cli get name
"orangleliu"

注意逗号2边的空格
]]--
