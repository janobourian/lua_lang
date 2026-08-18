# Module 03: Tables, Sequences, Queues & Graph Data Structures
**Domain:** Tables, Array/Hash Part, Sequences, table Library, Queues, Sets & Graphs
**Target Level:** Intermediate Systems Developer
**Status:** ✅ Completed

---

## 1. High-Level Overview
In Lua, the **Table** is the sole associative data structuring mechanism. Internally, tables combine an optimized continuous **Array Part** for integer keys ($1 \dots N$) and a **Hash Part** utilizing Robin Hood hashing for arbitrary string and object keys.

This module explores advanced data structure implementation in pure Lua: **Double-Ended Queues (Deques)**, **Mathematical Sets**, **Sparse Matrices**, and **Directed Graphs**.

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)
* **Business Purpose**: Enables developers to organize complex business software, customer records, and product catalogues using an ultra-flexible, high-speed data structuring engine.
* **How It Works**: Uses versatile data containers (tables) that automatically optimize themselves into fast hardware arrays for numbers and indexing tables for words.
* **Key Business Value & Use Cases**: Reduces development time through simple data modeling, eliminates boilerplate code, and ensures maximum memory efficiency for data-heavy applications.

---

## 2. Hands-On Walkthrough: High-Performance Double-Ended Queue (Deque)
### Step 1: Implement Deque in Pure Lua
```lua
local List = {}

function List.new()
    return { first = 0, last = -1 }
end

function List.push_first(list, value)
    local first = list.first - 1
    list.first = first
    list[first] = value
end

function List.push_last(list, value)
    local last = list.last + 1
    list.last = last
    list[last] = value
end

function List.pop_first(list)
    local first = list.first
    if first > list.last then error("List is empty") end
    local value = list[first]
    list[first] = nil -- Allow garbage collection
    list.first = first + 1
    return value
end

function List.pop_last(list)
    local last = list.last
    if list.first > last then error("List is empty") end
    local value = list[last]
    list[last] = nil -- Allow garbage collection
    list.last = last - 1
    return value
end
```

---

## 4. Pure CLI Commands
### 1. Test Deque Execution
```bash
lua deque_test.lua
```

---

## References

### Official Documentation
* [Lua 5.4 Reference Manual: Tables and Sequences](https://www.lua.org/manual/5.4/manual.html#3.4.9) - Table constructors.
* [Programming in Lua: Chapter 14 (Data Structures)](https://www.lua.org/pil/14.html) - Queues, sets, and graphs.
* [Lua Table Library Reference](https://www.lua.org/manual/5.4/manual.html#6.6) - `table.insert`, `table.remove`, `table.concat`.
* [The Implementation of Lua 5.0 (Table Hash/Array Paper)](https://www.lua.org/doc/jucs05.pdf) - Internal memory mechanics.
* [SEI CERT: Safe Table Key Handling in Dynamic Scripting](https://wiki.sei.cmu.edu/) - Safe table indexing.

### Authoritative Web Pages, Blogs & Tutorials
* [Eli Bendersky: Data Structures in Lua](https://eli.thegreenplace.net/) - Graph algorithms and deques.
* [Cloudflare Engineering: Table Optimization and Memory Management](https://blog.cloudflare.com/) - Preventing table re-hashes.
* [OpenResty Guide: High-Performance Lua Tables](https://openresty.org/) - Array pre-allocation patterns.
* [Datadog Engineering: Profiling Lua Table Allocations](https://www.datadoghq.com/blog/) - Memory leak detection.
* [FinOps Foundation: Table Memory Footprint Optimization](https://www.finops.org/) - Container rightsizing.

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
