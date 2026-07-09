# Week 4 · Inference Engineering — Scaling & Stacks

> **Goal of the week:** from one GPU to many GPUs. From theory to real software.

<!-- AUTO-GEN:CARD-GRID:START -->
<div class="ox-card-grid" markdown="0">
  <a class="ox-card" href="module-1/" style="--i:16">
    {status:week-04/module-1}
    <span class="ox-card__eyebrow">Day 16</span>
    <h3 class="ox-card__title">Multi-GPU Parallelism</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-2/" style="--i:17">
    {status:week-04/module-2}
    <span class="ox-card__eyebrow">Day 17</span>
    <h3 class="ox-card__title">Pipeline Parallelism + MoE</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-3/" style="--i:18">
    {status:week-04/module-3}
    <span class="ox-card__eyebrow">Day 18</span>
    <h3 class="ox-card__title">Speculative Decoding</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-4/" style="--i:19">
    {status:week-04/module-4}
    <span class="ox-card__eyebrow">Day 19</span>
    <h3 class="ox-card__title">vLLM Introduction</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-5/" style="--i:20">
    {status:week-04/module-5}
    <span class="ox-card__eyebrow">Day 20</span>
    <h3 class="ox-card__title">Consolidation</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
</div>
<!-- AUTO-GEN:CARD-GRID:END -->

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 16 (Mon) | Tensor Parallelism | Reader 6 — parallelism overview | [Day 1 · Tensor Parallelism](module-1/index.md) |
| 17 (Tue) | Pipeline & Expert Parallelism | Reader 6 — PP + MoE | [Day 2 · Pipeline Expert Parallelism](module-2/index.md) |
| 18 (Wed) | Speculative Decoding | Reader 8 — advanced serving | [Day 3 · Speculative Decoding](module-3/index.md) |
| 19 (Thu) | Serving Engines & Continuous Batching | Reader 9 — production engines | [Day 4 · Serving Engines](module-4/index.md) |
| 20 (Fri) | **Consolidation** — serving-system design | — | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **Canonical quiz:** parallelism (TP/PP/EP), speculation, batching, engines. Item bank: Problem Sets Day 19/20 ★.
- **[Assignment](module-1/assignment.md)** — **Design a serving system.** Given 70B model, 8×H100, P99 < 500 ms, throughput 50 req/s → what config? Rubric: Worksheets Appendix C.

## Big-picture connect

Week 4 turns Week 3's bottleneck knowledge into engineering decisions: *which* parallelism, *which* engine, *which* batching mode.

## Stuck?

Ask **oxtutor** to re-explain — the TP-vs-PP-vs-EP decision tree is the most-asked interview question of the entire program.
