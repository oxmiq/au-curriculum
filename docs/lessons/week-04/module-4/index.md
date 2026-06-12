# Day 19 · Serving Engines & Continuous Batching

> **Concept of the day:** **Continuous batching** = new requests join the running batch every step. Engines (vLLM, TGI, TensorRT-LLM) bundle this with PagedAttention, FlashAttention, quantization, scheduling. PyTorch alone is *not* a production serving stack.
> **Pre-reading:** vLLM landing page + "what is continuous batching" — Pre-Lecture Reading **Reader 9** (~15 min).
> **Source:** [Study Guide §A.5](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Glossary: vLLM, TGI, TensorRT-LLM](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Glossary.md).

---

## Why this matters

The serving engine is **where every Week 2–3–4 concept lands in code**. Continuous batching is the *single biggest throughput multiplier* of the era — often 5–10× over PyTorch. Pick the wrong engine for your workload and you give up performance and operability for nothing.

## Readiness check

1. What does **static batching** wait for? Why is that wasteful?
2. What does **continuous batching** allow that static doesn't?
3. Name three production serving engines.
4. Which engine pioneered PagedAttention?
5. Why is plain PyTorch ~5–10× slower than vLLM for serving?

## Core concept — continuous batching

### Static batching (the naive approach)

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

## Practice (90 min)

1. (15 min) Draw two timelines: static batching (4 requests, lengths 50/150/100/300) vs continuous batching. Mark idle GPU time.
2. (25 min) Read the vLLM quickstart page. Identify three CLI flags that correspond to concepts from Weeks 2–3 (e.g. `--dtype`, `--max-num-seqs`).
3. (25 min) Pair: pick an engine for each scenario — research lab w/ frequent model swaps; large-scale production on H100s; agentic tool-use product; on-prem cluster of Tenstorrent.
4. (15 min) Discussion: PyTorch is fine for *what*? When does it become a liability?
5. (10 min) Write a one-line rule: *"Continuous batching wins because ___."*

## Wrap-up

Cohort can recite: **continuous batching + PagedAttention + FlashAttention + quantization** = modern serving stack. Engines bundle these — you don't build them, you choose between them.

## Connect forward

Friday: design a serving system end-to-end. Then **[the canonical quiz](knowledge-check.html)**.

---

## Pre-read for Friday (Day 20 · Consolidation)

- **Resource:** Bring your Week 3 memory calculator and the Day 17 parallelism decision tree.
- **Reflection questions:**
  1. For a 70B-on-8-H100 deployment hitting P99 < 500 ms at 50 req/s, where do you start? TP, engine, quantization?
  2. What's the single biggest lever you have for *latency*? For *throughput*?
  3. Speculative decoding: yes/no for this workload?
