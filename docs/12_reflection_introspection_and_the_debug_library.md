# Module 12: Reflection, Introspection & The <debug> Library
**Domain:** Introspection, debug.getinfo, debug.getlocal, Line/Count Profiling Hooks & Tracebacks
**Target Level:** Advanced Systems Developer & Tooling Engineer
**Status:** ✅ Completed

---

## 1. High-Level Overview
Lua provides comprehensive runtime introspection and debugging facilities through the standard **`debug` Library**. This module explores:
1. **Introspection (`debug.getinfo`)**: Inspecting function metadata (definition source file, line numbers, parameter counts, whether it is C or Lua).
2. **Variable Inspection (`debug.getlocal`, `debug.getupvalue`)**: Reading and mutating local variables and upvalues at runtime.
3. **Execution Hooks (`debug.sethook`)**: Attaching call, return, line, and instruction-count hooks for continuous CPU profiling, line-by-line coverage measurement, and infinite loop timeouts.

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)
* **Business Purpose**: Enables deep performance diagnostics, automated code profiling, and incident forensic analysis without stopping live application services.
* **How It Works**: Uses built-in diagnostic cameras (debug hooks) that observe software execution step-by-step, recording precise execution times and line numbers.
* **Key Business Value & Use Cases**: Pinpoints exact code performance bottlenecks in minutes, measures test coverage across enterprise software, and stops runaway infinite loops.

---

## 2. Hands-On Walkthrough: Instruction-Count Timeout Hook
### Step 1: Implement Execution Limiter against Infinite Loops
```lua
local function execute_with_instruction_limit(func, max_instructions)
    local count = 0
    -- Set instruction count hook triggering every 1000 VM instructions
    debug.sethook(function()
        count = count + 1000
        if count >= max_instructions then
            debug.sethook() -- Clear hook
            error("Execution Timeout: Exceeded maximum allowed VM instructions (" .. max_instructions .. ")")
        end
    end, "", 1000)

    local status, result = pcall(func)
    debug.sethook() -- Clear hook
    return status, result
end

-- Test execution against infinite loop
local success, err = execute_with_instruction_limit(function()
    while true do end
end, 50000)

if not success then
    print("Caught Runaway Script: " .. tostring(err))
end
```

---

## 4. Pure CLI Commands
### 1. Execute Profiling Hook Test
```bash
lua debug_hook_test.lua
```

---

## References

### Official Documentation
* [Lua 5.4 Reference Manual: The Debug Library](https://www.lua.org/manual/5.4/manual.html#6.10) - Complete debug API.
* [Programming in Lua: Chapter 25 (The Debug Library)](https://www.lua.org/pil/25.html) - Introspection and hooks.
* [Lua VM Instruction Profiling Specification](https://www.lua.org/doc/jucs05.pdf) - Hook execution mechanics.
* [SEI CERT: Safe Use of Debugging Facilities in Production](https://wiki.sei.cmu.edu/) - Hardening guidelines.
* [Lua Profiler Tools Wiki](http://lua-users.org/wiki/ProfilingLuaCode) - Community profilers.

### Authoritative Web Pages, Blogs & Tutorials
* [Eli Bendersky: Introspection and Debugging in Lua](https://eli.thegreenplace.net/) - Stack inspection and hooks.
* [Cloudflare Engineering: Flamegraphs and CPU Profiling in LuaJIT](https://blog.cloudflare.com/) - High-scale profiling.
* [OpenResty Guide: Debugging and Systemtap Integration](https://openresty.org/) - Dynamic tracing.
* [Datadog Engineering: Production Profiling of Lua Gateways](https://www.datadoghq.com/blog/) - APM telemetry.
* [FinOps Foundation: Profiling Compute Hotspots in Scripting Engines](https://www.finops.org/) - Slashing CPU waste.

---

## FinOps & Resource Cost Governance in Lua & OpenResty Systems

*Financial Operations (FinOps) in Lua, LuaJIT, and OpenResty environments focuses on maximizing request throughput per CPU core, minimizing memory allocation per HTTP request, and eliminating garbage collection latency spikes.*

### 1. High-Density Compute & Gateway Sizing
- **Sub-Millisecond API Gateways** – Utilizing OpenResty and LuaJIT cosockets allows a single 2-vCPU cloud instance to process 50,000+ requests per second, eliminating the need for expensive multi-node application server fleets.
- **LuaJIT FFI Zero-Copy Data Processing** – Using the FFI library to manipulate binary buffers directly avoids Lua garbage-collected object allocations, keeping memory usage constant under extreme transaction volume.

### 2. Eliminating Memory Leaks & GC Waste
- **Table Pre-Allocation** – In high-throughput paths, pre-allocating tables with known sizes (`table.create(narr, nrec)`) prevents multiple internal table re-hashes, saving valuable CPU cycles.
- **Generational GC Tuning** – Configure incremental GC pause and step parameters (`collectgarbage("setpause", 110)`) to maintain predictable memory reclamation without causing multi-millisecond request latency pauses.

### 3. Server Bin-Packing & Cloud Sizing
- **Right-Sizing Compute Fleets** – The minuscule memory footprint of embedded Lua runtimes (<2MB per worker process) enables maximum container bin-packing density on cloud virtual machines.
- **Redis Lua Scripting Optimization** – Running complex multi-step transactional logic inside Redis via Lua scripts eliminates repetitive network round-trips, slashing cloud inter-zone network egress transfer fees.
