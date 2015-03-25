--简单模块写法的模板

local _M = {}

function _M.is_ip(ip)
    if ip == nil or type(ip) ~= "string" then 
        return false 
    end 

    --check ipv4
    local chunks = {ip:match("(%d+)%.(%d+)%.(%d+)%.(%d+)")}
    if (#chunks == 4) then
        for _, v in pairs(chunks) do 
                if (tonumber(v)) < 0 or tonumber(v) > 255 then 
                    return false 
                end 
        end 
        return true 
    else
        return false 
    end 
end 


function _M.test_ip()
    local ips = {
       "127.0.0.1",
       "255.255.255.255",
       "192.169.1.-1",
       "erya.com",
       12.9,
       "114.114.114.114"
    }

    for k,v in pairs(ips) do
        print(v, _M.is_ip(v))
    end
end 

return _M
