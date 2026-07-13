# Day 17 · Pipeline & Expert Parallelism

> **Concept of the day:** **PP** splits the model by layer depth across nodes — needed when one node isn't enough. **EP** distributes experts in MoE models across GPUs. **Pipeline bubbles** = the idle time PP creates.<br>
> **Pre-reading:** Pipeline parallelism + Expert Parallelism — <a href="https://lilianweng.github.io/posts/2023-01-10-inference-optimization/" target="_blank" rel="noopener">Lilian Weng — Large Transformer Model Inference Optimization</a> (PP and MoE sections).

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
    {status:week-04/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review + Readiness Check |
| Part 2 | Core Concept: Pipeline Parallelism |
| Part 3 | Deep Dive: Bubbles & TP vs PP |
| Part 4 | Core Concept: Expert Parallelism |
| Part 5 | Hands-On: Config Design |
| Part 6 | Wrap-up & Connection |

---

## Part 1 — Pre-Reading Review + Readiness Check
### Before You Start

You should have already read: Pipeline parallelism overview + Mixtral MoE architecture — Pre-Lecture Reading **Reader 8**.

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m2-readiness" data-kind="readiness" data-draw="5" data-source="Lilian Weng — Large Transformer Model Inference Optimization">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What axis does pipeline parallelism (PP) split along? What does each GPU hold?",
    "options": [
      "PP splits along the batch dimension; each GPU holds different samples",
      "PP splits along the layer depth; each GPU holds consecutive layers of the model",
      "PP splits along the attention head dimension; each GPU holds different heads",
      "PP splits along the vocabulary dimension; each GPU holds different tokens"
    ],
    "answer": 1,
    "explain": "Pipeline parallelism splits the model along layer depth. Each GPU (or node) holds consecutive layers. For example, with 8 layers and 2 GPUs, GPU 0 has layers 0-3, GPU 1 has layers 4-7."
  },
  {
    "stem": "What is a 'pipeline bubble' in pipeline parallelism?",
    "options": [
      "A memory overflow error",
      "The idle time when some GPUs are waiting for others to complete their computation",
      "A technique to reduce memory usage",
      "A type of pipeline parallelism"
    ],
    "answer": 1,
    "explain": "A pipeline bubble is the idle time when some GPUs are waiting. At the start, GPU 1 waits for GPU 0 to finish first layer. At the end, GPU 0 waits for GPU 1. This idle time is the bubble overhead."
  },
  {
    "stem": "Why does a pipeline bubble exist?",
    "options": [
      "Because GPUs are too slow",
      "Because of the sequential nature of layer computation — later layers can't start until earlier layers finish",
      "Because of memory limitations",
      "Because of network latency"
    ],
    "answer": 1,
    "explain": "Bubbles exist because transformer layers have dependencies: layer N needs output from layer N-1. This creates sequential bottlenecks. Techniques like microbatching help reduce bubble overhead."
  },
  {
    "stem": "Pipeline parallelism needs ___ bandwidth between stages compared to tensor parallelism.",
    "options": [
      "Much higher",
      "Much lower",
      "The same",
      "No"
    ],
    "answer": 1,
    "explain": "PP needs much lower bandwidth between stages because it only passes activations (layer input/output), not model weights. TP needs to communicate weights for each layer computation — much higher bandwidth."
  },
  {
    "stem": "In a Mixture of Experts (MoE) model, what is an 'expert'?",
    "options": [
      "A human researcher",
      "A separate feedforward network that processes different inputs",
      "A type of GPU",
      "A training dataset"
    ],
    "answer": 1,
    "explain": "An 'expert' in MoE is a separate feedforward network (MLP) within the model. In Mixtral, each layer has 8 experts, and only 2 are activated per token — sparse MoE."
  },
  {
    "stem": "What is 'Top-K routing' in MoE models?",
    "options": [
      "Selecting the top K most important features",
      "For each token, selecting the K most relevant experts to process it",
      "Routing to the K nearest experts",
      "Sorting experts by size"
    ],
    "answer": 1,
    "explain": "Top-K routing: for each input token, the model selects the top-K most relevant experts (Mixtral uses Top-2). This gives sparse activation — only a fraction of experts process each token."
  },
  {
    "stem": "Why does Expert Parallelism (EP) create load-balancing problems that Tensor Parallelism (TP) doesn't?",
    "options": [
      "EP doesn't have load balancing",
      "Because different tokens may route to different experts, causing some experts to be over/under-utilized",
      "Because TP is more efficient",
      "There is no difference"
    ],
    "answer": 1,
    "explain": "EP routes tokens to experts dynamically. If one expert gets more 'popular' tokens, it becomes overloaded while others idle. TP has fixed computation per layer. EP needs load-balancing mechanisms (like aux loss) to prevent this."
  },
  {
    "stem": "What is the key advantage of Pipeline Parallelism over Tensor Parallelism?",
    "options": [
      "PP is faster than TP",
      "PP requires less communication bandwidth between stages",
      "PP doesn't create bubbles",
      "PP works on a single GPU"
    ],
    "answer": 1,
    "explain": "PP requires much less bandwidth because only layer activations (not weights) are passed between stages. TP needs to communicate weight matrices. This makes PP suitable for multi-node clusters with less network bandwidth."
  }
]
</script>
</div>

