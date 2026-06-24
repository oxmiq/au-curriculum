# Day 18 · Speculative Decoding

> **Concept of the day:** a small **draft** model proposes K tokens; the big **target** model verifies them in **one** parallel forward pass. Convert sequential memory-bound decode into batched-style verification. 2–3× speedup typical.<br>
> **Pre-reading:** "Speculative decoding explained" — Pre-Lecture Reading **Reader 6** (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 4 — Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <span>Day 18 · Speculative Decoding</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-04/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review + Readiness Check | 15 min |
| Part 2 | Core Concept: The Wasted-Compute Problem | 15 min |
| Part 3 | Core Concept: The Speculative Trick | 20 min |
| Part 4 | Deep Dive: Why It's Faster + Bit-Exactness | 15 min |
| Part 5 | Hands-On: Calculations + Tradeoffs | 30 min |
| 7 | Wrap-up & Connection | 15 min |

---

## Part 1 — Pre-Reading Review + Readiness Check · 15 min
### Before You Start

You should have already read: "Speculative decoding explained" — Pre-Lecture Reading **Reader 6** (~15 min).

### Readiness Check

Answer these questions from memory before proceeding:

1. Why is single-stream decode so wasteful of Tensor Core throughput?
2. What's the role of the draft model? Why must it be much smaller?
3. What happens in the target model's verification pass?
4. What if the draft is wrong on token 3 of 5? Are tokens 1–2 still kept?
5. Expected speedup, and what kills it?

---

## Part 2 — Core Concept — The Wasted-Compute Problem · 15 min
### Reading — Why This Matters

The most impactful "free" decode speedup of the last two years. Used in vLLM, TGI, TensorRT-LLM. **Bit-exact** with greedy decoding under speculative sampling — so quality is unchanged.

### The Wasted-Compute Observation

Decode reads all 16 GB of weights from HBM to produce **one token**, doing ~32 GFLOPs of work. The H100 can do **989 TFLOPs FP16** — so the Tensor Cores are **~99.99% idle** during the 4.8 ms read.

Idea: while the GPU reads weights anyway, can it produce **more than one token of useful work**?

### Key Terms to Understand

| Term | Definition |
|------|------------|
| **Speculative decoding** | Technique where a smaller draft model proposes tokens, verified in parallel by the target model |
| **Draft model** | Smaller, faster model that proposes candidate tokens |
| **Target model** | The actual large model that verifies draft tokens |
| **Verification pass** | Target model checks all draft tokens in one forward pass |

---

## Part 3 — Core Concept — The Speculative Trick · 20 min
### Reading — How Speculative Decoding Works

1. A tiny **draft model** (e.g. 1B params, 30× smaller and faster) proposes the next **K tokens** sequentially. Cheap because it's tiny.
2. The **target model** (the real 70B) does **one forward pass over all K tokens at once** — like a mini-prefill.
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

## Part 4 — Deep Dive — Why It's Faster + Bit-Exactness · 15 min
### Reading — The Speedup Math

The target's single forward pass over K tokens has roughly the **same memory cost** as one decode step (it reads all weights once). But it produces up to K accepted tokens.

| K | If all accepted | If 60% acceptance |
|---|---|---|
| 1 (no spec) | 1 token / step | 1 token / step |
| 4 | 4 / step (4×) | ~2.4 / step (2.4×) |
| 8 | 8 / step (8×) | ~4 / step (4×) |

In practice: **2–3× end-to-end decode speedup** is the production norm for code-like or predictable text; less for surprising outputs.

### Bit-Exactness

Under **speculative sampling** (the rejection-sampling variant), the output distribution is **provably identical** to the target model decoding alone. No quality drop — it's a pure systems win.

### What Kills Speculative Decoding

- **Draft quality too low** → low acceptance rate, draft compute wasted
- **Draft too big** → draft itself becomes memory-bound, no compute savings
- **High-temperature / creative text** → less predictable, lower acceptance
- **Memory contention** — draft + target competing for HBM bandwidth

### Production Choices

- vLLM: optional draft model (`--speculative-model`)
- **EAGLE** / **Medusa**: instead of a separate draft model, train extra prediction heads on the target — even cheaper

---

## Part 5 — Hands-On — Calculations + Tradeoffs · 30 min
### Exercise 1: Verification Walkthrough (15 min)

On paper, walk through one verification step:
- Draft proposes: "the cat sat on"
- Target verifies, what's the output?

**Answer:** If target accepts "the cat sat", tokens 1-3 are kept, token 4 is rejected. Next iteration starts from "on".

### Exercise 2: Speedup Math (15 min)

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

## Part 7 — Wrap-up & Connection · 15 min
### Self-Check

Can you explain these from memory?
- [ ] Why is decode so wasteful of Tensor Cores?
- [ ] What's the role of the draft model vs target model?
- [ ] Why is speculative decoding bit-exact with vanilla decode?
- [ ] What kills the speedup?

### The Key Phrase

> **"Speculative decoding = free latency, if the workload is predictable. Always try it."**

### Connect Forward

Tomorrow: putting it all together — **serving engines** (vLLM, TGI, TensorRT-LLM) and **continuous batching**, the throughput trick that lets one server handle many users.

### Pre-read for tomorrow (Day 19 · Serving Engines & Continuous Batching)

- **Resource:** vLLM landing page + "what is continuous batching" — Pre-Lecture Reading **Reader 6** (production engines) (~15 min).
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

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
