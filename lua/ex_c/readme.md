C API 调用lua
=============

> C 和lua交互主要是用lua API中提供的栈, 理解这部分原理是写好lua c交互的关键。lua版本是5.1，这部分知识在 `lua编程语言第二版` 中有比较详细讲解。

lauxlib.h 中定义了 `luaL_`开通的一些方法，包含了lua的标准库，是lua内部api的更高级封装。



## API lua5.1

```
void lua_pushnil     (lua_State *L);
void lua_pushboolean (lua_State *L, int bool);
void lua_pushnumber  (lua_State *L, lua_Number n);
void lua_pushinteger (lua_State *L, lua_Integer n);
void lua_pushlstring (lua_State *L, const char *s, size_t len);
void lua_pushstring  (lua_State *L, const char *s);
```

取栈值并转化为C type

```
int lua_checkstack (lua_State *L, int sz); 检查栈的大小
int lua_is* (lua_State *L, int index);  检查元素是否能转化为某个类型
int         lua_toboolean (lua_State *L, int index);
lua_Number  lua_tonumber  (lua_State *L, int index);
lua_Integer lua_tointeger (lua_State *L, int index);
const char *lua_tolstring (lua_State *L, int index, size_t *len); 自动补0
size_t      lua_objlen    (lua_State *L, int index); 类似 ＃tablename
```

stack操作

```
int  lua_gettop    (lua_State *L);  返回栈有多少元素，top元素的index
void lua_settop    (lua_State *L, int index); 设置top value为某个值，加nil或者丢弃到某个index。 index为0，清空栈
void lua_pushvalue (lua_State *L, int index); 把index对应的元素压栈
void lua_remove  (lua_State *L, int index);
void lua_insert  (lua_State *L, int index); 移动top元素到某index
void lua_replace (lua_State *L, int index); pop top元素到某index，没发生移动
```


载入和处理

```
luaL_loadfile(L, "settings.lua") || lua_pcall(L, 0, 0, 0)
int t = lua_type(L, i); char *typename=lua_typename(L, t)
```

## stack

stack 的增长方式 1 -> 2 -> 3, 负数的方式 ..-3 -> -2 -> -1
lua对栈本身提供了非常多的直接操作，也提供了一些状态函数，例如创建table这种。

## 执行流程

1. `lua_State *L = luaL_newstate()` 新建一个state
2. `luaL_openlibs(L)` 载入标准库
3. 可选 `luaL_dofile(L, "xx.lua")` 执行lua文件，类似于shell中执行 `lua xx.lua` 一般情况不执行这个操作。 而是初始化一些变量给lua脚本，或者是调用lua脚本中的某些固定的函数来完成逻辑。


## userdata 是什么



阅读资料

* http://www.troubleshooters.com/codecorn/lua/lua_c_calls_lua.htm
* https://www.youtube.com/watch?v=ZysdYWuPwJU lua c api的视频
* http://www.ewald-arnold.de/lua/lua-apiref.pdf  lua C API的一个查询手册
* https://www.lua.org/manual/5.1/manual.html#3  lua5.1的文档
