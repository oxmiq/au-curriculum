**Inference Engineering Flashcards**

208 study cards across two decks:

- **Deck A — Recall (cards 1–104):** definitions and core facts. Sit-down review.
- **Deck B — Application, discrimination & numbers (cards 105–208):** scenarios, "what's the difference between X and Y", and back-of-envelope math. Quiz a partner.

> **Source & permitted use.** These flashcards are an instructor-authored companion derived from *Inference Engineering* by Philip Kiely (Baseten Books, 2026). Card content paraphrases and adapts material from that book for internal use within the Andhra University / Oxmiq curriculum only. **Do not redistribute, mirror, or publish outside this course.** Students and instructors should obtain the original book for canonical text, code samples, and references. If a formal license or permission grant for this material is established, replace this notice with a pointer to the source agreement.

*Print double-sided, flip on long edge. Cut along grid lines.* Each page has 4 cards in a 2×2 grid; the back of each front-page card holds the matching definition.

Coverage: every Inference-phase concept node from `docs/kb/concepts.json` appears in at least one card. Several appear in 3+ (different angles).

|                                |                            |
|:------------------------------:|:--------------------------:|
|         **Inference**          | **Training vs. inference** |
| **The three inference layers** | **Six runtime techniques** |

|  |  |
|:--:|:--:|
| Training learns weights from data (one-time, capital expense). Inference uses those weights at runtime (continuous, operational expense). | Serving AI models in production — using trained weights to answer user requests. |
| Batching · Caching · Quantization · Speculation · Parallelism · Disaggregation. | Runtime (single instance), Infrastructure (scaling, multi-cloud), Tooling (developer abstraction). |

|                               |                        |
|:-----------------------------:|:----------------------:|
|           **TTFT**            |   **Perceived TPS**    |
| **Inter-token latency (ITL)** | **P50, P90, P95, P99** |

|  |  |
|:--:|:--:|
| Tokens per second observed by one user during streaming. Driven by decode (memory-bound). | Time to First Token. Latency metric, driven by prefill (compute-bound). |
| Latency percentiles. P50 = median; P99 = 99% of requests faster (1 in 100 slower). Optimize P99 for user-facing reliability. | Time between consecutive tokens. Formula: perceived TPS = 1000 / ITL (ms). |

|                                        |                            |
|:--------------------------------------:|:--------------------------:|
| **Inference time vs. end-to-end time** | **Online vs. offline app** |
|   **Shared vs. dedicated inference**   |      **Fine-tuning**       |

|  |  |
|:--:|:--:|
| Online: user waiting, optimize latency. Offline: batch jobs, optimize throughput. | Inference time = on-GPU time only. End-to-end time = what user experiences (includes network, queueing, client). |
| Adapt a pretrained foundation model to a domain by training on new data. Same architecture, new weight values. | Shared: public API, pay per token, zero ops. Dedicated: rented GPUs, pay per hour, full control. Switch when scale economics flip or specialization needed. |

|                    |                  |
|:------------------:|:----------------:|
|  **Distillation**  |    **Evals**     |
| **Goodhart's Law** | **Linear layer** |

|  |  |
|:--:|:--:|
| Task-specific tests that mirror your product's real use cases. Used to confirm a model is useful and to establish a baseline before optimizing. | Train a smaller student model to emulate a larger teacher's probability distributions. Different (smaller) architecture. |
| Simplest neural layer: y = xW + b. Matrix multiplication plus bias. | "When a measure becomes a target, it ceases to be a good measure." Why public benchmarks get gamed and you need product-specific evals. |

|                         |                                          |
|:-----------------------:|:----------------------------------------:|
| **Activation function** |              **Tokenizer**               |
|       **Logits**        | **Greedy / temperature / top-k / top-p** |

|  |  |
|:--:|:--:|
| Maps strings to integer IDs deterministically. Vocabulary typically \>100K tokens. ~4:3 token:word ratio in English. | Non-linear, mostly-differentiable function inserted between linear layers (ReLU, SwiGLU). Prevents collapse of stacked matmuls. |
| Sampling strategies. Greedy = argmax (deterministic). Temperature scales logits. Top-k keeps highest k. Top-p (nucleus) keeps smallest set summing to p. | Vector of unnormalized scores (one per vocab token) emitted by the LM head. Softmax → probabilities → sample. |

|                       |                          |
|:---------------------:|:------------------------:|
|      **Prefill**      |        **Decode**        |
| **Attention formula** | **Multi-head attention** |

|  |  |
|:--:|:--:|
| Memory-bandwidth-bound phase: generate one output token per forward pass autoregressively. Drives TPS. | Compute-bound phase: process all input tokens in parallel, build the KV cache. Drives TTFT. |
| Multiple independent attention computations in parallel — each head specializes in different relationships. | Attention(Q,K,V) = softmax( QK^T / √d_k ) V. Q = query, K = keys (prior), V = values (prior), d_k = head dim. |

|                              |                         |
|:----------------------------:|:-----------------------:|
| **Self vs. cross-attention** |      **KV cache**       |
| **Mixture of Experts (MoE)** | **Iterative denoising** |

