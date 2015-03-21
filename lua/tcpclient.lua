-- tcp client
local socket = require("socket")

local host = "127.0.0.1"
local port = 3691
local sock = assert(socket.connect(host, port))
sock:settimeout(0)

local recvt, sendt, status 
local send_str = "Q=0 \n"

while 1 do
    assert(sock:send(send_str))

    recvt, sendt, status = socket.select({sock}, nil, 1)
    while #recvt > 0 do 
        local reps, resp_status = sock:receive()
        if resp_status ~= "closed" then
            if reps then
                print(reps)
                recvt, sendt, status = socket.select({sock}, nil, 1)
                sock:close()
            end
        end 
    end 
end 
