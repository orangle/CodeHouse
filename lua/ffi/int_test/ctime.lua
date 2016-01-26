-- https://gist.github.com/aktau/9732390
-- taken from:
-- http://www.freelists.org/post/luajit/gettimeofday-day-returning-same-value-possible-bug-or,2

local ffi = require("ffi")

ffi.cdef[[
   struct timeval {
      long sec;
      long usec;
   };

   int gettimeofday(struct timeval *restrict tp, void *restrict tzp);
]]

local tp = ffi.new("struct timeval")

local timeval = ffi.typeof("struct timeval")

local function elapsed_usecs(start, finish)
    local s = tonumber(finish.sec - start.sec)
    local us = tonumber(finish.usec - start.usec)
    return s * 1000000 + us
end

local function now()
    local t = timeval()
    ffi.C.gettimeofday(t, nil)
    return t
end

local function gettime()
   ffi.C.gettimeofday(tp, nil)
   print("***", tp.sec, tp.usec)
   return tonumber(tp.sec) + (tonumber(tp.usec) / 1000000)
end

return {
    elapsed_usecs = elapsed_usecs,
    now = now,
    gettime = gettime,
}
