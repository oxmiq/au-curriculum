# Day 16 · Tensor Parallelism

> **Concept of the day:** **TP** splits each layer's matrices across GPUs. Used for one model that's too big for one GPU, or to reduce per-token decode latency. **NVLink required** — TP is intra-node only.<br>
> **Pre-reading:** "Tensor parallelism explained" — <a href="https://huggingface.co/docs/transformers/v4.15.0/parallelism" target="_blank" rel="noopener">Hugging Face — Model Parallelism</a> (~20 min, read the Tensor Parallel section). Alternative: <a href="https://lilianweng.github.io/posts/2023-01-10-inference-optimization/" target="_blank" rel="noopener">Lilian Weng — Transformer Inference Optimization</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 4 — Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <span>Day 16 · Multi-GPU Parallelism</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-04/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review + Readiness Check | 15 min |
| Part 2 | Core Concept: What TP Splits | 20 min |
| Part 3 | Worked Example: Llama-3-70B on 8×H100 | 15 min |
| Part 4 | Deep Dive: NVLink & The Roofline | 20 min |
| Part 5 | Hands-On: Memory Calculations | 30 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review + Readiness Check · 15 min
### Before You Start

You should have already read: "Tensor parallelism explained" — Pre-Lecture Reading **Reader 8** (parallel computing primer) (~20 min).

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m1-readiness" data-kind="readiness" data-draw="5" data-source="Reader 8">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "In tensor parallelism, which of these is <em>split</em> across GPUs?",
    "options": [
      "LayerNorm parameters",
      "The residual-stream activations",
      "The Q / K / V / output projection matrices",
      "The cluster's load-balancer state"
    ],
    "answer": 2,
    "explain": "TP splits the dense weight matrices column-wise: Q/K/V/output projections and the MLP up/down matrices. LayerNorm and the residual stream stay replicated on every GPU because they are small and needed by every shard."
  },
  {
    "stem": "Which of these stays <em>replicated</em> on every TP rank?",
    "options": [
      "MLP up-projection",
      "LayerNorm parameters and the residual stream",
      "The first half of the embedding table",
      "The output projection"
    ],
    "answer": 1,
    "explain": "LayerNorm parameters and the residual-stream activations are replicated. They are small relative to the dense matrices and every GPU needs them to compute its slice."
  },
  {
    "stem": "Why must tensor parallelism run inside a single node?",
    "options": [
      "Because Linux kernels can't pin memory across nodes",
      "Because the all-reduce per layer needs NVLink-class bandwidth that cross-node fabrics can't sustain",
      "Because CUDA streams can't be shared across machines",
      "Because the model file can't be opened by two processes at once"
    ],
    "answer": 1,
    "explain": "Every transformer layer ends in an all-reduce that moves tens of GB/s of activation data between TP ranks. Only NVLink (~900 GB/s on H100) keeps up — PCIe and inter-node networks become the bottleneck and decode latency collapses."
  },
  {
    "stem": "What communication primitive does TP rely on after every layer?",
    "options": [
      "All-gather",
      "Broadcast",
      "All-reduce",
      "Scatter"
    ],
    "answer": 2,
    "explain": "Each GPU computes a partial sum from its slice of the matmul. All-reduce sums the partials across every GPU and gives every GPU the combined result, so the next layer sees the full activation tensor."
  },
  {
    "stem": "Roughly how much memory does each GPU hold for the weights of a 70B FP16 model at <code>tp=8</code>?",
    "options": [
      "~140 GB",
      "~70 GB",
      "~35 GB",
      "~17.5 GB"
    ],
    "answer": 3,
    "explain": "70B params \u00d7 2 bytes (FP16) = 140 GB total. Split across 8 GPUs \u2192 17.5 GB of weights per GPU. (Activations and KV cache add on top.)"
  },
  {
    "stem": "Which phase of LLM inference benefits <em>most</em> from increasing TP?",
    "options": [
      "Prefill (compute-bound)",
      "Decode (memory-bandwidth-bound)",
      "Both equally",
      "Neither \u2014 TP only affects training"
    ],
    "answer": 1,
    "explain": "Decode reads the full weights from HBM for every output token, so it is memory-bandwidth bound. Splitting the weights across N GPUs roughly divides per-token weight reads by N \u2192 latency drops near-linearly with TP."
  },
  {
    "stem": "TP is best described as which kind of model parallelism?",
    "options": [
      "Depth-wise (different layers on different GPUs)",
      "Width-wise (each layer's matrices sliced across GPUs)",
      "Batch-wise (different requests on different GPUs)",
      "Replica-wise (the same model duplicated)"
    ],
    "answer": 1,
    "explain": "TP slices each layer's matrices column-wise across GPUs. Depth-wise is pipeline parallelism; batch-wise is data parallelism; replica-wise is just replication."
  },
  {
    "stem": "What is the practical upper bound on a single TP group in production today?",
    "options": [
      "2",
      "4",
      "8 (the NVLink domain of one H100/A100 node)",
      "32"
    ],
    "answer": 2,
    "explain": "TP is capped by the NVLink domain, which is 8 GPUs on a standard H100 or A100 node. Going beyond the node forces traffic onto PCIe or the cross-node fabric, where the per-layer all-reduce becomes the bottleneck."
  },
  {
    "stem": "If a model fits in a single GPU's memory, what is the main reason to still use TP?",
    "options": [
      "To improve training throughput \u2014 TP only matters in training",
      "To reduce decode latency by dividing per-token weight reads across GPUs",
      "To make the model load faster from disk",
      "It's never worth it if the model fits"
    ],
    "answer": 1,
    "explain": "Even when the model fits on one GPU, TP can cut decode latency: each GPU only reads its shard of the weights per token, so latency drops roughly with TP-size (until comms dominate)."
  },
  {
    "stem": "A team tries <code>tp=8</code> spanning two nodes (4 GPUs each, NVLink only within a node). What is the most likely symptom?",
    "options": [
      "Out-of-memory \u2014 the weights no longer fit",
      "Lower decode throughput than <code>tp=4</code> within one node, because the cross-node all-reduce dominates",
      "Higher decode throughput than <code>tp=4</code>",
      "No change \u2014 TP is bandwidth-agnostic"
    ],
    "answer": 1,
    "explain": "Cross-node fabrics (PCIe + IB) cannot sustain the per-layer all-reduce at NVLink speeds. The communication time grows enough that effective throughput drops below an intra-node <code>tp=4</code> configuration."
  },
  {
    "stem": "Which is the correct formula for per-GPU weight memory under TP (ignoring KV cache and activations)?",
    "options": [
      "params \u00d7 bytes_per_param",
      "params \u00d7 bytes_per_param \u00f7 tp_size",
      "params \u00f7 tp_size",
      "params \u00d7 tp_size"
    ],
    "answer": 1,
    "explain": "Total bytes for the dense weights = params \u00d7 bytes_per_param. TP splits those bytes across the TP group, so each GPU holds that total divided by <code>tp_size</code>."
  },
  {
    "stem": "What is the approximate NVLink bandwidth on an H100?",
    "options": [
      "~64 GB/s",
      "~200 GB/s",
      "~900 GB/s",
      "~12 TB/s"
    ],
    "answer": 2,
    "explain": "H100 NVLink runs at roughly 900 GB/s per GPU. PCIe Gen5 is ~64 GB/s and inter-node InfiniBand is ~50 GB/s per NIC \u2014 neither is fast enough for the TP all-reduce."
  },
  {
    "stem": "Why is column-wise splitting of attention projections a natural fit for TP?",
    "options": [
      "It avoids any communication at all",
      "Each GPU can independently compute its slice of the output, then the shards combine via a single all-reduce per layer",
      "Column-wise splits halve the number of parameters",
      "The hardware can only address columns, not rows"
    ],
    "answer": 1,
    "explain": "Column-wise sharding lets each GPU compute a partial output independently from its slice of the weight matrix. One all-reduce per layer recombines the partial outputs into the full activation."
  },
  {
    "stem": "Under TP, when does the all-reduce happen in a transformer layer?",
    "options": [
      "Once per token, before the first layer",
      "Once per layer, after the sharded matmul",
      "Once per request, after all layers complete",
      "Never \u2014 TP avoids communication"
    ],
    "answer": 1,
    "explain": "Every layer's sharded matmul produces partial sums per GPU. An all-reduce per layer combines those partials, then the next layer begins."
  },
  {
    "stem": "TP and data parallelism solve different problems. Which statement is accurate?",
    "options": [
      "TP scales a single model across GPUs; data parallelism scales throughput by replicating the model",
      "Both replicate the model; only one improves throughput",
      "TP only helps training; DP only helps inference",
      "They are interchangeable terms"
    ],
    "answer": 0,
    "explain": "TP shards one model across GPUs so it fits and serves faster. DP replicates the model and feeds different batches/requests in parallel. Production setups often combine them: TP within a node, DP across nodes."
  },
  {
    "stem": "Adding more TP ranks improves decode latency, but with diminishing returns. Why?",
    "options": [
      "Because GPUs slow down past 8 ranks",
      "Because per-layer all-reduce time eventually grows faster than the per-GPU compute time shrinks",
      "Because PyTorch caps tensor parallelism at 4",
      "Because HBM bandwidth drops with more GPUs"
    ],
    "answer": 1,
    "explain": "More ranks shrinks per-GPU compute roughly linearly, but the all-reduce involves more participants and more data, so its cost grows. At some point comms dominate and the latency curve flattens or reverses."
  },
  {
    "stem": "Which of these is <em>not</em> typically split by tensor parallelism?",
    "options": [
      "Attention output projection",
      "MLP down-projection",
      "Token embedding matrix",
      "Residual-stream activations"
    ],
    "answer": 3,
    "explain": "Residual-stream activations are replicated across TP ranks. Q/K/V/output projections, MLP matrices, and the embedding/unembedding tables are split."
  },
  {
    "stem": "Within one transformer layer, how does each TP rank produce its share of the next layer's input?",
    "options": [
      "It receives the full activation directly from rank 0 via broadcast",
      "It computes a partial output from its weight slice, then all ranks all-reduce to obtain the full activation",
      "It reads the activation from disk",
      "It runs the full matmul independently and discards N-1 of the results"
    ],
    "answer": 1,
    "explain": "Each rank multiplies the input by its column-shard of the weight matrix, producing a partial sum. All-reduce combines the partials so every rank has the full activation needed for the next layer."
  },
  {
    "stem": "Which knob would you tune first to fit a 70B FP16 model on a single 8\u00d7H100 node?",
    "options": [
      "Pipeline parallelism across nodes",
      "Expert parallelism",
      "Tensor parallelism with <code>tp=8</code>",
      "Lower the batch size to 1"
    ],
    "answer": 2,
    "explain": "TP with <code>tp=8</code> is the canonical fit for 70B on a single 8\u00d7H100 node \u2014 17.5 GB of weights per GPU leaves room for KV cache and activations. PP and EP are for problems TP cannot solve alone."
  },
  {
    "stem": "What kind of parallelism do you reach for <em>after</em> exhausting TP within a node?",
    "options": [
      "More TP across nodes",
      "Pipeline parallelism (depth-wise, cross-node)",
      "Increase batch size only",
      "There is nothing further to try"
    ],
    "answer": 1,
    "explain": "Once you saturate TP within a node, pipeline parallelism splits the model depth-wise across nodes. PP's communication pattern (point-to-point activations at layer boundaries) tolerates the slower cross-node fabric far better than TP's all-reduce would."
  }
]
</script>
</div>

