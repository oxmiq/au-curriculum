# Day 23 · Evaluation & Quality

> **Concept of the day:** **perplexity** for sanity, **benchmarks** for comparison, **task evals** for production decisions. Public benchmarks are gameable; your own eval suite is the only one that matters. **Quantization quality must be measured, not assumed.**
> **Pre-reading:** "Evaluating LLMs" overview — Pre-Lecture Reading **Reader 10** (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 23 · Evaluation & Quality</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-05/module-3}
  </div>
  <div class="ox-lesson-header__cta">
    <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
    <a class="md-button md-button--primary" href="knowledge-check.html">Knowledge check</a>
    <a class="md-button" href="assignment.md">Assignment</a>
    <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| # | What you do | Time |
|---|-------------|------|
| 1 | Why Evaluation Matters | 15 min |
| 2 | Three Evaluation Layers | 25 min |
| 3 | Build a Task Eval Suite | 25 min |
| 4 | Quantization Quality Check | 25 min |
| 5 | LLM-as-a-Judge | 20 min |
| 6 | Design Your Eval Pipeline | 20 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Why Evaluation Matters · 15 min

### Reading

A quantized model that ships with 5% quality regression on *your task* will silently lose customers. A model that scores +2 on MMLU might be worse for *you*. Eval is the only thing that closes the loop between engineering speedups and business outcomes.

### Reflection (write your answer)

Take 2 minutes to write down:
> Why is "it scores 85% on MMLU" not enough to ship a model to production?

---

## Part 2 — Three Evaluation Layers · 25 min

### Layer 1: Sanity (Perplexity)

**Perplexity** = exp(cross-entropy) on a held-out text set.

- **What it tells you:** The model still produces "reasonable" probability distributions
- **What it misses:** Task-specific quality
- **Goes up** = quality dropped

**Use for:** Catching catastrophic damage from a bad quantization or bug.

### Layer 2: Benchmarks (MMLU, etc.)

| Benchmark | What It Tests | Use For |
|-----------|---------------|---------|
| MMLU | Multi-subject knowledge (57 subjects) | Quick comparison |
| HellaSwag | Commonsense reasoning | Reasoning check |
| HumanEval / MBPP | Code generation | Code products |
| GSM8K / MATH | Math word problems | Math ability |
| HELM | Multi-task batteries | Comprehensive |

> **Goodhart again:** Model trainers know which benchmarks matter. They optimize for those. MMLU saturation has more to do with training data leakage than capability gains.

**Benchmarks are for comparing — never for declaring production ready.**

### Layer 3: Task Evals (Your Own Suite)

Build a suite of **50–200 prompts** that look like real production traffic.

For each prompt:
- Reference output (if available) OR
- Graded rubric (what makes a "good" response)

**Report:**
- Pass rate (binary correct/incorrect)
- Format compliance (valid JSON? structured output?)
- Safety / refusal behavior
- Side-by-side win rate vs previous deployment

> **Task evals are for shipping decisions — benchmarks are tiebreakers.**

---

## Part 3 — Build a Task Eval Suite · 25 min

### Exercise: Create a 10-Prompt Eval Suite

**Use case:** "Summarize a Slack thread"

For each of these 10 scenarios, write a prompt and define what makes it "pass" or "fail":

1. Short thread (5 messages) → Summary < 50 words
2. Long thread (50 messages) → Summary captures all key points
3. Thread with decisions → Summary includes decisions made
4. Thread with questions → Summary identifies unanswered questions
5. Thread with code snippets → Code is preserved accurately
6. Thread with links → Links are preserved
7. Thread with emoji/reactions → Tone captured
8. Thread with a debate → Both sides summarized
9. Thread in another language → Language preserved appropriately
10. Thread with no clear content → Appropriate "nothing to summarize" response

### Write Your Rubric

For each prompt, define:
- **Input:** The Slack thread (simulated)
- **Expected output:** What a good summary looks like
- **Pass criteria:** 3-5 specific things that must be present

---

## Part 4 — Quantization Quality Check · 25 min

### Scenario

A teammate proposes: "Let's quantize to INT4 — only 1% perplexity loss."

### Exercise: Your Counter-Checklist

Before approving any quantization change, you must verify:

1. **Perplexity check** — Run on a held-out set. Reject if Δ > ___%
2. **Task eval check** — Run your task eval suite. Reject if regression > ___ percentage points
3. **Side-by-side human eval** — Compare 50 outputs. Reject if win rate < ___%
4. **Refusal-rate sanity** — Did we break safety tuning?
5. **Format compliance** — Did we break JSON output?

**Fill in the thresholds** from Day 23's content.

### Discussion

**Why is perplexity not enough?**

Even with only 1% perplexity loss, the model could:
- Lose instruction-following capability
- Become worse at your specific task
- Have degraded safety behavior

**Fill in:** Perplexity catches ___% of problems; task eval catches the rest.

---

## Part 5 — LLM-as-a-Judge · 20 min

### Reading — When It Works, When It Deceives

A bigger model (often GPT-4 or Claude) grades the smaller model's outputs. **Cheap to run, dangerous to trust.**

| Works Well | Works Poorly |
|------------|--------------|
| Format / structural checks | Subjective quality (length, style) |
| Factuality with reference | Math correctness without reference |
| Pairwise win-rate | Absolute scoring (judges are biased toward positive scores) |

**Always pair with human spot-checks** on ~10% of items.

### Exercise: Design a Judge Prompt

Design an LLM-as-a-judge prompt for grading:

> "Is this JSON valid and complete per the schema?"

**Potential deception points:**
- The judge might accept invalid JSON that "looks right"
- The judge might miss subtle schema violations
- The judge might be biased toward longer outputs

**How would you mitigate these?**

---

## Part 6 — Design Your Eval Pipeline · 20 min

### The Quantization-Quality Contract

Standard process when you push FP16 → FP8 (or any precision change):

1. **Perplexity delta** on a held-out set. Reject if Δ > 1%.
2. **Task eval pass rate**. Reject if regression > 2 pp.
3. **Side-by-side human eval** on 50 prompts. Reject if win rate < 45%.
4. **Refusal-rate sanity** (didn't break safety tuning).

Document and ship.

### Reflection Question

Write one sentence:
> The quality contract ensures that ___ doesn't ship without measuring ___.

---

## Part 7 — Wrap-up & Connection · 10 min

### Synthesis

Today's three layers — perplexity, benchmarks, task evals — form the quality axis of the SLO tripod. Tomorrow you tackle the third axis: **cost**. Every decision you make about quantization and serving has a dollar sign attached. The quality contract you built today is what protects you from optimizing cost at the expense of your users.

### Pre-read for tomorrow (Day 24 · Cost & Economics)

- **Resource:** "Cost of inference" calculator / blog — Pre-Lecture Reading **Reader 10** (~15 min).
- **Reflection questions:**
  1. What dominates cost: prefill tokens or decode tokens? Why?
  2. **Dedicated GPU** vs **token-priced API** — at what utilization does dedicated break even?
  3. Why does **GPU utilization** translate directly to cost-per-million-tokens?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
