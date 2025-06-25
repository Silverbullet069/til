# Lua Cheatsheet

<!-- tl;dr starts -->

It's designed as a simple, lightweight, embeddable glue language for integration between services.

<!-- tl;dr ends -->

```sh
resty -e '
print(type("hello world"))  -- string
print(type(print))          -- function
print(type(true))           -- boolean
print(type(360.0))          -- number
print(type({}))             -- table
print(type(nil))            -- nil
'

# best to do explicit comparison
resty -e '
local a = 0;
if a == false then
  print("true");
end
'

# index start with 1
resty -e "local t={100};print(t[0])"        # no error! that"s dangerous
resty -e "local t={100};print(type(t[0]))"  # nil
resty -e "local t={100};print(type(t[1]))"  # number

# concat string
resty -e "print('hello' .. 'world')"

# one data structure: table
# use equal signs instead of colon like JavaScript
# it's surprisingly confuse, can't believe someone design it
# - key-value pairs are referenced using key name in square bracket
# - scalar elements are references using indexes
# - table length is the total number of scalar elements before encountering the first `nil`
resty -e '
local color = {first = "red", "blue", third = "green", "yellow"}
print(color["first"]);  -- red
print(color[1]);        -- blue
print(color["third"]);  -- green
print(color[2]);        -- yellow
print(type(color[3]));  -- nil
'

# all variables are global by default, placed in a table named _G
# use them requiring expensive operations
# Best practice: use `local` scope when declaring varibles
resty -e 'local s = "hello"'
resty -e 's = "global hello"'

# Dummy variables
resty -e '
local  _, end_pos = string.find("hello", "he")
print(end_pos)'
2
```

- String. Immutable. A modified string is a new string in memory. Use single quotes or double quotes.
- Boolean. Type inference logic: `nil` and `false` => `false`. Everything else is true, even empty string `""` and zero `0`.
- Number. Double-precision floating-point by default. If `dual-number` mode is on, integers will be stored as integers and floating-point numbers will be stored as double-precision floating-point numbers.
- Function. First-class citizens.
- Table. Similar to JavaScript objects. Lua index starts with 1.
- Null. `nil`. Define a var but do not assign a value.

Order of priority when learning Lua libraries:

```
OpenResty's API > LuaJIT's library functions > Standard Lua's functions
```

- String library: `string.*`
- Table library: `table.*`
- Math library: `math.*`
- Dummy variable: specify underscore `_` as name (now I know where Python dummy variable' convention is from)

**LuaJIT:** a high-performance runtime environment consists of 3 components:

- Lua AOT Compiler source-to-bytecode.
- Lua interpreter, a.k.a LuaJIT VM, implemented in assembly.
- Lua JIT Compiler, compiles frequently interpreted bytecode into native machien code during runtime.

> Similar mechanism to Java and CPython (>=v3.13).

It integrates with FFI (Foreign Function Interface), allowing Lua to:

- Invoke external C functions from C standard libraries, Nginx and OpenSSL C modules, ...
- Use C data structures.

Through two new `table.new` and `table.clear` API, you can achieve performance optimization.

```sh
resty -e '
local ffi = require("ffi");
ffi.cdef[[
int printf(const char *fmt, ...);
]]
ffi.C.printf("Hello %s\n", "world");
'
```
