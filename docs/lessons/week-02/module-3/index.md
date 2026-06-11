# Day 8 · Memory Is the Bottleneck

> **Concept of the day:** the memory hierarchy. Data movement is the real cost. Most inference time = moving data, not computing.
> **Pre-reading:** "Why bandwidth matters more than compute" — Pre-Lecture Reading **Reader 5 (memory section)** + Study Guide §A.3 (~20 min).
> **Source:** [Pre-Lecture Reading § Reader 5 memory subsection](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Pre_Lecture_Reading.md) · [Study Guide §A.3](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Glossary entries: bandwidth, HBM, L2](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Glossary.md).

---

## Why this matters

This is the single most important insight in the entire phase: **for LLM decode, the GPU is almost always waiting on HBM, not computing.** Once you see it, every Week 3–5 trick (KV cache, FlashAttention, quantization, paged attention) becomes "obvious" — they're all about moving less data.

## Readiness check

1. Which is faster: L2 cache or HBM on an H100? By how much (rough ratio)?
2. What's temporal locality? Spatial locality?
3. If a kernel writes intermediate results to HBM and reads them back, vs. keeping them in registers, why does the second one go faster?
4. What is **arithmetic intensity** (ops per byte)?
5. Name one common workload that's compute-bound and one that's memory-bound.

## Core concept — the memory hierarchy

```
fast ▲   Registers     <1 ns       KBs/core
     │   L1 / Shared    ~1 ns       256 KB/SM
     │   L2             ~5 ns       50 MB chip-wide
     │   HBM3           ~80 ns      80 GB @ 3.35 TB/s
slow ▼   PCIe / Net     µs–ms       unlimited
```

Two rules govern this picture:

- **Fast memory is small.** You can't fit the model in L2.
- **Bandwidth, not latency, dominates for large reads.** What matters is the *rate* at which data flows.

### The decisive math: am I compute-bound or memory-bound?

For a kernel that does `B` bytes of memory traffic and `F` FLOPs:

- **Arithmetic intensity** = `F / B` (ops per byte).
- **Hardware ridge point** for H100 FP16: ~989 TFLOPs ÷ 3.35 TB/s ≈ **295 ops/byte**.

If your intensity is **above** the ridge → compute-bound (you're limited by Tensor Cores). If **below** → memory-bound (you're limited by HBM bandwidth — the Tensor Cores are sitting idle waiting for data).

> **Decode for one user = ~2 ops/byte. That is ~150× below the ridge. The GPU is idle ~99% of the time waiting on weights.**

That single fact explains why batching, KV cache, quantization, and continuous batching all exist.

### Worked example — read 16 GB from HBM at 3.35 TB/s

> 16 GB ÷ 3.35 TB/s = 16 ÷ 3350 s ≈ **4.8 ms** just to *read* the data once.

If you had to do this for every output token of a 70B model loaded across 8 GPUs (so each GPU reads ~17 GB of weights per token), decode latency floor ≈ 4–5 ms/token — and that's *before* doing any actual math.

### Why kernel fusion matters

Two unfused kernels: each writes output to HBM (~80 ns + bandwidth cost), then the next reads it back. Fused into one kernel: intermediates stay in registers (sub-ns). **Same math, ~75× faster** for a 4 KB block reused 1000 times (per Reader 5's worked example). FlashAttention (tomorrow's day) is exactly this idea.

## Practice (90 min)

1. (15 min) Calculate: time to read 16 GB from H100 HBM at 3.35 TB/s. Time if you could somehow keep it in L2 (assume L2 bandwidth ≈ 12 TB/s).
2. (20 min) Compute the arithmetic intensity for: (a) matrix multiply of two N×N matrices (N=4096) → ~2N³ FLOPs, ~3N² × 2 bytes (FP16); (b) elementwise add of two N-vectors. Which is compute-bound, which is memory-bound?
3. (25 min) Pair worked example: estimate decode time per token for Llama-3-8B (16 GB FP16 weights) on one H100. Then estimate prefill time per token. Why is decode so much closer to the memory ceiling?
4. (20 min) Group discussion: "what's the difference between *kernel fusion* and *operator fusion*?" Resolve from the glossary.
5. (10 min) Write one sentence that you can use tomorrow to motivate FlashAttention.

## Wrap-up

Each pair states *one* memory number they'll remember forever (most pick 3.35 TB/s or the 295 ridge point).

## Connect forward

Tomorrow: arithmetic intensity gets formalized into the **roofline model**, and we classify five real workloads against it.

---

## Pre-read for tomorrow (Day 9 · Compute-Bound vs Memory-Bound)

- **Resource:** "Arithmetic intensity" explainer — Pre-Lecture Reading **Reader 4 (complexity / memory / attention math)** + Study Guide §A.5 roofline subsection (~15 min).
- **Reflection questions:**
  1. If a kernel does 100 ops and reads 50 bytes, what's its intensity?
  2. Why is prefill compute-bound and decode memory-bound? (One sentence.)
  3. What does the *roofline model* tell you that arithmetic intensity alone doesn't?
