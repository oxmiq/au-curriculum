<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 4 — Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <a href="../">Day 20 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-04/module-5}
  </div>
</div>

# Week 4 Knowledge Check

**Week 4 · Scaling & Stacks.** 15 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 4 · Scaling &amp; Stacks" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Tensor parallelism is most beneficial because it:",
    "options": [
      "Adds more memory",
      "Splits each layer's weights across GPUs, reducing per-GPU decode reads",
      "Replaces FlashAttention",
      "Eliminates the KV cache"
    ],
    "answer": 1,
    "explain": "TP shards weights → less per-GPU HBM traffic per token → lower decode latency."
  },
  {
    "stem": "TP must run within one node because:",
    "options": [
      "NVIDIA only allows it",
      "NVLink bandwidth is needed for the per-layer all-reduce",
      "Pipeline parallelism doesn't exist",
      "Of legal restrictions"
    ],
    "answer": 1,
    "explain": "All-reduce after every layer demands NVLink-class bandwidth (~900 GB/s). PCIe/IB are too slow."
  },
  {
    "stem": "Llama-3-70B FP16 on tp=8: per-GPU weight shard is:",
    "options": [
      "140 GB",
      "70 GB",
      "17.5 GB",
      "8 GB"
    ],
    "answer": 2,
    "explain": "140 / 8 = 17.5 GB. Fits in 80 GB H100 with room for KV cache."
  },
  {
    "stem": "Pipeline parallelism splits the model:",
    "options": [
      "Width-wise (within layers)",
      "Depth-wise (across layers / stages)",
      "By head",
      "By precision"
    ],
    "answer": 1,
    "explain": "Each stage holds a contiguous block of layers; activations flow stage→stage."
  },
  {
    "stem": "A 'pipeline bubble' is:",
    "options": [
      "A GPU manufacturing defect",
      "Idle time in a stage waiting for inputs from a prior stage",
      "Out-of-memory error",
      "A cache eviction"
    ],
    "answer": 1,
    "explain": "Mitigated by running many micro-batches concurrently; bubble fraction ≈ (stages-1)/microbatches."
  },
  {
    "stem": "Which connection type is appropriate for cross-node pipeline parallelism?",
    "options": [
      "NVLink only",
      "PCIe Gen 3",
      "InfiniBand",
      "USB"
    ],
    "answer": 2,
    "explain": "InfiniBand (~50 GB/s/NIC) handles activation transfer between stages."
  },
  {
    "stem": "In a Mixture-of-Experts model with top-2 of 8 experts, each token activates:",
    "options": [
      "All 8 experts",
      "2 experts",
      "1 expert",
      "Depends on temperature"
    ],
    "answer": 1,
    "explain": "Router picks top-K (typically 2) experts per token; that's the 'active parameters' count."
  },
  {
    "stem": "Expert parallelism's biggest operational risk is:",
    "options": [
      "Out of memory",
      "Hot experts — uneven load creating stragglers",
      "Slow weights",
      "Quantization error"
    ],
    "answer": 1,
    "explain": "Routers don't produce uniform distributions; capacity planning must accommodate worst-case expert load."
  },
  {
    "stem": "Speculative decoding works by:",
    "options": [
      "Lossy approximation",
      "A small draft model proposes K tokens, the big model verifies all K in one parallel pass",
      "Pre-computing all possible outputs",
      "Skipping layers"
    ],
    "answer": 1,
    "explain": "Converts memory-bound decode into a batched-style verification step; 2–3× typical speedup."
  },
  {
    "stem": "Under proper speculative sampling, output quality vs vanilla decoding is:",
    "options": [
      "Lower",
      "Identical (provably)",
      "Higher",
      "Random"
    ],
    "answer": 1,
    "explain": "Speculative sampling is provably equivalent to sampling from the target model alone."
  },
  {
    "stem": "Static batching is wasteful primarily because:",
    "options": [
      "It uses too much memory",
      "New requests wait for the current batch to finish, and short outputs idle while long ones complete",
      "It only works on CPU",
      "It can't use TP"
    ],
    "answer": 1,
    "explain": "Continuous batching fixes both: admit at every step, evict on completion."
  },
  {
    "stem": "Continuous batching relies structurally on:",
    "options": [
      "FP8 weights",
      "Block-based KV-cache allocation (PagedAttention)",
      "Speculative decoding",
      "CPU offload"
    ],
    "answer": 1,
    "explain": "Variable-sized, dynamically allocated KV slots demand block allocation; that's why vLLM ships both."
  },
  {
    "stem": "vLLM is most associated with:",
    "options": [
      "Pipeline parallelism",
      "PagedAttention",
      "INT8 quantization",
      "Expert parallelism"
    ],
    "answer": 1,
    "explain": "vLLM's UC Berkeley team introduced PagedAttention."
  },
  {
    "stem": "Plain PyTorch is typically ___ slower than vLLM for serving:",
    "options": [
      "No different",
      "About 5–10×",
      "100×",
      "Faster"
    ],
    "answer": 1,
    "explain": "Missing: continuous batching, PagedAttention, FlashAttention, quantization, fused kernels."
  },
  {
    "stem": "Pick the BEST default engine choice for an OSS NVIDIA deployment with broad model support:",
    "options": [
      "vLLM",
      "TGI",
      "TensorRT-LLM",
      "SGLang"
    ],
    "answer": 0,
    "explain": "vLLM is the OSS default; TensorRT-LLM if you need NVIDIA peak; SGLang for tool/JSON-heavy."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 20 · Consolidation](index.md)

-   __Back to the week__

    [Week 4 — Scaling &amp; Stacks overview](../index.md)

-   __Continue the curriculum__

    [Day 21 · Latency vs Throughput](../../week-05/module-1/index.md)

</div>
