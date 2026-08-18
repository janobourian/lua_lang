# Module 09: Environments, _ENV & Security Sandboxing
**Domain:** Global Environment _G, Lexical _ENV (5.2+), Sandboxing & Untrusted Script Isolation
**Target Level:** Advanced Systems Developer & Security Engineer
**Status:** ✅ Completed

---

## 1. High-Level Overview
In Lua 5.2, 5.3, and 5.4, the global variable mechanism was re-architected around **Lexical Environments (`_ENV`)**. Every free name `x` in a chunk is translated by the compiler into `_ENV.x`. By manipulating `_ENV`, developers can isolate untrusted user scripts inside **Secure Execution Sandboxes**, selectively exposing only safe whitelisted functions while blocking dangerous OS and filesystem APIs (`io.*`, `os.execute`, `debug.*`).

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)
* **Business Purpose**: Allows enterprise platforms to execute custom customer code, plugin scripts, and third-party rules safely without risking server compromise or data leaks.
* **How It Works**: Creates an impenetrable digital sandbox around untrusted scripts, granting access only to safe math and text functions while completely blocking access to server files and network commands.
* **Key Business Value & Use Cases**: Enables secure user-extensible SaaS platforms, satisfies strict enterprise multi-tenant cybersecurity requirements, and prevents remote code execution (RCE) attacks.

---

## 2. Lexical `_ENV` Compilation Pipeline

```
Code Written by Developer:
x = 10; print(x)

Code Translated by Lua Compiler:
_ENV.x = 10; _ENV.print(_ENV.x)
```

---

## 3. Hands-On Walkthrough: Creating a Secure Multi-Tenant Script Sandbox
### Step 1: Implement a Hardened Lua Sandbox
```lua
local function run_sandboxed_script(user_code, input_data)
    -- Define strict safe environment whitelist
    local sandbox_env = {
        input = input_data,
        result = nil,
        math = {
            abs = math.abs,
            min = math.min,
            max = math.max,
            sqrt = math.sqrt
        },
        string = {
            format = string.format,
            upper = string.upper,
            lower = string.lower
        },
        ipairs = ipairs,
        pairs = pairs
    }

    -- Load chunk with custom _ENV
    local chunk, err = load(user_code, "user_sandbox", "t", sandbox_env)
    if not chunk then
        return false, "Compilation Error: " .. tostring(err)
    end

    -- Execute in protected mode
    local status, exec_err = pcall(chunk)
    if not status then
        return false, "Runtime Error: " .. tostring(exec_err)
    end

    return true, sandbox_env.result
end

-- Test safe execution
local safe_code = "result = math.max(input.a, input.b) * 10"
local success, res = run_sandboxed_script(safe_code, { a = 12, b = 45 })
print("Sandbox Success! Result: " .. tostring(res))
```

---

## 4. Pure CLI Commands
### 1. Test Sandboxing Execution
```bash
lua sandbox_test.lua
```

---

## References

### Official Documentation
* [Lua 5.4 Reference Manual: Environments and the Global Environment](https://www.lua.org/manual/5.4/manual.html#2.2) - `_ENV` mechanics.
* [Programming in Lua: Chapter 22 (Environments)](https://www.lua.org/pil/22.html) - Canonical environment chapter.
* [Lua Security & Sandboxing Guidelines](https://www.lua.org/security.html) - Official sandboxing documentation.
* [Lua load Function API](https://www.lua.org/manual/5.4/manual.html#pdf-load) - Passing custom environment tables.
* [SEI CERT: Safe Sandbox Design in Multi-Tenant Platforms](https://wiki.sei.cmu.edu/) - Preventing privilege escalation.

### Authoritative Web Pages, Blogs & Tutorials
* [Eli Bendersky: Environments in Lua 5.2 and 5.3](https://eli.thegreenplace.net/) - Detailed `_ENV` tutorial.
* [Cloudflare Engineering: Sandboxing Untrusted Customer Logic](https://blog.cloudflare.com/) - Edge multi-tenancy.
* [OpenResty Guide: Request Isolation and Environments](https://openresty.org/) - Worker-level isolation.
* [Datadog Engineering: Security Auditing of Embedded Lua Engines](https://www.datadoghq.com/blog/) - CVE mitigation.
* [FinOps Foundation: Multi-Tenant Density and Resource Governance](https://www.finops.org/) - Bin-packing secure sandboxes.

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
