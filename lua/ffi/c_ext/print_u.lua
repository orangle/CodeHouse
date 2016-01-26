local ffi = require [[ffi]]

ffi.cdef [[
typedef struct __IO_FILE FILE;
FILE *stdout;
int printf(const char *fmt, ...);
void setbuf(FILE *stream, char *buf);
void *malloc(size_t size);
void *memset(void *s, int c, size_t n);
]]

local buffer = ffi.C.malloc(1024)

ffi.C.setbuf(io.stdout, buffer)
ffi.C.printf([[Hello]])

ffi.C.memset(buffer, 0, 1024)

local buffer = ffi.C.malloc(1024)
ffi.C.setbuf(io.stdout, buffer)
ffi.C.printf([[ World!
]])
-- 不好使

