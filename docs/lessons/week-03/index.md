# Week 3 · Inference Engineering — Attention & KV Cache

> **Goal of the week:** understand the central resource management problem of serving LLMs.

<!-- AUTO-GEN:CARD-GRID:START -->
<div class="ox-card-grid" markdown="0">
  <a class="ox-card" href="module-1/" style="--i:11">
    {status:week-03/module-1}
    <span class="ox-card__eyebrow">Day 11</span>
    <h3 class="ox-card__title">Prefill vs Decode</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-2/" style="--i:12">
    {status:week-03/module-2}
    <span class="ox-card__eyebrow">Day 12</span>
    <h3 class="ox-card__title">KV Cache</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-3/" style="--i:13">
    {status:week-03/module-3}
    <span class="ox-card__eyebrow">Day 13</span>
    <h3 class="ox-card__title">FlashAttention</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-4/" style="--i:14">
    {status:week-03/module-4}
    <span class="ox-card__eyebrow">Day 14</span>
    <h3 class="ox-card__title">Quantization</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-5/" style="--i:15">
    {status:week-03/module-5}
    <span class="ox-card__eyebrow">Day 15</span>
    <h3 class="ox-card__title">Consolidation</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
</div>
<!-- AUTO-GEN:CARD-GRID:END -->

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 11 (Mon) | Prefill and Decode | Reader 4 + Study Guide §A.2 | [Day 1 · Prefill And Decode](module-1/index.md) |
| 12 (Tue) | The KV Cache | Reader 4 + Study Guide §A.2 KV subsection | [Day 2 · Kv Cache](module-2/index.md) |
| 13 (Wed) | FlashAttention & PagedAttention | Reader 4 FlashAttention section | [Day 3 · Flash And Paged Attention](module-3/index.md) |
| 14 (Thu) | Quantization | Reader 7 — numerical precision | [Day 4 · Quantization](module-4/index.md) |
| 15 (Fri) | **Consolidation** — memory-budget calculator | — | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **Canonical quiz:** prefill/decode, KV cache math, FP8/INT4 sizing. Item bank: Flashcards Days 11–14.
- **[Assignment](module-1/assignment.md)** — **Memory budget calculator.** Given GPU (80 GB), model, context length, batch size → does it fit? What if you quantize to FP8? Worked example in Inference Engineering Worksheets.

## Big-picture connect

Prefill = compute-bound. Decode = memory-bound. The KV cache is the resource you spend most of Week 4 trying to fit and Week 5 trying to budget.

## Stuck?

Ask **oxtutor** to re-explain — the KV cache and quantization sensitivity ladder (weights → activations → KV → attention) are the highest-leverage concepts of the entire phase.
