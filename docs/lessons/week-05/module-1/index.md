# Day 21 · Metrics That Matter

> **Concept of the day:** **TTFT, ITL/TPS, throughput, percentiles (P50/P95/P99)**. Means lie; percentiles tell the truth. **Goodhart's Law:** once a metric becomes a target it stops being a good metric.<br>
> **Pre-reading:** "Latency vs throughput in LLM serving" - <a href="https://www.anyscale.com/blog/llm-inference-performance" target="_blank" rel="noopener">Anyscale - LLM Inference Performance</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 - Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 21 · Latency vs Throughput</span>
    {status:week-05/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Read: Why Metrics Matter |
| Part 2 | Deep Dive: Metric Vocabulary |
| Part 3 | Hands-On: Percentile Calculations |
| Part 4 | Hands-On: Latency vs Throughput |
| Part 5 | Discussion: Goodhart Traps |
| Part 6 | Reflection: Metric Scorecard |

---

## Part 1 - Why Metrics Matter

### Before You Start

You should have already read: <a href="https://www.anyscale.com/blog/llm-inference-performance" target="_blank" rel="noopener">Anyscale - Latency vs Throughput in LLM Serving</a>.

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m1-readiness" data-kind="readiness" data-draw="5" data-source="Anyscale - Latency vs Throughput in LLM Serving">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does TTFT (Time To First Token) measure?", "options": ["The time between consecutive output tokens", "The wall-clock time from request received to first output token", "The total time to process the entire request", "The time spent in the decode phase"]},
  {"stem": "What is the relationship between ITL (Inter-Token Latency) and TPS (Tokens Per Second)?", "options": ["TPS = ITL × 1000", "TPS = 1000 / ITL_ms", "TPS = ITL / 1000", "TPS and ITL are unrelated metrics"]},
  {"stem": "In LLM inference, what happens to latency when you increase batch size?", "options": ["Latency always decreases", "Latency always increases", "Latency typically increases while throughput improves", "Batch size has no impact on latency"]},
  {"stem": "What is the 'prefill' phase in LLM inference?", "options": ["Generating the first token of output", "Processing the input prompt to compute KV caches", "Decoding tokens one-by-one", "Finalizing the response"]},
  {"stem": "Why do real-world LLM deployments often report P99 latency instead of average latency?", "options": ["P99 is easier to calculate", "Average latency hides outliers; P99 captures the experience of the slowest 1% of requests", "P99 is always lower than average", "Users only care about the slowest requests"]},
  {"stem": "What is the primary driver of ITL (Inter-Token Latency)?", "options": ["Prefill speed", "Queueing delay", "Decode speed", "Network latency"]},
  {"stem": "What is continuous batching in LLM serving?", "options": ["Batching that processes all requests at once", "A technique that adds new requests to a batch while other requests are still decoding", "Batching that only processes requests with continuous token streams", "A method to reduce batch size over time"]},
  {"stem": "In the latency vs throughput tradeoff, what does high throughput with high latency typically indicate?", "options": ["An underutilized GPU", "A system with large batch sizes processing many concurrent requests", "A system with no batching", "A failed deployment"]}
]
</script>
</div>

### Reading

Every decision in Weeks 2–4, TP size, engine, FP8, is justified by *some* metric improving. If you measure the wrong number, or the wrong percentile, you ship the wrong system. This day is when "fast" stops being a feeling and becomes a number with a percentile attached.

### Reflection (write your answer)

Take 2 minutes to write down:
> What's the difference between "fast" as a feeling and "fast" as a number?

---

## Part 2 - Deep Dive - The Metric Vocabulary
### Reading - Latency Metrics (Per Request)

| Metric | What it Measures | Driven By |
|--------|-----------------|-----------|
| **TTFT** (Time To First Token) | Wall-clock from request received → first output token | Prefill speed, queueing |
| **ITL** (Inter-Token Latency) | Time between consecutive output tokens | Decode speed |
| **TPS** (Tokens Per Second) | 1000 / ITL_ms | Decode speed |
| **End-to-end Latency** | Request received → response complete | TTFT + output_tokens × ITL |

### Reading - Throughput Metrics (Per System)

| Metric | What it Measures |
|--------|-----------------|
| **Requests Per Second** | Sustained request admission rate |
| **Tokens Per Second (aggregate)** | Across all concurrent requests |
| **Concurrency** | In-flight requests at peak |
| **GPU Utilization** | Tensor Core busy time fraction (compute) and HBM bandwidth fraction (memory) |

### Reading - Percentile Metrics

Mean latency hides outliers. Real reporting uses **percentiles**:

- **P50 (median)** - typical request.
- **P95** - 1 in 20 requests slower than this.
- **P99** - 1 in 100 requests slower. **Most user-experience SLOs are P99.**

> **Rule of thumb:** P99 / P50 ratio > 5× means you have a queueing or batching issue.

---

## Part 3 - Hands-On - Percentile Calculations
### Exercise 1: Calculate Percentiles

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

### Exercise 2: Interpret the Distribution

Look at the distribution above. The value `5000` ms (5 seconds) represents a cold start or a timeout.

- If you only report "mean latency," what does the user see?
- If you report "P99 latency," what does the user see?
- Why is P99 more relevant for user experience than mean?

---

## Part 4 - Hands-On - Latency vs Throughput Tradeoff
### Exercise 1: Sketch the Frontier

