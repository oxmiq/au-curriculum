# Week 4 · Inference Engineering — Scaling & Stacks

> **Goal of the week:** from one GPU to many GPUs. From theory to real software.
> **Source material:** [`Inference Engineering/`](../../../planning/source-material/Inference%20Engineering/) — Study Guide §A.5, Pre-Lecture Reading §Days 16–19, Problem Sets, Worksheets Appendix C.

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 16 (Mon) | Tensor Parallelism | Reader 6 — parallelism overview (~20 min) | [Day 1 · Tensor Parallelism](module-1/index.md) |
| 17 (Tue) | Pipeline & Expert Parallelism | Reader 6 — PP + MoE (~20 min) | [Day 2 · Pipeline Expert Parallelism](module-2/index.md) |
| 18 (Wed) | Speculative Decoding | Reader 8 — advanced serving (~15 min) | [Day 3 · Speculative Decoding](module-3/index.md) |
| 19 (Thu) | Serving Engines & Continuous Batching | Reader 9 — production engines (~15 min) | [Day 4 · Serving Engines](module-4/index.md) |
| 20 (Fri) | **Consolidation** — serving-system design | — | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **Canonical quiz:** parallelism (TP/PP/EP), speculation, batching, engines. Item bank: Problem Sets Day 19/20 ★.
- **[Assignment](module-1/assignment.md)** — **Design a serving system.** Given 70B model, 8×H100, P99 < 500 ms, throughput 50 req/s → what config? Rubric: Worksheets Appendix C.

## Big-picture connect

Week 4 turns Week 3's bottleneck knowledge into engineering decisions: *which* parallelism, *which* engine, *which* batching mode.

## Stuck?

Ask **oxtutor** to re-explain — the TP-vs-PP-vs-EP decision tree is the most-asked interview question of the entire program.