|  |  |
|:--:|:--:|
| Stored K and V for each prior token. Turns attention from O(N²) to O(N). Lives on GPU memory by default. | Self: Q, K, V from same sequence (LLMs). Cross: Q from one sequence, K/V from another (e.g., image gen conditioning on text). |
| Image/video gen archetype: start from random noise in latent space, refine over ~50 steps. | Linear layers split into many sparse experts; a router activates a few per token. e.g., Qwen3-235B-A22B: 22B active of 235B total. |

|                  |                              |
|:----------------:|:----------------------------:|
| **Latent space** | **Classifier-free guidance** |
|     **VAE**      |   **Arithmetic intensity**   |

|  |  |
|:--:|:--:|
| Each denoising step runs 2 passes (with prompt + without), combined by guidance scale. 50 steps × 2 = 100 forward passes. | Low-dimensional representation (e.g., 128×128 for a 1024×1024 image) where denoising happens. ~1% of pixel space. |
| Ops per byte of memory traffic for a specific kernel. Compare to GPU's ops:byte ratio to diagnose compute- vs memory-bound. | Variational autoencoder. Decodes denoised latent into pixel-space image. |

|                            |                    |
|:--------------------------:|:------------------:|
|     **Ops:byte ratio**     | **Roofline model** |
| **Three core bottlenecks** | **FlashAttention** |

|  |  |
|:--:|:--:|
| Visualization of arithmetic intensity vs. bandwidth & compute ceilings. Shows whether to optimize memory or compute. | GPU peak compute / memory bandwidth. H100 FP16 ≈ 295. If kernel intensity \> ops:byte → compute-bound; \< → memory-bound. |
| Lossless optimized attention kernel that minimizes HBM reads/writes. FA-3 = Hopper, FA-4 = Blackwell. | LLM prefill = compute-bound. LLM decode = memory-bound. Image/video gen = compute-bound. |

|                                   |                              |
|:---------------------------------:|:----------------------------:|
|        **PagedAttention**         | **Sliding-window attention** |
| **Streaming Multiprocessor (SM)** |       **Tensor Core**        |

|  |  |
|:--:|:--:|
| Lossy variant: each token attends only to a window of w previous tokens. O(N²) → O(Nw). | Partitions KV cache into fixed-size pages accessed by lookup table. Reduces VRAM fragmentation. |
| GPU hardware unit for matrix multiply-accumulate (MMA): D = A×B + C. The most important compute for inference. | GPU compute unit. Contains Tensor Cores, CUDA Cores, SFUs, and L1 cache. |

|               |                              |
|:-------------:|:----------------------------:|
| **CUDA Core** |           **HBM**            |
| **L2 cache**  | **FLOPS — dense vs. sparse** |

|  |  |
|:--:|:--:|
| High-Bandwidth Memory. GPU VRAM. Generations: HBM3, HBM3e, HBM4 (Rubin). | General-purpose scalar arithmetic unit on a GPU. |
| Inference uses dense FLOPS. Sparse (2:4 sparsity) Tensor Cores can skip zeros but is uncommon in inference. | Global on-chip GPU cache shared across all SMs. 50 MB on H100. |

|          |            |
|:--------:|:----------:|
| **H100** |  **H200**  |
| **B200** | **NVLink** |

|  |  |
|:--:|:--:|
| Hopper, 141 GB HBM, 4.8 TB/s bandwidth. Better for memory-bound decode. | Hopper, 80 GB HBM, 3.35 TB/s bandwidth, 989 TFLOPS FP16 / 1,979 FP8. Today's workhorse. |
| GPU-to-GPU interconnect within a node. 900 GB/s on Hopper, up to 1,800 GB/s on Blackwell. | Blackwell, 192 GB HBM, ~8 TB/s, ~5 PFLOPS FP8. Adds FP4 and microscaling formats. New gold standard. |

|              |                |
|:------------:|:--------------:|
| **NVSwitch** | **InfiniBand** |
|   **Node**   |    **MIG**     |

|  |  |
|:--:|:--:|
| Inter-node interconnect, up to 400 Gb/s per NIC. Much slower than NVLink — shapes parallelism choices. | All-to-all communication layer on top of NVLink. Connects all GPUs in a node. |
| Multi-Instance GPU. Splits one GPU into up to 7 compute slices / 8 memory slices for serving small models. | Standard 8-GPU chassis with NVLink + NVSwitch. |

|                   |                    |
|:-----------------:|:------------------:|
|     **NVL72**     |  **CUDA kernel**   |
| **Kernel fusion** | **cuBLAS / cuDNN** |

|  |  |
|:--:|:--:|
| User-defined function that runs in parallel on the GPU. NVIDIA's GPU programming primitive. | Rack-scale Blackwell system with 72 GPUs + 36 Grace CPUs, all on NVLink. |
| NVIDIA's linear algebra and deep-learning primitive libraries. | Combine multiple kernels into one to avoid HBM round-trips. Critical for memory-bound decode. |

|                 |                |
|:---------------:|:--------------:|
|    **GEMM**     | **FlashInfer** |
| **safetensors** |    **ONNX**    |

|  |  |
|:--:|:--:|
| Library of optimized attention + sampling kernels for LLM inference. | General Matrix-Matrix Multiplication. The dominant operation in inference. Implemented in cuBLAS. |
| Open Neural Network Exchange. Stores weights + execution graph. Portable across hardware. | Hugging Face's safe weight-storage format. Doesn't execute arbitrary code on load (unlike pickle). |

