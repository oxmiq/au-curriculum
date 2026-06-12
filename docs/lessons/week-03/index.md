# Week 3 · Inference Engineering — Attention & KV Cache

> **Goal of the week:** understand the central resource management problem of serving LLMs.
> **Source material:** [`Inference Engineering/`](../../../planning/source-material/Inference%20Engineering/) — Study Guide §A.2–A.4, Pre-Lecture Reading §Days 11–14, Problem Sets, Flashcards.

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 11 (Mon) | Prefill and Decode | Reader 4 + Study Guide §A.2 (~15 min) | [Day 1 · Prefill And Decode](module-1/index.md) |
| 12 (Tue) | The KV Cache | Reader 4 + Study Guide §A.2 KV subsection (~20 min) | [Day 2 · Kv Cache](module-2/index.md) |
| 13 (Wed) | FlashAttention & PagedAttention | Reader 4 FlashAttention section (~20 min) | [Day 3 · Flash And Paged Attention](module-3/index.md) |
| 14 (Thu) | Quantization | Reader 7 — numerical precision (~20 min) | [Day 4 · Quantization](module-4/index.md) |
| 15 (Fri) | **Consolidation** — memory-budget calculator | — | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **Canonical quiz:** prefill/decode, KV cache math, FP8/INT4 sizing. Item bank: Flashcards Days 11–14.
- **[Assignment](module-1/assignment.md)** — **Memory budget calculator.** Given GPU (80 GB), model, context length, batch size → does it fit? What if you quantize to FP8? Worked example in Inference Engineering Worksheets.

## Big-picture connect

Prefill = compute-bound. Decode = memory-bound. The KV cache is the resource you spend most of Week 4 trying to fit and Week 5 trying to budget.

## Stuck?

Ask **oxtutor** to re-explain — the KV cache and quantization sensitivity ladder (weights → activations → KV → attention) are the highest-leverage concepts of the entire phase.
