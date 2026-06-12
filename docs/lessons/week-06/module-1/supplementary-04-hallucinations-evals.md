# Day 29 · Hallucinations, Complex Prompts & Evals

> **Concept of the day:** LLMs **hallucinate** when they extrapolate beyond their training or context. Guardrails: ground on source, allow "I don't know," chain into validation steps. **Prompt evals** catch regressions before users do. Anthropic tutorial Chapters 8–9.
> **Pre-reading:** Anthropic tutorial **Ch 8 (Avoiding Hallucinations)** + **Ch 9 (Complex Prompts from Scratch)** (~25 min).
> **Source:** [Student Guide Module 4](../../../../planning/source-material/Prompt%20Engineering/Prompt-Engineering-Student-Guide.md) · [Problem Sets §Set 30](../../../../planning/source-material/Prompt%20Engineering/Prompt-Engineering-Problem-Sets.md).

---

## Why this matters

The two production failure modes in Phase 2: **hallucinations** (wrong with confidence) and **silent regressions** (the prompt got worse and nobody noticed). Both are preventable. This is the day prompts become **engineered systems**, not artisanal text.

## Readiness check

1. Why do LLMs hallucinate — what structural mismatch causes it?
2. Name three guardrails for grounded answers.
3. Why is "if you don't know, say 'I don't know'" surprisingly effective?
4. What's a **prompt eval suite**?
5. **Chain reliability:** if each of 3 chained prompts is 90% reliable, what's end-to-end success rate? At 95%? At 99%?

## Core concept — hallucinations

### Why they happen

Two main causes:

1. **Out-of-distribution input.** The model has no training data for your specific question; it produces the *most plausible-sounding* completion, which is not the same as the *correct* one.
2. **No grounding source.** Asked open-endedly, the model draws on parametric memory, which is lossy and outdated.

LLMs are next-token predictors. **"I don't know" is a low-probability token** unless the prompt explicitly invites it.

### Guardrails

| Guardrail | What it does | Cost |
|---|---|---|
| **Ground on source** | Provide the document; instruct "only use information in `<source>` tags" | Prefill cost grows with context |
| **Allow "I don't know"** | Add: "If the answer isn't in the source, reply *I don't know*" | Free — and very effective |
| **Citation requirement** | "Cite the exact sentence from the source for every claim" | Output tokens up; quality up |
| **Constrain to known values** | Schema with enum types ("severity must be one of: high/med/low") | Free |
| **Self-check pass** | Second prompt: "Verify the answer above is supported by the source. List any unsupported claims." | 2× cost; catches ~60% of remaining errors |
| **External validation** | Run the model's code/SQL through a real interpreter | Best for code-y tasks |

### Chain reliability — the multiplicative trap

If you chain 3 prompts each 90% reliable:

> **End-to-end success = 0.90 × 0.90 × 0.90 = 72.9%**

| Per-step reliability | 3-chain | 5-chain | 10-chain |
|---|---|---|---|
| 0.90 | 72.9% | 59.0% | 34.9% |
| 0.95 | 85.7% | 77.4% | 59.9% |
| 0.99 | 97.0% | 95.1% | 90.4% |

> **Implication for Week 7 agents:** each step must be **at least 95% reliable** or the agent collapses at 5+ steps. Most failures are at the prompt level, not the model.

## Core concept — complex prompts from scratch

A production prompt rarely starts perfect. The Anthropic tutorial Ch 9 process:

1. **Define success.** What does a good output look like? Write 5 examples.
2. **Draft v1.** Role + context + task + format + constraints.
3. **Run on 5–10 test inputs.** Note failures.
4. **Add guardrails for each failure mode.** Delimiters? Schema? Few-shot? "I don't know" clause?
5. **Re-run.** Measure delta.
6. **Repeat until stable.**

This is **prompt engineering as engineering** — iterative, measurable, version-controlled.

## Core concept — prompt evals

A **prompt eval suite** is a set of {input, expected output (or rubric)} pairs that you run on every prompt change. Like a unit-test suite for prompts.

### Building one

| Step | What |
|---|---|
| 1 | Collect 20–50 representative inputs from real (anonymized) traffic. |
| 2 | Write reference outputs (or graded rubrics: "must contain X, must not contain Y"). |
| 3 | Run the prompt; score each input (exact match, regex, schema valid, LLM-judge with caveats). |
| 4 | Track pass rate over time. Block deploys on regression > 2pp. |

### What makes a good eval

- **Mix of easy and hard.** 70% easy / 30% hard is a reasonable distribution.
- **Edge cases included.** Empty input, malicious input, off-topic input, very long input.
- **Schema validation always.** If you ask for JSON, every test checks the JSON parses.
- **Owner per eval.** A human reviews failures, doesn't auto-trust judges.

### When to LLM-as-judge

Yes:
- Format compliance ("is this valid JSON?")
- Pairwise comparison ("which of A/B answers the question better?")
- Factuality with reference ("does this match the source?")

No:
- Subjective quality without rubric
- Math correctness (use a real solver)
- Safety scoring (use specialized classifiers)

## Practice (90 min)

1. (15 min) Take an open-ended prompt. Add the three free guardrails (ground, "I don't know," schema). A/B test on 5 inputs including one without a true answer.
2. (25 min) Build a 5-input prompt eval suite for a real task. Run twice with one tiny prompt change. Detect the regression / improvement.
3. (25 min) Chain math: design a 3-step chain (extract → classify → format). At what per-step reliability do you need to operate to clear 90% end-to-end?
4. (15 min) Self-check pattern: write a 2-prompt sequence where the second checks the first's output against rules. Demonstrate it catching at least one bad output.
5. (10 min) Write the rule: *"Every production prompt needs ___, ___, and ___."*

## Wrap-up

Cohort agrees on the **definition of "production-ready" prompt**: has eval suite, has guardrails, has schema, has owner.

## Connect forward

Friday: **the bar** — chaining drill + your own prompt-eval suite + canonical quiz. The **5% PE assessment** is graded on the eval suite + a 2-step chain.

---

## Pre-read for Friday (Day 30 · Consolidation)

- **Resource:** Anthropic tutorial **Appendix (Tool Use + Chaining intro)** (~15 min).
- **Reflection questions:**
  1. How will today's "self-check" pattern evolve into Week 7's "tool use"?
  2. What's the most important guardrail you'll bring forward to agents?
  3. What's the prompt failure-mode you're most worried about in agents?