|                  |                   |
|:----------------:|:-----------------:|
|     **vLLM**     |    **SGLang**     |
| **TensorRT-LLM** | **NVIDIA Dynamo** |

|  |  |
|:--:|:--:|
| Inference engine with strong MoE support (DeepSeek, Kimi). Flexible frontend language. Supports image/video gen. | Most widely-used inference engine. Broadest hardware support (NVIDIA, AMD, Intel, TPU). Easy to use. |
| Distributed serving system that orchestrates across replicas. Works with vLLM, SGLang, TRT-LLM as backends. KV reuse, disaggregation, multi-node. | NVIDIA's high-performance inference engine. Best raw perf on Hopper/Blackwell, NVFP4-native. Harder to use. |

|                |                                       |
|:--------------:|:-------------------------------------:|
| **FP8 (E4M3)** |           **MXFP8 / MXFP4**           |
|   **NVFP4**    | **Why float beats int for inference** |

|  |  |
|:--:|:--:|
| Microscaling 8-bit / 4-bit formats. Block of 32 values share a scale factor → better outlier preservation. | 8-bit floating point. Sweet spot for inference quality + perf. 4-bit exponent + 3-bit mantissa + 1 sign bit. |
| Floats have an exponent → dynamic range to preserve outliers. Integers clip outliers, hurting attention quality. | NVIDIA's 4-bit format. Block of 16 + global 32-bit scale factor. Highest granularity 4-bit option. |

|                          |                                           |
|:------------------------:|:-----------------------------------------:|
|     **PTQ vs. QAT**      | **Component sensitivity to quantization** |
| **Speculative decoding** |       **Draft-target speculation**        |

|  |  |
|:--:|:--:|
| Least → most sensitive: weights → activations → KV cache → attention. Softmax is almost always left in original precision. | Post-training quantization (calibrate after training; only option for open models) vs. quantization-aware training (train weights + scales jointly). |
| Use a smaller separate draft model (≥10× smaller, same family). Quick OOTB but high overhead. | Generate cheap draft tokens; target model validates. Yields N+1 tokens per forward pass. Only useful when batch size is low (spare compute). |

|                        |                    |
|:----------------------:|:------------------:|
|       **Medusa**       |     **EAGLE**      |
| **N-gram speculation** | **Prefix caching** |

|  |  |
|:--:|:--:|
| Purpose-built draft model trained on target's hidden states. Up to 8 draft tokens. Production go-to. | Fine-tune extra decoder heads onto the target. 2-4 draft tokens. Inspired EAGLE. |
| Reuse KV cache for shared prefix across requests. Improves TTFT. Rule: novel tokens last. | Build n-gram dictionary at prefill; match suffixes during decode. Best for code completion. |

|                             |                             |
|:---------------------------:|:---------------------------:|
|     **KV cache tiers**      |   **Cache-aware routing**   |
| **Tensor Parallelism (TP)** | **Expert Parallelism (EP)** |

|  |  |
|:--:|:--:|
| Route a user's conversation back to the same replica so their prefix cache hits. | G1 GPU VRAM (TB/s) \> G2 CPU RAM (100s GB/s) \> G3 local SSD (GB/s) \> G4 networked SSD. |
| Shard MoE experts across GPUs. Highest throughput. Multi-node-friendly (low communication). | Split each layer's weights across GPUs in a node. Lowest latency. Needs all-reduce — not multi-node-friendly. |

|                               |                                |
|:-----------------------------:|:------------------------------:|
| **Pipeline Parallelism (PP)** |       **Disaggregation**       |
|       **xPyD notation**       | **Conditional disaggregation** |

|  |  |
|:--:|:--:|
| Separate prefill and decode onto independent engines. Each can be sized for its bottleneck. | Split successive layers across GPUs. Multi-node fallback for dense models. Pipeline bubbles waste compute. |
| Requests go to decode first; only forwarded to prefill if input is long or uncached. | x prefill engines + y decode engines serving one model. e.g., 5P3D = 5 prefill, 3 decode. |

|                               |                            |
|:-----------------------------:|:--------------------------:|
|            **VLM**            |    **Embedding model**     |
| **Matryoshka representation** | **Real-Time Factor (RTF)** |

|  |  |
|:--:|:--:|
| Encodes input to fixed-length semantic vector. Used for RAG, search, recommendations. Big batches, no caching, scale horizontally. | Vision-Language Model. Wraps an LLM with a small vision encoder. Adds ~1,000 tokens per image. |
| How fast ASR transcribes audio. RTF 600 = 1 hour in 6 seconds. Optimized Whisper hits ~1,000×. | Embedding where the prefix of the vector encodes more meaning. Variable dimensionality without retraining. |

|                                    |                                  |
|:----------------------------------:|:--------------------------------:|
| **Voice Activity Detection (VAD)** | **Time to first sentence (TTS)** |
|      **Context Parallelism**       |        **Ring attention**        |

