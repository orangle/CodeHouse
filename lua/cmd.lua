-- how lua run shell cmd 

function cmd1()
    local handle = io.popen("ls -lsh")
    local result = handle:read("*a")
    handle:close()
    print(result)
end 

function cmd2()
    
end 
