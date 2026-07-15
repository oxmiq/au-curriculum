# Day 11 · Prefill and Decode

> **Concept of the day:** the two phases of inference. **Prefill** = parallel, compute-bound, drives TTFT. **Decode** = sequential, memory-bound, drives TPS.<br>
> **Pre-reading:** "Prefill vs decode" explainer: <a href="https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices" target="_blank" rel="noopener">Databricks - LLM Inference Performance Engineering Best Practices</a> (read the prefill/decode section).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 - Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 11 · Prefill vs Decode</span>
    {status:week-03/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Prefill |
| Part 3 | Core Concepts: Decode |
| Part 4 | Visual Timeline |
| Part 5 | Hands-On: Calculate |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: "Prefill vs decode" explainer: Pre-Lecture Reading **Reader 4 (attention math)** and Reader 6 sections on serving.

### Quick Self-Check

Answer these questions from memory:

1. Which phase processes all input tokens at once? Which one at a time?
2. Which phase is compute-bound? Which is memory-bound?
3. What does **TTFT** stand for? What drives it?

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m1-readiness" data-kind="readiness" data-draw="5" data-source="Databricks - LLM Inference Performance Engineering Best Practices">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What is the key difference between the prefill and decode phases?", "options": ["Prefill processes one token at a time; decode processes all tokens in parallel", "Prefill processes all input tokens in parallel; decode generates one token at a time sequentially", "Prefill is for loading the model; decode is for running inference", "There is no difference; they are the same thing"]},
  {"stem": "Which phase is typically compute-bound?", "options": ["Decode", "Prefill", "Both are memory-bound", "Neither: both are compute-bound"]},
  {"stem": "Which phase is typically memory-bound?", "options": ["Prefill", "Decode", "Both are compute-bound", "Neither: both are memory-bound"]},
  {"stem": "What does TTFT stand for, and what does it primarily depend on?", "options": ["Time To First Token: primarily depends on decode phase speed", "Time To First Token: primarily depends on prefill phase speed", "Total Time For Training: depends on compute capacity", "Token Transfer Fine Time: depends on network speed"]},
  {"stem": "What does TPS stand for, and what does it primarily depend on?", "options": ["Tokens Per Second: primarily depends on prefill speed", "Tokens Per Second: primarily depends on decode speed", "Throughput Per Sequence: depends on batch size", "Time Per Sequence: depends on model size"]},
  {"stem": "Why does prefill being compute-bound mean it benefits from more compute resources?", "options": ["Compute resources don't help prefill", "It does lots of matrix multiplications in parallel, so more SMs/Tensor Cores directly reduces latency", "It is limited by memory bandwidth", "It only benefits from more memory"]},
  {"stem": "Why does decode being memory-bound mean it benefits more from batching than from faster GPUs?", "options": ["Decode doesn't benefit from batching", "Decode is limited by compute, so faster GPUs help more", "Batching amortizes the memory read across multiple sequences, increasing effective compute per memory access", "Batching doesn't help decode: only prefill"]},
  {"stem": "In the two-phase inference model, what is the 'memory-bound wall' that decode hits?", "options": ["The model runs out of VRAM", "The GPU is waiting on data from HBM more than it's computing: limited by memory bandwidth", "The model is too large to fit in memory", "The GPU overheats"]}
]
</script>
</div>

---

## Part 2 - Core Concepts - Prefill
### Reading - The Two Phases

This is the conceptual hinge of the entire serving stack. Every metric, every engine, every parallelism choice in Weeks 4–5 is about *which phase* it optimizes. Confuse them and your latency/throughput trade-offs make no sense.

### Prefill - Process All Input Tokens in Parallel

> **Analogy: reading a whole book to build context.**

Given N input tokens, prefill runs them through the transformer as a single large batch. The work is one giant set of GEMMs:

| Property | Prefill |
|----------|---------|
| **Processing** | Parallel across all N tokens |
| **Bottleneck** | Compute-bound: high arithmetic intensity |
| **Time scales** | Linearly with N (short context), quadratically (attention layer, long context) |
| **Produces** | First output token + initial KV cache |
| **Metric** | **TTFT** (Time To First Token) |

### Why Prefill is Compute-Bound

- All input tokens processed simultaneously
- Large matrix multiplications (GEMMs)
- High arithmetic intensity (hundreds of ops/byte)
- You're hitting the Tensor Cores, not waiting on HBM

---

## Part 3 - Core Concepts - Decode
### Decode - One Token at a Time

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
| **Processing** | Sequential: each token depends on previous |
| **Bottleneck** | Memory-bound for single user |
| **Time per token** | Scales with model size and HBM bandwidth |
| **Metrics** | **ITL** (Inter-Token Latency), **TPS** (Tokens Per Second) |

### Why Decode is Memory-Bound

- One token at a time
- Must re-read all model weights for each token
- Low arithmetic intensity (~2 ops/byte)
- GPU is idle ~99% of the time waiting for data

### The Metrics

- **ITL** - gap between consecutive output tokens
- **TPS** = 1000 / ITL_ms: tokens per second per stream

---

## Part 4 - Visual Timeline
### Reading - One Picture, Both Phases

```
time →
│■■■■■■│ ← prefill (one big GEMM batch)
       │█ █ █ █ █ █ █ █ ...│ ← decode (one token per step)
       ↑                       ↑
       TTFT (first token)       end-to-end latency
```

