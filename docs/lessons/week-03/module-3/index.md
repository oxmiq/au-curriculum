# Day 13 · FlashAttention & PagedAttention

> **Concept of the day:** **FlashAttention** = fuse attention into one kernel, minimize HBM trips (lossless). **PagedAttention** = virtual memory for the KV cache, modeled on OS paging.<br>
> **Pre-reading:** FlashAttention summary + PagedAttention: <a href="https://gordicaleksa.medium.com/eli5-flash-attention-5c44017022ad" target="_blank" rel="noopener">Aleksa Gordić - ELI5 FlashAttention</a> + <a href="https://blog.vllm.ai/2023/06/20/vllm.html" target="_blank" rel="noopener">vLLM - PagedAttention</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 - Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 13 · FlashAttention</span>
    {status:week-03/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Naive Attention Problem |
| Part 3 | Deep Dive: FlashAttention Mechanics |
| Part 4 | Hands-On: Memory Traffic Calculation |
| Part 5 | Core Concepts: PagedAttention |
| Part 6 | Hands-On: Multi-User Throughput |
| Part 7 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: FlashAttention blog summary + paper abstract: Pre-Lecture Reading **Reader 4**.

### Quick Self-Check

Answer these questions from memory:

1. In naive attention, where does the N×N attention matrix live? (Hint: it's huge.)
2. Why is FlashAttention called "I/O-aware"?
3. What's "lossless" about FlashAttention?
4. PagedAttention's KV blocks are analogous to OS ___?
5. What problem does PagedAttention solve that FlashAttention doesn't?

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m3-readiness" data-kind="readiness" data-draw="5" data-source="Aleksa Gordić - ELI5 FlashAttention + vLLM PagedAttention">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "In naive attention, where does the N×N attention matrix live, and why is this a problem?",
    "options": [
      "In registers: fast but small",
      "In HBM: huge memory traffic bottleneck",
      "In L2 cache: moderate speed",
      "In the model's weights"
    ],
    "answer": 1,
    "explain": "Naive attention computes and stores the full N×N attention matrix in HBM. For 4096 context, that's 16M values. Every forward pass reads/writes this: massive memory traffic. This is the core inefficiency."
  },
  {
    "stem": "Why is FlashAttention called 'I/O-aware'?",
    "options": [
      "It uses more memory than naive attention",
      "It explicitly accounts for the cost of reading/writing HBM in its algorithm design, minimizing data movement",
      "It works with any GPU",
      "It requires fast storage"
    ],
    "answer": 1,
    "explain": "FlashAttention is I/O-aware because it accounts for the slow HBM read/write in its algorithm. It uses tiling to keep data in fast SRAM, doing many small HBM accesses instead of one massive one."
  },
  {
    "stem": "What does 'lossless' mean in the context of FlashAttention?",
    "options": [
      "It cannot compress data",
      "It maintains full precision (no dropout or approximation) compared to naive attention",
      "It is faster but less accurate",
      "It uses lossless compression algorithms"
    ],
    "answer": 1,
    "explain": "FlashAttention is 'lossless': it produces identical results to naive attention mathematically, just with far fewer HBM accesses. The output is bit-for-bit identical, not an approximation."
  },
  {
    "stem": "PagedAttention's KV blocks are analogous to what OS concept?",
    "options": [
      "CPU registers",
      "Virtual memory / paging",
      "Hard drive defragmentation",
      "Process scheduling"
    ],
    "answer": 1,
    "explain": "PagedAttention models itself on OS virtual memory: KV cache is split into fixed-size blocks (like memory pages), allowing non-contiguous storage. This eliminates the need to allocate huge contiguous memory buffers."
  },
  {
    "stem": "What problem does PagedAttention solve that FlashAttention doesn't?",
    "options": [
      "FlashAttention is not fast enough",
      "Memory fragmentation in long-context serving: KV cache allocation and reallocation",
      "Model weight loading",
      "Attention computation accuracy"
    ],
    "answer": 1,
    "explain": "PagedAttention solves memory fragmentation. In long-running inference, the KV cache grows/shrinks dynamically. Contiguous allocation wastes memory. PagedAttention pages non-contiguously like OS virtual memory."
  },
  {
    "stem": "How does FlashAttention minimize HBM traffic?",
    "options": [
      "By using more compute",
      "By using tiling: keeping data in SRAM, doing attention in blocks, and streaming results back",
      "By reducing model size",
      "By using quantization"
    ],
    "answer": 1,
    "explain": "FlashAttention uses tiling: load a block of Q, K, V into fast SRAM, compute partial attention, store intermediate results, repeat. Only final results go to HBM. This is O(N) instead of O(N²) HBM accesses."
  },
  {
    "stem": "What is the main benefit of combining FlashAttention and PagedAttention?",
    "options": [
      "They are mutually exclusive",
      "FlashAttention provides the fast attention computation, PagedAttention provides efficient memory management for the KV cache",
      "They both use the same block size",
      "They eliminate the need for KV caching"
    ],
    "answer": 1,
    "explain": "vLLM combines both: FlashAttention for fast attention computation, PagedAttention for efficient KV cache memory management. Together they provide both fast compute AND efficient memory use."
  },
  {
    "stem": "Why is block-sparse attention important?",
    "options": [
      "It uses more memory",
      "It skips computation on attention blocks that are likely to be zero, reducing compute for sparse patterns",
      "It requires special hardware",
      "It is slower than FlashAttention"
    ],
    "answer": 1,
    "explain": "Block-sparse attention extends FlashAttention by skipping entire blocks where attention scores are near-zero. This gives additional speedup for patterns like local attention or structured sparsity: compute savings without accuracy loss."
  }
]
</script>
</div>

