# Module 12: Lua Reflection, Introspection, debug Library & CPU Profiling

**Track:** Lua Systems Architecture, LuaJIT Internals & OpenResty Ecosystem
**Category:** Introspection Engine, debug.getinfo, Upvalue Inspection, Execution Hooks & Profiling
**Standard Identifier:** `DOC-STD-UNIVERSAL-2026`
**Status:** ✅ Completed

---

## 📑 Table of Contents

1. [High-Level Overview & Executive Summary](#1-high-level-overview--executive-summary)
2. [Runtime Introspection: debug.getinfo & Stack Activation Frames](#2-runtime-introspection-debuggetinfo--stack-activation-frames)
3. [Variable Reflection: Local Variables (getlocal) & Upvalues (getupvalue)](#3-variable-reflection-local-variables-getlocal--upvalues-getupvalue)
4. [Execution Hooks (debug.sethook): Call, Return, Line & Count Modes](#4-execution-hooks-debugsethook-call-return-line--count-modes)
5. [Tracebacks, Error Formatting & Forensic Stack Dumps](#5-tracebacks-error-formatting--forensic-stack-dumps)
6. [Building a Production CPU Call-Graph & Coverage Profiler](#6-building-a-production-cpu-call-graph--coverage-profiler)
7. [Certification & Engineering Essentials (Lua / OpenResty Cheat Sheet)](#7-certification--engineering-essentials-lua--openresty-cheat-sheet)
8. [Comparative Analysis Matrix: Profiling Approaches in Dynamic Runtimes](#8-comparative-analysis-matrix-profiling-approaches-in-dynamic-runtimes)
9. [Performance & Hardware Resource Optimization](#9-performance--hardware-resource-optimization)
10. [Step-by-Step Production Lab: Enterprise Deterministic CPU Call Profiler](#10-step-by-step-production-lab-enterprise-deterministic-cpu-call-profiler)
11. [Pure CLI / Command Interface](#11-pure-cli--command-interface)
12. [Advanced Architecture & Edge-Case Failure Modes](#12-advanced-architecture--edge-case-failure-modes)
13. [Detailed Sub-Components & Subsystems](#13-detailed-sub-components--subsystems)
14. [References (The 5+5 Rule)](#14-references-the-55-rule)
15. [Universal FinOps & Hardware Cost Governance](#15-universal-finops--hardware-cost-governance)

---

## 1. High-Level Overview & Executive Summary

In mission-critical enterprise systems, understanding exactly what is executing inside the virtual machine—measuring function execution times, tracking code coverage, generating detailed forensic stack dumps during crashes, and enforcing CPU instruction quotas—is powered by Lua's **`<debug>` Standard Library**.

Unlike static compiled languages where debugging symbols are stripped from release binaries, the Lua VM retains rich debug metadata:

1. **Introspection (`debug.getinfo`)**: Traverses the active activation records on the C/Lua call stack, querying source filenames, line numbers, function types (`"Lua"` vs `"C"`), parameter counts, and active line tables.
2. **Variable Reflection (`debug.getlocal`, `debug.getupvalue`)**: Inspects and mutates local variables and captured lexical closures dynamically at runtime.
3. **Execution Hooks (`debug.sethook`)**: Attaches non-intrusive event listeners triggered on function calls (`"c"`), function returns (`"r"`), source line transitions (`"l"`), or every $N$ VM bytecode instructions (`count`).

Mastering the debug subsystem allows systems architects to build **Deterministic CPU Call Profilers**, **Line-by-Line Test Coverage Tools**, and **Forensic Incident Triage Handlers**.

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│               LUA ACTIVATION FRAME STACK & INTROSPECTION TOPOLOGY              │
├────────────────────────────────────────────────────────────────────────────────┤
│ [Active Execution Point: `debug.getinfo(level)`]                              │
│         │                                                                      │
│         ├── Level 0: `debug.getinfo` function itself                           │
│         ├── Level 1: Calling function (`process_order()`)                      │
│         ├── Level 2: Caller's caller (`dispatch_request()`)                    │
│         └── Level 3: Master Event Loop (`nginx_worker_main()`)                 │
│                                                                                │
│ ┌────────────────────────────────────────────────────────────────────────────┐ │
│ │ ACTIVATION RECORD METADATA RETURNED BY `debug.getinfo(1, "nSlf")`:         │ │
│ │ ├── `name`            ──► "process_order"                                  │ │
│ │ ├── `namewhat`        ──► "method" / "field"                               │ │
│ │ ├── `source`          ──► "@/app/services/orders.lua"                      │ │
│ │ ├── `currentline`     ──► 142                                              │ │
│ │ ├── `what`            ──► "Lua" (or "C" for native bindings)               │ │
│ │ ├── `nparams`         ──► 2 (Explicit parameters)                          │ │
│ │ ├── `nups`            ──► 4 (Captured Upvalues)                            │ │
│ │ └── `func`            ──► Function Object Reference                        │ │
│ └────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────┘
```

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)

* **Business Purpose**: Enables automated code profiling, performance bottleneck detection, and crash forensics to keep enterprise cloud services fast and stable.
* **How It Works**: Operates like an internal diagnostic camera that monitors code execution line-by-line, recording exact execution durations and call hierarchies.
* **Key Business Value & ROI**: Pinpoints slow code sections in minutes instead of days, ensures 100% test coverage compliance, and captures detailed post-mortem crash dumps for instant bug resolution.

---

## 2. Runtime Introspection: debug.getinfo & Stack Activation Frames

$$\text{Syntax: } \mathbf{info = debug.getinfo(level\_or\_func, what\_options)}$$

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│                     DEBUGINFO QUERY OPTION FLAGS TABLE                        │
├───────────────────┬────────────────────────────────────────────────────────────┤
│ Option Character  │ Populated Metadata Fields in Info Table                    │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"s"`**         │ `source`, `short_src`, `what`, `linedefined`, `lastline`   │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"l"`**         │ `currentline` (Active executing line on stack)             │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"u"`**         │ `nups` (Upvalue count), `nparams`, `isvararg`              │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"n"`**         │ `name` (Function name if deduced), `namewhat`              │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"f"`**         │ `func` (Pushes actual function object onto table)          │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"L"`**         │ `activelines` (Table of valid executable source lines)     │
└───────────────────┴────────────────────────────────────────────────────────────┘
```

---

## 3. Variable Reflection: Local Variables (getlocal) & Upvalues (getupvalue)

```lua
-- 1. Inspect Local Variables on Stack Level 1
local function inspect_locals()
    local idx = 1
    while true do
        local name, val = debug.getlocal(2, idx)
        if not name then break end
        print(string.format("Local [%d]: %s = %s", idx, name, tostring(val)))
        idx = idx + 1
    end
end

-- 2. Inspect Captured Upvalues on Function Closure
local function inspect_upvalues(func)
    local idx = 1
    while true do
        local name, val = debug.getupvalue(func, idx)
        if not name then break end
        print(string.format("Upvalue [%d]: %s = %s", idx, name, tostring(val)))
        idx = idx + 1
    end
end
```

---

## 4. Execution Hooks (debug.sethook): Call, Return, Line & Count Modes

$$\text{Syntax: } \mathbf{debug.sethook([thread], hook\_function, mask\_string, [count])}$$

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│                     DEBUG HOOK EVENT MASK SPECIFICATION                        │
├───────────────────┬────────────────────────────────────────────────────────────┤
│ Hook Mask         │ Event Trigger Condition                                    │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"c"`**         │ **Call Hook**: Triggered whenever a function is called.    │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"r"`**         │ **Return Hook**: Triggered whenever a function returns.    │
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`"l"`**         │ **Line Hook**: Triggered before executing a new source line│
├───────────────────┼────────────────────────────────────────────────────────────┤
│ **`count`**       │ **Instruction Count Hook**: Triggered every $N$ opcodes.   │
└───────────────────┴────────────────────────────────────────────────────────────┘
```

---

## 5. Tracebacks, Error Formatting & Forensic Stack Dumps

When an unhandled error occurs, **`debug.traceback`** formats the entire call stack into a readable post-mortem diagnostic report:

```lua
local function safe_run(func)
    local ok, result = xpcall(func, function(err)
        return debug.traceback("FATAL CRASH: " .. tostring(err), 2)
    end)
    return ok, result
end
```

---

## 6. Building a Production CPU Call-Graph & Coverage Profiler

By combining call (`"c"`) and return (`"r"`) hooks with `os.clock()`, a deterministic profiler tracks total calls and self-time for every function:

```lua
local profile_data = {}

local function profiler_hook(event)
    local info = debug.getinfo(2, "nS")
    local fn_name = info.name or (info.short_src .. ":" .. info.linedefined)
    if event == "call" then
        local record = profile_data[fn_name] or { calls = 0, start = os.clock(), total_time = 0 }
        record.calls = record.calls + 1
        record.start = os.clock()
        profile_data[fn_name] = record
    elseif event == "return" and profile_data[fn_name] then
        local record = profile_data[fn_name]
        record.total_time = record.total_time + (os.clock() - record.start)
    end
end
```

---

## 7. Certification & Engineering Essentials (Lua / OpenResty Cheat Sheet)

* ⚠️ **Production Performance Rule**: **NEVER leave `debug.sethook` active in production request workers!** Line and call hooks disable JIT compilation in LuaJIT and slow down execution by $5\times$ to $20\times$.
* 🔒 **Security Sandboxing Rule**: Strip the entire `debug` library from untrusted user execution sandboxes.
* ⚙️ **Stack Level 1 vs 2**: In helper diagnostic functions, inspect level 2 (`debug.getinfo(2)`) to capture the actual caller rather than the helper itself.
* ⚠️ **LuaJIT FFI & Hooks**: In LuaJIT, compiled JIT traces do not trigger standard Lua debug hooks unless compiled with specific debug flags.

---

## 8. Comparative Analysis Matrix: Profiling Approaches in Dynamic Runtimes

| Dimension | Lua debug.sethook | Linux Perf / SystemTap | FlameGraphs (eBPF) |
| :--- | :--- | :--- | :--- |
| **Intrusiveness** | High (Interpreted Hook) | **Zero (Sampling)** | **Zero (Kernel eBPF)** |
| **Accuracy** | 100% Deterministic Count | Statistical Sample | Statistical Sample |
| **JIT Compatibility** | Disables LuaJIT Traces | **Profiles Native JIT** | **Profiles Native JIT** |
| **Use Case** | Unit Test Coverage / CI | Production Profiling | Production Fleet APM |

---

## 9. Performance & Hardware Resource Optimization

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│                         DEBUG TUNING PLAYBOOK                                  │
├────────────────────────────────────────────────────────────────────────────────┤
│ 1. Pass minimal query strings to `debug.getinfo` (e.g. `"Sl"` instead of `"nSl│
│ 2. Use `debug.sethook()` strictly during testing, profiling, or sandbox quota. │
│ 3. Always clear debug hooks with `debug.sethook()` in `finally` cleanup logic. │
│ 4. Capture stack traces using `xpcall(func, debug.traceback)`.                 │
│ 5. Use eBPF / SystemTap for production profiling without touching VM hooks.   │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Step-by-Step Production Lab: Enterprise Deterministic CPU Call Profiler

### File Structure

* [`src/cpu_profiler.lua`](file:///Users/frgonzal/Documents/maxine/lua_lang/src/cpu_profiler.lua)

### Step 1: Implement Call-Graph Profiler with Table Reporting

```lua
-- src/cpu_profiler.lua
local debug         = debug
local os_clock      = os.clock
local string_format = string.format
local table_sort    = table.sort
local pairs         = pairs
local print         = print

local CpuProfiler = {}
CpuProfiler.__index = CpuProfiler

function CpuProfiler.new()
    local self = setmetatable({}, CpuProfiler)
    self.records = {}
    self.call_stack = {}
    return self
end

function CpuProfiler:start()
    self.records = {}
    self.call_stack = {}

    debug.sethook(function(event)
        local info = debug.getinfo(2, "nS")
        if not info then return end

        local fn_id = (info.name or "anonymous") .. "@" .. info.short_src .. ":" .. (info.linedefined or 0)
        local now = os_clock()

        if event == "call" then
            local entry = { fn_id = fn_id, start_time = now }
            self.call_stack[#self.call_stack + 1] = entry

            local record = self.records[fn_id] or { fn_id = fn_id, call_count = 0, total_time = 0 }
            record.call_count = record.call_count + 1
            self.records[fn_id] = record
        elseif event == "return" then
            if #self.call_stack > 0 then
                local last = self.call_stack[#self.call_stack]
                self.call_stack[#self.call_stack] = nil
                local elapsed = now - last.start_time
                local record = self.records[last.fn_id]
                if record then
                    record.total_time = record.total_time + elapsed
                end
            end
        end
    end, "cr")
end

function CpuProfiler:stop()
    debug.sethook() -- Clear hook!
end

function CpuProfiler:print_report()
    self:stop()
    local report_list = {}
    for _, record in pairs(self.records) do
        report_list[#report_list + 1] = record
    end

    table_sort(report_list, function(a, b) return a.call_count > b.call_count end)

    print("\n========================= CPU PROFILER REPORT =========================")
    print(string_format("%-45s | %-10s | %-12s", "Function Target", "Calls", "Total Secs"))
    print("------------------------------------------------------------------------")
    for i = 1, #report_list do
        local r = report_list[i]
        print(string_format("%-45s | %-10d | %-12.6f", r.fn_id, r.call_count, r.total_time))
    end
    print("========================================================================\n")
end

-- Verification Workload
local function calculate_fibonacci(n)
    if n <= 1 then return n end
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
end

local function fast_loop()
    local s = 0
    for i = 1, 10000 do s = s + i end
    return s
end

local profiler = CpuProfiler.new()
print("Starting Profiler...")
profiler:start()

calculate_fibonacci(15)
fast_loop()
fast_loop()

profiler:print_report()
print("CPU Profiler Lab Completed Successfully!")
```

---

## 11. Pure CLI / Command Interface

### 1. Execute CPU Profiler Script

Run profiler suite:

```bash
lua src/cpu_profiler.lua
```

### 2. Verify Stack Traceback Formatting via CLI

Inspect formatted traceback output:

```bash
lua -e 'local function a() error("TEST TRACEBACK") end; xpcall(a, function(err) print(debug.traceback(err, 2)) end)'
```

### 3. Inspect Local Variable Extraction via getlocal

Verify variable introspection:

```bash
lua -e 'local function f() local secret = "TOP_SECRET"; local n, v = debug.getlocal(1, 1); print("Captured:", n, v) end; f()'
```

---

## 12. Advanced Architecture & Edge-Case Failure Modes

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│                        DEBUG FAILURE RECOVERY MATRIX                           │
├──────────────────────┬────────────────────────┬────────────────────────────────┤
│ Failure Scenario     │ Underlying Root Cause  │ Production Mitigation Runbook  │
├──────────────────────┼────────────────────────┼────────────────────────────────┤
│ **`Massive Prod CPU`**| Left `debug.sethook`   │ Ensure hooks are strictly      │
│ **`Slowdown (5x-20x)`**| active in production. │ disabled in production configs.│
├──────────────────────┼────────────────────────┼────────────────────────────────┤
│ **`Security Escape`**| Exposed `debug` library│ Strip `debug` completely from  │
│ **`in Multi-Tenant`**| inside user sandbox.   │ tenant `_ENV` environments.    │
├──────────────────────┼────────────────────────┼────────────────────────────────┤
│ **`LuaJIT Profiler`**| JIT compiled traces    │ Use eBPF sampling profilers    │
│ **`Blind Spot`**     │ bypassed Lua hooks.    │ (SystemTap/FlameGraphs).       │
├──────────────────────┼────────────────────────┼────────────────────────────────┤
│ **`Stack Overflow on`| Recursive traceback    │ Pass max level limit to        │
│ **`Deep Traceback`** │ formatting in error.   │ `debug.traceback(msg, level)`. │
└──────────────────────┴────────────────────────┴────────────────────────────────┘
```

---

## 13. Detailed Sub-Components & Subsystems

### 1. Lua Virtual Machine Debug Hook Engine (`luaD_hook`)

* **Key Concepts**: Internal C dispatcher invoking registered hook function when bytecode instructions or call events match mask.
* **CLI / Tool Snippet**:

```bash
lua -e 'debug.sethook(function(e) print("Event:", e) end, "c"); local function f() end; f(); debug.sethook()'
```

### 2. Stack Frame Activation Record Scanner (`lua_getinfo`)

* **Key Concepts**: Traverses CallInfo (`CI`) linked list on the execution stack to extract symbol names and line numbers.
* **CLI / Tool Snippet**:

```bash
lua -e 'print(debug.getinfo(1, "S").short_src)'
```

### 3. Upvalue Introspection Bridge (`lua_getupvalue`)

* **Key Concepts**: Accesses closure `UpVal` array by 1-based index, returning variable name and value.
* **CLI / Tool Snippet**:

```bash
lua -e 'local x=10; local f=function() return x end; print(debug.getupvalue(f, 1))'
```

### 4. Traceback String Formatter (`luaL_traceback`)

* **Key Concepts**: Formats stack frames into human-readable call stacks with source files and line numbers.
* **CLI / Tool Snippet**:

```bash
lua -e 'print(debug.traceback())'
```

---

## 14. References (The 5+5 Rule)

### Official Documentation & Academic Specifications

1. [Lua 5.4 Reference Manual: Section 6.10 The Debug Library](https://www.lua.org/manual/5.4/manual.html#6.10)
2. [Programming in Lua: Chapter 25 (The Debug Library)](https://www.lua.org/pil/25.html)
3. [Lua VM Introspection and Hooking Mechanics](https://www.lua.org/doc/jucs05.pdf)
4. [SEI CERT: Safe Use of Debugging and Introspection in Production](https://wiki.sei.cmu.edu/)
5. [Lua 5.4 C API: lua_getinfo and lua_sethook](https://www.lua.org/manual/5.4/manual.html#lua_getinfo)

### Authoritative Engineering Textbooks & Systems Deep Dives

1. [Roberto Ierusalimschy: Programming in Lua (4th Edition, Part IV: The Standard Libraries)](https://www.lua.org/pil/)
2. [Eli Bendersky: Introspection, Hooks and Profiling in Lua](https://eli.thegreenplace.net/)
3. [Cloudflare Engineering: Profiling High-Throughput LuaJIT Gateways with FlameGraphs](https://blog.cloudflare.com/)
4. [Datadog Engineering: Real-Time APM Tracing in Embedded Scripting Runtimes](https://www.datadoghq.com/blog/)
5. [High-Performance Linux Systems: Low-Overhead Sampling Profilers vs VM Hooks](https://www.kernel.org/)

---

## 15. Universal FinOps & Hardware Cost Governance

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│                         DEBUG FINOPS SAVINGS MATRIX                            │
├──────────────────────────┬──────────────────────────┬──────────────────────────┤
│ Optimization Strategy    │ Technical Mechanism      │ Measurable FinOps ROI    │
├──────────────────────────┼──────────────────────────┼──────────────────────────┤
│ **Selective `"Sl"` Query**| Queries only needed info │ Slashes `getinfo` CPU    │
│                          │ fields from stack frames │ overhead by 65%          │
├──────────────────────────┼──────────────────────────┼──────────────────────────┤
│ **Zero Hooks in Prod**   │ Guarantees LuaJIT trace  │ Prevents 5x compute fleet│
│                          │ compilation stays active │ over-provisioning spend  │
├──────────────────────────┼──────────────────────────┼──────────────────────────┤
│ **Automated Coverage**   │ Line hooks measure test  │ Prevents multi-million-  │
│                          │ coverage in CI pipelines │ dollar production outages│
├──────────────────────────┼──────────────────────────┼──────────────────────────┤
│ **Structured Tracebacks**│ Captures full forensic   │ Cuts Mean-Time-To-Repair │
│                          │ context on error panics  │ (MTTR) by 75%            │
└──────────────────────────┴──────────────────────────┴──────────────────────────┘
```

### 1. Removing Debug Hooks from Production Gateways Economics

In an API gateway cluster processing 100,000 requests per second:

* **Accidentally Leaving Debug Hooks Active**: Disables LuaJIT trace compilation, forcing the runtime into slow interpreted mode ($20\text{ cloud servers required} \times \$450/\text{month} = \mathbf{\$9,000/\text{month}}$).
* **Disabling Debug Hooks & Enabling LuaJIT Trace Compilation**: Restores native hardware JIT execution speed.
* Required server fleet drops from 20 to **4 cloud servers** ($4 \times \$450 = \mathbf{\$1,800/\text{month}}$).
* **FinOps ROI**: Delivers **\$7,200/month (\$86,400/year) in direct cloud compute infrastructure savings**.

### 2. Forensic Traceback MTTR Engineering ROI

* Vague error messages (`"attempt to index nil"`) require hours of developer log-trawling to reproduce.
* Structured `debug.traceback` capture identifies the exact file, function, line number, and stack frame parameters instantly.
* **FinOps ROI**: Reduces developer troubleshooting time by **75%**, saving hundreds of engineering hours annually.
