# Day 15 (Fri) · Week 3 Consolidation

> **Goal of the day:** consolidate attention + KV cache + quantization. No new content.

## What today is for

You've covered prefill/decode, KV cache math, FlashAttention/PagedAttention, and quantization. Friday is the day to:

1. **Pass the knowledge check.** [Take the canonical knowledge check](knowledge-check.html) — prefill/decode, KV cache math, FP8/INT4 sizing. Item bank: Flashcards Days 11–14.
2. **Submit the memory budget calculator assignment** — given GPU (80 GB), model, context length, batch size → does it fit? What if you quantize to FP8?
3. **Open-ended lab time.** Catch up; ask oxtutor to re-explain anything still fuzzy; generate extra practice.

## Self-check before Week 4

Prefill = compute-bound. Decode = memory-bound. The KV cache is the resource you spend most of Week 4 trying to fit and Week 5 trying to budget.

## Stuck?

Ask **oxtutor** to re-explain — the KV cache and the quantization sensitivity ladder (weights → activations → KV → attention) are the highest-leverage concepts of the entire phase.
