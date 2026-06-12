# Day 14 · Quantization

> **Concept of the day:** fewer bits → less data to move → faster decode. FP16 → FP8 → FP4 progression. **Float > int** (dynamic range). Sensitivity ladder: weights → activations → KV → attention.
> **Pre-reading:** "What is quantization?" — Pre-Lecture Reading **Reader 7** (~20 min).
> **Source:** [Study Guide §A.5 quantization](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Glossary entries: FP16, FP8, INT4](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Glossary.md).

---

## Why this matters

Quantization is the *single biggest lever* for decode latency. Halving the bits roughly halves the HBM traffic — and decode is memory-bound, so that roughly halves the time per token. But unlike FlashAttention, quantization **changes the numbers** — so you have to measure quality (Week 5 Day 23).

## Readiness check

1. FP16 = ___ bytes. FP8 = ___. INT4 = ___.
2. Why does *float* (FP) have an advantage over *int* (INT) at the same bit count?
3. Which is more sensitive to quantization: weights or activations?
4. What's the typical quality cost of going FP16 → FP8 weights?
5. If you quantize weights from FP16 to FP8 on a memory-bound kernel, what's the rough speedup ceiling?

## Core concept — the precision ladder

| Precision | Bytes | Dynamic range | Notes |
|---|---|---|---|
| FP32 | 4 | huge | Training default |
| FP16 / BF16 | 2 | wide (BF16 wider) | Standard inference baseline |
| FP8 (E4M3 / E5M2) | 1 | medium | Hopper+ Tensor Cores native |
| INT8 | 1 | symmetric ±127 | Mature, lossless-ish for many models |
| FP4 / NF4 | 0.5 | small | Aggressive but works for many weights |
| INT4 | 0.5 | symmetric ±7 | Heavy quantization, often w/ group scale |

### Float vs int — why float usually wins

Floats spread precision across magnitudes (more precision near zero). Ints quantize uniformly. Neural network activations are heavy-tailed (outliers in every layer) → float handles outliers gracefully; int either clips them or wastes range.

> **Rule of thumb:** at the same bit count, **FP8 > INT8** in quality for LLM weights, especially with outlier features.

### The sensitivity ladder (least → most sensitive to quantization)

1. **Weights.** Quantize aggressively (FP8, INT8, INT4) with small quality loss. Biggest decode win.
2. **KV cache.** FP8 KV is now common — halves cache size *and* halves the bandwidth to read it.
3. **Activations.** More sensitive — outliers can blow up. Usually FP8 ok with calibration.
4. **Attention output / softmax.** Most sensitive — usually kept in higher precision.

### Why decode benefits most

Decode for a single user reads all weights once per token (memory-bound). Going FP16 → FP8 means **half the bytes per token**:

- 16 GB FP16 weights → 8 GB FP8.
- At 3.35 TB/s, decode floor: 4.8 ms/token → 2.4 ms/token.
- ~2× faster, ~2× more tokens per second.

Prefill, being compute-bound, also speeds up — but the win is via faster Tensor Core throughput at lower precision (H100 FP8 is ~2× FP16 throughput) rather than via memory.

### Quality measurement (preview of Week 5 Day 23)

Quantization is **lossy**. Standard practice:

- **Perplexity delta** on a held-out set — coarse, but quick.
- **Task evals** — MMLU, code-completion pass rate, etc.
- **Side-by-side human eval** on representative prompts.
- **Sanity prompts** — facts, refusal behaviour, format compliance.

If quality is acceptable at FP8 weights + FP8 KV, you ship FP8.

## Practice (90 min)

1. (15 min) Calculate weight memory for Llama-3-8B at FP16, FP8, INT4. How much HBM saved?
2. (20 min) Calculate decode-time floor for Llama-3-70B (140 GB FP16 weights) on 8×H100 with NVLink, at FP16 vs FP8 weights (per-GPU shard = 17.5 GB vs 8.75 GB).
3. (25 min) Lab: combine. Memory budget for a 70B model on 8×H100 at FP8 weights + FP8 KV. Max context length at batch=8?
4. (20 min) Pair discussion: when would you *not* quantize? (Hint: small batch + abundant memory + quality-critical task.)
5. (10 min) Write a one-sentence rule for choosing between FP8 weights and INT4 weights.

## Wrap-up

Cohort agrees on a *default starting point* for new model deployments. Most settle on **FP8 weights, FP16 activations, FP8 KV cache** — the modern Hopper sweet spot.

## Connect forward

Friday: consolidation. We build the **memory budget calculator** — given GPU, model, context, batch → does it fit, and what does it cost at each precision level? Then [the canonical quiz](knowledge-check.html).

---

## Pre-read for Friday (Day 15 · Consolidation)

- **Resource:** None. Bring your Day 12 KV math and Day 14 quantization math.
- **Reflection questions:**
  1. Of {KV cache, FlashAttention, quantization} — which one would you teach a peer first? Why?
  2. What's still confusing about prefill vs decode? Write the question.
  3. What's the *one* number you'd put on a wall-poster for Week 3?
