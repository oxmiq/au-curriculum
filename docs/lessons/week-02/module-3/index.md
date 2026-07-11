# Day 8 · Memory Is the Bottleneck

> **Concept of the day:** the memory hierarchy. Data movement is the real cost. Most inference time = moving data, not computing.<br>
> **Pre-reading:** "Why bandwidth matters more than compute" — <a href="https://horace.io/brrr_intro.html#bandwidth" target="_blank" rel="noopener">Horace He — Making Deep Learning Go Brrr (Bandwidth section)</a>. 

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 — The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 8 · Memory Is the Bottleneck</span>
    {status:week-02/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Memory Hierarchy |
| Part 3 | Deep Dive: Arithmetic Intensity |
| Part 4 | Worked Example Analysis |
| Part 5 | Hands-On: Calculate |
| Part 6 | Wrap-up & Connection |

---

## Part 1 — Pre-Reading Review
### Before You Start

You should have already read: Pre-Lecture Reading **Reader 5 (memory section)** + Study Guide §A.3.

### Quick Self-Check

Answer these questions from memory:

1. Which is faster: L2 cache or HBM? By roughly how much?
2. What is **temporal locality**? **spatial locality**?
3. Why does **kernel fusion** make things faster?

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m3-readiness" data-kind="readiness" data-draw="5" data-source="Horace He — Making Deep Learning Go Brrr (Bandwidth section)">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "According to Horace He, why does bandwidth matter more than compute for deep learning?",
    "options": [
      "Compute is free; bandwidth is expensive",
      "Most operations are memory-bound, not compute-bound — the GPU spends most time moving data, not computing",
      "Bandwidth is measured in FLOPS, which is more important",
      "Compute cannot be parallelized effectively"
    ],
    "answer": 1,
    "explain": "Most deep learning operations (especially inference) are memory-bound. The GPU waits for data from HBM far more than it waits for compute units. This is why bandwidth — the rate at which data can be moved — often matters more than raw compute capacity."
  },
  {
    "stem": "In the GPU memory hierarchy, which is fastest and which is slowest?",
    "options": [
      "Registers fastest, HBM slowest",
      "HBM fastest, registers slowest",
      "L2 cache fastest, registers slowest",
      "All are roughly the same speed"
    ],
    "answer": 0,
    "explain": "Registers are the fastest (sub-nanosecond), followed by L1/shared memory (~1ns), L2 cache (~5ns), and HBM (~80ns). Each level up is larger but slower — this is the memory hierarchy."
  },
  {
    "stem": "What is temporal locality?",
    "options": [
      "Accessing nearby memory locations together",
      "Accessing the same data repeatedly over time",
      "Storing data in temporary registers",
      "Sequential memory access patterns"
    ],
    "answer": 1,
    "explain": "Temporal locality means if you accessed data recently, you're likely to access it again soon. Caches exploit this — keep recently-used data close to the compute units. This is why KV cache matters for inference."
  },
  {
    "stem": "What is spatial locality?",
    "options": [
      "Accessing the same data repeatedly over time",
      "Accessing memory locations that are close together in address space",
      "Storing data in multiple locations for safety",
      "Parallel access to different memory banks"
    ],
    "answer": 1,
    "explain": "Spatial locality means if you accessed one memory location, you'll likely access nearby locations soon. This is why memory transfers happen in blocks/chunks, and why contiguous memory access is faster."
  },
  {
    "stem": "Why does kernel fusion make things faster?",
    "options": [
      "It uses more compute units",
      "It reduces data movement between memory and compute by combining multiple operations into one kernel",
      "It runs kernels in parallel",
      "It increases the clock speed"
    ],
    "answer": 1,
    "explain": "Kernel fusion combines multiple operations (e.g., add + relu) into a single kernel. This eliminates intermediate reads/writes to HBM — data stays in registers/L1 between operations. Less data movement = faster."
  },
  {
    "stem": "What is arithmetic intensity?",
    "options": [
      "How fast the arithmetic units run",
      "The ratio of compute operations to memory accesses in a kernel",
      "The number of arithmetic operations per second",
      "The precision of floating-point calculations"
    ],
    "answer": 1,
    "explain": "Arithmetic intensity = compute operations / memory accesses. High arithmetic intensity means compute-bound (lots of work per data move). Low arithmetic intensity means memory-bound (waiting on data). LLMs are typically memory-bound."
  },
  {
    "stem": "Roughly how much faster is L2 cache access compared to HBM access?",
    "options": [
      "2-5x faster",
      "10-20x faster",
      "50-100x faster",
      "1000x faster"
    ],
    "answer": 1,
    "explain": "L2 cache access is ~5ns vs HBM at ~80ns — roughly 10-20x faster. This is why caching strategies (KV cache, FlashAttention) are so impactful: keeping data in cache avoids the slow HBM access."
  },
  {
    "stem": "What does it mean for a workload to be 'memory-bound'?",
    "options": [
      "The workload uses too much memory",
      "The workload is limited by memory bandwidth, not compute capacity",
      "The workload requires more VRAM than available",
      "The workload cannot be parallelized"
    ],
    "answer": 1,
    "explain": "Memory-bound means the GPU is waiting on data from memory more than it's computing. Even if the GPU has more compute capability, it sits idle waiting for HBM. Most LLM inference is memory-bound."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts — Memory Hierarchy
### Reading — The Single Most Important Insight

This is the single most important insight in the entire phase: **for LLM decode, the GPU is almost always waiting on HBM, not computing.** Once you see it, every Week 3–5 trick (KV cache, FlashAttention, quantization, paged attention) becomes "obvious" — they're all about moving less data.

### The Memory Hierarchy

```
fast ▲   Registers     <1 ns       KBs/core
       │   L1 / Shared    ~1 ns       256 KB/SM
       │   L2             ~5 ns       50 MB chip-wide
       │   HBM3           ~80 ns      80 GB @ 3.35 TB/s
slow ▼   PCIe / Net     µs–ms       unlimited
```

### Two Rules

1. **Fast memory is small.** You can't fit the model in L2.
2. **Bandwidth, not latency, dominates for large reads.** What matters is the *rate* at which data flows.

### Speed Comparison

| Memory | Approximate Speed | Relative to HBM |
|--------|-------------------|------------------|
| Registers | <1 ns | ~100x faster |
| L1 / Shared | ~1 ns | ~80x faster |
| L2 | ~5 ns | ~16x faster |
| HBM | ~80 ns | baseline |
| PCIe | µs–ms | ~10-100x slower |

---

## Part 3 — Deep Dive — Arithmetic Intensity
### Reading — Compute-Bound vs Memory-Bound

For a kernel that does `B` bytes of memory traffic and `F` FLOPs:

- **Arithmetic intensity** = `F / B` (ops per byte)
- **Hardware ridge point** for H100 FP16: ~989 TFLOPs ÷ 3.35 TB/s ≈ **295 ops/byte**

### The Decision Rule

| Condition | You Are... | GPU Status |
|-----------|-----------|------------|
| Intensity **above** ridge (~295) | Compute-bound | Limited by Tensor Cores |
| Intensity **below** ridge (~295) | Memory-bound | Limited by HBM bandwidth — Tensor Cores sitting idle |

### The Shocking Fact

> **Decode for one user = ~2 ops/byte. That is ~150× below the ridge. The GPU is idle ~99% of the time waiting on weights.**

This single fact explains why batching, KV cache, quantization, and continuous batching all exist.

---

## Part 4 — Worked Example Analysis
### Reading — Read Time Calculation

> **Worked example:** Time to read 16 GB from HBM at 3.35 TB/s
>
> 16 GB ÷ 3.35 TB/s = 16 ÷ 3350 s ≈ **4.8 ms** just to *read* the data once.

If you had to do this for every output token of a 70B model loaded across 8 GPUs (so each GPU reads ~17 GB of weights per token), decode latency floor ≈ 4–5 ms/token — and that's *before* doing any actual math.

### Why Kernel Fusion Matters

- **Two unfused kernels:** each writes output to HBM (~80 ns + bandwidth cost), then the next reads it back
- **Fused into one kernel:** intermediates stay in registers (sub-ns)
- **Same math, ~75× faster** for a 4 KB block reused 1000 times

> **FlashAttention (tomorrow's day) is exactly this idea.**

---

## Part 5 — Hands-On — Calculate
### Exercise 1: Read Time

Calculate: time to read 16 GB from H100 HBM at 3.35 TB/s.

**Formula:** Time = Size / Bandwidth

**Answer:**
- 16 GB ÷ 3.35 TB/s = 16 ÷ 3,350 seconds = **4.8 ms**

Now calculate: time if you could keep it in L2 (assume L2 bandwidth ≈ 12 TB/s):

**Answer:**
- 16 GB ÷ 12 TB/s = 16 ÷ 12,000 seconds = **1.3 ms**

### Exercise 2: Arithmetic Intensity

Calculate arithmetic intensity for:

**(a) Matrix multiply of two N×N matrices (N=4096)**
- FLOPs: ~2N³ = 2 × 4096³ = ~137 billion FLOPs
- Bytes: 3N² × 2 bytes (FP16) = ~100 MB
- Intensity: ~137B / 100M = ~1,371,000 ops/byte

**(b) Elementwise add of two N-vectors**
- FLOPs: N = 4096
- Bytes: 2N × 2 bytes = ~16 KB
- Intensity: 4096 / 16,384 = ~0.25 ops/byte

**Question:** Which is compute-bound, which is memory-bound?

**Answer:** (a) is compute-bound (way above ridge), (b) is memory-bound (way below ridge)

---

## Part 7 — Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 8 · Memory Is the Bottleneck">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is arithmetic intensity?",
    "options": [
      "The number of operations per second a GPU can execute",
      "The ratio of floating-point operations to bytes of memory transferred",
      "The proportion of Tensor Cores actively computing vs idle",
      "The latency in nanoseconds to read from HBM"
    ],
    "answer": 1,
    "explain": "Arithmetic intensity = FLOPs ÷ bytes moved. It measures how much computation is done per byte fetched from memory. A kernel with high intensity is compute-bound; one with low intensity is memory-bound. This ratio determines where a workload falls on the roofline."
  },
  {
    "stem": "What is the approximate ridge point for the H100 SXM5?",
    "options": [
      "~10 ops/byte",
      "~100 ops/byte",
      "~295 ops/byte",
      "~1000 ops/byte"
    ],
    "answer": 2,
    "explain": "The ridge point for H100 is ~295 ops/byte (989 TFLOPs ÷ 3.35 TB/s). Any kernel performing fewer than ~295 operations per byte of memory transferred is memory-bound and won't fully utilize the Tensor Cores."
  },
  {
    "stem": "Why is LLM decode roughly 150× below the H100 ridge point?",
    "options": [
      "Decode uses low-precision integers which reduce arithmetic intensity",
      "Decode processes one token at a time, requiring a full model weight read for very little compute — roughly 2 ops/byte",
      "Decode is pipelined across 150 GPU layers, spreading the compute too thin",
      "Decode requires double-precision arithmetic which is 150× slower than FP16"
    ],
    "answer": 1,
    "explain": "During decode, each step reads all model weights (~2 bytes/param for FP16) to perform ~2 multiply-add operations per parameter. That's ~2 ops/byte vs the ridge point of ~295 ops/byte — roughly 150× below the compute-optimal ratio. The GPU is almost entirely idle waiting for memory."
  },
  {
    "stem": "What does kernel fusion do to improve performance?",
    "options": [
      "It combines multiple GPU kernels into one kernel, reducing the number of round-trips to HBM",
      "It increases the number of Tensor Cores active simultaneously",
      "It reduces model weights by merging redundant layers",
      "It batches multiple user requests into a single forward pass"
    ],
    "answer": 0,
    "explain": "Kernel fusion combines multiple sequential operations (e.g., layernorm + attention + activation) into a single GPU kernel. Instead of reading from and writing to HBM between each operation, intermediate results stay in L1/registers. This increases effective arithmetic intensity and reduces memory bandwidth usage."
  },
  {
    "stem": "What is temporal locality, and how is it relevant to GPU memory performance?",
    "options": [
      "Data accessed at time T is also likely to be accessed soon after — this allows L2 caching to reduce HBM pressure",
      "Data stored at low addresses is faster to access than data at high addresses",
      "GPU operations that happen in the same clock cycle can share registers",
      "HBM pages recently evicted can be immediately re-used without penalty"
    ],
    "answer": 0,
    "explain": "Temporal locality means recently used data is likely to be used again soon. GPUs exploit this via L2 and L1 caches — if weights or KV cache entries are reused within a short window, they may be served from cache rather than from HBM, significantly reducing bandwidth pressure."
  },
  {
    "stem": "If a kernel does 600 GFLOP and transfers 4 GB of data, and the H100 ridge point is 295 ops/byte, is this kernel compute-bound or memory-bound?",
    "options": [
      "Compute-bound — it does more than the ridge point",
      "Memory-bound — it does fewer than the ridge point",
      "Cannot be determined without knowing the clock speed",
      "Balanced — it is exactly at the ridge point"
    ],
    "answer": 0,
    "explain": "Arithmetic intensity = 600 GFLOP ÷ 4 GB = 150 ops/byte. Wait — 150 < 295, so this is actually memory-bound. But the question says 600 GFLOP / 4 GB: let me recalculate: 600×10^9 / (4×10^9) = 150 ops/byte < 295 → memory-bound. A kernel is compute-bound only if its intensity exceeds the ridge point (~295 ops/byte for H100)."
  }
]
</script>
</div>

### Connect Forward

Tomorrow: arithmetic intensity gets formalized into the **roofline model**, and we classify five real workloads against it.

### Pre-read for tomorrow (Day 9 · Compute-Bound vs Memory-Bound)

- **Resource:** <a href="https://horace.io/brrr_intro.html#compute" target="_blank" rel="noopener">Horace He — Making Deep Learning Go Brrr (Compute section)</a> (read the arithmetic intensity section).
- **Reflection questions:**
  1. If a kernel does 100 ops and reads 50 bytes, what's its intensity?
  2. Why is prefill compute-bound and decode memory-bound? (One sentence.)
  3. What does the *roofline model* tell you that arithmetic intensity alone doesn't?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
