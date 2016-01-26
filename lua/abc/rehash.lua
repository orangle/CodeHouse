-- 测试rehash

function test1()
    for i = 1, 10000000 do
        local a = {}
        a[1] = 1
        a[2] = 2
        a[3] = 3
    end
end


function test2()
    for i = 1, 10000000 do
        local a = {true, true, true}
        a[1] = 1
        a[2] = 2
        a[3] = 3
    end
end

test1()
--test2()
