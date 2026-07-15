# Day 9 · Compute-Bound vs Memory-Bound

> **Concept of the day:** ops:byte ratio. The roofline model. Which ceiling you're hitting. **Punchline: prefill = compute. Decode = memory.**<br>
> **Pre-reading:** <a href="https://horace.io/brrr_intro.html#compute" target="_blank" rel="noopener">Horace He - Making Deep Learning Go Brrr (Compute section)</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 - The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 9 · Compute-Bound vs Memory-Bound</span>
    {status:week-02/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Roofline Model |
| Part 3 | Deep Dive: Ridge Points |
| Part 4 | Deep Dive: Where Kernels Sit |
| Part 5 | Hands-On: Calculate |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: Pre-Lecture Reading **Reader 4 (complexity, memory, attention math)** + Study Guide §A.5 roofline subsection.

### Quick Self-Check

Answer these questions from memory:

1. If a kernel does 100 ops and reads 50 bytes, what's its intensity?
2. Why is prefill compute-bound and decode memory-bound? (One sentence.)
3. What does the *roofline model* tell you that arithmetic intensity alone doesn't?

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m4-readiness" data-kind="readiness" data-draw="5" data-source="Horace He - Making Deep Learning Go Brrr (Compute section)">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does the 'ops:byte ratio' (arithmetic intensity) measure?", "options": ["How many operations the GPU can do per second", "The ratio of compute operations to memory accesses in a kernel", "How much memory is used by the model", "The total number of operations in the model"]},
  {"stem": "Why is the prefill phase typically compute-bound?", "options": ["It processes many tokens in parallel, doing lots of matrix multiplications per byte read", "It reads from HBM repeatedly", "It uses small batch sizes", "It requires caching"]},
  {"stem": "Why is the decode phase typically memory-bound?", "options": ["It doesn't do any computation", "It generates one token at a time, so there's minimal compute per token read from HBM", "It uses too much VRAM", "It is always slower than prefill"]},
  {"stem": "What does the roofline model show that arithmetic intensity alone doesn't?", "options": ["The exact model latency", "The maximum performance achievable given your hardware's memory bandwidth and compute ceiling", "The number of parameters", "The batch size needed"]},
  {"stem": "What is a 'ridge point' in the roofline model?", "options": ["The highest point on the roofline", "The arithmetic intensity where compute-bound and memory-bound are equally limiting", "The point where batch size is optimal", "The memory bandwidth limit"]},
  {"stem": "If a kernel has arithmetic intensity 5, and your GPU's ridge point is 10, which ceiling are you hitting?", "options": ["Compute ceiling (compute-bound)", "Memory bandwidth ceiling (memory-bound)", "Neither - the kernel is perfectly balanced", "Both simultaneously"]},
  {"stem": "What is the key insight about batching for decode-phase inference?", "options": ["Batching doesn't help decode", "Batching increases arithmetic intensity by amortizing the memory access over more tokens", "Batching only works with large batch sizes", "Batching makes decode compute-bound"]},
  {"stem": "What does Horace He mean by 'making deep learning go brrr'?", "options": ["Making models sound funny", "Optimizing for throughput by addressing the memory bottleneck", "Running models on GPUs", "Using faster GPUs"]}
]
</script>
</div>

---

## Part 2 - Core Concepts - Roofline Model
### Reading - Why the Roofline Matters

Knowing *which ceiling* a workload hits tells you *which knob to turn*: more FLOPs (bigger / better Tensor Cores)? more bandwidth (HBM3e, NVLink)? more parallelism? You can't optimize what you can't classify.

### The Roofline Model

The roofline is a single plot that tells you the **maximum achievable performance** for a given workload on given hardware.

```
performance (FLOP/s)
   ▲
   │           ╭───── compute ceiling (peak TFLOPs)
   │          ╱
   │         ╱
   │        ╱
   │       ╱
   │      ╱       ← BW × intensity slope
   │     ╱
   │    ╱
   │   ╱
   ├──┴─────────────────────► arithmetic intensity (ops/byte)
       ridge point
       (peak FLOPs ÷ BW)
```

### How to Use the Roofline

For each kernel:

1. **Plot it horizontally** at its intensity (ops/byte)
2. **Plot it vertically** at its measured FLOP/s
3. The line above it is the ceiling:
   - Left of ridge: bandwidth-slope
   - Right of ridge: compute-ceiling

---

## Part 3 - Deep Dive - Ridge Points
### Reading - Ridge Point Examples

### Ridge Point Formula

> **Ridge Point = Peak FLOPs ÷ Bandwidth**

### Examples (FP16)

| Hardware | Peak FLOPs | BW | Ridge ≈ |
|---|---|---|---|
| H100 SXM5 | 989 TFLOPs | 3.35 TB/s | ~295 ops/byte |
| RTX 4090 | 165 TFLOPs | 1 TB/s | ~165 ops/byte |
| Wormhole n150 | ~74 TFLOPs | ~270 GB/s | ~274 ops/byte |

### Key Insight

- **Above the ridge:** You're compute-bound (hitting the Tensor Cores)
- **Below the ridge:** You're memory-bound (hitting the HBM bandwidth)

---

## Part 4 - Deep Dive - Where Kernels Sit
### Reading - Common Workloads

| Kernel | Intensity (rough) | Verdict |
|---|---|---|
| GEMM, large square | ~N (thousands) | **Compute-bound** |
| Prefill attention (long input) | ~hundreds | **Compute-bound** |
| Decode attention (one token) | ~2–10 | **Memory-bound** |
| Decode MLP (one token, one user) | ~2 | **Memory-bound** |
| Elementwise add / scale | ~0.5 | **Bandwidth-bound** |
| All-reduce across nodes | ~0 | **Network-bound** |