Draw a coordinate system with:
- **X-axis:** Throughput (tokens/sec)
- **Y-axis:** Latency (ms per request)

Sketch two curves:

1. **P50 Latency** curve - typically decreases slightly then increases as batch size grows
2. **P99 Latency** curve - stays low initially, then spikes dramatically at high load

**Mark the point** where the system transitions from "healthy" to "overloaded."

### Exercise 2: The Tradeoff Explained

**Why does this tradeoff exist?**

| Batch Size | Effect on Latency | Effect on Throughput |
|------------|-------------------|---------------------|
| Small (1-2) | Low (fast) | Low (under-utilized GPU) |
| Medium (8-16) | Moderate | High |
| Large (64+) | High (queueing + slower decode) | Very High (but P99 suffers) |

**Write one sentence** summarizing the latency-throughput tradeoff in your own words.

---

## Part 5 - Discussion - Goodhart Traps
### Reading - Goodhart's Law

> *"When a measure becomes a target, it ceases to be a good measure."*

If you bonus on "TPS averaged over the day" you'll see engineers slowly slip TTFT and never get called on it. Always report **a vector of metrics with percentiles**, not a single number.

### Exercise: Identify Goodhart Traps (Pair Drill)

Pick two products from this list:
- ChatGPT (consumer chat)
- GitHub Copilot (code completion)
- A nightly research summarizer (batch job)
- An agent that does 30 tool calls per task (agentic)

For each product:

1. Name the **top-two metrics** you'd track
2. Identify **one Goodhart trap**: what could go wrong if you optimized only for that metric?

### Discussion Prompt

**"GPU utilization is 95%."** Why is that not enough to know if your system is healthy?

Think about:
- What if 95% is spent waiting for KV cache, not computing?
- What if the requests are queuing up waiting for that 5% idle time?

---

## Part 7 - Wrap-up & Connection
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

### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 21 · Metrics &amp; SLOs">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does TTFT (Time To First Token) measure?", "options": ["The total time for the model to generate all output tokens", "The time from when the request is received to when the first output token is produced", "The time it takes to tokenize the input prompt", "The time between consecutive output tokens during streaming"]},
  {"stem": "For code completion (e.g., GitHub Copilot-style), what is the top-priority latency metric and why?", "options": ["Aggregate TPS: because code generation needs to be fast overall", "P99 TTFT with a very tight target (< 200 ms): because users expect instant inline completions and any delay breaks the typing flow", "Cost per million tokens: because code assistants are used frequently", "GPU utilization: because maximum hardware usage minimizes per-user cost"]},
  {"stem": "What does P99 TTFT mean?", "options": ["The average TTFT across 99 requests", "The TTFT at the 99th percentile: 99% of requests have lower TTFT, only 1% are slower", "The maximum TTFT ever observed", "The TTFT target that 99% of the engineering team agreed to"]},
  {"stem": "For batch summarization (e.g., overnight document processing), what is the top-priority metric?", "options": ["P99 TTFT: because documents must start processing quickly", "Aggregate throughput (TPS) and cost per million tokens: because the workload is not user-facing and maximizing throughput minimizes cost", "GPU utilization: because batch jobs must run at 100% GPU usage", "Median TTFT: because individual document latency matters"]},
  {"stem": "Why is GPU utilization important as a cost metric?", "options": ["Higher GPU utilization always means lower latency", "GPU cost is roughly fixed per hour; higher utilization means more tokens generated per dollar of GPU time", "GPU utilization determines whether the model runs in FP16 or FP8", "Low GPU utilization triggers autoscaling which increases costs"]},
  {"stem": "What is the top-priority metric for an agentic tool-calling workload with multiple back-and-forth turns?", "options": ["Aggregate TPS: because agents make many small calls", "P99 TTFT per turn: because agent tools block on each LLM call and latency accumulates across turns", "P99 end-to-end per turn: because the user only cares about each turn completing, not the first token", "GPU utilization: because agents have low concurrency so the GPU may be idle"]},
  {"stem": "If a deployment's inter-token latency (ITL) is 25 ms, what is its tokens-per-second (TPS)?", "options": ["40 tokens/sec", "25 tokens/sec", "400 tokens/sec", "0.04 tokens/sec"]},
  {"stem": "As batch size grows very large, what does the lesson say happens to P99 latency and throughput?", "options": ["Both P99 latency and throughput fall", "P99 latency stays flat while throughput falls", "P99 latency spikes dramatically (queueing + slower decode) even as aggregate throughput keeps rising", "P99 latency and throughput are unaffected by batch size"]},
  {"stem": "The lesson's rule of thumb says a P99/P50 latency ratio above what value points to a queueing or batching problem?", "options": ["Above 1.5×", "Above 5×", "Above 100×", "Below 1×"]}
]
</script>
</div>

### Pre-read for tomorrow (Day 22 · Production Patterns)

- **Resource:** <a href="https://modal.com/docs/guide/high-performance-llm-inference" target="_blank" rel="noopener">Modal - High-Performance LLM Inference</a> (throughput, latency, cold-start sections). Alternative: <a href="https://huyenchip.com/mlops/" target="_blank" rel="noopener">Chip Huyen - MLOps Guide</a> (serving section).
- **Reflection questions:**
  1. What's the difference between **horizontal** and **vertical** autoscale for LLM serving? Why is horizontal usually preferred?
  2. What's a **warm pool** and why does cold-start hurt LLMs more than other services?
  3. Where do you put the **load balancer**?

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
