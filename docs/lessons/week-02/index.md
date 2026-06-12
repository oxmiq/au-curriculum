# Week 2 · Inference Engineering — The GPU & Memory

> **Goal of the week:** build the hardware mental model. Understand *where* inference happens and *why* it's shaped the way it is.
> **Source material:** [`Inference Engineering/`](../../../planning/source-material/Inference%20Engineering/) — Study Guide, Pre-Lecture Reading, Lecture Slides, Problem Sets, Flashcards, Glossary.

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 6 (Mon) | What Happens When You Send a Prompt | Reader 1 — AI in production (~15 min) | [Day 1 · Prompt Pipeline](module-1/index.md) |
| 7 (Tue) | Meet the GPU | Reader 5 — Computer architecture (~10 min) | [Day 2 · Meet The Gpu](module-2/index.md) |
| 8 (Wed) | Memory Is the Bottleneck | Reader 5 memory subsection + Study Guide §A.3 (~20 min) | [Day 3 · Memory Bottleneck](module-3/index.md) |
| 9 (Thu) | Compute-Bound vs Memory-Bound | Reader 4 + Study Guide §A.5 roofline (~15 min) | [Day 4 · Compute Vs Memory Bound](module-4/index.md) |
| 10 (Fri) | **Consolidation** — Feynman teach-back + quiz | — | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **Canonical [quiz](module-5/knowledge-check.html):** GPU anatomy + memory hierarchy + bottleneck classification. Drawn from Flashcards Days 6–9.
- **[Assignment](module-1/assignment.md)** — Feynman teach-back: explain one of {bandwidth, FLOPs, roofline, memory hierarchy} as if to a peer who missed the week.

## Big-picture connect

By Friday you can answer: *"Why is most LLM inference time spent moving data, not computing?"* That single insight unlocks Weeks 3–5.

## Stuck?

Ask **oxtutor** to re-explain any concept; the glossary entries on *bandwidth*, *FLOPs*, *roofline*, and *memory hierarchy* are the canonical definitions.
