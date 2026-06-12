**Inference Engineering**

Course Glossary

*207 terms from Appendix A of Inference Engineering by Philip Kiely*

> **Source & permitted use.** This glossary is an instructor-authored companion derived from Appendix A of *Inference Engineering* by Philip Kiely (Baseten Books, 2026). Definitions are paraphrased and adapted for internal use within the Andhra University / Oxmiq curriculum only. **Do not redistribute, mirror, or publish outside this course.** Students and instructors should obtain the original book for canonical definitions and references. If a formal license or permission grant for this material is established, replace this notice with a pointer to the source agreement.

How to study with this glossary

This glossary contains all definitions from Appendix A of the book — the canonical reference for terminology. Use it three ways:

- **As a reference** — look up any term you encounter in lecture or in the book.

- **As a study tool** — read straight through once per week. Many terms gain meaning only after Chapter 5 or 6.

- **As a quiz prep aid** — pair with the Flashcards deliverable. The exams test your ability to use these terms, not just recite them.

A

**Activation function**

A (mostly) differentiable nonlinear function like ReLU inserted between linear layers to prevent multi-layer neural networks from collapsing into a single matmul.

**Active–active**

A high-availability posture where multiple regions/clusters actively serve live traffic at once. If any plane fails, traffic seamlessly continues on the others.

**Active–passive**

A failover posture where a "hot standby" cluster or region is kept ready but idle. If the active plane fails, traffic is cut over to the passive plane.

**Ada Lovelace (architecture)**

NVIDIA's graphics-oriented GPU architecture, released alongside Hopper in 2022. Useful for small models and cost-sensitive workloads, not suited for large-scale LLM inference.

**Agent**

An AI application that takes action rather than just providing information. Agent workflows usually rely on multiple inference calls, often across multiple models and modalities, and require access to tools.

**AI-native application**

A product where the core UX and value depend on generative models. Inference choices are downstream of app constraints: modality, latency budget, unit economics, and usage patterns.

**Ampere (architecture)**

An older NVIDIA GPU architecture still used in legacy or small-scale deployments. Hopper and Blackwell architectures generally outperform Ampere on both raw speed and cost at scale.

**Application Programming Interface (API)**

A structured interface for sending requests and receiving responses. Inference engines expose an API for making queries to models.

**Arithmetic intensity**

Operations performed per byte moved for a given algorithm. When compared to a GPU's ops:byte ratio, arithmetic intensity indicates whether a kernel is compute bound or memory bound.

**Attention**

The core transformer mechanism relating a token to prior tokens via Q/K/V projections and softmax. Attention is a primary target for optimization due to its compute and memory demands.

**Automatic Speech Recognition (ASR)**

Audio-in, text-out transcription models (e.g., Whisper). Decoder work dominates runtime and benefits from LLM-style optimizations and in-flight batching.

**Autoregressive token generation**

Iterative generation of tokens where each token depends on each previous token. Split into two phases: prefill (input tokens processed) and decode (output tokens generated).

**Autoscaling**

Scaling the number of replicas serving a given model up and down automatically based on traffic or utilization. Matches capacity to demand, maintaining latency SLAs and minimizing wasted spend.

**Autoscaling window**

The rolling time horizon used to decide scale-up/scale-down actions. Longer windows keep replica counts steady; shorter windows react faster to spikes.

B

**B200**

NVIDIA Blackwell-based datacenter GPU with 192 GB of VRAM, 8 TB/s of memory bandwidth, and 5 petaFLOPS of FP8 compute.

**B300**

NVIDIA Blackwell-based datacenter GPU with 288 GB of VRAM, 8 TB/s of memory bandwidth, and 5 petaFLOPS of FP8 compute.

**Bandwidth**

The amount of data per second that can pass through memory like VRAM or an interconnect like NVLink.

**Baselines**

Initial, carefully recorded measurements of performance and quality before applying optimizations. Baselines enable clear attribution of gains or regressions.

**Basic Linear Algebra Subprograms (BLAS)**

A standard interface for fundamental operations in linear algebra.

**Batch**

Process multiple inputs simultaneously, common for LLM inference.

**Batch sizing**

A core latency-throughput lever for inference engines. Larger batches improve total throughput but worsen per-user latency.

**Benchmark (intelligence)**

A measurement of a model's ability to answer questions correctly or take appropriate actions (e.g., MMLU).

**Benchmark (performance)**

A measurement of an inference service's latency and throughput for a given model with a defined workload.

**BF16**

A 16-bit floating-point format with larger exponent than FP16, useful in training and sometimes inference. Higher dynamic range helps preserve outliers.

**Bin packing (multi-cloud)**

Treating heterogeneous pools of GPUs across clouds, regions, and clusters as a single schedulable resource, enabled by multi-cloud capacity management infrastructure.

**Blackwell (architecture)**

NVIDIA's late-2024 GPU generation featuring FP4 support, microscaling formats (MXFP8, MXFP4, NVFP4), and high memory bandwidth.

**Blue-green deployment**

Two parallel production environments ("blue" and "green"); shift traffic between them for zero-downtime deploys and quick rollback.

C

**Cache-aware routing**

Steering requests to replicas that already hold matching prefixes or required LoRAs. Higher cache hit rates yield lower TTFT.

**Canary deployment**

A new production deployment that starts with a small share of live traffic to a new deployment to validate stability and performance. Over time, the new deployment absorbs all production traffic.

**Causal language model (CLM)**

A decoder-only transformer that predicts the next token given the prior context. All generative LLMs in this book are CLMs.

**Central Processing Unit (CPU)**

A general-purpose processor optimized for sequential workloads. CPUs are used for orchestration, scheduling, networking, and preprocessing, but rarely handle generative AI inference directly.

**Chat template**

The model-specific formatting and serialization of messages (roles, separators, beginning/end of sequence tokens).

**Chunked prefill**

Splits long inputs into chunks and overlaps prefill with decode or other work, preventing single long sequences from monopolizing resources.

**Classifier-free guidance**

Balances unconditional and prompt-conditioned denoising passes on each step of image generation. Lower guidance enhances creativity; higher guidance enforces prompt adherence.

**CLIP (text encoder)**

A text/image encoder used in earlier image pipelines (e.g., SDXL). Modern systems often swap in full LLMs for stronger prompt understanding.

**Closed model**

A proprietary model where weights are unavailable, like GPT-5, Claude Sonnet, or Google Gemini.

**Cold start**

The time from scaling a replica from zero to its first successful response (steps include GPU provisioning, container startup, model load, inference engine compilation).

