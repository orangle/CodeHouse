#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

int main(void){
    //init lua state
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);
    luaL_dofile(L, "hi.lua");
    luaL_dostring(L, "print ('hi C')");
    lua_close(L);
    return 0;
}
