# Supplementary · Hallucinations, Complex Prompts & Evals

> **Concept of the day:** LLMs hallucinate when they extrapolate beyond their training data or context — "I don't know" is a low-probability token unless explicitly invited. Guardrails, chain reliability math, and eval suites are the engineering tools that convert a fragile prompt into a production system. **Pre-reading:** Anthropic tutorial Ch 8 (Avoiding Hallucinations) + Ch 9 (Complex Prompts from Scratch) (~25 min).

---

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Why LLMs Hallucinate | 20 min |
| Part 3 | Core Concepts: Six Guardrails | 25 min |
| Part 4 | Deep Dive: Chain Reliability Math | 15 min |
| Part 5 | Core Concepts: Prompt Evals | 20 min |
| Part 6 | Hands-On: Hallucination Guardrail Lab | 30 min |
| Part 7 | Wrap-up & Connection | 15 min |
| **Total** | | **~180 min** |

---

## Part 1 — Pre-Reading Review · 15min

### Reading —

Before continuing, you should have read:

- Anthropic tutorial **Ch 8 (Avoiding Hallucinations)** — causes, guardrails, grounding patterns
- **Ch 9 (Complex Prompts from Scratch)** — the iterative process for building production prompts

If you haven't yet, stop and read them now (~25 min).

### Exercise:

Answer from memory:

1. Name two structural reasons why LLMs hallucinate.
2. What does "grounding" mean in the context of prompt engineering?
3. Why is adding "if you don't know, say 'I don't know'" surprisingly effective?
4. What is a **prompt eval suite**? How is it different from an LLM-as-judge?
5. Chain reliability: if each of 3 chained prompts is 90% reliable, what is the end-to-end success rate?

---

## Part 2 — Core Concepts: Why LLMs Hallucinate · 20min

### Reading —

**Hallucination** = a model producing confident, fluent, wrong output. Two structural causes:

**1. Out-of-distribution input**

The model has no training data for your specific question. It produces the most plausible-sounding completion — which is not the same as the correct one. The model cannot distinguish between "I know this" and "I'm extrapolating."

**2. No grounding source**

Asked open-endedly ("What year did X happen?"), the model draws on **parametric memory** — facts compressed into weights during training. Parametric memory is lossy, outdated, and cannot be checked at inference time.

**The core problem:**

LLMs are next-token predictors. The token "I don't know" is a low-probability token in most training contexts — people writing on the internet rarely say they don't know something. Unless you explicitly invite "I don't know" as a valid output, the model avoids it.

**Consequence:** Models hallucinate most on:

- Questions about obscure facts with sparse training data
- Questions outside the training cutoff
- Questions that look like they have an answer but don't (questions about non-existent entities, events, papers)
- Tasks requiring precise recall of numbers, dates, citations

**Recognition heuristic:** If you yourself aren't sure of the exact answer, the model probably isn't either — and unlike you, it won't hedge.

### Exercise:

For each of the following prompts, assess hallucination risk (high/medium/low) and explain why:

1. "What is 2 + 2?"
2. "Summarize the key arguments of this paper: [paper text pasted in]"
3. "What did Elon Musk tweet on March 3, 2022?"
4. "What are the main differences between Python 3.10 and 3.11?"
5. "What is the revenue of AcmeCorp for Q3 2025?"

---

## Part 3 — Core Concepts: Six Guardrails · 25min

### Reading —

These six guardrails address hallucination at different cost/effectiveness tradeoffs:

| Guardrail | What it does | Cost |
|---|---|---|
| **1. Ground on source** | Provide the document; instruct "only use content inside `<source>` tags" | Prefill cost grows with source length |
| **2. Allow "I don't know"** | Add: "If the answer isn't in the source, reply exactly: *I don't know*" | Free — and very effective |
| **3. Citation requirement** | "Cite the exact sentence from the source for every claim you make" | Output tokens ↑; quality ↑ |
| **4. Constrain to known values** | Schema with enum: `"severity": "high \| medium \| low"` — no free-form string | Free |
| **5. Self-check pass** | Second prompt: "Verify the answer above is supported by the source. List any claim not directly supported." | ~2× cost; catches ~60% of remaining errors |
| **6. External validation** | Run the model's code through a real interpreter; run the SQL against a sandbox DB | Best for code / structured data tasks |

