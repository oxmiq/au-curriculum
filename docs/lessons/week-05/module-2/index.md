# Day 22 · Production Patterns

> **Concept of the day:** **autoscale, warm pools, load balancing, observability, rollout strategies**. The operational layer that turns a serving stack into a service.
> **Pre-reading:** "Deploying LLMs in production" — Pre-Lecture Reading **Reader 10** (~20 min).
> **Source:** [Study Guide §A.7](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

A great engine running on great hardware will still fall over without **operational discipline**. Cold starts kill TTFT. A bad load-balancing policy puts 80% of requests on 20% of GPUs. A bad rollout breaks for 5% of users for 30 minutes. These are *not* model problems.

## Readiness check

1. What's a **cold start**? Why is it especially painful for LLMs?
2. **Horizontal** vs **vertical** scaling — which works for serving and why?
3. What does a **load balancer** route on, for LLM serving — round-robin? Least-loaded? Stickiness?
4. Name three signals you'd put in production observability.
5. **Canary** vs **blue-green** deploy — when do you reach for each?

## Core concept

### Autoscaling for LLM serving

**Horizontal** scaling (add replicas) is dominant. Vertical (bigger GPUs) is impossible mid-deploy.

The autoscaler watches a signal:

| Signal | Pros | Cons |
|---|---|---|
| GPU utilization | Cheap, available | Lags real demand by 30–60 s |
| Request queue depth | Direct demand signal | Spiky |
| Concurrent requests | Stable | Doesn't see queue |
| P95 TTFT | User-facing | Slowest to react |

Production usually combines two (e.g. queue depth + P95 TTFT thresholds).

### Cold starts — the LLM problem

A fresh replica needs to:
1. Pull the model image (10–50 GB).
2. Load weights into HBM (10s of seconds for 70B FP16).
3. Warm caches, JIT-compile kernels.

**Total cold start: 1–5 minutes for big models.**

Mitigations:
- **Warm pools** — keep N replicas always-on, pre-warmed.
- **Image / weight caching** at the node level.
- **Pre-loaded base images** with weights baked in or mounted.
- **Don't auto-scale to zero** during business hours.

### Load balancing for LLMs

Round-robin is bad — different requests cost very different amounts (200-token vs 8K-token output). Common strategies:

- **Least outstanding requests (LOR)** — route to replica with fewest in-flight.
- **Least KV-cache used** — when engines expose this metric.
- **Session affinity** — multi-turn conversations stuck to one replica to reuse prefix cache.
- **Per-tenant pinning** — when each customer has a custom adapter (LoRA).

### Observability — the minimum kit

**Metrics (Prometheus + Grafana style):**
- TTFT P50/P95/P99
- TPS P50/P95
- Requests/sec, concurrency, queue depth
- GPU utilization, HBM utilization
- Token cost per request

**Logging:**
- Request ID + tenant + prompt hash + output token count
- *Not the full prompt body* (privacy).

**Tracing:**
- Per-request span: queue → prefill → decode → response.

**Alerts:**
- P99 TTFT breach for > 5 min
- GPU error / OOM
- Replica unhealthy

### Rollout strategies

| Strategy | When |
|---|---|
| **Blue-green** | Major engine / model version change |
| **Canary** (1% → 10% → 100%) | Most weight / config changes |
| **Shadow** (parallel run, compare outputs, don't serve) | Quality-sensitive changes (new model, quantization) |
| **Feature flag** per-tenant | Adapter / system-prompt changes |

### The two failure modes that bite

1. **Cold start during traffic spike.** Replica added but not ready → existing replicas overload → cascading P99 breach.
2. **Bad model rollout.** New model produces lower-quality output that doesn't trigger latency alerts. Caught only by quality eval (Day 23).

## Practice (90 min)

1. (15 min) Draw the request lifecycle: client → LB → replica → engine → response. Mark each metric you'd capture at each hop.
2. (25 min) Design an autoscaler for the Week 4 system (8×H100, 50 req/s baseline, 200 req/s peak). What signal, what threshold, what warm-pool size, what max?
3. (25 min) Pair: write a postmortem outline for "P99 TTFT spiked to 12 s for 8 minutes during morning traffic." What three things do you check first?
4. (15 min) Pick a rollout strategy for each: (a) bump vLLM 0.4 → 0.5, (b) replace Llama-3-70B FP16 with FP8, (c) add a new tenant-specific LoRA adapter.
5. (10 min) Write the one-line rule: *"Never autoscale to zero when ___."*

## Wrap-up

Cohort can answer: *what's the difference between a serving stack (engine + GPUs) and a serving system (everything around it)?*

## Connect forward

Tomorrow: **evaluation & quality** — the *other* set of metrics, the ones that catch the bad-model-rollout case above.

---

## Pre-read for tomorrow (Day 23 · Evaluation & Quality)

- **Resource:** "Evaluating LLMs" overview (HELM, MMLU, perplexity) — Pre-Lecture Reading **Reader 10** (~20 min).
- **Reflection questions:**
  1. What's **perplexity** and what does it capture? What does it miss?
  2. **Benchmark** (MMLU) vs **task eval** (your own use-case suite) — which is more honest about production quality?
  3. **Goodhart's Law** revisited: why is MMLU saturating not actually progress?
