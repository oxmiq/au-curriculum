<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 5 - Metrics &amp; Production</a>
    <span class="sep">/</span>
    <a href="../">Day 25 · Consolidation + Phase 1 Problem Set</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-05/module-5}
  </div>
</div>

# Week 5 Knowledge Check

**Phase 1 Assessment · Week 5.** 26-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative, it never blocks you, but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Phase 1 Assessment · Week 5" data-source="Canonical knowledge check">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "A chat product reports P50 TTFT = 80 ms, P99 TTFT = 4200 ms. The most likely cause is:", "options": ["Slow GPU", "Cold start", "Queueing or batching tail under load", "Bad prompt"]},
  {"stem": "You compress a 70B model FP16 → FP8. Decode throughput should:", "options": ["Roughly double", "Stay the same", "Halve", "Drop 10×"]},
  {"stem": "For a request with 100 input / 5000 output tokens, what dominates wall-clock time?", "options": ["Prefill", "Tokenization", "Network", "Decode"]},
  {"stem": "TP=8 on 8×H100 instead of TP=4 on 4×H100 (same model that fits both): the primary benefit is:", "options": ["Lower decode latency (less per-GPU weight to read)", "Higher quality", "Lower cost", "Smaller model"]},
  {"stem": "Continuous batching gives ~5–10× throughput over static batching because:", "options": ["Better GPU drivers", "Tensor Cores get faster", "Requests admit at every decode step, no waiting at batch boundaries; the GPU stays full", "The model is smaller"]},
  {"stem": "Speculative decoding produces output that is:", "options": ["Slightly different", "Always worse", "Faster but lower quality", "Provably identical to sampling from the target model"]},
  {"stem": "Which is the MOST honest single quality metric for shipping a quantization change?", "options": ["Perplexity", "MMLU", "Your own task-eval pass rate + side-by-side win rate", "Training loss"]},
  {"stem": "Goodhart's Law applied to LLM serving means:", "options": ["Once you bonus a single metric, behaviour optimizes for that metric at the cost of others; report a vector with percentiles", "Measure more of everything", "Trust averages over percentiles", "Report only P50"]},
  {"stem": "PagedAttention's contribution is best described as:", "options": ["Better attention math", "Quantization of the KV cache", "OS-style virtual paging for the KV cache, eliminating fragmentation", "Speculative decoding"]},
  {"stem": "Choose the right deployment for a bursty internal tool at ~5% GPU utilization with no privacy constraints:", "options": ["Hosted API, priced per token", "Dedicated 8×H100", "Pipeline parallelism across nodes", "Build your own GPU cluster"]},
  {"stem": "Llama-3-70B FP8 weights on 8×H100 with NVLink, TP=8: the per-GPU weight shard is:", "options": ["140 GB", "70 GB", "17.5 GB", "8.75 GB"]},
  {"stem": "A new vLLM version arrives. The best rollout strategy is:", "options": ["Push to production immediately", "Canary 1% → 10% → 100% with metrics gates", "Swap the model at the same time to save a deploy", "Skip evaluation and monitor later"]},
  {"stem": "Cold start for a fresh 70B-FP16 replica is typically:", "options": ["100 ms", "1–2 sec", "1–5 min", "Several hours"]},
  {"stem": "Mixtral 8x7B is described as 'top-2 of 8 experts.' Per token, active params are approximately:", "options": ["7B", "13B", "47B", "56B"]},
  {"stem": "FlashAttention + PagedAttention together are most important for which workload?", "options": ["Short-context, single-stream", "Model training", "Embedding generation", "Long-context, high-concurrency serving"]},
  {"stem": "A deployment reports ITL (inter-token latency) = 20 ms. Its decode TPS is:", "options": ["20 tokens/sec", "50 tokens/sec", "500 tokens/sec", "0.05 tokens/sec"]},
  {"stem": "For an overnight batch document-summarization job, the top-priority metric is:", "options": ["P99 TTFT with a very tight target", "Aggregate TPS and cost per 1M tokens", "P99 end-to-end latency per turn", "P50 TTFT"]},
  {"stem": "In the autoscaler signal table, which signal is a direct demand signal but spiky?", "options": ["GPU utilization", "Request queue depth", "Concurrent requests", "P95 TTFT"]},
  {"stem": "Why is round-robin a poor load-balancing strategy for LLM serving?", "options": ["Requests cost very different amounts (200-token vs 8K-token outputs), so even distribution still overloads some replicas", "It can only address two replicas", "It requires session affinity to function", "It always routes to the coldest replica"]},
  {"stem": "You are swapping Llama-3-70B FP16 for an FP8 quantization (a quality-sensitive change). The lesson's recommended rollout strategy is:", "options": ["Immediate 100% rollout", "Feature flag per tenant", "Shadow - run in parallel, don't serve the output", "Round-robin across old and new"]},
  {"stem": "Which rollout strategy does the lesson recommend for a major engine/model version change that needs full rollback in seconds?", "options": ["Canary 1% → 10% → 100%", "Blue-green", "Feature flag per tenant", "Shadow"]},
  {"stem": "Perplexity is defined as:", "options": ["The number of parameters in the model", "A user-satisfaction survey score", "The exponential of cross-entropy loss on a held-out text set", "Inference latency in milliseconds"]},
  {"stem": "In the quantization-quality contract, you reject a precision change if the held-out perplexity delta exceeds:", "options": ["Δ > 1%", "Δ > 10%", "Δ > 25%", "Any increase at all"]},
  {"stem": "Using the worked example (8×H100 at ~$30/hr producing 10.8M tokens/hour at 100% util), the cost per 1M tokens at a realistic 50% utilization is about:", "options": ["$2.78", "$5.56", "$6.94", "$9.26"]},
  {"stem": "In the cost-lever table, which change offers the largest typical cost reduction?", "options": ["Switching FP16 → FP8 weights + KV (1.5–2×)", "Enabling speculative decoding (1.5–2.5×)", "Caching system-prompt prefixes (1.2–3× on prefill)", "Continuous batching instead of static batching (5–10×)"]},
  {"stem": "The 'SLO tripod' that frames every Phase 1 serving decision consists of:", "options": ["Latency, quality, and cost", "Hardware, software, and networking", "Training, fine-tuning, and serving", "Prefill, decode, and tokenization"]}
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Back to today's lesson__

    [Day 25 · Consolidation + Phase 1 Problem Set](index.md)

-   __Back to the week__

    [Week 5 - Metrics &amp; Production overview](../index.md)

-   __Continue the curriculum__

    [Day 26 · Prompt Engineering](../../week-06/module-1/index.md)

</div>
