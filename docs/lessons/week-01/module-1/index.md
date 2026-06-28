# Day 1 · Welcome & Context

> **Concept of the day:** What is Oxmiq? Why remote GPUs matter. The 10-week journey.<br>
> **Pre-reading:** None — first day.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 — Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 1 · Welcome & Context</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-01/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Read: Why This Matters | 10 min |
| Part 2 | Read: Core Concepts | 20 min |
| Part 3 | Deep Dive: 10-Week Journey | 15 min |
| Part 4 | Hands-On: Research Capsule | 30 min |
| Part 5 | Hands-On: Write Your Summary | 30 min |
| 7 | Reflection: Connect Forward | 15 min |

---

## Part 1 — Why This Matters · 10 min
### Reading

You're about to spend 10 weeks learning how GPU inference works, how agents are built, and how Capsule is operated. That's a lot. Today is the only day that's *just* context — every day after this is technical content. Use today to internalize the "why."

This foundational understanding will inform every technical decision you make in Weeks 2-10. When you're debugging aKV cache issue in Week 3 or optimizing a prompt in Week 6, you'll need to recall *why* these systems exist in the first place.

### Reflection (write your answer)

Take 2 minutes to write down:
> What do you currently think Capsule does? (No wrong answer — this is a baseline.)

---

## Part 2 — Core Concepts · 20 min
### Reading — What Oxmiq Does (in three sentences)

1. **Oxmiq Labs builds Capsule** — a platform that lets engineers and researchers use remote GPU machines (NVIDIA H100, Tenstorrent, AMD MI300, Apple Silicon, etc.) as if they were sitting on their own desk.

2. **The problem Capsule solves:** GPUs are expensive (an 8×H100 box rents for ~$24/hour, ~$17K/month), scarce, and operationally painful. Most teams can't justify owning them; the ones who do, can't keep them busy. Capsule turns a fleet of GPUs into a self-service utility.

3. **Where you fit in:** by the end of Week 10 you can take a model, pick the right GPU + serving config + quantization, benchmark it on Capsule, and write a recommendation that an engineering manager would act on. That's a hireable engineer.

### Key Terms to Understand

| Term | Definition |
|------|------------|
| **GPU Inference** | Running a trained model to generate outputs (vs. training which learns) |
| **Remote GPU** | A GPU machine accessed over the network, not local to your machine |
| **Self-service utility** | A system where you can provision resources on-demand without manual tickets |

---

## Part 3 — The 10-Week Journey · 15 min
### Reading

Here's the roadmap you'll follow:

| Week | What you'll learn | Key Technologies |
|------|-------------------|------------------|
| 1 | Tooling — shell, git, GPU primer | Linux, bash, git |
| 2 | GPU hardware & memory bottlenecks | NVIDIA H100, memory hierarchy |
| 3 | Attention, KV cache, quantization | FlashAttention, AWQ, GPTQ |
| 4 | Multi-GPU scaling, speculative decoding, serving engines | vLLM, TensorRT-LLM |
| 5 | Metrics, production patterns, cost economics | TTFT, TPOT, throughput |
| 6 | Prompt engineering — the LLM-side companion to inference | Chain-of-thought, few-shot |
| 7 | AI agents — tools, governance, orchestration | ReAct, MCP, LangChain |
| 8 | Capsule foundations & operations (hands-on) | Capsule CLI, fleet management |
| 9 | Capsule benchmarking & evaluation (apply Phase 1) | Benchmarking, eval frameworks |
| 10 | Capstone — prove it independently | Your final project |

### How Each Day Works (Self-Study Version)

- **Part A** (10-20 min): Reading — understand the core concept
- **Part B** (20-30 min): Deep dive — explore the details
- **Part C** (30 min): Hands-on practice — apply what you learned
- **Part D** (15 min): Reflection — connect to tomorrow's content

**Fridays are consolidation days.** No new content. Practice, ask, catch up.
**Afternoons are free.** Learning needs space.

---

## Part 4 — Hands-On — Research Capsule · 30 min
### Exercise 1: Explore the Capsule Product (15 min)

1. Visit `oxmiq.com` and browse the product documentation
2. Look for information about:
   - What GPUs are available
   - How to connect to remote machines
   - Pricing model (if available)
3. Take notes on 3 things that surprise you

### Exercise 2: Watch the Demo (15 min)

If a demo video link is available, watch it. Otherwise, search for "Capsule platform demo" or similar.

Focus on:
- What does the user interface look like?
- How do you select a GPU?
- What's the workflow from model to output?

---

## Part 5 — Hands-On — Write Your Summary · 30 min
### Assignment: Three-Sentence Summary

Write a **three-sentence answer** to: *"What does Capsule do, and why does it exist?"*

Requirements:
- In your own words
- No jargon (or if you must use jargon, explain it)
- Include the problem it solves
- Include who it's for