### The Punchline

> **Prefill = compute-bound.** All input tokens are processed in parallel → big GEMMs → intensity is high → you're hitting the Tensor Cores.
>
> **Decode = memory-bound.** One token at a time → you re-read all weights per token → intensity is tiny → you're hitting the HBM ceiling.

### Why This Matters - Every Week 3-4 Trick

| Trick | Why It Helps |
|-------|--------------|
| **KV cache** | Don't re-compute past keys/values, just read them |
| **FlashAttention** | Fuse attention into one pass, minimize HBM reads |
| **Quantization** | Fewer bits per weight = less data to move = decode goes faster |
| **Continuous batching** | Pack many users' decodes so weights are re-used across them |
| **Speculative decoding** | Convert decode (memory-bound, 1 token) into a small prefill (compute-bound, K tokens) |

---

## Part 5 - Hands-On - Calculate
### Exercise 1: Arithmetic Intensity

Calculate arithmetic intensity for:

**(a) `y = a*x + b` over 1M elements**
- FLOPs: 2 ops per element × 1M = 2M FLOPs
- Bytes: 3 arrays × 1M × 2 bytes (FP16) = 6 MB
- Intensity: 2M / 6M = ~0.33 ops/byte

**(b) Matrix multiply 4096×4096 by 4096×4096 in FP16**
- FLOPs: 2N³ = 2 × 4096³ = ~137B FLOPs
- Bytes: 3N² × 2 = ~100 MB
- Intensity: ~1,371,000 ops/byte

### Exercise 2: Tensor Core Utilization

At intensity = 2 ops/byte (decode), what fraction of H100's peak compute can you actually use?

**Calculation:**
- Ridge = ~295 ops/byte
- Your intensity = 2 ops/byte
- Fraction = 2 / 295 ≈ **0.68%**

**Answer:** Only ~0.7% of the Tensor Cores are being used! The other 99.3% are idle, waiting for data.

**Implication:** This explains why batching exists: if you pack multiple decodes together, you reuse weights and increase your effective intensity.

---

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 9 · Compute-Bound vs Memory-Bound">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does the roofline model show?", "options": ["The total FLOP count of a forward pass for a given model size", "The maximum achievable performance given a kernel's arithmetic intensity and the hardware's compute and bandwidth limits", "The maximum memory that can be used before an OOM error occurs", "The latency from submitting a request to receiving the first output token"]},
  {"stem": "Where does LLM decode sit on the roofline, relative to the ridge point?", "options": ["Well above the ridge - it is heavily compute-bound", "At the ridge - it is perfectly balanced", "Well below the ridge - it is heavily memory-bound (~2 ops/byte vs ridge of ~295 ops/byte)", "Off the chart - the roofline does not apply to LLM workloads"]},
  {"stem": "During decode, approximately what fraction of Tensor Cores are actively being used on an H100?", "options": ["~50%", "~10%", "~5%", "~0.7%"]},
  {"stem": "Why does batching multiple decode requests together increase arithmetic intensity?", "options": ["Batching allows model weights to be split across multiple GPUs, reducing per-GPU memory pressure", "When N requests share a single forward pass, N×computations are done against the same weight load, multiplying intensity by N", "Batching enables the use of INT8 precision, which has higher ops/byte than FP16", "Batching reduces the KV cache size because requests share context"]},
  {"stem": "Where does LLM prefill sit on the roofline?", "options": ["Well below the ridge, even deeper into the memory-bound region than decode", "At or above the ridge - it is compute-bound because all input tokens are processed in parallel", "At the same point as decode since both use the same model weights", "Above all hardware limits - it exceeds both memory and compute ceilings"]},
  {"stem": "Name two techniques that attack the memory bottleneck in LLM decode.", "options": ["Gradient checkpointing and model pruning", "Quantization (reducing weight precision) and batching (amortizing weight reads across requests)", "Increasing GPU clock speed and adding more CUDA cores", "Reducing vocabulary size and using a smaller tokenizer"]},
  {"stem": "What is the ridge-point formula given in Part 3?", "options": ["Bandwidth ÷ Peak FLOPs", "Peak FLOPs ÷ Bandwidth", "Peak FLOPs × Bandwidth", "Peak FLOPs − Bandwidth"]},
  {"stem": "Using the Part 3 examples, what is the approximate ridge point of an RTX 4090 (165 TFLOPs, 1 TB/s)?", "options": ["~2,950 ops/byte", "~10 ops/byte", "~165 ops/byte", "~1,000 ops/byte"]},
  {"stem": "In the Part 4 workloads table, which kernel is classified as network-bound?", "options": ["GEMM, large square", "Decode attention (one token)", "All-reduce across nodes", "Prefill attention (long input)"]}
]
</script>
</div>

### Connect Forward

Friday: consolidation - Feynman teach-back across the four concepts (pipeline, GPU anatomy, memory hierarchy, roofline). Then the canonical [quiz](knowledge-check.md).

---

## Pre-read for Friday (Day 10 · Consolidation)

- **Resource:** None. Re-read your Day 6–9 notes. Bring your roofline plot.
- **Reflection questions:**
  1. Which of the four Week 2 days felt least clear?
  2. If you had to teach one of {pipeline, anatomy, bandwidth, roofline} to a peer in 5 minutes: which would you pick? Why?
  3. Write one question you want answered before Week 3.

---

## Stuck?

Ask **oxtutor**: share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
