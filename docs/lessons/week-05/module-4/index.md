# Day 24 · Cost & Economics

> **Concept of the day:** **cost / million tokens** = (GPU $/hour × hours) / (tokens served × utilization). **Decode dominates** end-to-end cost for chat workloads. **Dedicated breaks even with API** somewhere around 30–50% utilization.
> **Pre-reading:** "Cost of inference" with worked numbers — <a href="https://a16z.com/the-economics-of-ai-inference/" target="_blank" rel="noopener">a16z — The Economics of AI Inference</a> (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 24 · Cost & Economics</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-05/module-4}
  </div>
  <div class="ox-lesson-header__cta">
    <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
    <a class="md-button md-button--primary" href="knowledge-check.html">Knowledge check</a>
    <a class="md-button" href="assignment.md">Assignment</a>
    <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| # | What you do | Time |
|---|-------------|------|
| 1 | The Cost Formula | 15 min |
| 2 | Worked Example | 20 min |
| 3 | Calculate Your Cost | 25 min |
| 4 | Break-Even Analysis | 25 min |
| 5 | Cost Levers | 20 min |
| 6 | Build Your Cost Model | 25 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — The Cost Formula · 15 min

### Before You Start

You should have already read: <a href="https://a16z.com/the-economics-of-ai-inference/" target="_blank" rel="noopener">a16z — The Economics of AI Inference</a> (~15 min).

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m4-readiness" data-kind="readiness" data-draw="5" data-source="a16z — The Economics of AI Inference">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the approximate break-even point where dedicated deployment becomes cheaper than using an API?",
    "options": [
      "5-10% utilization",
      "30-50% utilization",
      "80-90% utilization",
      "It is never cheaper than API"
    ],
    "answer": 1,
    "explain": "Dedicated deployment (running your own GPUs) breaks even with API pricing somewhere around 30-50% utilization. Below that, the fixed cost of owning GPUs isn't worth it; above that, you save by running your own infrastructure."
  },
  {
    "stem": "In LLM inference, which phase typically dominates end-to-end cost for chat workloads?",
    "options": [
      "Prefill phase",
      "Decode phase",
      "Tokenization",
      "They are equal"
    ],
    "answer": 1,
    "explain": "For chat workloads with short prompts and long outputs, the decode phase dominates end-to-end cost. This is because the decode phase processes one token at a time sequentially, while prefill processes the entire prompt in parallel."
  },
  {
    "stem": "What is the formula for cost per million tokens in dedicated deployment?",
    "options": [
      "GPU $ / hour / tokens served",
      "(GPU $/hour × hours) / (tokens served × utilization)",
      "Tokens served / GPU $",
      "GPU hours × utilization / tokens"
    ],
    "answer": 1,
    "explain": "Cost per million tokens = (GPU $/hour × hours) / (tokens served × utilization). This accounts for GPU hourly cost, time running, total tokens processed, and the utilization fraction."
  },
  {
    "stem": "Why does higher GPU utilization decrease cost per token?",
    "options": [
      "It doesn't — higher utilization increases cost",
      "Fixed GPU costs are spread across more tokens when utilization is higher",
      "Higher utilization requires cheaper GPUs",
      "Utilization has no effect on cost"
    ],
    "answer": 1,
    "explain": "Higher utilization spreads the fixed GPU hourly cost across more tokens. If a GPU costs $3/hour and you process 1M tokens at 50% utilization vs 10% utilization, your cost per token is 5x lower at higher utilization."
  },
  {
    "stem": "What is a key insight about batch processing economics in LLM inference?",
    "options": [
      "Batching always reduces cost",
      "Large batches improve throughput but may increase latency, creating a tradeoff",
      "Batching has no impact on economics",
      "Small batches are always more economical"
    ],
    "answer": 1,
    "explain": "Large batches improve throughput (more tokens/second) which spreads fixed GPU costs across more requests, but they increase latency for individual requests. There's an optimal batch size that balances cost efficiency with latency requirements."
  },
  {
    "stem": "Why might a startup choose API over dedicated deployment even if it could afford GPUs?",
    "options": [
      "APIs are always cheaper",
      "APIs provide flexibility, no ops overhead, and can scale to zero cost during low traffic",
      "Dedicated deployment is illegal for startups",
      "APIs provide better quality"
    ],
    "answer": 1,
    "explain": "Even if a company can afford GPUs, APIs provide: (1) no ops overhead — no need to manage infrastructure, (2) flexibility — switch models instantly, (3) scale to zero — no idle GPU costs during low traffic. The break-even analysis isn't just about raw cost."
  },
  {
    "stem": "What is the relationship between input tokens and output tokens in terms of compute cost?",
    "options": [
      "Input and output tokens cost the same",
      "Output tokens (decode) cost more per token than input tokens (prefill)",
      "Input tokens cost more per token than output tokens",
      "There is no relationship"
    ],
    "answer": 1,
    "explain": "For most workloads, output tokens (decode phase) cost more per token than input tokens. The decode phase processes tokens one-at-a-time sequentially (memory-bandwidth bound), while prefill processes the entire prompt in parallel (compute-bound)."
  },
  {
    "stem": "What does 'utilization' mean in the context of GPU cost modeling?",
    "options": [
      "The percentage of time the GPU is powered on",
      "The fraction of time the GPU is actively processing requests vs sitting idle",
      "The percentage of GPU memory used",
      "The number of concurrent requests"
    ],
    "answer": 1,
    "explain": "Utilization is the fraction of time the GPU is actively processing requests. If a GPU runs for 1 hour but is only processing requests for 30 minutes, utilization is 50%. Low utilization wastes money because you're paying for idle GPU time."
  }
]
</script>
</div>

