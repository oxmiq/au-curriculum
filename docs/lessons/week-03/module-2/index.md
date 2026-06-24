# Day 12 · The KV Cache

> **Concept of the day:** KV cache = stored keys and values from all prior tokens. Grows linearly with context. **Can exceed model weight memory** at long contexts.<br>
> **Pre-reading:** "KV cache explained" blog with diagrams — Pre-Lecture Reading **Reader 4** + Study Guide §A.2 (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 — Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 12 · KV Cache</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-03/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts: Why KV Cache Exists | 20 min |
| Part 3 | Deep Dive: KV Cache Size Formula | 20 min |
| Part 4 | Hands-On: Calculate KV Cache Size | 30 min |
| Part 5 | Hands-On: GQA Impact | 20 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: "KV cache explained" blog with diagrams — Pre-Lecture Reading **Reader 4** + Study Guide §A.2 (~20 min).

### Quick Self-Check

Answer these questions from memory:
1. What grows every time the model generates a token?
2. Where in the transformer is the KV cache used?
3. For a 70B model at 128K context, can the KV cache exceed the size of the model weights?

---

## Part 2 — Core Concepts — Why KV Cache Exists · 20 min
### Reading — The Problem Without Cache

Without a cache, generating output token *t* would require re-running attention over *all t–1* previously seen tokens. That's O(t²) cumulative work for *t* output tokens.

### The Solution: KV Cache

The KV cache stores the **K** (keys) and **V** (values) tensors that each layer computed for every token already in the sequence. Generating token *t* only needs to:

1. **Compute** new K, V for the *one* new token
2. **Attend** over the *cached* K, V for all previous tokens

> **That turns decode into O(t) per token — and is the only reason single-user generation is feasible.**

### Why This Matters

Without KV cache:
- 4-token reply would need ~16 forward passes worth of compute
- With KV cache: only ~5 forward passes (1 prefill + 4 decode)

---

## Part 3 — Deep Dive — KV Cache Size Formula · 20 min
### Reading — The Math

For one token, one layer:

> **bytes = 2 × num_kv_heads × head_dim × bytes_per_element**

For the whole sequence:

> **KV bytes = 2 × L × num_kv_heads × head_dim × seq_len × bytes_per_element**

Where:
- L = number of layers
- 2 = for K and V
- seq_len = context length

### Worked Example — Llama-3.1-8B (FP16)

Llama-3.1-8B uses **GQA** with 8 KV heads, head_dim 128, 32 layers, 2 bytes (FP16):

| Calculation | Value |
|-------------|-------|
| Per-token, per-layer | 2 × 8 × 128 × 2 = **4 KB** |
| Per-token, full model | 4 KB × 32 layers = **128 KB** |

### Context Size Comparison

| Context | KV Cache Size | Vs 16 GB Model Weights |
|---------|---------------|------------------------|
| 4K | 128 KB × 4096 = 512 MB | 3.1% |
| 32K | 128 KB × 32,768 = **4 GB** | 25% |
| 128K | 128 KB × 131,072 = **16 GB** | **100%** |

> **At 128K context with batch = 1, the KV cache is as big as the model itself.** With any meaningful batch, it dwarfs the model.

---

## Part 4 — Hands-On — Calculate KV Cache Size · 30 min
### Exercise 1: Llama-3.1-8B at Different Contexts (15 min)

Calculate KV cache size for Llama-3.1-8B at:
- 4K context
- 32K context  
- 128K context

Then calculate: At 80 GB H100, what's the max batch size at each context length (after subtracting 16 GB model weights)?

**Answers:**
- 4K: 512 MB → max batch ~80 (before weights)
- 32K: 4 GB → max batch ~19
- 128K: 16 GB → max batch ~4 (if just model + KV, no room for computation)

### Exercise 2: 70B Model (15 min)

Recalculate for a 70B model with:
- 64 KV heads
- head_dim 128
- 80 layers
- GQA

At 80 GB H100, what context length saturates a single H100?

---

## Part 5 — Hands-On — GQA Impact · 20 min
### Reading — Why MQA / GQA Exist

Multi-Query Attention and Grouped-Query Attention shrink the KV cache by reducing `num_kv_heads`.

Llama-3 uses GQA with 8 KV heads vs 32 query heads → **4× smaller KV cache** than full MHA.

### Exercise: Quantization Preview

If K and V are stored in FP8 (1 byte) instead of FP16 (2 bytes), redo the 128K calculation for 8B:

- Per-token: 2 × 8 × 128 × 1 = 2 KB
- Per-model: 2 KB × 32 = 64 KB
- At 128K: 64 KB × 131,072 = **8 GB**

**Question:** Does the cache now fit alongside the model?

**Answer:** Yes! 8 GB KV + 16 GB weights = 24 GB (leaves 56 GB for batching)

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you explain these from memory?
- [ ] Why does the KV cache exist?
- [ ] What's the formula for KV cache size?
- [ ] At what context length does KV cache match model weight size for 8B?
- [ ] Why does long-context serving push against HBM limits?

### The Key Insight

> **KV cache scales linearly with context, blows past model weights, eats HBM that batching needs.**

### Connect Forward

Tomorrow: how **FlashAttention** rearranges the attention math to use HBM less, and how **PagedAttention** treats KV cache like an OS paging system — both are direct attacks on today's problem.

### Pre-read for tomorrow (Day 13 · FlashAttention & PagedAttention)

- **Resource:** FlashAttention blog summary + paper abstract — Pre-Lecture Reading **Reader 4** (FlashAttention section) (~20 min).
- **Reflection questions:**
  1. Why is naive attention slow? Think about memory reads.
  2. What does "lossless" mean about FlashAttention?
  3. What does **PagedAttention** borrow from operating-system design?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
