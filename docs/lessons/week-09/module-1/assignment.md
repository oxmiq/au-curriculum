# Week 9 — Capsule Benchmarking · Module Assignment

> **Source:** Capsule Power User Problem Sets §Set 45 (timed-sprint retrospective). **Feeds directly into Day 47 Capstone charter.**

## What you submit

A **retrospective** in your fork at `docs/practice/week-09/module-1/<date>-retrospective.md`, written *after* Friday's timed sprint, with these required sections:

### 1. Sprint result

- Did you complete the full sequence (find machine → benchmark → evaluate → record) in the 20-minute target?
- If not, where did time go? Be specific to the second if possible.

### 2. What surprised me about the benchmark results

At least **three** specific surprises. Each surprise must:

- State the prediction you (or the class) had.
- State what actually happened (with numbers).
- Name the Phase 1 concept that explains the gap.

> Example shape: *"I predicted FP8 would halve TTFT. It didn't — TTFT only dropped 12%. Because we were memory-bandwidth-bound at decode but compute-bound at prefill, and TTFT is dominated by prefill. (Week 2 Day 9 + Week 3 Day 11.)"*

### 3. Quality vs speed verdict

For the two configs you compared in Day 43: which would you ship and why? Two sentences max.

### 4. Personal command sequence

The exact sequence of `capsule` commands you'd run cold tomorrow to repeat the sprint. Copy-pasteable. **No prose between commands.**

### 5. Capstone seed (feeds Week 10 Day 47)

Three sentences:

- A use case you'd want to investigate in the capstone.
- A model you'd benchmark.
- A claim you'd hope to defend in the form: *"For use case X, deploy model Y at config Z, because [evidence] shows [metric] at [cost], with [quality tradeoff] that is [acceptable/not] because [reasoning]."*

This becomes your Day 47 charter input. **Make it real — Week 10 builds on it.**

## Grading rubric

| Section | Pass requires |
|---|---|
| Sprint result | Honest time accounting |
| Surprises | 3+ surprises, each with prediction + actual + Phase-1 concept |
| Quality vs speed | Defended in ≤2 sentences |
| Command sequence | Copy-pasteable, no missing steps |
| Capstone seed | Use case + model + claim sentence completed |

## Why this assignment exists

Two reasons:

1. **Forced reflection.** A sprint without retro just feels like adrenaline. Three written surprises convert it into durable learning.
2. **Capstone bootstrap.** Week 10 Day 47 expects you to walk in with a half-formed charter. This assignment is where it crystallizes.

Don't skip section 5. Future-you on Monday will thank present-you.
