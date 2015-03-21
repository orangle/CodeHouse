-- some demo of lua coroutine, 这种实现跟用一个线程有啥区别。。
local socket = require "socket"

function check()
    while true do 
        socket.sleep(1)
        print("find task file, co.............")
        coroutine.yield(coo)
    end 
end 

coo = coroutine.create(
    function()
        while true do 
            check() 
            print("阻塞线程 前")
            coroutine.yield()
            socket.sleep(5)
            print("阻塞线程 后")
        end 
    end 
)

coroutine.resume(coo)
