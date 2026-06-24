# Day 13 · FlashAttention & PagedAttention

> **Concept of the day:** **FlashAttention** = fuse attention into one kernel, minimize HBM trips (lossless). **PagedAttention** = virtual memory for the KV cache, modeled on OS paging.<br>
> **Pre-reading:** FlashAttention blog summary + paper abstract — Pre-Lecture Reading **Reader 4** (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 — Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 13 · FlashAttention</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-03/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts: Naive Attention Problem | 20 min |
| Part 3 | Deep Dive: FlashAttention Mechanics | 20 min |
| Part 4 | Hands-On: Memory Traffic Calculation | 25 min |
| Part 5 | Core Concepts: PagedAttention | 20 min |
| Part 6 | Hands-On: Multi-User Throughput | 20 min |
| Part 7 | Wrap-up & Connection | 5 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: FlashAttention blog summary + paper abstract — Pre-Lecture Reading **Reader 4** (~20 min).

### Quick Self-Check

Answer these questions from memory:
1. In naive attention, where does the N×N attention matrix live? (Hint: it's huge.)
2. Why is FlashAttention called "I/O-aware"?
3. What's "lossless" about FlashAttention?
4. PagedAttention's KV blocks are analogous to OS ___?
5. What problem does PagedAttention solve that FlashAttention doesn't?

---

## Part 2 — Core Concepts — Naive Attention's Memory Problem · 20 min
### Reading — The Hidden Cost

For sequence length N, attention computes the matrix `S = Q · Kᵀ` of shape **N × N**. For N = 32K, that's a **1 billion element matrix** per head per layer.

> **For N=32K with 32 heads: that's 32 billion elements — all in floating-point — just for the attention scores.**

### Why This Matters

Naive implementations materialize this in HBM, softmax it, then multiply by V:

- **HBM writes:** O(N²) per head per layer
- **HBM reads:** O(N²) again to apply softmax and multiply
- The actual math is O(N²) but the *traffic* is O(N²) too — far above the GPU's roofline ridge

### The Roofline Insight

On H100, the ops:byte ratio is ~295. Standard attention during decode has intensity ~62 ops/byte — far below the ridge. The GPU sits idle waiting for memory, not computing.

> **This is why long-context serving was impractical before FlashAttention.**

---

## Part 3 — Deep Dive — FlashAttention Mechanics · 20 min
### Reading — The I/O-Aware Solution

> **Don't materialize the N×N matrix in HBM. Compute attention in tiles that fit in SRAM, using an online softmax trick.**

FlashAttention works by:

1. **Tile** Q, K, V into blocks small enough to fit in SM-local SRAM (per-SM 256 KB)
2. Compute partial softmax statistics (max + denominator) incrementally
3. Combine tiles using **online softmax** (numerically stable rescaling)
4. Only the **final O(N)-sized output** ever touches HBM

### Result

- **HBM traffic drops from O(N²) to O(N)**
- **5–20× wall-clock speedup** on long context
- **Bit-identical output** — same softmax, same numerical precision

### Why "Lossless"

It's just a different memory schedule. The math is identical; only the order of operations changes. Compare to quantization (Day 14), which *does* change the numbers.

### Source Material Reference

From **Inference Engineering Study Guide §2.5**: "FlashAttention — tens of thousands of lines of fused kernels tailored per GPU generation (FA-3 for Hopper, FA-4 for Blackwell). Eliminates redundant HBM reads/writes."

---

## Part 4 — Hands-On — Memory Traffic Calculation · 25 min
### Exercise 1: Naive vs FlashAttention Traffic (15 min)

Calculate HBM traffic for one attention head at different sequence lengths (FP16, 2 bytes per element):

| Sequence Length | Naive: QKᵀ Write | Naive: Softmax Read | Naive: PV Write | FlashAttention | Ratio |
|-----------------|------------------|--------------------|-----------------|-----------------|-------|
| 1K | ? | ? | ? | ? | — |
| 4K | ? | ? | ? | ? | — |
| 32K | ? | ? | ? | ? | — |

**Formula hints:**
- Naive QKᵀ: 2 × N × N (write + read)
- Naive PV: 2 × N × N × d (write + read, includes d factor)
- FlashAttention: ~3 × N × d (tile loads + output)

**Answer (N=4K, d=128):**
- Naive: ~8 GB per head per layer
- FlashAttention: ~0.003 GB per head per layer
- **Ratio: ~2500× reduction!**

### Exercise 2: When Does FlashAttention Dominate? (10 min)

Given:
- Naive attention: 2 × N² × d bytes per layer
- FlashAttention: 3 × N × d bytes per layer
- Break-even when: 2N² = 3N → N = 1.5

For N > 1.5, FlashAttention saves memory. At what sequence length does this become *dramatically* better (>100×)?

---

## Part 5 — Core Concepts — PagedAttention · 20 min
### Reading — The Fragmentation Problem

In a naive implementation, you reserve a **contiguous** chunk of HBM for each request's KV cache — sized for the *worst-case* sequence length:

- Reserve 128K-token cache slot per request
- Request actually uses 2K tokens
- **98% of that slot is wasted**

With concurrent users, you run out of HBM long before you run out of bandwidth — throughput collapses.

### What PagedAttention Does

> **Treat KV cache as fixed-size blocks (pages) in a virtual address space — like an OS pages physical RAM.**

Key concepts:
- KV cache split into **blocks** (typically 16 tokens each)
- Each request has a **block table** mapping logical positions → physical blocks
- New blocks allocated on demand
- **Sharing:** prefix caching (shared system prompt across requests) becomes free — same blocks referenced by many requests

### Result

- HBM utilization for KV cache: **~20% → ~90%+**
- Practical throughput on long-context: **2–4×** at same hardware

### Why This Matters Together

| Trick | What It Attacks | Symbiotic With |
|-------|-----------------|----------------|
| FlashAttention | Per-step HBM traffic (per-token cost) | PagedAttention (more concurrent = more value) |
| PagedAttention | HBM fragmentation (multi-user cost) | FlashAttention (each user's attention faster) |

Together they enable **vLLM-class throughput**: high concurrency at long context.

---

## Part 6 — Hands-On — Multi-User Throughput · 20 min
### Exercise: Concurrent User Memory Budget (20 min)

From Day 12: Llama-3-8B at 128K context, KV = 16 GB per request (single user).

**Scenario:** 4 concurrent users, each averaging 8K context.

**Question 1:** Naive contiguous allocation — total KV cache reserved?
- 4 users × 128K worst-case slots = 4 × 16 GB = **64 GB** reserved
- But actual usage: 4 × 8K × 128 KB = 4 × 1 GB = **4 GB** used
- **Waste: 60 GB = 94% wasted!**

**Question 2:** PagedAttention with 16-token blocks — what's the overhead?
- Block table per request: 8192 / 16 = 512 entries
- Each entry: 8 bytes → 4 KB per request
- Total overhead: 4 × 4 KB = **16 KB** (negligible)

**Question 3:** Combined with FlashAttention, what's the throughput improvement?
- FlashAttention: ~5× faster attention per user
- PagedAttention: ~4× more concurrent users fit
- **Combined: ~20× more effective throughput**

### Connect to Practice

This is why vLLM and SGLang use both together. The kernel (FlashAttention) makes each user faster; the memory manager (PagedAttention) fits more users.

---

## Part 7 — Wrap-up & Connection · 5 min
### Self-Check

Can you explain these from memory?
- [ ] Why does naive attention require O(N²) HBM traffic?
- [ ] How does FlashAttention reduce this to O(N)?
- [ ] What does "lossless" mean in FlashAttention?
- [ ] What's the fragmentation problem PagedAttention solves?
- [ ] Why are FlashAttention and PagedAttention symbiotic?

### The Key Insight

> **These two innovations are the reason long-context serving (32K, 128K, 1M tokens) became commercially viable. Both are pure systems wins — the model output is identical.**

### Connect Forward

Tomorrow: **quantization** — the lossy-but-massive lever. K/V/W/A precision matters in different orders. We finish Week 3 by combining FlashAttention + KV cache + INT4/FP8 weights into a single mental model.

### Pre-read for tomorrow (Day 14 · Quantization)

- **Resource:** "What is quantization?" Hugging Face blog — Pre-Lecture Reading **Reader 7 (numerical precision)** (~20 min).
- **Reflection questions:**
  1. FP16 = how many bytes per number? FP8? INT4?
  2. Why is *float* generally preferred over *int* for weights, despite using more bits?
  3. Of {weights, activations, KV cache, attention output} — which is *least* sensitive to quantization?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
