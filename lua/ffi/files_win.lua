-- https://gist.github.com/XuJiandong/2300963
local ffi = require("ffi")
FfiFs = {}

ffi.cdef[[
typedef struct _finddata32_t
{
    uint32_t  attrib;
    uint32_t  time_create;    /* -1 for FAT file systems */
    uint32_t  time_access;    /* -1 for FAT file systems */
    uint32_t  time_write;
    uint32_t  size;
    char      name[260];
} _finddata32_t;
int _findfirst32(const char* filespec, _finddata32_t*);
int _findnext32(int handle, struct _finddata32_t *fileinfo);
int _findclose(int handle);
int _chdir(const char *dirname);
char *_getcwd(char *buffer, int maxlen);
]]

--[[
#define _A_NORMAL       0x00    /* Normal file - No read/write restrictions */
#define _A_RDONLY       0x01    /* Read only file */
#define _A_HIDDEN       0x02    /* Hidden file */
#define _A_SYSTEM       0x04    /* System file */
#define _A_SUBDIR       0x10    /* Subdirectory */
#define _A_ARCH         0x20    /* Archive file */
]]

function FfiFs.Dir(dir)
    local C = ffi.C
    local dirContent = {}
    function ProcessEntry(cdata)
        local entry = {}
        entry.name = ffi.string(cdata.name)
        if bit.band(cdata.attrib, 0x20) > 0 then
            entry.attrib = "file"
        elseif bit.band(cdata.attrib, 0x10) > 0 then
            entry.attrib = "dir"
        else
            entry.attrib = "unknown"
        end
        entry.size = cdata.size
        return entry
    end

    local cdata = ffi.new("struct _finddata32_t")
    local handle = C._findfirst32(dir, cdata)
    if handle == -1 then return end
    table.insert(dirContent, ProcessEntry(cdata))
    while true do
        local e = C._findnext32(handle, cdata)
        if e ~= 0 then break end
        table.insert(dirContent, ProcessEntry(cdata))
    end
    C._findclose(handle)
    return dirContent
end

function FfiFs.Getcwd()
    local length = 2048
    local cDir = ffi.new("char[?]", length)
    ffi.C._getcwd(cDir, length)
    return ffi.string(cDir)
end

function FfiFs.Chdir(dir)
    local v = ffi.C._chdir(dir)
    if v == 0 then return true end
    return false
end

-- test
local content = FfiFs.Dir("./*")
if content then
    for i, k in ipairs(content) do
        print(k.attrib .. " -> " .. k.name .. "(" .. k.size .. ")")
    end
else
    print("nothing found")
end

local cwd = FfiFs.Getcwd()
print(cwd)
FfiFs.Chdir("C:/")
local cwd = FfiFs.Getcwd()
print(cwd)
