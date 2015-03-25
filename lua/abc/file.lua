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
        print(file:read())
        file:close()
    else
        print("file not existed")
        return 0 
    end 

end 

function fremove()
    ok, err = os.remove("test.txt")
    if not ok then 
        print("error"..err)
    else
        print("ok!")
    end 
end 

--fremove()
--fread()
wfile()
