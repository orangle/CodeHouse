/*学习写lua c拓展，对于一些简单的函数自己提供C拓展
 *ubuntu 编译 $ gcc -fPIC -shared -llua sleep.c -o orangleliu.so -I/usr/include/lua5.1 -std=gnu99 
 */

#include "unistd.h"

/*这个三个是必须的头文件*/
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"


/*simple sleep*/
static int sleep_c (lua_State *L){
    long secs = lua_tointeger(L, -1); /*获取参数*/
    sleep(secs);
    return 0;                         /*返回0个值，所以为0*/
}

static const struct luaL_Reg libs[] = {
    {"sleep", sleep_c},
    {NULL, NULL}  /*the end*/
};

int luaopen_orangleliu (lua_State *L){   
    /*注册lib， 上面luaopen_名称 跟下面注册的名称要一致, 还要和编译的.so文件名一致*/
    luaL_register(L, "orangleliu", libs);  
    return 1; 
}