---

## Part 2 — Core Concept — What TP Splits · 20 min
### Reading — Why This Matters

The first scaling lever you reach for. Tensor Parallelism is what runs Llama-3-70B on 8×H100 — the bread-and-butter production config. Get this wrong and you either OOM or burn latency on PCIe round-trips.

### What TP Splits

Inside a transformer layer:

- **Attention projection matrices** (Q, K, V, output) — each split column-wise across TP GPUs.
- **MLP up/down projections** — split similarly.
- **Embedding and unembedding** — usually split.
- **LayerNorm, residual stream** — **replicated** (small + needed by all shards).

Each GPU holds its slice of the weights, computes its slice of the matmul, then participates in an **all-reduce** to combine partial results before the next layer.

### Key Terms to Understand

| Term | Definition |
|------|------------|
| **Tensor Parallelism (TP)** | Splits each layer's weight matrices across GPUs — width-wise parallelism |
| **All-reduce** | Communication primitive where every GPU sends data to every other GPU and receives the combined result |
| **Replicated** | Weights/activations that exist identically on every GPU (not split) |
| **NVLink** | NVIDIA's high-bandwidth GPU interconnect (~900 GB/s on H100) |

---

## Part 3 — Worked Example — Llama-3-70B on 8×H100 · 15 min
### Reading — The Numbers

