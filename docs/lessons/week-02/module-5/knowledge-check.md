<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 2 — The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <a href="../">Day 10 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-02/module-5}
  </div>
</div>

# Week 2 Knowledge Check

**Week 2 · Inference: GPU & Memory.** 21-question bank · **12 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m5-canonical" data-kind="wrap-up" data-draw="12" data-lesson="Week 2 · Inference: GPU &amp; Memory" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "One forward pass through a transformer produces…",
    "options": [
      "The entire response",
      "Exactly one output token",
      "All input embeddings",
      "One output sentence"
    ],
    "answer": 1,
    "explain": "Generation loops one forward pass per token; that's why decode is sequential and memory-bound."
  },
  {
    "stem": "What determines TTFT (Time To First Token)?",
    "options": [
      "The prefill phase — processing all input tokens before the first token can be produced",
      "The decode phase — the rate at which each subsequent output token is generated",
      "The size of the model's vocabulary",
      "The sampling temperature"
    ],
    "answer": 0,
    "explain": "The first token can only appear after all input tokens are processed, so prefill drives TTFT. Decode (one token at a time) drives TPS instead."
  },
  {
    "stem": "What does the KV cache store so that decode doesn't have to redo work?",
    "options": [
      "The final generated text, for repeated queries",
      "The model weights in a compressed form",
      "The key and value matrices from attention for previous tokens, so they aren't recomputed each step",
      "The tokenizer's vocabulary table"
    ],
    "answer": 2,
    "explain": "Without KV caching each decode step would recompute attention over every prior token. Caching the keys/values means each step only processes the new token — critical for decode efficiency."
  },
  {
    "stem": "A request has 1000 input tokens and generates 500 output tokens. How many sequential decode forward passes are required?",
    "options": [
      "1500 — one per input and output token",
      "1000 — one per input token",
      "1 — decode processes all output tokens in parallel",
      "500 — one decode pass per output token"
    ],
    "answer": 3,
    "explain": "Prefill processes the 1000 input tokens in parallel (one pass); decode then generates the 500 output tokens one at a time — 500 sequential decode passes."
  },
  {
    "stem": "An H100 SXM5 has roughly:",
    "options": [
      "24 GB GDDR6X, 1 TB/s",
      "40 GB HBM2, 1.5 TB/s",
      "80 GB HBM3, ~3.35 TB/s",
      "192 GB HBM3e, 8 TB/s"
    ],
    "answer": 2,
    "explain": "80 GB HBM3 and ~3.35 TB/s — the two numbers everyone should know cold."
  },
  {
    "stem": "The RTX 4090 has roughly:",
    "options": [
      "24 GB GDDR6X, ~1 TB/s",
      "80 GB HBM3, ~3.35 TB/s",
      "12 GB GDDR6, ~0.27 TB/s",
      "48 GB HBM2, ~2 TB/s"
    ],
    "answer": 0,
    "explain": "The consumer RTX 4090 pairs 24 GB of GDDR6X with ~1 TB/s bandwidth — far less than the H100's 80 GB HBM3 at 3.35 TB/s, which limits how large a model it can serve."
  },
  {
    "stem": "Tensor Cores are…",
    "options": [
      "Specialized units that accelerate matrix multiplication",
      "Larger CUDA cores",
      "On-chip caches",
      "Networking hardware"
    ],
    "answer": 0,
    "explain": "Tensor Cores do dense matrix-multiply-accumulate in one operation — the AI workhorse. CUDA Cores are general-purpose ALUs by comparison."
  },
  {
    "stem": "Order these by bandwidth, highest to lowest:",
    "options": [
      "PCIe → NVLink → HBM",
      "NVLink → HBM → PCIe",
      "HBM → PCIe → NVLink",
      "HBM → NVLink → PCIe"
    ],
    "answer": 3,
    "explain": "On-GPU HBM (~3.35 TB/s) > NVLink GPU-to-GPU (~900 GB/s) > PCIe CPU-to-GPU (~64 GB/s). Staying on-chip is always fastest; crossing the PCIe bus is the slowest hop."
  },
  {
    "stem": "Order the GPU memory hierarchy from fastest to slowest:",
    "options": [
      "HBM → L2 → L1/Shared → Registers",
      "Registers → L1/Shared → L2 → HBM",
      "L2 → L1/Shared → Registers → HBM",
      "Registers → L2 → L1/Shared → HBM"
    ],
    "answer": 1,
    "explain": "Registers (<1 ns) → L1/Shared (~1 ns) → L2 (~5 ns) → HBM (~80 ns). Faster memory is smaller and closer to the compute units."
  },
  {
    "stem": "Why is decode memory-bound for a single user?",
    "options": [
      "Because attention is O(N²)",
      "Because the GPU re-reads all model weights from HBM per output token, doing only a tiny amount of math per byte",
      "Because the CPU is the bottleneck",
      "Because the network can't keep up"
    ],
    "answer": 1,
    "explain": "Arithmetic intensity ≈ 2 ops/byte vs ridge of ~295 → Tensor Cores idle ~99% of the time."
  },
  {
    "stem": "Arithmetic intensity is defined as:",
    "options": [
      "Bytes moved ÷ FLOPs",
      "FLOPs ÷ GPU clock speed",
      "FLOPs ÷ bytes moved from memory",
      "Tensor Cores ÷ CUDA Cores"
    ],
    "answer": 2,
    "explain": "Arithmetic intensity = FLOPs per byte fetched. High intensity means compute-bound; low intensity (like decode's ~2 ops/byte) means memory-bound."
  },
  {
    "stem": "Time to read 16 GB of weights from HBM at 3.35 TB/s is roughly:",
    "options": [
      "48 µs",
      "0.5 ms",
      "4.8 ms",
      "48 ms"
    ],
    "answer": 2,
    "explain": "16 / 3350 s ≈ 4.8 ms — the decode latency floor before any math."
  },
  {
    "stem": "Why can't you keep an entire LLM in L2 cache?",
    "options": [
      "Fast memory is small — L2 is only ~50 MB while models are many gigabytes",
      "L2 is actually slower than HBM, so it wouldn't help",
      "L2 can only store integers, not floating-point weights",
      "L2 is reserved for the operating system"
    ],
    "answer": 0,
    "explain": "The first rule of the hierarchy is 'fast memory is small.' L2 is ~50 MB versus 80 GB of HBM, so multi-GB weights must be streamed from HBM — the root of the memory bottleneck."
  },
  {
    "stem": "The 'ridge point' of a roofline is:",
    "options": [
      "Peak FLOPs ÷ memory bandwidth",
      "Bandwidth ÷ peak FLOPs",
      "Cache size ÷ register count",
      "Network bandwidth ÷ PCIe bandwidth"
    ],
    "answer": 0,
    "explain": "Intensity at which compute and bandwidth ceilings meet (≈ 295 ops/byte for H100 FP16)."
  },
  {
    "stem": "The ridge point of an RTX 4090 (165 TFLOPs, 1 TB/s) is approximately:",
    "options": [
      "~165 ops/byte",
      "~295 ops/byte",
      "~10 ops/byte",
      "~1000 ops/byte"
    ],
    "answer": 0,
    "explain": "Ridge = Peak FLOPs ÷ Bandwidth = 165 TFLOPs ÷ 1 TB/s ≈ 165 ops/byte. Different hardware has a different ridge, so the same kernel can be compute-bound on one GPU and memory-bound on another."
  },
  {
    "stem": "Where on the roofline does prefill typically sit?",
    "options": [
      "Memory-bound (left of ridge)",
      "Compute-bound (right of ridge, hitting the Tensor Core ceiling)",
      "Network-bound",
      "Below both ceilings"
    ],
    "answer": 1,
    "explain": "Prefill processes all input tokens in parallel → big GEMMs → high intensity → compute-bound."
  },
  {
    "stem": "Why does kernel fusion make code faster when it does the same math?",
    "options": [
      "It uses more FLOPs",
      "It compiles to better SIMD instructions",
      "It keeps intermediate values in registers instead of writing them to HBM",
      "It uses Tensor Cores instead of CUDA cores"
    ],
    "answer": 2,
    "explain": "FlashAttention is exactly this trick — fewer HBM round-trips, same algebra."
  },
  {
    "stem": "Pick the BEST classification of these workloads:",
    "options": [
      "Both = network-bound",
      "Decode = compute-bound · Prefill = memory-bound",
      "Both = compute-bound",
      "Decode = memory-bound · Prefill = compute-bound"
    ],
    "answer": 3,
    "explain": "The single most important sentence in Phase 1: prefill hits the Tensor Cores, decode waits on HBM."
  },
  {
    "stem": "Why does batching many users' decode steps together improve GPU utilization?",
    "options": [
      "It reduces the model's parameter count",
      "It reuses one weight load across many requests, raising the effective arithmetic intensity",
      "It moves the workload from the GPU to the CPU",
      "It shrinks the KV cache"
    ],
    "answer": 1,
    "explain": "A single decode reads all weights to do ~2 ops/byte. Batching 8 requests reads those weights once but does 8× the compute — intensity ×8, pulling a memory-bound workload toward the ridge."
  },
  {
    "stem": "What is <strong>temporal locality</strong>?",
    "options": [
      "Reading the same address again soon",
      "Reading nearby memory addresses",
      "Doing math in parallel",
      "Writing back to disk"
    ],
    "answer": 0,
    "explain": "Temporal = same value reused soon; spatial = neighbouring addresses. Caches (and the KV cache) exploit temporal locality."
  },
  {
    "stem": "Doubling memory bandwidth on a memory-bound kernel roughly:",
    "options": [
      "Has no effect — it's compute-bound",
      "Halves throughput",
      "Roughly doubles throughput",
      "Increases latency"
    ],
    "answer": 2,
    "explain": "Memory-bound = bandwidth ceiling — more bandwidth lifts the ceiling proportionally."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 10 · Consolidation](index.md)

-   __Back to the week__

    [Week 2 — The GPU &amp; Memory overview](../index.md)

-   __Continue the curriculum__

    [Day 11 · Prefill vs Decode](../../week-03/module-1/index.md)

</div>
