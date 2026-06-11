# Day 24 · Cost & Economics

> **Concept of the day:** **cost / million tokens** = (GPU $/hour × hours) / (tokens served × utilization). **Decode dominates** end-to-end cost for chat workloads. **Dedicated breaks even with API** somewhere around 30–50% utilization.
> **Pre-reading:** "Cost of inference" blog with worked numbers — Pre-Lecture Reading **Reader 10** (~15 min).
> **Source:** [Study Guide §A.7 economics](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

This is the *third leg* of the SLO tripod: latency, quality, **cost**. Every choice in Phase 1 has a cost implication. By the end of today you should be able to give a number for "what does our deployment cost per million output tokens?" — and defend it.

## Readiness check

1. Why does **decode** typically dominate total cost in chat?
2. Define **cost per million tokens** in one formula.
3. What's the rough hourly cost of an 8×H100 instance on a major cloud (2024–25)?
4. At what utilization does a dedicated 8×H100 break even with paying per token via an API?
5. What's the cheapest knob you can pull to cut cost / 1M tokens *without* changing the model?

## Core concept

### The cost formula

> **Cost per 1M output tokens = (GPU $/hour × hours of usage) / (1M output tokens served at that utilization)**

Equivalently:

> **Cost / 1M tokens = $ per GPU-hour / (utilization × tokens-per-GPU-hour)**

Three levers:

1. **$ per GPU-hour** — hardware choice, contract length, region.
2. **Tokens-per-GPU-hour at full util** — engine + model + parallelism (Weeks 3–4).
3. **Utilization** — what fraction of paid GPU time you're actually serving tokens.

### Worked example — Llama-3-70B FP16 on 8×H100

Assumptions (rough, 2024–25):

- 8×H100 on-demand: **~$30/hour** (varies wildly: $20 spot to $50 reserved).
- Peak decode throughput at TP=8, large batch: **~3000 tokens/sec aggregate**.
- Hours per month: 730.

At **100% utilization** (impossible, but the ceiling):
- Tokens / hour = 3000 × 3600 = 10.8M
- Cost / 1M tokens = $30 / 10.8 = **$2.78**

At **realistic 40% utilization**:
- Cost / 1M tokens = $30 / (10.8 × 0.4) = **$6.94**

API pricing (Llama-3-70B class via fireworks/together/etc.): **~$0.60–$1.00 / 1M output tokens** mid-2024.

> **Conclusion:** for low utilization, API is much cheaper. Dedicated breaks even around **35–60% sustained utilization** for general-purpose inference.

### Why decode dominates cost

A typical chat request: 500 input tokens, 1500 output tokens. Prefill is one parallel pass (fast); decode is 1500 sequential passes (slow). For most workloads, **70–90% of GPU-time is spent in decode** — so per-token cost is essentially per-output-token cost.

(Exceptions: RAG with huge prompts and short outputs invert this.)

### When dedicated wins

| Condition | Verdict |
|---|---|
| Sustained > 50% utilization, 24/7 | Dedicated wins, possibly big |
| Bursty, < 20% utilization | API wins |
| Need a custom fine-tune | Dedicated (or API w/ adapter support) |
| Data residency / privacy | Dedicated (or VPC-deployed API) |
| Want speed-of-experimentation | API |

### The levers in order of impact

| Lever | Typical cost reduction | Risk |
|-------|------------------------|------|
| Switch to FP8 weights + KV | 1.5–2× | Quality regression (Day 23) |
| Enable speculative decoding | 1.5–2.5× | Implementation complexity |
| Continuous batching, no static | 5–10× | Already standard in vLLM |
| Spot / reserved GPU pricing | 2–4× | Availability / lock-in |
| Smaller model + better prompting | 5–10× | Quality regression — measure |
| Caching prefixes (system prompt) | 1.2–3× on prefill cost | None (free win) |

### Token-economics for product pricing

If you're building a product on top: **know your cost / token before pricing.** Two pitfalls:

1. **Long-context products** — KV cache blows up cost per request 10× at 128K. Charge for context.
2. **Multi-turn agentic** — Week 7's agents make 10–50 LLM calls per "task." Cost / task ≠ cost / call.

## Practice (90 min)

1. (15 min) Re-derive cost / 1M tokens for the Week 4 system at 30%, 50%, 70% utilization. Plot mentally.
2. (25 min) Pick an API price point ($0.80 / 1M output tokens). At what monthly token volume does buying 8×H100 (~$30/hr × 730 = $21,900/mo) break even at 40% util?
3. (25 min) Pair: estimate cost / task for a "research agent" that makes 30 LLM calls of 500/2000 token I/O average. Per call, then per task.
4. (15 min) Discussion: when is "scale to zero overnight" a false economy for LLM serving? (Hint: cold starts.)
5. (10 min) Write the rule: *"Dedicated wins when ___; API wins when ___."*

## Wrap-up

Cohort produces a one-page **cost model** for the Week 4 system. Includes: $/hr, peak TPS, expected utilization, $/1M tokens at each util, API break-even.

## Connect forward

Friday: Phase 1 wrap. **[The canonical quiz](knowledge-check.html)** is the 15% open-book assessment. Tomorrow is reflection + Phase 2 (Prompt Engineering) pre-read.

---

## Pre-read for Friday (Day 25 · Phase 1 Wrap)

- **Resource:** Skim the Inference Engineering Glossary one more time. Bring your Week 3 calculator, Week 4 design doc, and today's cost model.
- **Reflection questions:**
  1. Of everything in Phase 1, what's the *one* concept you'd teach a new joiner first?
  2. What concept are you *least* sure of?
  3. For the cost model above — what's the single change you'd push for to cut cost in half? Justify with one number.
