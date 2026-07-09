# Supplementary · Chain-of-Thought & Few-Shot Prompting

> **Concept of the day:** each token a model writes becomes context for the next — "writing out reasoning" gives the model more effective compute steps before committing to an answer. Showing 2–5 examples teaches format and style without weight updates. CoT and few-shot are the two highest-leverage capability levers you have before touching the model itself. **Pre-reading:** Anthropic tutorial Ch 6 (Pre-cognition / CoT) + Ch 7 (Using Examples).

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Chain-of-Thought |
| Part 3 | Deep Dive: When CoT Helps and Costs |
| Part 4 | Core Concepts: Few-Shot In-Context Learning |
| Part 5 | Hands-On: CoT Token Cost Lab |
| Part 6 | Hands-On: Few-Shot Classifier Build |
| Part 7 | Wrap-up & Connection |
| **Total** | |

---

## Part 1 — Pre-Reading Review

### Reading —

Before continuing, you should have read:

- Anthropic tutorial **Ch 6 (Pre-cognition / Chain-of-Thought)** — why CoT works, zero-shot vs few-shot CoT
- **Ch 7 (Using Examples)** — how many examples, bias risks, choosing good examples

If you haven't yet, stop and read them now.

### Exercise:

Answer from memory:

1. Why does asking the model to "show its work" improve final-answer accuracy on multi-step problems?
2. What is the **token cost** of CoT? Connect to the decode bottleneck from Week 2.
3. What is the difference between **zero-shot CoT**, **few-shot CoT**, and **scratchpad-then-answer**?
4. How many few-shot examples is "enough"? At what point do more examples stop helping?
5. Why might you want to **hide** the CoT from the end user?

---

## Part 2 — Core Concepts: Chain-of-Thought

### Reading —

Adding *"Think step by step. Show your reasoning before giving the final answer."* measurably improves multi-step reasoning tasks: math, logic, code analysis, and planning.

**Why it works:** The model produces tokens autoregressively. Each token it writes becomes context for the next. By "writing out reasoning," the model gives itself more compute and more recall steps before committing to a final answer. The reasoning tokens function as an extended scratchpad.

**Three CoT output structures:**

| Pattern | Template | Use when |
|---|---|---|
| Free-form | `Let's think step by step. ... \n\nFinal answer: X` | Quick, exploratory |
| Tagged | `<reasoning>...</reasoning>\n<answer>X</answer>` | Production — easy to parse, easy to hide |
| Structured plan | `Plan: ...\nSteps: 1... 2...\nAnswer: X` | Multi-step task decomposition |

**The production-grade pattern:**

```
You are a math tutor. Think through this problem step by step
before giving your final answer.

<reasoning>
[your step-by-step working here]
</reasoning>
<answer>
[final answer only]
</answer>

Problem: {problem}
```

The `<reasoning>` block can be extracted and discarded before showing the user the `<answer>`. Users see a clean response; the model gets the full compute benefit.

**Zero-shot CoT:** Adding "Let's think step by step." or "Think carefully before answering." to an existing prompt. Costs nothing to try. Often surprising how much this alone helps.

**Few-shot CoT:** Include worked examples with visible reasoning in your few-shot examples. The model learns to reason the same way. More on this in Part 4.

**Scratchpad (hidden):** Use a multi-turn conversation where the first turn produces reasoning and the second turn produces the answer based on the reasoning. The first turn is never shown to the user.

### Exercise:

Take this multi-step word problem:

> "A company has 240 employees. 30% work remotely full-time. Of the in-office employees, 25% work part-time. How many full-time in-office employees are there?"

1. Run it zero-shot (no CoT instruction). Record the answer and any errors.
2. Run it with "Think step by step" appended. Record the answer and reasoning.
3. Run it with the tagged `<reasoning>...</reasoning><answer>...</answer>` structure. Record both.
4. Which version was most accurate? Which was most parseable?

---

## Part 3 — Deep Dive: When CoT Helps and Costs