### Reading

This is the *third leg* of the SLO tripod: latency, quality, **cost**. Every choice in Phase 1 has a cost implication. By the end of today you should be able to give a number for "what does our deployment cost per million output tokens?" — and defend it.

### The Cost Formula

> **Cost per 1M output tokens = (GPU $/hour × hours of usage) / (1M output tokens served at that utilization)**

Equivalently:

> **Cost / 1M tokens = $ per GPU-hour / (utilization × tokens-per-GPU-hour)**

**Three levers:**
1. **$ per GPU-hour** — hardware choice, contract length, region
2. **Tokens-per-GPU-hour at full util** — engine + model + parallelism (Weeks 3–4)
3. **Utilization** — what fraction of paid GPU time you're actually serving tokens

### Why Decode Dominates

A typical chat request: 500 input tokens, 1500 output tokens. Prefill is one parallel pass (fast); decode is 1500 sequential passes (slow). For most workloads, **70–90% of GPU-time is spent in decode** — so per-token cost is essentially per-output-token cost.

---

## Part 2 — Worked Example · 20 min

### Reading — Llama-3-70B FP16 on 8×H100

Assumptions (rough, 2024–25):

- **8×H100 on-demand:** ~$30/hour (varies: $20 spot to $50 reserved)
- **Peak decode throughput** at TP=8, large batch: ~3000 tokens/sec aggregate
- **Hours per month:** 730

### At 100% Utilization (impossible, but the ceiling)

- Tokens / hour = 3000 × 3600 = 10.8M
- Cost / 1M tokens = $30 / 10.8 = **$2.78**

### At Realistic 40% Utilization

- Cost / 1M tokens = $30 / (10.8 × 0.4) = **$6.94**

### API Pricing Comparison

API pricing (Llama-3-70B class via fireworks/together/etc.): **~$0.60–$1.00 / 1M output tokens** mid-2024.

> **Conclusion:** For low utilization, API is much cheaper. Dedicated breaks even around **35–60% sustained utilization** for general-purpose inference.

---

## Part 3 — Calculate Your Cost · 25 min

### Exercise: Re-Derive Cost at Different Utilizations

Using the formula and the numbers above, calculate **cost / 1M tokens** at:

1. **30% utilization:** ___
2. **50% utilization:** ___
3. **70% utilization:** ___

**Show your work:**
```
Cost / 1M = $30 / (10.8M × utilization)
```

