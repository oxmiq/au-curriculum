# Day 7 · Meet the GPU

> **Concept of the day:** GPU anatomy. SMs, Tensor Cores, CUDA Cores, HBM, L2 cache. Analogy: SM = factory floor, Tensor Core = specialized machine, HBM = warehouse.
> **Pre-reading:** Pre-Lecture Reading **Reader 5 — Computer architecture primer** (~10 min) + H100 1-page spec.
> **Source:** [Pre-Lecture Reading § Reader 5](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Pre_Lecture_Reading.md) · [Study Guide Ch 3 + §A.3](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

Every optimization in Weeks 3–5 — KV cache layout, FlashAttention, tensor parallelism, batching — is a response to the *physical* GPU. You can't reason about the optimization without the hardware.

## Readiness check

1. What does "80 GB HBM3" mean?
2. SRAM vs DRAM — which is fast/small, which is slow/big? Which is HBM?
3. Roughly: PCIe vs NVLink vs InfiniBand — fastest to slowest?
4. What's the difference between a CPU core and a CUDA core?
5. What is a Tensor Core *for*?

## Core concept — GPU anatomy

### The H100 SXM5 in one table

| Component | What it is | H100 numbers |
|---|---|---|
| **SM (Streaming Multiprocessor)** | A "factory floor" — the unit of work scheduling | 132 SMs |
| **CUDA Core** | General-purpose ALU within an SM | 16,896 total |
| **Tensor Core** | Specialized matrix-multiply unit (the workhorse for AI) | 528 total |
| **Register file** | Per-thread scratch (sub-ns) | KBs per SM |
| **L1 / Shared memory** | Per-SM SRAM (~1 ns) | ~256 KB per SM |
| **L2 cache** | Chip-wide SRAM (~5 ns) | 50 MB |
| **HBM3** | Off-chip "warehouse" DRAM (~80 ns, but very wide) | 80 GB @ 3.35 TB/s |
| **NVLink** | GPU↔GPU interconnect | 900 GB/s |
| **PCIe** | CPU↔GPU | ~64 GB/s |

### The mental model

> **SM = factory floor. Tensor Core = specialized machine on the floor. HBM = warehouse across the road. L2 = on-site storage. Registers = workbench.**

You produce more by:
- (a) putting more machines on each floor (more Tensor Cores per SM),
- (b) keeping the workbench full (locality, kernel fusion),
- (c) **not running back to the warehouse on every move** (bandwidth-bound = "you're stuck walking to the warehouse").

### Compute throughput (FP16 / TF / Tensor-Core dense math)

- **H100 SXM5:** ~989 TFLOPs FP16 (dense, with Tensor Cores).
- For comparison: consumer RTX 4090 ≈ 165 TFLOPs FP16 — but only **24 GB GDDR6X** and only **1 TB/s** bandwidth.

### Three GPU classes to remember

| Class | Example | Memory | Bandwidth | Where you see it |
|---|---|---|---|---|
| Datacenter flagship | H100 SXM5 | 80 GB HBM3 | 3.35 TB/s | Large model serving |
| Consumer / workstation | RTX 4090 | 24 GB GDDR6X | 1 TB/s | Prototyping, ≤13B serving |
| Next-gen / accelerator | Tenstorrent Wormhole n150 | 12 GB GDDR6 | ~0.27 TB/s | Cost-effective MoE, ARM hosts |

## Practice (90 min)

1. (15 min) Label a blank GPU diagram (facilitator will hand one out) — SMs, Tensor Cores, L2, HBM, NVLink ports.
2. (25 min) Match specs to models. Given a stripped table of (memory, bandwidth, TFLOPs), identify which row is H100 / 4090 / B200 / Wormhole n150. Justify each match.
3. (25 min) Estimate: how long would it take to move all 80 GB of H100 weights from HBM into the chip *once*? (80 GB ÷ 3.35 TB/s.) Now estimate the same for a 4090 (24 GB ÷ 1 TB/s). Why do these numbers matter for decode latency?
4. (15 min) Pair discussion: why is a 4090 cheaper per FLOP than an H100, yet datacenters still buy H100s? (Bandwidth, capacity, NVLink, reliability, ECC.)
5. (10 min) Write one open question for Friday's teach-back.

## Wrap-up

Each pair quotes one H100 number from memory. The two facts everyone leaves with: **80 GB HBM3 · 3.35 TB/s.**

## Connect forward

Tomorrow: why those bandwidth numbers — not the TFLOPs — usually decide how fast your model goes.

---

## Pre-read for tomorrow (Day 8 · Memory Is the Bottleneck)

- **Resource:** "Why bandwidth matters more than compute" — Pre-Lecture Reading **Reader 5 (memory hierarchy section)** + Study Guide §A.3 memory-hierarchy subsection (~20 min).
- **Reflection questions:**
  1. Which is faster: L2 cache or HBM? By roughly how much?
  2. What is **temporal locality**? **Spatial locality**?
  3. Why does **kernel fusion** make things faster, given that the math is the same?