**ComfyUI**

A workflow tool for assembling image pipelines (base model, refiner, LoRAs, ControlNets). Encourages modular, swappable components.

**Compute-bound**

An algorithm limited by available FLOPS rather than memory bandwidth. LLM prefill and image/video generation are usually compute bound.

**Context Parallelism (CP)**

Replicates weights across GPUs and partitions the attention context. Essential for video models where attention works across a massive latent space.

**Context window**

The maximum number of tokens that a model can process across input, reasoning, and output for a single request.

**Continuous batching (in-flight)**

Token-level interleaving of requests so GPU slots are always utilized. Minimizes per-user latency penalties of batching.

**Control plane (multi-cloud)**

Global orchestrator for deploying models and allocating resources.

**Core (CUDA)**

A general-purpose arithmetic unit that executes a wide range of scalar and element-wise operations.

**Core (Tensor)**

A specialized hardware unit optimized for mixed-precision matrix multiply-accumulate (MMA) operations. The most important type of compute for inference.

**Cross-attention**

Conditioning one sequence (Q) on another's K/V (e.g., text conditioning images). Common in multimodal and denoising pipelines.

**cuBLAS**

CUDA's BLAS implementation offering high-quality GEMM and related primitives.

**CUDA**

NVIDIA's programming model and platform for GPU kernels, graphs, memory, and execution.

**CUDA driver**

A low-level interface between the application and the GPU hardware to manage memory and execution.

**CUDA graph**

A directed acyclic graph (DAG) of kernels and other GPU operations for optimizing repeated workflows.

**CUDA kernel**

A user-defined function that executes parallelized code on the GPU.

**CUDA runtime**

A developer-facing API for launching kernels and managing memory.

**cuDNN**

Primitives for building deep neural networks in CUDA.

**CuTe**

A domain-specific C++ template library that abstracts tiled tensor operations to help developers compose precision-aware, hardware-optimized GEMM and fused kernels.

**CUTLASS**

A CUDA C++ template library that provides building blocks for writing high-performance, architecture-tuned GEMM and related kernels.

D

**Data sovereignty**

Legal constraints around where model inputs and outputs are processed and stored geographically.

**Decode**

The memory-bound phase of LLM inference where the autoregressive generation loop emits one token per forward pass.

**DeepGEMM**

A library of clean and efficient GEMM kernels created by the DeepSeek AI team with strong performance in FP8.

**Denoising model**

The heart of diffusion pipelines that iteratively refines latent noise into an image or video.

**Diarization**

Segmenting audio by speaker ("who spoke when"); often paired with VAD in ASR pipelines.

**Diffusers (library)**

Reference implementations for image and video generation pipelines.

**Disaggregation**

Separating prefill and decode onto independently scaling engines running on separate hardware resources.

**Distillation**

Training a smaller student to emulate a larger teacher model based on probability distributions, not just outputs, to retain model behavior on fewer parameters.

**Docker**

Containerization technology for building standardized packages of inference services with their dependencies.

**Dockerfile**

A human-readable file with well-specified, machine-interpretable instructions for creating an image.

**Dynamic batching**

Starts a batch when the batch is full or a short timer elapses, whichever comes first. Balances latency stability with utilization; superseded by continuous batching for LLMs.

**Dynamic range (quantization)**

The range of absolute values that can be represented in a number format. Floating-point numbers have a higher dynamic range than integers with the same number of bytes thanks to their exponent-mantissa structure.

E

**EAGLE (speculation)**

A small, purpose-built draft model trained to consume hidden states and propose multiple tokens for high acceptance rates in speculative decoding.

**Elo (quality meta-metric)**

Head-to-head win-rate style scoring to compare model quality. Useful directional signal beyond intelligence benchmarks.

**Embedding model**

Encodes text or image input into fixed-dimensional vectors for semantic similarity, used in RAG and agent memory. Modern variants often use LLM backbones and Matryoshka representations.

**Encoder**

Network that converts raw inputs into internal representations (e.g., audio features in Whisper). Paired with a decoder in encoder-decoder models.

**Evals**

Task-specific tests that mirror real-world use cases for a model, used for product-specific model intelligence testing.

**Expert Parallelism (EP)**

Shards experts of an MoE across GPUs; each GPU contains multiple full experts. Increases total throughput with low inter-GPU communication overhead.

F

**Few-step image generation**

Models that produce usable images in eight or fewer steps. 80-90% faster but with noticeable quality tradeoffs; strong fit for real-time applications.

**Feynman (architecture)**

A future NVIDIA generation after Rubin. Details are limited; expect continued emphasis on low-precision and memory bandwidth.

**Fine-tuning**

Adapts a pretrained base to a domain, often enabling much smaller models to meet quality needs.

**FlashAttention**

A series of optimized attention kernels that minimize memory traffic. FlashAttention 3 is written for Hopper, FlashAttention 4 targets Blackwell.

**Floating-point data formats**

Precisions like FP16, FP8, and FP4 used in inference with high dynamic range and an exponent-mantissa structure.

**FLOPS**

Floating-point operations per second, typically measured on Tensor Cores.

**Foundation model**

A model trained on broad data that serves as a base for multiple downstream tasks. Foundation models (e.g., GPT, Claude, Llama) are typically fine-tuned or used directly via prompting.

**Function calling**

Also known as tool calling or tool use, a model is given a set of available functions along with a prompt and returns a structured output including both selected functions and arguments for those functions.

G

**GB200**

An NVIDIA superchip that pairs a Grace CPU with a B200 GPU via high-bandwidth NVLink chip-to-chip connection. Used in rack-scale NVLink systems like the NVL72 and useful for KV cache offloading, LoRA swapping, and other techniques that benefit from NVLink-C2C.

**General matrix-matrix multiplication (GEMM)**

An algorithm in BLAS and the key operation for inference.

**Generative AI**

A class of models that, in contrast to predictive ML models, create new content across modalities (text, images, audio, video, code) by learning the underlying patterns of training data.

**Generative Pretrained Transformer (GPT)**

A family of large language models for text generation created by OpenAI.

**GH200**

An NVIDIA superchip that pairs a Grace CPU with an H200 GPU via high-bandwidth NVLink chip-to-chip connection. Useful for KV cache offloading, LoRA swapping.

**Goodhart's Law**

"When a measure becomes a target, it ceases to be a good measure."

**GPU node**

A standard chassis of 8 interconnected GPUs with NVLink and NVSwitch.

**Grace CPU**

