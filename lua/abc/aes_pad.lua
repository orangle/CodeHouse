-- 给AES加密解密字符 补位和清理工作 16位为例子

local addpad = function(plain, pad, size)
    local bsize = size or 16
    local pad = pad or "{"
    local n = bsize - string.len(plain)%bsize
    return plain..string.rep(pad, n)
end

local cleanpad = function(plain, pad)
    local pad = pad or "{"
    local res, _  = string.gsub(plain, pad.."*$", '')
    return res
end

t = {"z", "10.0.11.23", "12323,34324,10:21:21:dt", "432{fsdf..*"}

for _, v in ipairs(t) do
    print(addpad(v))
    print(cleanpad(addpad(v)))
end
