-- how lua run shell cmd

function cmd1()
    cmd = "ls|wc -l"
    local handle = io.popen(cmd)
    local result = handle:read("*a")
    handle:close()
    res = string.gsub(result, "\n", "")
    print(tonumber(res)==0)
end

cmd1()

