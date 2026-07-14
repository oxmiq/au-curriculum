# Day 22 · Production Patterns

> **Concept of the day:** **autoscale, warm pools, load balancing, observability, rollout strategies**. The operational layer that turns a serving stack into a service.<br>
> **Pre-reading:** "Deploying LLMs in production" - <a href="https://modal.com/docs/guide/high-performance-llm-inference" target="_blank" rel="noopener">Modal - High-Performance LLM Inference</a> (throughput, latency, and cold-start sections).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 - Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 22 · Production Deployment</span>
    {status:week-05/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Read: Why Production Matters |
| Part 2 | Deep Dive: Scaling & Cold Starts |
| Part 3 | Hands-On: Design an Autoscaler |
| Part 4 | Hands-On: Load Balancing Strategies |
| Part 5 | Discussion: Rollout Strategies |
| Part 6 | Reflection: Observability Kit |

---

## Part 1 - Why Production Matters

### Before You Start

You should have already read: <a href="https://modal.com/docs/guide/high-performance-llm-inference" target="_blank" rel="noopener">Modal - High-Performance LLM Inference</a> (throughput, latency, and cold-start sections).

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m2-readiness" data-kind="readiness" data-draw="5" data-source="Modal - High-Performance LLM Inference + Chip Huyen - MLOps Guide">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is a 'cold start' problem in ML serving?",
    "options": [
      "The first request to an model takes longer because the model must be loaded into memory",
      "The model produces incorrect outputs when first initialized",
      "The GPU fails to initialize on startup",
      "The first batch of requests always fails"
    ],
    "answer": 0,
    "explain": "A cold start occurs when a model instance must be loaded into GPU memory before it can process requests. This causes high latency for the first request(s) to a new instance. Techniques like warm pools keep model instances pre-loaded to avoid cold starts."
  },
  {
    "stem": "What is a warm pool in ML deployment?",
    "options": [
      "A pool of preheated GPU instances with models already loaded",
      "A dataset of previous requests for testing",
      "A queue of pending requests waiting to be processed",
      "A monitoring system for tracking request history"
    ],
    "answer": 0,
    "explain": "A warm pool is a set of pre-started model instances that are already loaded in GPU memory and ready to serve requests. This eliminates cold start latency by having instances ready to go before requests arrive."
  },
  {
    "stem": "What is the purpose of load balancing in ML model serving?",
    "options": [
      "To ensure all requests return the same output",
      "To distribute incoming requests across multiple model instances fairly",
      "To increase the batch size of each request",
      "To reduce the total number of requests processed"
    ],
    "answer": 1,
    "explain": "Load balancing distributes incoming requests across multiple model instances to prevent any single instance from being overwhelmed. Without proper load balancing, some GPUs may be overloaded while others sit idle."
  },
  {
    "stem": "What is canary deployment?",
    "options": [
      "Deploying only to GPU nodes named 'Canary'",
      "Gradually rolling out a new version to a small subset of users before full deployment",
      "Deploying with a fallback to the previous version",
      "Testing deployment in a separate environment first"
    ],
    "answer": 1,
    "explain": "Canary deployment is a rollout strategy where a new version is first deployed to a small subset of users (e.g., 5%). If the canary performs well, the rollout expands to all users. This reduces risk of widespread outages from bad deployments."
  },
  {
    "stem": "Why is observability important in ML production systems?",
    "options": [
      "It increases the throughput of the system",
      "It helps identify issues like cold starts, model degradation, or input/output drift",
      "It is required by law",
      "It reduces the cost of serving"
    ],
    "answer": 1,
    "explain": "Observability (metrics, logs, traces) helps operators identify and diagnose issues in production: cold starts, model latency spikes, input drift, output degradation, GPU utilization problems, etc. Without observability, you're blind to production issues."
  },
  {
    "stem": "What is autoscaling in the context of ML model serving?",
    "options": [
      "Automatically adjusting model weights for better performance",
      "Automatically adding or removing model instances based on demand",
      "Automatically selecting which model to use for each request",
      "Automatically tuning hyperparameters"
    ],
    "answer": 1,
    "explain": "Autoscaling automatically adds or removes model instances (or GPU resources) based on incoming load. When request volume increases, new instances are provisioned; when it decreases, instances are terminated to save cost."
  },
  {
    "stem": "What is a rollback strategy in ML deployment?",
    "options": [
      "A technique for reverting to a previous model version when issues are detected",
      "A method for testing model performance on historical data",
      "A way to reduce model size for deployment",
      "A process for cleaning up old training data"
    ],
    "answer": 0,
    "explain": "A rollback strategy defines how to quickly revert to a previous model version if issues are detected in production. This is critical for minimizing the blast radius of bad deployments: being able to roll back in minutes rather than hours."
  },
  {
    "stem": "What is the relationship between TTFT (Time To First Token) and warm pools?",
    "options": [
      "Warm pools increase TTFT",
      "Warm pools decrease TTFT by pre-loading models",
      "Warm pools have no effect on TTFT",
      "TTFT determines the size of warm pools needed"
    ],
    "answer": 1,
    "explain": "Warm pools decrease TTFT by keeping model instances pre-loaded in GPU memory. Without warm pools, new instances must load the model (which can take seconds to minutes), causing high TTFT for requests landing on new instances."
  }
]
</script>
</div>