### Reading —

CoT can **triple or 10× the output token count**. Since decode is memory-bound and sequential (Week 2), output tokens are the primary cost and latency driver. CoT trades:

- **More latency** (more decode steps)
- **More cost** (more output tokens billed)
- **Higher accuracy** on reasoning tasks

**The cost math:**

If a direct answer takes 50 output tokens, CoT might take 200–500. At $5/1M output tokens, across 10,000 daily requests:

| Mode | Output tokens per request | Daily cost |
|---|---|---|
| Direct answer | 50 | $2.50 |
| CoT (3×) | 150 | $7.50 |
| CoT (10×) | 500 | $25.00 |

Worth it for hard tasks. Wasteful on easy ones. **The pro move:** gate CoT on a complexity classifier — run CoT only when the input exceeds a complexity threshold.

**When CoT helps:**

- Multi-step math or logic
- Code analysis / debugging
- Multi-hop reasoning ("if A implies B and B implies C...")
- Planning tasks with dependencies

**When CoT doesn't help (or hurts):**

- Simple factual lookups ("What's the capital of France?")
- Format conversion ("translate this JSON to YAML")
- Open-ended creative writing
- Tasks where the model's first instinct is already correct
- Very short inputs where reasoning adds noise

**Rule:** If you can't write out the intermediate reasoning steps yourself in 3–5 sentences, CoT probably won't help the model either.

### Exercise:

For each of the following tasks, decide: CoT or no CoT? Explain your reasoning.

1. "Translate this sentence to Spanish: 'The server is down.'"
2. "Given this buggy async Python function, identify all potential race conditions."
3. "Is this tweet positive, negative, or neutral?"
4. "Plan the steps to migrate a PostgreSQL database to a new server with zero downtime."
5. "What year was the Eiffel Tower built?"

---

## Part 4 — Core Concepts: Few-Shot In-Context Learning

### Reading —

**Few-shot prompting:** include 2–5 input → output examples before the actual input. The model pattern-matches and produces output in the same shape, format, and style.

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

**Why few-shot works:** the model has been trained on sequences of pattern-matched examples. Providing examples activates that pattern-completion behavior.

**How many examples:**

| N examples | Use when |
|---|---|
| 0 (zero-shot) | Task is obvious from instructions; format doesn't matter |
| 2–3 | Format consistency, simple classification |
| 4–8 | Subtle format / style, edge-case handling |
| > 10 | Diminishing returns; consider fine-tuning instead |

**Costs and traps:**

- **Context cost** — every example consumes prefill tokens
- **Bias risk** — if all your examples are positive, the model leans positive
- **Confounders** — examples that share an irrelevant feature (all positive reviews mention actors) teach the wrong rule

**Rule:** pick examples that **vary** along irrelevant dimensions and are **representative** of the real input distribution.

**CoT + Few-Shot together:** include the reasoning *in* your few-shot examples:

```
Q: A train leaves NY at 9am at 60mph...
Reasoning: Distance = speed × time. At noon (3 hrs), distance = 3 × 60 = 180 miles.
Answer: 180 miles.

Q: {new problem}
Reasoning:
```

This teaches the **reasoning style**, not just the answer style. Often the strongest pattern for multi-step problems.

**Master rule:** *"Use CoT when multi-step reasoning; use few-shot when format/style; use both when both."*

### Exercise:

1. Write a zero-shot prompt for: "Classify this support ticket as: `billing_issue | technical_issue | general_question`."
2. Add 3 few-shot examples. Choose examples that vary across irrelevant dimensions (different writing styles, different companies, different products).
3. Now add reasoning to each example (CoT + few-shot). Compare output quality on 5 new tickets.
4. Deliberately introduce a bias: make all 3 examples `technical_issue`. Run on a clear `billing_issue` ticket. Observe the bias. Fix it.

---

## Part 5 — Hands-On: CoT Token Cost Lab

### Exercise:

