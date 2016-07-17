#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lua.h"
#include "lauxlib.h"

#define MAX_COLOR 255

struct ColorTable {
    char *name;
    unsigned char red, green, blue;
} colortable [] = {
    {"WHITE", MAX_COLOR, MAX_COLOR, MAX_COLOR},
    {"RED",   MAX_COLOR, 0, 0},
    {"GREEN", 0, MAX_COLOR, 0},
    {"BLUE", 0, 0, MAX_COLOR},
    {"NULL", 0, 0, 0}
};

int getfield(lua_State *L, const char *key){
    int result;
    //lua_pushstring(L, key);
    //lua_gettable(L, -2); //-2 is table, get key's value, push stack 
    lua_getfield(L, -1, key);

    if(!lua_isnumber(L, -1)){
        printf("key is not number\n");
    }
    result = (int)lua_tonumber(L, -1) * MAX_COLOR;
    lua_pop(L, 1);
    return result;
}

void setfield(lua_State *L, const char *index, int value){
    //lua_pushstring(L, index);
    //lua_pushnumber(L, (double)value/MAX_COLOR);
    //lua_settable(L, -3);

    lua_pushnumber(L, (double)value/MAX_COLOR);
    lua_setfield(L, -2, index);
}

void setcolor(lua_State *L, struct ColorTable *ct){
    lua_newtable(L);
    setfield(L, "r", ct->red);
    setfield(L, "g", ct->green);
    setfield(L, "b", ct->blue);
    lua_setglobal(L, ct->name);
}

//C API 最主要的就是理解 lua state stack 的工作方式
int main(void){
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);

    //load文件
    //luaL_dofile(L, "hello.lua");
    luaL_loadfile(L, "hello.lua");
    //lua_pcall(L, 0, 0, 0);

    int i = 0;
    int red;
    int green;
    int blue;

    while(colortable[i].name != NULL){
        setcolor(L, &colortable[i++]);
    }

    luaL_dofile(L, "hello.lua");

    // 获取table的值
    lua_getglobal(L, "background");
    lua_getglobal(L, "GREEN");

    if (lua_isnil(L, -2)){
        printf("GREEN is nill");  
    }

    if (lua_isnil(L, -1)){
        printf("background is nil\n");
        exit(1);
    }

    if(lua_isstring(L, -1)){
        const char *colorname = lua_tostring(L, -1);
        int j;
        for(j=0; colortable[j].name !=NULL; j++){
           if(strcmp(colorname, colortable[j].name) == 0){
                break;
           } 
        }

        if(colortable[j].name == NULL){
            printf("invaild color name (%s)", colorname);
        }else{
            red = colortable[j].red;
            green = colortable[j].green;
            blue = colortable[j].blue;
        }
    }else if(lua_istable(L, -1)){
        red = getfield(L, "r");
        green = getfield(L, "g");
        blue = getfield(L, "b"); 
    }else{
        printf("invalid value");
    }
    
    printf("red %d green %d blue %d\n", red, green, blue);

    //释放state
    lua_close(L);
    return 0;
}
