--how to use c json
--cjson 文档 https://www.kyne.com.au/~mark/software/lua-cjson-manual.html

--import
local cjson = require "cjson"
-- cjson safe 和 cjson作用一样，只是发生错误的时候会返回 nil
local cjson_safe = require "cjson.safe"

print(cjson._VERSION)

-- settings json解析还可以进行一些配置
depth = cjson.encode_max_depth(20) --default 1000

-- encode
-- support types: boolean, nil, num, string, table
local json_t = {
    {name="lzz", age=18, book="lua"},
    {name="xiaoniu", age=20, play="python"}
}
local json_res = cjson.encode(json_t)
print(json_res)

local json_so = cjson.decode(json_res)
print(#json_so)

-- json safe 对于错误的解析返回 nil, err
local json_tt = [[ {"key:"value"} ]]
print(cjson_safe.decode(json_tt))

-- 稀疏数组的处理
local arr = {1, 2}
arr[5] = 3
print(cjson.encode(arr))
