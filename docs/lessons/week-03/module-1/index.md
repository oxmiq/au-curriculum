# Day 11 · Prefill and Decode

> **Concept of the day:** the two phases of inference. **Prefill** = parallel, compute-bound, drives TTFT. **Decode** = sequential, memory-bound, drives TPS.<br>
> **Pre-reading:** "Prefill vs decode" explainer — Pre-Lecture Reading **Reader 4 (attention math)** and Reader 6 sections on serving (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 — Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 11 · Prefill vs Decode</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-03/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts: Prefill | 20 min |
| Part 3 | Core Concepts: Decode | 20 min |
| Part 4 | Visual Timeline | 15 min |
| Part 5 | Hands-On: Calculate | 30 min |
| 7 | Wrap-up & Connection | 15 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: "Prefill vs decode" explainer — Pre-Lecture Reading **Reader 4 (attention math)** and Reader 6 sections on serving (~15 min).

### Quick Self-Check

Answer these questions from memory:
1. Which phase processes all input tokens at once? Which one at a time?
2. Which phase is compute-bound? Which is memory-bound?
3. What does **TTFT** stand for? What drives it?

---

## Part 2 — Core Concepts — Prefill · 20 min
### Reading — The Two Phases

This is the conceptual hinge of the entire serving stack. Every metric, every engine, every parallelism choice in Weeks 4–5 is about *which phase* it optimizes. Confuse them and your latency/throughput trade-offs make no sense.

### Prefill — Process All Input Tokens in Parallel

> **Analogy: reading a whole book to build context.**

Given N input tokens, prefill runs them through the transformer as a single large batch. The work is one giant set of GEMMs:

| Property | Prefill |
|----------|---------|
| **Processing** | Parallel across all N tokens |
| **Bottleneck** | Compute-bound — high arithmetic intensity |
| **Time scales** | Linearly with N (short context), quadratically (attention layer, long context) |
| **Produces** | First output token + initial KV cache |
| **Metric** | **TTFT** (Time To First Token) |

### Why Prefill is Compute-Bound

- All input tokens processed simultaneously
- Large matrix multiplications (GEMMs)
- High arithmetic intensity (hundreds of ops/byte)
- You're hitting the Tensor Cores, not waiting on HBM

---

## Part 3 — Core Concepts — Decode · 20 min
### Decode — One Token at a Time

> **Analogy: writing one word at a time.**

Once prefill finishes, decode loops:

```
loop:
  use KV cache + previous token → compute attention + MLP → next token
  append next token's K, V to the cache
until stop
```

| Property | Decode |
|----------|--------|
| **Processing** | Sequential — each token depends on previous |
| **Bottleneck** | Memory-bound for single user |
| **Time per token** | Scales with model size and HBM bandwidth |
| **Metrics** | **ITL** (Inter-Token Latency), **TPS** (Tokens Per Second) |

### Why Decode is Memory-Bound

- One token at a time
- Must re-read all model weights for each token
- Low arithmetic intensity (~2 ops/byte)
- GPU is idle ~99% of the time waiting for data

### The Metrics

- **ITL** — gap between consecutive output tokens
- **TPS** = 1000 / ITL_ms — tokens per second per stream

---

## Part 4 — Visual Timeline · 15 min
### Reading — One Picture, Both Phases

```
time →
│■■■■■■│ ← prefill (one big GEMM batch)
       │█ █ █ █ █ █ █ █ ...│ ← decode (one token per step)
       ↑                       ↑
       TTFT (first token)       end-to-end latency
```

### Annotate the Timeline

1. **Prefill bar** — represents compute-bound phase
2. **Decode train** — represents sequential memory-bound phase
3. **TTFT** — time from request to first token (driven by prefill)
4. **End-to-end latency** — TTFT + (tokens × ITL)

---

## Part 5 — Hands-On — Calculate · 30 min
### Exercise 1: Sketch the Timeline (15 min)

Given a request with 1000 input + 500 output tokens:

1. Draw the timeline showing prefill and decode phases
2. Label where TTFT lives
3. Label where end-to-end latency lives

### Exercise 2: Numerical Calculation (15 min)

**Given:** Llama-3-8B on one H100

**Estimate:**
1. **Prefill time** for 1000 input tokens (compute-bound, use ~989 TFLOPs FP16)
2. **Decode time** per token (memory-bound, use 16 GB ÷ 3.35 TB/s)
3. **Total wall-clock time**

**Hint:**
- Prefill: ~1000 tokens × (computation per token) ÷ TFLOPs
- Decode: ~16 GB ÷ 3.35 TB/s = ~4.8 ms per token × 500 tokens

---

## Part 7 — Wrap-up & Connection · 15 min
### Self-Check

Can you explain these from memory?
- [ ] What's the difference between prefill and decode?
- [ ] Which phase is compute-bound? Which is memory-bound?
- [ ] What drives TTFT? What drives TPS?
- [ ] Why does decode take so much longer per token than prefill?

### The Key Phrase

> **"Prefill = compute, decode = memory."**

### Connect Forward

Tomorrow: the **KV cache** — the structure that makes decode possible at all, and the resource you spend the next three weeks trying to fit, share, and prune.

### Pre-read for tomorrow (Day 12 · The KV Cache)

- **Resource:** "KV cache explained" — Pre-Lecture Reading **Reader 4 (attention math)** + Study Guide §A.2 KV-cache subsection (~20 min).
- **Reflection questions:**
  1. What grows every time the model generates a token?
  2. Where in the transformer is the KV cache used?
  3. For a 70B model at 128K context, can the KV cache exceed the size of the model weights themselves?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
