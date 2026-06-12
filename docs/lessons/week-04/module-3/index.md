# Day 18 · Speculative Decoding

> **Concept of the day:** a small **draft** model proposes K tokens; the big **target** model verifies them in **one** parallel forward pass. Convert sequential memory-bound decode into batched-style verification. 2–3× speedup typical.
> **Pre-reading:** "Speculative decoding explained" — Pre-Lecture Reading **Reader 8** (~15 min).
> **Source:** [Study Guide §A.5](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

The most impactful "free" decode speedup of the last two years. Used in vLLM, TGI, TensorRT-LLM. **Bit-exact** with greedy decoding under speculative sampling — so quality is unchanged.

## Readiness check

1. Why is single-stream decode so wasteful of Tensor Core throughput?
2. What's the role of the draft model? Why must it be much smaller?
3. What happens in the target model's verification pass?
4. What if the draft is wrong on token 3 of 5? Are tokens 1–2 still kept?
5. Expected speedup, and what kills it?

## Core concept

### The wasted-compute observation

Decode reads all 16 GB of weights from HBM to produce **one token**, doing ~32 GFLOPs of work. The H100 can do **989 TFLOPs FP16** — so the Tensor Cores are **~99.99% idle** during the 4.8 ms read.

Idea: while the GPU reads weights anyway, can it produce **more than one token of useful work**?

### The speculative trick

1. A tiny **draft model** (e.g. 1B params, 30× smaller and faster) proposes the next **K tokens** sequentially. Cheap because it's tiny.
2. The **target model** (the real 70B) does **one forward pass over all K tokens at once** — like a mini-prefill.
3. For each draft token, target computes the probability it would have produced that token. Accept the longest prefix that matches.

### Why this is faster

The target's single forward pass over K tokens has roughly the **same memory cost** as one decode step (it reads all weights once). But it produces up to K accepted tokens.

| K | If all accepted | If 60% acceptance |
|---|---|---|
| 1 (no spec) | 1 token / step | 1 token / step |
| 4 | 4 / step (4×) | ~2.4 / step (2.4×) |
| 8 | 8 / step (8×) | ~4 / step (4×) |

In practice: **2–3× end-to-end decode speedup** is the production norm for code-like or predictable text; less for surprising outputs.

### Bit-exactness

Under **speculative sampling** (the rejection-sampling variant), the output distribution is **provably identical** to the target model decoding alone. No quality drop — it's a pure systems win.

### What kills it

- **Draft quality too low** → low acceptance rate, draft compute wasted.
- **Draft too big** → draft itself becomes memory-bound, no compute savings.
- **High-temperature / creative text** → less predictable, lower acceptance.
- **Memory contention** — draft + target competing for HBM bandwidth.

### Production choices

- vLLM: optional draft model (`--speculative-model`).
- **EAGLE** / **Medusa**: instead of a separate draft model, train extra prediction heads on the target — even cheaper.

## Practice (90 min)

1. (15 min) Walk through one verification step end-to-end on a whiteboard: draft proposes "the cat sat on", target verifies, what's the output?
2. (25 min) Math: if draft is 30× faster and acceptance rate is 0.7 at K=4, what's expected speedup over plain decode? Generalize.
3. (20 min) Pair: when *wouldn't* you use speculative decoding? (Cases where it hurts.)
4. (20 min) Tradeoff exercise: K=4 vs K=8. Pros and cons.
5. (10 min) Write a one-line rule: *"Speculative decoding wins when ___ and loses when ___."*

## Wrap-up

Cohort agrees: spec decoding is **free latency**, *if* the workload is predictable. Always try it.

## Connect forward

Tomorrow: putting it all together — **serving engines** (vLLM, TGI, TensorRT-LLM) and **continuous batching**, the throughput trick that lets one server handle many users.

---

## Pre-read for tomorrow (Day 19 · Serving Engines & Continuous Batching)

- **Resource:** vLLM landing page + "what is continuous batching" — Pre-Lecture Reading **Reader 9** (production engines) (~15 min).
- **Reflection questions:**
  1. Why can't you just use PyTorch in production? What's missing?
  2. What does "continuous batching" do that "static batching" doesn't?
  3. Name three serving engines and one differentiator each.