### Reading

A great engine running on great hardware will still fall over without **operational discipline**. Cold starts kill TTFT. A bad load-balancing policy puts 80% of requests on 20% of GPUs. A bad rollout breaks for 5% of users for 30 minutes. These are *not* model problems.

### Reflection (write your answer)

Take 2 minutes to write down:
> What's the difference between a "serving stack" (engine + GPUs) and a "serving system" (everything around it)?

---

## Part 2 - Deep Dive - Scaling & Cold Starts
### Reading - Autoscaling for LLM Serving

**Horizontal** scaling (add replicas) is dominant. Vertical (bigger GPUs) is impossible mid-deploy.

The autoscaler watches a signal:

| Signal | Pros | Cons |
|--------|------|------|
| GPU utilization | Cheap, available | Lags real demand by 30–60s |
| Request queue depth | Direct demand signal | Spiky |
| Concurrent requests | Stable | Doesn't see queue |
| P95 TTFT | User-facing | Slowest to react |

Production usually combines two (e.g., queue depth + P95 TTFT thresholds).

### Reading - Cold Starts: The LLM Problem

A fresh replica needs to:

1. **Pull the model image** (10–50 GB over the network)
2. **Load weights into HBM** (10s of seconds for 70B FP16)
3. **Warm caches, JIT-compile kernels** (additional seconds)

**Total cold start: 1–5 minutes for big models.**

### Mitigations for Cold Starts

- **Warm pools** - keep N replicas always-on, pre-warmed
- **Image / weight caching** at the node level (e.g., local PV or cached image)
- **Pre-loaded base images** with weights baked in or mounted
- **Never auto-scale to zero** during business hours

> **Rule:** Never autoscale to zero when user-facing traffic is expected.

---

## Part 3 - Hands-On - Design an Autoscaler
### Exercise: Autoscaler Design

Consider your Week 4 system:
- **Hardware:** 8×H100
- **Baseline traffic:** 50 req/s
- **Peak traffic:** 200 req/s

Design an autoscaler by answering:

1. **What signal(s)** would you watch? (Pick from the table above)
2. **What threshold** would trigger scale-up? What threshold for scale-down?
3. **What's your warm pool size?** (How many replicas stay always-on?)
4. **What's your max replicas?** (Cap to prevent runaway costs)

### Exercise: Identify Failure Modes

**Scenario:** A cold start during a traffic spike.

Draw the failure chain:

1. Traffic spikes
2. Autoscaler adds a new replica
3. ___?___
4. ___?___
5. P99 TTFT spikes to 12 seconds

**What breaks, and at what step?**

---

## Part 4 - Hands-On - Load Balancing Strategies
### Reading - Load Balancing for LLMs

Round-robin is bad; different requests cost very different amounts (200-token vs 8K-token output). Common strategies:

| Strategy | When to Use |
|----------|-------------|
| **Least Outstanding Requests (LOR)** | General-purpose serving |
| **Least KV-Cache Used** | When engine exposes this metric |
| **Session Affinity** | Multi-turn conversations (reuse prefix cache) |
| **Per-Tenant Pinning** | Each customer has custom adapter (LoRA) |

### Exercise: Choose Your LB Strategy

For each scenario, pick the best load balancing strategy:

1. **Chatbot with 1000 concurrent users** - most have short conversations, some have long threads
2. **Code completion tool** - short inputs, varying output lengths
3. **Multi-tenant SaaS** - each customer has their own fine-tuned adapter

### Exercise: Request Lifecycle Diagram

Draw the request lifecycle:
```
Client → [?] → [?] → Engine → [?] → Response
```

At each **[?]**, list:
- One metric you'd capture
- One thing that could go wrong

---

## Part 5 - Discussion - Rollout Strategies
### Reading - Rollout Strategies

