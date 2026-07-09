# Day 25 (Fri) · Week 5 — Phase 1 Wrap (Assessment)

> **Phase 1 assessment.** This is the gate for Phase 2 (Prompt Engineering + Agents). Open-book, reasoning-focused.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 25 · Phase 1 Wrap</span>
    {status:week-05/module-5}
  </div>
  <div class="ox-lesson-header__cta">
    <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
    <a class="md-button md-button--primary" href="knowledge-check/">Knowledge check</a>
    <a class="md-button" href="assignment/">Assignment</a>
    <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Self-Study Time Buckets

This consolidation day is different from other days — it's for practice, review, and assessment. Here's how your ~3 hours are organized:

| Time Bucket | Activity Type |
|-------------|---------------|
| 🔵 Bucket 1 | Phase 1 Assessment |
| 🟢 Bucket 2 | Self-Assessment |
| 🟡 Bucket 3 | Practice: Metric Review |
| 🟠 Bucket 4 | Practice: Production Review |
| 🔴 Bucket 5 | Practice: Cost Model Review |
| 🟣 Bucket 6 | Open Lab & Wrap-up |

---

## 🔵 Bucket 1: Phase 1 Assessment

### Exercise: Take the Knowledge Check

[Take the Phase 1 assessment](knowledge-check.md) — 15 questions covering Weeks 2-5.

**Passing score:** 10/15 (67%)

This is **15% of the program grade**. The quiz is open-book — reasoning-focused.

### If You Score Below Passing

- Review the questions you got wrong
- Go back to the relevant day's content
- Re-read that section
- Retake the quiz after reviewing

---

## 🟢 Bucket 2: Self-Assessment

### Self-Check List

Go through each item and mark whether you can do it **without notes**:

**Week 2 — GPU Hardware**
- [ ] Explain why decode dominates cost in chat workloads
- [ ] Name three differences between H100 and A100
- [ ] Draw the memory hierarchy (HBM → L2 → registers)

**Week 3 — Attention & Quantization**
- [ ] Explain what KV cache is and why it matters
- [ ] Describe the difference between FP16 and FP8 quantization
- [ ] Calculate memory requirements for a 70B model at TP=8

**Week 4 — Serving Engines**
- [ ] Name two serving engines and their key features
- [ ] Explain continuous batching vs static batching
- [ ] Describe speculative decoding

**Week 5 — Metrics & Production**
- [ ] Define TTFT, ITL, TPS, P50, P95, P99
- [ ] Explain the latency-throughput tradeoff
- [ ] Build a cost model for a deployment
- [ ] List the three evaluation layers (perplexity, benchmarks, task evals)

### Action Items

For any item you can't do:
1. Note which week/day it came from
2. Spend 10 minutes reviewing that day's content
3. Practice until you can explain it from memory

---

## 🟡 Bucket 3: Practice — Metric Review

### Hands-On: Metric Drills

Practice these until they're automatic:

**Drill 1: Percentile Calculation**
Given: {50, 60, 70, 80, 90, 100, 110, 120, 150, 5000} ms
- Calculate mean: ___
- Calculate P50: ___
- Calculate P95: ___
- What does the mean hide?

**Drill 2: Metric Selection**
For each workload, pick the top metric:
- Chat/Q&A: ___
- Batch summarization: ___
- Code completion: ___
- Agentic tool calls: ___

**Drill 3: Goodhart's Law**
Complete the rule: "When a measure becomes a ___, it ceases to be a ___."
Always report a ___ of metrics with ___, not a single ___.

---

## 🟠 Bucket 4: Practice — Production Review

### Hands-On: Production Drills

**Drill 1: Autoscaler Design**
For a system with 8×H100, 50 req/s baseline, 200 req/s peak:
- What signal would you watch? ___
- What's your warm pool size? ___
- What's your max replicas? ___

**Drill 2: Rollout Strategy**
Pick the right strategy for each change:
- vLLM 0.4 → 0.5: ___
- FP16 → FP8 quantization: ___
- New tenant LoRA adapter: ___
- System prompt change: ___

**Drill 3: Failure Mode**
Draw the failure chain for "cold start during traffic spike":
1. Traffic spikes →
2. ___ →
3. ___ →
4. P99 TTFT spikes

---

## 🔴 Bucket 5: Practice — Cost Model Review

### Hands-On: Cost Model Drills

**Drill 1: Cost Formula**
Complete: Cost / 1M tokens = $___ / (___ × ___)

**Drill 2: Calculate at Utilization**
For 8×H100 at $30/hr, 3000 tokens/sec peak:
- At 30% util, cost/1M = ___
- At 50% util, cost/1M = ___
- At 70% util, cost/1M = ___

**Drill 3: Break-Even**
API price: $0.80/1M tokens
Dedicated: $30/hr
At what utilization does dedicated break even? ___

**Drill 4: Cost Levers**
Rank these by typical cost reduction (highest first):
1. FP8 quantization
2. Speculative decoding
3. Spot pricing
4. Continuous batching
5. Prefix caching

Answer: ___, ___, ___, ___, ___

---

## 🟣 Bucket 6: Open Lab & Wrap-up

### What to Do

This is open time. Choose what you need:

1. **Catch up** on any assignments from Mon–Thu
2. **Ask questions** — use oxtutor or review the relevant day
3. **Extra practice** — generate more exercises on any concept
4. **Complete your reflection assignment** — "The most important thing I learned in Weeks 2–5"

### Phase 2 Pre-Reading

Read **Phase 2 (Prompt Engineering) intro** from `planning/source-material/Prompt Engineering/` (file: `Prompt_Engineering_Student_Guide.md`, Modules 0–1).

Bring **one written question** to Week 6 Day 26.

### Connect Forward

Week 6 begins on Monday. You'll learn about:
- Prompt engineering fundamentals
- Chain-of-thought reasoning
- Few-shot learning
- Output structuring

### Big-Picture Connect

This week is the lens through which everything in Phase 1 becomes a *decision*:
- TTFT vs throughput
- Autoscale vs reserve
- FP16 vs FP8
- Dedicated vs API

By Friday, you can defend a cost model.

---

## Stuck?

Ask **oxtutor** to re-explain — Goodhart's Law and the percentile (P50/P95/P99) tension show up in every Friday discussion for the rest of the program.

---

## Pre-read for Monday (Week 6 · Day 26 · Prompt Engineering)

- **Resource:** <a href="../../../readings/prompt-engineering/#day-26-primer-why-the-same-question-gives-different-answers">Prompt Engineering Pre-Lecture Reading</a> — work through the Day 26 and Day 27 primers before Monday. Supplement: <a href="https://github.com/anthropics/prompt-eng-interactive-tutorial" target="_blank" rel="noopener">Anthropic Prompt Engineering Interactive Tutorial</a>.
- **Reflection questions:**
  1. What's the difference between "prompting" and "prompt engineering"?
  2. Why does chain-of-thought work? What's happening inside the model?
  3. How many examples do you need for few-shot learning?