ARM-based NVIDIA CPU with high-bandwidth chip-to-chip interconnects between the CPU and GPU. Used alongside Hopper and Blackwell GPUs.

**Graphics Processing Unit (GPU)**

A highly parallel processor originally designed for graphics rendering and now widely used for training and inference of generative AI models.

**gRPC**

Structured, schema-first bidirectional streaming protocol.

H

**Head (attention)**

One independent attention computation within a layer.

**High-Bandwidth Memory (HBM)**

The memory used for VRAM on datacenter GPUs. Recent generations include HBM3, HBM3e, and HBM4.

**Hopper (architecture)**

NVIDIA's 2022 GPU generation featuring FP8 support and async programming features.

**Hyperscaler**

Generalized cloud service providers like AWS and GCP.

I

**Image generation pipeline**

Foundation models for image generation are pipelines of multiple models: a text encoder, an iterative denoiser, and a VAE.

**Inference**

Serving AI models in production.

**Inference engine**

A high-performance runtime (vLLM, SGLang, TensorRT-LLM) with support for optimization techniques like batching, caching, quantization, and speculation.

**InfiniBand**

Inter-node interconnect for scaling inference and training across multiple nodes. Bandwidth is higher than alternatives like Ethernet but substantially lower than NVLink.

**Input sequence**

The tokens provided to a model as part of a request, processed during the prefill phase of inference.

**Input Sequence Length (ISL)**

The number of tokens in the input sequence for a given request.

**Instance (cloud)**

The provisioned virtual machine that includes GPU(s), CPU and RAM resources, storage, networking, and interconnect.

**Integer data formats**

Number formats like INT8 and INT4 with limited dynamic range.

**Inter-token latency (ITL)**

Time between generated tokens during decode. Converts to perceived TPS (e.g., 2 ms ITL equates to 500 TPS).

**In-flight batching**

See continuous batching. Token-level interleaving for high utilization with stable latency.

**Iterative denoising (diffusion)**

Start from noise and progressively refine into an image or video in latent space.

J

**Jitter (benchmark)**

Adding randomness to arrival times and sequence shapes to more closely mirror real traffic than uniform or bursty synthetic loads.

K

**Kernel fusion**

Taking two or more kernels and re-implementing them into a single kernel that handles both operations, avoiding unnecessary round-trips through memory.

**KV cache**

Stored K/V tensors for each token to avoid recomputing attention, turning the attention equation from a quadratic-time to a linear-time operation.

L

**L0/L1/L2 caches (GPU)**

On-chip cache memory hierarchy for instructions, shared memory, and global cache.

**Large Language Model (LLM)**

A type of generative AI model that takes a text prompt and returns a new sequence of text. Famous LLM families include GPT, Claude, Llama, and DeepSeek.

**Latency percentiles**

Measuring latency on a percentile basis (P50/P90/P95/P99) for awareness of both the average and the worst-case user experience.

**Latent consistency**

A few-step strategy that predicts target latents directly, possibly repeated for refinement. Very fast; lower fidelity than full diffusion.

**Latent space (images/videos)**

Lower-dimensional representation where denoising occurs (e.g., 128x128).

**Load testing**

Sending sustained high traffic to probe throughput limits, queue behavior, and autoscaling.

**Local (edge) inference**

Running inference on end-user devices like phones and computers.

**Logit biasing**

Nudging or constraining token probabilities to steer structured outputs (e.g., JSON/tool calls). Applied post-logits before sampling.

**Logits**

A vector of non-normalized probabilities, one per token in the model's vocabulary, generated in each forward pass during decode.

**Lookahead decoding**

Constructs n-grams during inference to enable draft token prediction without a separate model.

**LoRA**

Low-rank adaptation, a lightweight fine-tuning method that produces small changes to models. Inference services often need to swap between thousands of LoRAs for a single foundation model.

M

**Machine learning (ML)**

Predictive modeling for tasks like classification and trend forecasting, as opposed to generative AI which creates novel outputs.

**Matmul**

Matrix multiplication.

**Matryoshka representations (embeddings)**

Nested vector schemes allowing variable dimensionality where the early part of the vector encodes more semantic meaning. Allows tradeoffs between vector size and embedding quality.

**Medusa (speculation)**

Adds extra decoder heads via fine-tuning to generate multiple draft tokens per pass.

**Microscaling formats**

Floating-point data formats like MXFP8, MXFP4, and NVFP4 that use blockwise quantization with small-block scale factors (e.g., every 32 elements) to improve accuracy.

**Mixture of Experts (MoE)**

A model architecture where linear layers of weights are separated into sparse experts. A router activates a subset of experts for each forward pass.

**Model parallelism**

Splitting work across GPUs via Tensor, Expert, or Pipeline Parallelism. Parallelism strategy depends on model size, topology, and latency versus throughput goals.

**Multi-cloud capacity management**

A global scheduler placing workloads across providers and regions.

**Multi-Instance GPU (MIG)**

A capability in larger Ampere, Hopper, Blackwell, and Rubin GPUs where the GPU can be carved into up to eight slices of memory and seven slices of compute.

**Multi-node inference**

Scaling across two or more nodes using InfiniBand when one node of eight GPUs doesn't have enough VRAM for weights, activations, and KV cache. Requires appropriate parallelism strategies (PP or EP).

N

**Neocloud**

Specialized cloud service providers focused on GPUs like CoreWeave and Nebius.

**Neural audio codec**

A learned encoder that compresses audio into tokens and a paired decoder that turns tokens back into audio.

**NIM**

A pre-packaged, containerized microservice for a specific model created by NVIDIA.

**Node**

The physical 8-GPU base unit with NVLink/NVSwitch. Multi-node adds InfiniBand between nodes.

**NVFP4**

NVIDIA's 4-bit floating-point microscaling number format with dual scale factors and blockwise quantization with a block size of 16.

**NVIDIA Dynamo**

An open-source distributed serving platform for KV reuse, disaggregation, and multi-GPU/multi-node orchestration.

**NVL72**

A rack-scale Blackwell system interconnecting 72 GPUs and 36 CPUs. Purpose-built for serving very large models with extreme throughput.

**NVLink**

A one-to-one communication layer between GPUs, up to 1,800 GB/s on Blackwell and 900 GB/s on Hopper.

**NVSwitch**

An all-to-all communication layer on top of NVLink for coordination among all GPUs in a node.

**N-gram speculation**

Uses observed n-grams from prefill to propose long draft sequences during decode. Extremely effective for code completion.

O