| Strategy | When to Use |
|----------|-------------|
| **Blue-green** | Major engine / model version change (full rollback in seconds) |
| **Canary** (1% → 10% → 100%) | Most weight / config changes |
| **Shadow** (parallel run, don't serve) | Quality-sensitive changes (new model, quantization) |
| **Feature flag** per-tenant | Adapter / system-prompt changes |

### Exercise: Pick the Right Rollout (Pair Drill)

For each change, recommend a rollout strategy and explain why:

1. **Change:** Bump vLLM 0.4 → 0.5 (engine upgrade)
2. **Change:** Replace Llama-3-70B FP16 with FP8 (quantization)
3. **Change:** Add a new tenant-specific LoRA adapter (new customer)
4. **Change:** Modify the system prompt for all users (behavior change)

### Discussion Prompt

**Two failure modes that bite:**

1. **Cold start during traffic spike** - Replica added but not ready → existing replicas overload → cascading P99 breach
2. **Bad model rollout** - New model produces lower-quality output that doesn't trigger latency alerts

**Which one is harder to detect? Why?**

---

## Part 7 - Wrap-up & Connection
### The Minimum Observability Kit

**Metrics (Prometheus + Grafana style):**
- TTFT P50/P95/P99
- TPS P50/P95
- Requests/sec, concurrency, queue depth
- GPU utilization, HBM utilization
- Token cost per request

**Logging:**
- Request ID + tenant + prompt hash + output token count
- *Not the full prompt body* (privacy)

**Tracing:**
- Per-request span: queue → prefill → decode → response

**Alerts:**
- P99 TTFT breach for > 5 min
- GPU error / OOM
- Replica unhealthy

### Reflection Question

Tomorrow: **evaluation & quality** - the *other* set of metrics.

Write one sentence about why quality evaluation matters for production:

### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 22 · Production Patterns">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What causes cold-start latency to be worse for LLMs than for typical web services?",
    "options": [
      "LLMs use older hardware that takes longer to initialize",
      "LLM weights are large (often gigabytes) and must be loaded into GPU HBM before the first request can be served",
      "LLMs require a warmup training phase before inference",
      "LLMs need to download new model versions before serving starts"
    ],
    "answer": 1,
    "explain": "A typical web service starts in seconds. An LLM serving replica must load gigabytes of model weights from storage into GPU HBM before processing any requests. A 70B FP16 model requires loading ~140 GB; this can take 30–120 seconds. Warm pools keep pre-warmed replicas ready to accept traffic instantly."
  },
  {
    "stem": "Why is horizontal autoscaling preferred over vertical autoscaling for LLM serving?",
    "options": [
      "Vertical scaling is impossible for GPU workloads",
      "Horizontal scaling adds more replicas (each handling requests in parallel); vertical scaling would require a larger single GPU which may not exist and doesn't scale linearly",
      "Horizontal scaling reduces latency per request; vertical scaling only increases throughput",
      "Vertical scaling requires retraining the model for each new hardware tier"
    ],
    "answer": 1,
    "explain": "Vertical scaling (bigger machine) quickly hits hardware limits; you can't always get an 8×H100+ machine. Horizontal scaling (more replicas) is linearly scalable and uses commodity nodes. Each additional replica handles more concurrent users in parallel."
  },
  {
    "stem": "What is a warm pool?",
    "options": [
      "A group of GPU servers operating at high temperature for efficiency",
      "A set of pre-warmed, idle serving replicas kept ready to accept traffic without cold-start delay",
      "A memory pool that caches recently used model weights",
      "A queue of requests waiting for an available GPU"
    ],
    "answer": 1,
    "explain": "A warm pool keeps pre-initialized serving replicas with model weights already loaded into GPU HBM. When traffic spikes, these replicas accept requests immediately: no cold-start. Without a warm pool, autoscaling adds new replicas that take minutes to warm up, causing P99 latency spikes during ramp."
  },
  {
    "stem": "What are the four key components of a minimum observability kit for LLM serving?",
    "options": [
      "CPU usage, memory usage, disk I/O, network bandwidth",
      "Metrics (TTFT/TPS/GPU utilization), logging (request IDs + token counts), tracing (per-request spans), and alerts (P99 breach, OOM, unhealthy replicas)",
      "Model version, serving engine version, quantization level, hardware type",
      "Cost per request, cost per token, monthly budget, budget alerts"
    ],
    "answer": 1,
    "explain": "The lesson's 'Minimum Observability Kit' lists: Metrics (TTFT P50/P95/P99, TPS, requests/sec, GPU/HBM utilization), Logging (request ID + tenant + output tokens: NOT full prompt body), Tracing (queue → prefill → decode spans), and Alerts (P99 breach, GPU errors, OOM, unhealthy replicas)."
  },
  {
    "stem": "Which alert threshold from the lesson should trigger investigation?",
    "options": [
      "P99 TTFT breach for more than 5 minutes",
      "Any single request exceeding median TTFT by 10%",
      "GPU utilization dropping below 80%",
      "Cost per request exceeding the 30-day moving average"
    ],
    "answer": 0,
    "explain": "The lesson specifies: 'Alerts: P99 TTFT breach for > 5 min.' A single spike might be a fluke; a sustained breach indicates a systemic issue: queue backup, OOM-induced restart, or a degraded replica. The 5-minute window filters transient noise."
  },
  {
    "stem": "Why should production logging capture request IDs and token counts but NOT the full prompt body?",
    "options": [
      "Full prompts are too large to store efficiently in log systems",
      "Full prompt logging violates user privacy; prompts may contain PII, confidential content, or sensitive business data",
      "Prompt bodies are redundant since the model output is already logged",
      "Logging full prompts increases inference latency"
    ],
    "answer": 1,
    "explain": "The lesson explicitly notes: 'Not the full prompt body (privacy).' Prompts may contain user PII, confidential business data, or sensitive information. Logging only the request ID, tenant, prompt hash, and output token count provides operational visibility without creating a privacy liability."
  },
  {
    "stem": "The lesson lists GPU utilization as an autoscaling signal. What is its main drawback?",
    "options": [
      "It lags real demand by 30–60 seconds",
      "It is expensive to collect",
      "It is only exposed by some serving engines",
      "It cannot be read during the decode phase"
    ],
    "answer": 0,
    "explain": "In the autoscaler signal table, GPU utilization is 'cheap, available' but 'lags real demand by 30–60s.' That lag is why production usually combines signals: e.g., request queue depth (direct but spiky) plus P95 TTFT thresholds."
  },
  {
    "stem": "What rule does the lesson give about autoscaling replicas down to zero?",
    "options": [
      "Always scale to zero to eliminate idle cost",
      "Never autoscale to zero when user-facing traffic is expected",
      "Scale to zero only during peak hours",
      "Scale to zero whenever GPU utilization exceeds 80%"
    ],
    "answer": 1,
    "explain": "Because a fresh replica takes 1–5 minutes to cold-start (pull image, load weights into HBM, warm caches), the lesson's rule is: 'Never autoscale to zero when user-facing traffic is expected.' Warm pools keep N replicas always-on to absorb the first requests."
  },
  {
    "stem": "Why does the lesson call round-robin a poor load-balancing strategy for LLM serving?",
    "options": [
      "Different requests cost very different amounts (e.g., 200-token vs 8K-token outputs), so even distribution still overloads some replicas",
      "It requires session affinity to function",
      "It cannot distribute across more than two replicas",
      "It always routes to the coldest replica"
    ],
    "answer": 0,
    "explain": "The lesson states 'Round-robin is bad; different requests cost very different amounts.' A replica handed several 8K-token generations is far busier than one handed 200-token replies. Strategies like Least Outstanding Requests or Least KV-Cache Used route by actual load instead."
  },
  {
    "stem": "Which rollout strategy does the lesson recommend for a quality-sensitive change such as swapping in a quantized model?",
    "options": [
      "Blue-green (full rollback in seconds)",
      "Feature flag per tenant",
      "Shadow (run in parallel, don't serve the output)",
      "Immediate 100% rollout"
    ],
    "answer": 2,
    "explain": "The rollout table pairs Shadow, 'parallel run, don't serve', with quality-sensitive changes like a new model or quantization, because a quality regression may not trip latency alerts. Blue-green fits major version swaps, canary fits most weight/config changes, and feature flags fit adapter/system-prompt changes."
  }
]
</script>
</div>

### Pre-read for tomorrow (Day 23 · Evaluation & Quality)

- **Resource:** <a href="https://huggingface.co/docs/evaluate/index" target="_blank" rel="noopener">Hugging Face - Evaluate</a> + <a href="https://eugeneyan.com/writing/evals/" target="_blank" rel="noopener">Eugene Yan - Task-Specific LLM Evals that Do & Don't Work</a>.
- **Reflection questions:**
  1. What's **perplexity** and what does it capture? What does it miss?
  2. **Benchmark** (MMLU) vs **task eval** (your own use-case suite): which is more honest about production quality?
  3. **Goodhart's Law** revisited: why is MMLU saturating not actually progress?

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