|  |  |
|:--:|:--:|
| User-meaningful latency metric for text-to-speech. More useful than time to first byte. | Detects speech vs. silence; chunks audio at natural boundaries for ASR. Used in real-time pipelines. |
| GPUs pass partial attention results around a ring. Mechanism behind Context Parallelism. | Used by video gen models. Replicates weights across all GPUs; splits attention computation via ring attention. |

|  |  |
|:--:|:--:|
| **Container / Docker / image / registry** | **NIM** |
| **Autoscaling signals** | **Continuous (in-flight) batching** |

|  |  |
|:--:|:--:|
| NVIDIA Inference Microservice. Pre-built containers for popular models. | Container = running instance. Image = built package. Dockerfile = build script. Registry = image store. |
| Token-level interleaving of requests. Best latency. Default in vLLM, SGLang, TRT-LLM. | Use both utilization (lagging) and traffic (proactive). They diverge. |

|  |  |
|:--:|:--:|
| **Cold start** | **Scale to zero** |
| **Hyperscaler vs. neocloud vs. reseller** | **Reserved vs. on-demand vs. spot** |

|  |  |
|:--:|:--:|
| Drop to 0 replicas when idle. Good for dev or predictable workloads; bad for latency-sensitive low traffic. | Time from launching a replica to first response. Mitigate: slim images, cached engines, weights stored near GPUs. |
| Reserved (long-term, discounted), on-demand (flexible), spot (cheap, pre-emptible). Production mixes all three. | AWS/GCP (premium, broad) vs. CoreWeave/Nebius (GPU-focused) vs. spot markets like SF Compute. |

|                                      |                              |
|:------------------------------------:|:----------------------------:|
| **Active-active vs. active-passive** | **Geo-aware load balancing** |
| **Blue-green vs. canary deployment** |   **WebSockets vs. gRPC**    |

|  |  |
|:--:|:--:|
| Roughly 5 ms per time zone. Route users to a nearby datacenter. | Active-active: multiple regions serve live, failures transparent. Active-passive: hot standby idle until failover. |
| WebSockets = unstructured bidirectional real-time (audio). gRPC = schema-enforced service-to-service. Both enable streaming. | Blue-green doubles GPU spend; canary ramps traffic gradually. Canary preferred for GPU workloads. |

---

## Deck B — Application, Discrimination & Numbers (cards 105–208)

These cards test whether you can *use* the vocabulary, not just recite it. Many have multi-part answers — say all parts out loud before flipping.

### B.1 — Differences ("what's the difference between X and Y?")

|  |  |
|:--:|:--:|
| **Prefill vs. decode — three differences** | **TTFT vs. ITL — when does each dominate user pain?** |
| **TP vs. PP vs. EP — one-line each** | **Reserved vs. on-demand vs. spot — when to use each** |

|  |  |
|:--:|:--:|
| TTFT dominates for short outputs (chat first reply, code completions). ITL dominates for long outputs (essay, agent traces). A 50-token reply with 200 ms TTFT + 10 ms ITL feels worse than a 2,000-token reply with the same numbers. | (1) Prefill processes all input tokens in parallel; decode processes one token at a time. (2) Prefill is compute-bound; decode is memory-bandwidth-bound. (3) Prefill drives TTFT; decode drives ITL/TPS. |
| Reserved: predictable steady load (baseline). On-demand: bursty unknown traffic. Spot: batch / offline / restartable jobs. Production mixes all three. | TP: shard each layer's weights across GPUs *inside a node* — lowest latency, needs all-reduce. PP: split layers sequentially across GPUs — multi-node, bubbles. EP: shard MoE experts — highest throughput, low comms. |

|  |  |
|:--:|:--:|
| **Continuous batching vs. static batching** | **PTQ vs. QAT — when forced to use each** |
| **FP16 vs. FP8 vs. FP4 — quality vs. speed tradeoff** | **Self-attention vs. cross-attention** |

|  |  |
|:--:|:--:|
| PTQ: you're consuming an open-weights model someone else trained. QAT: you control training and want best-quality 4-bit (e.g., on-device deployment). Default to PTQ; QAT only if PTQ quality is unacceptable. | Static: wait for batch to fill (or timeout), then run. Continuous: interleave requests at token granularity — exited requests free their slot immediately. Continuous wins on both latency and throughput; static is rarely correct. |
| Self: Q, K, V from the *same* sequence (LLM token-on-token). Cross: Q from one sequence, K/V from another (image-gen UNet attending over text encoder output). | FP16: baseline quality, baseline speed. FP8: ~0 perceptible quality loss, ~30–50% real speedup. FP4: visible quality drop, ~2× speedup over FP8. Default to FP8 in production; FP4 only after evals confirm. |

|  |  |
|:--:|:--:|
| **Hyperscaler vs. neocloud — three trade-offs** | **NVLink vs. InfiniBand — which is faster, and why does it matter?** |
| **Greedy vs. temperature sampling — when is each correct?** | **MoE vs. dense model — serving cost comparison** |

