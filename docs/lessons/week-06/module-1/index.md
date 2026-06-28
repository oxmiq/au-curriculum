# Day 26 · Prompt Structure & Clarity

> **Concept of the day:** **clear, specific, structured prompts** beat clever ones. A model can't read your mind — give it role, context, task, format, and constraints **explicitly**. Anthropic tutorial Chapters 1–2.<br>
> **Pre-reading:** <a href="../../../readings/prompt-engineering/">Prompt Engineering Pre-Lecture Reading — Day 26 primer</a> (~10 min). Supplement: <a href="https://github.com/anthropics/prompt-eng-interactive-tutorial" target="_blank" rel="noopener">Anthropic Prompt Engineering Interactive Tutorial</a> (Ch 1 + Ch 2, ~20 min).

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

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m1-readiness" data-kind="readiness" data-draw="5" data-source="Anthropic Prompt Engineering Interactive Tutorial Ch 1-2">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the two structural slots in a chat-completion API call?",
    "options": [
      "Input and output",
      "System prompt and user messages",
      "Temperature and max tokens",
      "Prefill and decode"
    ],
    "answer": 1,
    "explain": "The two structural slots are: (1) System prompt — sets the model's behavior, role, and context, and (2) User messages — where you provide the actual task/input. The system prompt is like the 'environment' or 'persona' and the user message is the 'task'."
  },
  {
    "stem": "What is the primary purpose of the system prompt?",
    "options": [
      "To provide the actual task or question",
      "To set the model's behavior, role, and context",
      "To limit the model's output length",
      "To control the randomness of responses"
    ],
    "answer": 1,
    "explain": "The system prompt sets the model's behavior, role, and context. It's the 'environment' that shapes how the model responds to user messages. A good system prompt defines who the model is, what context it has, and how it should approach tasks."
  },
  {
    "stem": "Why does specificity generally produce better results than vague prompts?",
    "options": [
      "It reduces API costs",
      "The model can only follow explicit instructions, not infer implied intent",
      "It makes responses faster",
      "Specific prompts are always shorter"
    ],
    "answer": 1,
    "explain": "Specificity beats vagueness because LLMs can only follow explicit instructions — they can't read your mind or infer what you 'meant' to say. Vague prompts like 'write a good summary' leave too much to interpretation; specific prompts like 'write a 3-paragraph executive summary targeting C-suite readers' produce predictable results."
  },
  {
    "stem": "What is the difference between the system prompt and user messages in the chat API?",
    "options": [
      "There is no difference",
      "System prompt is persistent across turns; user messages are per-turn inputs",
      "System prompts are shorter than user messages",
      "User messages cannot contain instructions"
    ],
    "answer": 1,
    "explain": "In most APIs, the system prompt is set once and persists across the conversation, while user messages are the per-turn inputs. The system prompt defines the 'persona' and 'context' while each user message provides a specific task."
  },
  {
    "stem": "What is 'prefilling' in the context of LLM prompting?",
    "options": [
      "Providing the beginning of the model's response to guide its output",
      "Loading the model into memory",
      "Sending the first message in a conversation",
      "Configuring model parameters"
    ],
    "answer": 0,
    "explain": "Prefilling (also called 'prompt injection' or providing a 'response prefix') is providing the beginning of the model's response to guide its output. For example, if you want a JSON response, you might prefill with '{' to start the model in the right format."
  },
  {
    "stem": "What is the 'response prefix' technique in prompting?",
    "options": [
      "Starting every response with 'Hello'",
      "Providing the beginning of the desired output format",
      "The first message in a multi-turn conversation",
      "Repeating the prompt at the end of the response"
    ],
    "answer": 1,
    "explain": "Response prefix is providing the beginning of the desired output (like '{' for JSON or 'Sure, here is' for a helpful response) to guide the model into the right format. This is more reliable than asking the model to 'output JSON' after generating text."
  },
  {
    "stem": "What does it mean to 'give the model an escape hatch'?",
    "options": [
      "Allowing the model to refuse inappropriate requests",
      "Providing the model a way to indicate uncertainty or ask for clarification",
      "Letting the model generate unlimited output",
      "Removing all restrictions from the model"
    ],
    "answer": 1,
    "explain": "Giving an 'escape hatch' means providing the model a way to indicate uncertainty, say it doesn't know, or ask for clarification rather than making up an answer. This is part of building reliable, honest AI systems."
  },
  {
    "stem": "What is the key insight about prompting versus programming?",
    "options": [
      "They are the same thing",
      "Prompting is 'programming' with natural language — you need the same rigor as code",
      "Prompting is easier than programming",
      "Programming skills are not useful for prompting"
    ],
    "answer": 1,
    "explain": "Prompting is essentially 'programming' with natural language. Just like code, prompts can have bugs (vagueness, ambiguity, missing edge cases), and you need the same rigor: clear requirements, explicit instructions, testing edge cases, and iteration."
  }
]
</script>
</div>

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

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 26 · Prompt Engineering Fundamentals">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the two structural slots in a chat-completion API?",
    "options": [
      "Question and answer",
      "System message (instructions to the model) and user message (the actual input)",
      "Prompt and completion",
      "Context window and output buffer"
    ],
    "answer": 1,
    "explain": "Chat-completion APIs (e.g., OpenAI, Anthropic) have a system message — permanent instructions that shape behavior for the whole conversation — and a user message — the current input. Structuring prompts across these two slots correctly is a foundational prompt engineering skill."
  },
  {
    "stem": "Why does specificity beat vagueness in prompt engineering?",
    "options": [
      "Longer prompts always generate better outputs regardless of content",
      "Specific prompts constrain the model's output space to the intended task, reducing ambiguity and irrelevant responses",
      "Specific prompts are cached by the model, reducing inference cost",
      "Vague prompts cause syntax errors in the model"
    ],
    "answer": 1,
    "explain": "Vague prompts leave the model to guess intent, resulting in generic, off-target, or inconsistent outputs. Specificity (task + context + format + constraints) reduces the model's 'decision space' to what the user actually wants. The lesson's core principle: 'Specificity beats vagueness.'"
  },
  {
    "stem": "What does zero-shot prompting mean?",
    "options": [
      "Sending an empty prompt to see the model's default behavior",
      "Asking the model to perform a task without providing any examples of how to do it",
      "Running inference with zero temperature (fully deterministic output)",
      "Prompting the model with no system message"
    ],
    "answer": 1,
    "explain": "Zero-shot prompting asks the model to complete a task with no examples. Few-shot prompting provides K examples (shots) before the task. Zero-shot relies entirely on the model's pre-trained capabilities. Few-shot guides the model toward a specific format or reasoning style."
  },
  {
    "stem": "What does chain-of-thought (CoT) prompting do mechanically?",
    "options": [
      "It forces the model to output answers in a numbered list format",
      "It instructs the model to reason step-by-step before giving the final answer, improving accuracy on multi-step tasks",
      "It chains multiple model calls together, passing output as input",
      "It uses a sequence of fine-tuned adapters to improve coherence"
    ],
    "answer": 1,
    "explain": "Chain-of-thought prompting (e.g., 'Think step by step') causes the model to generate intermediate reasoning before the final answer. This improves accuracy on tasks requiring multi-step logic, math, or complex analysis — the model's own reasoning steps act as a working memory aid."
  },
  {
    "stem": "What are the three vagueness traps in prompt engineering?",
    "options": [
      "Too long, too technical, too creative",
      "No task definition, no output format, no constraints",
      "Wrong temperature, wrong token limit, wrong model",
      "Missing examples, missing context, missing persona"
    ],
    "answer": 1,
    "explain": "The three vagueness traps from the lesson are: (1) no clear task definition — the model doesn't know what to do; (2) no output format — the model picks its own structure; (3) no constraints — the model makes assumptions the user didn't intend. Each trap increases output variance."
  },
  {
    "stem": "Which of these is a complete well-structured prompt using the 6-component checklist?",
    "options": [
      "Summarize this.",
      "Tell me about AI.",
      "You are a technical writer. Summarize the following GPU benchmark report for a non-technical manager. Focus on cost and performance. Output exactly 3 bullet points, each under 20 words. Do not mention FLOPS or bandwidth. [report text]",
      "Be very helpful and give a great answer about machine learning."
    ],
    "answer": 2,
    "explain": "The 6-component checklist includes: role (technical writer), task (summarize), context (GPU benchmark report), audience (non-technical manager), constraints (3 bullets, 20 words, no FLOPS), and data (report text). Option C covers all six. Options A, B, D are vague or missing multiple components."
  }
]
</script>
</div>

### Connect Forward

Tomorrow: **roles, data separation, output formatting** — the patterns that turn a clear prompt into one safe to put into production code.

### Pre-read for tomorrow (Day 27 · Roles, Data, Output Formatting)

- **Resource:** <a href="../../../readings/prompt-engineering/">Prompt Engineering Pre-Lecture Reading — Day 27 primer</a> (~12 min). Supplement: <a href="https://github.com/anthropics/prompt-eng-interactive-tutorial" target="_blank" rel="noopener">Anthropic tutorial</a> Ch 3 + Ch 4 + Ch 5 (~20 min).
- **Reflection questions:**
  1. How does giving the model a **specific role** change its output quality? Why?
  2. What attack does proper data separation defend against?
  3. Why do production systems usually demand JSON output rather than prose?

---

## Stuck?

Ask **oxtutor** to re-explain any concept from today's lesson, or to generate extra practice questions on rewriting vague prompts.