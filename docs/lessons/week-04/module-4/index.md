# Day 19 · Serving Engines & Continuous Batching

> **Concept of the day:** **Continuous batching** = new requests join the running batch every step. Engines (vLLM, TGI, TensorRT-LLM) bundle this with PagedAttention, FlashAttention, quantization, scheduling. PyTorch alone is *not* a production serving stack.<br>
> **Pre-reading:** vLLM landing page + "what is continuous batching" — Pre-Lecture Reading **Reader 6** (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 4 — Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <span>Day 19 · vLLM Introduction</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-04/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review + Readiness Check | 15 min |
| Part 2 | Core Concept: Static vs Continuous Batching | 20 min |
| Part 3 | Deep Dive: Why This Needs PagedAttention | 15 min |
| Part 4 | Core Concept: Serving Engines Comparison | 20 min |
| Part 5 | Hands-On: Engine Selection + vLLM Quickstart | 30 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review + Readiness Check · 15 min
### Before You Start

You should have already read: vLLM landing page + "what is continuous batching" — Pre-Lecture Reading **Reader 6** (~15 min).

### Readiness Check

Answer these questions from memory before proceeding:

1. What does **static batching** wait for? Why is that wasteful?
2. What does **continuous batching** allow that static doesn't?
3. Name three production serving engines.
4. Which engine pioneered PagedAttention?
5. Why is plain PyTorch ~5–10× slower than vLLM for serving?

---

## Part 2 — Core Concept — Static vs Continuous Batching · 20 min
### Reading — Why This Matters

The serving engine is **where every Week 2–3–4 concept lands in code**. Continuous batching is the *single biggest throughput multiplier* of the era — often 5–10× over PyTorch. Pick the wrong engine for your workload and you give up performance and operability for nothing.

### Static Batching (The Naive Approach)

1. Wait for N requests
2. Run them as a batch through prefill + decode
3. Return when *all* finish (longest output dominates)

**Problems:**
- New arrivals wait for the current batch
- Short outputs sit idle while long ones finish
- GPU underutilized between batches

### Continuous Batching (A.k.a. **Iteration-Level Scheduling**)

1. Maintain a running batch of in-flight requests
2. After **every decode step**, evict finished requests and admit new ones
3. Batch size dynamically fills the GPU's KV-cache capacity

**Result:**
- New requests start almost immediately (no waiting for a batch boundary)
- GPU stays saturated
- Throughput up **5–10× vs static**

### Key Terms to Understand

| Term | Definition |
|------|------------|
| **Static batching** | Wait for N requests, process all together, return when longest finishes |
| **Continuous batching** | Admit/evict requests at every decode step; GPU stays saturated |
| **Iteration-level scheduling** | Another name for continuous batching — schedule at each token step |
| **PagedAttention** | Block-based KV-cache allocation that prevents fragmentation |

---

## Part 3 — Deep Dive — Why This Needs PagedAttention · 15 min
### Reading — The Connection

Continuous batching ⇒ KV-cache slots constantly allocated/freed at variable sizes. Without PagedAttention's block-based allocator, fragmentation kills you. That's why vLLM ships both — they're symbiotic.

**The problem:**
- Traditional attention assumes contiguous KV cache
- Variable-length outputs mean cache size changes every token
- Without paging: internal fragmentation, wasted memory, OOM crashes

**The solution:**
- PagedAttention: KV cache in fixed-size blocks (typically 16 tokens each)
- Blocks can be allocated/freed independently
- Near-zero fragmentation → full GPU memory utilization

---

## Part 4 — Core Concept — Serving Engines Comparison · 20 min
### Reading — The Big Three

| Engine | Maintainer | Key strengths | Best for |
|--------|------------|---------------|----------|
| **vLLM** | UC Berkeley + community | PagedAttention origin, broad model support, continuous batching, prefix caching | Most workloads, OSS default |
| **TGI** (Text Generation Inference) | Hugging Face | Tight HF model integration, simple HTTP API, good observability | HF ecosystem, prototyping |
| **TensorRT-LLM** | NVIDIA | Maximum NVIDIA perf, deep kernel optimization, Triton integration | Production at scale on NVIDIA |
| **SGLang** | LMSys | Strong on structured output, multi-turn / tool calls | Agentic workloads, JSON-heavy |

### What Every Modern Engine Ships With

- Continuous batching
- PagedAttention (or equivalent)
- FlashAttention v2+ kernels
- Quantized weight loading (FP8, INT4, GPTQ, AWQ)
- KV-cache prefix sharing (system-prompt caching)
- HTTP / gRPC server with OpenAI-compatible API
- Multi-GPU TP, optional PP

### Why PyTorch Alone Is Not Enough

A 10-line `model.generate()` script uses:
- Eager mode (no kernel fusion)
- Static batching
- Full attention (no FlashAttention)
- No KV-cache packing
- No quantization on the hot path

It works. It's also **5–10× slower** and falls over under any real concurrency.

### Engine Selection Rubric

| Need | Pick |
|------|------|
| Default, OSS, broad model coverage | vLLM |
| Squeeze last 20% out of NVIDIA H100s | TensorRT-LLM |
| Easy HF model + simple deploy | TGI |
| Heavy structured output / tool calls | SGLang |
| Edge / specialty accelerator (Tenstorrent, Apple) | Vendor SDK first, vLLM if supported |

1. Wait for N requests.
2. Run them as a batch through prefill + decode.
3. Return when *all* finish (longest output dominates).

Problems:
- New arrivals wait for the current batch.
- Short outputs sit idle while long ones finish.
- GPU underutilized between batches.

### Continuous batching (a.k.a. **iteration-level scheduling**)

1. Maintain a running batch of in-flight requests.
2. After **every decode step**, evict finished requests and admit new ones.
3. Batch size dynamically fills the GPU's KV-cache capacity.

Result:
- New requests start almost immediately (no waiting for a batch boundary).
- GPU stays saturated.
- Throughput up **5–10× vs static**.

### Why this needs PagedAttention

Continuous batching ⇒ KV-cache slots constantly allocated/freed at variable sizes. Without PagedAttention's block-based allocator, fragmentation kills you. That's why vLLM ships both — they're symbiotic.

## Core concept — serving engines

### The big three

| Engine | Maintainer | Key strengths | Best for |
|---|---|---|---|
| **vLLM** | UC Berkeley + community | PagedAttention origin, broad model support, continuous batching, prefix caching | Most workloads, OSS default |
| **TGI** (Text Generation Inference) | Hugging Face | Tight HF model integration, simple HTTP API, good observability | HF ecosystem, prototyping |
| **TensorRT-LLM** | NVIDIA | Maximum NVIDIA perf, deep kernel optimization, Triton integration | Production at scale on NVIDIA |
| **SGLang** | LMSys | Strong on structured output, multi-turn / tool calls | Agentic workloads, JSON-heavy |

### What every modern engine ships with

- Continuous batching.
- PagedAttention (or equivalent).
- FlashAttention v2+ kernels.
- Quantized weight loading (FP8, INT4, GPTQ, AWQ).
- KV-cache prefix sharing (system-prompt caching).
- HTTP / gRPC server with OpenAI-compatible API.
- Multi-GPU TP, optional PP.

### Why PyTorch alone is not enough

A 10-line `model.generate()` script uses:
- Eager mode (no kernel fusion).
- Static batching.
- Full attention (no FlashAttention).
- No KV-cache packing.
- No quantization on the hot path.

It works. It's also **5–10× slower** and falls over under any real concurrency.

### Choosing an engine — a quick rubric

| Need | Pick |
|---|---|
| Default, OSS, broad model coverage | vLLM |
| Squeeze last 20% out of NVIDIA H100s | TensorRT-LLM |
| Easy HF model + simple deploy | TGI |
| Heavy structured output / tool calls | SGLang |
| Edge / specialty accelerator (Tenstorrent, Apple, etc.) | Vendor SDK first, vLLM if supported |

---

## Part 5 — Hands-On — Engine Selection + vLLM Quickstart · 30 min
### Exercise 1: Draw the Batching Timeline (15 min)

Draw two timelines for 4 requests with lengths 50/150/100/300:
- Timeline A: Static batching
- Timeline B: Continuous batching

Mark where GPU is idle in Timeline A. This visual difference explains the 5-10× throughput gap.

### Exercise 2: vLLM CLI Flags (15 min)

Visit the vLLM quickstart page. Identify three CLI flags that correspond to concepts from Weeks 2-3:
- Example: `--dtype` relates to numerical precision (Week 3)
- Example: `--max-num-seqs` relates to batching (today)

Document your findings.

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you explain these from memory?
- [ ] What's the difference between static and continuous batching?
- [ ] Why does continuous batching need PagedAttention?
- [ ] Which engine is best for each use case (vLLM, TGI, TensorRT-LLM, SGLang)?
- [ ] Why is PyTorch alone not enough for production?

### The Key Phrase

> **"Continuous batching + PagedAttention + FlashAttention + quantization = modern serving stack."**

### Connect Forward

Friday: design a serving system end-to-end. Then **[the canonical quiz](knowledge-check.html)**.

---

## Pre-read for Friday (Day 20 · Consolidation)

- **Resource:** Bring your Week 3 memory calculator and the Day 17 parallelism decision tree.
- **Reflection questions:**
  1. For a 70B-on-8-H100 deployment hitting P99 < 500 ms at 50 req/s, where do you start? TP, engine, quantization?
  2. What's the single biggest lever you have for *latency*? For *throughput*?
  3. Speculative decoding: yes/no for this workload?

- **Resource:** Bring your Week 3 memory calculator and the Day 17 parallelism decision tree.
- **Reflection questions:**
  1. For a 70B-on-8-H100 deployment hitting P99 < 500 ms at 50 req/s, where do you start? TP, engine, quantization?
  2. What's the single biggest lever you have for *latency*? For *throughput*?
  3. Speculative decoding: yes/no for this workload?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