|  |  |
|:--:|:--:|
| NVLink: intra-node, ~900 GB/s (Hopper) up to 1.8 TB/s (Blackwell). InfiniBand: inter-node, ~400 Gb/s per NIC — *50× slower*. That gap is exactly why TP stays inside a node and PP/EP crosses nodes. | Hyperscaler (AWS, GCP): broad services, higher $/GPU-hr, deep ecosystem. Neocloud (CoreWeave, Nebius): GPU-focused, lower $/GPU-hr, fewer ancillaries. Reseller / spot markets (SF Compute): cheapest, least guarantees. |
| MoE: parameter count overstates serving cost. Qwen3-235B-A22B uses 22B active per token → serves like a 22B dense model on compute, but needs ~235B worth of VRAM for weights. Cheaper per-token, expensive per-GPU. | Greedy (T=0): deterministic, repeatable evals, code completion. Temperature > 0: creative tasks, brainstorming. Top-p ~0.9 is a safer default than temperature alone for production chat. |

|  |  |
|:--:|:--:|
| **vLLM vs. SGLang vs. TensorRT-LLM — pick one for each scenario** | **Active-active vs. active-passive — the cost-vs-RTO trade** |
| **Disaggregation vs. continuous batching — which problem do they solve?** | **Quantization-of-weights vs. quantization-of-KV-cache** |

|  |  |
|:--:|:--:|
| Active-active doubles GPU spend (both regions live). Active-passive saves money but adds failover latency (10s of seconds, sometimes minutes). Pick active-active for consumer chat, active-passive for batch / B2B. | (1) Broad hardware portability, easy MoE → vLLM. (2) Cutting-edge MoE (DeepSeek, Kimi) + multi-modal → SGLang. (3) Raw peak perf on Hopper/Blackwell, NVFP4 native, can afford harder ops → TensorRT-LLM. |
| Weights: large fixed footprint, cheapest to quantize first (FP8 weights ≈ 0 quality loss). KV cache: grows per-request, quantizing it (FP8 KV) lets you serve longer contexts or more concurrent users without OOM. Often combined. | Continuous batching solves *within-replica* GPU under-utilization. Disaggregation solves *prefill vs. decode contention* — they have opposite bottlenecks fighting for the same GPU. Different problems; both can be on at once. |

|  |  |
|:--:|:--:|
| **Medusa vs. EAGLE vs. n-gram speculation** | **MIG vs. MPS — when to slice a GPU vs. share it** |
| **L1 cache vs. L2 cache vs. HBM** | **Speculative decoding vs. parallel sampling** |

|  |  |
|:--:|:--:|
| Medusa: extra heads on the target. EAGLE: small dedicated draft model trained on target's hidden states (production go-to). N-gram: zero-model dictionary lookup (best for code completion, repeating tokens). | MIG: hardware partition into up to 7 isolated compute slices. Use for *deterministic* small-model serving (embeddings). MPS: software time-share between processes. Use for *bursty* mixed workloads where isolation isn't critical. |
| Speculation: one user, faster generation (draft + verify). Parallel sampling: one user, *N* alternative completions in parallel (for best-of-N reranking). Different goals — don't confuse them. | L1: per-SM, ~256 KB, ~10 TB/s. L2: chip-wide, ~50 MB on H100, ~5 TB/s. HBM: off-die VRAM, ~80–192 GB, ~3–8 TB/s. Each tier is roughly 2× slower and 100× larger than the next. |

### B.2 — Scenario cards ("you're asked X, what's the right answer?")

|  |  |
|:--:|:--:|
| **Scenario: chat product TTFT regressed from 200 ms to 800 ms. Three things to check.** | **Scenario: throughput is fine but P99 latency is awful. What's likely?** |
| **Scenario: serving 70B model, 8×A100 80GB node, OOM under load. Two fixes.** | **Scenario: long-context RAG (40K tokens). Top three optimizations.** |

|  |  |
|:--:|:--:|
| (1) Long-tail batching — a few P99 outliers dragging the tail; check static batch timeout. (2) GC / Python pauses in the serving layer. (3) A specific input length triggering re-compile or new CUDA graph capture. | (1) Did average input length grow (more prefill work)? (2) Is prefix caching still hitting (system prompt change?)? (3) Did a model swap or quant change happen (FP8 → FP16)? |
| (1) Prefix caching for the retrieved chunks (TTFT killer otherwise). (2) Quantize KV cache to FP8 (long context = huge KV). (3) Disaggregate prefill from decode — different bottlenecks at scale. | (1) Quantize weights to FP8 (frees ~50% weight memory). (2) Quantize KV cache to FP8 (frees per-request memory). Combined, you can usually double concurrency before next OOM. |

|  |  |
|:--:|:--:|
| **Scenario: cold start is 4 minutes; SLA needs <30 s. What to fix?** | **Scenario: cost-per-token is fine but cost-per-GPU-hour grew 3×. What happened?** |
| **Scenario: a new model release uses MLA. What changes in your serving?** | **Scenario: agentic workload — average 12 LLM calls per task. Optimization priority?** |

|  |  |
|:--:|:--:|
| Utilization dropped — same per-token cost but GPUs sit idler. Likely causes: traffic dropped (autoscale lagging), batch size shrank, or KV cache hit ratio collapsed (cache invalidation). Cost-per-token is the right unit; per-GPU-hr alone is a trap. | (1) Slim the container image (no torch dev deps). (2) Cache compiled engines (TRT compile is minutes). (3) Pre-warm replicas before traffic shifts. (4) Store weights on local NVMe near the GPU. |
| (1) Prefix caching — agent loops reuse system prompt + recent turns; cache hit ratio dominates cost. (2) Smaller model — most agent steps are routing/tool-calls, not reasoning. (3) Speculative decoding for the long generation steps. | KV cache footprint shrinks dramatically (MLA compresses KV via low-rank projection) — you can serve longer context per GPU. But engine support is the gating factor; check vLLM/SGLang version. |

