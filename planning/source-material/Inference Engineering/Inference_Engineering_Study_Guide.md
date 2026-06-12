**Inference Engineering**

Student Study Guide

*Companion to the book by Philip Kiely (Baseten Books, 2026)*

A 10-week course for undergraduate CS / ML students

> **Source & permitted use.** This document is an instructor-authored companion derived from *Inference Engineering* by Philip Kiely (Baseten Books, 2026). It paraphrases and adapts material from that book for internal use within the Andhra University / Oxmiq curriculum only. **Do not redistribute, mirror, or publish outside this course.** Students and instructors should obtain the original book for canonical text, code samples, and references. If a formal license or permission grant for this material is established, replace this notice with a pointer to the source agreement.

How to use this guide

This study guide compresses the seven-chapter book *Inference Engineering* into a structured companion for a 10-week undergraduate course. Each chapter starts with learning objectives, then walks through key concepts, formulas, worked examples, and the pitfalls instructors find students stumble over most. End-of-chapter summaries are designed to be re-read the night before an exam.

**Prerequisites assumed:** basic neural network mechanics (you've seen a transformer slide once), linear algebra (matmul, vectors), and comfort reading Python. No CUDA or systems background is required — we build that up over the course.

**Pairing with the book:** each chapter in this guide maps 1:1 to a chapter in the book. The book has more depth, code snippets, and references; this guide gives you the structure to navigate it.

Suggested 10-week schedule

| **Week** | **Topic** | **Book chapter** |
|----|----|----|
| 1 | What is inference? The three-layer model | Chapter 0 + §1.1–1.2 |
| 2 | Model selection, latency & throughput metrics | §1.3–1.4 |
| 3 | Neural nets and LLM mechanics | §2.1–2.2 |
| 4 | Image generation, bottlenecks, attention | §2.3–2.5 |
| 5 | GPU hardware and architecture generations | Chapter 3 |
| 6 | The software stack: CUDA → engines | Chapter 4 |
| 7 | Quantization and speculative decoding | §5.1–5.2 |
| 8 | Caching, parallelism, disaggregation | §5.3–5.5 |
| 9 | Modalities beyond text | Chapter 6 |
| 10 | Production: containers, autoscaling, multi-cloud | Chapter 7 |

Chapter 0: What is Inference?

Learning objectives

- Define inference and contrast it with training.

- Name the three layers of an inference stack and what each does.

- List the six runtime techniques used to optimize a single instance.

- Explain why infrastructure (scaling, multi-cloud) is a separate problem from runtime optimization.

Core definitions

**Training** is the process of *learning* model weights from data. **Inference** is *serving* those weights to users in production. Training is a one-time (or periodic) capital expense; inference is a continuous operational expense that scales with users. Once you ship a product, almost all of the GPU-hours your company pays for are spent on inference.

Generative AI is too computationally demanding to serve naively. You can't just download weights, rent some GPUs, and expect production-grade speed and reliability. The discipline that closes that gap is **inference engineering**.

The three layers of inference

Doing inference well requires three layers working together. Optimizing only one is wasted effort if the others are broken.

- **Runtime** — getting a single model on a single instance to run as fast as possible. This is where CUDA, PyTorch, and inference engines (vLLM, SGLang, TensorRT-LLM) live.

- **Infrastructure** — scaling across clusters, regions, and clouds without creating silos. Includes autoscaling, load balancing, multi-cloud capacity, GPU procurement.

- **Tooling** — providing engineers the right level of abstraction. Too low and developers drown in YAML; too high and you can't optimize for mission-critical workloads.

The six runtime techniques (memorize these)

Every optimization in Chapter 5 of the book — and most of the second half of this course — comes back to these six levers.

1.  **Batching** — run multiple requests in parallel, weaving them token-by-token. Improves throughput.

2.  **Caching** — reuse the **KV cache** between requests that share prefixes. Improves TTFT.

3.  **Quantization** — lower the numeric precision of model weights (and sometimes activations/KV cache) to get more FLOPS and reduce memory traffic.

4.  **Speculation** — generate draft tokens cheaply and validate them with the real model, yielding more than one token per forward pass during decode.

5.  **Parallelism** — split a model across multiple GPUs to fit larger models or speed up forward passes.

6.  **Disaggregation** — separate the two phases of LLM inference (prefill and decode) onto independently scaling workers.

> **Key insight:** These six techniques generalize beyond LLMs. They apply (with variations) to vision-language models, image generation, ASR, TTS, embeddings, and video generation.

Why infrastructure matters

Even a perfectly optimized single instance will eventually receive more traffic than it can handle. Solving that is a systems problem, not a CUDA problem. The phases of infrastructure growth:

- **Small scale:** autoscaling — knowing when to add or remove replicas, and doing so quickly.

- **A few hundred GPUs:** capacity becomes the constraint. You spread workload across regions and clouds.

- **Largest scale:** silos kill you. Treat all GPUs across all clouds as a single fungible pool — like Kubernetes for clusters of clusters.

Chapter summary

Inference is the half of AI that lives in production. It splits into runtime (one box, one model), infrastructure (many boxes, many regions), and tooling (the developer abstraction in between). The six runtime techniques — batching, caching, quantization, speculation, parallelism, disaggregation — are the verbs you'll use over and over for the rest of the course.

Chapter 1: Prerequisites Before You Optimize

Learning objectives

- Decide when to use shared inference APIs versus dedicated deployments.

- Categorize an AI application by online vs. offline and consumer vs. B2B.

- Pick a model based on size, architecture, and quality budget.

- Define TTFT, TPS, ITL, and latency percentiles, and compute conversions between them.

- Distinguish inference time from end-to-end time.

1.1 Scale and specialization

Two ways to add AI to a product: **shared inference** (public API, pay per million tokens) or **dedicated deployment** (rent or own the GPUs).

|  |  |  |
|----|----|----|
|  | **Shared inference (APIs)** | **Dedicated deployment** |
| Cost | Zero overhead, pay per use | Per-GPU-hour; cheaper at scale |
| Latency | No control | Tunable |
| Uptime | Capped by provider | You control |
| Engineering effort | Tiny — just an API key | Substantial |

> **Rule of thumb:** Start on shared APIs. Migrate to dedicated when scale economics flip, when you need a custom or fine-tuned model, or when latency / uptime SLAs demand it.

1.2 What kind of app are you building?

The book uses a coach analogy: a basketball coach wants tall players, a gymnastics coach wants short ones. Inference systems must be similarly specialized to their workload. Foundation-model labs and inference platforms are the only places that must stay maximally general.

Online vs. offline

This is the master tradeoff in inference engineering.

- **Online apps** (chat, code completion, voice agents) — a user is waiting. Optimize for **latency**.

- **Offline apps** (batch transcription, document embedding, corpus prep) — no real-time user. Optimize for **throughput**.

A single model (e.g., Whisper) can serve both, but if both have volume you should run two separately tuned deployments.

Consumer vs. B2B

- **Consumer** apps are cost-sensitive with viral, spiky usage patterns. Prioritize *marginal cost* and *flexibility* with decent (not best-in-class) latency.

- **B2B** apps have better margins and more stable usage but require high availability and consistently low latency.

Compliance applies to both: data sovereignty (where are the GPUs?), user privacy, and regulatory requirements. Work with security and legal.

1.3 Model selection

All else equal, smaller models are faster and cheaper. The single most important model-performance decision is **which model you pick in the first place** — not the engine, not the speculation algorithm.

Stick to **popular architectures** (Llama, Qwen, DeepSeek, GPT-OSS) — the inference engines have the most mature support for them.

Evals

Evals are systematic measurements of model intelligence on tasks that mirror your product. They serve two purposes:

- Confirm a model is useful *before* you spend a quarter optimizing it.

- Establish a **baseline** so you can detect quality regressions from quantization or speculation.

> **Goodhart's Law:** "When a measure becomes a target, it ceases to be a good measure." Frontier labs game public benchmarks. Always build evals tailored to your product.

Fine-tuning vs. distillation

**Fine-tuning** = adapting a pre-trained foundation model to a specific use case with new data. Same architecture, new weight values.

**Distillation** = training a smaller "student" model to emulate a larger "teacher" by matching the teacher's probability distributions (not just final answers). Different architecture, smaller model.

**Concrete example:** When DeepSeek released the 671B-parameter R1 in January 2025, they also released distilled versions on top of Llama 3 and Qwen 2.5 architectures — small enough to run cheaply, while inheriting most of R1's reasoning quality.

1.4 Measuring latency and throughput

The two core LLM performance metrics, with the two phases of inference they correspond to:

| **Metric** | **What it measures** | **Tied to which phase?** |
|----|----|----|
| TTFT (time to first token) | How long until the first output token appears | Prefill (compute-bound) |
| TPS (tokens per second) | Tokens streamed per second after the first one | Decode (memory-bound) |

**TPS is ambiguous.** Disambiguating terms:

- **Perceived TPS** — tokens/sec observed by *one user* after their first token. Latency metric.

- **Total TPS** — tokens/sec generated *across the whole service*. Throughput metric.

- **Inter-token latency (ITL)** — milliseconds between tokens. Conversion: **perceived TPS = 1000 / ITL_ms**. Example: ITL 10 ms = 100 TPS/user.

Latency percentiles

Latency is right-skewed: most requests cluster near a mode, but outliers extend a long tail. The mean is misleading; report percentiles.

| **Percentile** | **Meaning**                              | **Interpretation** |
|----------------|------------------------------------------|--------------------|
| P50 (median)   | Half of requests are faster, half slower | 1 in 2 is slower   |
| P90            | 90% of requests are faster               | 1 in 10 is slower  |
| P95            | 95% of requests are faster               | 1 in 20 is slower  |
| P99            | 99% of requests are faster               | 1 in 100 is slower |

> **Don't optimize for the average.** It's not enough for most interactions to feel snappy if one in ten takes several seconds. Drive down P90 and P99, not just P50.

Inference time vs. end-to-end time

- **Inference time** — on-GPU time to generate tokens.

- **End-to-end time** — what the user experiences. Includes network, queueing, and client overhead.

> **Diagnostic heuristic:** If inference time is fast but end-to-end time is slow, the bottleneck is in the infrastructure or client, not the model.

Chapter summary

Before optimizing, understand your app. Pick a model (smallest that passes your evals). Decide whether you're optimizing for latency or throughput. Track TTFT, perceived TPS, total TPS at P50/P90/P99 — and don't conflate inference time with end-to-end time.

Chapter 2: How Models Work

Learning objectives

- Describe a neural network in terms of layers, weights, activations, and dimensionality.

- Walk through LLM inference: tokenization, prefill, decode, KV cache, logit sampling.

- Write the scaled dot-product attention formula and explain Q, K, V, multi-head, and self-attention.

- Compare dense vs. MoE architectures.

- Compute arithmetic intensity and use the ops:byte ratio to diagnose compute- vs. memory-bound kernels.

2.1 Neural networks

The fundamental unit is a **node (neuron)**: a function that takes input, multiplies by weights, adds a bias, and returns an output. Nodes are grouped into **layers**, and layers stack into a **network**. Three layer types: input, hidden, and output. The outputs of hidden layers are called **hidden states**.

Linear layers and matmul

A linear layer is the simplest layer: input vector x, weight matrix W, bias vector b.

> y = xW + b

Without something between them, two stacked linear layers collapse into one (W₃ = W₁W₂). That defeats the purpose of having multiple layers.

Activation functions

An **activation function** is a nonlinear, (mostly) differentiable function inserted between linear layers to prevent collapse. Examples: ReLU, SiLU, Swish, SwiGLU.

> ReLU(x) = max(0, x)

2.2 LLM inference mechanics

LLMs are **autoregressive token generators**: each new token depends on all prior tokens. Inference has two phases.

| **Phase** | **What happens** | **Bottleneck** |
|----|----|----|
| **Prefill** | Process the input sequence, build the KV cache | Compute-bound |
| **Decode** | Generate one output token per forward pass | Memory-bandwidth-bound |

Tokens, embeddings, and the output layer

A **tokenizer** maps strings to integer IDs deterministically. The **vocabulary** is the set of all tokens (typically \>100,000). The example *"Inference engineering makes AI apps fast."* tokenizes to 8 tokens — *In*, *ference*, *engineering*, *makes*, *AI*, *apps*, *fast*, *.*

Each forward pass during decode produces a **logit vector** of length = vocabulary size. After softmax, these become probabilities over the next token. Sampling parameters control selection:

- **Temperature** — scales logits before softmax. Lower = more deterministic.

- **Top-k** — keep only the k highest-probability tokens.

- **Top-p (nucleus)** — keep the smallest set summing to probability p.

- **Greedy** — temperature 0 or top-k 1 → deterministic.

Transformer blocks

An LLM is dozens to hundreds of stacked **transformer blocks**, each containing attention, a feed-forward network (FFN), and normalization. The FFN sublayers are the majority of trainable weights. The **LM head** at the output converts the final hidden state into the logit vector.

Attention

Attention relates each token to prior tokens. The canonical formula:

> Attention(Q, K, V) = softmax( QK^T / sqrt(d_k) ) V

- **Q (query)** — representation of the token being generated.

- **K (key)** — representations of prior tokens used for matching.

- **V (value)** — the information to pull from prior tokens.

**Multi-head attention** runs many attention operations in parallel — each head can specialize (subject-verb agreement, co-reference, etc.).

**Self-attention** (LLMs): Q, K, V all come from the same sequence. **Cross-attention**: Q comes from a different sequence (used in image generation to condition on text).

> **Quadratic to linear:** Naively, attention is O(N²) in sequence length. The **KV cache** stores K and V for prior tokens so decode becomes O(N) per generated token. Without the KV cache, modern LLMs would be unusable.

Mixture of Experts (MoE)

MoE replaces dense linear layers with hundreds of smaller "expert" matrices. A small **router** model picks a few experts per token per layer.

**Example: Qwen3-235B-A22B** — 235B total parameters but only **22B active** per request. At each layer, the router picks 8 of 128 experts; over 94 layers, the experts visited per token form a unique combination.

> **Single request vs. batched:** MoE is highly efficient for a single request (sparse activation). Under batched production load, different requests activate different experts, so almost all weights end up active simultaneously unless you split experts across GPUs (Expert Parallelism — Chapter 5).

2.3 Image generation: iterative denoising

Image generation models work by **iterative denoising**, not autoregressive token prediction. A pipeline of three components:

1.  **Text encoder** — converts the prompt into latent instructions (early models use CLIP, modern ones use a full LLM).

1.  **Denoising model** — the heart. Iteratively refines random noise in a low-dimensional **latent space** (e.g., 128×128, ~1% of pixel space).

1.  **VAE (variational autoencoder)** — decodes the final latent representation back into pixel-space image.

Each denoising step runs **two forward passes** — one with text guidance, one without — combined by the **guidance scale**. A 50-step generation = **100 forward passes**.

**Few-step models** (≤8 steps) are distilled or trained for latent consistency — 80-90% faster but with noticeably lower quality. Used for real-time generative filters.

Video generation

Video models are architecturally similar to image gen, just bigger: 3-5× more parameters, 10-100× more information in latent space (3D: width × height × time). Modern models hold the *entire* video in latent space and modify it each step — naive framewise approaches accumulate errors. Video models run with batch size 1 on a full 8-GPU node.

2.4 Calculating inference bottlenecks

A perfectly optimized GPU is busy 100% of the time on both compute and memory bandwidth. Real systems have a **bottleneck** — one resource is saturated while the other sits idle.

Three bottlenecks to memorize

- **LLM prefill** — compute-bound.

- **LLM decode** — memory-bandwidth-bound.

- **Image / video generation** — compute-bound (latent operations are like extended prefill).

Arithmetic intensity and the ops:byte ratio

Each GPU has a **peak compute speed** (FLOPS) and a **memory bandwidth** (bytes/sec). Their ratio is the **ops:byte ratio**.

**Worked example: H100 (FP16):**

- 989 TFLOPS dense compute

- 3.35 TB/s memory bandwidth

- Ops:byte ≈ 295

So for FP16 inference on an H100 to be perfectly balanced, your kernel must perform **~295 floating-point operations for every byte of memory it reads**.

**Arithmetic intensity** (also: operational intensity) is the ratio for a *specific algorithm execution*:

> intensity = work (ops) / memory traffic (bytes)
>
> **Roofline rule:** If a kernel's arithmetic intensity is **greater than** the GPU's ops:byte → compute-bound. If **less than** → memory-bound. Compare across precisions consistently.

Worked example: standard attention is memory-bound

Sequence length N = 4096, head dimension d = 128, FP16 (2 bytes/value).

Reads + writes through HBM:

> total memory = 8N² + 8Nd bytes

Compute:

> total ops = 4N²d + 3N² operations

Arithmetic intensity:

> intensity = (4N²d + 3N²) / (8N² + 8Nd) ≈ 62 ops:byte at N=4096, d=128

**62 is much less than the H100's 295** → standard attention during decode is firmly memory-bound. This is why decode TPS is bandwidth-limited and why optimizing attention is so important.

2.5 Optimizing attention

Two strategies:

- **Implementation improvements** — same math, more efficient kernels. **Lossless**. Examples: FlashAttention, PagedAttention.

- **New algorithms** — change the math to break the quadratic ceiling. **Lossy** by nature. Examples: sliding-window attention, sparse / compressed attention.

**FlashAttention** — tens of thousands of lines of fused kernels tailored per GPU generation (FA-3 for Hopper, FA-4 for Blackwell). Eliminates redundant HBM reads/writes.

**PagedAttention** — partitions the KV cache into fixed-size blocks (pages) accessed by a lookup table, allowing fragmented memory storage. Improves long-context VRAM usage.

**Sliding-window attention** — each token attends only to the previous *w* tokens (often 8K-32K). Turns O(N²) into O(Nw). Used as a lossy variant for long contexts.

Chapter summary

Linear layers do matmul; activations break linearity. Transformers stack attention + FFN blocks. LLMs prefill (compute-bound, builds KV cache) then decode (memory-bound, one token per forward pass). MoE adds sparsity. Image gen does iterative denoising in latent space. Compare each kernel's arithmetic intensity to the GPU's ops:byte ratio to know whether you should be optimizing memory or compute.

Chapter 3: GPU Hardware

Learning objectives

- Describe GPU architecture: SMs, Tensor Cores, CUDA Cores, SFUs, and the HBM/L2/L1/L0 memory hierarchy.

- Compare NVIDIA GPU generations — Ampere, Lovelace, Hopper, Blackwell, Rubin.

- Differentiate NVLink, NVSwitch, and InfiniBand.

- Explain MIG (Multi-Instance GPUs) and when to use them.

- Identify when to use other accelerators (TPU, MI300, Groq LPU, Cerebras, etc.).

3.1 GPU architecture in one page

GPUs are **throughput machines**: optimized for doing the same operation across thousands of data items in parallel. This matches the matmul-heavy workload of AI inference.

Compute

A GPU contains **Streaming Multiprocessors (SMs)**. Each SM has three kinds of compute units:

- **CUDA Cores** — scalar operations.

- **Tensor Cores** — matrix multiply-accumulate (MMA) operations: D = A × B + C. **This is the most important type of compute for inference.**

- **Special Function Units (SFUs)** — sine, cosine, log, etc. Crucial for softmax.

Compute is measured in **FLOPS**. Spec sheets list both **dense FLOPS** (every element) and **sparse FLOPS** (with 2:4 sparsity — Tensor Cores skip multiplications by zero). **Inference is dense by default** — compare dense numbers.

> **Precision and FLOPS:** FLOPS roughly double with each halving of precision. 1 PFLOPS at FP16 ≈ 2 PFLOPS at FP8. Always compare GPUs at the same precision.

Memory hierarchy

GPU memory has multiple tiers, fastest first:

- **L0** — instruction cache per Tensor Core.

- **L1** — shared memory per SM (e.g., 256 KB/SM on H100).

- **L2** — global on-chip cache (50 MB on H100).

- **VRAM (HBM)** — main GPU memory, off-chip but extremely high bandwidth.

**HBM** = High-Bandwidth Memory. Generations: HBM3, HBM3e, HBM4 (Rubin). Memory bandwidth (TB/s) is the bottleneck for LLM decode. **VRAM size limits model size**: weights must fit, plus ≥50% headroom for KV cache. Out-of-memory (OOM) is a common failure.

3.2 NVIDIA generations at a glance

| **Architecture** | **Year** | **Key features** | **Best for** |
|----|----|----|----|
| Ampere (A100) | 2020 | FP16, FP32 tensor ops | Legacy / low-cost |
| Ada Lovelace (L4, L40) | 2022 | FP8 added; no NVLink | Small models, embedding |
| Hopper (H100, H200) | 2022 | FP8, async, FlashAttention 3 | Most production today |
| Blackwell (B100, B200, B300) | 2024 | FP4, MXFP8/4, NVFP4, FA-4 | New gold standard |
| Rubin | 2026 | HBM4, dedicated CPX chip for prefill | Bandwidth-bound decode |

Key Hopper specs

| **GPU** | **FP8 (dense)** | **VRAM** | **Bandwidth** |
|---------|-----------------|----------|---------------|
| H100    | 1,979 TFLOPS    | 80 GB    | 3.35 TB/s     |
| H200    | 1,979 TFLOPS    | 141 GB   | 4.8 TB/s      |

Key Blackwell specs

| **GPU** | **FP8 (dense)** | **VRAM** | **Bandwidth** |
|---------|-----------------|----------|---------------|
| B200    | ~5 PFLOPS       | 192 GB   | up to 8 TB/s  |
| B300    | ~5 PFLOPS       | 288 GB   | up to 8 TB/s  |

3.3 Instances: how GPUs ship

A cloud **instance** is a VM bundling GPUs, CPUs, RAM, storage, networking, and interconnect. Even within one GPU model, **form factor matters**: SXM modules have ~5% higher bandwidth than PCIe cards.

Interconnects — speed hierarchy

| **Tier** | **Interconnect** | **Approximate bandwidth** | **Scope** |
|----|----|----|----|
| Fastest | NVLink (Blackwell) | Up to 1,800 GB/s | GPU ↔ GPU within a node |
| Fast | NVLink (Hopper) | 900 GB/s | GPU ↔ GPU within a node |
| Medium | NVSwitch | All-to-all on top of NVLink | All GPUs in a node |
| Slow | InfiniBand | Up to 400 Gb/s per NIC | Node ↔ Node |
| Slowest | Ethernet | Up to 100 Gb/s per NIC | Generic networking |

> **Why this matters:** Multi-node parallelism is bottlenecked by InfiniBand, which is dramatically slower than NVLink. This drives the choice of parallelism strategy in Chapter 5.

Standard node and superchips

- **Node** = 8 GPUs interconnected via NVLink + NVSwitch.

- **NVL72 GB200** = 72 Blackwell GPUs + 36 Grace CPUs in one rack, all on NVLink.

- **GH200 / GB200 superchips** pair a Grace CPU with a Hopper / Blackwell GPU via NVLink Chip-to-Chip (~900 GB/s) — useful for offloading KV cache or LoRA weights to CPU.

Multi-Instance GPUs (MIG)

MIG splits one large GPU into up to **seven smaller pieces** at the hardware level. An H100 has 132 SMs split into 7 compute slices and 8 memory slices. Useful for serving small models (TTS, small embeddings) where a full H100 would be wasteful.

3.4 Beyond NVIDIA

| **Vendor** | **Product**           | **Bet**                            |
|------------|-----------------------|------------------------------------|
| AMD        | MI350                 | CUDA-alternative on AMD silicon    |
| AWS        | Inferentia / Trainium | AWS-native cost optimization       |
| Google     | TPU                   | AI-specific ASIC                   |
| Groq       | LPU                   | Use SRAM for extreme bandwidth     |
| Cerebras   | WSE-3                 | Wafer-scale chip                   |
| Sambanova  | RDU                   | Reconfigurable dataflow            |
| Qualcomm   | Cloud AI 100          | Power-efficient mobile-derived GPU |
| Etched     | Sohu                  | Transformer-only ASIC              |

All face the same three challenges: **software** (no CUDA), **manufacturing** (extreme complexity), **distribution** (capacity rollout).

3.5 Local inference

Running inference on a user's device (phone, laptop, RTX 5090, Apple Silicon). Advantages: zero network latency, independence, privacy, free. Limitations: weaker hardware, thermal limits, fragmented software, battery drain.

Chapter summary

GPUs are throughput machines built around Tensor Cores. The memory hierarchy (HBM → L2 → L1 → registers) and the interconnect hierarchy (NVLink → NVSwitch → InfiniBand) both impose costs on inference. Hopper is the workhorse today; Blackwell is the new gold standard; Rubin lands soon. Other accelerators exist but the NVIDIA software moat is real.

Chapter 4: The Software Stack

Learning objectives

- Describe the CUDA stack: kernel, graph, driver, runtime.

- Explain kernel fusion and why it matters for decode.

- Pick between PyTorch, ONNX/TensorRT, and a production inference engine.

- Compare vLLM, SGLang, and TensorRT-LLM and pick one for a workload.

- Use benchmarking and profiling to diagnose performance issues.

4.1 CUDA

CUDA = NVIDIA's proprietary GPU programming platform. Four pieces:

- **Kernel** — a user-defined function that runs in parallel on the GPU.

- **Graph** — a DAG of kernels and ops for optimizing repeated workflows.

- **Driver** — low-level interface to GPU hardware.

- **Runtime** — developer-facing API for launching kernels.

Most inference kernels build on standard libraries:

- **cuBLAS** — CUDA's BLAS (linear algebra) implementation. **GEMM** (matrix-matrix multiply) is the most-used op.

- **cuDNN** — neural network primitives.

- **CUTLASS / CuTe** — templates for building high-performance, hardware-tuned GEMM kernels. FlashAttention 3 is built on CUTLASS.

- **FlashInfer** — optimized attention + sampling kernels for LLM inference.

Kernel fusion

Running kernels back-to-back wastes round-trips through HBM. Example: kernel A doubles \`\[1,2,3\]\` → writes \`\[2,4,6\]\` → kernel B triples it → reads \`\[2,4,6\]\`, writes \`\[6,12,18\]\`. The intermediate write/read is wasted I/O. Fused kernel: do both ops in one pass. **Critical during memory-bound decode.**

\`torch.compile\` does automatic fusion. Manual fusion (FlashAttention) is hand-written for specific GPUs and is often the difference between good and best performance.

4.2 Frameworks and file formats

- **PyTorch** — the industry standard. Python-friendly, drop-down-to-CUDA flexibility. \`torch.compile\` targets a specific GPU.

- **safetensors** (Hugging Face) — dominant weights format. Doesn't execute arbitrary code on load (unlike Python pickle/bin).

- **ONNX** — bundles weights + execution graph. Portable across hardware via ONNX Runtime.

- **GGUF** — popular for local / quantized inference.

- **Transformers / Diffusers** (Hugging Face) — *reference implementations*, not production servers. Great for spec discovery.

4.3 The three inference engines

|               |                         |             |                  |
|---------------|-------------------------|-------------|------------------|
|               | **vLLM**                | **SGLang**  | **TensorRT-LLM** |
| Performance   | Good                    | Good        | **Best**         |
| Ease of use   | Easy                    | Easy        | Hard             |
| Hardware      | NVIDIA, AMD, Intel, TPU | NVIDIA, AMD | NVIDIA only      |
| Model support | Most (day-zero usually) | Most        | Some             |
| License       | Apache 2.0              | Apache 2.0  | Apache 2.0       |

All three support continuous (in-flight) batching, post-training quantization, speculative decoding, prefix caching, parallelism, and disaggregation out of the box.

When to pick which engine

- **vLLM** — rapid stand-up, broadest model + hardware support, multimodal Omni models. Largest community.

- **SGLang** — large MoE models (DeepSeek, Kimi), strong Chinese-model day-zero support, frontend language for customization, image/video gen support.

- **TensorRT-LLM** — best raw performance on Hopper/Blackwell, NVFP4 support, willing to invest in extra engineering, plan to use NVIDIA Dynamo.

4.4 NVIDIA Dynamo

Open-source (Apache 2.0) distributed serving system, announced GTC March 2025. Works *with* every inference engine as a backend. Provides:

- **KV cache re-use** across requests.

- **Disaggregation** — splitting prefill and decode workers.

- **Multi-node parallelism** with EP.

- **SLA-based planner** that auto-scales prefill vs. decode workers using TTFT and TPS targets.

**Skip Dynamo** if you don't have huge model + huge traffic; the orchestration overhead isn't worth it.

4.5 Benchmarking and profiling

**Benchmarking** measures *what* (P90 TTFT = 350 ms). **Profiling** explains *why* (kernel A took 200 ms, kernel B took 150 ms).

Benchmarking tips

- **Best benchmark = shadow real traffic** onto a test system.

- Vary sequence lengths, traffic volume/jitter, request contents, and input parameters.

- Always establish a **baseline** before optimizing.

- **Change one variable at a time.** Some optimizations interact (speculation + large batch sizes fight each other).

- Use eval datasets (MMLU, HumanEval, SWE-bench) as realistic inputs *and* to spot-check quality.

Tooling

- **SGLang Genai-bench** — works with any framework.

- **NVIDIA GenAI-Perf** — client-side latency/throughput on varied traffic.

- **Locust** — general open-source load tester.

- **PyTorch Profiler** — per-op CPU/GPU time and memory.

Chapter summary

CUDA is the foundation. PyTorch wraps it for productivity. safetensors stores weights. Inference engines (vLLM/SGLang/TRT-LLM) bring it all together. NVIDIA Dynamo orchestrates across replicas. Benchmark and profile relentlessly — change one variable at a time.

Chapter 5: Performance Techniques

Learning objectives

- Compare FP16, BF16, FP8, FP4, INT8, INT4 — and the microscaling formats MXFP8 and NVFP4.

- Explain how quantization helps both prefill and decode.

- Describe four speculation methods: draft-target, Medusa, EAGLE, n-gram.

- Identify when prefix caching helps and where to store the KV cache.

- Choose between Tensor, Expert, and Pipeline Parallelism for a given workload.

- Decide when to use disaggregation.

> **Core principle:** The more constraints you can introduce in your inference system, the better performance you'll achieve. The more traffic you have, the more techniques become worthwhile.

5.1 Quantization

Quantization lowers the numeric precision of weights (and optionally activations and KV cache) to access more compute and reduce memory traffic. Wins both bottlenecks:

- **Prefill** (compute-bound) — lower precision = 2× FLOPS on Tensor Cores.

- **Decode** (memory-bound) — half as many bytes per value = effectively 2× memory bandwidth.

Empirically, dropping one precision level gives roughly **30-50% better LLM performance** (overhead eats some of the theoretical 2×).

Number formats

| **Format** | **Bits** | **First seen on** | **Use case** |
|----|----|----|----|
| FP32 | 32 | Kepler 2012 | Training (rare for inference) |
| FP16 / BF16 | 16 | Pascal / Ampere | Default training + inference |
| FP8 (E4M3) | 8 | Hopper 2022 | Sweet spot for inference quality + perf |
| MXFP8 | 8 | Blackwell 2024 | Microscaled FP8 with block factors |
| FP4 / MXFP4 / NVFP4 | 4 | Blackwell 2024 | Aggressive perf, careful quality work |
| INT8 / INT4 | 8 / 4 | Pascal / Turing | Low dynamic range — avoid for LLMs |

> **Float beats integer for inference.** Floating-point formats have a sign bit, exponent, and mantissa, giving them **dynamic range** to represent very large and very small values — critical for preserving outliers in attention. Integer formats can't and degrade quality.

Granularity and microscaling

Each low-precision value gets a **scale factor** to map back to its high-precision range. Granularity options:

- **Tensor-level** — one scale factor for the whole tensor. Coarse.

- **Channel-level** — per feature vector.

- **Block-level (microscaling)** — every N values get their own factor. MXFP8/MXFP4 use blocks of 32. NVFP4 uses blocks of 16 plus a global 32-bit factor.

Finer granularity = better quality (outliers preserved), more overhead. Blackwell's Tensor Cores apply scale factors in hardware to keep overhead low.

Sensitivity ranking — what to quantize

Components by increasing sensitivity to quantization:

1. **Weights** (linear layers) — *least sensitive*.

1. **Activations** — somewhat sensitive.

1. **KV cache** — moderately sensitive; quantizing here unlocks more capacity for prefix caching + disaggregation.

1. **Attention components** — *most sensitive*. Errors accumulate over thousands of tokens. **Softmax is almost always left at original precision** even in aggressive schemes.

> **Recommended starter approach:** Use FP8 (or MXFP8) on select linear layers, activations, and often the KV cache. Skip the attention sublayer. Keep the input and output layers at native precision.

QAT vs. PTQ

- **Quantization-aware training (QAT)** — train weights and scale factors jointly. Examples: GPT-OSS in MXFP4, Kimi K2 Thinking in INT4.

- **Post-training quantization (PTQ)** — convert finished weights using calibration data. **The only option for open models you didn't train.**

Tools: **NVIDIA TensorRT Model Optimizer (ModelOpt)** is the leading open-source PTQ library.

Measuring quality

Standard for production quantization is **zero perceptible quality loss**. Three quality checks:

14. **Perplexity** — quantized vs. original on representative sequences. Look for *minimal increase*.

15. **Intelligence benchmarks** — MMLU, SWE-bench, HumanEval.

16. **Custom evals** — your product-specific suite.

LLMs are non-deterministic; differences should be indistinguishable from noise.

5.2 Speculative decoding

Decode is memory-bound — compute sits idle at low batch sizes while weights are read. **Speculation** uses that spare compute to generate multiple tokens per forward pass.

Three steps:

17. **Draft** — generate one or more draft tokens cheaply.

18. **Validate** — target model runs forward pass and checks them.

19. **Accept** + generate one new token.

Result: **N+1 tokens per forward pass**, where N = accepted drafts. The book's analogy: solving a sudoku is hard; *checking* a finished one is easy.

Performance factors

- **Draft cost** — must be cheap relative to target.

- **Draft length** — too long and tail tokens get rejected.

- **Acceptance rate** — depends on temperature, subject matter, batch size.

> **When to disable:** Speculation hurts at high batch sizes because compute is no longer idle — it must be *dynamically disabled* when the system is saturated.

Four methods

| **Method** | **How** | **Best use** |
|----|----|----|
| **Draft-target** | Small separate draft model (≥10× smaller than target, same family) | Quick OOTB; no training |
| **Medusa** | Graft 2-4 extra decoder heads onto target via fine-tuning | Simple; limited in practice |
| **EAGLE** | Purpose-built draft model trained on hidden states from the target; up to 8 draft tokens | **Go-to in production** when you can train |
| **N-gram / Lookahead** | Build n-gram dictionary at prefill; match suffixes during decode | Code completion (long matches), repetitive input |

5.3 Caching

Prefix caching

Two requests sharing a prefix can skip prefill for the shared portion. Example: \`"Weather in SF ?"\` and \`"Weather in NYC ?"\` share \`"Weather in"\`. The KV cache for the prefix is reused — improving TTFT.

> **Hard rule:** Prefix caching works **only until the first non-repeated token**. If \`SF\` and \`NYC\` appear at position 3, nothing after position 2 is shared — even tokens that *happen* to match (like the \`?\`) won't be cached. **Place novel tokens as late as possible** in your context.

High-value domains: complex system prompts, code completion, document retrieval, multi-turn chat.

Where to store the KV cache

| **Tier** | **Storage**   | **Speed**     | **Size**     |
|----------|---------------|---------------|--------------|
| G1       | GPU VRAM      | TB/s          | 10s-100s GB  |
| G2       | CPU RAM       | 10s-100s GB/s | 100s GB - TB |
| G3       | Local SSD     | 5-10 GB/s     | TB           |
| G4       | Networked SSD | GB/s          | 10s TB       |

**NVIDIA Dynamo's KVBM (KV Block Manager)** moves blocks between tiers as access patterns shift.

Cache-aware routing

In production with multiple replicas, send a user's long conversation back to the *same* replica so prefix caching pays off. Alternative: a **global KV cache** on networked storage (G4), accessible from any replica.

Long context handling

Long context arrives when the KV cache itself becomes the bottleneck. Tools: FlashAttention, PagedAttention, chunked prefill (overlaps long prefill with ongoing decode). Beyond that, you parallelize across GPUs.

5.4 Model parallelism

**Every frontier LLM today is too big to fit on a single GPU** during real workloads. Sizing math (FP8, ~1 GB per 1B params, ~1.8× headroom for KV cache):

> VRAM_needed = (bits/8) \* params \* kv_overhead DeepSeek-V3 (671B, FP8) → ~1,200+ GB → 8 × B200 (1,440 GB)

Three parallelism strategies

| **Strategy** | **What it splits** | **Strength** | **Weakness** |
|----|----|----|----|
| **Tensor Parallelism (TP)** | Each layer's weights across GPUs | **Lowest latency** | Heavy all-reduce — no multi-node |
| **Expert Parallelism (EP)** | Experts of an MoE across GPUs | **Highest throughput**, multi-node-friendly | Only for MoE models |
| **Pipeline Parallelism (PP)** | Successive layers across GPUs | Multi-node fallback | Pipeline bubbles waste compute |

Real production deployments often **combine TP within a node + EP across nodes** (e.g., TP8 + EP across 2 nodes). For dense models multi-node, fall back to TP8 + PP2.

5.5 Disaggregation

Separate prefill and decode onto different engines. The prefill engine processes the input, builds the KV cache, and sends it over the interconnect to the decode engine.

Why disaggregate

- Prefill (compute-bound) and decode (memory-bound) **interfere** when run together at high load.

- Each engine can use **different parallelism, quantization, and TP factors** — prefill wants more compute and lower TP; decode wants more memory and higher TP.

- Prefill and decode engines **scale independently** based on traffic shape.

Conditional disaggregation

Real traffic is mixed. Requests first go to the decode engine, which checks if input is cached or short enough — if so it handles prefill locally; otherwise it forwards to the prefill engine. Notation: **xPyD** = x prefill engines + y decode engines (e.g., 5P3D).

> **When to disaggregate (all three must be true):** 1) Heavy traffic (~100M-1B tokens/day for the model size); 2) Large model (≥100B params); 3) Prefill-heavy workload (long input sequences). If not all three, use the GPUs for horizontal replica scaling instead.

Chapter summary

Quantization gives you compute + bandwidth simultaneously. Speculation buys parallel tokens for free when batch sizes are low. Caching reuses prefill work. Parallelism makes huge models fit and run fast — TP for latency, EP for throughput on MoE. Disaggregation only earns its complexity at large scale on large models.

Chapter 6: Other Modalities

Learning objectives

- Describe how VLMs, embeddings, ASR, TTS, image gen, and video gen differ from LLM inference.

- Identify which LLM optimizations transfer and which don't (per modality).

- Define modality-specific metrics like time to first sentence and Real-Time Factor.

- Explain why image and video generation are compute-bound.

- Describe Context Parallelism and why video models need it.

Quick comparison

| **Modality** | **Archetype** | **Bottleneck** | **Key optimization** |
|----|----|----|----|
| LLM | Autoregressive | Decode = memory | Speculation, quantization, KV cache |
| VLM | Autoregressive + vision encoder | Long context | Prefix caching, attention opts, downsampling |
| Embedding | Encoder-only | Throughput | Big batches, horizontal scaling |
| ASR (e.g. Whisper) | Encoder-decoder | Decode (LLM-like) | TensorRT-LLM, WebSocket streaming, VAD |
| TTS | LLM-style + audio decoder | Audio decoder | FP8 quant, in-flight batching, MIG |
| Image gen | Iterative denoising | Compute | Kernel fusion, guidance trick, few-step models |
| Video gen | Iterative denoising over X,Y,T | Compute (attention dominates) | Context Parallelism, attention caching |

6.1 Vision Language Models (VLMs)

VLMs wrap two modules: a **small vision encoder** (often ~2B params) and a **standard LLM backbone**. The encoder adds ~1,000 visual tokens per high-resolution image, making input sequences long. High-res = 4× more tokens than low-res — necessary for video, where one second at 24 fps × ~1,000 tokens = 24,000 tokens.

Standard LLM optimizations all transfer: KV cache quantization, EAGLE speculation, prefix caching, Tensor Parallelism, disaggregation. **New tradeoff:** downsampling input resolution and frame rate.

**Omni-modal models** (text + image + audio + video in/out) trade specialization for generality. Specialized models (dedicated OCR, dedicated VAD) often outperform a VLM at a fraction of the cost. Real production pipelines mix both.

6.2 Embedding models

Embeddings convert variable-length input into fixed-length vectors used for RAG, search, recommendations. Two traffic profiles:

- **High-throughput backfills** — bulk indexing of millions of docs.

- **Low-latency lookups** — user-facing search/retrieval.

Architectures: **BERT-style** (encoder-only, \<1B params, fast) and **LLM-based** (≤8B, higher quality). **Matryoshka representations** allow trading vector dimensionality for speed/quality.

> **Why embedding inference differs:** Tokens process in parallel → **prefix caching and disaggregation are irrelevant**. Models are small → **multi-GPU parallelism is wasted**; scale horizontally. **Batching is huge** — dozens to hundreds of inputs per request. Robust queuing for surges is essential.

FP8 quantization of weights works well. Validate with cosine similarity between original and quantized outputs (target ≥99%).

6.3 Automatic Speech Recognition (ASR)

Whisper is the canonical open ASR model — even the largest (Whisper 3 Large) is just 1.55B params. **Decoder dominates runtime** and is LLM-like → TensorRT-LLM is the main optimization tool.

Two scenarios

- **Single-chunk latency (live dictation)** — target ~200 ms per chunk. Most gains come from **WebSocket streaming + Voice Activity Detection (VAD)**, not the model.

- **Long file** — measured in **Real-Time Factor (RTF)**: optimized Whisper can hit ~1,000× (transcribe an hour in 4 seconds). Pipeline: VAD chunks → distribute across MIG slices → stitch by timestamp.

Diarization

"Who spoke when." Different architecture entirely — classic ML pipeline (pyannote: segmentation + embedding + clustering). Optimize with PyTorch + Torch compilation. Diarization is the slow part — typically ~2× transcription time even when optimized.

6.4 Text to Speech (TTS)

Modern TTS models (e.g., Orpheus, derived from Llama 3.2 3B) are fine-tuned LLMs whose vocabulary includes audio tokens. They feed an **audio decoder** (e.g., SNAC) to produce waveform. Custom metrics:

- **TTFB (time to first byte)** — analog of TTFT.

- **Time to first sentence** — more user-meaningful.

- **TPS** capped at real-time playback (~80-100 tokens/sec). Extra capacity → more concurrent users per GPU.

WebSocket streaming + FP8 quantization + in-flight batching are standard. Orpheus on a single H100 achieves ~150 ms TTFB.

6.5 Image generation

Compute-bound. Kernel selection is critical (FlashAttention 3/4 for attention, GEMM with 8-bit FP, RMSNorm fusion). Three engines: **SGLang Diffusion**, **TensorRT**, or **PyTorch directly**. Engines must be compiled for the exact GPU.

> **"One Weird Trick":** Classifier-free guidance requires 2 forward passes per step. Skipping guidance for the last 20 of 50 steps drops 80 passes vs. 100 — quality usually holds because the model isn't repainting a cat as a dog late in generation.

6.6 Video generation

The most demanding modality. **Attention is 70-80% of compute time.** Should run on Blackwell (or Rubin). Batch size 1; all 8 GPUs of a node work on one video.

Attention caching

- **Timestep-based** — reuse outputs of certain timesteps to skip whole steps.

- **Transformer-based** — reuse hidden states to skip layers.

30-40% faster, but quality impact varies — test carefully.

Context Parallelism

Video models use **CP** (not TP). Weights are *replicated* across all 8 GPUs (small enough); the *attention computation* is split via **ring attention** — each GPU holds a piece of the context and passes intermediates around the ring. Attention heads are independent so they parallelize naturally.

Chapter summary

LLM tricks transfer broadly (VLMs, ASR, TTS) but not universally. Embeddings need different ops (big batches, no caching, no parallelism). Image and video gen are compute-bound, run via specialized engines, and benefit from kernel fusion and selective skipping. Video models break the parallelism mold with Context Parallelism.

Chapter 7: Production

Learning objectives

- Build a container image for an inference workload.

- Configure autoscaling with concurrency and batch sizing in mind.

- Diagnose and mitigate cold starts.

- Explain multi-cloud capacity management and GPU procurement modes.

- Compare blue-green and canary deployment strategies for GPU workloads.

- Estimate cost: dedicated vs. per-token API.

7.1 Containerization

Containers package your app + dependencies into an immutable image. Vocabulary: **container** (running instance), **image** (executable package), **Dockerfile** (build script), **registry** (image store).

Inference dependency chains are long and fragile. A typical image bundles:

- **CUDA toolkit + cuDNN + driver versions** (must match the GPU).

- **Python packages** — torch, transformers, diffusers.

- **Inference engine** — vLLM / SGLang / TensorRT-LLM.

- **System packages** — ffmpeg, etc.

> **Best practices: Pin exact versions** (\`transformers==4.56.2\`). Start from vLLM/SGLang's official base images. For day-zero model launches, expect to use pre-release builds and rebuild against stable releases over the following weeks.

7.2 Autoscaling

Goal: enough capacity for traffic + SLAs without paying for idle GPUs. Built on Kubernetes (control plane + worker plane).

Signals to autoscale on

- **Utilization** — GPU memory/compute (lagging indicator).

- **Traffic** — incoming request count (proactive).

Use both — they diverge. A few requests with 100K uncached tokens can spike utilization more than many small high-cache-hit requests.

Five autoscaler knobs

- **Min replicas** — floor at low traffic.

- **Max replicas** — ceiling at peak.

- **Autoscaling window** — measurement timeframe.

- **Scale-down delay** — wait before honoring a scale-down.

- **Concurrency target** — requests per replica. **Must match the inference engine's batch size.**

Batch sizing strategies

- **Static batching** — wait for batch to fill. High queue times.

- **Dynamic batching** — fill or timer-cutoff.

- **Continuous (in-flight) batching** — token-level interleaving. **Best latency.** All three engines support it.

7.3 Cold starts

The time from launching a replica to its first response. Four contributors:

20. **GPU procurement** — cloud-provider problem.

21. **Image loading** — slim images load faster.

22. **Model loading** — *don't bake huge weights into images*; load from cached storage close to the GPU.

23. **Engine startup** — TensorRT-LLM/PyTorch-compiled engines take *minutes* to compile. **Cache the compiled engines** and load them on matching GPUs.

7.4 Routing, load balancing, queueing

- **Router** — "where *should* this request go?" (e.g., KV-cache-aware).

- **Load balancer** — "where *could* it go?" (based on current load).

- **Queue** — FIFO or priority. Holds requests during surges.

Intelligent routing matters when sequences vary widely. KV-cache-aware routing sends a user back to the replica that already has their prefix; LoRA-aware routing finds replicas with the right adapter loaded.

Scale to zero

Drop to zero replicas when idle, spin up on demand. Requires fast cold starts and robust queueing. Good for development and predictable batch workloads. **Bad for latency-sensitive light traffic** — pay-per-token APIs are better there.

7.5 Multi-cloud capacity management

Single clusters cap out. Global products need thousands of GPUs across many regions. **True multi-cloud** treats all clusters as a single fungible pool — like Kubernetes for clusters of clusters. Unlocks capacity, redundancy, low latency (proximity to users), and compliance (data sovereignty).

Provider types

- **Hyperscalers** (AWS, GCP) — premium-priced, broadest services.

- **Neoclouds** (CoreWeave, Nebius) — GPU-focused.

- **Resellers** (SF Compute Company) — secondary spot market.

Procurement modes

- **Reserved** — hundreds to thousands of GPUs locked in for months/years, discounted.

- **On-demand** — per-instance, no commitment.

- **Spot** — discounted, pre-emptible.

Reliability

> **Failure is expected.** Llama 3 training had **419 unexpected interruptions in 54 days on 16,000 GPUs** — roughly 1 failure per 50,000 GPU-hours. A single 8-GPU node running inference for a year accumulates 70,000+ GPU-hours. Build for failure.

- **Active-active** — multiple regions serve live traffic simultaneously.

- **Active-passive** — hot standby idle until failover.

7.6 Testing and deployment

Blue-green vs. canary

- **Blue-green** — two parallel environments, cut over fully. Classic but **doesn't scale for inference** — 100-GPU blue means 100-GPU green too.

- **Canary** — route small % of live traffic to the new deployment, ramp up gradually. **Preferred for GPU workloads** because autoscaling shrinks the old version as traffic moves.

Cost estimation example

Compare per-token to dedicated for a workload of 1B input tokens + 500M output tokens:

> Per-token: 1B × \$1.25/M + 500M × \$10/M = \$6,250 Dedicated: 1,600 GPU-hours × \$3.50/hour = \$5,600

Use ≥1 week time horizons to smooth variance. Add engineering time and TCO to dedicated costs.

Observability

Treat inference like any mission-critical service. Metrics to track:

- Total volume, request/response sizes.

- Response codes (2XX / 4XX / 5XX).

- TTFT, TPS, end-to-end latency at P50/P90/P99.

- Replica count, queue depth, utilization.

Send metrics to Grafana, Datadog, PagerDuty, Sentry — don't silo them from the rest of the app.

7.7 Client code

Often overlooked latency source.

- Establishing a TLS session takes "a few dozen ms." **Reuse sessions** — the OpenAI SDK does this silently.

- **Asynchronous inference** for throughput-not-latency workloads (bulk doc processing). Webhook callback when done.

- **Streaming** matters for UX. For LLMs: HTTP streaming is enough. For voice/video: **WebSockets** (unstructured, real-time) or **gRPC** (structured, schema-enforced).

Chapter summary

Production inference is a systems discipline. Container images bundle the stack. Autoscalers balance traffic + utilization signals using batch-aware concurrency targets. Cold starts are usually fixable by caching engines and weights close to GPUs. Multi-cloud unlocks capacity, redundancy, latency, and compliance. Plan for failure — it's the default.

Quick reference card

Six runtime techniques

Batching · Caching · Quantization · Speculation · Parallelism · Disaggregation.

Key formulas

> - ITL (ms) → perceived TPS: `TPS = 1000 / ITL`
> - Arithmetic intensity: `intensity = ops / bytes`
> - Ops:byte ratio (H100 FP16) ≈ `295`
> - Attention: `Attention(Q, K, V) = softmax( QK^T / sqrt(d_k) ) V`
> - Linear layer: `y = xW + b`
> - VRAM rule of thumb (FP8): `GB ≈ params (B) × 1.8` (KV cache headroom)

Bottleneck cheatsheet

- **LLM prefill** → compute-bound → quantization, FP8 Tensor Cores.

- **LLM decode** → memory-bound → speculation, KV cache, microscaling formats.

- **Image / video gen** → compute-bound → attention kernels, guidance skipping, Context Parallelism.

Parallelism cheatsheet

- **Lowest latency** → Tensor Parallelism (within a node).

- **Highest throughput on MoE** → Expert Parallelism.

- **Multi-node dense fallback** → Pipeline Parallelism (don't love it, but it works).

- **Video generation** → Context Parallelism with ring attention.

When to disaggregate

Only when all three are true: ≥100M tokens/day, ≥100B-param model, prefill-heavy traffic.

Engine selection one-liner

- **vLLM** = anywhere, anything, fast to stand up.

- **SGLang** = MoE LLMs, Chinese models day-zero, image/video gen.

- **TensorRT-LLM** = best perf on Hopper/Blackwell when you have time to tune.

---

# Appendix A — Per-chapter depth supplements

This appendix exists because the main body, while broad, sometimes moves quickly past the numbers and the traps. Each section below adds four things to the matching chapter: a **Why this matters** framing paragraph, a **Worked numerical example** with real hardware specs, a **Common confusions** list, and a **How this connects to later weeks** pointer. Use it on the second pass — after you've read the chapter once and want to stress-test your understanding.

Concept-ID cross-references use the IDs in `docs/kb/concepts.json`. If a section says "see `kv-cache`", you can look that ID up in the concept graph and the glossary's Appendix B to go deeper.

---

## A.0 Chapter 0 supplement — What is Inference?

**Why this matters.** Most CS students arrive having only seen *training* (Karpathy videos, an Andrew Ng course, a homework on MNIST). They think AI engineering is mostly hyperparameter tuning. It isn't. By 2026, the GPU-hours your future employer pays for are >95% inference, <5% training. The career bet you make by mastering inference engineering is enormous: you're learning the half of AI that pays the bills.

**Worked numerical example — training vs. inference cost ratio.** Suppose a startup trains a 7B Llama-style model once. Training cost: roughly 100,000 H100-hours at ~$2/hr = **$200K, one-time**. Now they ship it to 100,000 daily users who each chat 5,000 tokens/day. That's 500M tokens/day. A single H100 at FP8 can serve ~5,000 tokens/sec with batching → ~430M tokens/day. So they need ~2 H100s running 24/7 just for steady-state load = ~$3K/day = **~$1M/year, recurring**. Within 3 months, inference cost exceeds the one-time training cost. By year 1, inference is 5× training. This is why "make inference 2× cheaper" is a higher-impact lever than "make training 2× cheaper" at almost every shipping AI company.

**Common confusions.**

- *"Inference is just `model.forward()` in a loop."* — No. Production inference is batching, paging, scheduling, kernel selection, and quantization, all running while requests stream in continuously.
- *"The six runtime techniques are independent."* — They interact. Quantization frees memory that enables larger batches. Speculation only works with batching that can absorb the variable-token-per-step pattern. Disaggregation rebalances which technique applies to which phase.
- *"Tooling is a polish concern."* — At scale, the abstraction layer is what determines whether your team ships in days or months. Bad tooling at 1,000 GPUs creates a separate full-time SRE team.

**How this connects to later weeks.** The six techniques are the spine of Weeks 7–9. The runtime/infra/tooling split is the spine of Week 10. Internalize this taxonomy now — every later chapter slots back into it.

Concept-graph anchors: `inference-vs-training`, `ai-stack-overview`.

---

## A.1 Chapter 1 supplement — Prerequisites Before You Optimize

**Why this matters.** Optimizing the wrong thing is the most common rookie mistake. You can spend a month getting +20% throughput on a workload that's actually latency-bound, and your users will not notice. Chapter 1's whole job is to teach you to *measure first*, *pick targets second*, *optimize third*.

**Worked numerical example — TTFT vs. throughput trade-off.** A chat app has 1,000 concurrent users. On one H100 you can run batch-size 32 with TTFT ≈ 300 ms and per-user TPS ≈ 50, or batch-size 128 with TTFT ≈ 900 ms and per-user TPS ≈ 25. Which is better? Depends on the product. For a chat UI where users read at ~250 words/min ≈ 5 tokens/sec, even 25 TPS feels instant after the first token — so the 900 ms TTFT is the perceptible regression. **The bigger batch wins on cost-per-token but loses on user experience.** Most teams pick the smaller batch and pay 30–40% more per token in exchange for snappier UX. This trade-off is rediscovered by every team that ships an LLM product.

**Common confusions.**

- *"Latency is one number."* — Latency is a distribution. P50 and P99 can differ by 5×. Optimizing the mean often *worsens* the tail.
- *"TTFT and TPS are the same metric in different units."* — They are independent. TTFT is dominated by prefill compute on the input prompt. TPS (decode rate) is dominated by memory bandwidth on weight + KV reads.
- *"Shared inference APIs are always cheaper than dedicated."* — Crossover is usually around 100M tokens/day for a popular model. Past that, dedicated wins on $/token, often by 3–5×.

**How this connects to later weeks.** TTFT becomes a Chapter 5 lever (caching). TPS becomes a Chapter 5 lever (speculation). The shared-vs-dedicated decision becomes a Chapter 7 lever (autoscaling + multi-cloud).

Concept-graph anchors: `latency-throughput`, `inference-cost`, `token`.

---

## A.2 Chapter 2 supplement — How Models Work

**Why this matters.** You cannot reason about kernel-level optimizations without knowing what the model is actually doing at each step. The students who skip this chapter end up cargo-culting flags into vLLM with no idea why one helped and another didn't.

**Worked numerical example — KV-cache size for Llama-3.1 8B.** Llama-3.1 8B has 32 layers, 32 attention heads (8 KV heads after GQA), head dim 128, FP16. KV-cache per token = `2 (K+V) × 32 layers × 8 KV-heads × 128 dim × 2 bytes = 131,072 bytes = 128 KiB/token`. At 8K context per request: `128 KiB × 8192 ≈ 1 GiB per request`. On an H100 with 80 GB, after subtracting ~16 GB for weights, you have ~60 GB for KV cache → **~60 concurrent 8K-context requests**, not the hundreds you might naively expect. This single number drives the rest of the course: it's why we care about paged attention, KV quantization, GQA, and MLA.

**Worked numerical example — arithmetic intensity of prefill vs. decode.** A prefill on a 1,000-token prompt does `~2 × N × D²` ops per layer for the matmul-dominant linear projections, while reading the weights once: arithmetic intensity ≈ several hundred ops/byte → above H100's FP16 ridge-point (~295) → **compute-bound**. A single decode step does `~2 × D²` ops per layer (one token) but reads the same weights → intensity ≈ 1 op/byte → **memory-bound by ~300×**. Same model, same GPU, two phases — completely different bottleneck. This is the single most important diagram in inference engineering.

**Common confusions.**

- *"Attention is the expensive part."* — Only for long contexts. For short prompts and small models, the FFN matmuls dominate FLOPs.
- *"Bigger model = slower inference linearly."* — Not at decode. Decode is memory-bound; a 70B FP16 model isn't 10× slower than a 7B FP16 model, it's roughly 10× more memory traffic. Then bandwidth saturation kicks in.
- *"Softmax is cheap."* — Numerically it's cheap. But it forces FP precision and creates the bf16/fp32 boundary every quantization scheme has to respect.

**How this connects to later weeks.** Every Chapter 5 technique is "make prefill less compute-bound" or "make decode less memory-bound." Hold those two sentences in your head and the next four weeks make sense.

Concept-graph anchors: `transformer-architecture`, `self-attention`, `kv-cache`.

---

## A.3 Chapter 3 supplement — GPU Hardware

**Why this matters.** Hardware is the floor under every software optimization. If you don't know your GPU's HBM bandwidth, FLOPS, and interconnect topology, you can't tell whether you're hitting a fundamental limit or leaving 5× on the table.

**Worked numerical example — H100 vs. B200 decode bandwidth.** H100 SXM: 80 GB HBM3 at 3.35 TB/s. B200: 192 GB HBM3e at 8 TB/s. For a memory-bound decode step on a 70B FP8 model (~70 GB of weight reads per token at the limit, in practice less due to TP), peak token rate scales roughly with bandwidth: B200 should give ~2.4× the decode TPS of H100, all else equal. In published benchmarks (mid-2025), B200 typically gives 2.0–2.5× on decode-dominant workloads — close to the bandwidth ratio, confirming decode really is bandwidth-bound on these chips.

**Worked numerical example — why TP stays inside a node.** NVLink 4 bandwidth ≈ 900 GB/s GPU-to-GPU. InfiniBand HDR ≈ 50 GB/s GPU-to-GPU across nodes. Ratio: 18×. An all-reduce in tensor parallelism happens *every layer* (so ~80× per token for a 80-layer model). If you cross a node boundary with TP, you pay the 18× penalty 80 times per token. This is why every production deployment uses TP ≤ 8 (one node) and switches to PP or EP across nodes.

**Common confusions.**

- *"More VRAM is always better."* — Only if your bandwidth keeps up. A GPU with 2× the VRAM but the same bandwidth gives you bigger models at the same speed, not faster inference.
- *"Tensor Cores and CUDA Cores do the same thing."* — Tensor Cores are matmul-specialized and ~10–30× faster than CUDA Cores for matmul. Most of your inference FLOPS come from Tensor Cores.
- *"L4 is just a smaller H100."* — Different architecture (Ada vs. Hopper), no NVLink, half the memory bandwidth class. L4 wins on $/token for small models served at scale; H100 wins on absolute latency.

**How this connects to later weeks.** Chapter 4's CUDA stack exists to extract performance from this hardware. Chapter 5's parallelism choices are forced by NVLink-vs-IB asymmetry. Chapter 7's multi-cloud strategy is partly driven by which clouds have which GPU SKUs available.

Concept-graph anchors: `gpu-memory-hierarchy`, `gpu-generations`.

---

## A.4 Chapter 4 supplement — The Software Stack

**Why this matters.** Every CUDA bug story you read on the vLLM issue tracker is a story about one of these four layers misbehaving. Knowing which layer owns which symptom turns a 3-day debugging session into a 30-minute fix.

**Worked numerical example — kernel fusion payoff.** A naive PyTorch forward of a single transformer block launches ~30 kernels per layer (matmul, add, layernorm, matmul, GELU, matmul, add, …). H100 kernel launch overhead ≈ 5 µs. At 30 layers × 30 kernels × 5 µs = **4.5 ms of pure launch overhead per token**, before any actual compute. At target decode latencies of ~10 ms/token, launch overhead eats half your budget. Fused kernels (FlashAttention, RMSNorm fused with matmul, etc.) collapse 30 launches into 3–5, recovering nearly all of that budget. This is why kernel-fused engines (TRT-LLM, SGLang) beat naive PyTorch by 2–3× on small models even before any quantization.

**Common confusions.**

- *"PyTorch is the inference engine."* — PyTorch is a *deep learning framework*. vLLM, SGLang, TRT-LLM are the *inference engines* sitting on top of it (or replacing parts of it). They add continuous batching, paged attention, scheduling, and CUDA graph capture — none of which PyTorch does on its own.
- *"CUDA version doesn't matter."* — It matters a lot. FP8 requires CUDA 12+, FlashAttention-3 requires specific compute capability, certain MoE kernels are H100-only. Version mismatches cause 40% of production startup failures.
- *"More layers in the stack = more overhead."* — Sometimes the *opposite*. Adding TensorRT below PyTorch gives 2× speedup because it folds the graph. Layering is a tax only when each layer redoes work.

**How this connects to later weeks.** The Chapter 5 techniques are all *engine-level*: you don't write your own attention kernel, you pick an engine that has one. Engine selection (vLLM / SGLang / TRT-LLM) is the single most consequential Week-7 decision.

Concept-graph anchors: `cuda-stack`, `inference-engines`, `continuous-batching`.

---

## A.5 Chapter 5 supplement — Performance Techniques

**Why this matters.** This is the most exam-able chapter and the most interview-able material. Every senior inference engineer can riff for 20 minutes on each of the six techniques. The depth here separates "I read a blog post" from "I can ship this."

**Worked numerical example — speculative decoding speedup.** Target model: Llama-3.1 70B FP8 on H100. Draft model: Llama-3.2 1B FP8. Decode latency: target = 25 ms/token, draft = 2 ms/token. Speculate 5 tokens per draft pass, average acceptance rate = 3 of 5. One spec cycle = `1 draft pass × 5 tokens × 2 ms + 1 target verify × 25 ms = 10 + 25 = 35 ms`, produces 3 accepted tokens → **11.7 ms per accepted token vs. 25 ms baseline = 2.1× speedup**. The acceptance rate is the whole game — if it drops to 2/5 you only get 1.7×; if it rises to 4/5 you get 2.6×. This is why draft model selection is its own subdiscipline.

**Worked numerical example — FP8 vs. FP16 throughput on H100.** H100 SXM peak: 989 TFLOPS FP16 dense, 1979 TFLOPS FP8 dense. **2× peak compute for FP8.** But for memory-bound decode, FP8 also *halves* the weight bytes you read → another 2× speedup. Combined effect on a 70B model: **~4× decode throughput vs. FP16, with typical 0.1–0.3 point MMLU regression.** This is why FP8 is the default for serious deployments in 2026, not an exotic option.

**Common confusions.**

- *"Quantize everything to INT4 and you're done."* — Attention computations require FP precision through the softmax. KV cache below FP8 starts losing quality on long contexts. Weight-only quant is safe; activation quant is harder; KV quant is hardest.
- *"Tensor Parallelism is always the right parallelism."* — Only inside a node. Across nodes, PP or EP wins. For very long contexts, Context Parallelism is the only viable approach.
- *"Disaggregation always wins."* — Only when prefill and decode have wildly different traffic shapes. For chat (short prompts, long generations) it's marginal. For RAG (long prompts, short answers) it's huge.

**How this connects to later weeks.** Week 8 lets you measure all of this on real hardware. Week 9 shows which modalities need which techniques (image gen lives on the compute-bound side, ASR on the streaming side, etc.).

Concept-graph anchors: `quantization`, `speculative-decoding`, `paged-attention`, `flash-attention`, `tensor-parallelism`, `moe`, `mla`, `disaggregated-serving`.

---

## A.6 Chapter 6 supplement — Other Modalities

**Why this matters.** LLMs get all the attention, but most production AI traffic is multi-modal. ASR for call centers, image gen for marketing, embeddings for search — these are *bigger* revenue lines than chat for many companies. The same six techniques apply with twists.

**Worked numerical example — image generation step budget.** SDXL at 1024×1024, 30 diffusion steps. Each step is one UNet forward pass ≈ 60 ms on H100 → **1.8 s/image baseline**. Apply guidance skipping (skip CFG on alternate steps): 25% faster → 1.35 s. Apply Context Parallelism across 4 H100s for the attention layers: another 2× → ~700 ms. Production target for "instant" image gen is ~1 s, so a single H100 with guidance skipping just barely meets it; for batch image gen you stick with one H100 per request; for premium latency you scale to TP=4. The math is what drives the productization choice.

**Worked numerical example — ASR Real-Time Factor.** Whisper-large-v3 on H100 transcribes 1 minute of audio in ~3 seconds → **RTF = 0.05** (20× faster than real-time). For real-time captioning you need RTF < 1 with low per-chunk latency. So you switch to streaming with 100 ms audio chunks and a smaller distilled model (Whisper-base or Distil-Whisper-large): RTF ≈ 0.02, chunk-latency ≈ 200 ms. Choosing model + chunking strategy is the entire ASR engineering job.

**Common confusions.**

- *"Image gen is compute-bound so we don't need batching."* — You still want batching for throughput, but the batch-size sweet spot is much smaller than for LLM decode.
- *"ASR is just an LLM with audio tokens."* — Architecturally close, but the encoder-decoder shape and the mel-spectrogram front-end change what optimizations apply.
- *"Embeddings are easy."* — Per-request they're easy. At Google-scale they're a separate engineering discipline (vector DBs, sharding, ANN indexes).

**How this connects to later weeks.** Week 10 production lessons apply identically to multi-modal serving — the autoscaler doesn't care if you're serving Llama or Whisper, but the right concurrency target differs.

Concept-graph anchors: see Glossary Appendix B.6 (Decode), B.18 (memory-bound vs compute-bound).

---

## A.7 Chapter 7 supplement — Production

**Why this matters.** A perfectly tuned single-GPU inference server that falls over at 100 concurrent users is worth zero dollars. Productionization is what separates a research demo from a business.

**Worked numerical example — autoscaler concurrency target.** Your engine runs continuous batching with batch size 32. You set Kubernetes HPA target = 80% CPU → wrong signal entirely (GPU is the bottleneck). You switch to target = `in-flight requests per pod = 24` (75% of max batch). New pod spins up when each existing pod hits 24 in-flight; spins down when it drops below ~12. Cold start time = 90 s (image pull + weight load). So you also pre-warm with a min replica count of 2. With this configuration P99 latency stays stable across a 10× traffic spike instead of cliff-falling. **The right concurrency-target metric is the single most-important production knob.**

**Worked numerical example — multi-cloud capacity arbitrage.** AWS p5 (H100) on-demand: ~$98/hr per 8-GPU node = $12.25/GPU-hr. Lambda Labs reserved H100: ~$2/GPU-hr. CoreWeave 1-year reserved H100: ~$2.50/GPU-hr. If you run 100 GPUs 24/7 for a year: AWS on-demand = ~$10.7M; reserved Lambda mix = ~$1.75M. **Multi-cloud savings: ~$9M/year on 100 GPUs.** This is why every serious AI infra team is multi-cloud, even when the engineering pain is real.

**Common confusions.**

- *"Scale to zero is always a cost win."* — For latency-sensitive consumer products, cold-start kills UX. Scale-to-zero only works for batch or async workloads.
- *"Container size doesn't matter."* — A 40 GB image takes 2+ minutes to pull on a fresh node. Slim images and cached layers shave 80% off cold-start.
- *"Logs alone are observability."* — You need metrics (per-pod TPS, GPU util, batch size, KV-cache occupancy), traces (request → kernel breakdown), AND logs. Missing any one of the three pillars makes incidents 10× harder.

**How this connects to later weeks.** This is the last chapter — it's where everything you've learned gets bolted together. The capstone problem set in Week 10 will ask you to size, deploy, and price-out a real inference service. Use the numbers in this section as your reference sheet.

Concept-graph anchors: `inference-cost`, `ai-stack-overview`.

---

## Appendix B — Cross-week study planner

A practical schedule for the night-before-an-exam reread. If you have only ~3 hours to review the whole course:

| Time | What to reread | Why |
|---|---|---|
| 0:00–0:20 | Six runtime techniques (Ch. 0) + Bottleneck cheatsheet (Quick Reference) | The spine of every exam question |
| 0:20–0:45 | Worked KV-cache + arithmetic-intensity examples (A.2) | The most-asked numerical questions |
| 0:45–1:10 | Hardware specs (A.3) + parallelism cheatsheet | Memorize HBM bandwidths and NVLink/IB ratio |
| 1:10–1:50 | Chapter 5 supplement (A.5) | The technique deep-dives that show up on the long-answer questions |
| 1:50–2:15 | Production knobs (A.7) | Cold-start, autoscale targets, multi-cloud arithmetic |
| 2:15–2:45 | Glossary Appendix B (extended entries) | Confirms vocabulary precision |
| 2:45–3:00 | Re-read your own problem-set notes from the worst-scoring week | This is always the highest-leverage 15 minutes |

If you have 30 minutes instead of 3 hours: only the rows in **bold** above (or just the Quick Reference card at the end of the main body).
