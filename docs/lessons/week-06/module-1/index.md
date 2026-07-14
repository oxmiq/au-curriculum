# Day 26 · Prompt Structure & Clarity

> **Concept of the day:** **clear, specific, structured prompts** beat clever ones. A model can't read your mind; give it role, context, task, format, and constraints **explicitly**. Anthropic tutorial Chapters 1–2.<br>
> **Pre-reading:** <a href="../../../readings/prompt-engineering/#day-26-primer-why-the-same-question-gives-different-answers">Prompt Engineering Pre-Lecture Reading - Day 26 primer</a>. Supplement: <a href="https://github.com/anthropics/prompt-eng-interactive-tutorial" target="_blank" rel="noopener">Anthropic Prompt Engineering Interactive Tutorial</a> (Ch 1 + Ch 2).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 6 - Prompt Engineering + AI Agents</a>
    <span class="sep">/</span>
    <span>Day 26 · Prompt Engineering</span>
    {status:week-06/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Prompt Anatomy |
| Part 3 | Deep Dive: The Three Vagueness Traps |
| Part 4 | Hands-On: Rewrite Vague Prompts |
| Part 5 | Hands-On: Prompt Checklist Practice |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: Anthropic Prompt Engineering Interactive Tutorial - **Chapter 1 (Basic Prompt Structure)** + **Chapter 2 (Being Clear and Direct)**.

### Quick Self-Check

Answer these questions from memory:

1. What are the two structural slots in a chat-completion API call?
2. What's the difference between the system prompt and user messages?
3. Why does specificity beat vagueness in prompting?

If you couldn't answer all three, review the tutorial chapters again before proceeding.

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m1-readiness" data-kind="readiness" data-draw="5" data-source="Prompt Engineering Day 26 Primer + Anthropic Tutorial Ch 1-2">
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
    "explain": "The two structural slots are: (1) System prompt - sets the model's behavior, role, and context, and (2) User messages - where you provide the actual task/input. The system prompt is like the 'environment' or 'persona' and the user message is the 'task'."
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
    "explain": "Specificity beats vagueness because LLMs can only follow explicit instructions; they can't read your mind or infer what you 'meant' to say. Vague prompts like 'write a good summary' leave too much to interpretation; specific prompts like 'write a 3-paragraph executive summary targeting C-suite readers' produce predictable results."
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
    "stem": "Why can the same prompt produce two different answers on repeated runs?",
    "options": [
      "The model retrieves a stored answer that changes over time",
      "The model samples each next token from a probability distribution, so runs can differ",
      "The model is being retrained between requests",
      "Network latency changes the output"
    ],
    "answer": 1,
    "explain": "An LLM doesn't retrieve an answer; it samples the next token from a probability distribution, token by token. With temperature above 0, different runs can sample different tokens, producing different completions. That is why the same prompt can give different answers."
  },
  {
    "stem": "What does setting temperature = 0 do?",
    "options": [
      "Disables the model",
      "Makes sampling deterministic: the model always picks the most likely next token",
      "Removes the system prompt",
      "Doubles the response speed"
    ],
    "answer": 1,
    "explain": "temperature = 0 gives deterministic (greedy) sampling: the model always takes the most likely next token, so the same prompt yields the same output. Most production systems run around 0.7 because deterministic outputs are less flexible."
  },
  {
    "stem": "In the Day 26 mental model, what does every word you add to a prompt do?",
    "options": [
      "It slows the model down proportionally",
      "It moves probability mass around: shaping the model's next-token distribution",
      "It is stored in the model's long-term memory",
      "Nothing until you press enter twice"
    ],
    "answer": 1,
    "explain": "The primer's mental model: the model has a probability distribution over completions, and your prompt determines its shape. A vague prompt produces a broad distribution (many completions about equally likely); a specific prompt produces a sharp one. Every word moves probability mass; prompt engineering is shaping that distribution."
  },
  {
    "stem": "What is the key insight about prompting versus programming?",
    "options": [
      "They are the same thing",
      "Prompting is 'programming' with natural language; you need the same rigor as code",
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

## Part 2 - Core Concepts: Prompt Anatomy
### Reading - Why This Matters

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

> **Key insight:** The model sees system and user concatenated with role markers. From the model's point of view, they're not magically different; but the **convention** matters. System instructions are stable across turns; user content is the per-turn payload.

### Why Two Slots Matter

1. **Caching:** Anthropic and others cache the system prompt prefix, so you pay per-token once and reuse it across requests: huge savings at scale.
2. **Discipline:** Separating "rules" from "data" stops you from accidentally rewriting rules every turn.

---

## Part 3 - Deep Dive: The Three Vagueness Traps
### Reading - Specificity Beats Vagueness

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

## Part 4 - Hands-On: Rewrite Vague Prompts
### Exercise 1: Identify the Trap

For each vague prompt, identify which trap it falls into (Undefined Audience, Undefined Format, or Undefined Success Criteria), then rewrite it:

| Vague Prompt | Trap | Rewrite |
|--------------|------|---------|
| "Explain Docker" | | |
| "Write a function to download a file" | | |
| "Summarize this article" | | |
| "Tell me about AI" | | |
| "List the best GPUs" | | |

### Exercise 2: Test Your Rewrites

If you have access to an LLM:

1. Run the original vague prompt
2. Run your rewritten prompt
3. Compare the outputs

**What to look for:**
- Did the output change significantly?
- Which improvements gave the biggest output-quality jump?
- Was there anything you forgot to specify?

---

## Part 5 - Hands-On: Prompt Checklist Practice
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

## Part 7 - Wrap-up & Connection
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
    "explain": "Chat-completion APIs (e.g., OpenAI, Anthropic) have a system message, permanent instructions that shape behavior for the whole conversation, and a user message: the current input. Structuring prompts across these two slots correctly is a foundational prompt engineering skill."
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
    "stem": "Why do production systems separate the system prompt from the user turn(s)?",
    "options": [
      "The model executes them in two separate processes",
      "It doubles the effective context window",
      "The system-prompt prefix can be cached and reused across requests, and separating stable rules from per-turn data keeps you from rewriting the rules every turn",
      "User turns are encrypted while system prompts are not"
    ],
    "answer": 2,
    "explain": "The lesson gives two reasons the two slots matter: (1) Caching - Anthropic and others cache the system-prompt prefix, so you pay for those tokens once and reuse them across requests; (2) Discipline - separating 'rules' (system) from 'data' (user turn) stops you from accidentally rewriting the rules on every turn."
  },
  {
    "stem": "The 6-component prompt checklist is Role, Context, Task, Input, Format, and which sixth component?",
    "options": [
      "Temperature",
      "Examples",
      "Audience",
      "Constraints"
    ],
    "answer": 3,
    "explain": "The lesson's 6-component checklist is Role, Context, Task, Input, Format, and Constraints. Constraints are the hard rules the output must obey (length limits, forbidden content, required tone). 'Audience' and 'Examples' are useful but are not the sixth named component in this checklist."
  },
  {
    "stem": "What are the three vagueness traps covered in the lesson?",
    "options": [
      "Undefined Audience, Undefined Format, Undefined Success Criteria",
      "Undefined Length, Undefined Tone, Undefined Language",
      "No role, no context, no examples",
      "Wrong temperature, wrong token limit, wrong model"
    ],
    "answer": 0,
    "explain": "The three vagueness traps are: (1) Undefined Audience - for whom? (a 5-year-old, a CS undergrad, a datacenter engineer?); (2) Undefined Format - bulleted, numbered, JSON, a table?; (3) Undefined Success Criteria - how long, what depth, what counts as done? The fix for each is to state the missing dimension explicitly."
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
    "explain": "Mapping option C to the 6-component checklist: Role (technical writer), Context (a GPU benchmark report, reader is a non-technical manager), Task (summarize), Input (the [report text]), Format (exactly 3 bullet points, each under 20 words), and Constraints (do not mention FLOPS or bandwidth). It covers all six components; options A, B, and D are vague or missing multiple components."
  },
  {
    "stem": "The prompt 'Explain what a GPU is' primarily falls into which vagueness trap?",
    "options": [
      "Undefined Format",
      "Undefined Success Criteria",
      "No trap - it is specific enough",
      "Undefined Audience"
    ],
    "answer": 3,
    "explain": "In the lesson this is the Trap 1 (Undefined Audience) example: it never says for whom; a 5-year-old, a CS undergrad, or a datacenter engineer would all need different explanations. The fix names the audience and their prior knowledge (e.g., 'a second-year CS undergrad who knows what a CPU is but has never written CUDA')."
  },
  {
    "stem": "What heuristic does the lesson give for deciding whether a prompt is specific enough?",
    "options": [
      "If a junior engineer would need to ask a clarifying question, the LLM does too",
      "If the prompt is over 100 words, it is specific enough",
      "If the prompt contains a role, it is complete",
      "If temperature is set to 0, specificity no longer matters"
    ],
    "answer": 0,
    "explain": "The lesson's rule: 'If a junior engineer would need to ask a clarifying question, the LLM does too.' Any ambiguity a capable human would need resolved is ambiguity the model will otherwise resolve by guessing; so specify it up front."
  }
]
</script>
</div>

### Connect Forward

Tomorrow: **roles, data separation, output formatting** - the patterns that turn a clear prompt into one safe to put into production code.

### Pre-read for tomorrow (Day 27 · Roles, Data, Output Formatting)

- **Resource:** <a href="../../../readings/prompt-engineering/#day-27-primer-roles-walls-and-shapes">Prompt Engineering Pre-Lecture Reading - Day 27 primer</a>. Supplement: <a href="https://github.com/anthropics/prompt-eng-interactive-tutorial" target="_blank" rel="noopener">Anthropic tutorial</a> Ch 3 + Ch 4 + Ch 5.
- **Reflection questions:**
  1. How does giving the model a **specific role** change its output quality? Why?
  2. What attack does proper data separation defend against?
  3. Why do production systems usually demand JSON output rather than prose?

---

## Stuck?

Ask **oxtutor** to re-explain any concept from today's lesson, or to generate extra practice questions on rewriting vague prompts.