**Example structure:**
> Capsule is [what it does]. It exists because [the problem]. It's useful for [who benefits].

### Peer Review (if available)

If you have a partner:
1. Read your three sentences to them
2. Ask: "Did you understand what Capsule does?"
3. Revise based on their feedback
4. Submit your final version

---

## Part 7 — Wrap-up & Connection · 15 min
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 1 · Welcome & Context">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the core problem that Capsule solves?",
    "options": [
      "It trains large language models faster",
      "It provides self-service remote GPU access so teams can use expensive hardware without owning it",
      "It replaces cloud storage with local SSDs",
      "It compresses model weights to reduce inference cost"
    ],
    "answer": 1,
    "explain": "Capsule turns a fleet of GPUs into a self-service utility. GPUs are expensive (~$24/hour for an 8×H100 box) and operationally painful to own. Capsule lets engineers and researchers use them on-demand over the network, as described in Part 2."
  },
  {
    "stem": "What is the difference between GPU training and GPU inference?",
    "options": [
      "Training uses CPUs; inference uses GPUs",
      "Training updates model weights via backpropagation; inference runs a forward pass to generate outputs",
      "Training is done once; inference is done at most three times",
      "Inference is always done on the same machine as training"
    ],
    "answer": 1,
    "explain": "Training modifies the model's weights by learning from data. Inference only reads those weights to produce outputs for new inputs. This distinction is fundamental to the 10-week curriculum, as explained in Part 2's Key Terms table."
  },
  {
    "stem": "By the end of Week 10, which of the following should you be able to do?",
    "options": [
      "Train a large language model from scratch on Capsule hardware",
      "Take a model, pick the right GPU + serving config + quantization, benchmark it on Capsule, and write a defensible recommendation",
      "Build a new GPU architecture to replace the H100",
      "Teach a deep-learning course to undergraduates"
    ],
    "answer": 1,
    "explain": "Part 2 states: \"by the end of Week 10 you can take a model, pick the right GPU + serving config + quantization, benchmark it on Capsule, and write a recommendation that an engineering manager would act on.\" That's the target hireable skill."
  },
  {
    "stem": "What is the approximate hourly cost of an 8×H100 GPU box?",
    "options": [
      "~$2/hour",
      "~$10/hour",
      "~$24/hour",
      "~$100/hour"
    ],
    "answer": 2,
    "explain": "Part 2 states: \"an 8×H100 box rents for ~$24/hour, ~$17K/month\". This number establishes why most teams can't justify owning them — and why Capsule's self-service model matters."
  },
  {
    "stem": "What happens every Friday in this 10-week program?",
    "options": [
      "New technical content is introduced",
      "Students take a graded exam worth 40% of the final grade",
      "Consolidation day — practice, Q&A, and catch-up; no new content",
      "Lectures from external industry speakers"
    ],
    "answer": 2,
    "explain": "Part 3 explains: \"Fridays are consolidation days. No new content. Practice, ask, catch up.\" Friday modules are also where weekly knowledge-check assessments live."
  },
  {
    "stem": "What does the term 'remote GPU' mean in the context of Capsule?",
    "options": [
      "A GPU that has been remotely updated with new firmware",
      "A GPU machine accessed over the network rather than physically attached to your workstation",
      "A GPU running inside a virtual machine with reduced performance",
      "A GPU shared between multiple cloud regions via DNS routing"
    ],
    "answer": 1,
    "explain": "Part 2 defines a remote GPU as: \"A GPU machine accessed over the network, not local to your machine.\" Capsule provides the tooling to make remote GPUs feel like local ones."
  },
  {
    "stem": "In what week of the program do students begin hands-on use of Capsule itself?",
    "options": [
      "Week 1",
      "Week 4",
      "Week 7",
      "Week 8"
    ],
    "answer": 3,
    "explain": "The Week-by-Week roadmap in Part 3 shows: Week 8 = \"Capsule foundations & operations (hands-on)\" and Week 7 bridges with agent case studies. The Capsule CLI itself is introduced in Week 7 module-2."
  }
]
</script>
</div>

### Reading

Tomorrow: the shell. Every operation in this curriculum — every git commit, every benchmark run, every Capsule command — starts with you in a terminal. We make sure you're fluent on Day 2 so it doesn't slow you down for the next 49 days.

### Pre-read for tomorrow (Day 2 · Shell & Linux)

**Resource:** <a href="https://missing.csail.mit.edu/2020/course-shell/" target="_blank" rel="noopener">MIT Missing Semester — Shell chapter</a> (~20 min, lecture 1 only).

**Reflection questions** (write your answers; bring them to the readiness check):
1. What's the difference between `ls` and `ls -la`?
2. Pipes (`|`) let you compose small commands into larger workflows. What's one example of two commands you'd pipe together?
3. Why is the shell still the primary tool for engineers in 2026, despite GUIs being everywhere?


## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
