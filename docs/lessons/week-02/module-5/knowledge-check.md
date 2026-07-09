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

**Week 2 · Inference: GPU & Memory.** 12 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
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
    "stem": "Tensor Cores are…",
    "options": [
      "Larger CUDA cores",
      "Specialized units that accelerate matrix multiplication",
      "On-chip caches",
      "Networking hardware"
    ],
    "answer": 1,
    "explain": "Tensor Cores do small dense matrix-multiply-accumulate in one cycle — the AI workhorse."
  },
  {
    "stem": "Order these from fastest to slowest interconnect:",
    "options": [
      "PCIe → NVLink → InfiniBand → Ethernet",
      "NVLink → PCIe → InfiniBand → Ethernet",
      "InfiniBand → NVLink → PCIe → Ethernet",
      "NVLink → InfiniBand → PCIe → Ethernet"
    ],
    "answer": 1,
    "explain": "Intra-node NVLink (900 GB/s) > PCIe (~64 GB/s) > InfiniBand (~50 GB/s per NIC) > Ethernet."
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
      "It keeps intermediate values in registers instead of writing them to HBM",
      "It compiles to better SIMD",
      "It uses Tensor Cores instead of CUDA cores"
    ],
    "answer": 1,
    "explain": "FlashAttention is exactly this trick — fewer HBM round-trips, same algebra."
  },
  {
    "stem": "Pick the BEST classification of these workloads:",
    "options": [
      "Decode = compute-bound · Prefill = memory-bound",
      "Decode = memory-bound · Prefill = compute-bound",
      "Both = compute-bound",
      "Both = network-bound"
    ],
    "answer": 1,
    "explain": "The single most important sentence in Phase 1."
  },
  {
    "stem": "What is <strong>temporal locality</strong>?",
    "options": [
      "Reading nearby memory addresses",
      "Reading the same address again soon",
      "Doing math in parallel",
      "Writing back to disk"
    ],
    "answer": 1,
    "explain": "Temporal = same value reused; spatial = neighbouring addresses."
  },
  {
    "stem": "Doubling memory bandwidth on a memory-bound kernel roughly:",
    "options": [
      "Has no effect — it's compute-bound",
      "Roughly doubles throughput",
      "Halves throughput",
      "Increases latency"
    ],
    "answer": 1,
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