---

## Part 2 - Core Concepts - Naive Attention's Memory Problem
### Reading - The Hidden Cost

For sequence length N, attention computes the matrix `S = Q · Kᵀ` of shape **N × N**. For N = 32K, that's a **1 billion element matrix** per head per layer.

> **For N=32K with 32 heads: that's 32 billion elements, all in floating-point, just for the attention scores.**

### Why This Matters

Naive implementations materialize this in HBM, softmax it, then multiply by V:

- **HBM writes:** O(N²) per head per layer
- **HBM reads:** O(N²) again to apply softmax and multiply
- The actual math is O(N²) but the *traffic* is O(N²) too: far above the GPU's roofline ridge

### The Roofline Insight

On H100, the ops:byte ratio is ~295. Standard attention during decode has intensity ~62 ops/byte: far below the ridge. The GPU sits idle waiting for memory, not computing.

> **This is why long-context serving was impractical before FlashAttention.**

---

## Part 3 - Deep Dive - FlashAttention Mechanics
### Reading - The I/O-Aware Solution

> **Don't materialize the N×N matrix in HBM. Compute attention in tiles that fit in SRAM, using an online softmax trick.**

FlashAttention works by:

1. **Tile** Q, K, V into blocks small enough to fit in SM-local SRAM (per-SM 256 KB)
2. Compute partial softmax statistics (max + denominator) incrementally
3. Combine tiles using **online softmax** (numerically stable rescaling)
4. Only the **final O(N)-sized output** ever touches HBM

### Result

- **HBM traffic drops from O(N²) to O(N)**
- **5–20× wall-clock speedup** on long context
- **Bit-identical output**: same softmax, same numerical precision

### Why "Lossless"

It's just a different memory schedule. The math is identical; only the order of operations changes. Compare to quantization (Day 14), which *does* change the numbers.

### Source Material Reference

From **Inference Engineering Study Guide §2.5**: "FlashAttention - tens of thousands of lines of fused kernels tailored per GPU generation (FA-3 for Hopper, FA-4 for Blackwell). Eliminates redundant HBM reads/writes."

---

## Part 4 - Hands-On - Memory Traffic Calculation
### Exercise 1: Naive vs FlashAttention Traffic

Calculate HBM traffic for one attention head at different sequence lengths (FP16, 2 bytes per element):

| Sequence Length | Naive: QKᵀ Write | Naive: Softmax Read | Naive: PV Write | FlashAttention | Ratio |
|-----------------|------------------|--------------------|-----------------|-----------------|-------|
| 1K | ? | ? | ? | ? | - |
| 4K | ? | ? | ? | ? | - |
| 32K | ? | ? | ? | ? | - |

**Formula hints:**
- Naive QKᵀ: 2 × N × N (write + read)
- Naive PV: 2 × N × N × d (write + read, includes d factor)
- FlashAttention: ~3 × N × d (tile loads + output)

**Answer (N=4K, d=128):**
- Naive: ~8 GB per head per layer
- FlashAttention: ~0.003 GB per head per layer
- **Ratio: ~2500× reduction!**

### Exercise 2: When Does FlashAttention Dominate?

Given:
- Naive attention: 2 × N² × d bytes per layer
- FlashAttention: 3 × N × d bytes per layer
- Break-even when: 2N² = 3N → N = 1.5

