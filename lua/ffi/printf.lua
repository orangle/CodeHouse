print(jit.version)
print(jit.version_num)
print(jit.os)
print(jit.arch)

print('---------------')

local ffi = require("ffi")
ffi.cdef[[
int printf(const char *fmt, ...);
]]

ffi.C.printf("Hello %s \n", "girl")

print(package.path)
print(package.cpath)
