# Day 22 · Production Patterns

> **Concept of the day:** **autoscale, warm pools, load balancing, observability, rollout strategies**. The operational layer that turns a serving stack into a service.<br>
> **Pre-reading:** "Deploying LLMs in production" — Pre-Lecture Reading **Reader 10** (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 22 · Production Deployment</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-05/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Read: Why Production Matters | 10 min |
| Part 2 | Deep Dive: Scaling & Cold Starts | 20 min |
| Part 3 | Hands-On: Design an Autoscaler | 25 min |
| Part 4 | Hands-On: Load Balancing Strategies | 20 min |
| Part 5 | Discussion: Rollout Strategies | 20 min |
| 7 | Reflection: Observability Kit | 15 min |

---

## Part 1 — Why Production Matters · 10 min
### Reading

A great engine running on great hardware will still fall over without **operational discipline**. Cold starts kill TTFT. A bad load-balancing policy puts 80% of requests on 20% of GPUs. A bad rollout breaks for 5% of users for 30 minutes. These are *not* model problems.

### Reflection (write your answer)

Take 2 minutes to write down:
> What's the difference between a "serving stack" (engine + GPUs) and a "serving system" (everything around it)?

---

## Part 2 — Deep Dive — Scaling & Cold Starts · 20 min
### Reading — Autoscaling for LLM Serving

**Horizontal** scaling (add replicas) is dominant. Vertical (bigger GPUs) is impossible mid-deploy.

The autoscaler watches a signal:

| Signal | Pros | Cons |
|--------|------|------|
| GPU utilization | Cheap, available | Lags real demand by 30–60s |
| Request queue depth | Direct demand signal | Spiky |
| Concurrent requests | Stable | Doesn't see queue |
| P95 TTFT | User-facing | Slowest to react |

Production usually combines two (e.g., queue depth + P95 TTFT thresholds).

### Reading — Cold Starts: The LLM Problem

A fresh replica needs to:
1. **Pull the model image** (10–50 GB over the network)
2. **Load weights into HBM** (10s of seconds for 70B FP16)
3. **Warm caches, JIT-compile kernels** (additional seconds)

**Total cold start: 1–5 minutes for big models.**

### Mitigations for Cold Starts

- **Warm pools** — keep N replicas always-on, pre-warmed
- **Image / weight caching** at the node level (e.g., local PV or cached image)
- **Pre-loaded base images** with weights baked in or mounted
- **Never auto-scale to zero** during business hours

> **Rule:** Never autoscale to zero when user-facing traffic is expected.

---

## Part 3 — Hands-On — Design an Autoscaler · 25 min
### Exercise: Autoscaler Design (15 min)

Consider your Week 4 system:
- **Hardware:** 8×H100
- **Baseline traffic:** 50 req/s
- **Peak traffic:** 200 req/s

Design an autoscaler by answering:

1. **What signal(s)** would you watch? (Pick from the table above)
2. **What threshold** would trigger scale-up? What threshold for scale-down?
3. **What's your warm pool size?** (How many replicas stay always-on?)
4. **What's your max replicas?** (Cap to prevent runaway costs)

### Exercise: Identify Failure Modes (10 min)

**Scenario:** A cold start during a traffic spike.

Draw the failure chain:
1. Traffic spikes
2. Autoscaler adds a new replica
3. ___?___
4. ___?___
5. P99 TTFT spikes to 12 seconds

**What breaks, and at what step?**

---

## Part 4 — Hands-On — Load Balancing Strategies · 20 min
### Reading — Load Balancing for LLMs

Round-robin is bad — different requests cost very different amounts (200-token vs 8K-token output). Common strategies:

| Strategy | When to Use |
|----------|-------------|
| **Least Outstanding Requests (LOR)** | General-purpose serving |
| **Least KV-Cache Used** | When engine exposes this metric |
| **Session Affinity** | Multi-turn conversations (reuse prefix cache) |
| **Per-Tenant Pinning** | Each customer has custom adapter (LoRA) |

### Exercise: Choose Your LB Strategy (10 min)

For each scenario, pick the best load balancing strategy:

1. **Chatbot with 1000 concurrent users** — most have short conversations, some have long threads
2. **Code completion tool** — short inputs, varying output lengths
3. **Multi-tenant SaaS** — each customer has their own fine-tuned adapter

### Exercise: Request Lifecycle Diagram (10 min)

Draw the request lifecycle:
```
Client → [?] → [?] → Engine → [?] → Response
```

At each **[?]**, list:
- One metric you'd capture
- One thing that could go wrong

---

## Part 5 — Discussion — Rollout Strategies · 20 min
### Reading — Rollout Strategies

| Strategy | When to Use |
|----------|-------------|
| **Blue-green** | Major engine / model version change (full rollback in seconds) |
| **Canary** (1% → 10% → 100%) | Most weight / config changes |
| **Shadow** (parallel run, don't serve) | Quality-sensitive changes (new model, quantization) |
| **Feature flag** per-tenant | Adapter / system-prompt changes |

### Exercise: Pick the Right Rollout (Pair Drill) (15 min)

For each change, recommend a rollout strategy and explain why:

1. **Change:** Bump vLLM 0.4 → 0.5 (engine upgrade)
2. **Change:** Replace Llama-3-70B FP16 with FP8 (quantization)
3. **Change:** Add a new tenant-specific LoRA adapter (new customer)
4. **Change:** Modify the system prompt for all users (behavior change)

### Discussion Prompt (5 min)

**Two failure modes that bite:**

1. **Cold start during traffic spike** — Replica added but not ready → existing replicas overload → cascading P99 breach
2. **Bad model rollout** — New model produces lower-quality output that doesn't trigger latency alerts

**Which one is harder to detect? Why?**

---

## Part 7 — Wrap-up & Connection · 15 min
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

Tomorrow: **evaluation & quality** — the *other* set of metrics.

Write one sentence about why quality evaluation matters for production:

### Pre-read for tomorrow (Day 23 · Evaluation & Quality)

- **Resource:** "Evaluating LLMs" overview (HELM, MMLU, perplexity) — Pre-Lecture Reading **Reader 10** (~20 min).
- **Reflection questions:**
  1. What's **perplexity** and what does it capture? What does it miss?
  2. **Benchmark** (MMLU) vs **task eval** (your own use-case suite) — which is more honest about production quality?
  3. **Goodhart's Law** revisited: why is MMLU saturating not actually progress?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
