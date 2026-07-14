# Day 45 (Fri) · Week 9 Consolidation

> **Goal of the day:** consolidate Capsule benchmarking + evaluation. Timed end-to-end sprint, then seed your capstone charter.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 - Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 45 · Consolidation</span>
    {status:week-09/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Self-Study Time Buckets

| Bucket | Activity |
|---|---|
| 🔵 Bucket 1 | Knowledge Check |
| 🟢 Bucket 2 | Self-Assessment: Full Bench-to-Dashboard Sprint |
| 🟡 Bucket 3 | Benchmark Drills |
| 🟠 Bucket 4 | Eval & Quality Drills |
| 🔴 Bucket 5 | Capstone Seed - Draft Your Charter |
| 🟣 Bucket 6 | Open Lab & Week 10 Preview |

---

## 🔵 Bucket 1: Knowledge Check

[Take the canonical knowledge check](knowledge-check.md). Covers benchmark mechanics, model evaluation, scheduling, MCP.

---

## 🟢 Bucket 2: Self-Assessment - Full Bench-to-Dashboard Sprint

**Timed - 20 min target.** Execute from scratch without notes:

1. Find an NVIDIA machine with ≥24 GB VRAM that has no active user
2. Connect via VS Code
3. Run `capsule benchmark` on `meta-llama/Llama-3.1-8B-Instruct` with concurrency 8, ISL 256, OSL 256
4. Note the throughput (tokens/sec)
5. Re-run with `--quant awq`
6. Open the benchmark dashboard and find both runs

If you can do this in <20 minutes, you're ready for the Capstone.

---

## 🟡 Bucket 3: Benchmark Drills

1. What does `--concurrency 8` mean? How does it differ from `--num-prompts`?
2. At what ISL/OSL do you expect the system to become compute-bound vs memory-bound? (Phase 1 vocabulary)
3. You see throughput drop 40% from run 1 to run 2 on the same machine. Name 3 possible causes and the diagnostic command for each.
4. Explain the saturation curve: why does throughput plateau at high concurrency while latency continues rising?
5. What does `--no-upload` do, and when would you use it?

---

## 🟠 Bucket 4: Eval & Quality Drills

1. You benchmark two quantizations: FP16 = 1400 tok/s, AWQ = 1800 tok/s. AWQ is 29% faster. Is AWQ strictly better? What else must you check?
2. Run `capsule chat` against a model with `--temperature 0.1`. Ask the same question 5 times. Describe what you observe (consistency).
3. Define a 5-prompt eval suite for a "code assistant" use case. Include: 1 easy (factual), 1 medium (multi-step reasoning), 1 hard (edge case), 1 refusal probe, 1 format-compliance test.
4. How does `--agent oxsol` change the `capsule chat` session?

---

## 🔴 Bucket 5: Capstone Seed - Draft Your Charter

The capstone starts Monday. Today you draft your charter. Template fields to fill:

```
Capstone Charter Draft
Team: ___
Use case (one sentence: who is the user, what is the specific task): ___
Model selection (name + size + why this one): ___
Hardware selection (GPU type + why): ___
Quantization plan (FP16 baseline + at least 1 alternative + why): ___
Eval plan (5-10 prompts, what success looks like per prompt): ___
Success criterion (metric + threshold): ___
Anti-goals (what you will NOT test, and why): ___
```

Review your draft against the capstone deliverable format:

> "For [use case], deploy [model] at [config], because [benchmark evidence] shows [metric] at [cost], with [quality tradeoff] that is [acceptable / not] because [reasoning]."

Can you fill in the brackets now (as a hypothesis)? If not, the charter is incomplete.

---

## 🟣 Bucket 6: Open Lab & Week 10 Preview

- Pre-read for Monday: Capstone Guide + Day-46-Charter-Template
- Ask oxtutor to peer-review your charter draft
- Catch up on any incomplete Week 9 assignments

## Pre-read for Monday (Week 10 · Day 46 · Kickoff & Planning)

Resource: Capstone Guide + Day-46-Charter-Template. Questions to carry in:

- What does a "strong" vs "weak" charter look like?
- What does the panel check for?
- Why is "it works" not an acceptable success criterion?

---

## Stuck?

Ask **oxtutor**; the Week 9 → Week 10 bridge is the [Day-46 Charter Template](../../../../planning/source-material/Capstone/Day-46-Charter-Template.md), which assumes you can run all four Day 41–44 skills cold.
