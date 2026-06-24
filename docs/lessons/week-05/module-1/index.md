# Day 21 · Metrics That Matter

> **Concept of the day:** **TTFT, ITL/TPS, throughput, percentiles (P50/P95/P99)**. Means lie; percentiles tell the truth. **Goodhart's Law:** once a metric becomes a target it stops being a good metric.<br>
> **Pre-reading:** "Latency vs throughput in LLM serving" — Pre-Lecture Reading **Reader 10** (production metrics) (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 21 · Latency vs Throughput</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-05/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Read: Why Metrics Matter | 10 min |
| Part 2 | Deep Dive: Metric Vocabulary | 20 min |
| Part 3 | Hands-On: Percentile Calculations | 25 min |
| Part 4 | Hands-On: Latency vs Throughput | 25 min |
| Part 5 | Discussion: Goodhart Traps | 20 min |
| 7 | Reflection: Metric Scorecard | 10 min |

---

## Part 1 — Why Metrics Matter · 10 min
### Reading

Every decision in Weeks 2–4 — TP size, engine, FP8 — is justified by *some* metric improving. If you measure the wrong number, or the wrong percentile, you ship the wrong system. This day is when "fast" stops being a feeling and becomes a number with a percentile attached.

### Reflection (write your answer)

Take 2 minutes to write down:
> What's the difference between "fast" as a feeling and "fast" as a number?

---

## Part 2 — Deep Dive — The Metric Vocabulary · 20 min
### Reading — Latency Metrics (Per Request)

| Metric | What it Measures | Driven By |
|--------|-----------------|-----------|
| **TTFT** (Time To First Token) | Wall-clock from request received → first output token | Prefill speed, queueing |
| **ITL** (Inter-Token Latency) | Time between consecutive output tokens | Decode speed |
| **TPS** (Tokens Per Second) | 1000 / ITL_ms | Decode speed |
| **End-to-end Latency** | Request received → response complete | TTFT + output_tokens × ITL |

### Reading — Throughput Metrics (Per System)

| Metric | What it Measures |
|--------|-----------------|
| **Requests Per Second** | Sustained request admission rate |
| **Tokens Per Second (aggregate)** | Across all concurrent requests |
| **Concurrency** | In-flight requests at peak |
| **GPU Utilization** | Tensor Core busy time fraction (compute) and HBM bandwidth fraction (memory) |

### Reading — Percentile Metrics

Mean latency hides outliers. Real reporting uses **percentiles**:

- **P50 (median)** — typical request.
- **P95** — 1 in 20 requests slower than this.
- **P99** — 1 in 100 requests slower. **Most user-experience SLOs are P99.**

> **Rule of thumb:** P99 / P50 ratio > 5× means you have a queueing or batching issue.

---

## Part 3 — Hands-On — Percentile Calculations · 25 min
### Exercise 1: Calculate Percentiles (15 min)

Given the following latency distribution (in milliseconds):
```
{50, 60, 70, 80, 90, 100, 110, 120, 150, 5000}
```

**Calculate:**
1. **Mean** (arithmetic average)
2. **P50** (median)
3. **P95** (95th percentile)
4. **P99** (99th percentile)

**Write down:** What does the mean hide? What does P99 reveal that the mean doesn't?

### Exercise 2: Interpret the Distribution (10 min)

Look at the distribution above. The value `5000` ms (5 seconds) represents a cold start or a timeout.

- If you only report "mean latency," what does the user see?
- If you report "P99 latency," what does the user see?
- Why is P99 more relevant for user experience than mean?

---

## Part 4 — Hands-On — Latency vs Throughput Tradeoff · 25 min
### Exercise 1: Sketch the Frontier (15 min)

Draw a coordinate system with:
- **X-axis:** Throughput (tokens/sec)
- **Y-axis:** Latency (ms per request)

Sketch two curves:
1. **P50 Latency** curve — typically decreases slightly then increases as batch size grows
2. **P99 Latency** curve — stays low initially, then spikes dramatically at high load

**Mark the point** where the system transitions from "healthy" to "overloaded."

### Exercise 2: The Tradeoff Explained (10 min)

**Why does this tradeoff exist?**

| Batch Size | Effect on Latency | Effect on Throughput |
|------------|-------------------|---------------------|
| Small (1-2) | Low (fast) | Low (under-utilized GPU) |
| Medium (8-16) | Moderate | High |
| Large (64+) | High (queueing + slower decode) | Very High (but P99 suffers) |

**Write one sentence** summarizing the latency-throughput tradeoff in your own words.

---

## Part 5 — Discussion — Goodhart Traps · 20 min
### Reading — Goodhart's Law

> *"When a measure becomes a target, it ceases to be a good measure."*

If you bonus on "TPS averaged over the day" you'll see engineers slowly slip TTFT and never get called on it. Always report **a vector of metrics with percentiles**, not a single number.

### Exercise: Identify Goodhart Traps (Pair Drill) (15 min)

Pick two products from this list:
- ChatGPT (consumer chat)
- GitHub Copilot (code completion)
- A nightly research summarizer (batch job)
- An agent that does 30 tool calls per task (agentic)

For each product:
1. Name the **top-two metrics** you'd track
2. Identify **one Goodhart trap** — what could go wrong if you optimized only for that metric?

### Discussion Prompt (5 min)

**"GPU utilization is 95%."** Why is that not enough to know if your system is healthy?

Think about:
- What if 95% is spent waiting for KV cache, not computing?
- What if the requests are queuing up waiting for that 5% idle time?

---

## Part 7 — Wrap-up & Connection · 10 min
### What to Measure Per Workload

| Workload | Top-Priority Metric |
|----------|---------------------|
| Chat / Q&A (user waiting) | P99 TTFT + median TPS |
| Batch summarization | Aggregate TPS, cost / 1M tokens |
| Code completion | P99 TTFT (very tight, < 200 ms) |
| Document analysis (long output) | Median TPS, P95 end-to-end |
| Agentic tool calls (multi-turn) | P99 end-to-end per turn |

### Reflection Question

Based on your Week 4 serving design (8×H100), what would your **metric scorecard** look like?

Create a table with:
- TTFT P99 target: ___
- TPS median target: ___
- Requests/sec: ___
- GPU utilization target: ___

### Pre-read for tomorrow (Day 22 · Production Patterns)

- **Resource:** "Deploying LLMs in production" overview — Pre-Lecture Reading **Reader 10** (~20 min).
- **Reflection questions:**
  1. What's the difference between **horizontal** and **vertical** autoscale for LLM serving? Why is horizontal usually preferred?
  2. What's a **warm pool** and why does cold-start hurt LLMs more than other services?
  3. Where do you put the **load balancer**?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
