-- lua字符串的一些操作


-- split and join http://lua-users.org/wiki/SplitJoin
-- spilt 把字符串按照某个字符串 拆分，返回一个array

function str_split(str, pat)
    local t = {}  -- NOTE: use {n = 0} in Lua-5.0
    local fpat = "(.-)" .. pat
    local last_end = 1
    local s, e, cap = str:find(fpat, 1)
    while s do
        if s ~= 1 or cap ~= "" then
            table.insert(t,cap)
        end
        last_end = e+1
        s, e, cap = str:find(fpat, last_end)
    end
    if last_end <= #str then
        cap = str:sub(last_end)
        table.insert(t, cap)
    end
    return t
end

function arr_join(tb, pat)
    return table.concat(tb, pat)
end


local raw = {"aaa", "bbb", "ccc"}
local jraw = arr_join(raw, "|")
print(jraw)
sraw = str_split("dfdsfdsfsd 343", "|")
--foreach 给定回调执行
print(#sraw)
table.foreach(sraw, function(k,v) print(v) end)
