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

**Phase 1 Assessment · Week 5.** 26-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Phase 1 Assessment · Week 5" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "A chat product reports P50 TTFT = 80 ms, P99 TTFT = 4200 ms. The most likely cause is:",
    "options": [
      "Slow GPU",
      "Cold start",
      "Queueing or batching tail under load",
      "Bad prompt"
    ],
    "answer": 2,
    "explain": "A P99/P50 ratio above 5× signals tail behaviour — queue depth or batch boundaries under load — not raw compute speed. Here the ratio is ~52×."
  },
  {
    "stem": "You compress a 70B model FP16 → FP8. Decode throughput should:",
    "options": [
      "Roughly double",
      "Stay the same",
      "Halve",
      "Drop 10×"
    ],
    "answer": 0,
    "explain": "Decode is memory-bandwidth bound. Halving the bytes read per token (FP16→FP8) roughly doubles decode throughput."
  },
  {
    "stem": "For a request with 100 input / 5000 output tokens, what dominates wall-clock time?",
    "options": [
      "Prefill",
      "Tokenization",
      "Network",
      "Decode"
    ],
    "answer": 3,
    "explain": "Prefill processes all 100 input tokens in one parallel pass; decode runs 5000 sequential steps, so decode swamps the total."
  },
  {
    "stem": "TP=8 on 8×H100 instead of TP=4 on 4×H100 (same model that fits both): the primary benefit is:",
    "options": [
      "Lower decode latency (less per-GPU weight to read)",
      "Higher quality",
      "Lower cost",
      "Smaller model"
    ],
    "answer": 0,
    "explain": "Decode latency is bound by the per-GPU weight bytes read each step. Doubling TP halves per-GPU shard bytes, so decode latency drops roughly linearly (cost stays similar because you use twice the GPUs)."
  },
  {
    "stem": "Continuous batching gives ~5–10× throughput over static batching because:",
    "options": [
      "Better GPU drivers",
      "Tensor Cores get faster",
      "Requests admit at every decode step, no waiting at batch boundaries; the GPU stays full",
      "The model is smaller"
    ],
    "answer": 2,
    "explain": "Static batching wastes idle time between batches and while short-output requests wait on long-output ones. Continuous batching admits and retires requests every decode step, keeping the GPU saturated."
  },
  {
    "stem": "Speculative decoding produces output that is:",
    "options": [
      "Slightly different",
      "Always worse",
      "Faster but lower quality",
      "Provably identical to sampling from the target model"
    ],
    "answer": 3,
    "explain": "Speculative sampling accepts a draft token only when it matches the target model's distribution, so the output distribution is provably identical — it is a pure systems speedup with no quality cost."
  },
  {
    "stem": "Which is the MOST honest single quality metric for shipping a quantization change?",
    "options": [
      "Perplexity",
      "MMLU",
      "Your own task-eval pass rate + side-by-side win rate",
      "Training loss"
    ],
    "answer": 2,
    "explain": "Perplexity is only a sanity check and public benchmarks are gameable/overfit. Task evals on your production distribution plus side-by-side win rate reflect what your customers actually experience."
  },
  {
    "stem": "Goodhart's Law applied to LLM serving means:",
    "options": [
      "Once you bonus a single metric, behaviour optimizes for that metric at the cost of others; report a vector with percentiles",
      "Measure more of everything",
      "Trust averages over percentiles",
      "Report only P50"
    ],
    "answer": 0,
    "explain": "'When a measure becomes a target, it ceases to be a good measure.' Bonus on average TPS and engineers will quietly let TTFT slip. Always report a vector of metrics with percentiles, not one number."
  },
  {
    "stem": "PagedAttention's contribution is best described as:",
    "options": [
      "Better attention math",
      "Quantization of the KV cache",
      "OS-style virtual paging for the KV cache, eliminating fragmentation",
      "Speculative decoding"
    ],
    "answer": 2,
    "explain": "PagedAttention stores the KV cache in fixed-size blocks with a per-request block table — an OS virtual-memory analogy — which eliminates fragmentation and enables high concurrency."
  },
  {
    "stem": "Choose the right deployment for a bursty internal tool at ~5% GPU utilization with no privacy constraints:",
    "options": [
      "Hosted API, priced per token",
      "Dedicated 8×H100",
      "Pipeline parallelism across nodes",
      "Build your own GPU cluster"
    ],
    "answer": 0,
    "explain": "Dedicated GPUs only break even around 30–50% sustained utilization. At ~5% util a per-token API is dramatically cheaper than paying for idle dedicated GPUs."
  },
  {
    "stem": "Llama-3-70B FP8 weights on 8×H100 with NVLink, TP=8: the per-GPU weight shard is:",
    "options": [
      "140 GB",
      "70 GB",
      "17.5 GB",
      "8.75 GB"
    ],
    "answer": 3,
    "explain": "70B params × 1 byte (FP8) = 70 GB of weights; split across TP=8 gives 70 / 8 = 8.75 GB per shard."
  },
  {
    "stem": "A new vLLM version arrives. The best rollout strategy is:",
    "options": [
      "Push to production immediately",
      "Canary 1% → 10% → 100% with metrics gates",
      "Swap the model at the same time to save a deploy",
      "Skip evaluation and monitor later"
    ],
    "answer": 1,
    "explain": "Canary catches regressions on a small slice before full exposure. Never combine an engine upgrade with a model change — you couldn't tell which one caused a regression."
  },
  {
    "stem": "Cold start for a fresh 70B-FP16 replica is typically:",
    "options": [
      "100 ms",
      "1–2 sec",
      "1–5 min",
      "Several hours"
    ],
    "answer": 2,
    "explain": "The replica must pull a 10s-of-GB image, load ~140 GB of weights into HBM, and warm/JIT kernels — minutes for a big model. This is why you keep a warm pool."
  },
  {
    "stem": "Mixtral 8x7B is described as 'top-2 of 8 experts.' Per token, active params are approximately:",
    "options": [
      "7B",
      "13B",
      "47B",
      "56B"
    ],
    "answer": 1,
    "explain": "Only 2 of 8 expert MLPs fire per token; two ~7B experts plus the shared attention/embedding layers total ~13B active params (though all ~47B must sit in memory)."
  },
  {
    "stem": "FlashAttention + PagedAttention together are most important for which workload?",
    "options": [
      "Short-context, single-stream",
      "Model training",
      "Embedding generation",
      "Long-context, high-concurrency serving"
    ],
    "answer": 3,
    "explain": "FlashAttention cuts per-step HBM traffic (matters most at long context); PagedAttention removes KV fragmentation (matters most under high concurrency). Both shine at long context with many concurrent users."
  },
  {
    "stem": "A deployment reports ITL (inter-token latency) = 20 ms. Its decode TPS is:",
    "options": [
      "20 tokens/sec",
      "50 tokens/sec",
      "500 tokens/sec",
      "0.05 tokens/sec"
    ],
    "answer": 1,
    "explain": "TPS = 1000 / ITL_ms = 1000 / 20 = 50 tokens/sec. TPS and ITL are inverses describing decode speed."
  },
  {
    "stem": "For an overnight batch document-summarization job, the top-priority metric is:",
    "options": [
      "P99 TTFT with a very tight target",
      "Aggregate TPS and cost per 1M tokens",
      "P99 end-to-end latency per turn",
      "P50 TTFT"
    ],
    "answer": 1,
    "explain": "No user waits on individual responses, so the goal is to process the most tokens for the least money. The lesson lists batch summarization as 'Aggregate TPS, cost / 1M tokens.'"
  },
  {
    "stem": "In the autoscaler signal table, which signal is a direct demand signal but spiky?",
    "options": [
      "GPU utilization",
      "Request queue depth",
      "Concurrent requests",
      "P95 TTFT"
    ],
    "answer": 1,
    "explain": "Queue depth directly reflects unmet demand but is spiky. GPU utilization lags 30–60s, concurrent requests is stable but blind to the queue, and P95 TTFT is user-facing but slowest to react — so production combines two signals."
  },
  {
    "stem": "Why is round-robin a poor load-balancing strategy for LLM serving?",
    "options": [
      "Requests cost very different amounts (200-token vs 8K-token outputs), so even distribution still overloads some replicas",
      "It can only address two replicas",
      "It requires session affinity to function",
      "It always routes to the coldest replica"
    ],
    "answer": 0,
    "explain": "A replica handed several 8K-token generations is far busier than one handed 200-token replies. Round-robin ignores this; Least Outstanding Requests or Least KV-Cache Used route by actual load."
  },
  {
    "stem": "You are swapping Llama-3-70B FP16 for an FP8 quantization (a quality-sensitive change). The lesson's recommended rollout strategy is:",
    "options": [
      "Immediate 100% rollout",
      "Feature flag per tenant",
      "Shadow — run in parallel, don't serve the output",
      "Round-robin across old and new"
    ],
    "answer": 2,
    "explain": "A quality regression may not trip latency alerts, so the rollout table pairs quality-sensitive changes (new model, quantization) with Shadow: run the new version in parallel and compare outputs without serving them to users."
  },
  {
    "stem": "Which rollout strategy does the lesson recommend for a major engine/model version change that needs full rollback in seconds?",
    "options": [
      "Canary 1% → 10% → 100%",
      "Blue-green",
      "Feature flag per tenant",
      "Shadow"
    ],
    "answer": 1,
    "explain": "Blue-green keeps the old ('blue') stack fully live beside the new ('green') one, so a bad version rolls back in seconds by flipping traffic. Canary fits most weight/config changes; feature flags fit adapter/prompt changes; shadow fits quality-sensitive changes."
  },
  {
    "stem": "Perplexity is defined as:",
    "options": [
      "The number of parameters in the model",
      "A user-satisfaction survey score",
      "The exponential of cross-entropy loss on a held-out text set",
      "Inference latency in milliseconds"
    ],
    "answer": 2,
    "explain": "Perplexity = exp(cross-entropy) on held-out text; lower means the model assigns higher probability to the correct next tokens. It is a sanity check that catches catastrophic damage, not a production quality measure."
  },
  {
    "stem": "In the quantization-quality contract, you reject a precision change if the held-out perplexity delta exceeds:",
    "options": [
      "Δ > 1%",
      "Δ > 10%",
      "Δ > 25%",
      "Any increase at all"
    ],
    "answer": 0,
    "explain": "The contract's first gate is 'perplexity delta on a held-out set — reject if Δ > 1%.' It is the cheap first filter before the more expensive task and human evals (which reject on >2 pp regression and <45% win rate)."
  },
  {
    "stem": "Using the worked example (8×H100 at ~$30/hr producing 10.8M tokens/hour at 100% util), the cost per 1M tokens at a realistic 50% utilization is about:",
    "options": [
      "$2.78",
      "$5.56",
      "$6.94",
      "$9.26"
    ],
    "answer": 1,
    "explain": "Cost / 1M = $30 / (10.8M × 0.50) = $30 / 5.4M = $5.56. For reference: $2.78 at 100%, $6.94 at 40%, and $9.26 at 30%."
  },
  {
    "stem": "In the cost-lever table, which change offers the largest typical cost reduction?",
    "options": [
      "Switching FP16 → FP8 weights + KV (1.5–2×)",
      "Enabling speculative decoding (1.5–2.5×)",
      "Caching system-prompt prefixes (1.2–3× on prefill)",
      "Continuous batching instead of static batching (5–10×)"
    ],
    "answer": 3,
    "explain": "Continuous batching (5–10×) is the largest single lever, tied with 'smaller model + better prompting.' FP8 gives 1.5–2×, speculative decoding 1.5–2.5×, and prefix caching 1.2–3× on prefill only."
  },
  {
    "stem": "The 'SLO tripod' that frames every Phase 1 serving decision consists of:",
    "options": [
      "Latency, quality, and cost",
      "Hardware, software, and networking",
      "Training, fine-tuning, and serving",
      "Prefill, decode, and tokenization"
    ],
    "answer": 0,
    "explain": "Week 5 builds the three-axis framework: latency (Day 21 metrics), quality (Day 23 evals), and cost (Day 24 economics). A production deployment must satisfy all three at once — optimizing one at the expense of another creates problems."
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
