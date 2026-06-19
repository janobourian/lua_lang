#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

static int maxine_hello(lua_State *L) {
    const char *name = luaL_checkstring(L, 1);
    lua_pushfstring(L, "Hello, %s!", name);
    return 1; // Number of return values
}

static const struct luaL_Reg myfuncs[] = {
    {"hello", maxine_hello},
    {NULL, NULL} // Sentinel
};

int luaopen_maxine(lua_State *L) {
    luaL_newlib(L, myfuncs);
    return 1; // Number of return values
}