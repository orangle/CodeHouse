--table使用的技巧

-- table as list
function listt()
    --数组从1开始
    local nlist = {}
    for i = 1,10 do
        nlist[i] = i
    end
    print(#nlist)
end

-- table 元素连接
function concattb()
    local a = {1, 3, 4, 'lzz', 'sj'}
    print(table.concat(a))
    print(table.concat(a, '>'))
    print(table.concat(a, '=', 3, #a))
end

-- 返回最大的索引编号
function maxntb()
    a = {1, 3}
    print('len:'..#a..' max index:'..table.maxn(a))
    table.insert(a, 10, 10)
    print('len:'..#a..' max index:'..table.maxn(a))
end


function sorttb()
    lines = {
      name = 'lzz',
      age = '18',
    }
    a = {}
    for n in pairs(lines) do table.insert(a, n) end
    table.sort(a)
    for _,n in ipairs(a) do print(n,lines[n]) end
end


--listt()
--concattb()
--maxntb()
sorttb()
