#ifndef __LUA_DEV_DUMP_H__
#define __LUA_DEV_DUMP_H__

#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
#define DUMP(L) dump(L, __FILE__, __LINE__);
static void dump(lua_State *L, const char *file, int line) {
	int i;
	int top = lua_gettop(L);
	printf("%s %d\t", file, line);
	for (i = 1; i <= top; i++) {
		int t = lua_type(L, i);
		switch(t) {
		case LUA_TSTRING: 			printf("string:%s\t", lua_tostring(L, i)); break;
		case LUA_TBOOLEAN: 			printf("bool:%d\t", lua_toboolean(L, i)); break;
		case LUA_TNUMBER: 			printf("number:%g\t", lua_tonumber(L, i)); break; 
		case LUA_TNIL: 				printf("nil\t"); break;
		case LUA_TLIGHTUSERDATA: 	printf("luser\t"); break;
		case LUA_TTABLE: 			printf("table\t"); break; 
		case LUA_TFUNCTION: 		printf("func\t"); break;
		case LUA_TUSERDATA: 		printf("user\t"); break;
		case LUA_TTHREAD: 			printf("thread\t"); break; 
		default: 					printf("error:%s\t", lua_typename(L, i)); break; 
		}
	}
	printf("\n");
}

#define PFENV(L) pt(L, __FILE__, __LINE__)
static void pt(lua_State *L, const char *file, int line) {
	printf("trans table %s %d\n", file, line);
	lua_pushnil(L);
	while (lua_next(L, -2)) {
		printf("%g:%s\n", lua_tonumber(L, -2), lua_typename(L, lua_type(L, -1)));
		lua_pop(L, 1);
	}
}

#endif 
