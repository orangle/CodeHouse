-- how lua run shell cmd 

function cmd1()
    cmd = "wget -T 20 -t 2 -c http://127.0.0.1/2/2_150320162522828.tar -O /home/lzz/workpalce/vus/client_lua/download/2_150320162522828.tar"
    local handle = io.popen(cmd)
    local result = handle:read("*a")
    handle:close()
    print(result)
end 

cmd1()
    