**Offline inference**

Asynchronous batch processing of large jobs, optimized for throughput and cost over per-request latency.

**Omni-modal**

Models that accept multiple modalities of inputs (text, images, video, audio) and produce multiple modalities of output.

**Online inference**

Real-time serving of requests, optimized for tight latency budgets.

**ONNX**

An intermediate representation and runtime for models.

**Open model**

A model whose weights are freely available, like Llama, DeepSeek, or Whisper.

**Ops:byte ratio (GPU)**

Peak operations per byte of memory bandwidth for a GPU at a given precision. Compare with arithmetic intensity to diagnose bottlenecks.

**Output sequence**

The tokens generated by a model during the decode phase of inference.

**Output Sequence Length (OSL)**

The number of tokens in the output sequence generated by a model for a given request.

**Out-of-memory error (OOM)**

A common failure where the GPU runs out of VRAM to load weights or execute inference.

P

**PagedAttention**

An optimization for attention where KV blocks are stored in fixed-size pages to improve performance, especially with long context.

**PCIe (GPU form factor)**

A form factor for datacenter GPUs that uses standard PCI express slots for connection. PCIe GPUs often have lower base specs and fewer interconnect options than SXM variants of the same GPU.

**Perceived TPS**

Tokens per second observed by a single user during streaming output. A latency metric — what people usually mean when they say TPS.

**Pipeline Parallelism (PP)**

Splits layers into stages across GPUs. Acceptable for multi-node with dense models; introduces bubbles in the pipeline where some GPUs are idle while waiting for other steps to finish.

**Prefill**

The compute-bound phase of LLM inference where the input sequence is processed and the KV cache is built.

**Prefix caching**

Reuses KV for shared prefixes across requests to skip prefill. Majorly improves TTFT for code completion, multi-turn chat, and agents.

**Pretraining**

Large-scale (usually self-supervised) training on broad corpora to create a base model.

**Prompt**

The instruction to the model; for diffusion also includes a negative prompt and step/guidance parameters.

**PyTorch compile (torch.compile)**

Graph capture and kernel selection/fusion targeting a specific GPU. Cache compiled engines to cut cold-start times.

**PyTorch Profiler**

A developer tool measuring CPU and GPU time and memory per operation.

Q

**Quantization (post-training)**

Lowering precision of weights, activations, and potentially KV cache to reduce compute and memory bandwidth demands.

**Quantization-aware training (QAT)**

A training technique in which quantization scales are computed and weights are optimized jointly so that the final model is already calibrated for low-precision deployment.

**Queue (request)**

Holds excess traffic while autoscaling brings replicas online.

R

**Real-time factor (RTF)**

A measurement of how quickly ASR models can transcribe audio. Transcribing an hour of audio in six seconds is an RTF of 600.

**Retrieval-augmented generation (RAG)**

A common application pattern that fetches additional context for the LLM beyond the prompt.

**Ring attention**

A Context Parallelism mechanism in which GPUs pass partial attention results in a ring. Reduces all-to-all pressure for very large contexts.

**Roofline model**

Plots arithmetic intensity with bandwidth and compute ceilings, creating a visual guide on whether to optimize memory or compute.

**Rotary positional embeddings (RoPE)**

A positional encoding scheme that encodes positions as learned rotations, improving long-context extrapolation at the cost of higher memory demands for attention during inference.

**Routing (inference)**

Placing requests on replicas based on load, KV cache, available LoRAs, and sequence shapes to improve speed and utilization.

**Rubin (architecture)**

Next NVIDIA generation (2026) introducing HBM4 and CPX for compute-bound workloads.

S

**Sampling (decode)**

The process of selecting an output token based on the generated logits. Common strategies include greedy (argmax), temperature, top-k, and top-p (nucleus) sampling.

**Scale factor (quantization)**

Multipliers used to map low-precision values to their original number formats.

**Scale to zero**

Turn off all replicas when idle; spin up on demand. Requires fast cold starts and robust queueing; best for predictable or dev workloads.

**SDXL**

An instructive, earlier diffusion image pipeline (base + refiner + CLIP). Modern systems retain the structure with larger, more capable components.

**Service Level Agreement (SLA)**

A contractual promise of latency, throughput, uptime, or other performance factor from a system.

**Service Level Objective (SLO)**

An internal target designed to meet or beat the SLA for a given system.

**SGLang**

A fast inference engine with flexible frontend/backends and strong MoE support.

**Shadow traffic**

Mirroring real production requests to a candidate deployment.

**SNAC (audio decoder)**

A performant audio decoder path often paired with TTS token streams.

**Softmax**

Converts scores to probabilities in attention and normalizes logits to a probability distribution in decoding.

**Sparsity (FLOPS)**

In tensors with 2:4 structured sparsity, where 50% of the values are 0, Tensor Cores can skip multiplication by 0. Most inference is dense, not sparse.

**Special Function Unit (SFU)**

A dedicated hardware unit that accelerates specific math operations like sine and cosine, keeping specialized operations off of CUDA Cores.

**Speculative decoding**

A family of strategies for generating and validating draft tokens to generate multiple tokens per forward pass during decode.

**Streaming Multiprocessor (SM)**

GPU compute unit containing cores and cache.

**Structured output**

LLM output that adheres to a specific schema. Created by constraining generation to a supplied schema via logit biasing rather than via prompting.

**SXM (GPU form factor)**

A socketed GPU module that supports higher-bandwidth connections and delivers more power than PCIe. The standard for inference.

T

**Temperature**

Controls randomness in token selection: lower values (e.g., 0.1) make output more deterministic; higher values (e.g., 1.5) increase diversity.

**Tensor Parallelism (TP)**

Splits tensor operations across GPUs within a node. Best per-user latency; requires frequent all-reduce synchronization.

**TensorRT**

NVIDIA's optimized runtime for high-performance inference with fused kernels, quantization, and other optimizations.

**TensorRT-LLM**

An inference engine built by NVIDIA that provides a Python API and both TensorRT-engine and PyTorch-backend execution paths with fused kernels, quantization, and speculative decoding.

**Thread**

The minimal execution unit on a GPU. Kernels launch many threads to achieve massive parallelism.

**Throughput**

Total work per unit time (e.g., total tokens per second across the service).

**Time to first byte (TTFB)**

Time until first byte of output is returned, a latency metric.

**Time to first token (TTFT)**

Time until first token of output is returned, a latency metric.

**Token**

The atomic unit of text processing in LLMs. A token is an integer that represents a string of characters. In English, approximately a 4:3 token:word ratio for most tokenizers.

