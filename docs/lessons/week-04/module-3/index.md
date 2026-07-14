# Day 18 · Speculative Decoding

> **Concept of the day:** a small **draft** model proposes K tokens; the big **target** model verifies them in **one** parallel forward pass. Convert sequential memory-bound decode into batched-style verification. 2–3× speedup typical.<br>
> **Pre-reading:** "Speculative decoding explained" - <a href="https://huggingface.co/blog/assisted-generation" target="_blank" rel="noopener">Hugging Face - Assisted Generation (Speculative Decoding)</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 4 - Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <span>Day 18 · Speculative Decoding</span>
    {status:week-04/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review + Readiness Check |
| Part 2 | Core Concept: The Wasted-Compute Problem |
| Part 3 | Core Concept: The Speculative Trick |
| Part 4 | Deep Dive: Why It's Faster + Bit-Exactness |
| Part 5 | Hands-On: Calculations + Tradeoffs |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review + Readiness Check
### Before You Start

You should have already read: "Speculative decoding explained" - Pre-Lecture Reading **Reader 6**.

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m3-readiness" data-kind="readiness" data-draw="5" data-source="Hugging Face - Assisted Generation + NVIDIA - Speculative Decoding">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Why is single-stream decode so wasteful of Tensor Core throughput?",
    "options": [
      "It generates too many tokens",
      "The GPU sits idle most of the time waiting for the next token (memory-bound), while Tensor Cores could do more work",
      "It uses too much memory",
      "The model is too small"
    ],
    "answer": 1,
    "explain": "Single-token decode is memory-bound: the GPU waits on HBM for KV cache reads between each token. Tensor Cores sit idle. There's plenty of compute capacity that could be used if there were more work to do."
  },
  {
    "stem": "What is the role of the draft model in speculative decoding?",
    "options": [
      "To generate high-quality output",
      "To quickly propose K tokens that the larger model will verify",
      "To cache KV values",
      "To manage memory allocation"
    ],
    "answer": 1,
    "explain": "The draft model (small, fast) proposes K tokens in rapid succession. These drafts are then verified in one batch by the target model. The draft doesn't need to be perfect; it just needs to be good enough to speed things up."
  },
  {
    "stem": "Why must the draft model be much smaller than the target model?",
    "options": [
      "It doesn't need to be smaller",
      "So it can decode faster (more tokens per second), keeping the target model fed with work",
      "To save memory",
      "To reduce power consumption"
    ],
    "answer": 1,
    "explain": "The draft must be small enough to decode much faster than the target. Its job is to keep the target model fed with work: generating drafts faster than the target can verify them. A 1B draft vs 70B target gives the needed speed gap."
  },
  {
    "stem": "What happens in the target model's verification pass?",
    "options": [
      "The target model generates new tokens from scratch",
      "The target model verifies the draft tokens in parallel, accepting correct ones and sampling new ones for rejected positions",
      "The target model caches the KV values",
      "The target model does nothing"
    ],
    "answer": 1,
    "explain": "The target model takes all K draft tokens and verifies them in ONE parallel forward pass. It accepts tokens that match its own distribution, and for rejected positions, it resamples to get the 'correct' token."
  },
  {
    "stem": "If the draft model is wrong on token 3 of 5, what happens to tokens 1-2?",
    "options": [
      "All 5 tokens are rejected",
      "Tokens 1-2 are still kept (accepted); only token 3 and subsequent are reconsidered",
      "Tokens 1-2 are also rejected",
      "The draft model is not used"
    ],
    "answer": 1,
    "explain": "If draft token 3 is wrong, tokens 1-2 are still accepted and kept. Only from the rejection point onward does the target model take over. This is why speculative decoding is 'tree-based': branches are pruned at first rejection."
  },
  {
    "stem": "What is the typical speedup from speculative decoding, and what can kill it?",
    "options": [
      "2-3x speedup; killed by the draft model being too similar to the target",
      "2-3x speedup; killed if the draft model is too slow or acceptance rate is low",
      "10x speedup; killed by memory limitations",
      "No speedup; it's only for accuracy"
    ],
    "answer": 1,
    "explain": "Typical speedup is 2-3x. It's killed if: draft model is too slow (can't keep target fed), or if acceptance rate is low (draft keeps being wrong). The key metric is acceptance ratio: higher is better."
  },
  {
    "stem": "Why is speculative decoding 'bit-exact' with autoregressive decoding?",
    "options": [
      "It uses the same random numbers",
      "The target model's verification ensures the final output is identical to what autoregressive decoding would have produced",
      "It doesn't guarantee exactness",
      "Because it uses the same model"
    ],
    "answer": 1,
    "explain": "Speculative decoding is bit-exact: the target model's verification guarantees the final output is identical to what standard autoregressive decoding would produce. If draft is wrong, the target resamples: same result."
  },
  {
    "stem": "What is the key insight that makes speculative decoding work?",
    "options": [
      "Using two models",
      "Converting sequential memory-bound decode into batched verification: the target model checks multiple tokens at once",
      "Reducing memory usage",
      "Using quantization"
    ],
    "answer": 1,
    "explain": "The key insight: convert sequential decode (one token at a time, memory-bound) into batched verification (K tokens in one pass). This uses the target model's compute efficiently while the draft keeps it fed."
  }
]
</script>
</div>

