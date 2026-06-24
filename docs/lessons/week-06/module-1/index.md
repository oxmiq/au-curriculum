# Day 26 · Prompt Structure & Clarity

> **Concept of the day:** **clear, specific, structured prompts** beat clever ones. A model can't read your mind — give it role, context, task, format, and constraints **explicitly**. Anthropic tutorial Chapters 1–2.<br>
> **Pre-reading:** Anthropic Prompt Engineering Interactive Tutorial — **Chapter 1 (Basic Prompt Structure)** + **Chapter 2 (Being Clear and Direct)** (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 6 — Prompt Engineering + AI Agents</a>
    <span class="sep">/</span>
    <span>Day 26 · Prompt Engineering</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-06/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Prompt Anatomy | 20 min |
| Part 3 | Deep Dive: The Three Vagueness Traps | 20 min |
| Part 4 | Hands-On: Rewrite Vague Prompts | 30 min |
| Part 5 | Hands-On: Prompt Checklist Practice | 25 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review · 15 min
### Before You Start

You should have already read: Anthropic Prompt Engineering Interactive Tutorial — **Chapter 1 (Basic Prompt Structure)** + **Chapter 2 (Being Clear and Direct)** (~20 min).

### Quick Self-Check

Answer these questions from memory:
1. What are the two structural slots in a chat-completion API call?
2. What's the difference between the system prompt and user messages?
3. Why does specificity beat vagueness in prompting?

If you couldn't answer all three, review the tutorial chapters again before proceeding.

---

## Part 2 — Core Concepts: Prompt Anatomy · 20 min
### Reading — Why This Matters

Prompts are how you program an LLM. The single biggest source of bad output is **ambiguous instruction**, not model capability. By the end of this week you should be able to look at a failing prompt and say *what's missing* with the same fluency as debugging code.

### The Chat-Completion API Shape

Every modern chat-completion API has roughly this shape:

```
POST /v1/chat/completions
{
  "model": "claude-3-5-sonnet",
  "messages": [
    { "role": "system", "content": "<instructions to the model>" },
    { "role": "user",   "content": "<the user's turn>" },
    { "role": "assistant", "content": "<the model's reply>" },
    { "role": "user",   "content": "<next user turn>" }
  ],
  "temperature": 0.0,
  "max_tokens": 1024
}
```

### Two Structural Slots

| Slot | Purpose | Example |
|------|---------|---------|
| **System prompt** | Instructions that apply to the whole conversation | "You are a senior code reviewer. Focus on security bugs." |
| **User turn(s)** | The actual question, data, or task | "Review this diff and find race conditions." |

> **Key insight:** The model sees system and user concatenated with role markers. From the model's point of view, they're not magically different — but the **convention** matters. System instructions are stable across turns; user content is the per-turn payload.

### Why Two Slots Matter

1. **Caching:** Anthropic and others cache the system prompt prefix, so you pay per-token once and reuse it across requests — huge savings at scale.
2. **Discipline:** Separating "rules" from "data" stops you from accidentally rewriting rules every turn.

---

## Part 3 — Deep Dive: The Three Vagueness Traps · 20 min
### Reading — Specificity Beats Vagueness

The model is a probability machine over text. Give it a vague instruction → it samples from the broad distribution of valid completions. Give it a specific one → the distribution narrows to what you actually wanted.

### Trap 1: Undefined Audience

**Bad:** "Explain what a GPU is."
**Problem:** For whom? A 5-year-old? A CS undergrad? A datacenter engineer?
**Fix:** "Explain what a GPU is to a second-year computer science undergraduate who knows what a CPU is but has never written CUDA code. Use one analogy and one concrete example."

### Trap 2: Undefined Format

**Bad:** "List the top 5 inference frameworks."
**Problem:** Bulleted? Numbered? JSON? With descriptions?
**Fix:** "List the top 5 open-source LLM inference frameworks (vLLM, TensorRT-LLM, etc.) as a markdown table with columns: Name, Primary Language, Best Use Case, License. Sort by GitHub stars descending."

### Trap 3: Undefined Success Criteria

**Bad:** "Write a summary of this paper."
**Problem:** How long? Technical depth? Style? Bullets or prose?
**Fix:** "Write a 150-word summary of the paper below for a technical reader. Cover: (1) what problem it solves, (2) the core mechanism, (3) one limitation. Use plain prose, no bullets."

### The Rule

> **If a junior engineer would need to ask a clarifying question, the LLM does too.**

---

## Part 4 — Hands-On: Rewrite Vague Prompts · 30 min
### Exercise 1: Identify the Trap (15 min)

For each vague prompt, identify which trap it falls into (Undefined Audience, Undefined Format, or Undefined Success Criteria), then rewrite it:

| Vague Prompt | Trap | Rewrite |
|--------------|------|---------|
| "Explain Docker" | | |
| "Write a function to download a file" | | |
| "Summarize this article" | | |
| "Tell me about AI" | | |
| "List the best GPUs" | | |

### Exercise 2: Test Your Rewrites (15 min)

If you have access to an LLM:
1. Run the original vague prompt
2. Run your rewritten prompt
3. Compare the outputs

**What to look for:**
- Did the output change significantly?
- Which improvements gave the biggest output-quality jump?
- Was there anything you forgot to specify?

---

## Part 5 — Hands-On: Prompt Checklist Practice · 25 min
### Exercise: The 6-Component Prompt Checklist

Every well-formed prompt should have these components. Use this checklist:

| Component | Check | Your Prompt |
|-----------|-------|-------------|
| **Role** | Did you specify who the model is? | |
| **Context** | Did you provide background facts? | |
| **Task** | Is the concrete ask clear? | |
| **Input** | Is the data clearly marked? | |
| **Format** | Is the output shape specified? | |
| **Constraints** | Are hard rules stated? | |

### Practice: Real-World Refactor

Take one prompt from your real work (or these examples):

1. "Fix this code"
2. "Write a follow-up email"
3. "Explain transformer architecture"

For each:
1. Identify what's missing from the 6-component checklist
2. Rewrite with all 6 components
3. Test against an LLM if possible

### Personal Prompt Checklist

Write your own "prompt checklist" sticky note (max 6 items) that you'll reference when writing prompts:

```
My Prompt Checklist:
1. □
2. □
3. □
4. □
5. □
6. □
```

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you do these from memory?
- [ ] Name the two structural slots in a chat-completion API
- [ ] Explain why specificity beats vagueness
- [ ] Identify the three vagueness traps
- [ ] Use the 6-component prompt checklist

### Connect Forward

Tomorrow: **roles, data separation, output formatting** — the patterns that turn a clear prompt into one safe to put into production code.

### Pre-read for tomorrow (Day 27 · Roles, Data, Output Formatting)

- **Resource:** Anthropic tutorial **Ch 3 (Roles)** + **Ch 4 (Separating Data and Instructions)** + **Ch 5 (Output Formatting)** (~25 min).
- **Reflection questions:**
  1. How does giving the model a **specific role** change its output quality? Why?
  2. What attack does proper data separation defend against?
  3. Why do production systems usually demand JSON output rather than prose?

---

## Stuck?

Ask **oxtutor** to re-explain any concept from today's lesson, or to generate extra practice questions on rewriting vague prompts.