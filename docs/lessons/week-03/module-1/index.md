# Day 11 · Prefill and Decode

> **Concept of the day:** the two phases of inference. **Prefill** = parallel, compute-bound, drives TTFT. **Decode** = sequential, memory-bound, drives TPS.
> **Pre-reading:** "Prefill vs decode" explainer — Pre-Lecture Reading **Reader 4 (attention math)** and Reader 6 sections on serving (~15 min).
> **Source:** [Study Guide Ch 2 + §A.2](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

This is the conceptual hinge of the entire serving stack. Every metric, every engine, every parallelism choice in Weeks 4–5 is about *which phase* it optimizes. Confuse them and your latency/throughput trade-offs make no sense.

## Readiness check

1. Which phase processes all input tokens at once? Which one at a time?
2. Which phase is compute-bound? Which is memory-bound? (Day 9 vocabulary.)
3. What does **TTFT** stand for? What drives it?
4. What is **ITL**? What drives it?
5. For a 1000-input / 500-output token request: which phase dominates wall-clock time?

## Core concept

### Prefill — process all input tokens in parallel

> Analogy: **reading a whole book to build context.**

Given N input tokens, prefill runs them through the transformer as a single large batch. The work is one giant set of GEMMs:

- **Parallel** across all N tokens.
- **Compute-bound** — high arithmetic intensity (you're on the right side of the roofline).
- Time scales roughly **linearly with N** (for short context) and **quadratically** in the attention layer (long context).
- Produces: the first output token + the initial KV cache (Day 12).

**Metric driven:** **TTFT** (Time To First Token). The user's first signal that the model is working.

### Decode — one token at a time

> Analogy: **writing one word at a time.**

Once prefill finishes, decode loops:

```
loop:
  use KV cache + previous token → compute attention + MLP → next token
  append next token's K, V to the cache
until stop
```

- **Sequential** — each token depends on the previous.
- **Memory-bound** for single user — intensity ≈ 2 ops/byte.
- Time per token scales with **model size** and **HBM bandwidth** (Day 8 math).

**Metrics driven:**
- **ITL** (Inter-Token Latency) — gap between consecutive output tokens.
- **TPS** = 1000 / ITL_ms — tokens per second per stream.

### One picture, both phases

```
time →
│■■■■■■│ ← prefill (one big GEMM batch)
       │█ █ █ █ █ █ █ █ ...│ ← decode (one token per step)
       ↑                       ↑
       TTFT (first token)       end-to-end latency
```

### Why this matters for design

| Decision | Driven by |
|---|---|
| Bigger Tensor Cores | Prefill (compute-bound) |
| More HBM bandwidth | Decode (memory-bound) |
| Tensor Parallelism | Decode latency (smaller per-GPU weight slice = less to read per token) |
| Continuous batching | Decode throughput (share weight reads across users) |
| Speculative decoding | Decode (convert it into a tiny prefill) |
| Long-context tricks (paged attention) | Decode (KV cache pressure) |

## Practice (90 min)

1. (15 min) Given a request with 1000 input + 500 output tokens, sketch the timeline (prefill bar + decode train). Where does TTFT live? End-to-end latency?
2. (25 min) Numerical exercise: Llama-3-8B on one H100. Estimate prefill time for 1000 input tokens (compute-bound, use ~989 TFLOPs FP16). Estimate decode time per token (memory-bound, use 16 GB ÷ 3.35 TB/s). Total wall-clock?
3. (25 min) Pair drill: for each of these optimizations, label "helps prefill / helps decode / both": kernel fusion, FP8 weights, FlashAttention, larger batch, NVLink, speculative decoding, KV cache, faster Tensor Cores.
4. (15 min) Discussion: a request with 100 input + 5000 output tokens — what dominates? What about 5000 input + 100 output?
5. (10 min) Write the two facts you'll never forget: ___ drives TTFT. ___ drives TPS.

## Wrap-up

The cohort can recite: *"Prefill = compute, decode = memory."* If anyone can't, they get paired tomorrow.

## Connect forward

Tomorrow: the **KV cache** — the structure that makes decode possible at all, and the resource you spend the next three weeks trying to fit, share, and prune.

---

## Pre-read for tomorrow (Day 12 · The KV Cache)

- **Resource:** "KV cache explained" — Pre-Lecture Reading **Reader 4 (attention math)** + Study Guide §A.2 KV-cache subsection (~20 min).
- **Reflection questions:**
  1. What grows every time the model generates a token?
  2. Where in the transformer is the KV cache used?
  3. For a 70B model at 128K context, can the KV cache exceed the size of the model weights themselves?