**Guardrail selection guide:**

- Factual Q&A from a document → Guardrails 1 + 2 + 3
- Classification or extraction → Guardrail 4 (constrain to known values)
- High-stakes summaries (legal, medical) → Guardrails 1 + 2 + 5
- Code generation → Guardrail 6
- Multi-step pipelines → Guardrails 1 + 4 + 6 + reliability-aware design (Part 4)

**Important:** Guardrails are not a magic fix. A sufficiently sophisticated hallucination (a plausible-sounding citation that doesn't exist) may pass Guardrail 3 because the model invents a source that sounds real. Always add a domain-appropriate external check for high-stakes output.

### Exercise:

You are building a RAG (retrieval-augmented generation) prompt that answers user questions from a company knowledge base.

1. Write the base prompt with Guardrails 1 and 2 applied.
2. Add Guardrail 3 (citation requirement). Run on 5 questions — 3 answerable from the source, 2 not answerable. Verify the "I don't know" guardrail fires correctly.
3. Design the self-check pass (Guardrail 5). Write the second prompt that verifies the first prompt's answer. What fields does its output need?
4. For a question with a factual answer that is NOT in the source, what does your 2-prompt chain produce? Is that the right behavior?

---

## Part 4 — Deep Dive: Chain Reliability Math · 15min

### Reading —

If you chain $n$ steps, each with reliability $r$, end-to-end success is:

$$P_{\text{success}} = r^n$$

The multiplication table:

| Per-step reliability | 3-step chain | 5-step chain | 10-step chain |
|---|---|---|---|
| 0.90 | 72.9% | 59.0% | 34.9% |
| 0.95 | 85.7% | 77.4% | 59.9% |
| 0.99 | 97.0% | 95.1% | 90.4% |

> **Implication:** to achieve 80% end-to-end success on a 5-step agent, each step must be at least 96% reliable. Most production prompt steps are 90–95% reliable without tuning. This is why agents fail — not because the model is bad, but because reliability compounds.

**Building complex prompts from scratch — the iterative process (Ch 9):**

1. **Define success first.** Write 5 examples of good output before writing the prompt.
2. **Draft v1.** Role + context + task + format + constraints.
3. **Run on 5–10 test inputs.** Note every failure mode.
4. **Add guardrails for each failure mode.** Delimiter? Schema? "I don't know"? Few-shot?
5. **Re-run.** Measure delta.
6. **Repeat until pass rate is ≥ 95%.**

This is **prompt engineering as engineering** — iterative, measurable, version-controlled. Not artisanal text.

### Exercise:

Design a 3-step classification chain: (1) extract entities → (2) classify intent → (3) format as JSON.

1. Set a reliability target: you want 85% end-to-end success. What per-step reliability does that require?
2. For each step, identify the most likely failure mode.
3. For each failure mode, pick the guardrail from Part 3 that addresses it.
4. Estimate the new per-step reliability after adding guardrails. Does the chain now clear 85%?

---

## Part 5 — Core Concepts: Prompt Evals · 20min

### Reading —

A **prompt eval suite** is a set of `{input, expected output / rubric}` pairs that you run on every prompt change — like a unit-test suite for prompts.

**Building one:**

| Step | What |
|---|---|
| 1 | Collect 20–50 representative inputs from real (anonymized) traffic |
| 2 | Write reference outputs or rubrics ("must contain X", "must not contain Y", "must parse as JSON") |
| 3 | Run the prompt; score each input (exact match / regex / schema valid / LLM-judge with caveats) |
| 4 | Track pass rate over time. Block deploys on regression > 2 percentage points |

**What makes a good eval suite:**

- **Mix of easy and hard.** 70% easy / 30% hard is a good ratio.
- **Edge cases included.** Empty input, malicious input, off-topic input, very long input.
- **Schema validation always.** If you ask for JSON, every test case checks that the JSON parses.
- **Owner per eval.** A human reviews failures; never auto-trust an LLM judge on safety or correctness.

**When LLM-as-judge is acceptable:**

| Yes | No |
|---|---|
| Format compliance ("is this valid JSON?") | Math correctness (use a real solver) |
| Pairwise comparison ("which of A/B is better?") | Safety scoring (use specialized classifiers) |
| Factuality with a reference document | Unconstrained subjective quality |

### Exercise:

Build a 5-input eval suite for the RAG prompt from Part 3.

1. Write 5 test cases: 2 easy (answer clearly in source), 2 hard (answer requires inference from source), 1 edge (question not answerable from source).
2. For each test case, write the expected output or rubric.
3. Run your prompt on all 5. Record pass/fail.
4. Make one small change to the prompt (add a sentence, change a word). Re-run. Did any test case flip? Is that a regression or improvement?

---

## Part 6 — Hands-On: Hallucination Guardrail Lab · 30min

### Exercise — Part A: Guardrail A/B Test (15 min)

**Setup:** Use a factual Q&A task. Your source document is a short Wikipedia paragraph about a technical topic (your choice).

**Condition 1 — No guardrails (5 min):**
Ask a question whose answer is NOT in the paragraph. What does the model do? Does it say it doesn't know, or does it hallucinate?

**Condition 2 — Guardrail 1 + 2 (5 min):**
Add grounding (`<source>` tags) and "I don't know" permission. Run the same question. What happens?

**Condition 3 — Full guardrail stack (5 min):**
Add Guardrail 3 (citation) and write a 2-input eval suite. Does the model correctly cite the source for answerable questions and correctly return "I don't know" for unanswerable ones?

### Exercise — Part B: Chain Reliability Experiment (15 min)

Build a 2-step chain:
- Step 1: Extract action items from a meeting transcript (5 items)
- Step 2: Classify each action item as `high | medium | low` priority

1. Run Step 1 on 3 transcripts. Count parse successes. Estimate Step 1 reliability.
2. Pipe Step 1 output into Step 2. Count end-to-end successes. Compare to predicted $r^2$.
3. Identify the most common failure mode. Add one guardrail to fix it.
4. Re-run. Did end-to-end reliability improve?

---

## Part 7 — Wrap-up & Connection · 15min

### Self-check

Before closing, tick each item:

- [ ] I can name the two structural causes of hallucination.
- [ ] I can select the right guardrail for a given failure mode without looking at the table.
- [ ] I can calculate end-to-end chain reliability given per-step reliability and chain length.
- [ ] I can explain why 90% per-step reliability is not good enough for a 5-step agent.
- [ ] I know how to build a 20-input prompt eval suite from scratch.
- [ ] I know when LLM-as-judge is acceptable and when it isn't.
- [ ] I can describe the 6-step iterative process for building a complex prompt.

### Connect Forward

Every pattern in this supplementary is an ingredient of the agent loop you will build in Week 7–9:

- **Guardrails** → tool-call validation in Week 7
- **Chain reliability math** → agent loop design and retry budget in Week 8
- **Prompt evals** → agent regression testing throughout Weeks 7–9
- **Iterative prompt building** → the workflow you will use every day of the internship

---

Return to the [Day 26 main lesson](index.md) if you haven't taken the knowledge check yet, or proceed to Week 7.

---

## Stuck?

Ask **oxtutor** to walk through any concept in this supplementary, generate additional chain reliability scenarios, or quiz you on the six guardrails and when to apply each.


