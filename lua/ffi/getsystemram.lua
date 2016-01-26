-- https://gist.github.com/josefnpat/5cfc722952c77d572f4b
-- Gets the total amount of RAM in the system, in MB.
function GetSystemRAM()
  return 0
end

if jit then
  local ffi = require("ffi")

  ffi.cdef [[
  typedef struct SDL_version
  {
      uint8_t major;
      uint8_t minor;
      uint8_t patch;
  } SDL_version;

  void SDL_GetVersion(SDL_version *ver);

  int SDL_GetSystemRAM(void);
  ]]

  local sdl = ffi.os == "Windows" and ffi.load("SDL") or ffi.C

  local version = ffi.new("SDL_version[1]")
  sdl.SDL_GetVersion(version)

  if version[0].major == 2 and (version[0].minor > 0 or version[0].patch > 0) then
    GetSystemRAM = function()
      return tonumber(sdl.SDL_GetSystemRAM())
    end
  end
end
