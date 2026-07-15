# Day 18 · Speculative Decoding

> **Concept of the day:** a small **draft** model proposes K tokens; the big **target** model verifies them in **one** parallel forward pass. Convert sequential memory-bound decode into batched-style verification. 2–3× speedup typical.<br>
> **Pre-reading:** "Speculative decoding explained" - <a href="https://huggingface.co/blog/assisted-generation" target="_blank" rel="noopener">Hugging Face - Assisted Generation (Speculative Decoding)</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
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
  {"stem": "Why is single-stream decode so wasteful of Tensor Core throughput?", "options": ["It generates too many tokens", "The GPU sits idle most of the time waiting for the next token (memory-bound), while Tensor Cores could do more work", "It uses too much memory", "The model is too small"]},
  {"stem": "What is the role of the draft model in speculative decoding?", "options": ["To generate high-quality output", "To quickly propose K tokens that the larger model will verify", "To cache KV values", "To manage memory allocation"]},
  {"stem": "Why must the draft model be much smaller than the target model?", "options": ["It doesn't need to be smaller", "So it can decode faster (more tokens per second), keeping the target model fed with work", "To save memory", "To reduce power consumption"]},
  {"stem": "What happens in the target model's verification pass?", "options": ["The target model generates new tokens from scratch", "The target model verifies the draft tokens in parallel, accepting correct ones and sampling new ones for rejected positions", "The target model caches the KV values", "The target model does nothing"]},
  {"stem": "If the draft model is wrong on token 3 of 5, what happens to tokens 1-2?", "options": ["All 5 tokens are rejected", "Tokens 1-2 are still kept (accepted); only token 3 and subsequent are reconsidered", "Tokens 1-2 are also rejected", "The draft model is not used"]},
  {"stem": "What is the typical speedup from speculative decoding, and what can kill it?", "options": ["2-3x speedup; killed by the draft model being too similar to the target", "2-3x speedup; killed if the draft model is too slow or acceptance rate is low", "10x speedup; killed by memory limitations", "No speedup; it's only for accuracy"]},
  {"stem": "Why is speculative decoding 'bit-exact' with autoregressive decoding?", "options": ["It uses the same random numbers", "The target model's verification ensures the final output is identical to what autoregressive decoding would have produced", "It doesn't guarantee exactness", "Because it uses the same model"]},
  {"stem": "What is the key insight that makes speculative decoding work?", "options": ["Using two models", "Converting sequential memory-bound decode into batched verification: the target model checks multiple tokens at once", "Reducing memory usage", "Using quantization"]}
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
  {"stem": "What is the role of the draft model in speculative decoding?", "options": ["It generates the final output tokens that are shown to the user", "It proposes K candidate tokens quickly; the target model then verifies them in a single forward pass", "It compresses the KV cache to save memory during decode", "It handles low-complexity requests while the target model handles complex ones"]},
  {"stem": "How does the target model verify the draft model's proposals?", "options": ["It re-runs the draft model on each proposal and compares outputs", "It runs a single parallel forward pass over all K draft tokens and applies a rejection-sampling correction, accepting each token with probability min(1, p_target / p_draft), that preserves the target model's distribution", "It uses a separate scorer model trained specifically for verification", "It sends the proposals to a human evaluator"]},
  {"stem": "Why is speculative decoding output bit-exact with standard decode?", "options": ["Because the draft model is identical to the target model", "Because the acceptance/rejection mechanism mathematically preserves the target model's exact output distribution", "Because speculative decoding uses the same random seed as standard decode", "Because the draft tokens are always accepted without modification"]},
  {"stem": "What primarily kills the speedup from speculative decoding?", "options": ["The draft model using more memory than the target model", "Low token acceptance rate: if the draft model's proposals frequently mismatch the target model's preferences, the per-step cost rises with little gain", "High GPU temperature causing throttling", "Large batch sizes that eliminate the latency benefit"]},
  {"stem": "Why is speculative decoding particularly effective for LLM decode specifically?", "options": ["Because decode is compute-bound and speculative decoding maximizes Tensor Core utilization", "Because decode is memory-bound and serial: small batches leave the GPU mostly idle, so the draft model's proposals use otherwise wasted compute", "Because decode uses a different model architecture that benefits from speculation", "Because the draft model can be run on the CPU, freeing GPU bandwidth"]},
  {"stem": "What does the lesson mean when it says speculative decoding is 'free latency, if the workload is predictable'?", "options": ["Speculative decoding requires no additional hardware", "On predictable outputs (code, templates), high acceptance rates mean more tokens per step with no quality loss; unpredictable outputs have low acceptance rates and the speedup shrinks", "Speculative decoding automatically disables itself for creative tasks", "All tokens are always accepted for predictable workloads"]},
  {"stem": "According to the lesson, how much faster than the target must the draft model be for speculative decoding to pay off?", "options": ["Only about 2x faster", "Roughly 10-30x faster; if the draft is too big it becomes memory-bound itself and there is no compute savings", "Exactly the same speed as the target", "Draft speed does not matter; only its accuracy does"]},
  {"stem": "What do EAGLE and Medusa do differently from classic draft-model speculative decoding?", "options": ["They run the draft model on a separate GPU cluster to free HBM bandwidth", "They enlarge the draft model to push acceptance rates higher", "Instead of a separate draft model, they train extra prediction heads on the target model itself: even cheaper", "They remove the verification pass entirely and trust the draft"]},
  {"stem": "What observation about the decode step motivates speculative decoding in the first place?", "options": ["The KV cache grows too large to fit in HBM during long generations", "Prefill is compute-bound and underutilizes memory bandwidth", "Attention becomes the dominant cost during decode", "During decode the GPU reads all the model's weights from HBM just to produce one token, leaving the Tensor Cores almost entirely idle"]}
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
