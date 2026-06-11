---
drift: |
  Authored as one day of a 4-day prompt-engineering week in the previous architecture.
  In the new graph, prompt engineering is collapsed to a SINGLE module (week-06/module-1)
  before the four agent modules. Day 27/28/29 of the original week are preserved in this
  folder as `supplementary-02-roles-data-formatting.md`, `supplementary-03-cot-few-shot.md`,
  and `supplementary-04-hallucinations-evals.md` for self-study; the canonical knowledge
  check for this module should sample lightly across all four topics. Future authoring may
  rewrite this page to be a 1-day overview rather than the original Day-1 deep dive.
---

# Day 26 · Prompt Structure & Clarity

> **Concept of the day:** **clear, specific, structured prompts** beat clever ones. A model can't read your mind — give it role, context, task, format, and constraints **explicitly**. Anthropic tutorial Chapters 1–2.
> **Pre-reading:** Anthropic Prompt Engineering Interactive Tutorial — **Chapter 1 (Basic Prompt Structure)** + **Chapter 2 (Being Clear and Direct)** (~20 min).
> **Source:** [Student Guide Module 1](../../../../planning/source-material/Prompt%20Engineering/Prompt-Engineering-Student-Guide.md) · [Pre-Lecture Reading](../../../../planning/source-material/Prompt%20Engineering/Prompt-Engineering-Pre-Lecture-Reading.md). Supplementary deep-dives on roles/data/formatting, CoT/few-shot, and hallucinations/evals live as `supplementary-*.md` files in this folder.

---

## Why this matters

Prompts are how you program an LLM. The single biggest source of bad output is **ambiguous instruction**, not model capability. By the end of this week you should be able to look at a failing prompt and say *what's missing* with the same fluency as debugging code.

## Readiness check

1. What's the difference between a **system prompt** and a **user message**?
2. Name the five components every well-formed prompt should have.
3. Why is "summarize this" usually a bad prompt? Fix it.
4. What does "the model can't read your mind" mean in practice?
5. Why does **specifying output format** help quality even when format doesn't matter?

## Core concept

### Prompt anatomy

A well-formed prompt has — explicitly — these components:

| Component | What it does | Example |
|---|---|---|
| **Role** | Who is the model | "You are a senior code reviewer." |
| **Context** | Background facts | "The codebase is a Python serving stack using vLLM." |
| **Task** | The concrete ask | "Review the diff below and identify potential race conditions." |
| **Input** | The data | (the diff, marked with delimiters) |
| **Format** | Shape of the output | "Output a numbered list. For each issue: file, line, severity (high/med/low), one-sentence fix." |
| **Constraints** | Hard rules | "Do not invent code that isn't in the diff. If nothing is wrong, say 'No issues found.'" |

Missing any of these and the model will guess — usually badly.

### Be clear, not clever

> *"Summarize this"* — bad. What kind of summary? For whom? How long?
> *"In 3 bullet points for a busy engineering manager, summarize what this PR changes and what risk it introduces"* — good.

The rule: **if a junior engineer would need to ask a clarifying question, the LLM does too.**

### Markdown / delimiters

Use clear delimiters around input data. The model treats `<document>...</document>` or `"""...."""` as data, not instructions. This prevents accidental **prompt injection** (Day 28 + Day 29 + Week 7).

### One-sentence rules

- **Specify length** — "in 50 words" gets a ~50-word answer; "concisely" gets anywhere from 5 to 500.
- **Specify audience** — "explain to a 10-year-old" vs "explain to an ML researcher."
- **Specify format** — JSON, bullets, table, prose. Doesn't matter if you don't need it; helps quality.
- **Specify what NOT to do** — "do not include disclaimers" is often as valuable as positive instructions.

## Practice (90 min)

1. (15 min) Take three vague prompts and rewrite each into the 6-component form. Examples: *"explain Docker," "fix this code," "write a follow-up email."*
2. (20 min) Run the rewrites in your preferred LLM client. Note which improvements gave the biggest output-quality jump.
3. (25 min) Pair drill: one person writes a vague prompt, the other interrogates them with clarifying questions a junior engineer would ask. Then re-write together.
4. (20 min) Lab: take one prompt from your real work. Apply the 6-component refactor. A/B test old vs new.
5. (10 min) Write a personal "prompt checklist" sticky note.

## Wrap-up

Cohort shares: *the single biggest output-quality jump from today's rewrites.*

## Connect forward

Tomorrow: **roles, data separation, output formatting** — the patterns that turn a clear prompt into one safe to put into production code.

---

## Pre-read for tomorrow (Day 27 · Roles, Data, Output Formatting)

- **Resource:** Anthropic tutorial **Ch 3 (Roles)** + **Ch 4 (Separating Data and Instructions)** + **Ch 5 (Output Formatting)** (~25 min).
- **Reflection questions:**
  1. How does giving the model a **specific role** change its output quality? Why?
  2. What attack does proper data separation defend against?
  3. Why do production systems usually demand JSON output rather than prose?
