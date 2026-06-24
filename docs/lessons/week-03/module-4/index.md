# Day 14 · Quantization

> **Concept of the day:** fewer bits → less data to move → faster decode. FP16 → FP8 → FP4 progression. **Float > int** (dynamic range). Sensitivity ladder: weights → activations → KV → attention.<br>
> **Pre-reading:** "What is quantization?" — Pre-Lecture Reading **Reader 7** (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 — Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 14 · Quantization</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-03/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts: The Precision Ladder | 20 min |
| Part 3 | Deep Dive: Float vs Int & Sensitivity Ladder | 20 min |
| Part 4 | Hands-On: Weight Memory Calculations | 20 min |
| Part 5 | Hands-On: Decode Latency at Different Precisions | 25 min |
| Part 6 | Hands-On: Combined Memory Budget | 20 min |
| Part 7 | Wrap-up & Connection | 5 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: "What is quantization?" — Pre-Lecture Reading **Reader 7** (~20 min).

### Quick Self-Check

Answer these questions from memory:
1. FP16 = ___ bytes. FP8 = ___. INT4 = ___.
2. Why does *float* (FP) have an advantage over *int* (INT) at the same bit count?
3. Which is more sensitive to quantization: weights or activations?
4. What's the typical quality cost of going FP16 → FP8 weights?
5. If you quantize weights from FP16 to FP8 on a memory-bound kernel, what's the rough speedup ceiling?

---

## Part 2 — Core Concepts — The Precision Ladder · 20 min
### Reading — The Numerical Precision Spectrum

Quantization is the *single biggest lever* for decode latency. Halving the bits roughly halves the HBM traffic — and decode is memory-bound, so that roughly halves the time per token.

| Precision | Bytes | Dynamic Range | Notes |
|-----------|-------|---------------|-------|
| FP32 | 4 | Huge | Training default |
| FP16 / BF16 | 2 | Wide (BF16 wider) | Standard inference baseline |
| FP8 (E4M3 / E5M2) | 1 | Medium | Hopper+ Tensor Cores native |
| INT8 | 1 | Symmetric ±127 | Mature, lossless-ish for many models |
| FP4 / NF4 | 0.5 | Small | Aggressive but works for many weights |
| INT4 | 0.5 | Symmetric ±7 | Heavy quantization, often with group scale |

### Why Quantization Works

**Compute-bound (Prefill):** Lower precision = 2× FLOPS on Tensor Cores (H100 FP8 = ~2× FP16 throughput)

**Memory-bound (Decode):** Half as many bytes per value = effectively 2× memory bandwidth

> **Empirically, dropping one precision level gives ~30-50% better LLM performance** (overhead eats some of the theoretical 2×).

### Source Material Reference

From **Inference Engineering Study Guide §5.1**: "Quantization lowers the numeric precision of weights to access more compute and reduce memory traffic. Wins both bottlenecks: prefill (compute-bound) gets 2× FLOPS; decode (memory-bound) gets 2× effective bandwidth."

---

## Part 3 — Deep Dive — Float vs Int & Sensitivity Ladder · 20 min
### Float vs Int — Why Float Usually Wins

**Floating-point formats** have a sign bit, exponent, and mantissa — giving **dynamic range** to represent very large and very small values. **Integer formats** have no exponent — they represent uniformly spaced values.

> **Neural network activations are heavy-tailed** (outliers in every layer). Float handles outliers gracefully; int either clips them or wastes range.

| Format | Spacing | Handles Outliers? | Best For |
|--------|---------|-------------------|----------|
| FP8 | Logarithmic (wider near zero) | ✅ Yes | LLM inference (sweet spot) |
| INT8 | Uniform | ❌ No | Simple tasks, embeddings |

> **Rule of thumb:** At the same bit count, **FP8 > INT8** in quality for LLM weights, especially with outlier features.

### The Sensitivity Ladder (Least → Most Sensitive)

From **Inference Engineering Study Guide §5.1**:

1. **Weights** — *least sensitive*. Quantize aggressively (FP8, INT8, INT4) with small quality loss. Biggest decode win.
2. **KV cache** — FP8 KV is now common — halves cache size *and* halves the bandwidth to read it.
3. **Activations** — more sensitive; outliers can blow up. Usually FP8 OK with calibration.
4. **Attention output / softmax** — *most sensitive*; usually kept in higher precision. Errors accumulate over thousands of tokens.

> **Recommended starter:** FP8 weights, FP16 activations, FP8 KV cache — the modern Hopper sweet spot.

---

## Part 4 — Hands-On — Weight Memory Calculations · 20 min
### Exercise 1: Llama-3-8B Weight Memory (10 min)

Calculate weight memory for Llama-3-8B at different precisions:

| Precision | Bytes/Param | Total Memory | vs FP16 |
|-----------|-------------|--------------|---------|
| FP16 | 2 | ? | 100% |
| FP8 | 1 | ? | ?% |
| INT4 | 0.5 | ? | ?% |

**Answers:**
- FP16: 8B × 2 = **16 GB**
- FP8: 8B × 1 = **8 GB** (50% of FP16)
- INT4: 8B × 0.5 = **4 GB** (25% of FP16)

### Exercise 2: Savings Visualization (10 min)

If you have an 80 GB H100:
- FP16 weights + KV headroom = ~64 GB for model, 16 GB for KV
- FP8 weights + FP8 KV = 8 GB + 8 GB = **16 GB total** for model+KV
- **That's 4× more headroom for batching!**

---

## Part 5 — Hands-On — Decode Latency at Different Precisions · 25 min
### Exercise: 70B Model Decode Time Floor (25 min)

**Given:**
- Llama-3-70B: 140 GB FP16 weights
- 8×H100 with NVLink (per-GPU shard = 17.5 GB)
- H100 bandwidth: 3.35 TB/s

**Question 1:** At FP16 (17.5 GB per GPU), what's the decode time floor per token?
- Time = weight_bytes / bandwidth
- 17.5 GB / 3.35 TB/s = 17.5 × 10⁹ / 3.35 × 10¹² s ≈ **5.2 ms/token**

**Question 2:** At FP8 (8.75 GB per GPU), what's the decode time floor?
- 8.75 GB / 3.35 TB/s ≈ **2.6 ms/token**

**Question 3:** What's the speedup?
- 5.2 / 2.6 ≈ **2× faster**

**Question 4:** Including H100's FP8 Tensor Core boost (~2× more FLOPS), what's the combined speedup?
- Memory: 2×
- Compute: 2×
- **Combined: ~4× decode throughput** (typical实测: 3-4×)

### Source Material Reference

From **Inference Engineering Study Guide §A.5**: "FP8 vs FP16 throughput on H100: ~4× decode throughput, with typical 0.1–0.3 point MMLU regression. This is why FP8 is the default for serious deployments in 2026."

---

## Part 6 — Hands-On — Combined Memory Budget · 20 min
### Exercise: Full System Memory Budget (20 min)

**Scenario:** 70B model on 8×H100 (80 GB each = 640 GB total)

**At FP8 weights + FP8 KV + FP8 activations:**

| Component | Calculation | Size |
|-----------|--------------|------|
| Weights (FP8) | 70B × 1 | 70 GB |
| KV cache (FP8, 8 users, 4K context) | 8 × 4K × 128 KB | 4 GB |
| Activations (FP8, estimate) | ~10 GB | 10 GB |
| **Total** | | **~84 GB** |

**Question:** At 640 GB across 8 GPUs, how many concurrent users can you support?

- Per-GPU: 640 / 8 = 80 GB
- After weights (70/8 = 8.75 GB): 80 - 8.75 = 71.25 GB per GPU for KV + activations
- At 0.5 GB per user: ~140 concurrent 4K-context users!

### When NOT to Quantize

Pair discussion (10 min):
- Small batch + abundant memory + quality-critical task
- Early-stage eval where you're still measuring quality
- Models with known quantization sensitivity (some architectures)

---

## Part 7 — Wrap-up & Connection · 5 min
### Self-Check

Can you explain these from memory?
- [ ] What's the difference between FP8 and INT8? Why prefer FP8 for LLMs?
- [ ] What's the sensitivity ladder for quantization (least → most sensitive)?
- [ ] Why does decode benefit more from quantization than prefill?
- [ ] What's the default precision combination for modern deployments?

### The Key Insight

> **Quantization is the lossy-but-massive lever. It changes the numbers, so you measure quality. But the memory/compute savings are enormous: ~4× throughput on H100 at ~0.1-0.3 MMLU regression.**

### Connect Forward

Friday: consolidation. We build the **memory budget calculator** — given GPU, model, context, batch → does it fit, and what does it cost at each precision level? Then [the canonical quiz](knowledge-check.html).

---

## Pre-read for Friday (Day 15 · Consolidation)

- **Resource:** None. Bring your Day 12 KV math and Day 14 quantization math.
- **Reflection questions:**
  1. Of {KV cache, FlashAttention, quantization} — which one would you teach a peer first? Why?
  2. What's still confusing about prefill vs decode? Write the question.
  3. What's the *one* number you'd put on a wall-poster for Week 3?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