**Tokenizer**

Deterministically converts strings into sequences of tokens, and vice versa. Models have different tokenizers, and more efficient tokenizers improve end-to-end latency.

**Tokens per second (TPS)**

A latency metric for the number of tokens streamed to the end user per second. See perceived TPS.

**Training**

The process of learning model weights from data using backpropagation and optimization. Compute-intensive, typically runs on large GPU clusters, and produces the weights used in inference.

**Transformer**

The foundational architecture behind generative AI models.

**Transformers (library)**

Reference implementations for LLMs and other transformer-based models.

**Triton Inference Server**

A production serving framework by NVIDIA with support for multiple backends.

V

**VAE (variational autoencoder)**

Used in inference to decode from latent space to pixel space for image and video generation models (also used for encoding from pixel to latent space during training).

**Vector database**

A database for storing and querying the semantic vectors created by embedding models.

**Vector similarity**

A check between two vectors to see how close together they are based on an equation like cosine similarity. Vectors with high similarity encode similar semantic meaning.

**Vera CPU**

ARM-based NVIDIA CPU with high-bandwidth chip-to-chip interconnects between the CPU and GPU. Succeeds Grace alongside the Rubin GPU architecture.

**Vision-language model (VLM)**

Accepts images and video plus text prompts and outputs text.

**vLLM**

A widely adopted inference engine with broad model and hardware support and strong defaults.

**Vocabulary**

The total set of tokens, usually more than 100,000, that an LLM uses to represent data.

---

## Appendix B — Extended Entries

The short entries above are the canonical reference. The entries below go deeper on the highest-leverage terms: concrete examples with real numbers, common confusions, and cross-references. Use these when a topic feels hand-wavy after reading the short entry.

Each extended entry has four parts:

1. **Short def** — one line (a reminder; the long form is above).
2. **Why it matters / elaboration** — 2–4 sentences with a concrete worked example using real GPU specs or model sizes.
3. **Common confusion / what it is NOT** — the misunderstanding to head off.
4. **See also** — related glossary terms + concept IDs from `docs/kb/concepts.json`.

---

### B.1 — Arithmetic intensity

**Def.** Operations per byte of memory traffic, compared against the GPU's ops:byte ratio to decide compute- vs memory-bound.

**Elaboration.** Standard FP16 attention on H100 with N=4,096 tokens, head-dim d=128: total ops ≈ 34.5 GOps, memory traffic ≈ 545 MB → intensity ≈ 63 ops/byte. H100 FP16 ops:byte ≈ 295. Since 63 << 295, attention is **memory-bound** — the GPU's compute units sit idle waiting for HBM reads. At FP8 the intensity ~doubles to 126 ops/byte; still memory-bound (126 < 590 for H100 FP8) but you can now move data faster. This single calculation is *why* FlashAttention (fewer HBM reads) was such a leap.

**Common confusion.** "Higher intensity is always better." No — intensity itself isn't a goal. A *balanced* kernel (intensity ≈ ops:byte) is ideal; a memory-bound kernel at intensity 50 is fine if you can't make it cheaper to feed.

**See also.** Roofline model · Ops:byte ratio · Compute-bound · Memory-bound · concept `flash-attention`.

---

### B.2 — TTFT (Time to First Token)

**Def.** Latency from request submission to the user seeing the first generated token.

**Elaboration.** Dominated by prefill. A Llama-3 70B chat with a 1,300-token combined input (system prompt + chat history + question) on H100 takes ~200 ms to prefill → TTFT ≈ 200 ms. With prefix caching on the system prompt: TTFT drops to ~30 ms. Real-world targets: chat <500 ms (P95 <1s), code completion <100 ms (P99 <300 ms), long-context RAG can be 1–3 s and users tolerate it because they see the retrieval was substantial.

**Common confusion.** "TTFT is end-to-end latency." No — end-to-end also includes network RTT (10–100 ms), TLS, queueing at the load balancer, serialization, and client overhead. End-to-end is often 2–3× the on-GPU inference time.

**See also.** Prefill · ITL · Prefix caching · End-to-end latency · concept `latency-throughput`.

---

### B.3 — Inter-token latency (ITL)

**Def.** Time between consecutive output tokens during decode.

**Elaboration.** Drives *perceived* throughput per user: perceived TPS = 1000 / ITL (ms). Llama-3 70B on H100 with continuous batching: ITL ≈ 12 ms → ~83 TPS, smooth chat. Same model on an A10: ITL ≈ 50 ms → ~20 TPS, noticeably slow. Below ~30 TPS, users describe the output as "watching it type"; above ~100 TPS feels instant.

**Common confusion.** "ITL is the same as total TPS." No — ITL is per-user, measured in ms. Total system TPS scales with concurrent users. A system at 10,000 total TPS with 1,000 users gives each user 10 TPS — unusable.

**See also.** TTFT · Perceived TPS · Decode · concept `latency-throughput`.

---

### B.4 — KV cache

**Def.** Stored Key and Value tensors from prior tokens, reused so each new decode step is O(N) instead of O(N²).

**Elaboration.** For a 70B FP16 model at 8K context, KV ≈ 2.6 GB *per sequence* (formula: 2 × layers × hidden × bytes × seq_len). At 100 concurrent users averaging 200-token outputs, you can burn 18+ GB on KV alone — a serious chunk of a 40 GB A100. Three big optimizations exploit it: (1) prefix caching — reuse KV when requests share a prefix (system prompt, retrieved chunk); (2) FP8 KV quantization — halve per-request memory; (3) PagedAttention — page-based allocation eliminates fragmentation.

**Common confusion.** "KV cache size is part of model size." No — weights are a fixed cost (~2 GB per 1B params at FP16). KV cache is a *per-request* overhead that grows with context length. Mixing them up wrecks VRAM math.

**See also.** PagedAttention · Prefix caching · KV cache tiers · MLA · concept `kv-cache`.

---

### B.5 — Prefill

**Def.** The compute-bound phase that processes the entire input in parallel and builds the KV cache; drives TTFT.

**Elaboration.** A 2,000-token input on H100 takes ~150–250 ms to prefill. Compare to decode, which runs ~10 ms per token afterward. Prefill is *compute-bound* (lots of matmul on lots of tokens at once), decode is *memory-bound* (small matmul, but fetch every weight from HBM for each token). Their opposite bottlenecks are exactly why disaggregated serving puts prefill and decode on separate GPU pools.

