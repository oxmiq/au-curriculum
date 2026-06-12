# Day 28 · Chain-of-Thought & Few-Shot

> **Concept of the day:** **Chain-of-Thought** (CoT) = "think step by step" — measurable lift on reasoning, at decode-token cost. **Few-shot** = show 2–5 examples — high lift on format and style adherence. Both are free, both are bounded.
> **Pre-reading:** Anthropic tutorial **Ch 6 (Pre-cognition / CoT)** + **Ch 7 (Using Examples)** (~20 min).
> **Source:** [Student Guide Module 3](../../../../planning/source-material/Prompt%20Engineering/Prompt-Engineering-Student-Guide.md).

---

## Why this matters

These are the two most-cited prompting techniques in the research literature and the two most-misapplied in practice. Used well: 10–30% accuracy gains on hard tasks. Used badly: token cost up, latency up, no gain.

## Readiness check

1. Why does asking the model to "show its work" actually improve final-answer accuracy?
2. What's the **cost** of CoT in terms of output tokens? Connect to Week 2's decode bottleneck.
3. How many few-shot examples is "enough"? When does adding more hurt?
4. What's the difference between **zero-shot CoT**, **few-shot CoT**, and **scratchpad-then-answer**?
5. Why might you want to **hide** the CoT from the end user?

## Core concept — Chain-of-Thought

### The trick

Adding *"Think step by step. Show your reasoning before giving the final answer."* to a prompt measurably improves multi-step reasoning tasks (math, logic, code analysis).

Why it works: the model produces tokens autoregressively. Each token it writes becomes context for the next. By "writing out reasoning," the model effectively gives itself more compute and more recall steps before committing to an answer.

### Output structures for CoT

| Pattern | Use when |
|---|---|
| `Let's think step by step. ... \n\nFinal answer: X` | Quick, exploratory |
| `<reasoning>...</reasoning>\n<answer>X</answer>` | Production — easy to parse, easy to hide |
| `Plan: ... \n Steps: 1... 2... \n Answer: X` | Multi-step task decomposition |

### The cost

CoT can **triple or 10×** the output token count. Since decode is **memory-bound and sequential** (Week 2), output tokens are **the** cost driver. CoT trades:

- **More latency** (more decode steps).
- **More $** (more output tokens).
- **Higher accuracy** on reasoning tasks.

Worth it for hard tasks, wasteful on easy ones. The pro move: **CoT inside `<reasoning>` tags, hidden from UI, parsed away.**

### When CoT *doesn't* help (or hurts)

- Easy factual lookups ("What's the capital of France?")
- Open-ended creative writing
- Format conversion ("translate this to JSON")
- Anything where the model's first instinct is already correct

## Core concept — Few-shot

### The trick

Show 2–5 examples of input → output. The model pattern-matches and produces output in the same shape.

```
Classify the sentiment of these movie reviews as positive, negative, or neutral.

Review: "Best film I've seen all year."
Sentiment: positive

Review: "Visually stunning but the plot was incoherent."
Sentiment: neutral

Review: "Two hours of my life I won't get back."
Sentiment: negative

Review: "{the actual input}"
Sentiment:
```

This is **few-shot in-context learning** — the model "learns" the pattern without weight updates.

### How many examples

| N examples | When |
|---|---|
| 0 (zero-shot) | Task is obvious from instructions |
| 2–3 | Format consistency, simple classification |
| 4–8 | Subtle format / style, edge-case handling |
| > 10 | Diminishing returns; just fine-tune at that point |

### Why few-shot works

The model has seen the pattern *input → output* repeated. Its prediction for the *next* input → output completion follows the same pattern. Especially powerful for **format** (the model copies the shape exactly).

### Costs and traps

- **Context cost** — every example consumes prefill tokens.
- **Bias risk** — if all your examples are positive, the model leans positive.
- **Confounders** — examples that share an *irrelevant* feature (all 3 positive reviews mention actors) teach the model the wrong rule.

**Rule:** pick examples that **vary** along irrelevant dimensions and are **representative** of the real input distribution.

### CoT + Few-shot together

Show the model the *reasoning* in your few-shot examples too:

```
Q: A train leaves NY at 9am at 60mph...
Reasoning: Distance = speed × time. So at noon...
Answer: 180 miles.

Q: {new question}
Reasoning:
```

This **teaches the reasoning style**, not just the answer style. Often the strongest move for multi-step problems.

## Practice (90 min)

1. (15 min) Take a math word problem. Run it (a) zero-shot, (b) "think step by step," (c) hidden CoT inside `<reasoning>` tags. Compare accuracy and output length.
2. (25 min) Build a 4-shot classifier for a real task. Then run it without examples. Measure the gap.
3. (25 min) Adversarial few-shot: deliberately confound your examples (all positives mention rain). Show the model is biased on a new "rain" input. Then fix.
4. (15 min) Cost lab: estimate decode tokens (and $) for CoT-on vs CoT-off across 1000 requests at $5/1M output tokens. Worth it?
5. (10 min) Write the rule: *"Use CoT when ___; use few-shot when ___."*

## Wrap-up

Cohort agrees on the standard template for "production reasoning prompt": role + delimiters + few-shot + hidden CoT + schema'd output.

## Connect forward

Tomorrow: **what goes wrong** — hallucinations, complex prompts, and how to write evals that catch regressions.

---

## Pre-read for tomorrow (Day 29 · Hallucinations & Evals)

- **Resource:** Anthropic tutorial **Ch 8 (Avoiding Hallucinations)** + **Ch 9 (Complex Prompts from Scratch)** (~25 min).
- **Reflection questions:**
  1. Why do LLMs hallucinate? Name two structural causes.
  2. Name three guardrails that reduce hallucination in production.
  3. What's a **prompt eval suite** and how is it different from an LLM-as-judge?
