# Day 23 · Evaluation & Quality

> **Concept of the day:** **perplexity** for sanity, **benchmarks** for comparison, **task evals** for production decisions. Public benchmarks are gameable; your own eval suite is the only one that matters. **Quantization quality must be measured, not assumed.**
> **Pre-reading:** "Evaluating LLMs" overview — Pre-Lecture Reading **Reader 10** (~20 min).
> **Source:** [Study Guide §A.7 evaluation](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Glossary: perplexity, MMLU](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Glossary.md).

---

## Why this matters

A quantized model that ships with 5% quality regression on *your task* will silently lose customers. A model that scores +2 on MMLU might be worse for *you*. Eval is the only thing that closes the loop between engineering speedups and business outcomes.

## Readiness check

1. What is **perplexity** measuring?
2. Why does a model score 85% on MMLU but feel "dumber" on your specific task?
3. What's a **task eval suite** and how is it different from a benchmark?
4. **LLM-as-a-judge** — when does it work, when does it deceive?
5. After quantizing FP16 → FP8, what's the minimum eval you should run?

## Core concept

### The three layers of evaluation

**1. Sanity (perplexity / loss)** — cheap, fast, coarse.

Perplexity = exp(cross-entropy) on a held-out text set. Tells you the model still produces "reasonable" probability distributions. **Goes up = quality dropped.** Useful for catching catastrophic damage from a bad quantization.

**Limit:** doesn't tell you anything about *task* quality. A model can lose perplexity from a bug and still ace your benchmark, or vice versa.

**2. Benchmarks (MMLU, HellaSwag, HumanEval, etc.)** — comparable, citable, gameable.

| Benchmark | Tests |
|---|---|
| MMLU | Multi-subject knowledge (57 subjects) |
| HellaSwag | Commonsense reasoning |
| HumanEval / MBPP | Code generation |
| GSM8K / MATH | Math word problems |
| HELM / lm-eval-harness | Multi-task batteries |

**Use them for:** comparing model A vs model B at a glance.
**Don't use them for:** declaring you're "production ready."

> **Goodhart again:** model trainers know which benchmarks matter. They optimize for those. MMLU saturation has more to do with training data leakage than with capability gains.

**3. Task evals (your own suite)** — narrow, honest, the one that ships decisions.

Build a suite of **50–200 prompts** that look like real production traffic, with reference outputs (or graded rubrics). Run it on every model / quantization / engine change. Report:

- Pass rate (binary correct/incorrect).
- Format compliance (does it produce valid JSON / structured output?).
- Safety / refusal behaviour.
- Side-by-side win rate vs the previous deployment.

### LLM-as-a-judge

A bigger model (often GPT-4 or Claude) grades the smaller model's outputs. **Cheap to run, dangerous to trust.**

| Works well | Works poorly |
|---|---|
| Format / structural checks | Subjective quality (length, style) |
| Factuality with reference | Math correctness without reference |
| Pairwise win-rate | Absolute scoring (judges are biased toward positive scores) |

**Always pair with human spot-checks** on ~10% of items.

### The quantization-quality contract

Standard process when you push FP16 → FP8 (or any precision change):

1. **Perplexity delta** on a held-out set. Reject if Δ > 1%.
2. **Task eval pass rate**. Reject if regression > 2 pp (percentage points).
3. **Side-by-side human eval** on 50 representative prompts. Reject if win rate < 45%.
4. **Refusal-rate sanity** (didn't accidentally break safety tuning).

Document and ship.

### What to measure for *agentic* workloads (preview Week 7)

- **End-to-end task success rate** (did the agent complete the task?).
- **Tool-call validity** (did it call valid tools with valid arguments?).
- **Trajectory length** (how many turns did it take?).
- **Cost per task** (tokens spent).

## Practice (90 min)

1. (15 min) Build a 10-prompt task eval for a "summarize a Slack thread" use case. What does each prompt test?
2. (25 min) Take a published MMLU score and reason about what it does and doesn't tell you for a code-generation product.
3. (25 min) Pair: a teammate proposes "let's quantize to INT4 — only 1% perplexity loss." What's your full counter-checklist before approving?
4. (15 min) Design an LLM-as-a-judge prompt for grading "is this JSON valid and complete per the schema?" Where could it deceive you?
5. (10 min) Write the rule: *"Benchmarks are for ___; task evals are for ___."*

## Wrap-up

Cohort agrees: **no quantization or model change ships without a task-eval delta**. Public benchmarks are tiebreakers, never deciders.

## Connect forward

Tomorrow: **cost & economics** — the *third* metric layer (latency, quality, **cost**). Token economics, dedicated vs API, GPU utilization → cost per million tokens.

---

## Pre-read for tomorrow (Day 24 · Cost & Economics)

- **Resource:** "Cost of inference" calculator / blog — Pre-Lecture Reading **Reader 10** (~15 min).
- **Reflection questions:**
  1. What dominates cost: prefill tokens or decode tokens? Why?
  2. **Dedicated GPU** vs **token-priced API** — at what utilization does dedicated break even?
  3. Why does **GPU utilization** translate directly to cost-per-million-tokens?
