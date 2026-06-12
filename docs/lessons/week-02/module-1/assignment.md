# Week 2 — Inference: GPU & Memory · Module Assignment

> **Source:** Mindmap Week 2 Day 10 + Inference Engineering Glossary (Feynman teach-back prompts).

## What you submit

A **one-page write-up** (≤ 400 words) of the **Feynman teach-back** you delivered on Friday. Pick **one** of:

- *bandwidth*
- *FLOPs*
- *roofline*
- *memory hierarchy*

Explain it as if to a peer who missed all of Week 2.

## Required structure

1. **One-sentence definition** in plain English. No jargon-as-shield.
2. **Analogy** — your own, not the lecture's.
3. **The number that matters** — quote one Week 2 fact (e.g. *H100 HBM3 = 3.35 TB/s*, *ridge point ≈ 295 ops/byte*).
4. **The consequence** — one sentence: *"Because of this, when you do X, Y happens."*
5. **Why a Capsule benchmark in Week 9 will reveal this.** One sentence connecting your concept to a knob in `capsule benchmark` (concurrency, tp, quantization, etc.).

## What "good" looks like

- A peer who missed Week 2 can read your page in 5 minutes and answer one of the Day 8/9 readiness-check questions.
- The number is correct.
- The Week 9 connection is non-trivial — not just *"it shows up in metrics."*

## Grading

Pass / no-pass on each of the 5 sections. Need 4/5 to pass.

## Why this assignment exists

The Feynman technique — explaining a concept until a novice gets it — is the single best test of whether *you* actually understand it. The Glossary entries for bandwidth / FLOPs / roofline / memory hierarchy are the calibration reference; if your explanation collapses to those without using the Glossary's words, that's a pass.
