# Module 05: The External World, File I/O & System Interfaces
**Domain:** Simple/Complete I/O Models (io Library), File Handles, os Library & Subprocesses
**Target Level:** Intermediate Systems Developer
**Status:** ✅ Completed

---

## 1. High-Level Overview
Interacting with host operating systems requires mastering Lua's I/O subsystems:
1. **The Simple I/O Model**: Global standard input/output streams (`io.input`, `io.output`, `io.read`, `io.write`).
2. **The Complete I/O Model**: Object-oriented file handles (`io.open`, `file:read`, `file:write`, `file:seek`, `file:close`) for explicit streaming and random access.
3. **The `os` Library**: Environment variables (`os.getenv`), system execution (`os.execute`), file deletion/renaming (`os.remove`, `os.rename`), and system clocks (`os.time`, `os.clock`, `os.date`).

### 👔 Executive Summary (For Managers & Non-Technical Stakeholders)
* **Business Purpose**: Connects software applications to server filesystems, operating system commands, and persistent storage disks.
* **How It Works**: Opens, streams, and writes business records to disk files, ensuring that logs and reports are saved safely with zero data loss.
* **Key Business Value & Use Cases**: Enables automated file generation, configuration file loading, and system health reporting for cloud infrastructure.

---

## 2. Complete I/O Stream Architecture

```
File Handle Lifecycle:
io.open("log.txt", "w") ---> File Handle Object: [ File Descriptor + Stream Buffer ]
                                      |
                                      +---> file:write("Log Entry
")
                                      |
                                      +---> file:flush()
                                      |
                                      v
                                file:close() (Releases OS File Descriptor)
```

---

## 3. Hands-On Walkthrough: Streaming Large Log Files with Complete I/O
### Step 1: Implement Line-by-Line File Processing
```lua
local function process_log_file(filepath)
    local f, err = io.open(filepath, "r")
    if not f then
        error("Failed to open file: " .. tostring(err))
    end

    local line_count = 0
    local error_count = 0

    for line in f:lines() do
        line_count = line_count + 1
        if string.find(line, "ERROR") then
            error_count = error_count + 1
        end
    end

    f:close()
    return line_count, error_count
end
```

---

## 4. Pure CLI Commands
### 1. Test File I/O Stream Processing
```bash
lua log_processor.lua
```

---

## References

### Official Documentation
* [Lua 5.4 Reference Manual: Input and Output Facilities](https://www.lua.org/manual/5.4/manual.html#6.8) - io library.
* [Programming in Lua: Chapter 7 (The External World)](https://www.lua.org/pil/7.html) - Complete I/O model.
* [Lua Standard OS Library](https://www.lua.org/manual/5.4/manual.html#6.9) - Operating system facilities.
* [POSIX.1-2017 File Operations](https://pubs.opengroup.org/) - Underlying system calls.
* [SEI CERT: Safe File I/O in Embeddable Scripting](https://wiki.sei.cmu.edu/) - Preventing file leaks.

### Authoritative Web Pages, Blogs & Tutorials
* [Eli Bendersky: File I/O in Lua](https://eli.thegreenplace.net/) - Stream performance.
* [Cloudflare Engineering: Fast Streaming in Edge Runtimes](https://blog.cloudflare.com/) - Non-blocking streaming.
* [OpenResty Guide: File Logging Best Practices](https://openresty.org/) - Async log collection.
* [Datadog Engineering: Monitoring File Descriptor Leaks in Lua](https://www.datadoghq.com/blog/) - Telemetry.
* [FinOps Foundation: Disk I/O Optimization in Containerized Lua](https://www.finops.org/) - Infrastructure efficiency.

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
