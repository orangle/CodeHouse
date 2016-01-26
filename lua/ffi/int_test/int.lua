-- https://gist.github.com/aktau/9732390

local ffi = require("ffi")

-- lua integer module, int(some_number) creates an integer which will follow
-- vimscript semantics when used in mathematical operations
--
-- vim promotion and conversion/casting rules:
-- int   [OP] int   = int
-- int   [OP] float = float
-- float [OP] float = float

-- unfortunately we can't do "typedef int64_t cint;" to create a metatype.
-- As per http://luajit.org/ext_ffi_api.html, thus we have to manually
-- box/unbox on top of the boxing luajit already does, this is not very
-- efficient of course. This also means that these integers will be
-- allocated on the heap (in LuaJIT, scalar values on the stack have no
-- metatable). This will be horrible, performance-wise.
ffi.cdef[[
typedef struct { int64_t x; } packed_int_t;
]]

local int -- the metatype, to be defined later

-- the following are a few helper functions that help emulating the
-- semantics of vim mathematical operations, I'm sure they can be made quite
-- a bit more efficient, but they'll do for now.

-- unpack the struct to reveal the value (if necessary)
local function val(v)
    if ffi.istype("packed_int_t", v) then
        return v.x
    end
    return v
end

-- repack the value into a struct (if necessary)
local function repack(v)
    if type(v) == "number" then
        return v
    end
    return int(v)
end

local function convert(a, b)
    if type(a) == "cdata" and type(b) == "cdata" then
        return a, b
    end

    return tonumber(a), tonumber(b)
end


local mt = {
    -- unary operators
    __unm = function(a)
        return int(-a.x)
    end,

    -- binary operators
    __add = function(a, b)
        a, b = convert(val(a), val(b))
        return repack(a + b)
    end,
    __sub = function(a, b)
        a, b = convert(val(a), val(b))
        return repack(a - b)
    end,
    __mul = function(a, b)
        a, b = convert(val(a), val(b))
        return repack(a * b)
    end,
    __div = function(a, b)
        a, b = convert(val(a), val(b))
        return repack(a / b)
    end,
    __pow = function(a, b)
        a, b = convert(val(a), val(b))
        return repack(a ^ b)
    end,

    -- binary relations
    __eq = function(a, b) return val(a) == val(b) end,
    __ne = function(a, b) return val(a) ~= val(b) end,
    __le = function(a, b) return val(a) <= val(b) end,
    __lt = function(a, b) return val(a) < val(b) end,
    __ge = function(a, b) return val(a) >= val(b) end,
    __gt = function(a, b) return val(a) > val(b) end,

    -- misc
    __tostring = function(v)
        return tostring(v.x)
    end,
    __concat = function(a, b)
        return tostring(val(a)) .. tostring(val(b))
    end,
}
int = ffi.metatype("packed_int_t", mt)

return int