|  |  |
|:--:|:--:|
| **Scenario: ASR pipeline RTF is 30 (real-time = 1.0). Acceptable?** | **Scenario: image gen — denoising takes 50 steps × 2 (CFG) = 100 forward passes. Two ways to halve cost.** |
| **Scenario: a customer demands FP16 "for quality." How do you push back?** | **Scenario: P99 latency is 10× P50. Healthy or broken?** |

|  |  |
|:--:|:--:|
| (1) Skip classifier-free guidance in the last ~10–20% of steps (late steps refine detail, not structure). (2) Distill the model into a smaller stepped version (Latent Consistency Models, SDXL Turbo). | RTF 30 means 1 hour of audio in 2 minutes. Acceptable for offline batch transcription. For real-time captioning you need RTF ≥ ~1.0 with low latency per chunk; tune Whisper + VAD chunking. |
| Broken in most cases. P99/P50 > 5× usually means: (a) some requests hit cold compile/recapture, (b) static batching timeout, or (c) a specific input shape misses a fast path. Investigate the slow requests' shapes. | Run an eval at FP8 vs FP16 on *their* tasks. Almost always: FP8 is within noise. Cost: FP8 is ~2× cheaper per token. Frame it as ROI, not religion. If their eval shows a real gap, accept FP16 for that model only. |

|  |  |
|:--:|:--:|
| **Scenario: GPT-OSS-120B vs. Llama-3.1-70B for chat — quick decision framework.** | **Scenario: prefix cache hit rate dropped from 80% to 30% overnight. Triage.** |
| **Scenario: tokens/sec drops 40% when you turn on speculation. Why?** | **Scenario: serving in 3 regions, one region's P99 doubles. Likely cause.** |

|  |  |
|:--:|:--:|
| (1) Run both on the same eval. (2) Compare cost-per-completed-task (not cost-per-token). (3) Pick smaller model if eval-gap < ~2%. Don't over-pay for marginal quality. | (1) Did the system prompt change (invalidates cache for every user)? (2) Did the cache routing layer break (users no longer pinned to same replica)? (3) Did a new model rev evict cache on load? |
| Region-specific issues: hardware difference (older GPUs), data-center congestion, or interconnect saturation. Check per-region GPU model + utilization. Add a region-tag to your latency dashboards. | High batch size. Speculation only helps when there's spare compute during decode. At high batch, compute is saturated — speculation now *competes* with real tokens. Disable speculation under load. |

### B.3 — Numerical / back-of-envelope cards

|  |  |
|:--:|:--:|
| **A 70B FP16 model — how much VRAM for weights alone?** | **A 70B FP8 model — how much VRAM for weights?** |
| **8K-token context, 70B model, FP16 KV cache — KV size per sequence?** | **Same as above but FP8 KV — new size?** |

|  |  |
|:--:|:--:|
| ~70 GB. Rule of thumb: 1 GB per 1B params at FP8. Frees half your VRAM compared to FP16. | ~140 GB. Rule of thumb: 2 GB per 1B params at FP16. Doesn't fit on a single 80 GB GPU — needs TP across at least 2 GPUs. |
| ~1.3 GB per sequence. KV cache scales linearly with sequence length, halved by FP8 quantization. | ~2.6 GB per sequence. Formula: 2 (K+V) × num_layers × hidden_dim × bytes_per_value × seq_len. For 70B model: ~80 layers × ~8K hidden × 2 B × 8K seq ≈ 2.6 GB. |

|  |  |
|:--:|:--:|
| **H100 SXM5 specs — FP16 TFLOPS, HBM, bandwidth?** | **B200 specs — FP8 TFLOPS, HBM, bandwidth?** |
| **Arithmetic intensity of attention at N=4K, d=128, FP16 — bound by what?** | **Same kernel at FP8 — does it become compute-bound?** |

|  |  |
|:--:|:--:|
| ~5 PFLOPS FP8, 192 GB HBM3e, ~8 TB/s. Adds FP4 + microscaling formats. Today's gold standard. | ~989 TFLOPS FP16, ~1,979 TFLOPS FP8, 80 GB HBM3, ~3.35 TB/s. Workhorse of 2024–2025. |
| Intensity doubles to ~126 (bytes halved). H100 FP8 ops:byte ≈ 590. Still memory-bound (126 < 590). Quantization helps but doesn't flip the bottleneck — FlashAttention does (by reducing memory reads). | Intensity ≈ 63 ops/byte. H100 FP16 ops:byte ≈ 295. 63 < 295 → memory-bound. This is exactly why FlashAttention (fewer HBM reads) is so valuable. |

|  |  |
|:--:|:--:|
| **A user types ~5 words/sec. What's the minimum TPS that feels "faster than typing"?** | **A 200-token reply at 50 TPS — total streaming time?** |
| **Cost-per-1M-tokens decline — what's the historical rate?** | **A100 vs H100 — rough cost-per-token ratio?** |

