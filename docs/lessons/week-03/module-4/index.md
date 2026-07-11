# Day 14 · Quantization

> **Concept of the day:** fewer bits → less data to move → faster decode. FP16 → FP8 → FP4 progression. **Float > int** (dynamic range). Sensitivity ladder: weights → activations → KV → attention.<br>
> **Pre-reading:** "What is quantization?" — <a href="https://huggingface.co/docs/optimum/concept_guides/quantization" target="_blank" rel="noopener">Hugging Face — Quantization</a>.

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
    {status:week-03/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: The Precision Ladder |
| Part 3 | Deep Dive: Float vs Int & Sensitivity Ladder |
| Part 4 | Hands-On: Weight Memory Calculations |
| Part 5 | Hands-On: Decode Latency at Different Precisions |
| Part 6 | Hands-On: Combined Memory Budget |
| Part 7 | Wrap-up & Connection |

---

## Part 1 — Pre-Reading Review
### Before You Start

You should have already read: "What is quantization?" — Pre-Lecture Reading **Reader 7**.

### Quick Self-Check

Answer these questions from memory:

1. FP16 = ___ bytes. FP8 = ___. INT4 = ___.
2. Why does *float* (FP) have an advantage over *int* (INT) at the same bit count?
3. Which is more sensitive to quantization: weights or activations?
4. What's the typical quality cost of going FP16 → FP8 weights?
5. If you quantize weights from FP16 to FP8 on a memory-bound kernel, what's the rough speedup ceiling?

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m4-readiness" data-kind="readiness" data-draw="5" data-source="Hugging Face — Quantization">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "How many bytes is FP16?",
    "options": [
      "1 byte",
      "2 bytes",
      "4 bytes",
      "8 bytes"
    ],
    "answer": 1,
    "explain": "FP16 is 16 bits = 2 bytes. It provides sufficient precision for most deep learning while halving memory vs FP32 (4 bytes)."
  },
  {
    "stem": "Why does float (FP) have an advantage over integer (INT) at the same bit count?",
    "options": [
      "Integers are faster",
      "Float has a dynamic range — it can represent both very small and very large values",
      "Integers are more accurate",
      "There is no difference"
    ],
    "answer": 1,
    "explain": "Float has a dynamic range through its exponent. INT is fixed-range. At the same bit count, FP can represent orders of magnitude difference in values — crucial for neural network weights and activations."
  },
  {
    "stem": "Which is more sensitive to quantization: weights or activations?",
    "options": [
      "Weights — they change the most",
      "Activations — they vary more dynamically at runtime",
      "They are equally sensitive",
      "Neither are sensitive"
    ],
    "answer": 1,
    "explain": "Activations are more sensitive to quantization because they vary dynamically at runtime based on input. Weights are static. This is why many methods quantize weights aggressively but keep activations in higher precision."
  },
  {
    "stem": "What is the typical quality cost of going FP16 → FP8 weights?",
    "options": [
      "10-20% quality loss",
      "<1% quality loss (nearly lossless)",
      "50% quality loss",
      "No quality change"
    ],
    "answer": 1,
    "explain": "Going from FP16 to FP8 weights typically costs <1% quality loss. This makes it nearly lossless. The key insight is that weights are static — easier to quantize than dynamic activations."
  },
  {
    "stem": "If you quantize weights from FP16 to FP8 on a memory-bound kernel, what's the rough speedup ceiling?",
    "options": [
      "2x",
      "~2x (memory bandwidth doubles, so speed roughly doubles)",
      "10x",
      "No speedup"
    ],
    "answer": 1,
    "explain": "FP8 uses half the bytes of FP16, so memory bandwidth roughly doubles. For memory-bound kernels, speedup is ~2x. This is the theoretical ceiling — actual speedup may be slightly less due to overhead."
  },
  {
    "stem": "What is the 'sensitivity ladder' for quantization (from most to least sensitive)?",
    "options": [
      "Weights > Activations > KV > Attention",
      "Activations > KV > Attention > Weights",
      "KV > Attention > Activations > Weights",
      "Attention > Weights > KV > Activations"
    ],
    "answer": 1,
    "explain": "The sensitivity ladder (most to least sensitive): Activations > KV > Attention > Weights. This guides quantization strategy: quantize weights aggressively, keep activations higher precision."
  },
  {
    "stem": "What does quantization achieve for decode-phase inference?",
    "options": [
      "Faster prefill",
      "Less data to move from HBM — directly reduces decode latency",
      "Higher accuracy",
      "Better model quality"
    ],
    "answer": 1,
    "explain": "Quantization reduces the precision of weights (and sometimes activations), so less data needs to be moved from HBM during decode. Since decode is memory-bound, this directly reduces latency."
  },
  {
    "stem": "What is the difference between static and dynamic quantization?",
    "options": [
      "Static quantization quantizes weights only; dynamic quantizes weights and activations at runtime",
      "There is no difference",
      "Dynamic is always better",
      "Static is always better"
    ],
    "answer": 0,
    "explain": "Static quantization: quantize weights offline (at low precision), activations stay FP16. Dynamic quantization: quantize weights offline, quantize activations at runtime. Dynamic gives better accuracy but more overhead."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts — The Precision Ladder
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

## Part 3 — Deep Dive — Float vs Int & Sensitivity Ladder
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

## Part 4 — Hands-On — Weight Memory Calculations
### Exercise 1: Llama-3-8B Weight Memory

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

### Exercise 2: Savings Visualization

If you have an 80 GB H100:
- FP16 weights + KV headroom = ~64 GB for model, 16 GB for KV
- FP8 weights + FP8 KV = 8 GB + 8 GB = **16 GB total** for model+KV
- **That's 4× more headroom for batching!**

---

## Part 5 — Hands-On — Decode Latency at Different Precisions
### Exercise: 70B Model Decode Time Floor

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

## Part 6 — Hands-On — Combined Memory Budget
### Exercise: Full System Memory Budget

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

Pair discussion:
- Small batch + abundant memory + quality-critical task
- Early-stage eval where you're still measuring quality
- Models with known quantization sensitivity (some architectures)

---

## Part 7 — Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 14 · Quantization">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Why is FP8 generally preferred over INT8 for LLM weight quantization?",
    "options": [
      "FP8 uses less memory than INT8",
      "FP8 has a floating-point exponent allowing it to represent a wider dynamic range, reducing quality loss on outlier activations compared to INT8's fixed-range integer representation",
      "FP8 is faster because it requires fewer multiplications",
      "FP8 is hardware-accelerated on all GPU architectures since 2018"
    ],
    "answer": 1,
    "explain": "INT8 maps values to 256 fixed integer levels, which clips outlier values. FP8 (e.g., E4M3 format) has a floating-point exponent that better handles the wide range of weight magnitudes in transformer layers. This makes FP8 less lossy for LLMs, which have outlier-prone activations."
  },
  {
    "stem": "In the quantization sensitivity ladder (least to most sensitive), which is the ordering?",
    "options": [
      "Activations are least sensitive; KV cache is most sensitive",
      "Weights are least sensitive; activations are most sensitive",
      "KV cache is least sensitive; weights are most sensitive",
      "All components are equally sensitive to quantization"
    ],
    "answer": 1,
    "explain": "The sensitivity ladder from least to most sensitive is approximately: weights < KV cache < activations. Weights are static and can be calibrated offline. Activations are computed dynamically per input and vary widely, making them hardest to quantize without accuracy loss."
  },
  {
    "stem": "Why does decode benefit more from weight quantization than prefill does?",
    "options": [
      "Decode uses different model layers than prefill",
      "Decode is memory-bound — quantization reduces bytes per weight, directly increasing effective bandwidth and TPS; prefill is compute-bound so bandwidth savings matter less",
      "Prefill is never run with quantized weights",
      "Quantization is only applied to the KV cache during decode"
    ],
    "answer": 1,
    "explain": "Decode's bottleneck is memory bandwidth (reading weights from HBM). Halving weight size (e.g., FP16 to INT8) roughly halves the bytes transferred and doubles effective bandwidth, directly increasing TPS. Prefill is compute-bound — bandwidth savings don't help as much."
  },
  {
    "stem": "Approximately how much memory footprint reduction does FP8 provide compared to FP16?",
    "options": [
      "2× reduction (FP8 = 1 byte vs FP16 = 2 bytes per parameter)",
      "4× reduction (FP8 = 0.5 bytes per parameter)",
      "8× reduction",
      "No reduction — FP8 is only a compute optimization"
    ],
    "answer": 0,
    "explain": "FP8 = 1 byte per parameter; FP16 = 2 bytes per parameter. FP8 gives a 2× memory reduction vs FP16, the same as INT8. INT4 gives 4× vs FP16 (0.5 bytes per param). The memory savings directly reduce KV cache and weight footprints."
  },
  {
    "stem": "What is the typical quality cost of FP8 quantization on benchmarks like MMLU?",
    "options": [
      "Greater than 10 percentage points — noticeable degradation",
      "Around 5 percentage points — significant but acceptable",
      "Around 0.1–0.3 percentage points — negligible loss for ~2× throughput gain",
      "Zero — FP8 is perfectly lossless for all models"
    ],
    "answer": 2,
    "explain": "Well-calibrated FP8 quantization typically costs ~0.1–0.3 MMLU points compared to FP16 on modern LLMs. This is an excellent tradeoff: roughly 2× throughput improvement for less than 0.5% quality degradation. However, some models are more sensitive — always measure before deploying."
  },
  {
    "stem": "When should you avoid aggressive quantization (e.g., INT4)?",
    "options": [
      "When running on H100s, which do not support INT4",
      "When memory is abundant, quality requirements are high, or the model has known quantization sensitivity",
      "When running batch sizes larger than 32",
      "When serving more than 100 requests per second"
    ],
    "answer": 1,
    "explain": "The lesson notes: 'When NOT to use: small batch + abundant memory + quality-critical task; early-stage eval where you're still measuring quality; models with known quantization sensitivity.' INT4 is more aggressive — use it for throughput-critical deployments where you've validated quality on your specific workload."
  }
]
</script>
</div>

### The Key Insight

> **Quantization is the lossy-but-massive lever. It changes the numbers, so you measure quality. But the memory/compute savings are enormous: ~4× throughput on H100 at ~0.1-0.3 MMLU regression.**

### Connect Forward

Friday: consolidation. We build the **memory budget calculator** — given GPU, model, context, batch → does it fit, and what does it cost at each precision level? Then [the canonical quiz](knowledge-check.md).

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