---

## Part 2 - Core Concept - The Wasted-Compute Problem
### Reading - Why This Matters

The most impactful "free" decode speedup of the last two years. Used in vLLM, TGI, TensorRT-LLM. **Bit-exact** with greedy decoding under speculative sampling; so quality is unchanged.

### The Wasted-Compute Observation

Decode reads all 16 GB of weights from HBM to produce **one token**, doing ~32 GFLOPs of work. The H100 can do **989 TFLOPs FP16**; so the Tensor Cores are **~99.99% idle** during the 4.8 ms read.

Idea: while the GPU reads weights anyway, can it produce **more than one token of useful work**?

### Key Terms to Understand

| Term | Definition |
|------|------------|
| **Speculative decoding** | Technique where a smaller draft model proposes tokens, verified in parallel by the target model |
| **Draft model** | Smaller, faster model that proposes candidate tokens |
| **Target model** | The actual large model that verifies draft tokens |
| **Verification pass** | Target model checks all draft tokens in one forward pass |

---

## Part 3 - Core Concept - The Speculative Trick
### Reading - How Speculative Decoding Works

1. A tiny **draft model** (e.g. 1B params, 30× smaller and faster) proposes the next **K tokens** sequentially. Cheap because it's tiny.
2. The **target model** (the real 70B) does **one forward pass over all K tokens at once**: like a mini-prefill.
3. For each draft token, target computes the probability it would have produced that token. Accept the longest prefix that matches.

### Example Walkthrough

- Draft proposes: "The cat sat on the"
- Target verifies all 5 tokens in ONE forward pass
- If target accepts "The cat sat", tokens 1-3 are kept, tokens 4-5 are rejected
- Next iteration: target continues from "on the"

### Why Draft Must Be Smaller

- Draft needs to be 10-30× faster than target
- If draft is too big, it becomes memory-bound too
- No benefit if draft compute ≈ target compute

---

## Part 4 - Deep Dive - Why It's Faster + Bit-Exactness
### Reading - The Speedup Math

The target's single forward pass over K tokens has roughly the **same memory cost** as one decode step (it reads all weights once). But it produces up to K accepted tokens.

| K | If all accepted | If 60% acceptance |
|---|---|---|
| 1 (no spec) | 1 token / step | 1 token / step |
| 4 | 4 / step (4×) | ~2.4 / step (2.4×) |
| 8 | 8 / step (8×) | ~4 / step (4×) |

In practice: **2–3× end-to-end decode speedup** is the production norm for code-like or predictable text; less for surprising outputs.

### Bit-Exactness

Under **speculative sampling** (the rejection-sampling variant), the output distribution is **provably identical** to the target model decoding alone. No quality drop: it's a pure systems win.

### What Kills Speculative Decoding

- **Draft quality too low** → low acceptance rate, draft compute wasted
- **Draft too big** → draft itself becomes memory-bound, no compute savings
- **High-temperature / creative text** → less predictable, lower acceptance
- **Memory contention** - draft + target competing for HBM bandwidth

### Production Choices

