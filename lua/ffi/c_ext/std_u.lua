-- 调用标准库
local ffi = require("ffi")

-- 定义 使用C语法 一般从头文件获取
ffi.cdef[[
void Sleep(int ms);
int poll(struct pollfd *fds, unsigned long nfds, int timeout);
]]


local sleep
-- 根据不同平台调用不同的C接口
if ffi.os == "Windows" then
  function sleep(s)
    ffi.C.Sleep(s*1000)
  end
else
  function sleep(s)
    ffi.C.poll(nil, 0, s*1000)
  end
end

for i=1,160 do
  io.write("."); io.flush()
  sleep(0.01)
end
io.write("\n")
