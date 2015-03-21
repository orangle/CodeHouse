/*学习写lua c拓展，对于一些简单的函数自己提供C拓展
 *ubuntu 编译 gcc -fPIC -shared -llua lua_socketlib.c -o socketlib.so -I/usr/include/lua5.1 -std=gnu99
 */

#include "unistd.h"

#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

#define getcwd_error "Function 'getcwd' not provided by system"
#define MAXPATHLEN 1024

/*simple demo*/
static int hello_c (lua_State *L){
    const char *hello = "Hello boy";
    lua_pushstring(L, hello);  //return a string value
    return 1;  // the number of return values
}

/*this function returns then current directory*/
static int get_dir (lua_State *L){
    char *path;
    char buf[MAXPATHLEN];
    if ((path = getcwd(buf, MAXPATHLEN)) == NULL){
        lua_pushnil(L);
        lua_pushstring(L, getcwd_error);
        return 2;
    }
    else {
        lua_pushstring(L,path);
        return 1;
    }
}


static const struct luaL_Reg libs[] = {
    {"hello", hello_c},
    {"currentdir", get_dir},
    {NULL, NULL}  /*the end*/
};

int luaopen_lzz (lua_State *L){
    luaL_register(L, "lzz", libs);
    return 1;
}

