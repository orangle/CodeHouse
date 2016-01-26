-- lua字符串的一些操作

-- insert 效率低一些
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

--line：待分割字符串
--sep：分割符，
--maxsplit:分割次数
function split(line, sep, maxsplit)
    if string.len(line) == 0 then
        return {}
    end
    sep = sep or ' '
    maxsplit = maxsplit or 0
    local retval = {}
    local pos = 1
    local step = 0
    while true do
        local from, to = string.find(line, sep, pos, true)
        step = step + 1
        if (maxsplit ~= 0 and step > maxsplit) or from == nil then
            local item = string.sub(line, pos)
            retval[step] = item
            break
        else
            local item = string.sub(line, pos, from-1)
            retval[step] = item
            pos = to + 1
        end
    end
    return retval
end


function arr_join(tb, pat)
    return table.concat(tb, pat)
end


local raw = {"aaa", "bbb", "ccc"}
local jraw = arr_join(raw, "|")
--print(jraw)

sraw = str_split("dfdsfdsfsd 343", "|")
--foreach 给定回调执行
print(#sraw)
table.foreach(sraw, function(k,v) print(v) end)

ssraw = split(jraw, "|", 1)
print(#ssraw)
table.foreach(ssraw, function(k,v) print(v) end)

