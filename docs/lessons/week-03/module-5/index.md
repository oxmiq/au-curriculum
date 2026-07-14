# Day 15 (Fri) · Week 3 Consolidation

> **Goal of the day:** consolidate attention + KV cache + quantization. No new content.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 - Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 15 · Consolidation</span>
    {status:week-03/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Week 3 Concept Review |
| Part 2 | Knowledge Check |
| Part 3 | Memory Budget Calculator Assignment |
| Part 4 | Open Lab / Catch-up Time |
| Part 5 | Self-Check Before Week 4 |
| Part 6 | Wrap-up & Connection |
| Part 7 | Pre-read for Next Week |

---

## Part 1 - Week 3 Concept Review
### Before You Start

Today consolidates everything from Days 11-14. No new content: just mastery.

### Quick Concept Map

Fill in this quick reference from memory:

| Day | Concept | Key Formula |
|-----|---------|-------------|
| 11 | Prefill vs Decode | Prefill = compute-bound, Decode = memory-bound |
| 12 | KV Cache Size | 2 × L × num_kv_heads × head_dim × seq_len × bytes |
| 13 | FlashAttention | HBM traffic: O(N²) → O(N) |
| 13 | PagedAttention | KV blocks = OS pages; ~90% utilization |
| 14 | Quantization | FP16 → FP8 = 2× bandwidth; sensitivity: weights < KV < attn |
| 14 | FP8 vs INT8 | FP8 > INT8 for LLMs (dynamic range) |

### The Big Picture

> **Prefill = compute-bound. Decode = memory-bound. The KV cache is the resource you spend most of Week 4 trying to fit and Week 5 trying to budget.**

---

## Part 2 - Knowledge Check
### Take the Canonical Quiz

[Take the knowledge check](knowledge-check.md); this covers:
- Prefill vs decode distinction
- KV cache math
- FP8/INT4 sizing
- FlashAttention memory savings

**Item bank:** Flashcards Days 11–14 (from planning/source-material/Inference Engineering/)

### What to Expect

- 10-15 questions
- Mix of conceptual and numerical
- Time: ~20 min to complete, ~10 min to review mistakes

---

## Part 3 - Memory Budget Calculator Assignment
### The Assignment

**Memory budget calculator:** Given GPU (80 GB), model, context length, batch size → does it fit? What if you quantize to FP8?

### Exercise Template

Use this template for any scenario:

```
Given:
- GPU: ___-GB (e.g., H100 80 GB)
- Model: ___-B parameters (e.g., Llama-3-8B)
- Precision: FP16 / FP8 / INT4
- Context length: ___
- Batch size: ___

Calculate:
1. Weight memory = params × bytes/param
2. KV cache per user = 2 × L × kv_heads × head_dim × seq_len × bytes
3. Total KV = KV per user × batch_size
4. Activations (estimate) = ~10 GB
5. Total = weights + KV + activations
6. Does it fit? (Total < GPU memory)

If NO: iterate on batch_size, context, or precision
```

### Example: 8B Model on 80 GB H100

| Component | FP16 | FP8 |
|-----------|------|-----|
| Weights | 16 GB | 8 GB |
| KV (4K, batch=4) | 2 GB | 1 GB |
| Activations | 10 GB | 10 GB |
| **Total** | **28 GB** | **19 GB** |
| Fits? | ✅ Yes | ✅ Yes |
| Headroom | 52 GB | 61 GB |

### Source Material Reference

From **Inference Engineering Study Guide §A.2**: "At 8K context per request: 128 KiB × 8192 ≈ 1 GiB per request. On an H100 with 80 GB, after subtracting ~16 GB for weights, you have ~60 GB for KV cache → ~60 concurrent 8K-context requests."

---

## Part 4 - Open Lab / Catch-up Time
### Use This Time For

1. **Catch up** on any concepts still fuzzy
2. **Extra practice** - recalculate memory budgets for different scenarios
3. **Ask oxtutor** to re-explain anything still unclear

### Recommended Practice Scenarios

Try these memory budget calculations:

| GPU | Model | Context | Batch | FP16? FP8? |
|-----|-------|---------|-------|------------|
| H100 (80GB) | 8B | 4K | 8 | ? |
| H100 (80GB) | 8B | 128K | 4 | ? |
| H100 (80GB) | 70B | 8K | 2 | ? |
| 8×H100 | 70B | 32K | 8 | ? |

### Stuck?

The KV cache and quantization sensitivity ladder (weights → KV → activations → attention) are the highest-leverage concepts of the entire phase. Ask **oxtutor** to re-explain.

---

## Part 5 - Self-Check Before Week 4
### Can You Explain These From Memory?

- [ ] Why is prefill compute-bound and decode memory-bound?
- [ ] What's the formula for KV cache size?
- [ ] How does FlashAttention reduce HBM traffic?
- [ ] Why does PagedAttention enable more concurrent users?
- [ ] What's the quantization sensitivity ladder?
- [ ] Why is FP8 preferred over INT8 for LLMs?
- [ ] What's the combined speedup from FlashAttention + PagedAttention + FP8 quantization?

### The Key Numbers to Memorize

| Metric | Value |
|--------|-------|
| H100 bandwidth | 3.35 TB/s |
| KV per token (8B, GQA) | 128 KB |
| FP16 → FP8 speedup | ~2× memory, ~2× compute |
| Combined optimization speedup | ~20× vs naive |

---

## Part 6 - Wrap-up & Connection
### Week 3 Summary

You've now mastered:
- **Prefill vs Decode** - the two phases of LLM inference with different bottlenecks
- **KV Cache** - the central resource that grows with context
- **FlashAttention** - lossless kernel optimization (5-20× speedup)
- **PagedAttention** - virtual memory for KV cache (~90% utilization)
- **Quantization** - lossy but massive (4× throughput at 0.1-0.3 MMLU cost)

### Connect Forward

Week 4 builds on this foundation:
- Batching strategies (static, dynamic, continuous)
- Prefix caching
- Speculative decoding

> **The KV cache is the resource you spend most of Week 4 trying to fit and Week 5 trying to budget.**

---

## Part 7 - Wrap-up & Connection
### Pre-read for Monday (Week 4, Day 16 · Tensor & Pipeline Parallelism)

**Resource:** <a href="https://huggingface.co/docs/transformers/v4.15.0/parallelism" target="_blank" rel="noopener">Hugging Face - Model Parallelism</a> (read the Tensor Parallel section). Alternative: <a href="https://lilianweng.github.io/posts/2023-01-10-inference-optimization/" target="_blank" rel="noopener">Lilian Weng - Transformer Inference Optimization</a>.

**Reflection questions:**

1. Of {KV cache, FlashAttention, quantization}: which one would you teach a peer first? Why?
2. What's still confusing about prefill vs decode?
3. What's the *one* number you'd put on a wall-poster for Week 3?

---

## What Today Is For

You've covered prefill/decode, KV cache math, FlashAttention/PagedAttention, and quantization. Friday is the day to:

1. **Pass the knowledge check.** [Take the canonical knowledge check](knowledge-check.md): prefill/decode, KV cache math, FP8/INT4 sizing.
2. **Submit the memory budget calculator assignment**: given GPU (80 GB), model, context length, batch size → does it fit?
3. **Open-ended lab time.** Catch up; ask oxtutor to re-explain anything still fuzzy.

---

## Stuck?

Ask **oxtutor**: share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
