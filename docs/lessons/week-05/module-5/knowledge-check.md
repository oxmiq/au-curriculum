<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <a href="../">Day 25 · Consolidation + Phase 1 Problem Set</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-05/module-5}
  </div>
</div>

# Week 5 Knowledge Check

**Phase 1 Assessment · Week 5.** 15 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Phase 1 Assessment · Week 5" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "A chat product reports P50 TTFT = 80 ms, P99 TTFT = 4200 ms. The most likely cause is:",
    "options": [
      "Slow GPU",
      "Queueing or batching tail under load",
      "Cold start",
      "Bad prompt"
    ],
    "answer": 1,
    "explain": "P99/P50 > 5× signals tail behaviour: queue depth or batch boundaries, not raw compute speed."
  },
  {
    "stem": "You compress a 70B model FP16 → FP8. Decode throughput should:",
    "options": [
      "Stay the same",
      "Roughly double",
      "Halve",
      "Drop 10×"
    ],
    "answer": 1,
    "explain": "Half the bytes per token on memory-bound decode ≈ 2× throughput."
  },
  {
    "stem": "For a request with 100 input / 5000 output tokens, what dominates wall-clock?",
    "options": [
      "Prefill",
      "Decode",
      "Tokenization",
      "Network"
    ],
    "answer": 1,
    "explain": "5000 sequential decode steps swamp the one parallel prefill."
  },
  {
    "stem": "TP=8 on 8×H100 instead of TP=4 on 4×H100 (same model that fits both): primary benefit is:",
    "options": [
      "Lower decode latency (less per-GPU weight to read)",
      "Higher quality",
      "Lower cost",
      "Smaller model"
    ],
    "answer": 0,
    "explain": "Decode latency drops roughly linearly with TP because per-GPU weight bytes drop."
  },
  {
    "stem": "Continuous batching gives ~5–10× throughput over static batching because:",
    "options": [
      "Better GPU drivers",
      "Requests admit at every decode step, no waiting at batch boundaries; GPU stays full",
      "Tensor Cores get faster",
      "Smaller model"
    ],
    "answer": 1,
    "explain": "Static batching wastes idle time between batches and on tail-output requests."
  },
  {
    "stem": "Speculative decoding produces output that is:",
    "options": [
      "Slightly different",
      "Provably identical to vanilla sampling from the target model",
      "Always worse",
      "Faster but lower quality"
    ],
    "answer": 1,
    "explain": "Under speculative sampling — identical distribution. Pure systems win."
  },
  {
    "stem": "Which is the MOST honest single quality metric for shipping a quantization change?",
    "options": [
      "Perplexity",
      "MMLU",
      "Your own task-eval pass rate + side-by-side win rate",
      "Loss"
    ],
    "answer": 2,
    "explain": "Public benchmarks are gameable / overfit; task evals reflect your customers."
  },
  {
    "stem": "Goodhart's Law applied to LLM serving means:",
    "options": [
      "Measure more",
      "Once you bonus a single metric, behaviour will optimize for that metric at the cost of others; report a vector with percentiles",
      "Trust averages",
      "Use only P50"
    ],
    "answer": 1,
    "explain": "Always report a vector of metrics with percentiles, not a single number."
  },
  {
    "stem": "PagedAttention's contribution is best described as:",
    "options": [
      "Better attention math",
      "OS-style virtual paging for KV cache, eliminating fragmentation",
      "Quantization",
      "Speculation"
    ],
    "answer": 1,
    "explain": "Fixed-size KV blocks + per-request block table = OS paging analogy."
  },
  {
    "stem": "Choose the right deployment for: bursty internal tool, ~5% GPU utilization, no privacy constraints:",
    "options": [
      "Dedicated 8×H100",
      "Hosted API per-token",
      "Pipeline parallelism",
      "Build your own GPU"
    ],
    "answer": 1,
    "explain": "Low-utilization workloads — APIs are dramatically cheaper than idle dedicated GPUs."
  },
  {
    "stem": "Llama-3-70B FP8 weights on 8×H100 with NVLink, TP=8: per-GPU weight shard is:",
    "options": [
      "140 GB",
      "70 GB",
      "17.5 GB",
      "8.75 GB"
    ],
    "answer": 3,
    "explain": "70B params × 1 byte FP8 = 70 GB; / 8 = 8.75 GB per shard."
  },
  {
    "stem": "A new vLLM version arrives. Best rollout strategy:",
    "options": [
      "Push to production immediately",
      "Canary 1% → 10% → 100% with metrics gates",
      "Replace the model at the same time",
      "Skip evaluation"
    ],
    "answer": 1,
    "explain": "Canary catches regressions early; never combine engine + model changes."
  },
  {
    "stem": "Cold start for a fresh 70B-FP16 replica is typically:",
    "options": [
      "100 ms",
      "1–2 sec",
      "1–5 min",
      "Hours"
    ],
    "answer": 2,
    "explain": "Pull image (10s of GB), load weights into HBM, warm kernels — minutes."
  },
  {
    "stem": "Mixtral 8x7B is described as 'top-2 of 8 experts.' Per token, active params ≈:",
    "options": [
      "7B",
      "13B",
      "47B",
      "56B"
    ],
    "answer": 1,
    "explain": "Two ~7B expert MLPs + shared attention ≈ 13B active per token."
  },
  {
    "stem": "FlashAttention + PagedAttention together are most important for which workload?",
    "options": [
      "Short-context, single-stream",
      "Long-context, high-concurrency serving",
      "Training",
      "Embedding generation"
    ],
    "answer": 1,
    "explain": "FlashAttention kills per-step HBM traffic; PagedAttention enables high concurrency without fragmentation. Both shine at long context + many users."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 25 · Consolidation + Phase 1 Problem Set](index.md)

-   __Back to the week__

    [Week 5 — Metrics &amp; Production overview](../index.md)

-   __Continue the curriculum__

    [Day 26 · Prompt Engineering](../../week-06/module-1/index.md)

</div>
