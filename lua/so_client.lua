-- use luasocket client

socket = require("socket")
print(socket._VERSION)

local host = "vusd.wificdn.com"
local port = 3691
local c = assert(socket.connect(host, port))
c:settimeout(5)
c:send("Q=0\n")
local res, rep_status = c:receive() 
print(res) 
c:close() 

---------------------------------------------------

function receive(conn)
    conn:settimeout(0)
    local s, status = conn:receive(2^10)
    return s, status
end 

function is_empty(ss)
    return ss==nil or ss==""
end 


function basic_req()
    local host = '127.0.0.1'
    local port = 3691
    --local count = 0   --count number of bytes read 
    c = assert(socket.connect(host, port))
    c:send("GET / HTTP/1.0\r\n\r\n")
    while true do
        local s, status = receive(c)
        --count = count + string.len(s)
            if not is_empty(s) then
                print(s)
            end 
        if status == "closed" then break end 
    end 
    -- print("receive btyes:"..count)
    c:close()
end

