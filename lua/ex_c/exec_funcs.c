#include <stdio.h>
#include <stdlib.h>
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"

int l_bar(lua_State *L){
    //get params
    const char *str = lua_tostring(L, -1);
    int length = 1;
    while(1){
        char c = str[length];
        if(c == '\0')
            break;
        length++;
    }
    //set return value
    lua_pushstring(L, str);
    lua_pushnumber(L, length);
    printf("c: %s len is %d\n", str, length);

    //2 is return number to lua call
    return 2;
}


// 调用lua脚本中的函数
int main(void){

    lua_State *L = luaL_newstate();
    luaL_openlibs(L);
    luaL_dofile(L, "hello.lua");
    printf("lua dofile ..... end\n");
   
    //exec f1 function
    lua_getglobal(L, "f1");
    //L: stact 0:number of params 0:number of return value 0:errfun
    //int lua_pcall (lua_State *L, int nargs, int nresults, int errfunc);
    lua_pcall(L, 0, 0, 0);

    //exec f2 function
    lua_getglobal(L, "f2");
    lua_pushnumber(L, 2);
    lua_pushnumber(L, 3);
    //stack f1 f2 2 3
    lua_pcall(L, 2, 1, 0);
    //stack f1 f2 2 3 res
    int res1 = lua_tonumber(L, -1);
    printf("f2 return value is %d\n", res1);

    //exec f3 function, in f3 will call a c function 
    lua_pushcfunction(L, l_bar);
    lua_setglobal(L, "bar");

    lua_getglobal(L, "f3");
    lua_pushstring(L, "shijian");
    lua_pcall(L, 1, 2, 0);
    if(lua_isnil(L, -1)){
        printf("c: f3 return is nil\n");
    }else{
        int len = lua_tonumber(L, -1);
        int res2 = lua_tonumber(L, -2);
        printf("c: f3 res is (%d, %d) \n", res2, len); 
    }

    //释放state
    lua_close(L);
    return 1;
}