- vLLM: optional draft model (`--speculative-model`)
- **EAGLE** / **Medusa**: instead of a separate draft model, train extra prediction heads on the target: even cheaper

---

## Part 5 - Hands-On - Calculations + Tradeoffs
### Exercise 1: Verification Walkthrough

On paper, walk through one verification step:
- Draft proposes: "the cat sat on"
- Target verifies, what's the output?

**Answer:** If target accepts "the cat sat", tokens 1-3 are kept, token 4 is rejected. Next iteration starts from "on".

### Exercise 2: Speedup Math

If draft is 30× faster and acceptance rate is 0.7 at K=4:
- What's expected speedup over plain decode?

**General formula:** Speedup = draft_speed × (acceptance_rate × K + (1 - acceptance_rate))

**Calculate:**
- Draft speedup: 30×
- Accepted tokens: 0.7 × 4 = 2.8
- Rejected (redecode): 0.3 × 1 = 0.3
- Net: 2.8 + 0.3 = 3.1 tokens per step
- Speedup: 3.1× (vs 1× baseline) = ~3× overall

---

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 18 · Speculative Decoding">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the role of the draft model in speculative decoding?",
    "options": [
      "It generates the final output tokens that are shown to the user",
      "It proposes K candidate tokens quickly; the target model then verifies them in a single forward pass",
      "It compresses the KV cache to save memory during decode",
      "It handles low-complexity requests while the target model handles complex ones"
    ],
    "answer": 1,
    "explain": "The small, fast draft model speculatively generates K tokens. These K proposed tokens are then verified by the large target model in a single parallel forward pass: the same cost as generating one token. If accepted, you get K tokens for the price of one verification pass."
  },
  {
    "stem": "How does the target model verify the draft model's proposals?",
    "options": [
      "It re-runs the draft model on each proposal and compares outputs",
      "It runs a single parallel forward pass over all K draft tokens and applies a rejection-sampling correction, accepting each token with probability min(1, p_target / p_draft), that preserves the target model's distribution",
      "It uses a separate scorer model trained specifically for verification",
      "It sends the proposals to a human evaluator"
    ],
    "answer": 1,
    "explain": "The target model runs one forward pass over all K draft tokens simultaneously; this is the key insight. Each token is accepted with probability min(1, p_target / p_draft); on rejection the target resamples from the corrected distribution. This stochastic rejection-sampling correction preserves the target model's exact output distribution, which is why the output is bit-exact. Accepted tokens are effectively free."
  },
  {
    "stem": "Why is speculative decoding output bit-exact with standard decode?",
    "options": [
      "Because the draft model is identical to the target model",
      "Because the acceptance/rejection mechanism mathematically preserves the target model's exact output distribution",
      "Because speculative decoding uses the same random seed as standard decode",
      "Because the draft tokens are always accepted without modification"
    ],
    "answer": 1,
    "explain": "The acceptance-rejection scheme uses a rejection sampling correction that ensures the final output distribution is identical to what the target model would have produced alone. This is a mathematical guarantee, not an approximation; speculative decoding is lossless."
  },
  {
    "stem": "What primarily kills the speedup from speculative decoding?",
    "options": [
      "The draft model using more memory than the target model",
      "Low token acceptance rate: if the draft model's proposals frequently mismatch the target model's preferences, the per-step cost rises with little gain",
      "High GPU temperature causing throttling",
      "Large batch sizes that eliminate the latency benefit"
    ],
    "answer": 1,
    "explain": "Speculative decoding speedup depends on the acceptance rate α. If α is high (draft and target agree), multiple tokens per step are accepted: large speedup. If α is low (draft model mismatch), the rejection overhead reduces or eliminates the speedup. Workload predictability (code, templates) gives high α; creative text gives low α."
  },
  {
    "stem": "Why is speculative decoding particularly effective for LLM decode specifically?",
    "options": [
      "Because decode is compute-bound and speculative decoding maximizes Tensor Core utilization",
      "Because decode is memory-bound and serial: small batches leave the GPU mostly idle, so the draft model's proposals use otherwise wasted compute",
      "Because decode uses a different model architecture that benefits from speculation",
      "Because the draft model can be run on the CPU, freeing GPU bandwidth"
    ],
    "answer": 1,
    "explain": "During decode with small batches, the GPU uses ~0.7% of its Tensor Cores (memory-bound, serial). Speculative decoding converts that idle GPU capacity into useful work (running the draft model or the parallel verification pass). It is 'free latency' only because those cycles would otherwise be wasted."
  },
  {
    "stem": "What does the lesson mean when it says speculative decoding is 'free latency, if the workload is predictable'?",
    "options": [
      "Speculative decoding requires no additional hardware",
      "On predictable outputs (code, templates), high acceptance rates mean more tokens per step with no quality loss; unpredictable outputs have low acceptance rates and the speedup shrinks",
      "Speculative decoding automatically disables itself for creative tasks",
      "All tokens are always accepted for predictable workloads"
    ],
    "answer": 1,
    "explain": "The key phrase is: 'Free latency, if the workload is predictable.' For structured outputs (code, JSON, templated text), the small draft model closely predicts the large model: high acceptance rate, large speedup. For open-ended creative generation, acceptance rates are lower and speedup shrinks. Always profile your workload."
  },
  {
    "stem": "According to the lesson, how much faster than the target must the draft model be for speculative decoding to pay off?",
    "options": [
      "Only about 2x faster",
      "Roughly 10-30x faster; if the draft is too big it becomes memory-bound itself and there is no compute savings",
      "Exactly the same speed as the target",
      "Draft speed does not matter; only its accuracy does"
    ],
    "answer": 1,
    "explain": "The lesson states the draft needs to be about 10-30x faster than the target (e.g. a 1B draft vs a 70B target). If the draft is too big it becomes memory-bound like the target and there is no benefit: 'no benefit if draft compute is roughly target compute.'"
  },
  {
    "stem": "What do EAGLE and Medusa do differently from classic draft-model speculative decoding?",
    "options": [
      "They run the draft model on a separate GPU cluster to free HBM bandwidth",
      "They enlarge the draft model to push acceptance rates higher",
      "Instead of a separate draft model, they train extra prediction heads on the target model itself: even cheaper",
      "They remove the verification pass entirely and trust the draft"
    ],
    "answer": 2,
    "explain": "The lesson lists EAGLE and Medusa under production choices: rather than pairing the target with a separate draft model, they train extra prediction heads onto the target model itself, which is cheaper than maintaining a distinct draft."
  },
  {
    "stem": "What observation about the decode step motivates speculative decoding in the first place?",
    "options": [
      "The KV cache grows too large to fit in HBM during long generations",
      "Prefill is compute-bound and underutilizes memory bandwidth",
      "Attention becomes the dominant cost during decode",
      "During decode the GPU reads all the model's weights from HBM just to produce one token, leaving the Tensor Cores almost entirely idle"
    ],
    "answer": 3,
    "explain": "The wasted-compute observation: decode reads all ~16 GB of weights from HBM to produce just one token (~32 GFLOPs), while an H100 can do ~989 TFLOPs; so the Tensor Cores are ~99.99% idle during the weight read. Speculative decoding puts that otherwise-wasted compute to use by verifying K tokens at once."
  }
]
</script>
</div>

### The Key Phrase

> **"Speculative decoding = free latency, if the workload is predictable. Always try it."**

### Connect Forward

Tomorrow: putting it all together: **serving engines** (vLLM, TGI, TensorRT-LLM) and **continuous batching**, the throughput trick that lets one server handle many users.

### Pre-read for tomorrow (Day 19 · Serving Engines & Continuous Batching)

- **Resource:** <a href="https://docs.vllm.ai/en/latest/getting_started/quickstart.html" target="_blank" rel="noopener">vLLM - Getting Started</a> + <a href="https://www.anyscale.com/blog/comparing-llm-inference-frameworks" target="_blank" rel="noopener">Anyscale - Comparing LLM Inference Frameworks</a>.
- **Reflection questions:**
  1. Why can't you just use PyTorch in production? What's missing?
  2. What does "continuous batching" do that "static batching" doesn't?
  3. Name three serving engines and one differentiator each.
- **Reflection questions:**
  1. Why can't you just use PyTorch in production? What's missing?
  2. What does "continuous batching" do that "static batching" doesn't?
  3. Name three serving engines and one differentiator each.

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
