-- 生成随机数或者随机字符串
local math = math
local os = os

-- 并发下并不随机
local function gen_nonce()
    local charset= "0123456789.abcdefghijklmnopqrstuvwxyz-=_+!ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    math.randomseed(os.time())
    --math.randomseed(os.clock()*100000000000)
    local nonce=''
    for a = 1, 64 do
        local index=math.random(999999)%string.len(charset)
        nonce=nonce .. string.sub(charset,index+1,index+1);
    end
    return nonce
end

-- 可以解决一些问题
local function random1()
    math.randomseed(os.clock()*100000000000)
    return math.random(999999)
end

for i = 1, 100000 do
    print(gen_nonce())
    --print(random1())
end