**Common confusion.** "Prefill is always fast." Not for long contexts. A 100K-token RAG prefill can take 5+ seconds on a single H100. This is when you reach for prefix caching aggressively, or split prefill across GPUs with TP, or use chunked prefill.

**See also.** Decode · TTFT · Chunked prefill · Disaggregation · concept `paged-attention`.

---

### B.6 — Decode

**Def.** The memory-bound autoregressive phase generating one output token per forward pass; drives ITL and TPS.

**Elaboration.** Each decode step reads *all* model weights from HBM to generate one token. For a 70B FP16 model, that's ~140 GB of weight memory traffic per token — at 3.35 TB/s HBM bandwidth, the *minimum* possible ITL is ~42 ms regardless of compute speed. (Real ITL is lower because of multi-GPU TP and FP8 quant: 70B FP8 on TP-8 H100 → ITL ≈ 10–15 ms.) This bandwidth-bound nature explains why FP8 weights give a big decode speedup (halve the bytes per token).

**Common confusion.** "Decode benefits from a faster Tensor Core." Marginally. Decode benefits from *less memory traffic* — quantization, KV cache compression (MLA), and smaller models help more than raw FLOPS.

**See also.** Prefill · ITL · Memory-bound · Quantization · concept `kv-cache`.

---

### B.7 — Quantization

**Def.** Lowering numeric precision (weights, activations, KV cache) to shrink memory and speed up compute.

**Elaboration.** FP16→FP8 roughly halves weight memory *and* halves memory-bandwidth pressure *and* gives ~2× Tensor Core FLOPS. A 280B model that needs 8× H100s at FP16 fits on 4× H100s at FP8 (or 8× at FP8 with longer context). Default sensitivity ranking (least → most painful to quantize): weights < activations < KV cache < attention softmax. FP8 weights: usually zero perceptible quality loss. FP4 weights: requires careful eval, often needs QAT or sophisticated calibration (NVFP4 / MXFP4 microscaling helps).

**Common confusion.** "Quantization always hurts quality." FP8 typically shows **zero** loss on standard evals (the model is non-deterministic anyway). FP4 *can* hurt. Also: "INT8 and FP8 are interchangeable." No — FP8 has an exponent for dynamic range, INT8 clips outliers, which destroys attention softmax.

**See also.** FP8 · NVFP4 · MXFP8 · PTQ · QAT · concept `quantization`.

---

### B.8 — Continuous batching (in-flight batching)

**Def.** Token-level interleaving of requests: a completed request frees its slot immediately, and new requests join mid-flight without waiting for a batch to close.

**Elaboration.** Replaces static batching (wait for the batch to fill or time out, then run all together — every early-arriving request pays the waiting cost). With continuous batching, throughput goes up *and* latency goes down at the same time. It's the single biggest serving-engine improvement of the last few years and is the default in vLLM, SGLang, and TensorRT-LLM. The catch: scheduler is complex; you can't easily reason about per-request VRAM cost ahead of time.

**Common confusion.** "Continuous batching is the same as just running everything in parallel." No — there's still a max batch size (limited by KV cache memory). The win is at the *scheduling* layer: tokens are the scheduling unit, not requests.

**See also.** PagedAttention · Batch sizing · Disaggregation · concept `continuous-batching`.

---

### B.9 — PagedAttention

**Def.** KV cache stored in fixed-size virtual pages with a lookup table, so variable-length sequences don't cause memory fragmentation.

**Elaboration.** The analogy is OS virtual memory. Without paging: you allocate max_seq_len worth of KV per request, then waste 90% when most requests are short. With paging: only allocate pages as the sequence grows. vLLM's original killer feature; now standard across engines. Combined with continuous batching, lets you safely overcommit KV memory and discover the right cap by hitting it.

**Common confusion.** "PagedAttention is a model architecture." No — it's a serving-engine memory-management technique. The model is unchanged; only how the inference engine allocates KV memory changes.

**See also.** KV cache · Continuous batching · vLLM · concept `paged-attention`.

---

### B.10 — FlashAttention

**Def.** IO-aware attention kernel that tiles the computation in SRAM to minimize HBM reads/writes.

**Elaboration.** Standard attention reads Q, K, V from HBM, writes intermediate scores back, reads them again for softmax, writes again. FlashAttention fuses the whole operation: keep tiles in SRAM, never write intermediates to HBM. Same math, ~2–4× faster on long sequences. FA-3 targets Hopper, FA-4 targets Blackwell. Almost every modern inference engine uses it by default; you should *never* be doing naive attention in production.

**Common confusion.** "FlashAttention is a different attention algorithm (so it changes accuracy)." It's the *same* attention — just a smarter implementation that respects the memory hierarchy. Mathematically equivalent.

**See also.** Arithmetic intensity · Memory-bound · SRAM · concept `flash-attention`.

---

### B.11 — Speculative decoding

**Def.** A small draft model proposes N tokens; the target model verifies them all in one parallel forward pass.

