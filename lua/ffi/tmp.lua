-- https://gist.github.com/justincormack/3258916

local ffi = require "ffi"
local bit = require "bit"

local C = ffi.C

local S = {}
local t = {}
local s = {}

ffi.cdef [[
typedef uint32_t socklen_t;

struct nlmsghdr {
  uint32_t           nlmsg_len;
  uint16_t           nlmsg_type;
  uint16_t           nlmsg_flags;
  uint32_t           nlmsg_seq;
  uint32_t           nlmsg_pid;
};
struct ifinfomsg {
  unsigned char   ifi_family;
  unsigned char   __ifi_pad;
  unsigned short  ifi_type;
  int             ifi_index;
  unsigned        ifi_flags;
  unsigned        ifi_change;
};
struct rtattr {
  unsigned short  rta_len;
  unsigned short  rta_type;
};


]]

t.macaddr = ffi.metatype("struct {uint8_t mac_addr[6];}", {
  __tostring = function(m)
    local hex = {}
    for i = 1, 6 do
      hex[i] = string.format("%02x", m.mac_addr[i - 1])
    end
    return table.concat(hex, ":")
  end,
  __new = function(tp, str)
    local mac = ffi.new(tp)
    if str then
      for i = 1, 6 do
        local n = tonumber(str:sub(i * 3 - 2, i * 3 - 1), 16)
        mac.mac_addr[i - 1] = n
      end
    end
    return mac
  end,
})


t.ifinfomsg = ffi.typeof("struct ifinfomsg")
t.nlmsghdr = ffi.typeof("struct nlmsghdr")
t.rtattr = ffi.typeof("struct rtattr")

s.nlmsghdr = ffi.sizeof(t.nlmsghdr)
s.rtattr = ffi.sizeof(t.rtattr)


local function align(len, a) return bit.band(tonumber(len) + a - 1, bit.bnot(a - 1)) end


local function nlmsg_align(len) return align(len, 4) end
local nlmsg_hdrlen = nlmsg_align(s.nlmsghdr)

local function nlmsg_length(len) return len + nlmsg_hdrlen end

local function ifla_getmsg(args, messages, values, tab, lookup, af)
  local msg = table.remove(args, 1)
  local value

  local tp = t.macaddr

  value = table.remove(args, 1)
  if not value then error("not enough arguments") end


  if tp == "asciiz" then
    error("not used")
  else
    if type(tp) == "string" and tp == "address" then
      tp = S.addrtype[af]
    end
    if not ffi.istype(tp, value) then
      value = tp(value)
    end
  end

  len = nlmsg_align(s.rtattr) + nlmsg_align(ffi.sizeof(tp))

  messages[#messages + 1] = t.rtattr
  messages[#messages + 1] = tp
  values[#values + 1] = {rta_type = msg, rta_len = 0}
  values[#values + 1] = value

  return len, args, messages, values
end

local function ifla_f(tab, lookup, af, ...)
  local len
  local messages, values = {}, {}

  local args = {...}
  while #args ~= 0 do
    len, args, messages, values = ifla_getmsg(args, messages, values, tab, lookup, af)
  end

end


ifla_f("ifla", "IFLA_", nil, "address", "46:9d:c9:06:dd:dd")
