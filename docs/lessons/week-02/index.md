# Week 2 · Inference Engineering — The GPU & Memory

> **Goal of the week:** build the hardware mental model. Understand *where* inference happens and *why* it's shaped the way it is.

<!-- AUTO-GEN:CARD-GRID:START -->
<div class="ox-card-grid" markdown="0">
  <a class="ox-card" href="module-1/" style="--i:6">
    {status:week-02/module-1}
    <span class="ox-card__eyebrow">Day 6</span>
    <h3 class="ox-card__title">What Happens When You Send a Prompt</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-2/" style="--i:7">
    {status:week-02/module-2}
    <span class="ox-card__eyebrow">Day 7</span>
    <h3 class="ox-card__title">Meet the GPU</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-3/" style="--i:8">
    {status:week-02/module-3}
    <span class="ox-card__eyebrow">Day 8</span>
    <h3 class="ox-card__title">Memory Is the Bottleneck</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-4/" style="--i:9">
    {status:week-02/module-4}
    <span class="ox-card__eyebrow">Day 9</span>
    <h3 class="ox-card__title">Compute-Bound vs Memory-Bound</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-5/" style="--i:10">
    {status:week-02/module-5}
    <span class="ox-card__eyebrow">Day 10</span>
    <h3 class="ox-card__title">Consolidation</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
</div>
<!-- AUTO-GEN:CARD-GRID:END -->

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 6 (Mon) | What Happens When You Send a Prompt | Reader 1 — AI in production | [Day 1 · Prompt Pipeline](module-1/index.md) |
| 7 (Tue) | Meet the GPU | Reader 5 — Computer architecture | [Day 2 · Meet The Gpu](module-2/index.md) |
| 8 (Wed) | Memory Is the Bottleneck | Reader 5 memory subsection + Study Guide §A.3 | [Day 3 · Memory Bottleneck](module-3/index.md) |
| 9 (Thu) | Compute-Bound vs Memory-Bound | Reader 4 + Study Guide §A.5 roofline | [Day 4 · Compute Vs Memory Bound](module-4/index.md) |
| 10 (Fri) | **Consolidation** — Feynman teach-back + quiz | — | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **Canonical [quiz](module-5/knowledge-check.md):** GPU anatomy + memory hierarchy + bottleneck classification. Drawn from Flashcards Days 6–9.
- **[Assignment](module-1/assignment.md)** — Feynman teach-back: explain one of {bandwidth, FLOPs, roofline, memory hierarchy} as if to a peer who missed the week.

## Big-picture connect

By Friday you can answer: *"Why is most LLM inference time spent moving data, not computing?"* That single insight unlocks Weeks 3–5.

## Stuck?

Ask **oxtutor** to re-explain any concept; the glossary entries on *bandwidth*, *FLOPs*, *roofline*, and *memory hierarchy* are the canonical definitions.
