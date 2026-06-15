# Day 15 (Fri) · Week 3 Consolidation

> **Goal of the day:** consolidate attention + KV cache + quantization. No new content.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 — Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 15 · Consolidation</span>
    <span class="sep">·</span>
    <span class="duration">Friday · review &amp; wrap</span>
    {status:week-03/module-5}
  </div>
  <div class="ox-lesson-header__cta">
    <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
    <a class="md-button md-button--primary" href="knowledge-check.html">Knowledge check</a>
    <a class="md-button" href="assignment.md">Assignment</a>
    <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## What today is for

You've covered prefill/decode, KV cache math, FlashAttention/PagedAttention, and quantization. Friday is the day to:

1. **Pass the knowledge check.** [Take the canonical knowledge check](knowledge-check.html) — prefill/decode, KV cache math, FP8/INT4 sizing. Item bank: Flashcards Days 11–14.
2. **Submit the memory budget calculator assignment** — given GPU (80 GB), model, context length, batch size → does it fit? What if you quantize to FP8?
3. **Open-ended lab time.** Catch up; ask oxtutor to re-explain anything still fuzzy; generate extra practice.

## Self-check before Week 4

Prefill = compute-bound. Decode = memory-bound. The KV cache is the resource you spend most of Week 4 trying to fit and Week 5 trying to budget.

## Stuck?

Ask **oxtutor** to re-explain — the KV cache and the quantization sensitivity ladder (weights → activations → KV → attention) are the highest-leverage concepts of the entire phase.