|  |  |
|:--:|:--:|
| 4 seconds (200 / 50). Add ~300 ms TTFT → ~4.3 s end-to-end. Good chat feel; below the 5s "users disengage" threshold. | ~7 TPS (5 words × ~1.4 tokens/word). Below 10 TPS feels slow; 30+ TPS feels snappy; 100+ TPS feels instant for streaming. |
| H100 is ~2–3× more expensive per GPU-hour but delivers ~3–5× the throughput on FP8 workloads → roughly *half* the cost-per-token of A100 for properly-sized models. Newer hardware usually wins on $/token. | Roughly 10× per year over the past 3 years (Epoch AI, a16z 2025). Drives the "don't over-optimize for cost today, the curve will solve it" advice — but also the "capacity-planning is brutal" reality. |

|  |  |
|:--:|:--:|
| **A 70B model with 50% MoE sparsity (35B active) — VRAM and per-token compute?** | **8-GPU node with NVLink — TP-8 vs. TP-4 + DP-2: latency difference?** |
| **A 1,000-token system prompt, served 1M times/day, cached — savings?** | **Cold start 90 s, traffic doubles every 30 min — autoscale lead time?** |

|  |  |
|:--:|:--:|
| TP-8: lowest latency (all 8 GPUs work on each request, more all-reduce overhead per token but smaller per-GPU work). TP-4 + DP-2: 2× throughput (two independent requests in parallel) but per-request latency similar to TP-4. Pick TP-8 for latency-sensitive, TP-4+DP-2 for throughput. | VRAM: ~70 GB (need to store all 70B weights). Per-token compute: ~half that of dense 70B. MoE = same memory footprint as dense, but cheaper per token. |
| Autoscale must add capacity 30 min *before* you need it, but cold start takes 90 s. So launch new replicas when current utilization hits ~50% (giving 30 min headroom for traffic to grow + cold start). Reactive scaling at 80% utilization will always lag traffic doubling. | At ~1K tokens × ~$1/M input tokens × 1M requests = $1,000/day in input compute. Prefix caching turns ~95% of that prefill into a cache hit → savings of ~$950/day. |

### B.4 — Common-confusion / gotcha cards

|  |  |
|:--:|:--:|
| **Why doesn't more VRAM = more throughput automatically?** | **Why does "perceived TPS" matter more than "total TPS"?** |
| **Why is FP8 "usually fine" but FP4 "requires evals"?** | **Why is the model's parameter count a bad capacity-planning unit?** |

|  |  |
|:--:|:--:|
| Total TPS describes total system tokens/sec; perceived TPS describes one user's stream. A system at 10,000 TPS with 1,000 concurrent users gives each user 10 TPS — unusable. Always quote both. | More VRAM lets you fit a bigger model or more KV cache, but throughput is gated by *memory bandwidth*, not capacity. An H100 with 80 GB at 3.35 TB/s often out-throughputs an H200 with 141 GB at 4.8 TB/s by less than the bandwidth ratio suggests. |
| Need to also account for: activation memory during prefill, KV cache growth per request, framework overhead, and quantization scale factors. Rule of thumb: VRAM_required ≈ 1.5–1.8× weight memory. | FP8 has 4 exponent bits — preserves dynamic range needed by softmax. FP4 doesn't — softmax outliers get clipped, attention degrades. PTQ at FP8: works. PTQ at FP4: often visible quality loss; QAT or fancy calibration recommended. |

|  |  |
|:--:|:--:|
| **Why does turning on speculation sometimes "work in dev but break in prod"?** | **Why does quantizing the KV cache help long-context users more than short-context users?** |
| **Why doesn't "inference time" equal "end-to-end latency"?** | **Why is "the model is hallucinating" rarely the right diagnosis at the inference layer?** |

|  |  |
|:--:|:--:|
| KV grows linearly with context length. For a 1K-token chat, KV is small either way. For a 100K-token RAG request, FP8 KV is the difference between fitting and OOM. Long-context users benefit disproportionately. | Dev: low concurrency, spare GPU compute, speculation pays off (faster decode). Prod: high concurrency, GPU saturated, speculation now *steals* compute from real tokens. Tune by load, not by feature flag. |
| Hallucination is a *model behavior* — different model or different prompt fixes it. The inference layer determines *latency and cost*, not *content correctness*. Don't blame TensorRT for a confabulation. | E2E includes network RTT (10–100 ms), TLS handshake (cached after first request), queueing at the load balancer (variable), serialization, and client overhead. Often 2–3× the on-GPU inference time. Measure both. |

|  |  |
|:--:|:--:|
| **Why isn't "just use a bigger GPU" usually the right answer?** | **Why does the second user often experience higher latency than the first?** |
| **Why does autoscaling on "CPU utilization" usually fail for GPU workloads?** | **Why is prefix caching's value sensitive to user routing?** |

