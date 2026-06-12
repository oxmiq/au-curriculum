# Day 9 · Compute-Bound vs Memory-Bound

> **Concept of the day:** ops:byte ratio. The roofline model. Which ceiling you're hitting. **Punchline: prefill = compute. Decode = memory.**
> **Pre-reading:** Pre-Lecture Reading **Reader 4 (complexity, memory, attention math)** + Study Guide §A.5 roofline subsection (~15 min).
> **Source:** [Pre-Lecture Reading § Reader 4](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Pre_Lecture_Reading.md) · [Study Guide §A.5](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Problem Sets — Day 9 set](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Problem_Sets.md).

---

## Why this matters

Knowing *which ceiling* a workload hits tells you *which knob to turn*: more FLOPs (bigger / better Tensor Cores)? more bandwidth (HBM3e, NVLink)? more parallelism? You can't optimize what you can't classify.

## Readiness check

1. If a kernel does 100 ops and reads 50 bytes, what's its intensity?
2. What two numbers do you need to compute the roofline ridge for a piece of hardware?
3. Where on the roofline is **prefill** for a typical LLM? Where is **decode**?
4. Name one workload that's bandwidth-bound and one that's compute-bound.
5. What's the difference between "memory-bound" and "latency-bound"?

## Core concept — the roofline model

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
   └──┴─────────────────────► arithmetic intensity (ops/byte)
       ridge point
       (peak FLOPs ÷ BW)
```

For each kernel:

- **Plot it horizontally at its intensity (ops/byte).**
- **Plot it vertically at its measured FLOP/s.**
- The line above it is the ceiling: bandwidth-slope on the left, compute-ceiling on the right.

### Ridge point examples (FP16)

| Hardware | Peak FLOPs | BW | Ridge ≈ |
|---|---|---|---|
| H100 SXM5 | 989 TFLOPs | 3.35 TB/s | ~295 ops/byte |
| RTX 4090 | 165 TFLOPs | 1 TB/s | ~165 ops/byte |
| Wormhole n150 | ~74 TFLOPs | ~270 GB/s | ~274 ops/byte |

### Where common kernels sit

| Kernel | Intensity (rough) | Verdict |
|---|---|---|
| GEMM, large square | ~N (thousands) | **Compute-bound** |
| Prefill attention (long input) | ~hundreds | **Compute-bound** |
| Decode attention (one token) | ~2–10 | **Memory-bound** |
| Decode MLP (one token, one user) | ~2 | **Memory-bound** |
| Elementwise add / scale | ~0.5 | **Bandwidth-bound** |
| All-reduce across nodes | ~0 | **Network-bound** (a different roof) |

### The punchline

> **Prefill = compute-bound.** All input tokens are processed in parallel → big GEMMs → intensity is high → you're hitting the Tensor Cores.
>
> **Decode = memory-bound.** One token at a time → you re-read all weights per token → intensity is tiny → you're hitting the HBM ceiling.

Every Week 3–4 trick is an attack on this:

- **KV cache** — don't re-compute past keys/values, just read them.
- **FlashAttention** — fuse attention into one pass, minimize HBM reads.
- **Quantization** — fewer bits per weight = less data to move = decode goes faster.
- **Continuous batching** — pack many users' decodes so weights are re-used across them (raises intensity).
- **Speculative decoding** — convert decode (memory-bound, 1 token) into a small prefill (compute-bound, K tokens).

## Practice (90 min)

1. (15 min) Compute arithmetic intensity for: (a) `y = a*x + b` over 1M elements; (b) matrix multiply 4096×4096 by 4096×4096 in FP16. Plot on a roofline.
2. (25 min) Classify five workloads (facilitator hands them out). For each: estimate intensity, plot, label compute-bound / memory-bound, propose one optimization.
3. (25 min) Pair calculation: at intensity = 2 ops/byte (decode), what fraction of H100's peak compute can you actually use? *(Answer: ~2/295 ≈ 0.7%. The Tensor Cores are 99.3% idle.)* Discuss what this implies about why batching exists.
4. (15 min) Sketch a roofline for a Wormhole n150. How would the same workloads from Q2 land on it?
5. (10 min) Write a one-sentence "punchline" of your own for prefill vs decode.

## Wrap-up

Pairs share their punchlines. Best one goes on the cohort wall. Friday's quiz tests this classification skill.

## Connect forward

Friday: consolidation — Feynman teach-back across the four concepts (pipeline, GPU anatomy, memory hierarchy, roofline). Then the canonical [quiz](knowledge-check.html).

---

## Pre-read for Friday (Day 10 · Consolidation)

- **Resource:** None. Re-read your Day 6–9 notes. Bring your roofline plot.
- **Reflection questions:**
  1. Which of the four Week 2 days felt least clear?
  2. If you had to teach one of {pipeline, anatomy, bandwidth, roofline} to a peer in 5 minutes — which would you pick? Why?
  3. Write one question you want answered before Week 3.