### Annotate the Timeline

1. **Prefill bar** - represents compute-bound phase
2. **Decode train** - represents sequential memory-bound phase
3. **TTFT** - time from request to first token (driven by prefill)
4. **End-to-end latency** - TTFT + (tokens × ITL)

---

## Part 5 - Hands-On - Calculate
### Exercise 1: Sketch the Timeline

Given a request with 1000 input + 500 output tokens:

1. Draw the timeline showing prefill and decode phases
2. Label where TTFT lives
3. Label where end-to-end latency lives

### Exercise 2: Numerical Calculation

**Given:** Llama-3-8B on one H100

**Estimate:**

1. **Prefill time** for 1000 input tokens (compute-bound, use ~989 TFLOPs FP16)
2. **Decode time** per token (memory-bound, use 16 GB ÷ 3.35 TB/s)
3. **Total wall-clock time**

**Hint:**
- Prefill: ~1000 tokens × (computation per token) ÷ TFLOPs
- Decode: ~16 GB ÷ 3.35 TB/s = ~4.8 ms per token × 500 tokens

---

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 11 · Prefill vs Decode">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What makes prefill compute-bound?", "options": ["Prefill reads the KV cache repeatedly for each token", "Prefill processes all input tokens in parallel as a large matrix multiply, fully utilizing Tensor Cores", "Prefill runs at reduced precision to fit the context window", "Prefill is limited by the network bandwidth between the user and the server"]},
  {"stem": "What makes decode memory-bound?", "options": ["Decode uses FP32 instead of FP16, requiring more compute per operation", "Decode generates one token at a time, requiring a full model weight read for just ~2 operations per parameter", "Decode requires reading the entire training dataset for each generated token", "Decode is limited by the PCIe bus connecting the GPU to the CPU"]},
  {"stem": "What metric does TTFT (Time To First Token) measure, and which inference phase drives it?", "options": ["Time to generate all output tokens; driven by the decode phase", "Time until the model produces its first output token; driven by the prefill phase", "Total round-trip time from browser to server; driven by network latency", "Time to load model weights into GPU memory; driven by the embedding phase"]},
  {"stem": "What metric does TPS (Tokens Per Second) measure, and which phase drives it?", "options": ["How many users are served per second; driven by load balancing", "How fast output tokens are generated after the first token; driven by the decode phase", "How fast input tokens are tokenized; driven by the CPU", "The total token throughput across all requests on a server; driven by batching"]},
  {"stem": "Why does decode take longer per token than prefill, despite each decode step processing only one token?", "options": ["Decode uses a larger model than prefill", "Decode reads the entire KV cache and model weights for every single token: a memory-bound serial operation with no parallelism", "Decode must re-tokenize the output after each step", "Decode performs backpropagation to verify each generated token"]},
  {"stem": "For a user-facing chat application, which metric would you optimize first and why?", "options": ["End-to-end latency, because users only care about the total wait time", "TTFT, because users perceive the stream starting as 'fast' even if decode is slower", "Server throughput, because more requests/second reduces cost", "GPU utilization, because higher utilization always means better performance"]},
  {"stem": "When the prefill phase finishes, what has it produced besides beginning the response?", "options": ["The complete output response in a single parallel pass", "The first output token plus the initial KV cache for the prompt", "A quantized copy of the model weights for decode", "Only the tokenized input, with no computation performed yet"]},
  {"stem": "The lesson defines end-to-end latency in terms of the two phases. How is it computed?", "options": ["TTFT divided by the number of output tokens", "The prefill time alone, since decode overlaps with it", "TTFT + (number of output tokens × ITL)", "The decode time alone, since prefill is negligible"]},
  {"stem": "The lesson gives arithmetic-intensity figures for the two phases. Which statement matches them?", "options": ["Prefill runs at ~2 ops/byte; decode runs at hundreds of ops/byte", "Both phases run near the H100 ridge of ~295 ops/byte", "Prefill has high arithmetic intensity (hundreds of ops/byte); decode has low intensity (~2 ops/byte)", "Arithmetic intensity is identical in both phases"]},
  {"stem": "The lesson relates TPS to Inter-Token Latency (ITL). What is the relationship?", "options": ["TPS = ITL_ms × 1000", "TPS = 1000 / ITL_ms", "TPS and ITL measure unrelated things", "TPS = ITL_ms / 1000"]}
]
</script>
</div>

### The Key Phrase

> **"Prefill = compute, decode = memory."**

### Connect Forward

Tomorrow: the **KV cache** - the structure that makes decode possible at all, and the resource you spend the next three weeks trying to fit, share, and prune.

### Pre-read for tomorrow (Day 12 · The KV Cache)

- **Resource:** <a href="https://medium.com/@joaolages/kv-caching-explained-276520203249" target="_blank" rel="noopener">João Lages - KV Caching Explained</a>. Alternative: <a href="https://huggingface.co/docs/transformers/main/en/kv_cache" target="_blank" rel="noopener">Hugging Face - KV Cache in Transformers</a>.
- **Reflection questions:**
  1. What grows every time the model generates a token?
  2. Where in the transformer is the KV cache used?
  3. For a 70B model at 128K context, can the KV cache exceed the size of the model weights themselves?

---

## Stuck?

Ask **oxtutor**: share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