|  |  |
|:--:|:--:|
| First user arrives — empty batch, gets full GPU, low ITL. Second user arrives — joins the batch, contends for memory bandwidth, slower ITL for *both*. This is normal continuous-batching behavior, not a bug. | Bigger GPU helps when memory or compute is the bottleneck. But often the constraint is *interconnect* (NVLink saturation), *cold start time*, or *cache miss rate*. Bigger GPU may just mean a more expensive bottleneck. |
| If user A's request hits replica 1 (cache built up), and follow-up hits replica 2 (cold cache), the cache value evaporates. Need session affinity / cache-aware routing for prefix caching to actually pay off. | CPU on a GPU server is mostly idle — Python orchestration only. The right signals are: GPU utilization, KV cache occupancy, queue depth, and incoming RPS. Use multiple signals; they diverge. |

|  |  |
|:--:|:--:|
| **Why does enabling FP8 weights sometimes *slow down* inference?** | **Why is "this is a 70B model" not enough info to plan capacity?** |
| **Why does "we'll just retry on failure" not fix a latency tail?** | **Why is the 4 GB/s NVMe throughput often more interesting than HBM bandwidth?** |

|  |  |
|:--:|:--:|
| Also need: dense or MoE (active params)? Context length budget? FP16 or FP8? Concurrent users? Streaming or batch? Same 70B model can need 1 GPU or 8 GPUs depending on those answers. | Engine may not have FP8 kernels for that operation → falls back to upcast → slower than native FP16. Verify with profiler: are you actually on the FP8 fast path, or just *configured* to be? |
| For cold-start scenarios. If you're paging weights from NVMe to HBM on cold-load (not pre-cached), the 4 GB/s NVMe bottleneck dominates the 8,000 GB/s HBM speed. Storage tier choice matters more than people realize. | Retries multiply load on an already-strained system. If P99 is 10s, a 30s retry timeout means *every* slow request triggers a duplicate request hitting the same hot path. Classic incident amplifier. |

### B.5 — Concept-graph anchor cards (recall by ID)

For every Inference-phase concept in `docs/kb/concepts.json`, can you produce a 1-sentence definition and one consequence? Sample challenge cards:

|  |  |
|:--:|:--:|
| **`inference-vs-training` — one-sentence def + cost shape** | **`gpu-memory-hierarchy` — four tiers + relative speeds** |
| **`continuous-batching` — what it replaces + the win** | **`paged-attention` — analogy + what problem it solves** |

|  |  |
|:--:|:--:|
| Registers → SRAM (L1, ~10 TB/s) → L2 (~5 TB/s) → HBM (~3–8 TB/s) → system RAM (~100 GB/s). Each tier is ~10–100× larger and ~2× slower than the one above. | Training writes weights (one-time, capital expense, ~$10s of M for a frontier model). Inference uses them (ongoing, operational expense, $0.10–$10 per 1M tokens depending on size + provider). |
| Like OS virtual memory for KV cache. Stores K/V in fixed-size pages with a lookup table → variable-length sequences no longer cause memory fragmentation. Solves the "set max-seq-len to worst-case, waste 90% of allocation" problem. | Replaces static (wait-for-full-batch) batching. Win: token-granularity request scheduling — completed requests free their slot immediately, new requests join mid-flight. Both lower latency *and* higher throughput. |

|  |  |
|:--:|:--:|
| **`tensor-parallelism` — when it stops scaling** | **`disaggregated-serving` — when the overhead is worth it** |
| **`speculative-decoding` — the one number that decides if it pays off** | **`mla` — what gets compressed and why it matters** |

|  |  |
|:--:|:--:|
| All-reduce communication grows. Inside a node on NVLink: scales well to 8 GPUs. Across nodes on InfiniBand: communication eats the win. Rule: keep TP inside a node, use PP/EP across nodes. | Roughly: above ~100M tokens/day on one model. Below that, the routing + KV-transfer overhead exceeds the prefill/decode contention savings. Above that, disaggregation lets each engine be sized for its bottleneck. |
| KV cache. MLA compresses K and V via low-rank projection (DeepSeek's design) → 10–100× smaller per-token KV footprint → long-context becomes affordable. Trade: requires architectural buy-in (not retrofittable). | Accept rate of draft tokens. Above ~70% accept rate, speculation pays off (~1.5–2× decode speedup). Below ~50%, speculation costs more than it saves (verification overhead exceeds tokens won). |

|  |  |
|:--:|:--:|
| **`inference-cost` — name the unit that beats $/M-tokens** | **`flash-attention` — why HBM reads matter more than FLOPS** |
| **`cuda-stack` — name the four layers** | **`gpu-generations` — name three things that change each generation** |

|  |  |
|:--:|:--:|
| CUDA (kernels) → cuDNN / cuBLAS (DL & linear-algebra primitives) → framework (PyTorch) → inference engine (vLLM / SGLang / TRT-LLM). Each layer abstracts over the one below. | Cost per *completed task* (e.g., $ per resolved support ticket, $ per generated PR review). $/M-tokens is a vendor unit; $/task is the business unit. Lets you compare a smarter expensive model to a cheaper chain. |
| Tensor Core throughput (faster FP8, then FP4); HBM bandwidth (3 → 4.8 → 8 TB/s); interconnect (NVLink 900 → 1,800 GB/s). Plus new precisions (FP4, microscaling) every other generation. | Standard attention reads/writes K, V, and intermediate matrices to HBM multiple times. FlashAttention tiles the computation in SRAM → fewer HBM round-trips → kernel goes from memory-bound toward compute-bound. Same math, much faster. |