For N > 1.5, FlashAttention saves memory. At what sequence length does this become *dramatically* better (>100×)?

---

## Part 5 - Core Concepts - PagedAttention
### Reading - The Fragmentation Problem

In a naive implementation, you reserve a **contiguous** chunk of HBM for each request's KV cache: sized for the *worst-case* sequence length:

- Reserve 128K-token cache slot per request
- Request actually uses 2K tokens
- **98% of that slot is wasted**

With concurrent users, you run out of HBM long before you run out of bandwidth: throughput collapses.

### What PagedAttention Does

> **Treat KV cache as fixed-size blocks (pages) in a virtual address space: like an OS pages physical RAM.**

Key concepts:
- KV cache split into **blocks** (typically 16 tokens each)
- Each request has a **block table** mapping logical positions → physical blocks
- New blocks allocated on demand
- **Sharing:** prefix caching (shared system prompt across requests) becomes free: same blocks referenced by many requests

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

## Part 6 - Hands-On - Multi-User Throughput
### Exercise: Concurrent User Memory Budget

From Day 12: Llama-3-8B at 128K context, KV = 16 GB per request (single user).

**Scenario:** 4 concurrent users, each averaging 8K context.

**Question 1:** Naive contiguous allocation: total KV cache reserved?
- 4 users × 128K worst-case slots = 4 × 16 GB = **64 GB** reserved
- But actual usage: 4 × 8K × 128 KB = 4 × 1 GB = **4 GB** used
- **Waste: 60 GB = 94% wasted!**

