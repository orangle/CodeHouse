-- some demo of lua coroutine, 这种实现跟用一个线程有啥区别。。
local socket = require "socket"

function check()
        socket.sleep(1)
        print("find task file, co.............")
        coroutine.yield()
end 

coo = coroutine.create(
    function()
        while true do 
            print("阻塞线程 前")
            coroutine.yield()
            socket.sleep(5)
            print("阻塞线程 后")
        end 
    end 
)

print(coo)
print(coroutine.status(coo))
while true do 
    coroutine.resume(coo)
    check()
end 
