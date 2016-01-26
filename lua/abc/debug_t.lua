-- 简单模拟异常处理过程
local debug = debug

function hello()
    local a = 20
    print(a[10])
end

function errHandle()
    print(debug.traceback())
end

if xpcall(hello, errHandle) then
    print("ok")
else
    print("error")
end
