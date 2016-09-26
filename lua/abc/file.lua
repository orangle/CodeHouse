--lua file operation,read, write, create, remove, find string, log, sleep

function wfile()
    -- 写入的时候多个字符连接，用，号即可
    local file = io.open("test.txt", "w")
    file:write("version=v5.0 \n")
    file:write("Today ", "is ", string.format("good %s \n", "day"))
    file:close()
end

function fread()
    local file = io.open("test.txt", "r")
    if file ~= nil then
        print(file:read("*all"))
        file:close()
    else
        print("file not existed")
        return 0
    end
    io.close(file)
end

--[[
while true do
    local lines, next = f:read(1024, "*line")
    if not lines then bread end 

end
--]]

function fremove()
    ok, err = os.remove("test.txt")
    if not ok then
        print("error"..err)
    else
        print("ok!")
    end
end


function file_exists(name)
   local f=io.open(name,"r")
   if f~=nil then io.close(f) return true else return false end
end


--fremove()
--fread()
wfile()
