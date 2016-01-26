-- https://gist.github.com/westhood/5271465
local ffi = require("ffi")

ffi.cdef[[
typedef unsigned char uuid_t[16];
void uuid_generate(uuid_t out);
void uuid_unparse(const uuid_t uu, char *out);
]]

local libuuid = ffi.os == "OSX" and ffi.C or ffi.load("uuid")

function uuid()
    local buf = ffi.new('uint8_t[16]')
    local uu = ffi.new('uint8_t[?]', 36)
    libuuid.uuid_generate(buf)
    libuuid.uuid_unparse(buf, uu)
    return ffi.string(uu, 36)
end

print(uuid())
