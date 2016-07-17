#include "lua.h"
#include "lauxlib.h"

//C API 最主要的就是理解 lua state stack 的工作方式
int main(){
    //初始化 state
    lua_State *L = luaL_newstate();
    //载入 lib
    luaL_openlibs(L);
    //执行lua 文件
    luaL_dofile(L, "hello.lua");

    //读取lua文件中的变量 L是一个栈 
    lua_getglobal(L, "lzz");
    lua_getglobal(L, "foo");
    int i = lua_tonumber(L, -1);
    printf("foo is %d\n", i);

    if(lua_isnil(L, -2)){
        printf("lzz is nil\n"); 
    }else{
        int j = lua_tonumber(L, -2);
        printf("lzz is %d\n", j);
    }

    return 1;
}
