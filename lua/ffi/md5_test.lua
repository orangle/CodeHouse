local md5lib = require "md5"
local md5 = md5lib:new()

if not md5 then 
    print("not have md5 object")
end 

md5:update("lzz")
print(md5:final())