**Elaboration.** When the draft is right (acceptance rate >70%), you get N+1 tokens per forward pass instead of 1 — roughly 1.5–2× decode speedup. Three flavors: (1) **draft-target** (separate small model from the same family — easiest, highest overhead), (2) **EAGLE** (small dedicated draft trained on target's hidden states — production go-to), (3) **Medusa** (extra decoder heads on the target — 2–4 draft tokens). For repetitive content like code, n-gram speculation (no model at all, just a dictionary) often beats them.

**Common confusion.** "Speculation always helps." No — it consumes spare GPU compute. Under high batch load, compute is already saturated and speculation *steals* cycles from real tokens, slowing everything down. Turn off at high concurrency; turn on at low.

**See also.** EAGLE · Medusa · N-gram speculation · Acceptance rate · concept `speculative-decoding`.

---

### B.12 — Mixture of Experts (MoE)

**Def.** Architecture where each layer holds N expert sub-networks; a router activates a small subset per token.

**Elaboration.** Qwen3-235B-A22B has 235B total parameters but only 22B *active* per token. Serving cost is closer to a dense 22B model on compute, but VRAM footprint is closer to a dense 235B (you still need to store every expert). Cheaper *per token*, expensive *per GPU*. Expert Parallelism (EP) shards experts across GPUs to avoid duplicating weights; communication is naturally low because different requests activate different experts.

**Common confusion.** "MoE is always cheaper than dense." Only on compute per token. On VRAM, MoE often costs *more* than the equivalent-quality dense model. The trade-off is workload-dependent: many small requests favor MoE, few long requests favor dense.

**See also.** Expert Parallelism · Dense model · Router · MLA · concept `moe`.

---

### B.13 — MLA (Multi-head Latent Attention)

**Def.** Attention variant that compresses K and V via low-rank projection, slashing KV cache memory.

**Elaboration.** Introduced by DeepSeek-V2/V3. Standard MHA stores full K, V per token; MLA stores a small latent vector and reconstructs K/V on demand. KV cache footprint drops 10–100×, making long-context cheap. Trade: requires architectural buy-in at training time — you can't retrofit MLA onto a model trained with standard MHA. Engine support is the gating factor as of 2025; check that your vLLM/SGLang/TRT-LLM version handles MLA before adopting.

**Common confusion.** "MLA is a quantization technique." No — it's an *architectural* change to attention. It compresses K and V via a learned projection, not by lowering precision. Often combined with quantization for compounding gains.

**See also.** KV cache · Self-attention · DeepSeek · concept `mla`.

*(New entry — not in the short reference above; add to your study list.)*

---

### B.14 — Tensor Parallelism (TP)

**Def.** Each layer's weights (matrices) are sharded across GPUs; each GPU computes a partial result and all-reduces.

**Elaboration.** Lowest *latency* multi-GPU strategy because all GPUs work on the same request in lockstep. Communication is the cost: all-reduce after every parallelized layer. NVLink at 900 GB/s (Hopper) keeps this manageable inside one 8-GPU node; across nodes on InfiniBand at 400 Gb/s, all-reduce dominates and TP stops paying off. Rule: TP inside a node; PP/EP across nodes.

**Common confusion.** "More TP is always faster." Up to a point. TP-8 inside a node is great; TP-16 across two nodes is usually worse than TP-8 + PP-2 because of inter-node communication cost.

**See also.** Pipeline Parallelism · Expert Parallelism · NVLink · All-reduce · concept `tensor-parallelism`.

---

### B.15 — Disaggregated serving (prefill–decode disaggregation)

**Def.** Run prefill (compute-bound) on one GPU pool and decode (memory-bound) on another, transferring KV between them.

**Elaboration.** Notation: 5P3D = 5 prefill engines + 3 decode engines for one model. Each pool can be sized for its own bottleneck — prefill wants compute (B200 / H100 with strong FLOPS), decode wants bandwidth (H200 with 4.8 TB/s HBM). Overhead: KV must be transferred between pools when prefill finishes and decode starts. Worth it above roughly ~100M tokens/day on one model; below that, the routing overhead exceeds the contention savings.

**Common confusion.** "Disaggregation is the same as continuous batching." They solve different problems. Continuous batching solves *within-replica* GPU under-utilization. Disaggregation solves *prefill vs. decode contention*. Both can be on simultaneously.

**See also.** xPyD notation · Conditional disaggregation · Continuous batching · concept `disaggregated-serving`.

---

### B.16 — Inference engine

**Def.** The runtime that takes a model + serving config + requests and produces a stream of tokens.

**Elaboration.** Implements batching, KV cache management, paged attention, scheduling, quantization, speculative decoding. The three industry-standard choices: **vLLM** (most-used, broadest hardware portability, easy MoE), **SGLang** (cutting-edge MoE, strong DeepSeek/Kimi support, multi-modal), **TensorRT-LLM** (peak perf on Hopper/Blackwell, native NVFP4, harder to operate). Selection criteria: model family compatibility (does it support your model out-of-the-box?), hardware availability, ops sophistication you have.

**Common confusion.** "vLLM is always the right default." Often, but not always. For NVFP4 inference on Blackwell, TRT-LLM still leads. For some MoE models, SGLang ships day-zero support that vLLM hasn't caught up to.

**See also.** vLLM · SGLang · TensorRT-LLM · NVIDIA Dynamo · concept `inference-engines`.

---

### B.17 — Inference cost

**Def.** Per-token cost is the vendor metric; per-*completed-task* cost is the business metric.

**Elaboration.** A "cheap" model at $0.10/M tokens that takes 3 tries to produce a usable answer can cost more than a "premium" model at $3/M tokens that gets it right first try. Reasoning models multiply this — they consume thinking tokens nobody sees. The right denominator is *resolved tickets*, *merged PRs*, *correct extractions* — whatever your product produces. Industry trend: cost-per-token drops ~10× per year (Epoch AI / a16z 2025), so don't over-optimize for today's prices, but *do* measure cost-per-task today because it doesn't follow the curve uniformly.

**Common confusion.** "Cheaper per token = cheaper to serve." Only true at constant task quality. Without an eval, $/token comparisons are meaningless.

**See also.** Evals · Reasoning model · Goodhart's Law · concept `inference-cost`.

---

### B.18 — Memory-bound vs. compute-bound

**Def.** Two ends of the kernel-performance spectrum, decided by arithmetic intensity vs. ops:byte ratio.

**Elaboration.** LLM prefill: compute-bound (lots of math per byte moved). LLM decode: memory-bound (whole model read for one token). Image/video gen: usually compute-bound (heavy convolutions/attention per pixel). The fix for memory-bound: reduce memory traffic (FlashAttention, quantization, kernel fusion, smaller activations). The fix for compute-bound: faster Tensor Cores, larger batch, more parallelism. Don't apply memory-bound fixes to compute-bound problems — they won't help.

**Common confusion.** "If I'm not maxing out my GPU's FLOPS, it's a compute problem." Backwards. If FLOPS are idle, you're probably *memory-bound* — the compute is waiting for data. Profile before optimizing.

**See also.** Arithmetic intensity · Roofline model · FlashAttention · concept `flash-attention`.

---

### B.19 — Prefix caching

**Def.** Reuse KV cache across requests that share a common prefix (system prompt, retrieved chunk, prior turns).

**Elaboration.** A 1,000-token system prompt served 1M times/day at FP8 prefill cost: roughly $1,000/day in input compute. With prefix caching: ~95% of that becomes a cache hit → ~$950/day saved on prefill alone, plus a TTFT collapse from 100s of ms to <30 ms. Works best with cache-aware routing (pin a conversation to the same replica) — otherwise a follow-up turn lands on a cold replica and the value evaporates.

**Common confusion.** "Prefix caching is automatic and always on." Most engines support it but the *router* must cooperate. If users round-robin across replicas, cache hit rate stays low.

**See also.** Cache-aware routing · KV cache · TTFT · concept `kv-cache`.

---

### B.20 — Cold start

**Def.** Time from launching a replica from zero to its first successful response.

**Elaboration.** A naive cold start can take 5+ minutes: container pull (1+ min), model weights download from registry (2+ min for a 70B), inference-engine compilation (1–3 min for TRT-LLM), CUDA context init. Optimized: slim containers (no dev deps), pre-cached compiled engines, weights stored on local NVMe near the GPU → 30–60 s. Critical for *scale-to-zero* deployments and for autoscaling lead time. Rule: if traffic doubles every X minutes and cold start is Y seconds, you need to launch replicas X minutes before you need them.

**Common confusion.** "Cold start only matters for dev/test." False — it dictates how aggressively production can scale up. A 4-minute cold start makes traffic spikes impossible to track.

**See also.** Autoscaling · Scale to zero · NIM · concept `inference-engines`.

---

### B.21 — Autoscaling

**Def.** Adjusting replica count automatically based on traffic, utilization, or queue depth.

**Elaboration.** Use *multiple* signals: GPU utilization (lagging, smooth) for steady-state, incoming RPS or queue depth (leading) for spikes. CPU utilization is a trap on GPU servers — CPU is mostly idle Python orchestration regardless of GPU load. Lead time is the killer: if cold start is 90 s and traffic doubles every 30 min, you must scale up *before* utilization is high, not after. Predictive autoscaling (time-of-day patterns, calendar events) beats reactive autoscaling for known traffic shapes.

**Common confusion.** "Autoscale on CPU%." Almost always wrong for GPU workloads. Use GPU utilization and queue depth.

**See also.** Cold start · Scale to zero · Autoscaling window · concept `inference-cost`.

---

### B.22 — Latency percentiles (P50, P90, P95, P99)

**Def.** Latency at the 50th/90th/95th/99th percentile of requests. P50 = median, P99 = worst 1%.

**Elaboration.** Means are a trap. A service with mean 200 ms but P99 of 5 s feels broken — every 100th request hangs. SLAs should be on P95 or P99, never on mean. Healthy ratio: P99/P50 should be <5×. If you see 10× or worse, investigate: static batching timeout? cold compile on rare input shapes? a single replica running degraded?

**Common confusion.** "P99 latency is the worst 1%." Yes — and that's exactly the experience your power users see, because they hit you 100× a day. P99 is *user-perceived reliability*.

**See also.** TTFT · ITL · End-to-end latency · concept `latency-throughput`.

---

### B.23 — Reserved / on-demand / spot

**Def.** Three GPU pricing tiers: reserved (long-term commitment, discounted), on-demand (flexible, standard price), spot (pre-emptible, deeply discounted).

**Elaboration.** Production architectures *mix* all three. Reserved covers the predictable baseline (say, 60% of average traffic). On-demand handles known peaks (business hours). Spot handles offline/batch/restartable work (overnight evals, embedding backfills). Spot can be 60–80% cheaper but pre-emptions hit on short notice (minutes). Run nothing latency-critical on spot.

**Common confusion.** "Spot is cheap so use it for everything." Pre-emptions during user traffic = bad. Spot is for work that can be restarted without user-visible impact.

**See also.** Hyperscaler · Neocloud · Bin packing · concept `inference-cost`.

---

### B.24 — Active–active vs. active–passive

**Def.** Multi-region posture: active–active runs live in N regions; active–passive keeps a hot standby idle.

**Elaboration.** Active–active doubles GPU spend (both regions provisioned for peak) but failover is transparent — users notice nothing. Active–passive saves money but failover takes 10s of seconds, sometimes minutes (DNS propagation, warm-up). Consumer chat: active–active. Batch / B2B / dev: active–passive. Geo-aware load balancing on top is roughly 5 ms per time zone — route users to the nearest active region for the latency win on top of the reliability win.

**Common confusion.** "Active–active is always better." Cost. For a service serving 100 RPS, doubling GPU bill to insure against a rare outage may not be the right trade.

**See also.** Failover · Geo-aware load balancing · Multi-cloud · concept `inference-cost`.

---

### B.25 — Cost per completed task (vs. cost per token)

**Def.** The business unit for inference economics: dollars spent to produce one *useful output*, not one token.

**Elaboration.** A code-review agent that costs $0.50 per resolved PR review is what the business reasons about — not the $0.001/1K tokens its 12 LLM calls used. Lets you compare incomparable architectures: a cheap-model-chain that retries 3× vs. a premium-model one-shot. Required denominator when evaluating reasoning models (thinking tokens are invisible to users but cost real money). Track per-task cost as a top-line metric next to latency and quality.

**Common confusion.** "Per-token is the right metric because that's what vendors charge." Vendors charge per token because that's what they meter. Your business charges per task delivered.

**See also.** Inference cost · Evals · Reasoning model · concept `inference-cost`.

---

### Cross-reference map — extended entries vs. concept graph

| Concept ID (concepts.json) | Extended entry |
|---|---|
| `inference-vs-training` | (covered in short entry only; see *Inference* and *Training*) |
| `token` | (short entry; see *Token* and *Vocabulary*) |
| `context-window` | (short entry) |
| `temperature` | (short entry; see *Temperature*, *Top-k*, *Top-p*) |
| `latency-throughput` | B.2 TTFT · B.3 ITL · B.22 Latency percentiles |
| `transformer-architecture` | (short entry; see *Transformer* and *Attention*) |
| `self-attention` | B.10 FlashAttention (related) |
| `kv-cache` | B.4 KV cache · B.19 Prefix caching |
| `flash-attention` | B.10 FlashAttention · B.1 Arithmetic intensity · B.18 Memory- vs compute-bound |
| `moe` | B.12 MoE |
| `mla` | B.13 MLA *(new)* |
| `gpu-memory-hierarchy` | B.18 Memory- vs compute-bound |
| `gpu-generations` | (short entries: *Hopper*, *Blackwell*, *H100*, *H200*, *B200*) |
| `cuda-stack` | B.16 Inference engine |
| `inference-engines` | B.16 Inference engine · B.20 Cold start |
| `continuous-batching` | B.8 Continuous batching · B.5 Prefill · B.6 Decode |
| `paged-attention` | B.9 PagedAttention |
| `quantization` | B.7 Quantization |
| `speculative-decoding` | B.11 Speculative decoding |
| `tensor-parallelism` | B.14 Tensor Parallelism |
| `disaggregated-serving` | B.15 Disaggregated serving |
| `inference-cost` | B.17 Inference cost · B.21 Autoscaling · B.23 Reserved/on-demand/spot · B.24 Active–active · B.25 Cost per completed task |
