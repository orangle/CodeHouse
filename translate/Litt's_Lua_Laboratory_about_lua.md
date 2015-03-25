写个简单的Lua拓展-sleep函数
=======================

> 这几天在做一个小项目，其中用到了一些基本的API, 例如sleep，获取当前目录等等，lua标准库中没有提供这些接口，虽然所第三方库中也都有实现，但是要用的就那么几个函数，在一个嵌入式系统中安装那么多第三方库有点浪费资源，于是**@胜利哥** 写了一个socket的C实现，然后给我用。我试着把其他几个函数也用C实现，首先看下怎么用C写lua的拓展。

### C 部分
> 首先是根据Lua C语言的协议写好调用模块，编译成.so 文件，然后才可以在lua脚本中调用。 下面是在**Ubuntu14.04 **系统中，基于**lua5.1** 写的一个sleep实现。

####**sleep.c 文件 **

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

####编译

    $ gcc -fPIC -shared -llua sleep.c -o orangleliu.so -I/usr/include/lua5.1 -std=gnu99

### lua 调用

#### **test.lua**

    require "orangleliu"
    print(os.time())
    orangleliu.sleep(1)
    print(os.time())

#### 调用结果

    $ lua test.lua
    1427118862
    1427118863

### 小结

基本的模板就是这样的，复杂一些就是多个参数和多个返回值。 如果有C基础，写起来还是挺快的，不过要是跨平台处理起来也挺麻烦的。
大家可以在github上搜下别人写的lua拓展库，参考下。

### 参考
+ [Programming in Lua](http://www.lua.org/pil/26.1.html)
+ [Calling a C Function From Lua](http://www.troubleshooters.com/codecorn/lua/lua_lua_calls_c.htm#_Make_an_msleep_Function)













