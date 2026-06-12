# Day 13 · FlashAttention & PagedAttention

> **Concept of the day:** **FlashAttention** = fuse attention into one kernel, minimize HBM trips (lossless). **PagedAttention** = virtual memory for the KV cache, modeled on OS paging.
> **Pre-reading:** FlashAttention blog summary + paper abstract — Pre-Lecture Reading **Reader 4** (~20 min).
> **Source:** [Study Guide §A.5](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Lecture Slides Day 13](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Lecture_Slides.md).

---

## Why this matters

These two innovations are the reason long-context serving (32K, 128K, 1M tokens) became commercially viable. FlashAttention rewrote the attention kernel; PagedAttention rewrote how vLLM stores the cache. Both are pure systems wins — the model output is identical.

## Readiness check

1. In naive attention, where does the N×N attention matrix live? (Hint: it's huge.)
2. Why is FlashAttention called "I/O-aware"?
3. What's lossless about FlashAttention?
4. PagedAttention's KV blocks are analogous to OS ___?
5. What problem does PagedAttention solve that FlashAttention doesn't?

## Core concept — FlashAttention

### Naive attention's memory problem

For sequence length N, attention computes the matrix `S = Q · Kᵀ` of shape **N × N**. For N = 32K, that's a **1 billion element matrix** per head per layer. Naive implementations materialize this in HBM, softmax it, then multiply by V.

- HBM writes: O(N²) per head per layer.
- HBM reads: O(N²) again to apply softmax and multiply.
- The actual math is O(N²) but the *traffic* is O(N²) too — far above the roofline ridge.

### What FlashAttention does

> **Don't materialize the N×N matrix in HBM. Compute attention in tiles that fit in SRAM, using an online softmax trick.**

- **Tile** Q, K, V into blocks small enough to fit in SM-local SRAM (per-SM 256 KB).
- Compute partial softmax statistics (max + denominator) incrementally.
- Combine tiles using **online softmax** (numerically stable rescaling).
- Only the **final O(N)-sized output** ever touches HBM.

Result: HBM traffic drops from O(N²) to O(N). On long context, this is **a 5–20× wall-clock speedup with bit-identical output**.

### Why "lossless"

Same softmax, same numerical precision, same answer. It's just a different memory schedule. (Compare to quantization, Day 14, which *is* lossy.)

## Core concept — PagedAttention

### The fragmentation problem

In a naive implementation, you reserve a **contiguous** chunk of HBM for each request's KV cache — sized for the *worst-case* sequence length. This wastes huge amounts of HBM:

- Reserve 128K-token cache slot per request.
- Request actually uses 2K tokens.
- 98% of that slot is wasted.

With concurrent users, you run out of HBM long before you run out of bandwidth — throughput collapses.

### What PagedAttention does

> **Treat KV cache as fixed-size blocks (pages) in a virtual address space — like an OS pages physical RAM.**

- KV cache split into **blocks** (typically 16 tokens each).
- Each request has a **block table** mapping logical positions → physical blocks.
- New blocks allocated on demand.
- **Sharing:** prefix caching (shared system prompt across requests) becomes free — same blocks referenced by many requests.

Result: HBM utilization for KV cache jumps from ~20% to ~90%+. Practical throughput on long-context workloads jumps **2–4×** at the same hardware.

### Why this matters together

| Trick | What it attacks | Symbiotic with |
|---|---|---|
| FlashAttention | Per-step HBM traffic (the per-token cost) | PagedAttention (more concurrent requests = more value from kernel speedup) |
| PagedAttention | HBM capacity fragmentation (the multi-user cost) | FlashAttention (each user's attention is faster too) |

Together they enable **vLLM-class throughput**: high concurrency at long context.

## Practice (90 min)

1. (15 min) Draw two memory access patterns side by side: naive attention (many N×N HBM reads/writes) vs FlashAttention (tile-fused, output-only HBM write). Annotate the difference.
2. (25 min) Compute the HBM-traffic reduction for FlashAttention at N = 4K and N = 32K (assume one head, FP16). Ratio? At which N does FlashAttention dominate?
3. (20 min) Pair drill: take the Day 12 calculation (Llama-3-8B at 128K context, KV = 16 GB). Now imagine 4 concurrent users at avg 8K context each. Naive contiguous allocation: total reserved? PagedAttention with 16-token blocks: roughly?
4. (20 min) Read the vLLM docs intro page (will be Day 19's pre-read). Spot the words "PagedAttention" and "continuous batching." Note questions for later.
5. (10 min) Write a one-sentence answer to: *"Why aren't these two tricks just 'extra software'?"*

## Wrap-up

Each pair states the *one* trick they'd port to a new accelerator first, and why.

## Connect forward

Tomorrow: **quantization** — the lossy-but-massive lever. K/V/W/A precision matters in different orders. We finish Week 3 by combining FlashAttention + KV cache + INT4/FP8 weights into a single mental model.

---

## Pre-read for tomorrow (Day 14 · Quantization)

- **Resource:** "What is quantization?" Hugging Face blog — Pre-Lecture Reading **Reader 7 (numerical precision)** (~20 min).
- **Reflection questions:**
  1. FP16 = how many bytes per number? FP8? INT4?
  2. Why is *float* generally preferred over *int* for weights, despite using more bits?
  3. Of {weights, activations, KV cache, attention output} — which is *least* sensitive to quantization?