Let's walk through the actual math for the canonical production config:

- **Total weights:** 140 GB FP16 (70B params × 2 bytes)
- **Per-GPU shard** (`tp = 8`): 140 / 8 = **17.5 GB** of weights per GPU
- **Each H100 has 80 GB HBM** → plenty of room for KV cache + activations + batch

### Key Insight

With `tp = 8`, each GPU only needs to hold 17.5 GB of weights. The remaining ~62.5 GB per GPU goes to:
- KV cache (grows with sequence length)
- Activation tensors (batch × seq × hidden)
- Working memory for batched requests

This is why TP=8 is the default for 70B models — it fits comfortably while minimizing decode latency.

---

## Part 4 — Deep Dive — NVLink & The Roofline · 20 min
### Reading — Why NVLink Matters

The all-reduce after every layer moves **~per-token-batch × hidden-dim** bytes between all TP ranks. For 70B at hidden_dim = 8192, batch 32, that's:

- ~0.5 MB *per layer per token* × 80 layers = **~40 MB per output token**

At decode rates of 500–1000 tokens/s aggregate, you need massive bandwidth:

| Interconnect | Bandwidth | Verdict |
|-------------|-----------|---------|
| NVLink 4 (H100) | 900 GB/s | ✓ comfortable |
| PCIe Gen 5 | ~64 GB/s | choking under load |
| InfiniBand HDR | ~50 GB/s/NIC | not for TP — for cross-node |

