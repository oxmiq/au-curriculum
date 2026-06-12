# Week 10 — Capstone Project

> **Goal:** independently demonstrate everything from Weeks 1–9. This is the hiring signal.
> **Format:** 2–3 person teams. 5 days. Live presentation on Day 49.
> **Deliverable (one sentence):** *"For use case X, deploy model Y at config Z, because [evidence from benchmark] shows [metric] at [cost], with [quality tradeoff] that is [acceptable / not] because [reasoning]."*

This guide contains: the kickoff brief, daily plan, presentation outline, assessment rubric, and retrospective form. Each file in this folder is one day's anchor.

---

## How the week runs

| Day | Theme | Output by end of day |
|---|---|---|
| 46 | Kickoff & planning | Approved project charter |
| 47 | Execute | Benchmark + chat eval results, raw |
| 48 | Analyze & recommend | Comparison tables + recommendation + slide deck |
| 49 | Present | 15-min talk + 10-min Q&A, panel-assessed |
| 50 | Close | 1:1 feedback + retrospective + career pointer |

---

## The deliverable (read this first, then keep re-reading)

Your final answer fits one sentence:

> *"For [use case], deploy [model] at [config], because [benchmark evidence] shows [metric] at [cost], with [quality tradeoff] that is [acceptable / not] because [reasoning]."*

Worked example:

> *"For a customer-support chatbot serving 5K queries/hour at P95 ≤ 800 ms, deploy **Llama-3.1-8B-Instruct** at **FP8 on 1×H100** with **continuous batching (concurrency=16)**, because Capsule benchmarks show **214 tokens/sec with P95 TTFT of 480 ms at $1.42/1M output tokens**, with **a 1.8-point drop on our 20-prompt eval suite** that is **acceptable because the failures are formatting-only, not factual.**"*

If your final sentence has hand-waves like "fast," "cheap," "good quality," you haven't finished the work. Real numbers, real tradeoffs, real evidence.

---

## What the panel will look for

The panel is your facilitator + 1–2 Oxmiq engineers. They aren't grading polish. They're checking three things:

1. **Can you reason like an engineer?** Did you pick the right knobs to vary? Did you control for everything else? Can you defend why your benchmark is meaningful, not arbitrary?
2. **Did you actually do the work?** Did you run real benchmarks on real machines, or did you cargo-cult numbers? Probes: "What surprised you?", "What did you try that didn't work?", "What would you do with another day?"
3. **Can you articulate a recommendation a manager can act on?** Numbers without a verdict = a report, not a recommendation. The whole point is the one-sentence answer above.

---

## Choosing a use case

Pick one of these (or propose your own, approved on Day 46):

| Use case | Latency target | Throughput target | Quality bar |
|---|---|---|---|
| Customer-support chatbot | P95 TTFT ≤ 800 ms | 5K queries/hr | factual + tone correct |
| Code completion in an IDE | P95 TTFT ≤ 300 ms | 100 req/min/seat | syntactically valid |
| Document summarization (background) | TPS ≥ 80 | 50 docs/min | preserves named entities |
| Internal RAG search assistant | P95 ≤ 2 s end-to-end | 200 queries/hr | cites correctly |
| Translation gateway | P95 ≤ 600 ms | 10K req/hr | BLEU within 2 pts of baseline |

Notice: every use case is **a target shape, not a vibes-shape**. Your team is graded on whether your recommendation defensibly hits the target.

---

## Choosing a model + hardware + quantization

You have access to (verify with facilitator on Day 46):

| Family | Sizes available | GPUs available |
|---|---|---|
| Llama 3.1 / 3.2 | 1B, 3B, 8B, 70B | 1×H100, 8×H100, 1×L4, 1×T4 |
| Gemma 3 | 1B, 4B | 1×H100, Tenstorrent n150 |
| GPT-OSS | 20B | 1×H100, 1×L4, 1×T4 |

Quantization options (varies by model): FP16 baseline, FP8, INT8, INT4 (AWQ/GPTQ).

You are not required to try every combination. You **are** required to defend your search strategy.

---

## Files in this folder (one per day)

- [Day 46 — Project Charter Template](Day-46-Charter-Template.md)
- [Day 47 — Execution Checklist](Day-47-Execution-Checklist.md)
- [Day 48 — Presentation Outline](Day-48-Presentation-Outline.md)
- [Day 49 — Assessment Rubric](Day-49-Assessment-Rubric.md)
- [Day 50 — Retrospective Form](Day-50-Retrospective-Form.md)

---

## Code of conduct for the week

- **No new techniques.** Use what you learned. The capstone tests synthesis, not novelty.
- **Document as you go.** A great recommendation built on undocumented experiments is unreproducible.
- **Ask before guessing.** Office hours are open all week. Facilitator can unblock you in 5 min that you'd otherwise lose in 5 hours.
- **Two-person rule for destructive ops.** Anything that deletes / restarts / reconfigures a shared machine: pair on it.
- **Commit and push every evening.** No "I'll commit when it's done."

Onwards.