**Question 2:** PagedAttention with 16-token blocks: what's the overhead?
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

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 13 · FlashAttention &amp; PagedAttention">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Why does naive attention require O(N²) HBM traffic?",
    "options": [
      "Because the model has N² parameters that must all be read",
      "Because the N×N attention matrix must be fully materialized in HBM, requiring O(N²) reads and writes",
      "Because each of the N tokens requires N forward passes through the model",
      "Because vocabulary projection at the end scales as O(N²)"
    ],
    "answer": 1,
    "explain": "Naive attention computes QKᵀ/√d and materializes the full N×N attention score matrix, then softmax, then multiplies by V. This requires writing and re-reading O(N²) elements to/from HBM. For N=128K, that's 16 billion elements: a massive bandwidth bottleneck."
  },
  {
    "stem": "How does FlashAttention reduce HBM traffic from O(N²) to O(N)?",
    "options": [
      "By approximating the attention scores and skipping low-weight entries",
      "By splitting Q, K, V into tiles that fit in L1/SRAM and computing attention incrementally without materializing the full N×N matrix",
      "By caching the N×N matrix across requests to avoid recomputation",
      "By reducing sequence length N through token merging before attention"
    ],
    "answer": 1,
    "explain": "FlashAttention tiles the computation so Q, K, V blocks fit in fast on-chip SRAM (L1). It computes attention block by block and accumulates the softmax incrementally, never writing the full N×N matrix to HBM. The result: O(N) HBM reads/writes instead of O(N²), with identical mathematical output."
  },
  {
    "stem": "What does 'lossless' mean in the context of FlashAttention?",
    "options": [
      "FlashAttention uses lossless compression to reduce model weight size",
      "FlashAttention produces bit-exact outputs identical to standard attention: it only changes how memory is accessed, not the math",
      "FlashAttention avoids any numerical approximations in the softmax",
      "FlashAttention stores keys and values without any quantization"
    ],
    "answer": 1,
    "explain": "FlashAttention is a pure I/O optimization: it rearranges memory access patterns but computes exactly the same mathematical operation as naive attention. The output is numerically identical (up to floating-point associativity). This is why it can be dropped into any model without changing the weights."
  },
  {
    "stem": "What problem does PagedAttention solve?",
    "options": [
      "The O(N²) memory access pattern of standard attention",
      "KV cache memory fragmentation: large contiguous allocations waste HBM due to different sequence lengths per request",
      "The latency of reading model weights during prefill",
      "The imprecision introduced by mixed-precision attention computation"
    ],
    "answer": 1,
    "explain": "Without PagedAttention, engines pre-allocate contiguous KV cache blocks. Because requests have different lengths, internal fragmentation wastes significant HBM. PagedAttention allocates KV cache in small fixed-size pages (like OS virtual memory paging), eliminating fragmentation."
  },
  {
    "stem": "What OS concept does PagedAttention borrow from?",
    "options": [
      "File system journaling: writes are first buffered before committing",
      "Virtual memory paging: map logical memory to non-contiguous physical pages",
      "CPU scheduling: interleave small tasks to improve throughput",
      "Disk caching: keep recently accessed data in a fast buffer"
    ],
    "answer": 1,
    "explain": "PagedAttention borrows virtual memory paging from OS design. Instead of requiring a single contiguous HBM block per request, it uses a page table to map logical KV positions to any physical HBM pages. This allows non-contiguous allocation, eliminating fragmentation while supporting dynamic growth."
  },
  {
    "stem": "Why are FlashAttention and PagedAttention described as 'symbiotic'?",
    "options": [
      "They both reduce model weight size, so combining them gives larger savings",
      "FlashAttention speeds up each individual attention operation; PagedAttention fits more requests in HBM: together they improve both per-request latency and server throughput",
      "FlashAttention replaces PagedAttention when context lengths are short",
      "They share the same memory pool, so using both frees additional HBM"
    ],
    "answer": 1,
    "explain": "FlashAttention reduces the compute/IO cost per attention call (latency benefit). PagedAttention enables more concurrent requests to fit in HBM (throughput benefit). Neither substitutes for the other: production engines like vLLM use both together: FlashAttention for kernel efficiency, PagedAttention for memory management."
  },
  {
    "stem": "What technique lets FlashAttention compute attention in tiles without ever materializing the full N×N matrix in HBM?",
    "options": [
      "Quantizing the attention scores to INT8 before the matmul",
      "Skipping the softmax entirely for long sequences",
      "An online (incremental) softmax that combines per-tile statistics with numerically stable rescaling",
      "Precomputing the whole attention matrix during prefill and caching it"
    ],
    "answer": 2,
    "explain": "Part 3: FlashAttention tiles Q, K, V into blocks that fit in SM-local SRAM, then combines them with an online softmax: accumulating the running max and denominator incrementally with numerically stable rescaling. Only the O(N)-sized output ever touches HBM, so the full N×N matrix is never written."
  },
  {
    "stem": "The lesson describes PagedAttention's KV blocks. What is the typical block size, and what maps logical positions to physical blocks?",
    "options": [
      "Blocks of 128K tokens; a single contiguous buffer reserved per request",
      "One block per layer; the model weights hold the mapping",
      "Blocks of ~16 tokens each; a per-request block table maps logical positions to physical blocks allocated on demand",
      "Blocks of 1 token; the tokenizer holds the mapping"
    ],
    "answer": 2,
    "explain": "Part 5: KV cache is split into fixed-size blocks (typically 16 tokens). Each request has a block table mapping logical positions to physical blocks, with new blocks allocated on demand: exactly the way an OS pages physical RAM via a page table."
  },
  {
    "stem": "According to the lesson, what does PagedAttention do to KV-cache HBM utilization, and why does prefix caching become effectively free?",
    "options": [
      "It drops utilization to ~20%; prefix caching requires copying blocks between requests",
      "It raises utilization from ~20% to ~90%+; a shared prefix's blocks can be referenced by many requests instead of duplicated",
      "It has no effect on utilization; prefix caching is unrelated to paging",
      "It raises utilization only during prefill, never during decode"
    ],
    "answer": 1,
    "explain": "Part 5: paging raises KV-cache HBM utilization from ~20% to ~90%+ and lifts long-context throughput 2–4×. Because blocks are referenced through block tables, a shared system prompt's blocks can simply be pointed to by many requests: so prefix caching costs nothing extra."
  }
]
</script>
</div>

### The Key Insight

> **These two innovations are the reason long-context serving (32K, 128K, 1M tokens) became commercially viable. Both are pure systems wins: the model output is identical.**

### Connect Forward

Tomorrow: **quantization** - the lossy-but-massive lever. K/V/W/A precision matters in different orders. We finish Week 3 by combining FlashAttention + KV cache + INT4/FP8 weights into a single mental model.

### Pre-read for tomorrow (Day 14 · Quantization)

- **Resource:** <a href="https://huggingface.co/docs/optimum/concept_guides/quantization" target="_blank" rel="noopener">Hugging Face - Quantization</a>. Alternative: <a href="https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization" target="_blank" rel="noopener">Maarten Grootendorst - A Visual Guide to Quantization</a>.
- **Reflection questions:**
  1. FP16 = how many bytes per number? FP8? INT4?
  2. Why is *float* generally preferred over *int* for weights, despite using more bits?
  3. Of {weights, activations, KV cache, attention output}: which is *least* sensitive to quantization?

---

## Stuck?

Ask **oxtutor**: share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
