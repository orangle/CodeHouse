#include <stdio.h>
#include <stdlib.h>
#include "lua.h"
#include "lauxlib.h"

//C API 最主要的就是理解 lua state stack 的工作方式
int main(void){
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);

    

    //释放state
    lua_close(L);
    return 1;
}
