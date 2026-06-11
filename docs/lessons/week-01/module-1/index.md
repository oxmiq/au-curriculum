# Day 1 · Welcome & Context

> **Concept of the day:** What is Oxmiq? Why remote GPUs matter. The 10-week journey.
> **Pre-reading:** None — first day.
> **Source:** [Week 1 Orientation Student Guide § Day 1](../../../../planning/source-material/Orientation/Orientation-Student-Guide.md).

---

## Why this matters

You're about to spend 10 weeks learning how GPU inference works, how agents are built, and how Capsule is operated. Today is the only day that's *just* context — every day after this is technical content. Use today to internalize the "why."

## Readiness check

None today — first day.

In-class reflection (do during the readiness slot, not before):

1. What do you currently think Capsule does? (No wrong answer.)
2. What do you most want to learn in the next 10 weeks?
3. What's one thing about GPUs or AI infrastructure you've always wanted to ask but haven't?

## Core concept — What Oxmiq does (in three sentences)

1. **Oxmiq Labs builds Capsule** — a platform that lets engineers and researchers use remote GPU machines (NVIDIA H100, Tenstorrent, AMD MI300, Apple Silicon, etc.) as if they were sitting on their own desk.
2. **The problem Capsule solves:** GPUs are expensive (an 8×H100 box rents for ~$24/hour, ~$17K/month), scarce, and operationally painful. Most teams can't justify owning them; the ones who do, can't keep them busy. Capsule turns a fleet of GPUs into a self-service utility.
3. **Where you fit in:** by the end of Week 10 you can take a model, pick the right GPU + serving config + quantization, benchmark it on Capsule, and write a recommendation that an engineering manager would act on. That's a hireable engineer.

### The 10-week journey (one line each)

| Week | What you'll learn |
|---|---|
| 1 | Tooling — shell, git, GPU primer |
| 2 | GPU hardware & memory bottlenecks |
| 3 | Attention, KV cache, quantization |
| 4 | Multi-GPU scaling, speculative decoding, serving engines |
| 5 | Metrics, production patterns, cost economics |
| 6 | Prompt engineering — the LLM-side companion to inference |
| 7 | AI agents — tools, governance, orchestration |
| 8 | Capsule foundations & operations (hands-on) |
| 9 | Capsule benchmarking & evaluation (apply Phase 1) |
| 10 | Capstone — prove it independently |

### How each day works

- **Before class** (15–30 min): assigned pre-reading + 3 reflection questions you answer in writing.
- **0:00–0:20** Readiness check: 5-question quiz on pre-reading. Below 3/5 = paired with a buddy.
- **0:20–1:20** Concept lecture: one idea, analogy-first, demo, pause-and-check every 15 min.
- **1:30–3:00** Practice: guided exercise → open-ended challenge. Pair work encouraged.
- **3:00–3:30** Wrap-up: *you* summarize, not the instructor. Pre-reading for tomorrow assigned.
- **3:30–4:00** Office hours (optional).

**Fridays are consolidation days.** No new content. Practice, ask, catch up.
**Afternoons are free.** Learning needs space.

## Practice (~90 min)

1. Watch the Capsule demo (link provided in chat).
2. Browse `oxmiq.com` and any product docs your facilitator points you at.
3. Write a **three-sentence answer** to: *"What does Capsule do, and why does it exist?"* — in your own words, no jargon. This is also today's [assignment](assignment.md).
4. Pair up and read your three sentences to your partner. Revise based on their feedback.
5. Submit your final three sentences to your facilitator at end of session.

## Wrap-up

Students summarize, not the instructor. Connect today's "why" to tomorrow's "how."

## Connect forward

Tomorrow: the shell. Every operation in this curriculum — every git commit, every benchmark run, every Capsule command — starts with you in a terminal. We make sure you're fluent on Day 2 so it doesn't slow you down for the next 49 days.

---

## Pre-read for tomorrow (Day 2 · Shell & Linux)

- **Resource:** [MIT Missing Semester — Shell chapter](https://missing.csail.mit.edu/2020/course-shell/) (~20 min, lecture 1 only).
- **Reflection questions** (write your answers; bring them to the readiness check):
  1. What's the difference between `ls` and `ls -la`?
  2. Pipes (`|`) let you compose small commands into larger workflows. What's one example of two commands you'd pipe together?
  3. Why is the shell still the primary tool for engineers in 2026, despite GUIs being everywhere?
