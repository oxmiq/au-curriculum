# Day 17 · Pipeline & Expert Parallelism

> **Concept of the day:** **PP** splits the model by layer depth across nodes — needed when one node isn't enough. **EP** distributes experts in MoE models across GPUs. **Pipeline bubbles** = the idle time PP creates.
> **Pre-reading:** Pipeline parallelism overview + Mixtral architecture — Pre-Lecture Reading **Reader 6** (~20 min).
> **Source:** [Study Guide §A.5](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

For models that don't fit in one node (e.g. Llama-3-405B, GPT-4-class), Pipeline Parallelism is unavoidable. For MoE models (Mixtral, DeepSeek, GPT-OSS-20B), Expert Parallelism is the dominant cost. Both have unique failure modes (bubbles, hot experts) that TP doesn't have.

## Readiness check

1. What axis does PP split along? What does each GPU hold?
2. Define a "pipeline bubble." Why does it exist?
3. PP needs ___ bandwidth between stages, much less than TP.
4. In an MoE model, what is an "expert"? What is "Top-K routing"?
5. Why does EP create load-balancing problems that TP doesn't?

## Core concept — Pipeline Parallelism

### What PP splits

Layers 1–N of the model are **partitioned across stages**:

```
GPU group A: layers 1–20
GPU group B: layers 21–40       (across InfiniBand)
GPU group C: layers 41–60
GPU group D: layers 61–80
```

A token's forward pass flows **stage A → B → C → D → output**.

- Activations move between stages (not weights).
- Per-stage payload = batch × seq × hidden — small enough for InfiniBand.
- Each stage internally can still use TP.

### Bubbles

A single token can't be in two stages at once. Naïve scheduling: stage B idles while stage A computes layer 1, etc. → **pipeline bubble**.

**Mitigation:** schedule many micro-batches concurrently → stages fill up. Bubble fraction ≈ `(num_stages − 1) / num_micro_batches`. Real systems target < 10%.

### When you use PP

- Model > single-node weight capacity (typically 70B+).
- Combined with TP intra-node: e.g. **TP = 8 within a node × PP = 2 across nodes** for a 405B model on 16 H100s.
- Latency penalty: each stage adds ~1 inter-node hop per token.

### TP vs PP — the decision tree

| Question | Use TP | Use PP |
|---|---|---|
| Need to reduce decode latency? | Yes | Not much |
| Crossing node boundary? | No | Yes |
| Communication primitive | All-reduce | Point-to-point (activations) |
| Bandwidth needed | NVLink (~900 GB/s) | InfiniBand (~50 GB/s) |
| Hardware-aware | Yes (NVLink shape) | Yes (node count) |

## Core concept — Expert Parallelism

### MoE in 2 sentences

A **Mixture-of-Experts** layer has many "expert" MLPs but each token only flows through a small subset (typically **top-2 of 8** or top-2 of 64). Total parameters huge; **active** parameters per token small.

Mixtral 8x7B: 8 experts × ~7B each, top-2 → ~13B active per token despite ~47B total.

### EP — what it distributes

Each expert lives on a different GPU. Per token:

1. Router decides which top-K experts.
2. Token's activation **all-to-all'd** to those experts.
3. Each expert computes locally.
4. Results all-to-all'd back.

### Why EP is hard

- **Hot experts** — distribution is rarely uniform. Some experts get 4× the traffic. Causes stragglers.
- **All-to-all comms** are expensive — every token touches the network.
- **Capacity planning** — must size for worst-case expert load, not average.

### Combining all three

Production MoE serving often uses **TP × EP × PP** in a 3D mesh:

```
TP = 8       (within node, for dense weights + attention)
EP = 8       (across nodes, distributing experts)
PP = 1 or 2  (only if model exceeds even that)
```

## Practice (90 min)

1. (15 min) Compute pipeline bubble fraction for `num_stages = 4` and 1, 4, 16, 64 micro-batches. Plot mentally.
2. (20 min) Llama-3-405B FP16 = 810 GB. Design a config on 16 H100s: TP, PP, per-GPU shard size, comms budget.
3. (25 min) MoE math: Mixtral 8x7B FP16. Total weights, active per token, KV cache size. Why does EP help throughput more than latency?
4. (20 min) Pair drill: order the parallelism types by latency cost (best → worst): TP, PP, EP. Justify.
5. (10 min) Write a one-line rule: *"Reach for PP when ___, reach for EP when ___."*

## Wrap-up

Cohort can fill in: TP for **latency** (within node), PP for **fit** (across nodes), EP for **MoE throughput**.

## Connect forward

Tomorrow: **speculative decoding** — turn slow sequential decode into a series of fast mini-prefills.

---

## Pre-read for tomorrow (Day 18 · Speculative Decoding)

- **Resource:** "Speculative decoding explained" with diagrams — Pre-Lecture Reading **Reader 8** (advanced serving) (~15 min).
- **Reflection questions:**
  1. Decode is memory-bound and sequential. What can a smaller "draft" model contribute?
  2. What does the big "target" model verify?
  3. What's the expected speedup? What kills it?
