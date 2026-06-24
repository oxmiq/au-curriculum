# Day 17 · Pipeline & Expert Parallelism

> **Concept of the day:** **PP** splits the model by layer depth across nodes — needed when one node isn't enough. **EP** distributes experts in MoE models across GPUs. **Pipeline bubbles** = the idle time PP creates.<br>
> **Pre-reading:** Pipeline parallelism overview + Mixtral MoE architecture — Pre-Lecture Reading **Reader 8** (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 4 — Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <span>Day 17 · Pipeline Parallelism + MoE</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-04/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review + Readiness Check | 15 min |
| Part 2 | Core Concept: Pipeline Parallelism | 20 min |
| Part 3 | Deep Dive: Bubbles & TP vs PP | 15 min |
| Part 4 | Core Concept: Expert Parallelism | 20 min |
| Part 5 | Hands-On: Config Design | 30 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review + Readiness Check · 15 min
### Before You Start

You should have already read: Pipeline parallelism overview + Mixtral MoE architecture — Pre-Lecture Reading **Reader 8** (~20 min).

### Readiness Check

Answer these questions from memory before proceeding:

1. What axis does PP split along? What does each GPU hold?
2. Define a "pipeline bubble." Why does it exist?
3. PP needs ___ bandwidth between stages, much less than TP.
4. In an MoE model, what is an "expert"? What is "Top-K routing"?
5. Why does EP create load-balancing problems that TP doesn't?

---

## Part 2 — Core Concept — Pipeline Parallelism · 20 min
### Reading — Why This Matters

For models that don't fit in one node (e.g. Llama-3-405B, GPT-4-class), Pipeline Parallelism is unavoidable. For MoE models (Mixtral, DeepSeek, GPT-OSS-20B), Expert Parallelism is the dominant cost. Both have unique failure modes (bubbles, hot experts) that TP doesn't have.

### What PP Splits

Layers 1–N of the model are **partitioned across stages**:

```
GPU group A: layers 1–20
GPU group B: layers 21–40       (across InfiniBand)
GPU group C: layers 41–60
GPU group D: layers 61–80
```

A token's forward pass flows **stage A → B → C → D → output**.

- Activations move between stages (not weights)
- Per-stage payload = batch × seq × hidden — small enough for InfiniBand
- Each stage internally can still use TP

### Key Terms to Understand

| Term | Definition |
|------|------------|
| **Pipeline Parallelism (PP)** | Splits the model by layer depth across nodes — depth-wise parallelism |
| **Stage** | A contiguous group of layers on one GPU group |
| **Pipeline bubble** | Idle time in a stage waiting for inputs from a prior stage |
| **Micro-batch** | Small batch within a larger batch, used to fill pipeline stages |

---

## Part 3 — Deep Dive — Bubbles & TP vs PP · 15 min
### Reading — Pipeline Bubbles

A single token can't be in two stages at once. Naïve scheduling: stage B idles while stage A computes layer 1, etc. → **pipeline bubble**.

**Mitigation:** schedule many micro-batches concurrently → stages fill up. Bubble fraction ≈ `(num_stages − 1) / num_micro_batches`. Real systems target < 10%.

### When You Use PP

- Model > single-node weight capacity (typically 70B+)
- Combined with TP intra-node: e.g. **TP = 8 within a node × PP = 2 across nodes** for a 405B model on 16 H100s
- Latency penalty: each stage adds ~1 inter-node hop per token

### TP vs PP — The Decision Tree

| Question | Use TP | Use PP |
|-----------|--------|--------|
| Need to reduce decode latency? | Yes | Not much |
| Crossing node boundary? | No | Yes |
| Communication primitive | All-reduce | Point-to-point (activations) |
| Bandwidth needed | NVLink (~900 GB/s) | InfiniBand (~50 GB/s) |
| Hardware-aware | Yes (NVLink shape) | Yes (node count) |

---

## Part 4 — Core Concept — Expert Parallelism · 20 min
### Reading — MoE in 2 Sentences

A **Mixture-of-Experts** layer has many "expert" MLPs but each token only flows through a small subset (typically **top-2 of 8** or top-2 of 64). Total parameters huge; **active** parameters per token small.

Mixtral 8x7B: 8 experts × ~7B each, top-2 → ~13B active per token despite ~47B total.

### EP — What It Distributes

Each expert lives on a different GPU. Per token:

1. Router decides which top-K experts
2. Token's activation **all-to-all'd** to those experts
3. Each expert computes locally
4. Results all-to-all'd back

### Why EP Is Hard

- **Hot experts** — distribution is rarely uniform. Some experts get 4× the traffic. Causes stragglers.
- **All-to-all comms** are expensive — every token touches the network.
- **Capacity planning** — must size for worst-case expert load, not average.

### Combining All Three

Production MoE serving often uses **TP × EP × PP** in a 3D mesh:

```
TP = 8       (within node, for dense weights + attention)
EP = 8       (across nodes, distributing experts)
PP = 1 or 2  (only if model exceeds even that)
```

### Key Terms to Understand

| Term | Definition |
|------|------------|
| **Expert Parallelism (EP)** | Distributes experts across GPUs; each token goes to subset of experts |
| **MoE (Mixture-of-Experts)** | Layer with many expert MLPs; router selects top-K per token |
| **Top-K routing** | Router selects the K most relevant experts for each token |
| **Hot experts** | Experts receiving disproportionate traffic, causing performance issues |
| **All-to-all** | Communication pattern where every GPU sends to every other GPU |

---

## Part 5 — Hands-On — Config Design · 30 min
### Exercise 1: Pipeline Bubble Math (15 min)

Compute pipeline bubble fraction for `num_stages = 4` and 1, 4, 16, 64 micro-batches.

**Formula:** Bubble fraction ≈ `(num_stages − 1) / num_micro_batches`

**Calculate:**
- stages=4, microbatches=1: (4-1)/1 = 3 → 300% bubble!
- stages=4, microbatches=4: (4-1)/4 = 0.75 → 75% bubble
- stages=4, microbatches=16: (4-1)/16 = 0.1875 → ~19% bubble
- stages=4, microbatches=64: (4-1)/64 = 0.047 → ~5% bubble ✓

### Exercise 2: 405B Model Design (15 min)

Llama-3-405B FP16 = 810 GB. Design a config on 16 H100s:
- TP, PP, per-GPU shard size, comms budget

**Hint:** 810 GB ÷ 16 GPUs = 50.6 GB per GPU. With 80 GB H100s, you need TP=8 (17.5 GB weights) + PP=2 to fit.

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you explain these from memory?
- [ ] What axis does PP split along?
- [ ] What is a pipeline bubble and how do you mitigate it?
- [ ] What's the difference between TP and PP communication patterns?
- [ ] What is an MoE expert and why does EP create hot expert problems?

### The Key Phrase

> **"TP for latency (within node), PP for fit (across nodes), EP for MoE throughput."**

### Connect Forward

Tomorrow: **speculative decoding** — turn slow sequential decode into a series of fast mini-prefills.

### Pre-read for tomorrow (Day 18 · Speculative Decoding)

- **Resource:** "Speculative decoding explained" with diagrams — Pre-Lecture Reading **Reader 6** (advanced serving) (~15 min).
- **Reflection questions:**
  1. Decode is memory-bound and sequential. What can a smaller "draft" model contribute?
  2. What does the big "target" model verify?
  3. What's the expected speedup? What kills it?

- **Resource:** "Speculative decoding explained" with diagrams — Pre-Lecture Reading **Reader 8** (advanced serving) (~15 min).
- **Reflection questions:**
  1. Decode is memory-bound and sequential. What can a smaller "draft" model contribute?
  2. What does the big "target" model verify?
  3. What's the expected speedup? What kills it?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
