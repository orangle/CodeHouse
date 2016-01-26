local ffi = require [[ffi]]

ffi.cdef[[
void *curl_easy_init();
int curl_easy_setopt(void *curl, int option, ...);
int curl_easy_perform(void *curl);
void curl_easy_cleanup(void *curl);
char *curl_easy_strerror(int code);
]]

local libcurl = ffi.load("libcurl")
local CURLOPT_URL = 10002

local curl = libcurl.curl_easy_init()

if curl then
    libcurl.curl_easy_setopt(curl, CURLOPT_URL, "http://baidu.com")
    res = libcurl.curl_easy_perform(curl)
    if res ~= 0 then
        print(ffi.string(libcurl.curl_easy_strerror(res)))
    end
  libcurl.curl_easy_cleanup(curl)
end
