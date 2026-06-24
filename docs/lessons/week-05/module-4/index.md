# Day 24 · Cost & Economics

> **Concept of the day:** **cost / million tokens** = (GPU $/hour × hours) / (tokens served × utilization). **Decode dominates** end-to-end cost for chat workloads. **Dedicated breaks even with API** somewhere around 30–50% utilization.
> **Pre-reading:** "Cost of inference" blog with worked numbers — Pre-Lecture Reading **Reader 10** (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 24 · Cost & Economics</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-05/module-4}
  </div>
  <div class="ox-lesson-header__cta">
    <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
    <a class="md-button md-button--primary" href="knowledge-check.html">Knowledge check</a>
    <a class="md-button" href="assignment.md">Assignment</a>
    <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| # | What you do | Time |
|---|-------------|------|
| 1 | The Cost Formula | 15 min |
| 2 | Worked Example | 20 min |
| 3 | Calculate Your Cost | 25 min |
| 4 | Break-Even Analysis | 25 min |
| 5 | Cost Levers | 20 min |
| 6 | Build Your Cost Model | 25 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — The Cost Formula · 15 min

### Reading

This is the *third leg* of the SLO tripod: latency, quality, **cost**. Every choice in Phase 1 has a cost implication. By the end of today you should be able to give a number for "what does our deployment cost per million output tokens?" — and defend it.

### The Cost Formula

> **Cost per 1M output tokens = (GPU $/hour × hours of usage) / (1M output tokens served at that utilization)**

Equivalently:

> **Cost / 1M tokens = $ per GPU-hour / (utilization × tokens-per-GPU-hour)**

**Three levers:**
1. **$ per GPU-hour** — hardware choice, contract length, region
2. **Tokens-per-GPU-hour at full util** — engine + model + parallelism (Weeks 3–4)
3. **Utilization** — what fraction of paid GPU time you're actually serving tokens

### Why Decode Dominates

A typical chat request: 500 input tokens, 1500 output tokens. Prefill is one parallel pass (fast); decode is 1500 sequential passes (slow). For most workloads, **70–90% of GPU-time is spent in decode** — so per-token cost is essentially per-output-token cost.

---

## Part 2 — Worked Example · 20 min

### Reading — Llama-3-70B FP16 on 8×H100

Assumptions (rough, 2024–25):

- **8×H100 on-demand:** ~$30/hour (varies: $20 spot to $50 reserved)
- **Peak decode throughput** at TP=8, large batch: ~3000 tokens/sec aggregate
- **Hours per month:** 730

### At 100% Utilization (impossible, but the ceiling)

- Tokens / hour = 3000 × 3600 = 10.8M
- Cost / 1M tokens = $30 / 10.8 = **$2.78**

### At Realistic 40% Utilization

- Cost / 1M tokens = $30 / (10.8 × 0.4) = **$6.94**

### API Pricing Comparison

API pricing (Llama-3-70B class via fireworks/together/etc.): **~$0.60–$1.00 / 1M output tokens** mid-2024.

> **Conclusion:** For low utilization, API is much cheaper. Dedicated breaks even around **35–60% sustained utilization** for general-purpose inference.

---

## Part 3 — Calculate Your Cost · 25 min

### Exercise: Re-Derive Cost at Different Utilizations

Using the formula and the numbers above, calculate **cost / 1M tokens** at:

1. **30% utilization:** ___
2. **50% utilization:** ___
3. **70% utilization:** ___

**Show your work:**
```
Cost / 1M = $30 / (10.8M × utilization)
```

### Exercise: Fill in the Table

| Utilization | Tokens/hour | Cost/1M tokens |
|-------------|-------------|----------------|
| 30% | 10.8M × 0.3 = 3.24M | $30 / 3.24M = $9.26 |
| 50% | 10.8M × 0.5 = 5.4M | ___ |
| 70% | 10.8M × 0.7 = 7.56M | ___ |

---

## Part 4 — Break-Even Analysis · 25 min

### Exercise: When Does Dedicated Win?

**Scenario:**
- Your deployment: 8×H100 at $30/hour
- Monthly cost: $30 × 730 = **$21,900/month**
- API price: **$0.80 / 1M output tokens**

**Question:** At what monthly token volume does dedicated break even with the API at 40% utilization?

**Calculate:**
1. At 40% util, cost/1M = $6.94
2. To spend $21,900/month on API: $21,900 / $0.80 = ___ tokens/month
3. At 40% util on dedicated: $21,900 / $6.94 = ___ tokens/month

**The break-even point is when both cost the same.**

### When Dedicated Wins

| Condition | Verdict |
|-----------|---------|
| Sustained > 50% utilization, 24/7 | Dedicated wins, possibly big |
| Bursty, < 20% utilization | API wins |
| Need a custom fine-tune | Dedicated (or API w/ adapter support) |
| Data residency / privacy | Dedicated (or VPC-deployed API) |
| Want speed-of-experimentation | API |

---

## Part 5 — Cost Levers · 20 min

### Reading — The Levers in Order of Impact

| Lever | Typical Cost Reduction | Risk |
|-------|------------------------|------|
| Switch to FP8 weights + KV | 1.5–2× | Quality regression (Day 23) |
| Enable speculative decoding | 1.5–2.5× | Implementation complexity |
| Continuous batching, no static | 5–10× | Already standard in vLLM |
| Spot / reserved GPU pricing | 2–4× | Availability / lock-in |
| Smaller model + better prompting | 5–10× | Quality regression — measure |
| Caching prefixes (system prompt) | 1.2–3× on prefill cost | None (free win) |

### Discussion: Pick One Lever

If you could implement **one** change to cut your Week 4 deployment cost in half, which would it be?

**Justify with one number** — show the expected reduction.

---

## Part 6 — Build Your Cost Model · 25 min

### Exercise: One-Page Cost Model

Create a one-page cost model for your Week 4 serving system. Include:

1. **$/hour:** Hardware cost
2. **Peak TPS:** From your Week 3 + Week 4 calculations
3. **Cost / 1M tokens** at 30%, 50%, 70% utilization
4. **Break-even point** vs an API priced at $0.80 / 1M tokens
5. **One lever** you'd pull first to cut cost, with expected reduction

### Token Economics for Product Pricing

If you're building a product on top:

1. **Long-context products** — KV cache blows up cost per request 10× at 128K. Charge for context.
2. **Multi-turn agentic** — Week 7's agents make 10–50 LLM calls per "task." Cost / task ≠ cost / call.

### Reflection Question

Write one sentence summarizing what you learned about cost:
> The three levers are: ___, ___, ___. The most impactful is ___.

---

## Part 7 — Wrap-up & Connection · 10 min

### Synthesis

Cost is the third SLO axis. With perplexity + task evals from yesterday and cost numbers from today, you now have the full measurement framework for Phase 1. Tomorrow is the Phase 1 wrap — bring your cost model, Week 3 calculator, and Week 4 design doc.

### Pre-read for Friday (Day 25 · Phase 1 Wrap)

- **Resource:** Skim the Inference Engineering Glossary one more time. Bring your Week 3 calculator, Week 4 design doc, and today's cost model.
- **Reflection questions:**
  1. Of everything in Phase 1, what's the *one* concept you'd teach a new joiner first?
  2. What concept are you *least* sure of?
  3. For the cost model above — what's the single change you'd push for to cut cost in half? Justify with one number.

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
