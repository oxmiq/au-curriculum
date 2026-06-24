# Day 9 · Compute-Bound vs Memory-Bound

> **Concept of the day:** ops:byte ratio. The roofline model. Which ceiling you're hitting. **Punchline: prefill = compute. Decode = memory.**<br>
> **Pre-reading:** Pre-Lecture Reading **Reader 4 (complexity, memory, attention math)** + Study Guide §A.5 roofline subsection (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 — The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 9 · Compute-Bound vs Memory-Bound</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-02/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts: Roofline Model | 25 min |
| Part 3 | Deep Dive: Ridge Points | 15 min |
| Part 4 | Deep Dive: Where Kernels Sit | 20 min |
| Part 5 | Hands-On: Calculate | 25 min |
| 7 | Wrap-up & Connection | 15 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: Pre-Lecture Reading **Reader 4 (complexity, memory, attention math)** + Study Guide §A.5 roofline subsection (~15 min).

### Quick Self-Check

Answer these questions from memory:
1. If a kernel does 100 ops and reads 50 bytes, what's its intensity?
2. Why is prefill compute-bound and decode memory-bound? (One sentence.)
3. What does the *roofline model* tell you that arithmetic intensity alone doesn't?

---

## Part 2 — Core Concepts — Roofline Model · 25 min
### Reading — Why the Roofline Matters

Knowing *which ceiling* a workload hits tells you *which knob to turn*: more FLOPs (bigger / better Tensor Cores)? more bandwidth (HBM3e, NVLink)? more parallelism? You can't optimize what you can't classify.

### The Roofline Model

The roofline is a single plot that tells you the **maximum achievable performance** for a given workload on given hardware.

```
performance (FLOP/s)
   ▲
   │           ╭───── compute ceiling (peak TFLOPs)
   │          ╱
   │         ╱
   │        ╱
   │       ╱
   │      ╱       ← BW × intensity slope
   │     ╱
   │    ╱
   │   ╱
   ├──┴─────────────────────► arithmetic intensity (ops/byte)
       ridge point
       (peak FLOPs ÷ BW)
```

### How to Use the Roofline

For each kernel:

1. **Plot it horizontally** at its intensity (ops/byte)
2. **Plot it vertically** at its measured FLOP/s
3. The line above it is the ceiling:
   - Left of ridge: bandwidth-slope
   - Right of ridge: compute-ceiling

---

## Part 3 — Deep Dive — Ridge Points · 15 min
### Reading — Ridge Point Examples

### Ridge Point Formula

> **Ridge Point = Peak FLOPs ÷ Bandwidth**

### Examples (FP16)

| Hardware | Peak FLOPs | BW | Ridge ≈ |
|---|---|---|---|
| H100 SXM5 | 989 TFLOPs | 3.35 TB/s | ~295 ops/byte |
| RTX 4090 | 165 TFLOPs | 1 TB/s | ~165 ops/byte |
| Wormhole n150 | ~74 TFLOPs | ~270 GB/s | ~274 ops/byte |

### Key Insight

- **Above the ridge:** You're compute-bound (hitting the Tensor Cores)
- **Below the ridge:** You're memory-bound (hitting the HBM bandwidth)

---

## Part 4 — Deep Dive — Where Kernels Sit · 20 min
### Reading — Common Workloads

| Kernel | Intensity (rough) | Verdict |
|---|---|---|
| GEMM, large square | ~N (thousands) | **Compute-bound** |
| Prefill attention (long input) | ~hundreds | **Compute-bound** |
| Decode attention (one token) | ~2–10 | **Memory-bound** |
| Decode MLP (one token, one user) | ~2 | **Memory-bound** |
| Elementwise add / scale | ~0.5 | **Bandwidth-bound** |
| All-reduce across nodes | ~0 | **Network-bound** |

### The Punchline

> **Prefill = compute-bound.** All input tokens are processed in parallel → big GEMMs → intensity is high → you're hitting the Tensor Cores.
>
> **Decode = memory-bound.** One token at a time → you re-read all weights per token → intensity is tiny → you're hitting the HBM ceiling.

### Why This Matters — Every Week 3-4 Trick

| Trick | Why It Helps |
|-------|--------------|
| **KV cache** | Don't re-compute past keys/values, just read them |
| **FlashAttention** | Fuse attention into one pass, minimize HBM reads |
| **Quantization** | Fewer bits per weight = less data to move = decode goes faster |
| **Continuous batching** | Pack many users' decodes so weights are re-used across them |
| **Speculative decoding** | Convert decode (memory-bound, 1 token) into a small prefill (compute-bound, K tokens) |

---

## Part 5 — Hands-On — Calculate · 25 min
### Exercise 1: Arithmetic Intensity (10 min)

Calculate arithmetic intensity for:

**(a) `y = a*x + b` over 1M elements**
- FLOPs: 2 ops per element × 1M = 2M FLOPs
- Bytes: 3 arrays × 1M × 2 bytes (FP16) = 6 MB
- Intensity: 2M / 6M = ~0.33 ops/byte

**(b) Matrix multiply 4096×4096 by 4096×4096 in FP16**
- FLOPs: 2N³ = 2 × 4096³ = ~137B FLOPs
- Bytes: 3N² × 2 = ~100 MB
- Intensity: ~1,371,000 ops/byte

### Exercise 2: Tensor Core Utilization (15 min)

At intensity = 2 ops/byte (decode), what fraction of H100's peak compute can you actually use?

**Calculation:**
- Ridge = ~295 ops/byte
- Your intensity = 2 ops/byte
- Fraction = 2 / 295 ≈ **0.68%**

**Answer:** Only ~0.7% of the Tensor Cores are being used! The other 99.3% are idle, waiting for data.

**Implication:** This explains why batching exists — if you pack multiple decodes together, you reuse weights and increase your effective intensity.

---

## Part 7 — Wrap-up & Connection · 15 min
### Self-Check

Can you explain these from memory?
- [ ] What's the roofline model?
- [ ] What's the ridge point for H100? (~295 ops/byte)
- [ ] Where does prefill sit on the roofline? Where does decode sit?
- [ ] Why is decode only using ~0.7% of Tensor Cores?
- [ ] Name two tricks that attack the memory bottleneck

### Connect Forward

Friday: consolidation — Feynman teach-back across the four concepts (pipeline, GPU anatomy, memory hierarchy, roofline). Then the canonical [quiz](knowledge-check.html).

---

## Pre-read for Friday (Day 10 · Consolidation)

- **Resource:** None. Re-read your Day 6–9 notes. Bring your roofline plot.
- **Reflection questions:**
  1. Which of the four Week 2 days felt least clear?
  2. If you had to teach one of {pipeline, anatomy, bandwidth, roofline} to a peer in 5 minutes — which would you pick? Why?
  3. Write one question you want answered before Week 3.

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
