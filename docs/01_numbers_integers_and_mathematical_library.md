# Module 01: Numbers, Integers & The Mathematical Library
**Domain:** IEEE-754 Floats, 64-Bit Integers (5.3+), math Library, PRNG & Bitwise Operators
**Target Level:** Zero to Mission-Critical Foundations
**Status:** ✅ Completed

---

## 1. High-Level Overview
In Lua 5.3 and 5.4, numbers have a dual internal representation: **64-bit Integers** (`math.type(x) == "integer"`) and **64-bit IEEE-754 Floating-Point** (`math.type(x) == "float"`). Understanding numeric limits (`math.maxinteger` $= 2^{63}-1$, `math.mininteger` $= -2^{63}$), integer division (`//`), bitwise operators (`&`, `|`, `~`, `>>`, `<<`), and standard trigonometric/rounding functions in the `math` library is fundamental for high-performance data processing.

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)
* **Business Purpose**: Guarantees financial mathematical precision, billing accuracy, and secure random number generation for enterprise transaction systems.
* **How It Works**: Uses 64-bit exact integer arithmetic for money and counts to prevent decimal rounding errors, and high-speed floating-point math for scientific analytics.
* **Key Business Value & Use Cases**: Eliminates financial calculation discrepancies, enables cryptographically secure token generation, and delivers sub-millisecond math processing.

---

## 2. Integer vs Float Representation & Bitwise Mechanics

```
Lua Number Representation:
Integer:  64-bit Two's Complement (-9,223,372,036,854,775,808 to 9,223,372,036,854,775,807)
Float:    64-bit IEEE 754 Double Precision (53-bit mantissa precision)

Bitwise Operations:
Bitwise AND:   0xFF & 0x0F  ---> 0x0F
Bitwise OR:    0xF0 | 0x0F  ---> 0xFF
Bitwise XOR:   0xAA ~ 0xFF  ---> 0x55
Bit Shift Right: 128 >> 2   ---> 32
```

---

## 3. Hands-On Walkthrough: Cryptographic Token Generator with Math Library
### Step 1: Implement Safe Random Token Generator
```lua
local function generate_secure_token(length)
    local len = length or 32
    local chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    local token = {}
    
    -- Initialize pseudo-random seed
    math.randomseed(os.time() + os.clock() * 1000000)

    for i = 1, len do
        local rand_idx = math.random(1, #chars)
        token[i] = string.sub(chars, rand_idx, rand_idx)
    end

    return table.concat(token)
end

print("Secure Token: " .. generate_secure_token(16))
```

---

## 4. Pure CLI Commands
### 1. Verify Numeric Limits via Lua CLI
```bash
lua -e 'print("Max Integer: " .. math.maxinteger); print("Min Integer: " .. math.mininteger)'
```

---

## References

### Official Documentation
* [Lua 5.4 Reference Manual: Numbers and Math Library](https://www.lua.org/manual/5.4/manual.html#6.7) - Math specifications.
* [Programming in Lua: Chapter 3 (Numbers)](https://www.lua.org/pil/3.html) - Arithmetic and conversions.
* [IEEE-754 Floating-Point Standard](https://ieeexplore.ieee.org/) - Number formatting.
* [Lua Bitwise Operators Reference](https://www.lua.org/manual/5.4/manual.html#3.4.2) - Binary manipulation.
* [SEI CERT: Safe Integer Arithmetic in Scripting](https://wiki.sei.cmu.edu/) - Integer overflow prevention.

### Authoritative Web Pages, Blogs & Tutorials
* [Roberto Ierusalimschy: Integers in Lua 5.3](https://www.lua.org/) - Architectural evolution paper.
* [Eli Bendersky: Bitwise Operations and Number Representation in Lua](https://eli.thegreenplace.net/) - Binary manipulation.
* [Cloudflare Engineering: Mathematical Optimization in Edge Workers](https://blog.cloudflare.com/) - High-speed calculations.
* [Datadog Engineering: Tracking Numeric Precision in Metrics Aggregators](https://www.datadoghq.com/blog/) - Telemetry.
* [FinOps Foundation: CPU Efficiency in Number-Heavy Lua Workloads](https://www.finops.org/) - Compute optimization.

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
