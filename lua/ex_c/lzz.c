/*学习写lua c拓展，对于一些简单的函数自己提供C拓展
 *ubuntu 编译 gcc -fPIC -shared -llua lzz.c -o lzz.so -I/usr/include/lua5.1 -std=gnu99
 */

#include "unistd.h"
#include "sys/types.h"
#include "sys/stat.h"

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


static int fsize (lua_State *L){
    const char *filename = lua_tostring(L, 1);
    struct stat st;
    if (stat(filename, &st) == 0){
        lua_pushinteger(L, st.st_size);
        return 1;
    }else{
        lua_pushnil(L);
        lua_pushstring(L, "get size error");
        return 2;
    }
}


static const struct luaL_Reg libs[] = {
    {"hello", hello_c},
    {"currentdir", get_dir},
    {"fsize", fsize},
    {NULL, NULL}  /*the end*/
};

int luaopen_lzz (lua_State *L){
    luaL_register(L, "lzz", libs);
    return 1;
}

