# Module 02: Strings, Pattern Matching & UTF-8 Handling
**Domain:** String Interning, string Library, Lua Pattern Matching & <utf8> Library
**Target Level:** Intermediate Systems Developer
**Status:** ✅ Completed

---

## 1. High-Level Overview
In Lua, **Strings** are immutable, garbage-collected sequences of 8-bit bytes. Lua automatically performs **String Interning** (storing a single physical copy of every unique string in a global hash table), making string equality comparisons ($O(1)$ pointer comparisons) near-instantaneous.

Lua features a powerful, lightweight **Pattern Matching Engine** (implemented in `<string.h>` without the heavy memory footprint of full POSIX regular expressions) and native support for Unicode through the **`utf8` Library**.

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)
* **Business Purpose**: Enables fast text searching, email/URL validation, and international character support across customer-facing digital applications.
* **How It Works**: Uses memory-optimized text processing that compares identical words instantly and parses complex structured documents with high-speed pattern recognition.
* **Key Business Value & Use Cases**: Reduces server memory consumption by deduplicating identical customer strings, supports global multi-language text, and processes web URLs in microseconds.

---

## 2. Lua Pattern Matching Classes & Captures

```
Pattern Character Classes:
.   - Any character
%a  - Letters
%d  - Digits
%s  - Whitespace characters
%w  - Alphanumeric characters
%b() - Balanced parenthesis / brackets match
^ / $ - Anchor to start / end of string
```

---

## 3. Hands-On Walkthrough: Production URL Query String Parser
### Step 1: Implement Pattern Matching Parser
```lua
local function parse_url_query(query_str)
    local params = {}
    if not query_str or query_str == "" then return params end

    -- Lua pattern matching for key=value pairs separated by &
    for key, val in string.gmatch(query_str, "([^&=]+)=([^&=]*)") do
        params[key] = val
    end

    return params
end

local url_query = "user_id=1092&tier=enterprise&region=us-east-1&active=true"
local parsed = parse_url_query(url_query)

for k, v in pairs(parsed) do
    print(string.format("Key: %-12s | Value: %s", k, v))
end
```

---

## 4. Pure CLI Commands
### 1. Run Pattern Matching Script
```bash
lua parse_query.lua
```

---

## References

### Official Documentation
* [Lua 5.4 Reference Manual: String Manipulation](https://www.lua.org/manual/5.4/manual.html#6.4) - String library API.
* [Programming in Lua: Chapter 4 & 10 (Strings and Pattern Matching)](https://www.lua.org/pil/4.html) - Pattern matching guide.
* [Lua 5.4 UTF-8 Support Library](https://www.lua.org/manual/5.4/manual.html#6.5) - Unicode codepoints.
* [String Interning Architecture in Lua](https://www.lua.org/doc/jucs05.pdf) - Hash table mechanics.
* [SEI CERT: Safe String Manipulation in Embeddable Scripting](https://wiki.sei.cmu.edu/) - Safe text handling.

### Authoritative Web Pages, Blogs & Tutorials
* [Eli Bendersky: Lua Pattern Matching in Practice](https://eli.thegreenplace.net/) - Real-world patterns.
* [Cloudflare Engineering: Fast String Parsing in Edge Proxies](https://blog.cloudflare.com/) - Sub-millisecond URL parsing.
* [OpenResty Guide: High-Performance String Buffers with table.concat](https://openresty.org/) - Avoiding garbage collection bloat.
* [Datadog Engineering: Profiling String Allocations in Dynamic Runtimes](https://www.datadoghq.com/blog/) - Memory analysis.
* [FinOps Foundation: Slashing String Garbage Collection Overhead](https://www.finops.org/) - Infrastructure efficiency.

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