---

## Part 2 — Core Concept — Pipeline Parallelism
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

## Part 3 — Deep Dive — Bubbles & TP vs PP
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

## Part 4 — Core Concept — Expert Parallelism
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

## Part 5 — Hands-On — Config Design
### Exercise 1: Pipeline Bubble Math

Compute pipeline bubble fraction for `num_stages = 4` and 1, 4, 16, 64 micro-batches.

**Formula:** Bubble fraction ≈ `(num_stages − 1) / num_micro_batches`

**Calculate:**
- stages=4, microbatches=1: (4-1)/1 = 3 → 300% bubble!
- stages=4, microbatches=4: (4-1)/4 = 0.75 → 75% bubble
- stages=4, microbatches=16: (4-1)/16 = 0.1875 → ~19% bubble
- stages=4, microbatches=64: (4-1)/64 = 0.047 → ~5% bubble ✓

### Exercise 2: 405B Model Design

Llama-3-405B FP16 = 810 GB. Design a config on 16 H100s:
- TP, PP, per-GPU shard size, comms budget

**Hint:** 810 GB ÷ 16 GPUs = 50.6 GB per GPU. With 80 GB H100s, you need TP=8 (17.5 GB weights) + PP=2 to fit.

---

## Part 7 — Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 17 · Pipeline Parallelism &amp; MoE">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What axis does pipeline parallelism (PP) split the model along?",
    "options": [
      "The hidden dimension — each GPU holds part of each layer's weights",
      "The layer dimension — different groups of layers run on different GPUs",
      "The batch dimension — different requests run on different GPUs",
      "The vocabulary dimension — each GPU handles part of the output projection"
    ],
    "answer": 1,
    "explain": "Pipeline parallelism splits the model by depth: GPU 1 holds layers 1–8, GPU 2 holds layers 9–16, etc. A mini-batch passes through each stage sequentially. This is different from tensor parallelism (TP) which splits within a single layer."
  },
  {
    "stem": "What is a pipeline bubble in pipeline parallelism?",
    "options": [
      "A memory overflow that occurs when the KV cache exceeds HBM capacity",
      "Idle time on GPUs earlier in the pipeline while they wait for forward-pass data from the previous stage",
      "A network congestion event when multiple GPUs send activations simultaneously",
      "An out-of-memory error caused by storing too many intermediate activations"
    ],
    "answer": 1,
    "explain": "Pipeline bubbles are idle GPU cycles at the start and end of each batch. GPU 1 finishes its forward pass and idles while GPU 2 completes and passes activations forward. Microbatching (splitting the batch into smaller chunks) fills these gaps by keeping the pipeline occupied."
  },
  {
    "stem": "How does tensor parallelism (TP) communication differ from pipeline parallelism (PP) communication?",
    "options": [
      "TP sends gradients between GPUs; PP sends activations",
      "TP requires all-reduce communication at every layer (within-layer splits); PP only sends activations at layer boundaries",
      "TP is for inter-node communication; PP is for intra-node",
      "TP uses NVLink; PP uses PCIe"
    ],
    "answer": 1,
    "explain": "TP splits matrix multiplications within each layer, requiring an all-reduce at each layer boundary — high-frequency, small messages. PP splits by layers, so communication happens only at stage boundaries — lower frequency, larger activations. TP needs NVLink bandwidth; PP can tolerate slower interconnects."
  },
  {
    "stem": "What is an MoE (Mixture of Experts) model?",
    "options": [
      "A model that requires multiple GPUs to run",
      "A model where only a subset of 'expert' feed-forward networks are activated per token, reducing compute cost while maintaining parameter count",
      "A model architecture with more attention heads than standard transformers",
      "A model that uses specialized hardware (ASICs) instead of GPUs"
    ],
    "answer": 1,
    "explain": "MoE models (e.g., Mixtral) have many feed-forward expert layers but only activate K of N experts per token (sparse activation). This allows large parameter count (capacity) with lower compute per token, but creates routing and load-balancing complexity."
  },
  {
    "stem": "What problem does Expert Parallelism (EP) create that requires careful management?",
    "options": [
      "Expert parallelism requires all experts to be on the same GPU",
      "Hot expert imbalance — some experts receive far more tokens than others, creating compute bottlenecks on their GPUs while others sit idle",
      "EP cannot be combined with tensor parallelism",
      "EP doubles the memory required because experts are duplicated across GPUs"
    ],
    "answer": 1,
    "explain": "If certain experts are 'hot' (routed more tokens), those GPUs are overloaded while GPUs hosting less-popular experts are underutilized. This load imbalance reduces overall throughput. Solutions include auxiliary loss to encourage balanced routing and expert replication."
  },
  {
    "stem": "Which phrase captures the rule for choosing between TP, PP, and EP?",
    "options": [
      "TP for throughput, PP for latency, EP for cost",
      "TP for latency (within node), PP for fit (across nodes), EP for MoE throughput",
      "TP for large models, PP for small models, EP for very small models",
      "Use only one parallelism strategy at a time"
    ],
    "answer": 1,
    "explain": "The lesson states: 'TP for latency (within node), PP for fit (across nodes), EP for MoE throughput.' TP uses fast NVLink within a node to split layers for low latency. PP scales across nodes to fit models too large for a single node. EP handles MoE expert routing."
  },
  {
    "stem": "According to the lesson, how do you shrink the pipeline bubble fraction?",
    "options": [
      "Add more pipeline stages so the idle time is spread thinner",
      "Switch the interconnect from InfiniBand to NVLink between stages",
      "Increase the number of micro-batches — bubble fraction is approximately (num_stages - 1) / num_micro_batches, so more micro-batches keeps stages filled",
      "Reduce the hidden dimension of each transformer layer"
    ],
    "answer": 2,
    "explain": "The lesson gives the bubble fraction as approximately (num_stages - 1) / num_micro_batches. Scheduling many micro-batches concurrently fills the stages and drives the bubble toward zero: at stages=4, going from 1 to 64 micro-batches drops the bubble from ~300% to ~5%. Real systems target under 10%."
  },
  {
    "stem": "In Mixtral 8x7B, why is only about 13B of its ~47B total parameters active per token?",
    "options": [
      "It uses top-2-of-8 expert routing, so each token flows through only 2 of the 8 expert MLPs per layer",
      "The other ~34B parameters are stored on CPU and never used at inference",
      "Mixtral quantizes ~34B of its parameters down to zero",
      "Only the attention layers run per token; all experts are skipped"
    ],
    "answer": 0,
    "explain": "An MoE layer has many expert MLPs but each token is routed to only a small subset. Mixtral uses top-2 of 8 experts (8 experts x ~7B each), so ~13B parameters are active per token even though the model totals ~47B. Total parameters are huge; active parameters per token stay small."
  },
  {
    "stem": "What communication pattern does Expert Parallelism (EP) rely on to route tokens to their experts?",
    "options": [
      "All-reduce at every layer, exactly like tensor parallelism",
      "Point-to-point activation passing between adjacent stages, exactly like pipeline parallelism",
      "A single broadcast from a central parameter server to all experts",
      "All-to-all — each token's activation is sent to the GPUs holding its selected experts, and the results are sent back"
    ],
    "answer": 3,
    "explain": "In EP each expert lives on a different GPU. Per token: the router picks the top-K experts, the token's activation is all-to-all'd to those experts, each expert computes locally, and the results are all-to-all'd back. All-to-all is expensive because every token touches the network, which is part of why EP is hard."
  },
  {
    "stem": "How does production MoE serving typically combine parallelism strategies?",
    "options": [
      "It uses expert parallelism alone and never mixes in TP or PP",
      "In a 3D mesh — for example TP within a node for dense weights and attention, EP across nodes to distribute experts, and PP (1 or 2) only if the model still exceeds capacity",
      "It always picks exactly one strategy and refuses to combine them",
      "It uses PP to split experts and EP to split layers"
    ],
    "answer": 1,
    "explain": "The lesson describes a TP x EP x PP 3D mesh: e.g. TP=8 within a node for dense weights plus attention, EP=8 across nodes distributing experts, and PP=1 or 2 only if the model exceeds even that. Each stage can still use TP internally, so the strategies stack."
  }
]
</script>
</div>

### The Key Phrase

> **"TP for latency (within node), PP for fit (across nodes), EP for MoE throughput."**

### Connect Forward

Tomorrow: **speculative decoding** — turn slow sequential decode into a series of fast mini-prefills.

### Pre-read for tomorrow (Day 18 · Speculative Decoding)

- **Resource:** <a href="https://huggingface.co/blog/assisted-generation" target="_blank" rel="noopener">Hugging Face — Assisted Generation (Speculative Decoding)</a>. Alternative: <a href="https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/" target="_blank" rel="noopener">NVIDIA — An Introduction to Speculative Decoding</a>.
- **Reflection questions:**
  1. Decode is memory-bound and sequential. What can a smaller "draft" model contribute?
  2. What does the big "target" model verify?
  3. What's the expected speedup? What kills it?

- **Resource:** "Speculative decoding explained" with diagrams — Pre-Lecture Reading **Reader 8** (advanced serving).
- **Reflection questions:**
  1. Decode is memory-bound and sequential. What can a smaller "draft" model contribute?
  2. What does the big "target" model verify?
  3. What's the expected speedup? What kills it?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