**Rule:** TP within a node, never across nodes. Cross-node = Pipeline Parallelism (tomorrow).

### TP and the Roofline

Understanding which phase TP helps:

- **Prefill** (compute-bound): TP roughly divides compute time by TP-size, minus communication overhead. Helps a lot.
- **Decode** (memory-bound): TP divides per-GPU weight reads by TP-size → **latency per token drops roughly linearly with `tp`** (until comms dominate).

This is why production LLM serving uses **the largest TP that NVLink supports** (usually 8): it minimizes decode latency.

### Cost of TP

- All-reduce comms per layer adds latency — typically 5–15% overhead at `tp = 8`
- Diminishing returns past NVLink boundary
- More GPUs = more failures to handle

---

## Part 5 — Hands-On — Memory & Latency Calculations · 30 min
### Exercise 1: Weight Shard Calculator (15 min)

For Llama-3-70B FP16:
- Compute per-GPU weight shard at `tp = 1, 2, 4, 8`
- At which `tp` does the shard first fit in 80 GB?

**Answer:**
- tp=1: 140 GB (won't fit)
- tp=2: 70 GB (won't fit)
- tp=4: 35 GB (won't fit)
- tp=8: 17.5 GB ✓ (fits with room to spare)

### Exercise 2: Decode Latency Estimate (15 min)

Given:
- Per-GPU weight reads: 17.5 GB (at tp=8)
- H100 HBM bandwidth: 3.35 TB/s

Estimate decode latency per token at tp=4 and tp=8. What's the practical lower bound?

**Hint:** Latency = weight_shard ÷ bandwidth

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 16 · Tensor Parallelism">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Inside a transformer layer, which matrices does TP split column-wise across GPUs?",
    "options": [
      "LayerNorm gain and bias",
      "Q, K, V, and output projections; MLP up/down; embedding and unembedding",
      "Residual-stream activations only",
      "The KV cache only"
    ],
    "answer": 1,
    "explain": "The full list from Part 2: attention Q/K/V/output, MLP up/down, embedding/unembedding. LayerNorm and the residual stream stay replicated."
  },
  {
    "stem": "Which scalar best summarises the per-GPU weight memory for Llama-3-70B FP16 at <code>tp=8</code>?",
    "options": [
      "70 GB",
      "35 GB",
      "17.5 GB",
      "8.75 GB"
    ],
    "answer": 2,
    "explain": "140 GB total FP16 weights \u00f7 8 GPUs = 17.5 GB per GPU. Each H100 has 80 GB HBM, leaving ~62 GB for KV cache, activations, and working memory."
  },
  {
    "stem": "At <code>tp=4</code> on Llama-3-70B FP16, what is the per-GPU weight shard?",
    "options": [
      "70 GB",
      "35 GB",
      "17.5 GB",
      "12.5 GB"
    ],
    "answer": 1,
    "explain": "140 GB \u00f7 4 = 35 GB. This still does not fit in an 80 GB H100 once you add KV cache and activations under load, which is why <code>tp=4</code> is rarely the right choice for 70B."
  },
  {
    "stem": "Why does the lesson call <code>tp=8</code> the canonical config for 70B on H100?",
    "options": [
      "It uses the lowest possible bandwidth on the interconnect",
      "Each GPU holds 17.5 GB of weights, leaving ~62 GB for KV cache and activations \u2014 a comfortable fit",
      "It is the only configuration NVIDIA supports",
      "It eliminates the all-reduce per layer"
    ],
    "answer": 1,
    "explain": "Per Part 3: tp=8 yields 17.5 GB weights per GPU, with ~62.5 GB free per GPU for KV cache + activations + batched requests \u2014 the sweet spot."
  },
  {
    "stem": "Which interconnect is fast enough to host TP without the all-reduce becoming the bottleneck?",
    "options": [
      "PCIe Gen 5 (~64 GB/s)",
      "InfiniBand HDR (~50 GB/s per NIC)",
      "NVLink 4 on H100 (~900 GB/s)",
      "10 GbE"
    ],
    "answer": 2,
    "explain": "Per the Part 4 table: only NVLink-class bandwidth is comfortable. PCIe and IB choke under the per-layer all-reduce."
  },
  {
    "stem": "The lesson's rule of thumb: TP within a node, ___ across nodes.",
    "options": [
      "More TP",
      "Pipeline Parallelism",
      "Data Parallelism only",
      "No parallelism at all"
    ],
    "answer": 1,
    "explain": "From Part 4 and the wrap-up: \"TP within a node, never across nodes. Cross-node = Pipeline Parallelism (tomorrow).\""
  },
  {
    "stem": "TP cuts decode latency roughly linearly with <code>tp</code>. Why?",
    "options": [
      "Because more GPUs means more cores running in parallel",
      "Because decode is memory-bandwidth bound and TP divides per-GPU weight reads by <code>tp</code>",
      "Because TP turns off the KV cache",
      "Because each layer becomes shorter"
    ],
    "answer": 1,
    "explain": "Decode reads the entire model from HBM per token; with TP, each GPU only reads its 1/<code>tp</code> shard. Per-token weight reads drop near-linearly with <code>tp</code> until comms dominate."
  },
  {
    "stem": "Roughly how much data moves between TP ranks per output token for the 70B example (hidden_dim 8192, batch 32, 80 layers)?",
    "options": [
      "~40 KB",
      "~0.5 MB",
      "~40 MB",
      "~4 GB"
    ],
    "answer": 2,
    "explain": "Per Part 4: ~0.5 MB per layer per token \u00d7 80 layers = ~40 MB per output token. Multiply by aggregate decode rate to see why NVLink-class bandwidth is mandatory."
  },
  {
    "stem": "What is the typical all-reduce overhead at <code>tp=8</code> on NVLink-equipped nodes?",
    "options": [
      "0%",
      "5-15%",
      "30-50%",
      "Over 100%"
    ],
    "answer": 1,
    "explain": "From Part 4 \u2014 'Cost of TP': 5\u201315% overhead at <code>tp=8</code> is typical. The lesson lists this alongside other costs like diminishing returns past NVLink and more failure surface."
  },
  {
    "stem": "Which phase of inference does TP help <em>more</em> with?",
    "options": [
      "Prefill, because matmuls are large",
      "Decode, because it is memory-bandwidth bound",
      "Both equally",
      "Neither \u2014 TP only matters for training"
    ],
    "answer": 1,
    "explain": "Both phases benefit, but decode benefits more because it is memory-bound \u2014 TP divides per-GPU weight reads. Prefill is already compute-bound, so the win is smaller."
  },
  {
    "stem": "At <code>tp=8</code>, what is the approximate decode latency lower bound per token from weight reads alone (17.5 GB shard, H100 HBM bandwidth 3.35 TB/s)?",
    "options": [
      "~5 ms",
      "~5.2 ms",
      "~52 ms",
      "~520 ms"
    ],
    "answer": 1,
    "explain": "17.5 GB \u00f7 3.35 TB/s \u2248 5.2 ms per token from weight reads. Add comms + KV-cache reads + activation work for the actual end-to-end latency."
  },
  {
    "stem": "At which <code>tp</code> does the 70B FP16 weight shard <em>first</em> fit comfortably in 80 GB H100 HBM?",
    "options": [
      "tp=1",
      "tp=2",
      "tp=4",
      "tp=8"
    ],
    "answer": 3,
    "explain": "tp=1 \u2192 140 GB (no fit), tp=2 \u2192 70 GB (no fit once you add KV cache), tp=4 \u2192 35 GB (still tight), tp=8 \u2192 17.5 GB (comfortable). The hands-on exercise spells this out."
  },
  {
    "stem": "Which of these is NOT listed in the lesson as a cost of TP?",
    "options": [
      "All-reduce communication overhead per layer",
      "Diminishing returns past the NVLink boundary",
      "More GPUs = more failures to handle",
      "Higher per-token compute cost on each GPU"
    ],
    "answer": 3,
    "explain": "Per-GPU compute is lower under TP (each GPU does 1/<code>tp</code> of the matmul). The other three are explicit costs called out in Part 4's 'Cost of TP'."
  },
  {
    "stem": "What does 'replicated' mean in the TP context?",
    "options": [
      "The value is computed once and copied lazily",
      "Every GPU holds the identical tensor",
      "The tensor is sharded but with overlap between shards",
      "The tensor is stored on disk and streamed"
    ],
    "answer": 1,
    "explain": "From the Key Terms table: replicated weights/activations exist identically on every GPU. LayerNorm parameters and the residual stream are the standard examples."
  },
  {
    "stem": "Which sentence is the lesson's 'Key Phrase'?",
    "options": [
      "'TP = last resort, only for models that fit on one GPU.'",
      "'TP = first lever, capped at 8 by NVLink, halves decode latency by halving per-GPU weight reads.'",
      "'TP = always faster than PP, never worse.'",
      "'TP = a synonym for pipeline parallelism.'"
    ],
    "answer": 1,
    "explain": "The wrap-up's Key Phrase exactly: 'TP = first lever, capped at 8 by NVLink, halves decode latency by halving per-GPU weight reads.'"
  },
  {
    "stem": "What scaling lever comes <em>next</em> after TP, per the connect-forward note?",
    "options": [
      "Larger batches only",
      "Pipeline Parallelism (cross-node) and Expert Parallelism (for MoE)",
      "Quantisation",
      "Speculative decoding"
    ],
    "answer": 1,
    "explain": "The wrap-up's Connect Forward: tomorrow covers Pipeline Parallelism (cross-node) and Expert Parallelism (for MoE)."
  },
  {
    "stem": "Suppose you raise <code>tp</code> from 4 to 8 and decode throughput drops slightly. The most likely cause is:",
    "options": [
      "GPUs are overheating",
      "The all-reduce overhead at tp=8 outweighs the extra per-GPU bandwidth gain for this model size",
      "The KV cache vanishes",
      "PyTorch silently switches to CPU"
    ],
    "answer": 1,
    "explain": "Per the 'Cost of TP' section: comms grow as <code>tp</code> grows. For small enough models or short enough sequences, the all-reduce time can overtake the latency win from sharding weights more aggressively."
  },
  {
    "stem": "Why does the lesson recommend not crossing the NVLink boundary with TP?",
    "options": [
      "GPUs in different nodes cannot share the same CUDA context",
      "Cross-node fabrics (PCIe / IB) cannot sustain the per-layer all-reduce; latency collapses",
      "The model file gets corrupted in transit",
      "Cross-node TP is forbidden by the CUDA license"
    ],
    "answer": 1,
    "explain": "Per Part 4's interconnect table and the rule. PCIe (~64 GB/s) and IB (~50 GB/s/NIC) are an order of magnitude slower than NVLink \u2014 the all-reduce per layer becomes the dominant cost."
  },
  {
    "stem": "Which of these correctly orders the inference phases with respect to TP's benefit?",
    "options": [
      "Decode benefit > Prefill benefit (most of the win goes to decode latency)",
      "Prefill benefit > Decode benefit",
      "TP has no effect on either",
      "TP only helps training, not inference"
    ],
    "answer": 0,
    "explain": "Decode is memory-bound, so TP gives near-linear latency wins there. Prefill is compute-bound \u2014 still benefits, but less."
  },
  {
    "stem": "Which statement is the most accurate operational rule for choosing TP in production?",
    "options": [
      "Use the smallest TP that fits the model",
      "Use the largest TP that NVLink supports (usually 8)",
      "Use tp=2 always, regardless of model size",
      "Never use TP \u2014 prefer DP or PP first"
    ],
    "answer": 1,
    "explain": "From Part 4: 'production LLM serving uses the largest TP that NVLink supports (usually 8): it minimizes decode latency.'"
  }
]
</script>
</div>

### The Key Phrase

> **"TP = first lever, capped at 8 by NVLink, halves decode latency by halving per-GPU weight reads."**

### Connect Forward

Tomorrow: when one node isn't enough — **Pipeline Parallelism** (cross-node) and **Expert Parallelism** (for MoE).

### Pre-read for tomorrow (Day 17 · Pipeline & Expert Parallelism)

- **Resource:** <a href="https://lilianweng.github.io/posts/2023-01-10-inference-optimization/" target="_blank" rel="noopener">Lilian Weng — Large Transformer Model Inference Optimization</a> (~20 min, Pipeline Parallelism + MoE sections). Alternative: <a href="https://huggingface.co/docs/transformers/v4.15.0/parallelism" target="_blank" rel="noopener">Hugging Face — Model Parallelism</a>.
- **Reflection questions:**
  1. PP splits a model how? (Hint: depth-wise.)
  2. What is a "pipeline bubble" and why is it bad?
  3. In a Mixture-of-Experts model, what does Expert Parallelism distribute, and why is its communication pattern different from TP?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
