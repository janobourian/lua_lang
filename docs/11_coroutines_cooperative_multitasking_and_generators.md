# Module 11: Coroutines, Cooperative Multitasking & Generators
**Domain:** First-Class Asymmetric Coroutines, coroutine Library, Pipelines & Async Emulation
**Target Level:** Advanced Systems Developer
**Status:** ✅ Completed

---

## 1. High-Level Overview
Lua provides native support for **First-Class Asymmetric Coroutines** (collaborative multitasking threads managed entirely in userspace without OS kernel context switches). Unlike preemptive OS threads that require locking primitives and incur high context-switching overhead, Lua coroutines explicitly yield control via `coroutine.yield()` and resume via `coroutine.resume()`.

Coroutines are the foundational engine behind asynchronous, non-blocking network frameworks like **OpenResty (cosockets)** and game loop state machines, enabling thousands of concurrent client sessions to execute with sequential, readable code syntax.

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)
* **Business Purpose**: Allows a single cloud server to coordinate thousands of customer transactions simultaneously without requiring complex, multi-threaded server architectures.
* **How It Works**: Operates like cooperative relay runners. When an application waits for database data, it politely pauses (yields) and lets other tasks run, resuming automatically when data arrives.
* **Key Business Value & Use Cases**: Delivers ultra-low response times for high-volume customer portals, eliminates multithreading deadlocks, and reduces server CPU overhead by up to 70%.

---

## 2. Coroutine State Machine & Pipeline Mechanics

```
               coroutine.create()
                      |
                      v
                +-----------+
                | Suspended | <-------+
                +-----------+         |
                      |               | coroutine.yield()
      coroutine.resume()              |
                      v               |
                +-----------+         |
                |  Running  | --------+
                +-----------+
                      |
               Function Returns
                      v
                +-----------+
                |   Dead    |
                +-----------+
```

---

## 3. Hands-On Walkthrough: Producer-Consumer Pipeline with Data Filters
### Step 1: Implement Producer-Filter-Consumer Pipeline
```lua
local function producer()
    return coroutine.create(function()
        for i = 1, 5 do
            print("Producer generating data: " .. i)
            coroutine.yield(i)
        end
    end)
end

local function filter(prod_co)
    return coroutine.create(function()
        while true do
            local status, val = coroutine.resume(prod_co)
            if not status or val == nil then break end
            local filtered_val = val * 100 -- Multiply by 100
            coroutine.yield(filtered_val)
        end
    end)
end

local function consumer(filt_co)
    while true do
        local status, val = coroutine.resume(filt_co)
        if not status or val == nil then break end
        print("Consumer received filtered value: " .. val)
    end
end

-- Wire and execute pipeline
local prod = producer()
local filt = filter(prod)
consumer(filt)
```

---

## 4. Pure CLI Commands
### 1. Execute Coroutine Pipeline
```bash
lua pipeline.lua
```

---

## References

### Official Documentation
* [Lua 5.4 Reference Manual: Coroutines](https://www.lua.org/manual/5.4/manual.html#2.6) - Complete coroutine API manual.
* [Programming in Lua: Chapter 24 (Coroutines)](https://www.lua.org/pil/24.html) - Producer-consumer and pipeline patterns.
* [Coroutines in Lua Paper (Moura & Ierusalimschy)](https://www.inf.puc-rio.br/~roberto/docs/coro-revis-2004.pdf) - Formal academic coroutine paper.
* [OpenResty Cosockets API Specification](https://github.com/openresty/lua-nginx-module#ngxsockettcp) - Non-blocking coroutine network sockets.
* [Lua Thread Management API](https://www.lua.org/manual/5.4/manual.html#lua_newthread) - C API coroutine spawning.

### Authoritative Web Pages, Blogs & Tutorials
* [Cloudflare Engineering: How Cosockets and Coroutines Power Global Edge Traffic](https://blog.cloudflare.com/) - Real-world edge networking.
* [Eli Bendersky: Asynchronous Programming and Coroutines in Lua](https://eli.thegreenplace.net/) - Cooperative multi-tasking patterns.
* [OpenResty Official Architecture Guide](https://openresty.org/) - Non-blocking event loop design.
* [Datadog Engineering: Tracking Coroutine Lifecycle in High-Throughput Gateways](https://www.datadoghq.com/blog/) - APM tracing.
* [FinOps Foundation: Reducing CPU Context Switch Waste](https://www.finops.org/) - Cooperative multitasking economics.

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
