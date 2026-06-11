# Week 2 · Inference Engineering — The GPU & Memory

> **Goal of the week:** build the hardware mental model. Understand *where* inference happens and *why* it's shaped the way it is.
> **Source material:** [`Inference Engineering/`](../../../planning/source-material/Inference%20Engineering/) — Study Guide, Pre-Lecture Reading, Lecture Slides, Problem Sets, Flashcards, Glossary.

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 6 (Mon) | What Happens When You Send a Prompt | Reader 1 — AI in production (~15 min) | [01-prompt-pipeline.md](01-prompt-pipeline.md) |
| 7 (Tue) | Meet the GPU | Reader 5 — Computer architecture (~10 min) | [02-meet-the-gpu.md](02-meet-the-gpu.md) |
| 8 (Wed) | Memory Is the Bottleneck | Reader 5 memory subsection + Study Guide §A.3 (~20 min) | [03-memory-bottleneck.md](03-memory-bottleneck.md) |
| 9 (Thu) | Compute-Bound vs Memory-Bound | Reader 4 + Study Guide §A.5 roofline (~15 min) | [04-compute-vs-memory-bound.md](04-compute-vs-memory-bound.md) |
| 10 (Fri) | **Consolidation** — Feynman teach-back + quiz | — | [quiz.html](quiz.html) |

## Friday — the bar

- **Canonical [quiz](quiz.html):** GPU anatomy + memory hierarchy + bottleneck classification. Drawn from Flashcards Days 6–9.
- **[Assignment](assignment.md)** — Feynman teach-back: explain one of {bandwidth, FLOPs, roofline, memory hierarchy} as if to a peer who missed the week.

## Big-picture connect

By Friday you can answer: *"Why is most LLM inference time spent moving data, not computing?"* That single insight unlocks Weeks 3–5.

## Stuck?

Ask **oxcode** to re-explain any concept; the glossary entries on *bandwidth*, *FLOPs*, *roofline*, and *memory hierarchy* are the canonical definitions.
