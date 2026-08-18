# Mission-Critical Lua & OpenResty Encyclopedia — Master Index
**Repository:** `maxine/lua_lang`
**Domain:** Dynamic Embeddable Scripting, High-Throughput API Gateways & LuaJIT Internals
**Target Level:** Zero to Enterprise Mission-Critical Lead Architect
**Status:** ✅ Complete 19-Module Production-Grade Encyclopedia

---

## 📚 Complete Encyclopedia Module Index (From Zero to Master)

| Module | Core Topics & Hands-On Scope | Target Level | Document Link |
| :--- | :--- | :--- | :--- |
| **00. Foundations & Syntax** | Lua 5.1/5.4 syntax, dynamic typing, local variable discipline, 8 fundamental types, control flow | Zero to Beginner | [`00_lua_foundations_syntax_types_and_control_flow.md`](00_lua_foundations_syntax_types_and_control_flow.md) |
| **01. Numbers & Math** | 64-bit integers vs IEEE-754 floats, `math` library, PRNG seed generation, integer division (`//`), bitwise ops | Zero to Beginner | [`01_numbers_integers_and_mathematical_library.md`](01_numbers_integers_and_mathematical_library.md) |
| **02. Strings & Patterns** | String interning, `string` library, pattern matching `%a, %d, %b()`, UTF-8 codepoint iteration (`utf8`) | Intermediate | [`02_strings_pattern_matching_and_unicode_handling.md`](02_strings_pattern_matching_and_unicode_handling.md) |
| **03. Tables & Data Structures** | Dual array/hash representation, sequences (`#t`), deques, sets, sparse matrices, directed graphs | Intermediate | [`03_tables_sequences_and_data_structures.md`](03_tables_sequences_and_data_structures.md) |
| **04. Functions & Closures** | First-class functions, multiple return values, variadics `...`, lexical closures, proper tail call optimization | Intermediate | [`04_functions_closures_upvalues_and_variadics.md`](04_functions_closures_upvalues_and_variadics.md) |
| **05. The External World** | Simple I/O (`io.read/write`), Complete I/O (`io.open`), streaming large files, `os` system facilities | Intermediate | [`05_the_external_world_simple_and_complete_io_model.md`](05_the_external_world_simple_and_complete_io_model.md) |
| **06. Modules & Packages** | `require` caching pipeline, `package.path`, `package.loaded`, multi-file architecture, export lists | Intermediate | [`06_modules_packages_and_large_scale_architecture.md`](06_modules_packages_and_large_scale_architecture.md) |
| **07. Metatables & Overloading** | Metatables, arithmetic/relational metamethods, `__index`, `__newindex`, `__call`, `__tostring`, proxies | Core Language | [`07_metatables_metamethods_and_operator_overloading.md`](07_metatables_metamethods_and_operator_overloading.md) |
| **08. OOP & Inheritance** | Prototype OOP, Single and Multiple Inheritance, privacy via closures and dual representation | Core Language | [`08_object_oriented_programming_inheritance_and_privacy.md`](08_object_oriented_programming_inheritance_and_privacy.md) |
| **09. Environments & Sandboxes** | Global variables, `_ENV` lexical translation, creating impenetrable multi-tenant execution sandboxes | Security Architect | [`09_environments_env_and_security_sandboxing.md`](09_environments_env_and_security_sandboxing.md) |
| **10. Garbage Collection** | Incremental Mark-and-Sweep, Generational GC (5.4), `collectgarbage` tuning, weak tables, `__gc` finalizers | Systems Architect | [`10_garbage_collection_weak_tables_and_finalizers.md`](10_garbage_collection_weak_tables_and_finalizers.md) |
| **11. Coroutines & Multitasking** | First-class asymmetric coroutines (`yield`/`resume`), cooperative multitasking, async event loops, generators | Concurrency | [`11_coroutines_cooperative_multitasking_and_generators.md`](11_coroutines_cooperative_multitasking_and_generators.md) |
| **12. Reflection & Debugging** | Introspection (`debug.getinfo`), local variable access, instruction count timeout hooks, CPU profiling | Tooling Engineer | [`12_reflection_introspection_and_the_debug_library.md`](12_reflection_introspection_and_the_debug_library.md) |
| **13. C-Lua C API Stack** | Virtual stack mechanics, pushing/popping, calling Lua from C, memory allocators, native shared libraries | Systems Integration | [`13_the_c_lua_capi_virtual_stack_and_state_management.md`](13_the_c_lua_capi_virtual_stack_and_state_management.md) |
| **14. Userdata & Memory Binding** | Full userdata vs light userdata, attaching userdata metatables and `__gc` finalizers, C bit array library | Systems Integration | [`14_userdata_lightuserdata_and_c_memory_binding.md`](14_userdata_lightuserdata_and_c_memory_binding.md) |
| **15. LuaJIT Architecture & FFI** | LuaJIT architecture, Tracing JIT compiler, JIT NYI limits, C FFI zero-overhead native struct access and syscalls | High Performance | [`15_luajit_architecture_trace_compiler_and_c_ffi.md`](15_luajit_architecture_trace_compiler_and_c_ffi.md) |
| **16. OpenResty API Gateways** | OpenResty architecture, `lua-nginx-module` execution phases, non-blocking cosockets, JWT auth, API gateways | Distributed Cloud | [`16_enterprise_openresty_cosockets_and_api_gateways.md`](16_enterprise_openresty_cosockets_and_api_gateways.md) |
| **17. Redis Lua & ACID** | Redis server-side Lua execution, ACID transactional execution, distributed sliding-window rate limiters | Distributed Data | [`17_distributed_redis_lua_scripting_and_acid_transactions.md`](17_distributed_redis_lua_scripting_and_acid_transactions.md) |
| **18. Enterprise Projects** | Capstone: OpenResty Edge Gateway, Redis Sliding-Window Rate Limiter & Redlock, LuaJIT FFI Event Engine | Enterprise Lead Master | [`18_real_world_enterprise_case_studies_and_hands_on.md`](18_real_world_enterprise_case_studies_and_hands_on.md) |

---

## 🛠️ Documentation Standards Applied Across All Guides
1. **👔 Executive Summary**: Non-technical explanation of business purpose, mechanics, and value for managers and teammates.
2. **Technical Deep Dives**: Comprehensive architecture explanations, consensus mechanics, and kernel-level primitives.
3. **Hands-On Step-by-Step Walkthroughs**: Reproducible labs for building, scaling, securing, and debugging workloads.
4. **Clean, Escaped CLI Snippets**: Formatted with trailing ` \` line escapes, 4-space indentation, and zero in-code comments.
5. **Trustworthy Curated Sources**: Exactly 5 official documentation links + 5 authoritative engineering blogs per module.
6. **FinOps & Resource Governance**: 500+ word guidelines on compute throughput efficiency and GC tuning.
