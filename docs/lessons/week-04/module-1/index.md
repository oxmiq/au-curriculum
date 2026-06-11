# Day 16 · Tensor Parallelism

> **Concept of the day:** **TP** splits each layer's matrices across GPUs. Used for one model that's too big for one GPU, or to reduce per-token decode latency. **NVLink required** — TP is intra-node only.
> **Pre-reading:** "Tensor parallelism explained" — Pre-Lecture Reading **Reader 6** (parallelism overview) (~20 min).
> **Source:** [Study Guide §A.5](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

The first scaling lever you reach for. Tensor Parallelism is what runs Llama-3-70B on 8×H100 — the bread-and-butter production config. Get this wrong and you either OOM or burn latency on PCIe round-trips.

## Readiness check

1. What gets split, and what stays replicated, in TP?
2. Why must TP run inside one node (NVLink)?
3. If `tp = 8`, how big is each GPU's weight shard for a 70B FP16 model?
4. Does TP help prefill more, decode more, or both?
5. What's the *communication primitive* TP needs per layer?

## Core concept

### What TP splits

Inside a transformer layer:

- **Attention projection matrices** (Q, K, V, output) — each split column-wise across TP GPUs.
- **MLP up/down projections** — split similarly.
- **Embedding and unembedding** — usually split.
- **LayerNorm, residual stream** — **replicated** (small + needed by all shards).

Each GPU holds its slice of the weights, computes its slice of the matmul, then participates in an **all-reduce** to combine partial results before the next layer.

### Worked example — Llama-3-70B FP16 on 8×H100

- Total weights: 140 GB FP16.
- Per-GPU shard (`tp = 8`): 140 / 8 = **17.5 GB** of weights.
- Each H100 has 80 GB HBM → plenty of room for KV cache + activations + batch.

### Why NVLink matters

The all-reduce after every layer moves **~per-token-batch × hidden-dim** bytes between all TP ranks. For 70B at hidden_dim = 8192, batch 32, that's ~0.5 MB *per layer per token* × 80 layers = ~40 MB per output token. At decode rates (500–1000 tokens/s aggregate), you need:

| Interconnect | Bandwidth | Verdict |
|---|---|---|
| NVLink 4 (H100) | 900 GB/s | ✓ comfortable |
| PCIe Gen 5 | ~64 GB/s | choking under load |
| InfiniBand HDR | ~50 GB/s/NIC | not for TP — for cross-node |

**Rule:** TP within a node, never across nodes. Cross-node = Pipeline Parallelism (tomorrow).

### TP and the roofline

- **Prefill** (compute-bound): TP roughly divides compute time by TP-size, minus communication overhead. Helps a lot.
- **Decode** (memory-bound): TP divides per-GPU weight reads by TP-size → **latency per token drops roughly linearly with `tp`** (until comms dominate).

This is why production LLM serving uses **the largest TP that NVLink supports** (usually 8): it minimizes decode latency.

### Cost of TP

- All-reduce comms per layer adds latency — typically 5–15% overhead at `tp = 8`.
- Diminishing returns past NVLink boundary.
- More GPUs = more failures to handle.

## Practice (90 min)

1. (15 min) For Llama-3-70B FP16: compute per-GPU weight shard at `tp = 1, 2, 4, 8`. At which `tp` does it first fit in 80 GB?
2. (25 min) Estimate decode latency for that model at `tp = 1` (won't fit, hypothetical), `tp = 4`, `tp = 8`. Use 3.35 TB/s per H100. What's the practical lower bound?
3. (20 min) Pair drill: explain *why* an all-reduce is needed at every layer (not just at output). Walk through a single MLP forward pass.
4. (20 min) Numerical: if NVLink were 100 GB/s instead of 900 GB/s, at what TP size does comms overhead exceed compute savings?
5. (10 min) Write the one-line rule: *"TP is for ___, capped at ___."*

## Wrap-up

Cohort agrees: TP = first lever, capped at 8 by NVLink, halves decode latency by halving per-GPU weight reads.

## Connect forward

Tomorrow: when one node isn't enough — **Pipeline Parallelism** (cross-node) and **Expert Parallelism** (for MoE).

---

## Pre-read for tomorrow (Day 17 · Pipeline & Expert Parallelism)

- **Resource:** PP overview + Mixtral MoE architecture summary — Pre-Lecture Reading **Reader 6** (~20 min).
- **Reflection questions:**
  1. PP splits a model how? (Hint: depth-wise.)
  2. What is a "pipeline bubble" and why is it bad?
  3. In a Mixture-of-Experts model, what does Expert Parallelism distribute, and why is its communication pattern different from TP?