**Setup:** Pick a real multi-step task (math, code analysis, or logic). You'll need access to an LLM API with token counting (or use the token counter at platform.openai.com/tokenizer).

**Part A — Measure the cost:**

1. Write the task as a minimal prompt (no CoT). Count output tokens for 5 test inputs. Record average.
2. Add "Think step by step." Count output tokens for the same 5 inputs. Record average.
3. Add the full `<reasoning>...</reasoning><answer>...</answer>` structure. Count output tokens again.

**Part B — Calculate the economics:**

Assume: $5 / 1M output tokens; 1,000 requests per day.

| Mode | Avg output tokens | Daily cost | Monthly cost |
|---|---|---|---|
| Direct | | | |
| Zero-shot CoT | | | |
| Tagged CoT | | | |

At what request volume does CoT cost become a business decision rather than a rounding error?

**Part C — Quality vs cost decision:**

For your specific task, write a one-sentence justification for or against using CoT in production, quantified: "CoT costs $X/month extra and improves accuracy by approximately Y% on hard inputs — [worth it / not worth it] because ___."

---

## Part 6 — Hands-On: Few-Shot Classifier Build

### Exercise:

You are building a prompt to classify GitHub issue titles as: `bug | feature_request | question | documentation`.

**Step 1 — Zero-shot baseline:**

Write a zero-shot classification prompt. Run on 10 real GitHub issue titles (mix of all 4 classes). Record accuracy.

**Step 2 — Add few-shot examples:**

Write 4 few-shot examples (one per class). Rules for your examples:
- Must vary across irrelevant dimensions (language of the title, length, software domain)
- Must not share any surface feature that correlates with the class label

Run on the same 10 issues. Record accuracy delta.

**Step 3 — Add CoT to examples:**

Add one-sentence reasoning to each example:
```
Issue: "App crashes on startup when locale is set to Arabic"
Reasoning: This describes unexpected behavior (crash) — it's a bug report.
Class: bug
```

Run again. Record accuracy delta vs Step 2.

**Step 4 — Adversarial test:**

Write a deliberately confusing issue title that shares surface features of multiple classes (e.g., "The documentation for the login feature is wrong and causes bugs"). Which version (zero-shot / few-shot / CoT+few-shot) handles it best?

---

## Part 7 — Wrap-up & Connection

### Self-check

Before closing, tick each item:

- [ ] I can explain why CoT improves reasoning accuracy in one sentence.
- [ ] I can calculate the token cost of CoT vs direct answer for a given request volume.
- [ ] I know the three CoT patterns and when to use each.
- [ ] I understand when to use zero-shot vs 2-3 vs 4-8 few-shot examples.
- [ ] I can identify and fix a few-shot bias introduced by unrepresentative examples.
- [ ] I know the master rule: CoT for reasoning, few-shot for format/style, both when both.
- [ ] I can hide CoT from the user using `<reasoning>` tags.

### Connect Forward

These patterns are the final building blocks before agents:

- **CoT** → the planning step in a ReAct agent is CoT operating on tool outputs
- **Few-shot** → tool descriptions and tool-call examples in Week 7 are few-shot prompts
- **CoT + few-shot** → the full agentic prompt combines all techniques from Week 6

---

## Pre-read for the next supplementary (supplementary-04: Hallucinations, Complex Prompts & Evals)

- **Resource:** Anthropic tutorial **Ch 8 (Avoiding Hallucinations)** + **Ch 9 (Complex Prompts from Scratch)**.
- **Reflection questions:**
  1. Why do LLMs hallucinate? Name two structural causes.
  2. What is the chain reliability multiplication problem? If each of 3 steps is 90% reliable, what is the end-to-end success rate?
  3. What is a **prompt eval suite** and how is it different from an LLM-as-judge?

---

## Stuck?

Ask **oxtutor** to walk through any concept in this supplementary, generate additional practice problems for CoT reasoning, or quiz you on the master rule for combining CoT and few-shot.



