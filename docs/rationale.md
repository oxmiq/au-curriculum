# Why this curriculum

> Why this sequence, at this depth, at this pace - and what we deliberately leave out.

## The gap

Most CS programs teach AI as a science: papers, algorithms, loss functions, training. Industry needs AI as engineering: latency budgets, GPU economics, system reliability. Graduates can train a model in a notebook. They can't serve one. They understand attention mathematically. They have never thought about why decode is memory-bandwidth-bound, or what that implies for hardware selection.

This curriculum closes that gap: not by cramming, but by building intuition one concept at a time.

## Why 10 weeks, half-day

Knowledge doesn't transfer by passively absorbing information. It transfers through practice, sleep, spaced repetition, and explaining what you've learned to others. A 30-day intensive denies you three of those four. Spread to 10 weeks at half-days:

- Afternoons become processing time, not more input.
- Overnight sleep consolidates the morning's concept.
- Friday reviews create spacing.
- Collaborative work creates opportunities to teach others.

Learners who feel overwhelmed shut down; learners who feel competent lean in. One concept per day means you finish each day having understood today's idea. That confidence compounds.

Depth beats breadth: deeply understanding 40 concepts retains better than being exposed to 80 and remembering 20.

## Why this sequence

**Inference engineering first**: because it fills the biggest gap. Every learner here has studied transformers. None have studied *how* a transformer runs on a GPU at production scale. Four weeks, not two, because the layers stack:

- Week 2: where does inference happen? (hardware)
- Week 3: what is the central problem? (KV cache, memory)
- Week 4: how do you scale it? (parallelism, speculation)
- Week 5: how do you measure and pay for it? (metrics, economics)

No week makes sense without the one before it.

**Prompt engineering next**: the bridge. The same prompt produces different behaviour on different stacks; you can't reason about that without Phase 1, and you can't build agents without it.

**Agents after**: the application context. Without the agent framing, inference engineering is optimization in a vacuum. With it, you understand *why* latency matters (agents run in loops; every token of latency compounds), *why* tool calling must be fast and reliable, *why* governance is an engineering requirement, not a checkbox.

**Capsule next**: the proving ground. By the time you touch `capsule benchmark --tp 2 --quant awq`, every flag has meaning. Two weeks of hands-on, not a blitz, so you develop muscle memory, not just awareness.

**Capstone last**: where confidence becomes evidence. Selecting a model, justifying hardware, deploying, benchmarking, evaluating, recommending: these emerge from nine weeks of progressive understanding, not from cramming.

## Why this depth - and not deeper

Deep enough to reason. Not so deep you drown.

Forty distinct concepts across ten weeks. Each gets one full session: 60 minutes of explanation, 90 minutes of practice. A typical 3-day bootcamp "covers" the same material with 15 minutes per topic and no practice. The difference is that you can *explain* why PagedAttention exists (memory fragmentation in the KV cache). A bootcamp graduate can only *name* it.

What we deliberately leave out:

- **CUDA kernel programming**: important for engine developers; you are an operator and evaluator, not a kernel author.
- **Training techniques**: you learned this at university; we don't repeat it.
- **Paper-level math**: we cover the intuition behind attention and quantization, not the proofs.
- **Every GPU ever made**: H100 is the reference, B200 is the future, that's enough.

What stays is the *reasoning framework* that lets you understand new hardware and new techniques as they appear.

## Self-directed learning

Every session assumes you arrived having read 15–30 minutes of accessible material. This means:

- Session time isn't wasted on basic definitions.
- Learners who read carefully start ahead; those who don't discover gaps early through self-assessment: no shame, just valuable signal.
- Your study time focuses on deeper understanding because the pre-reading handled the foundations.

## What this is - and isn't

It **is**: a systems engineering program built progressively; half-day with room to breathe; one concept at a time; directly connected to real tools.

It **isn't**: a theory course (no proofs, no papers); a coding bootcamp (you already code); an information dump (one concept/day, never more); a pressure cooker (Fridays free, no surprise exams); a certification program (it produces skill, not credentials).

## Summary

| Choice | Why |
|---|---|
| 10 weeks, half-days | overnight consolidation and breathing room |
| One concept per day | mastery, not overwhelm |
| Pre-reading before every session | levels the playing field |
| Self-assessment (not exam) | catches gaps early, enables focused review |
| Friday consolidation | spacing effect; nobody falls irreversibly behind |
| Inference → Prompts → Agents → Capsule | each phase enables the next |
| 40% weight on the capstone | demonstrates judgment, not recall |
| Open-book, reasoning-based assessment | tests thinking, not memorization |
| Collaborative work throughout | teaching others is the deepest form of learning |

The goal isn't to produce learners who survived a gauntlet. It's to produce learners who *understand*, deeply, confidently, durably, how AI runs in production.

For the day-by-day map, see [Curriculum](curriculum.md).
