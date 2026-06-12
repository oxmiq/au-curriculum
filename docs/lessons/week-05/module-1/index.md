# Day 21 · Metrics That Matter

> **Concept of the day:** **TTFT, ITL/TPS, throughput, percentiles (P50/P95/P99)**. Means lie; percentiles tell the truth. **Goodhart's Law:** once a metric becomes a target it stops being a good metric.
> **Pre-reading:** "Latency vs throughput in LLM serving" — Pre-Lecture Reading **Reader 10** (production metrics) (~15 min).
> **Source:** [Study Guide §A.7](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Glossary: TTFT, ITL, P99](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Glossary.md).

---

## Why this matters

Every decision in Weeks 2–4 — TP size, engine, FP8 — is justified by *some* metric improving. If you measure the wrong number, or the wrong percentile, you ship the wrong system. This day is when "fast" stops being a feeling and becomes a number with a percentile attached.

## Readiness check

1. What does **TTFT** measure? What about **ITL**?
2. Why is **P99 latency** more relevant than average latency for user experience?
3. What's the tension between **single-stream latency** and **system throughput**?
4. State **Goodhart's Law** in your own words.
5. For a chat product, which metric matters more: TTFT or TPS?

## Core concept — the metric vocabulary

### Latency metrics (per request)

| Metric | What it measures | Driven by |
|---|---|---|
| **TTFT** (Time To First Token) | Wall-clock from request received → first output token | Prefill speed, queueing |
| **ITL** (Inter-Token Latency) | Time between consecutive output tokens | Decode speed |
| **TPS** (tokens per second) | 1000 / ITL_ms | Decode speed |
| **End-to-end latency** | Request received → response complete | TTFT + output_tokens × ITL |

### Throughput metrics (per system)

| Metric | What it measures |
|---|---|
| **Requests per second** | Sustained request admission rate |
| **Tokens per second (aggregate)** | Across all concurrent requests |
| **Concurrency** | In-flight requests at peak |
| **GPU utilization** | Tensor Core busy time fraction (compute) and HBM bandwidth fraction (memory) |

### Percentile metrics

Mean latency hides outliers. Real reporting uses **percentiles**:

- **P50 (median)** — typical request.
- **P95** — 1 in 20 requests slower than this.
- **P99** — 1 in 100 requests slower. **Most user-experience SLOs are P99.**

> **Rule of thumb:** P99 / P50 ratio > 5× means you have a queueing or batching issue.

### The latency ↔ throughput tradeoff

Smaller batches → lower per-request latency, lower GPU utilization.
Larger batches → higher utilization & throughput, higher per-request latency (queueing + slower decode step).

The **Pareto frontier** is what continuous batching engines (Day 19) optimize. Every config has a different (latency, throughput) point on this frontier; you pick based on workload.

### Goodhart's Law

> *"When a measure becomes a target, it ceases to be a good measure."*

If you bonus on "TPS averaged over the day" you'll see engineers slowly slip TTFT and never get called on it. Always report **a vector of metrics with percentiles**, not a single number.

### What to measure per workload

| Workload | Top-priority metric |
|---|---|
| Chat / Q&A (user waiting) | P99 TTFT + median TPS |
| Batch summarization | Aggregate TPS, cost / 1M tokens |
| Code completion | P99 TTFT (very tight, < 200 ms) |
| Document analysis (long output) | Median TPS, P95 end-to-end |
| Agentic tool calls (multi-turn) | P99 end-to-end per turn |

## Practice (90 min)

1. (15 min) Given a latency distribution {50, 60, 70, 80, 90, 100, 110, 120, 150, 5000} ms, compute mean, P50, P95, P99. What does the mean hide?
2. (25 min) Sketch a latency-vs-throughput curve. Mark P50 and P99 separately. Show how the curves diverge at high load.
3. (25 min) Pair drill: pick two products from {ChatGPT, GitHub Copilot, a nightly research summarizer, an agent that does 30 tool calls per task}. For each: name the top-two metrics and a Goodhart trap.
4. (15 min) Discussion: "GPU utilization is 95%." Why is that not enough to know if your system is healthy?
5. (10 min) Write the rule: *"Mean is for ___; percentile is for ___."*

## Wrap-up

Cohort agrees on a **metric scorecard** for the design from Week 4's assignment: TTFT P99, TPS median, requests/sec, GPU utilization. Each gets a target.

## Connect forward

Tomorrow: how production deployments actually run — **autoscaling, failover, observability**, the things that turn a good design into a reliable service.

---

## Pre-read for tomorrow (Day 22 · Production Patterns)

- **Resource:** "Deploying LLMs in production" overview — Pre-Lecture Reading **Reader 10** (~20 min).
- **Reflection questions:**
  1. What's the difference between **horizontal** and **vertical** autoscale for LLM serving? Why is horizontal usually preferred?
  2. What's a **warm pool** and why does cold-start hurt LLMs more than other services?
  3. Where do you put the **load balancer**?
