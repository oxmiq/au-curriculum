# Day 19 · Serving Engines & Continuous Batching

> **Concept of the day:** **Continuous batching** = new requests join the running batch every step. Engines (vLLM, TGI, TensorRT-LLM) bundle this with PagedAttention, FlashAttention, quantization, scheduling. PyTorch alone is *not* a production serving stack.<br>
> **Pre-reading:** vLLM + "what is continuous batching" — <a href="https://docs.vllm.ai/en/latest/getting_started/quickstart.html" target="_blank" rel="noopener">vLLM — Getting Started</a> + <a href="https://www.anyscale.com/blog/comparing-llm-inference-frameworks" target="_blank" rel="noopener">Anyscale — Comparing LLM Inference Frameworks</a> (~15 min).

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

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m4-readiness" data-kind="readiness" data-draw="5" data-source="vLLM + Continuous Batching">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "In static batching, what does the batch wait for before processing?",
    "options": [
      "A fixed number of requests to arrive",
      "All requests in the batch to finish their output",
      "GPU memory to be cleared",
      "The model to be reloaded"
    ],
    "answer": 1,
    "explain": "Static batching waits for ALL requests in the batch to complete their output before returning any results. The longest output dominates — if one request generates 500 tokens and others generate 10, everyone waits for the 500-token request to finish."
  },
  {
    "stem": "What is the key advantage of continuous batching over static batching?",
    "options": [
      "It uses less GPU memory",
      "It allows new requests to join a running batch mid-generation",
      "It processes requests faster",
      "It doesn't require any configuration"
    ],
    "answer": 1,
    "explain": "Continuous batching (iteration-level scheduling) allows new requests to join the batch after every decode step. This maximizes GPU utilization by keeping the batch full and reducing idle time between batches."
  },
  {
    "stem": "What is PagedAttention and which engine pioneered it?",
    "options": [
      "A memory optimization technique pioneered by vLLM",
      "A new attention algorithm pioneered by PyTorch",
      "A batching strategy pioneered by TensorRT-LLM",
      "A quantization method pioneered by Hugging Face"
    ],
    "answer": 0,
    "explain": "PagedAttention is a memory optimization technique that manages KV caches in non-contiguous pages, reducing memory fragmentation. It was pioneered by vLLM and is one of the key innovations that makes vLLM faster than vanilla PyTorch."
  },
  {
    "stem": "Which of these is a production serving engine for LLMs?",
    "options": [
      "PyTorch",
      "vLLM, TGI (Text Generation Inference), TensorRT-LLM",
      "NumPy",
      "Pandas"
    ],
    "answer": 1,
    "explain": "vLLM, TGI (Text Generation Inference by Hugging Face), and TensorRT-LLM (by NVIDIA) are production serving engines. Plain PyTorch is not a serving stack — it's a framework for building models, not for serving them efficiently."
  },
  {
    "stem": "Why is plain PyTorch significantly slower than vLLM for LLM serving?",
    "options": [
      "PyTorch uses older GPU architectures",
      "PyTorch lacks key optimizations like PagedAttention, continuous batching, and efficient KV cache management",
      "PyTorch is only for training, not inference",
      "PyTorch requires more GPU memory"
    ],
    "answer": 1,
    "explain": "Plain PyTorch lacks key serving optimizations: (1) PagedAttention for memory efficiency, (2) continuous batching for GPU utilization, (3) optimized CUDA kernels. These optimizations can provide 5-10x throughput improvement over naive PyTorch inference."
  },
  {
    "stem": "What is the primary benefit of iteration-level scheduling in continuous batching?",
    "options": [
      "It reduces the model size",
      "It allows the batch composition to change after every decode step",
      "It improves model accuracy",
      "It eliminates the need for GPUs"
    ],
    "answer": 1,
    "explain": "Iteration-level scheduling means the batch composition can change after every decode step. Finished requests are removed and new requests are added, allowing the batch to stay full and maximize GPU utilization throughout the serving period."
  },
  {
    "stem": "What problem does PagedAttention solve in LLM serving?",
    "options": [
      "It speeds up the prefill phase",
      "It reduces KV cache memory fragmentation",
      "It eliminates the need for quantization",
      "It improves model accuracy"
    ],
    "answer": 1,
    "explain": "PagedAttention manages KV caches in non-contiguous pages (like virtual memory in OSes), which reduces memory fragmentation. In traditional serving, KV caches must be stored contiguously, leading to waste when outputs have different lengths."
  },
  {
    "stem": "Which engine is developed by NVIDIA and optimized for their GPUs?",
    "options": [
      "vLLM",
      "TGI",
      "TensorRT-LLM",
      "LightLLM"
    ],
    "answer": 2,
    "explain": "TensorRT-LLM is NVIDIA's serving engine, optimized for NVIDIA GPUs with features like FP8 support, INT8 quantization, and tight integration with NVIDIA's software stack. It's one of the main production serving engines."
  }
]
</script>
</div>

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

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 19 · Serving Engines &amp; Continuous Batching">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the key difference between static batching and continuous batching?",
    "options": [
      "Static batching uses GPUs; continuous batching uses CPUs",
      "Static batching waits for the slowest request before accepting new ones; continuous batching inserts new requests as soon as a slot frees, without waiting",
      "Static batching supports larger batch sizes than continuous batching",
      "Continuous batching requires quantization; static batching does not"
    ],
    "answer": 1,
    "explain": "Static batching groups requests together and waits for all to complete before swapping in new ones — wasting GPU cycles when some requests finish early. Continuous batching (iteration-level scheduling) adds new requests as soon as slots open, keeping the GPU continuously busy."
  },
  {
    "stem": "Why does continuous batching require PagedAttention?",
    "options": [
      "PagedAttention speeds up continuous batching by pre-loading all KV caches",
      "Continuous batching dynamically adds and removes requests mid-batch; without PagedAttention, KV cache memory cannot be efficiently reallocated between requests",
      "PagedAttention allows continuous batching to use FP8 precision",
      "PagedAttention converts continuous batching to static batching for efficiency"
    ],
    "answer": 1,
    "explain": "Continuous batching adds/removes requests dynamically. Static contiguous KV cache allocation can't support this — fragmentation and inability to grow/shrink blocks for individual requests would cause inefficiency or OOM. PagedAttention's non-contiguous page-based allocation enables flexible dynamic memory management."
  },
  {
    "stem": "Which serving engine is best suited for maximum throughput with TensorRT optimization on NVIDIA hardware?",
    "options": [
      "vLLM — fastest time-to-first-token for any model",
      "Text Generation Inference (TGI) — best for CPU-GPU hybrid deployments",
      "TensorRT-LLM — uses NVIDIA TensorRT compilation for maximum throughput on NVIDIA hardware",
      "SGLang — best for multi-turn structured generation"
    ],
    "answer": 2,
    "explain": "TensorRT-LLM compiles models using NVIDIA's TensorRT graph optimizer, fusing operations and generating highly optimized CUDA kernels. This gives it the highest throughput on NVIDIA hardware, at the cost of longer model compilation time. vLLM prioritizes flexibility and wide model support."
  },
  {
    "stem": "Why is PyTorch alone insufficient for production LLM serving?",
    "options": [
      "PyTorch does not support FP16 inference",
      "PyTorch lacks production features: continuous batching, PagedAttention, KV cache management, and optimized kernels — it runs each request sequentially without batching infrastructure",
      "PyTorch cannot run on NVIDIA GPUs",
      "PyTorch requires training data to run inference"
    ],
    "answer": 1,
    "explain": "Bare PyTorch inference lacks production-critical features: continuous batching, PagedAttention for memory management, FlashAttention kernels, quantization support, and multi-GPU orchestration. These features are what serving engines provide on top of PyTorch's core computation graph."
  },
  {
    "stem": "What is the 'modern serving stack' described at the end of Part 7?",
    "options": [
      "Quantization + batching + caching + monitoring",
      "Continuous batching + PagedAttention + FlashAttention + quantization",
      "vLLM + TensorRT + TGI + SGLang running in parallel",
      "Load balancer + serving engine + model store + logging"
    ],
    "answer": 1,
    "explain": "The lesson states: 'Continuous batching + PagedAttention + FlashAttention + quantization = modern serving stack.' These four innovations work together: continuous batching maximizes GPU utilization; PagedAttention manages KV memory; FlashAttention speeds attention; quantization reduces memory footprint."
  },
  {
    "stem": "Which serving engine is best for structured generation and multi-turn agent workloads?",
    "options": [
      "TensorRT-LLM — best for all production workloads",
      "Text Generation Inference (TGI) — designed specifically for agent frameworks",
      "SGLang — optimized for structured generation and complex multi-turn control flow",
      "vLLM — already supports all structured generation out of the box"
    ],
    "answer": 2,
    "explain": "SGLang (Structured Generation LAnguage) is designed for structured output and complex generation programs — JSON schemas, constrained decoding, multi-turn agents. It adds a RadixAttention mechanism for KV cache reuse across shared prefixes. vLLM is the most versatile general-purpose engine."
  }
]
</script>
</div>

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