### Exercise: Fill in the Table

| Utilization | Tokens/hour | Cost/1M tokens |
|-------------|-------------|----------------|
| 30% | 10.8M × 0.3 = 3.24M | $30 / 3.24M = $9.26 |
| 50% | 10.8M × 0.5 = 5.4M | ___ |
| 70% | 10.8M × 0.7 = 7.56M | ___ |

---

## Part 4 — Break-Even Analysis · 25 min

### Exercise: When Does Dedicated Win?

**Scenario:**
- Your deployment: 8×H100 at $30/hour
- Monthly cost: $30 × 730 = **$21,900/month**
- API price: **$0.80 / 1M output tokens**

**Question:** At what monthly token volume does dedicated break even with the API at 40% utilization?

**Calculate:**
1. At 40% util, cost/1M = $6.94
2. To spend $21,900/month on API: $21,900 / $0.80 = ___ tokens/month
3. At 40% util on dedicated: $21,900 / $6.94 = ___ tokens/month

**The break-even point is when both cost the same.**

### When Dedicated Wins

| Condition | Verdict |
|-----------|---------|
| Sustained > 50% utilization, 24/7 | Dedicated wins, possibly big |
| Bursty, < 20% utilization | API wins |
| Need a custom fine-tune | Dedicated (or API w/ adapter support) |
| Data residency / privacy | Dedicated (or VPC-deployed API) |
| Want speed-of-experimentation | API |

---

## Part 5 — Cost Levers · 20 min

### Reading — The Levers in Order of Impact

| Lever | Typical Cost Reduction | Risk |
|-------|------------------------|------|
| Switch to FP8 weights + KV | 1.5–2× | Quality regression (Day 23) |
| Enable speculative decoding | 1.5–2.5× | Implementation complexity |
| Continuous batching, no static | 5–10× | Already standard in vLLM |
| Spot / reserved GPU pricing | 2–4× | Availability / lock-in |
| Smaller model + better prompting | 5–10× | Quality regression — measure |
| Caching prefixes (system prompt) | 1.2–3× on prefill cost | None (free win) |

### Discussion: Pick One Lever

If you could implement **one** change to cut your Week 4 deployment cost in half, which would it be?

**Justify with one number** — show the expected reduction.

---

## Part 6 — Build Your Cost Model · 25 min

### Exercise: One-Page Cost Model

Create a one-page cost model for your Week 4 serving system. Include:

1. **$/hour:** Hardware cost
2. **Peak TPS:** From your Week 3 + Week 4 calculations
3. **Cost / 1M tokens** at 30%, 50%, 70% utilization
4. **Break-even point** vs an API priced at $0.80 / 1M tokens
5. **One lever** you'd pull first to cut cost, with expected reduction

### Token Economics for Product Pricing

If you're building a product on top:

1. **Long-context products** — KV cache blows up cost per request 10× at 128K. Charge for context.
2. **Multi-turn agentic** — Week 7's agents make 10–50 LLM calls per "task." Cost / task ≠ cost / call.

### Reflection Question

Write one sentence summarizing what you learned about cost:
> The three levers are: ___, ___, ___. The most impactful is ___.

---

## Part 7 — Wrap-up & Connection · 10 min

### Synthesis

Cost is the third SLO axis. With perplexity + task evals from yesterday and cost numbers from today, you now have the full measurement framework for Phase 1. Tomorrow is the Phase 1 wrap — bring your cost model, Week 3 calculator, and Week 4 design doc.

### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 24 · Cost &amp; Economics">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Why do decode tokens typically cost more per token than prefill tokens?",
    "options": [
      "Decode uses higher-precision arithmetic than prefill",
      "Decode is serial and memory-bound — each decode step occupies the full GPU for one token; prefill processes many tokens in parallel per GPU-second",
      "Decode tokens are longer than prefill tokens",
      "Decode requires separate hardware that costs more to operate"
    ],
    "answer": 1,
    "explain": "Prefill is parallel: 1000 input tokens take roughly the same GPU time as one decode step. Decode is serial: each output token requires a full forward pass. So output tokens are roughly N× more expensive per token than input tokens when input length is N. Token-priced APIs reflect this asymmetry."
  },
  {
    "stem": "At what approximate GPU utilization does owning/leasing a dedicated GPU break even vs paying a token-priced API?",
    "options": [
      "Around 10–20%",
      "Around 30–50%",
      "Around 60–80%",
      "Only at 100% utilization"
    ],
    "answer": 2,
    "explain": "A dedicated GPU costs ~$X/hour regardless of load. A token-priced API charges per token. The break-even is when GPU cost / (utilization × tokens_per_hour) equals the API price per token. Typically this occurs around 60–80% sustained utilization — below that, APIs are cheaper; above that, dedicated is cheaper."
  },
  {
    "stem": "What are the three primary levers for reducing inference cost?",
    "options": [
      "Reducing input prompt length, using a smaller vocabulary, and switching hardware vendors",
      "Quantization (fewer bytes per weight), batching (amortize weight reads across requests), and improved GPU utilization (generate more tokens per GPU-dollar)",
      "Model pruning, knowledge distillation, and early exit",
      "Caching responses, deduplicating requests, and rate limiting users"
    ],
    "answer": 1,
    "explain": "The a16z Economics of AI Inference piece and the lesson identify three main cost levers: (1) quantization reduces memory footprint and bandwidth use; (2) batching amortizes fixed costs across more requests; (3) utilization — idle GPU time is wasted money. All three compound: quantize → fit larger batches → improve utilization."
  },
  {
    "stem": "What is the cost per request formula?",
    "options": [
      "cost = (GPU_price_per_token × output_tokens) + (network_cost × request_size)",
      "cost = (lease_$/hr ÷ 3600) × seconds_per_request",
      "cost = model_size_GB × bandwidth_GB_per_s × latency_seconds",
      "cost = TTFT × TPS × batch_size"
    ],
    "answer": 1,
    "explain": "The lesson formula: cost_per_request = (lease_$/hr ÷ 3600) × seconds_per_request. Where seconds_per_request = TTFT + (avg_output_tokens / throughput_per_request). This converts hourly GPU cost to per-request cost by factoring in how long each request holds GPU time."
  },
  {
    "stem": "How does quantization reduce cost per million tokens?",
    "options": [
      "Quantization reduces the number of tokens generated per request",
      "Quantization reduces weight bytes → increases arithmetic intensity → enables larger batch sizes → more tokens per GPU-second → lower cost per token",
      "Quantization reduces the GPU hourly rate",
      "Quantization is only a quality tradeoff and has no direct cost impact"
    ],
    "answer": 1,
    "explain": "The chain: fewer bytes per weight (e.g., FP16→INT4: 4× reduction) → each weight read loads more 'computations worth' of information → arithmetic intensity rises → decode becomes less memory-bound → GPU can handle larger batches → more tokens per GPU-hour → lower cost per million tokens."
  },
  {
    "stem": "What does the lesson's 'SLO tripod' consist of?",
    "options": [
      "Hardware, software, and networking",
      "Latency (TTFT/TPS), quality (task evals), and cost — all three must be balanced together",
      "Training, fine-tuning, and serving",
      "Model selection, hardware selection, and deployment automation"
    ],
    "answer": 1,
    "explain": "The 'SLO tripod' is the three-axis measurement framework built over Weeks 5 Days 21–24: latency (Day 21 metrics), quality (Day 23 evals), and cost (Day 24 economics). A production LLM deployment must satisfy all three axes simultaneously — optimizing one at the expense of another creates problems."
  }
]
</script>
</div>

### Pre-read for Friday (Day 25 · Phase 1 Wrap)

- **Resource:** Skim the Inference Engineering Glossary one more time. Bring your Week 3 calculator, Week 4 design doc, and today's cost model.
- **Reflection questions:**
  1. Of everything in Phase 1, what's the *one* concept you'd teach a new joiner first?
  2. What concept are you *least* sure of?
  3. For the cost model above — what's the single change you'd push for to cut cost in half? Justify with one number.

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
