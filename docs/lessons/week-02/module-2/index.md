# Day 7 · Meet the GPU

> **Concept of the day:** GPU anatomy. SMs, Tensor Cores, CUDA Cores, HBM, L2 cache. Analogy: SM = factory floor, Tensor Core = specialized machine, HBM = warehouse.<br>
> **Pre-reading:** Pre-Lecture Reading **Reader 5 — Computer architecture primer** (~10 min) + H100 1-page spec.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 — The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 7 · Meet the GPU</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-02/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts: GPU Anatomy | 25 min |
| Part 3 | The Mental Model | 15 min |
| Part 4 | GPU Classes Comparison | 20 min |
| Part 5 | Hands-On: Calculate Bandwidth | 30 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: Pre-Lecture Reading **Reader 5 — Computer architecture primer** (~10 min) + H100 1-page spec.

### Quick Self-Check

Answer these questions from memory:
1. What does "80 GB HBM3" mean? (Memory technology + capacity)
2. What's an SM? What's a Tensor Core?
3. Why is intra-GPU memory faster than GPU-to-GPU?

---

## Part 2 — Core Concepts — GPU Anatomy · 25 min
### Reading — Why GPU Anatomy Matters

Every optimization in Weeks 3–5 — KV cache layout, FlashAttention, tensor parallelism, batching — is a response to the *physical* GPU. You can't reason about the optimization without the hardware.

### The H100 SXM5 In One Table

| Component | What it is | H100 numbers | Speed |
|---|---|---|---|
| **SM (Streaming Multiprocessor)** | A "factory floor" — the unit of work scheduling | 132 SMs | — |
| **CUDA Core** | General-purpose ALU within an SM | 16,896 total | — |
| **Tensor Core** | Specialized matrix-multiply unit (the workhorse for AI) | 528 total | — |
| **Register file** | Per-thread scratch (sub-ns) | KBs per SM | ~0 ns |
| **L1 / Shared memory** | Per-SM SRAM (~1 ns) | ~256 KB per SM | ~1 ns |
| **L2 cache** | Chip-wide SRAM (~5 ns) | 50 MB | ~5 ns |
| **HBM3** | Off-chip "warehouse" DRAM (~80 ns, but very wide) | 80 GB @ 3.35 TB/s | ~80 ns |
| **NVLink** | GPU↔GPU interconnect | 900 GB/s | — |
| **PCIe** | CPU↔GPU | ~64 GB/s | — |

### Key Numbers to Memorize

- **80 GB HBM3** — the memory capacity
- **3.35 TB/s** — the memory bandwidth
- **132 SMs** — the compute units
- **528 Tensor Cores** — the specialized AI accelerators

---

## Part 3 — The Mental Model · 15 min
### Reading — Factory Floor Analogy

> **SM = factory floor. Tensor Core = specialized machine on the floor. HBM = warehouse across the road. L2 = on-site storage. Registers = workbench.**

### How This Analogy Works

| GPU Component | Factory Analogy | Why it Matters |
|---------------|-----------------|----------------|
| SM (Streaming Multiprocessor) | Factory floor | Where work is scheduled |
| Tensor Core | Specialized machine | Does the actual matrix multiplication |
| Register file | Workbench | Ultra-fast, per-thread scratch space |
| L1 / Shared memory | On-site storage | Fast access for frequently-used data |
| L2 cache | Warehouse storage | Larger but slower than L1 |
| HBM (High Bandwidth Memory) | Warehouse across the road | Large capacity but slow to access |

### You Produce More By:

1. **(a)** Putting more machines on each floor (more Tensor Cores per SM)
2. **(b)** Keeping the workbench full (locality, kernel fusion)
3. **(c)** **Not running back to the warehouse on every move** (bandwidth-bound = "you're stuck walking to the warehouse")

---

## Part 4 — GPU Classes Comparison · 20 min
### Reading — Three GPU Classes to Remember

| Class | Example | Memory | Bandwidth | Where You See It |
|---|---|---|---|---|
| Datacenter flagship | H100 SXM5 | 80 GB HBM3 | 3.35 TB/s | Large model serving |
| Consumer / workstation | RTX 4090 | 24 GB GDDR6X | 1 TB/s | Prototyping, ≤13B serving |
| Next-gen / accelerator | Tenstorrent Wormhole n150 | 12 GB GDDR6 | ~0.27 TB/s | Cost-effective MoE, ARM hosts |

### Key Comparison Points

- **H100:** Massive memory (80 GB), massive bandwidth (3.35 TB/s), massive price (~$30K)
- **RTX 4090:** Good compute, limited memory (24 GB), good bandwidth (1 TB/s), consumer price (~$1.6K)
- **Wormhole n150:** Lower cost, lower bandwidth, good for MoE models

### Compute Throughput

- **H100 SXM5:** ~989 TFLOPs FP16 (dense, with Tensor Cores)
- **RTX 4090:** ~165 TFLOPs FP16 — but only **24 GB GDDR6X** and only **1 TB/s** bandwidth

**Key insight:** TFLOPs alone don't tell the whole story. Memory bandwidth often matters more.

---

## Part 5 — Hands-On — Calculate Bandwidth · 30 min
### Exercise 1: Time to Load Weights (15 min)

**Calculate:** How long would it take to move all 80 GB of H100 weights from HBM into the chip *once*?

**Formula:** Time = Size / Bandwidth

**Answer:**
- 80 GB ÷ 3.35 TB/s = 80 GB ÷ 3,350 GB/s = ~0.024 seconds = **24 ms**

**Now calculate for RTX 4090:**
- 24 GB ÷ 1 TB/s = 24 GB ÷ 1,000 GB/s = **24 ms**

**Why do these numbers matter for decode latency?**

Each decode step needs to read the KV cache from HBM. If each step takes ~10 ms and you need 500 tokens, that's 5 seconds just for memory reads!

### Exercise 2: Match GPU Specs (15 min)

Given this stripped table, identify which row is which GPU:

| Memory | Bandwidth | TFLOPs | GPU |
|--------|-----------|--------|-----|
| 80 GB HBM3 | 3.35 TB/s | ~989 | ? |
| 24 GB GDDR6X | 1 TB/s | ~165 | ? |
| 12 GB GDDR6 | 0.27 TB/s | ~100 | ? |

**Answers:** Row 1 = H100, Row 2 = RTX 4090, Row 3 = Wormhole n150

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you explain these from memory?
- [ ] What's the difference between an SM and a Tensor Core?
- [ ] What's the difference between L1, L2, and HBM?
- [ ] What are the two most important H100 numbers? (80 GB, 3.35 TB/s)
- [ ] Why is a 4090 cheaper per FLOP than an H100?

### Connect Forward

Tomorrow: why those bandwidth numbers — not the TFLOPs — usually decide how fast your model goes.

### Pre-read for tomorrow (Day 8 · Memory Is the Bottleneck)

- **Resource:** "Why bandwidth matters more than compute" — Pre-Lecture Reading **Reader 5 (memory hierarchy section)** + Study Guide §A.3 memory-hierarchy subsection (~20 min).
- **Reflection questions:**
  1. Which is faster: L2 cache or HBM? By roughly how much?
  2. What is **temporal locality**? **spatial locality**?
  3. Why does **kernel fusion** make things faster, given that the math is the same?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
