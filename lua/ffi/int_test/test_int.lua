-- https://gist.github.com/aktau/9732390
-- compare the semantics of a few disparate types:
-- * lua numbers
-- * luajit 64-bit integers
-- * ctype 64-bit integers (int64_t)
-- * luajit metatype (packed struct w. int64_t)

local ffi = require("ffi")
local int = require("int")
local time = require("ctime")

local i64 = ffi.typeof("int64_t")

local atoms = {
    {"luajit 64-bit int  ", 1LL},
    {"ctype 64-bit int   ", i64(1)},
    {"metatype 64-bit int", int(1)},
    {"lua number         ", 1},
}

local function printf(s,...)
    return io.write(s:format(...))
end

local function typeinfo(v)
    local suf = "            "

    if ffi.istype("packed_int_t", v) then
        suf = "/packed_int_t"
    elseif ffi.istype("int64_t", v) then
        suf = "/int64_t     "
    elseif type(v) == "cdata" then
        suf = "/unknown       "
    end

    return type(v) .. suf
end

local function test(n, info)
    print("perform 1 + ", n, info, "for all types")
    for _, atom in pairs(atoms) do
        local desc, a = atom[1], atom[2]
        local v = a + n
        local s = "      %s + %s => %s"
        s = s:format(typeinfo(a), typeinfo(n), typeinfo(v))
        print("    " .. desc .. " + " .. info, v, s)
    end

    print("\n")
end

test(3LL, atoms[1][1])
test(i64(3.14), atoms[2][1])
test(int(3.14), atoms[3][1])
test(3.14, atoms[4][1])

-- benchmarking! Such fun

print("welcome to benchmarking academy, where no best practices are followed")
print("=====================================================================")
printf("  JIT:            %s\n", (jit.status() == true) and "enabled" or "disabled")
printf("  Version:        %s\n", jit.version)
printf("  OS:             %s\n", jit.os)
printf("  Arch:           %s\n", jit.arch)
print("")

local function cast_to_int(a, b, it)
    local comb = a + b

    for i = 1,it do
        local x = a + b
        local y = x + a - x
        local z = y - x + b
        comb = int(comb + z)
    end

    return comb
end

local function add_loop(a, b, it)
    local comb = a + b

    for i = 1,it do
        local x = a + b
        local y = x + a - x
        local z = y - x + b
        comb = comb + z
    end

    return comb
end

local function mul_loop(a, b, it)
    local comb = a + b

    for i = 1,it do
        local x = a * b
        local y = x / a
        local z = y / b
        comb = comb * z
    end

    return comb
end

local it = 1000000000

local function bench(desc, fn, it)
    -- printf("performing %d iterations of %s\n", it, desc)
    local t1 = time.now()
    local res = fn(it)
    local t2 = time.now()
    printf("%f msec passed, result = %s (%s)\n", time.elapsed_usecs(t1, t2) / 1000, tostring(res), desc)
end

local do_add_loop = true
local do_mul_loop = true

local function compare_methods(fn, desc)
    local createfn = function(a, b)
        return function(it)
            return fn(a, b, it)
        end
    end

    printf("BENCHMARKING => %s\n", desc)
    printf("========================\n")

    for i=1,3,2 do
        local it = 1000000000 * i
        printf("%d iterations:\n", it)
        io.write("    "); bench("regular lua number " .. desc, createfn(5, 7), it)
        io.write("    "); bench("mixed " .. desc .. " (should give the same result as regular mul/div)", createfn(int(5), 7), it)
        io.write("    "); bench("packed int " .. desc, createfn(int(5), int(7)), it)
        io.write("    "); bench("LuaJIT 64-bit int " .. desc .. " (should be a bit faster than packed int since it doesn't have to box/unbox all the time)", createfn(5LL, 7LL), it)
        print("\n")
    end
end

compare_methods(cast_to_int, "cast to int")

if do_add_loop then
    compare_methods(add_loop, "add/sub")
end

if do_mul_loop then
    compare_methods(mul_loop, "mul/div")
end
