**Inference Engineering**

Problem Sets, Quizzes & Answer Key

*Companion to the book by Philip Kiely (Baseten Books, 2026)*

Eight chapter problem sets · Midterm · Final exam · Full answer key

> **Source & permitted use.** This document is an instructor-authored companion derived from *Inference Engineering* by Philip Kiely (Baseten Books, 2026). It paraphrases and adapts material from that book for internal use within the Andhra University / Oxmiq curriculum only. **Do not redistribute, mirror, or publish outside this course.** Students and instructors should obtain the original book for canonical text, code samples, and references. If a formal license or permission grant for this material is established, replace this notice with a pointer to the source agreement.

How to use this packet

This packet contains eight problem sets (one per chapter), a midterm exam covering Chapters 0-4, and a final exam covering the full course. The **Answer Key** at the end is meant for instructors. Students should attempt all problems before turning to it.

Each problem set blends:

- **Conceptual short-answer** — test definitions and relationships (5-10 minutes each).

- **Calculations** — apply formulas like arithmetic intensity, latency conversions, VRAM sizing.

- **Design / open-ended** — pick a strategy for a described workload and defend it.

- **Multiple choice** — for quick comprehension checks.

Problem Set 1: What is Inference?

Chapter 0. Recommended time: 30 minutes.

Conceptual

1.  Define **inference** in one sentence. How does it differ from training?

2.  Name the **three layers** of an inference stack and give one example of work that happens in each.

3.  List the **six runtime techniques** from Chapter 0. Briefly (one sentence each) describe what each one does.

4.  The book argues that even a perfectly optimized single instance is insufficient. Why? Give two reasons.

Short answer

5.  Suppose you've fully optimized one replica of an inference server and it serves traffic perfectly under 100 concurrent users. Your product goes viral and traffic jumps to 100,000 concurrent users. Which **layer** must you now focus on, and what specific problems will you face?

6.  An engineer says: "We don't need infrastructure work — we just need a faster GPU." Push back on this. Give two scenarios where infrastructure matters more than raw GPU speed.

Multiple choice

7.  Which of these is **not** one of the six runtime techniques?

<!-- -->

1)  \(A\) Batching

2)  \(B\) Caching

3)  \(C\) Differentiation

4)  \(D\) Disaggregation

<!-- -->

8.  Multi-cloud capacity management primarily addresses which problem?

<!-- -->

5)  \(A\) Reducing per-token cost on a single GPU

6)  \(B\) Avoiding silos where some GPU pools are starved while others sit idle

7)  \(C\) Designing better attention kernels

8)  \(D\) Choosing the right quantization format

Problem Set 2: Prerequisites

Chapter 1. Recommended time: 45 minutes.

Latency calculations

9.  Your LLM has an **inter-token latency of 25 ms**. What is the perceived **TPS per user**?

10. Your team measures **P90 TTFT = 240 ms** and **P90 TPS = 50 tokens/sec** during chat workloads. For a 200-token response, what is the **approximate total response time** at P90? (Assume streaming.)

11. A latency distribution has **mean 380 ms** and **P50 = 300 ms**. What does this gap tell you about the distribution shape? What does it imply for the user experience?

Design questions

12. For each application, decide whether to optimize for **latency** or **throughput**. Justify each choice in one sentence.

<!-- -->

9)  \(a\) A customer-support chatbot embedded in a software product.

10) \(b\) A nightly job that embeds 50 million product descriptions for a recommendation system.

11) \(c\) A real-time voice translation app.

12) \(d\) A back-catalog podcast transcription pipeline.

<!-- -->

13. A startup is building a coding assistant on top of frontier closed-model APIs. Their monthly bill has grown from \$200 to \$40,000 in six months. Should they switch to dedicated deployments? **List three** considerations that should drive the decision.

Fine-tuning vs. distillation

14. In one or two sentences each, explain the difference between **fine-tuning** and **distillation**. Then describe a scenario where you'd choose distillation over fine-tuning.

Percentiles

15. Match each percentile to its interpretation:

| **Percentile** | **Interpretation**          |
|----------------|-----------------------------|
| P50            | 1 in 100 requests is slower |
| P90            | 1 in 2 requests is slower   |
| P95            | 1 in 10 requests is slower  |
| P99            | 1 in 20 requests is slower  |

Problem Set 3: Models, Attention, and Bottlenecks

Chapter 2. Recommended time: 60 minutes. **This is the most calculation-heavy set.**

Mechanics

16. Write the **scaled dot-product attention** formula. Define each symbol (Q, K, V, d_k, softmax).

17. Explain in your own words why **prefill is compute-bound** and **decode is memory-bandwidth-bound**. Use the words "matrix multiplication," "weights," and "per token" in your answer.

18. Why is multi-head attention better than single-head attention? Give a concrete intuition involving syntactic relationships.

19. **Mixture of Experts.** Qwen3-235B-A22B has 235B total parameters and 22B active. Routes 8 of 128 experts per layer across 94 layers. (a) Why is MoE efficient for single-user inference? (b) What can go wrong in *batched* production inference, and what technique fixes it?

Arithmetic intensity

For these problems, use the H100 ops:byte ratio of **295** at FP16.

20. A kernel performs **3.2 × 10¹⁰ FLOPs** while reading and writing **2.4 × 10⁸ bytes**. Compute its arithmetic intensity. Is it compute-bound or memory-bound on an H100?

21. Standard attention has memory traffic **8N² + 8Nd** bytes and compute **4N²d + 3N²** ops for FP16. For sequence length **N = 8192** and head dimension **d = 128**, compute:

<!-- -->

13) \(a\) Total memory traffic in bytes.

14) \(b\) Total compute in operations.

15) \(c\) Arithmetic intensity.

16) \(d\) On an H100 with ops:byte = 295, is this kernel compute- or memory-bound?

<!-- -->

22. **Compute the H100's effective ops:byte at FP8.** Hopper's FP8 Tensor Core compute is roughly 2× FP16 (≈ 1,979 TFLOPS), and memory bandwidth is unchanged at 3.35 TB/s. What is the FP8 ops:byte ratio? Why does this affect quantization decisions?

Image generation

23. Why does running an image generation model with **50 denoising steps** correspond to ~100 forward passes, not 50? What is the technique that exploits this for the "one weird trick" speedup?

Conceptual

24. FlashAttention is lossless; sliding-window attention is lossy. Explain that distinction. When is each appropriate?

25. Why must the KV cache exist? What goes wrong without it, and what does it cost?

Problem Set 4: GPU Hardware

Chapter 3. Recommended time: 30 minutes.

GPU architecture

26. Match the term to the description:

| **Term**    | **Description**                                      |
|-------------|------------------------------------------------------|
| SM          | On-chip global cache shared across all SMs           |
| Tensor Core | Hardware unit for matrix multiply-accumulate (MMA)   |
| CUDA Core   | Performs scalar arithmetic                           |
| L2 cache    | Streaming Multiprocessor — building block of the GPU |
| HBM         | Off-chip high-bandwidth main memory (the GPU's VRAM) |

27. Why are **Tensor Cores** more important than **CUDA Cores** for inference? Reference the dominant operation in transformer models.

28. For each GPU below, indicate which is best suited for the workload and why.

<!-- -->

17) \(a\) Frontier LLM inference at scale → H100, H200, L4, or B200?

18) \(b\) Small text-embedding model serving 100 RPS → L4 or H100?

19) \(c\) Video generation requiring all 8 GPUs of a node → A100 or B200?

Interconnects

29. Rank these interconnects from **highest** to **lowest** bandwidth and indicate the scope each operates at: NVLink (Blackwell), NVLink (Hopper), InfiniBand, Ethernet.

30. Why does the speed gap between NVLink and InfiniBand shape parallelism strategy choices for multi-node inference?

MIG

31. **MIG slices.** An H100 has 132 SMs. (a) How many compute slices and memory slices can it be split into? (b) Give one workload where MIG slicing is appropriate, and one where it isn't.

Alternative accelerators

32. For each accelerator, name one architectural "bet" it makes: (a) Cerebras WSE-3, (b) Groq LPU, (c) Google TPU, (d) Qualcomm Cloud AI 100. Why has NVIDIA remained dominant despite these alternatives?

Problem Set 5: Software Stack

Chapter 4. Recommended time: 30 minutes.

CUDA stack

33. Describe what each component does: **CUDA kernel**, **CUDA graph**, **CUDA driver**, **CUDA runtime**.

34. **Kernel fusion.** Given two pointwise kernels — one multiplies a vector by 2, the other by 3 — show why running them sequentially wastes HBM round trips. What does kernel fusion do, and which inference phase (prefill or decode) benefits most? Why?

File formats

35. Why is **safetensors** considered safer than older formats like Python pickle for loading model weights?

36. What does ONNX bundle that safetensors does not? Why might you prefer one over the other?

Engine selection

37. For each scenario, choose the most appropriate inference engine and justify in one sentence: **vLLM**, **SGLang**, or **TensorRT-LLM**.

<!-- -->

20) \(a\) Day-zero deployment of a brand-new open model on mixed NVIDIA + AMD hardware.

21) \(b\) High-throughput serving of DeepSeek-V3 on a GB200 NVL72 with expert parallelism.

22) \(c\) Squeezing the absolute best performance out of an H200 for a stable production workload using NVFP4 quantization.

23) \(d\) Generating images with a custom diffusion pipeline on a single A100.

<!-- -->

38. **NVIDIA Dynamo** sits where in the stack? When should you use it, and when should you skip it?

Benchmarking

39. List **four pitfalls** to avoid when running an inference benchmark. (Hint: think about variance, methodology, baselines, and ecosystem.)

40. What's the difference between **benchmarking** and **profiling**? When do you need each?

Problem Set 6: Performance Techniques

Chapter 5. Recommended time: 75 minutes. **Half-course capstone.**

Quantization

41. Rank the following components from **least sensitive** to **most sensitive** to quantization, and explain *why* the most-sensitive component is so dangerous to quantize: weights, KV cache, attention, activations.

42. Why are **floating-point** formats (FP8, FP4) preferred over **integer** formats (INT8, INT4) for LLM inference? Use the words "exponent" and "dynamic range" in your answer.

43. **Microscaling formats.** Compare MXFP8 (block size 32) to NVFP4 (block size 16 + global 32-bit scale factor). Why does block size affect quality?

44. Explain the difference between **PTQ** and **QAT**. When is each used?

45. What are **three quality-check methods** for validating a quantization run? Why do you need to run more than one?

Speculative decoding

46. Speculative decoding produces N+1 tokens per forward pass when N drafts are accepted. **For each of the following, explain in one sentence how the method works:**

<!-- -->

24) \(a\) Draft-target speculative decoding.

25) \(b\) Medusa.

26) \(c\) EAGLE.

27) \(d\) N-gram speculation.

<!-- -->

47. Why is speculative decoding **less useful at high batch sizes**? What happens to the system when speculation runs while batched compute is saturated?

48. Which speculation method would you pick for: (a) a fresh deployment with no training infrastructure, (b) a code-completion product where the output strongly resembles the input, (c) a production deployment where you want highest-quality drafts? Justify each.

Caching

49. **Prefix caching.** Two requests arrive: `"Translate this French sentence to English: Bonjour."` and `"Translate this French sentence to English: Au revoir."`. (a) Treating the literal `"Translate this French sentence to English: "` as the shared prefix and the per-request word as the variable suffix, what part can be cached? (b) Now consider the inverted shape, where the variable word comes *first* and the instruction comes after: `"Bonjour. Translate this to English."` and `"Au revoir. Translate this to English."` — what changes about cacheability?

50. Rank these KV-cache storage tiers by speed: networked SSD, GPU VRAM, local SSD, CPU RAM. For each, give one scenario in which it's the right choice.

Parallelism

51. **VRAM sizing.** Estimate VRAM needed (in GB) to serve **Llama 3.1 405B at FP8** with **1.8× KV-cache headroom**. How many B200 GPUs (180 GB each) does this require?

> vram_required = (bits/8) × params × kv_overhead = (8/8) × 405 × 1.8 = ?

52. Compare the three parallelism strategies. Pick which is best for each workload:

<!-- -->

28) \(a\) Llama 3.1 405B (dense, frontier) on a single 8×B200 node for the lowest possible TTFT.

29) \(b\) Qwen3-235B-A22B (MoE) across two nodes connected by InfiniBand for high throughput.

30) \(c\) A dense 800B model needing two nodes.

<!-- -->

53. Why does Tensor Parallelism not work well across nodes via InfiniBand?

Disaggregation

54. **xPyD notation:** What does 5P3D mean? Why are the prefill and decode counts typically not equal in production?

55. Disaggregation requires **three conditions** to be worthwhile. Name them. For each, give a workload where the condition fails (and disaggregation should be skipped).

Problem Set 7: Modalities Beyond Text

Chapter 6. Recommended time: 30 minutes.

VLMs

56. A VLM processes a single 1024×1024 image as roughly **1,000 tokens**. (a) Why does this make VLM inference "long context"? (b) Which LLM optimizations transfer directly to VLMs? Name three. (c) What's the new tradeoff VLMs introduce that pure LLMs don't have?

Embeddings

57. Embedding inference differs from LLM inference in **four** important ways. List each and explain why.

58. What are **Matryoshka representations** and what tradeoff do they enable?

59. Why is *cosine similarity* a reasonable QA check for FP8 weight quantization on an embedding model?

ASR and TTS

60. **Real-Time Factor (RTF).** An optimized Whisper pipeline transcribes a **3-hour podcast in 9 seconds**. What is its RTF? Is this realistic per the book?

61. For real-time dictation (single-chunk ASR), most performance gains come from **infrastructure**, not the model. Why? What is the role of WebSockets and VAD?

62. TTS introduces two custom metrics: **TTFB** and **time to first sentence**. Why is the second often more user-meaningful than the first?

63. Why is a **cascading pipeline** (VAD → ASR → LLM → TTS) currently preferred to a unified speech-to-speech model for most voice products?

Image and video gen

64. Explain the "one weird trick" for faster image generation. Why does quality remain acceptable when classifier-free guidance is skipped late in the schedule?

65. Why do **video generation** models use **Context Parallelism** rather than Tensor Parallelism? What is *ring attention*?

66. Why is quantization **risky for video generation** even though the speedup is significant? What techniques preserve quality?

Problem Set 8: Production

Chapter 7. Recommended time: 45 minutes.

Containerization

67. Name **four categories of dependencies** that go into a production inference container. Why is **pinning exact versions** important?

Autoscaling

68. Why must you autoscale on **both utilization and traffic** signals rather than just one?

69. Why must the **concurrency target** match the **inference engine's batch size**?

70. List the **four contributors** to cold start time. Which two are *most* under your control as an inference engineer?

71. Compare **static batching**, **dynamic batching**, and **continuous (in-flight) batching**. Which gives best latency? Which is the default in modern engines?

Cost estimation

72. A workload uses **2 billion input tokens** and **800 million output tokens** per month. The API charges **\$1.25/M input + \$10/M output**. The dedicated deployment uses **2,200 GPU-hours/month at \$3.50/hr**.

<!-- -->

31) \(a\) Compute the per-token API cost.

32) \(b\) Compute the dedicated deployment cost.

33) \(c\) Which is cheaper? By how much? What else should factor into the decision?

Multi-cloud

73. Llama 3 training had 419 unexpected interruptions in 54 days on 16,000 GPUs. What does this imply for designing inference systems? Compare **active-active** vs. **active-passive** reliability postures and pick one for: (a) a global consumer chat app, (b) an internal compliance-critical batch system.

74. **Geo-aware load balancing rule of thumb.** Roughly 5 ms per time zone. A user in London routes to a Seattle datacenter (8 time zones). What's the **minimum** added latency, and is that acceptable for a chat app with a 200 ms P95 TTFT SLA?

Deployments

75. Why is **blue-green deployment** poorly suited for GPU inference workloads? Why is **canary** preferred?

Client code

76. A team measures **300 ms P95 end-to-end latency** but server-side inference time is only **180 ms**. Where could the missing 120 ms be? Name three plausible culprits.

Midterm Examination — Chapters 0-4

90 minutes. 50 points total.

Section A: Multiple choice (10 × 1 pt = 10 pts)

77. **M1.** TTFT primarily reflects which phase of LLM inference?

<!-- -->

34) \(A\) Decode (B) Prefill (C) Sampling (D) Tokenization

<!-- -->

78. **M2.** Which is **memory-bandwidth-bound**?

<!-- -->

35) \(A\) LLM prefill (B) LLM decode (C) Image generation (D) Video generation

<!-- -->

79. **M3.** Inter-token latency of 5 ms corresponds to a perceived TPS of:

<!-- -->

36) \(A\) 50 (B) 100 (C) 200 (D) 500

<!-- -->

80. **M4.** A kernel with arithmetic intensity 800 ops/byte on an H100 (ops:byte = 295) is:

<!-- -->

37) \(A\) Memory-bound (B) Compute-bound (C) Perfectly balanced (D) Insufficient information

<!-- -->

81. **M5.** The KV cache primarily turns attention from:

<!-- -->

38) \(A\) Linear to quadratic (B) Quadratic to linear (C) Linear to constant (D) Constant to linear

<!-- -->

82. **M6.** Tensor Cores perform:

<!-- -->

39) \(A\) Scalar additions (B) Sin/cos (C) Matrix multiply-accumulate (D) Memory copies

<!-- -->

83. **M7.** NVLink connects:

<!-- -->

40) \(A\) Nodes to nodes (B) GPUs within a node (C) CPUs to storage (D) Datacenters to each other

<!-- -->

84. **M8.** Which inference engine has the **broadest hardware support**?

<!-- -->

41) \(A\) vLLM (B) SGLang (C) TensorRT-LLM (D) Triton

<!-- -->

85. **M9.** "Goodhart's Law" warns that:

<!-- -->

42) \(A\) GPUs degrade over time (B) Measures cease to be useful when they become targets (C) FP4 always loses quality (D) Multi-cloud is unreliable

<!-- -->

86. **M10.** A Multi-Instance GPU (MIG) can be split into up to:

<!-- -->

43) \(A\) 4 slices (B) 7 slices (C) 8 slices (D) 16 slices

Section B: Short answer (5 × 4 pts = 20 pts)

87. **M11.** Define **prefill** and **decode**. For each, name (a) what it does, (b) what bottleneck constrains it, and (c) which user-facing metric it primarily drives.

88. **M12.** A startup is deciding between a shared API (\$X/M tokens) and a dedicated deployment. List **four** factors they should consider.

89. **M13.** Write the **scaled dot-product attention formula**. Explain why attention scales quadratically with sequence length without the KV cache, and only linearly with it.

90. **M14.** What is **kernel fusion**? Why is it especially valuable during LLM decode?

91. **M15.** Compare **dense** and **MoE** architectures from an inference perspective. Why are MoE models often **larger** in total params but **smaller** in active params? What does this imply for VRAM sizing?

Section C: Computation (4 × 5 pts = 20 pts)

92. **M16.** **Arithmetic intensity.** A kernel performs 5.0 × 10⁹ ops while moving 4.0 × 10⁷ bytes. Compute the arithmetic intensity. If running on an H100 at FP16 (ops:byte = 295), is it compute- or memory-bound? Explain.

93. **M17.** **VRAM sizing.** A 200B-parameter model is deployed in FP8 with 1.8× KV cache overhead. (a) How much VRAM does it need? (b) How many B200 GPUs (180 GB each) does this require? (c) What if you quantize to FP4 instead?

94. **M18.** **Latency conversions.** A team sees:

<!-- -->

44) ITL = 8 ms

45) Average output length: 250 tokens

46) TTFT (P50): 180 ms

Compute: (a) perceived TPS, (b) estimated total response time (streaming), (c) what is the dominant contributor to total latency — TTFT or decode?

95. **M19.** **GPU comparison.** An H100 has 80 GB VRAM at 3.35 TB/s. An H200 has 141 GB at 4.8 TB/s. Both deliver 989 TFLOPS at FP16. (a) Compute each GPU's ops:byte ratio. (b) Which is better for LLM decode? Why?

Final Examination — Full Course

3 hours. 100 points total. Closed book except a one-page reference card.

Section A: Multiple choice (15 × 1 pt = 15 pts)

96. **F1.** Which technique improves **TTFT** but not **TPS**?

<!-- -->

47) \(A\) Speculative decoding (B) Prefix caching (C) FP8 weight quantization (D) Tensor Parallelism

<!-- -->

97. **F2.** Which is true about NVFP4 vs. MXFP4?

<!-- -->

48) \(A\) NVFP4 uses larger blocks (B) NVFP4 adds a global 32-bit scale factor (C) MXFP4 has lower dynamic range (D) MXFP4 is NVIDIA-proprietary

<!-- -->

98. **F3.** Which speculation method does **not** require a separate draft model?

<!-- -->

49) \(A\) Draft-target (B) EAGLE (C) N-gram (D) Both B and C

<!-- -->

99. **F4.** The **xPyD** notation describes:

<!-- -->

50) \(A\) Replica counts (B) Disaggregation engine ratios (C) Pipeline parallelism shape (D) Quantization granularity

<!-- -->

100. **F5.** Which parallelism strategy gives the **lowest per-user latency** for a large dense model within one node?

<!-- -->

51) \(A\) Pipeline (B) Tensor (C) Expert (D) Context

<!-- -->

101. **F6.** Which modality is **least well served** by prefix caching?

<!-- -->

52) \(A\) RAG chat (B) Code completion (C) Embedding inference (D) Long agentic workflows

<!-- -->

102. **F7.** Which Whisper deployment pattern requires WebSockets and Voice Activity Detection?

<!-- -->

53) \(A\) Long-file batch transcription (B) Live dictation (C) Diarization (D) None of the above

<!-- -->

103. **F8.** **One weird trick** for image generation drops:

<!-- -->

54) \(A\) Some denoising steps entirely (B) The text encoder (C) Classifier-free guidance late in the schedule (D) The VAE

<!-- -->

104. **F9.** **Continuous batching** operates at which granularity?

<!-- -->

55) \(A\) Request (B) Batch (C) Token (D) Layer

<!-- -->

105. **F10.** **Scale to zero** is best for:

<!-- -->

56) \(A\) Latency-critical consumer chat (B) Development workloads (C) Voice agents (D) Real-time recommenders

<!-- -->

106. **F11.** Which is **not** a procurement mode for cloud GPUs?

<!-- -->

57) \(A\) Reserved (B) On-demand (C) Spot (D) Spec

<!-- -->

107. **F12.** Why does video generation use Context Parallelism rather than Tensor Parallelism?

<!-- -->

58) \(A\) Video models are too large for one GPU

59) \(B\) Weights are small enough to replicate; attention dominates and parallelizes naturally

60) \(C\) TP doesn't support attention

61) \(D\) Video models don't use attention

<!-- -->

108. **F13.** Llama 3 training observed roughly one failure per:

<!-- -->

62) \(A\) 5,000 GPU-hours (B) 50,000 GPU-hours (C) 500,000 GPU-hours (D) 5,000,000 GPU-hours

<!-- -->

109. **F14.** Which deployment pattern is **preferred** for GPU inference?

<!-- -->

63) \(A\) Blue-green (B) Canary (C) Hard cutover (D) Manual rollout

<!-- -->

110. **F15.** Which Whisper RTF would be considered "good" for back-catalog transcription?

<!-- -->

64) \(A\) 1× (B) 10× (C) 100× (D) 1000×

Section B: Short answer (10 × 3 pts = 30 pts)

111. **F16.** Define **arithmetic intensity** and **ops:byte ratio**. Show how to use them together to classify a kernel as compute- or memory-bound.

112. **F17.** Explain why FP8 inference gives both **2× FLOPS** and **2× effective memory bandwidth** compared to FP16.

113. **F18.** Compare EAGLE vs. n-gram speculation. When is each the better choice?

114. **F19.** What is **conditional disaggregation**, and why is it preferred to unconditional disaggregation in production?

115. **F20.** Why is the **KV cache** the central data structure of modern LLM inference? Name **three** optimizations that exploit it.

116. **F21.** Describe the four contributors to **cold start** time and how to mitigate each.

117. **F22.** For **VLMs**, name three carry-over optimizations from LLM inference and one new tradeoff specific to vision.

118. **F23.** When is **scale-to-zero** appropriate and when is it inappropriate? Give one example of each.

119. **F24.** Why is **active-active** multi-cloud preferred for a global consumer chat product despite the added complexity?

120. **F25.** Describe how **WebSockets** improve UX for real-time voice products. Why HTTP streaming alone isn't enough.

Section C: Long-form design (3 × 10 pts = 30 pts)

121. **F26.** **System design.** A team wants to serve a fine-tuned Llama 3 70B model for a customer-support chatbot embedded in a SaaS product. Expected traffic: ~50 concurrent users at peak, ~30 RPS average, with predictable business-hours spikes. Median input length 1,200 tokens (with significant prefix overlap across requests). Median output length 200 tokens. Latency SLA: P95 TTFT under 400 ms.

<!-- -->

65) \(a\) Recommend a GPU + inference engine + quantization choice. Justify each.

66) \(b\) Will you disaggregate prefill and decode? Why or why not?

67) \(c\) Will you use prefix caching? What context-engineering rule must the app team follow to make it work?

68) \(d\) Sketch the autoscaling strategy: signals, scale-down delay, scale-to-zero or not.

<!-- -->

122. **F27.** **Performance triage.** A team reports their LLM endpoint's **P95 TTFT has risen from 250 ms to 700 ms** over two weeks, with no model change. Inference-time P95 (server-side only) is **still 250 ms**. **End-to-end P95 is 700 ms.** Total throughput has also dropped 15%.

<!-- -->

69) \(a\) What does the inference-time vs. end-to-end gap tell you?

70) \(b\) Name **three** distinct hypotheses for the regression and how you'd test each (e.g., metrics to collect, dashboards to check).

71) \(c\) Suppose you discover the queue depth has crept up and one cloud region has hit GPU capacity. Outline the multi-cloud + autoscaling response.

<!-- -->

123. **F28.** **New model launch.** A frontier lab releases an 800B-parameter MoE LLM today on Hugging Face. Your team needs to support it in production within 72 hours.

<!-- -->

72) \(a\) Which engine do you reach for first, and why? What is the day-zero support reality?

73) \(b\) Estimate VRAM requirements at FP8 with 1.8× KV-cache headroom. How many B200 GPUs (180 GB each)? Is single-node feasible?

74) \(c\) Recommend a parallelism scheme. Justify the choice between TP, EP, and PP.

75) \(d\) Quality validation: name three checks you'd run before going live.

76) \(e\) Containerization advice — what's specifically different about deploying a brand-new model vs. a stable one?

Answer Key

**For instructors.** Sample answers below; in many cases multiple defensible answers exist — credit reasoning, not memorization.

Problem Set 1

**1.** Inference is the serving of trained AI models in production. Training learns weights from data; inference uses those weights to answer requests.

**2.** Runtime (e.g., a fused attention kernel on one GPU), Infrastructure (autoscaling Kubernetes pods across a region), Tooling (a developer abstraction like an inference engine config or a managed platform).

**3.** Batching (parallel requests), Caching (reuse KV cache for shared prefixes), Quantization (lower precision for more FLOPS/bandwidth), Speculation (draft + verify multiple tokens per pass), Parallelism (split across GPUs), Disaggregation (separate prefill and decode workers).

**4.** (i) Single replica eventually hits a traffic ceiling; (ii) GPU procurement/capacity becomes the constraint at hundreds of GPUs and beyond.

**5.** Infrastructure layer. Problems: GPU capacity in any one region, network bottlenecks, scaling latency (cold starts), silos between cloud providers.

**6.** (a) Even the fastest GPU is finite — a single replica caps out; you must scale horizontally. (b) Geo-latency: a fast GPU in Virginia doesn't help users in Singapore; you need multi-region. **MC:** Q1: C, Q2: B.

Problem Set 2

**1.** TPS = 1000/25 = **40 tokens/sec per user**.

**2.** TTFT (240 ms) + 200 tokens × (1/50 sec/token = 20 ms) = 240 + 4000 = **~4,240 ms ≈ 4.2 s**.

**3.** Mean \> P50 indicates a right-skewed distribution with outliers extending the tail. Implication: some users have a much worse experience than the average suggests; P90/P99 matter more than the mean.

**4.** (a) latency (user waiting); (b) throughput (offline batch); (c) latency (real-time); (d) throughput (offline).

**5.** Scale economics flip (per-GPU-hour vs. per-token); custom or fine-tuned model needed; latency / uptime SLAs require dedicated control.

**6.** Fine-tuning adapts weights of a pre-trained model to a new domain (same architecture). Distillation trains a smaller student to emulate a larger teacher's probability distributions (different, smaller architecture). Pick distillation when only a large teacher is available and you need a small deployment-friendly student (e.g., DeepSeek-R1 distilled onto Llama 3 / Qwen 2.5).

**7.** P50 → "1 in 2 slower"; P90 → "1 in 10"; P95 → "1 in 20"; P99 → "1 in 100".

Problem Set 3

**1.** Attention(Q, K, V) = softmax(QK^T / √d_k)V. Q = query vectors for tokens being generated; K = key vectors for prior tokens; V = value vectors used as the actual content to attend to; d_k = head dimension (scaling stabilizes gradients); softmax converts dot products to probabilities.

**2.** Prefill processes the whole input sequence in parallel — many matmuls per byte of weights loaded, high arithmetic intensity → compute-bound. Decode generates one token per pass — must load all weights once per token, low ops per byte → memory-bound.

**3.** Different heads can specialize in different relationships (subject-verb agreement, co-reference, long-range dependencies). One head doing everything is a bottleneck.

**4.** (a) Only 22B of 235B activate per request, so VRAM bandwidth + compute focus on a small slice — efficient for a single forward pass. (b) Different requests in a batch activate different experts, so almost all weights end up active. Fix: Expert Parallelism spreads experts across GPUs so each GPU is only responsible for its assigned experts.

**5.** Intensity = 3.2×10¹⁰ / 2.4×10⁸ = **~133 ops/byte**. Below 295 → **memory-bound** on H100.

**6.** N=8192, d=128. (a) memory = 8N² + 8Nd = 8·(8192²) + 8·8192·128 = 8·67,108,864 + 8,388,608 = 536,870,912 + 8,388,608 = **~545,259,520 bytes ≈ 520 MiB**. (b) compute = 4N²d + 3N² = 4·67,108,864·128 + 3·67,108,864 = 34,359,738,368 + 201,326,592 = **~34.56 GOps**. (c) intensity = 34,561,064,960 / 545,259,520 ≈ **63 ops/byte**. (d) 63 \< 295 → **memory-bound**.

**7.** Doubling FLOPS while bandwidth is unchanged doubles ops:byte → **~590**. This raises the bar for arithmetic intensity to remain compute-bound, which is why FP8 quantization unlocks performance: kernels that were memory-bound at FP16 can become memory-bound *and* faster at FP8, with twice the math throughput available before re-hitting the ceiling.

**8.** Each step runs two passes (with and without classifier-free guidance), so 50 steps × 2 = 100 forward passes. The "trick" is to skip the guidance pass for the last ~20 steps, dropping to ~80 passes total with little quality loss.

**9.** FlashAttention is *lossless* — same math, fewer HBM reads. Sliding-window attention is *lossy* — each token attends only to a window of prior tokens, changing the math. Use FlashAttention always; use sliding-window only when the model was trained for it or when quadratic costs are intolerable.

**10.** Without KV cache: each new token must recompute attention over all prior tokens → quadratic time in sequence length. With KV cache: store K and V for prior tokens; each new token does linear work. Cost: GPU VRAM (often 50%+ of remaining memory after weights).

Problem Set 4

**1.** SM → "Streaming Multiprocessor — building block of the GPU". Tensor Core → "Hardware unit for MMA". CUDA Core → "Performs scalar arithmetic". L2 cache → "On-chip global cache shared across all SMs". HBM → "Off-chip high-bandwidth main memory".

**2.** Tensor Cores execute matrix multiply-accumulate, which is the dominant op in linear layers and attention. CUDA Cores handle scalar work; modern Transformer compute is ~all matmul.

**3.** (a) H100 or B200 for frontier scale (B200 is the new gold standard); H200 if bandwidth-bound. L4 is too weak. (b) **L4** — small model, cheap, sufficient for embeddings. (c) **B200** — needed for the memory + Tensor Core + FP4 support video generation requires.

**4.** NVLink (Blackwell ~1,800 GB/s) \> NVLink (Hopper ~900 GB/s) \> InfiniBand (≤400 Gb/s per NIC) \> Ethernet (≤100 Gb/s). NVLink: intra-node GPU-to-GPU; InfiniBand: node-to-node; Ethernet: generic.

**5.** InfiniBand is dramatically slower than NVLink. Tensor Parallelism requires all-reduce communication every layer — feasible on NVLink, prohibitive on InfiniBand. So multi-node uses Pipeline Parallelism (dense) or Expert Parallelism (MoE), both of which need less bandwidth.

**6.** (a) 7 compute slices, 8 memory slices. (b) Good for: serving multiple small models (TTS, embeddings, classifiers) where a full H100 would be wasted. Bad for: large LLMs that need full GPU memory and bandwidth.

**7.** (a) Cerebras WSE-3: wafer-scale chip with extreme memory bandwidth on-chip. (b) Groq LPU: composable language unit using SRAM for bandwidth. (c) TPU: AI-specific ASIC tightly integrated with Google's stack. (d) Qualcomm Cloud AI 100: power-efficient, derived from mobile GPU work. NVIDIA's moat: mature CUDA software ecosystem, deep tooling, decades of kernel work.

Problem Set 5

**1.** Kernel = function running on GPU. Graph = DAG of kernels for repeated workflows. Driver = low-level GPU interface. Runtime = developer-facing API for launching kernels.

**2.** Without fusion: Read \[1,2,3\] → write \[2,4,6\] → read \[2,4,6\] → write \[6,12,18\]. Two HBM round trips. Fusion combines into one kernel: read once, do both ops in registers, write once. Decode is memory-bandwidth bound, so eliminating HBM traffic is a direct win on TPS.

**3.** Pickle/bin formats can execute arbitrary Python on load (deserialization risk). safetensors holds only tensor data + memory-maps the file.

**4.** ONNX bundles weights *and* the execution graph (portable across hardware). safetensors is weights only. Prefer ONNX for portability; prefer safetensors when you're going straight to PyTorch or an inference engine.

**5.** (a) vLLM — broadest hardware, broadest day-zero support. (b) SGLang — strongest MoE support, especially DeepSeek/Kimi. (c) TensorRT-LLM — best raw perf, NVFP4 native. (d) PyTorch directly, or SGLang Diffusion / TensorRT for image gen.

**6.** Dynamo is an orchestration layer *above* the engines (vLLM/SGLang/TRT-LLM act as backends). Use it for very large MoE LLMs at very large traffic where KV-aware routing + disaggregation + multi-node parallelism are needed. Skip it for low traffic, small models, or simple deployments.

**7.** Pitfalls: (i) too few samples → outlier noise; (ii) no baseline → can't measure improvements; (iii) changing multiple variables at once → can't attribute; (iv) unrealistic traffic patterns → results won't match production. Also: optimizations that work together must also be tested individually.

**8.** Benchmarking tells you *what* the system does (P90 TTFT = 300 ms). Profiling tells you *why* (kernel X dominates). Profile when writing custom kernels, debugging unexplained slowdowns, or extracting the last few percent of performance.

Problem Set 6

**1.** Least → most sensitive: weights → activations → KV cache → attention. Attention is the most dangerous: every token's attention depends on every prior token's, so errors compound over thousands of tokens. Softmax especially is almost always left in original precision.

**2.** Floats have a sign + exponent + mantissa, giving them dynamic range to express both very large and very small numbers — critical for outliers in attention. Integers have just a sign + value bits, no exponent, so they smoothly quantize but clip outliers.

**3.** Smaller blocks (NVFP4: 16) mean each scale factor covers fewer values → less smoothing over outliers → better quality. MXFP4's 32-block size is coarser. NVFP4 adds a global 32-bit factor on top for extra precision. Tradeoff: more scale factors → more memory + compute overhead, but Blackwell Tensor Cores absorb this.

**4.** PTQ converts already-trained weights using calibration data (the only option for open models). QAT trains weights + scale factors jointly so the model is calibrated at deployment precision (e.g., GPT-OSS in MXFP4, Kimi K2 Thinking in INT4).

**5.** Perplexity, intelligence benchmarks (MMLU/SWE-bench), product-specific custom evals. Run multiple because LLMs are non-deterministic, and any single metric can mislead — you want differences indistinguishable from noise.

**6.** (a) Small separate draft model from same family, 10× smaller. (b) Graft additional decoder heads onto the target via fine-tuning to produce drafts directly. (c) Purpose-built draft model trained on the target's hidden states, generating up to 8 draft tokens. (d) Build an n-gram dictionary at prefill; during decode, use observed n-grams from the input as drafts.

**7.** Speculation uses spare compute. At high batch sizes, compute is saturated — speculation now competes with real generation and slows things down. Engines must dynamically disable speculation under load.

**8.** (a) Draft-target (no training needed). (b) N-gram (code has long repeated input). (c) EAGLE (highest acceptance rate, trained for the task).

**9.** (a) Everything from "Translate this French sentence to English:" is cached; only "Bonjour." / "Au revoir." differs after that. (b) Now the novel token ("Bonjour" / "Au revoir") is at position 1 — nothing after position 1 can be cached, even tokens that happen to match ("Translate this to English."). The rule: novel tokens last.

**10.** Speed: GPU VRAM (G1) \> CPU RAM (G2) \> local SSD (G3) \> networked SSD (G4). G1: hot prefix caches, active KV. G2: large LoRA libraries, KV offload via GB200 NVLink-C2C. G3: medium-warm caches. G4: global KV cache, cross-replica sharing.

**11.** VRAM = 1 × 405 × 1.8 = **729 GB**. At 180 GB/B200, need **5 B200s round up to 8 = full node** (1,440 GB).

**12.** (a) Tensor Parallelism within the 8-GPU node — lowest TTFT. (b) Expert Parallelism across nodes — MoE + InfiniBand-friendly. (c) TP within each node + Pipeline Parallelism between nodes (e.g., TP8PP2).

**13.** TP requires all-reduce sync on every layer. NVLink can absorb that; InfiniBand cannot — its bandwidth would dominate the critical path.

**14.** 5P3D = 5 prefill engines + 3 decode engines serving one model. Different counts because the workload's prefill-to-decode token ratio is rarely 1:1, and each engine can be sized for its bottleneck.

**15.** Conditions: (i) heavy traffic (100M-1B tokens/day for the model size); (ii) ≥100B-param model; (iii) prefill-heavy workload. Failures: (i) → low-traffic API for a small product (no need); (ii) → small Llama 8B (overhead exceeds win); (iii) → chat with mostly short messages and lots of cache hits (use horizontal scaling instead).

Problem Set 7

**1.** (a) 1K tokens per image inflates input sequences dramatically; multi-image or video pushes contexts into the tens of thousands. (b) KV cache quantization, EAGLE speculation, prefix caching for repeated images, Tensor Parallelism, disaggregation. (c) Downsampling input resolution and frame rate — quality vs. cost knob unique to vision input.

**2.** (i) Tokens process in parallel → no prefill/decode split → prefix caching and disaggregation are irrelevant. (ii) Models are small (\<8B) → multi-GPU parallelism wastes — scale horizontally. (iii) Batching is huge → one request can contain dozens-to-hundreds of inputs. (iv) Queuing is essential for backfill surges.

**3.** Matryoshka representations are nested embeddings where the *prefix* of the vector encodes more semantic meaning. You can store/transmit smaller vectors with graceful quality degradation — trading dimensionality for storage/compute.

**4.** Cosine similarity measures angular distance between vectors — embedding models are *only* useful via similarity comparisons, so cosine ≥99% between original and quantized outputs means downstream applications won't change behavior.

**5.** RTF = 3 hours / 9 seconds = (10,800 sec) / 9 sec = **1,200×**. Yes — the book cites optimized Whisper deployments hitting ~1,000× RTF.

**6.** Whisper kernels are already heavily optimized — runtime gains are nearly exhausted. WebSockets enable persistent connections so audio chunks stream continuously without reconnect overhead; VAD segments by silences (not arbitrary time) so words aren't severed. Both are infrastructure-layer wins, not model-layer.

**7.** TTFB is the first byte of audio — but a single "B" or stutter sound isn't intelligible. Time to first sentence is the first natural-language unit a user can comprehend, which actually defines perceived responsiveness.

**8.** Specialized models in each stage (VAD, ASR, LLM, TTS) outperform a unified speech-to-speech model on cost and quality. Open speech-to-speech isn't yet commercially viable; closed options are weaker than cascades.

**9.** Classifier-free guidance runs two passes per step (with prompt + without). Skipping guidance for the last ~20 of 50 steps drops total passes from 100 to 80. Late in generation the broad image structure is set; guidance primarily refines detail, which is more robust to skipping.

**10.** Video weights are small enough to *replicate* across all 8 GPUs (unlike LLMs that have to split weights). The bottleneck is attention over the massive latent space (3D: width × height × time). Ring attention splits the *attention computation* across GPUs by partitioning context, passing intermediates around the ring. Attention heads are independent and parallelize naturally.

**11.** Each step builds on the previous; errors accumulate across ~50 steps. Techniques: microscaling formats (MXFP8) for outlier preservation, selective quantization by step (keep early steps FP16, quantize later), and by layer (keep first/last layers high precision), specialized kernels like SageAttention.

Problem Set 8

**1.** CUDA toolkit + cuDNN + driver, Python packages, inference engine, system packages (ffmpeg). Pinning prevents upstream changes from silently breaking your build — critical because the dependency chain is long and fragile.

**2.** Utilization is a *lagging* indicator (already saturated by the time you measure). Traffic is *proactive* (you can scale before saturation). They can diverge — a few requests with 100K uncached tokens spike utilization without traffic volume.

**3.** If concurrency target \< batch size, replicas run half-full and you waste GPU. If concurrency target \> batch size, requests queue inside the engine and tail latency explodes.

**4.** GPU procurement, image loading, model loading, engine startup. The two most under your control: **image** (slim it down) and **engine** (cache compiled engines).

**5.** Static (wait until full — high queue time), dynamic (full OR timer — balanced), continuous/in-flight (token-level interleaving — best latency). Continuous is the default in vLLM, SGLang, TRT-LLM.

**6.** (a) Per-token: 2B × \$1.25/M + 800M × \$10/M = \$2,500 + \$8,000 = **\$10,500/month**. (b) Dedicated: 2,200 × \$3.50 = **\$7,700/month**. (c) Dedicated is **\$2,800/month cheaper (~27%)** — but factor in engineering time, on-call burden, GPU procurement risk.

**7.** Failures are expected — design for them. (a) Global consumer chat → **active-active** for transparent failover. (b) Compliance-critical batch → **active-passive** for clean failover audit trails.

**8.** 8 zones × 5 ms = **40 ms one-way ≈ 80 ms round trip**. That's 40% of the 200 ms TTFT SLA — unacceptable for chat. Route to a closer datacenter (e.g., EU).

**9.** Blue-green doubles GPU spend during cutover — 100-GPU blue requires 100-GPU green. Canary ramps traffic to the new deployment while autoscaling shrinks the old, keeping incremental cost manageable.

**10.** Network latency (TLS handshake, route to far region), client-side queueing or session overhead (TLS not reused), retries on the client. Roughly: ~30 ms TLS, ~40-80 ms geo, plus client-side delays.

Midterm answers

**M1.** B — TTFT reflects prefill (compute-bound). **M2.** B — decode is memory-bandwidth-bound. **M3.** C — 1000/5 = 200 TPS. **M4.** B — 800 \> 295, compute-bound. **M5.** B — quadratic to linear. **M6.** C — MMA. **M7.** B — GPUs within a node. **M8.** A — vLLM (NVIDIA, AMD, Intel, TPU). **M9.** B. **M10.** B — 7 compute slices.

**M11.** Prefill: processes the entire input sequence in parallel, builds the KV cache, compute-bound, drives TTFT. Decode: generates one token per forward pass autoregressively, memory-bandwidth-bound, drives TPS.

**M12.** Scale economics (token-volume crossover), latency requirements, uptime SLAs, custom model needs, compliance/data sovereignty, engineering team size to operate dedicated infrastructure.

**M13.** Attention(Q,K,V) = softmax(QK^T/√d_k) V. Without KV cache, each token attends to all prior tokens by recomputing K and V → N tokens generated × N tokens attended = O(N²). With KV cache, K and V are stored once → each new token does O(N) work.

**M14.** Combining two or more kernels into a single kernel to avoid intermediate HBM round trips. Decode is memory-bandwidth bound, so eliminating HBM traffic is directly a TPS win.

**M15.** Dense: every parameter participates in every forward pass. MoE: only a router-selected subset of experts activate per token. So a 235B MoE may have only 22B active params — efficient for single requests. But under batched load, different requests activate different experts → almost all weights end up active. VRAM sizing must still budget for the full param count, not just active params.

**M16.** Intensity = 5×10⁹ / 4×10⁷ = **125 ops/byte**. 125 \< 295 → **memory-bound** on H100.

**M17.** (a) 1 byte/param × 200B × 1.8 = **360 GB**. (b) **2 B200s** suffice (360 GB ≤ 360 GB), but realistically round up to 4 for KV cache + activations + headroom. (c) FP4: 0.5 byte × 200B × 1.8 = **180 GB → 1 B200** (tight; round to 2 in practice).

**M18.** (a) perceived TPS = 1000/8 = **125 TPS**. (b) total ≈ TTFT + 250 × 8 ms = 180 + 2000 = **2,180 ms**. (c) Decode (2000 ms) dominates over TTFT (180 ms) for a 250-token response.

**M19.** (a) H100: 989×10¹² / 3.35×10¹² ≈ **295 ops/byte**. H200: 989×10¹² / 4.8×10¹² ≈ **206 ops/byte**. (b) H200 wins decode because lower ops:byte means the GPU is balanced (or compute-bound) at lower arithmetic intensity, and higher absolute bandwidth means more bytes/sec for the memory-bound decode workload.

Final answers

**F1.** B (prefix caching → faster prefill → better TTFT). **F2.** B (NVFP4: 16-element blocks + global 32-bit factor). **F3.** D (EAGLE and n-gram both avoid a separate standalone draft model). **F4.** B. **F5.** B (Tensor Parallelism). **F6.** C (embedding inference has no shared prefix structure). **F7.** B (live dictation). **F8.** C. **F9.** C (token-level interleaving). **F10.** B. **F11.** D. **F12.** B. **F13.** B (419 failures / 54 days / 16,000 GPUs ≈ 1 per 50K GPU-hours). **F14.** B. **F15.** D (1000× — the book's optimized Whisper figure).

**F16.** Arithmetic intensity = ops/bytes for a specific algorithm; ops:byte = peak compute / memory bandwidth for the GPU. If arithmetic intensity \> ops:byte → compute-bound. If less → memory-bound.

**F17.** FP8 halves bits per value → halves bytes moved per value (2× effective bandwidth) and lower-precision Tensor Cores execute at 2× FLOPS.

**F18.** EAGLE: purpose-built draft model trained on the target's hidden states. Up to 8 draft tokens with high acceptance. Need training infrastructure. N-gram: build dictionary at prefill, use observed input n-grams as drafts. No training. Best for code-completion-style workloads where output looks like input.

**F19.** Requests first try the decode engine; only if input is large and uncached do they get routed to a prefill engine for disaggregated handling. Real traffic is mixed, so unconditional disaggregation wastes resources on short/cache-hit requests.

**F20.** KV cache turns attention from quadratic to linear; it's the dominant memory consumer in long-context inference. Optimizations: (i) prefix caching across requests, (ii) PagedAttention (fragmented page-based storage), (iii) KV cache quantization (FP8/MXFP8), (iv) tiered storage (G1-G4), (v) cache-aware routing.

**F21.** GPU procurement (negotiate with cloud provider; reserved/spot mixes). Image loading (slim images, minimal layers). Model loading (cached weights in same datacenter as GPUs; avoid baking huge weights into images). Engine startup (cache compiled engines on matching GPU+CUDA combinations).

**F22.** Carry-overs: KV cache quantization, prefix caching, speculation, Tensor Parallelism, disaggregation. New tradeoff: downsampling input resolution / frame rate to control token count.

**F23.** Good: development environments (latency irrelevant for first request), periodic production workloads (nightly batch, business-hours-only agents). Bad: latency-sensitive light traffic (a few RPS during business hours but every user needs \<1s response) — pay-per-token APIs better.

**F24.** Failures happen often (~1 per 50K GPU-hours); active-active means a regional failure is transparent (other regions absorb), critical for global consumer products with strict UX expectations. Active-passive adds failover latency users would notice.

**F25.** Voice apps stream audio chunks bidirectionally. HTTP is request-response, not naturally bidirectional. WebSockets maintain a persistent two-way connection: audio in, transcription/TTS audio out, all over one socket. Reduces handshake overhead and supports continuous streaming for natural conversation.

**F26.** (a) **H100 SXM** is sufficient and well-tuned; **TensorRT-LLM** for tightest performance on stable workload; **FP8 quantization** on weights (sweet spot, low quality risk for fine-tuned model — *validate*). (b) **No disaggregation** — 50 concurrent users is below the threshold; horizontal replicas are simpler. (c) **Yes, prefix caching** — heavy prefix overlap. App team must ensure shared system prompt and any reused chunks appear first; novel tokens (user input) last. (d) Signals: traffic + utilization. Scale-up: short window (seconds). Scale-down delay: 5+ minutes (business-hours-spiky). **Don't scale to zero** during business hours (cold-start latency would violate the 400 ms TTFT SLA). Maybe scale to 1 replica overnight.

**F27.** (a) Inference time is unchanged (250 ms) but end-to-end jumped — the bottleneck is **outside the model**: infrastructure or client. (b) Hypotheses: (i) queueing — autoscaler can't keep up with traffic growth (check queue depth, replica count); (ii) network/region — a region is congested or capacity-constrained (check per-region P95 latency); (iii) cold-start churn — scale-down too aggressive, frequent re-warming (check replica startup events); also: (iv) load balancer routing change, (v) certificate / TLS issue. (c) Multi-cloud response: open capacity in a second region/cloud, raise max-replicas, lengthen scale-down delay, and route a portion of traffic geographically away from the saturated region (geo-aware load balancing). If urgent: increase min replicas as a stop-gap.

**F28.** (a) **vLLM** — best day-zero support; community usually ships integrations same day. SGLang also strong for MoE; TRT-LLM lags on new architectures. (b) VRAM = 1 byte × 800 × 1.8 = **1,440 GB → exactly one node of 8 B200s** at 180 GB each (tight; in practice plan two nodes). (c) MoE → **Expert Parallelism across the node** (low inter-GPU comm, high throughput). If multi-node, **EP across nodes** with InfiniBand. Skip Tensor Parallelism for multi-node. (d) (i) Compare quantized vs. native perplexity on a small held-out set; (ii) MMLU / SWE-bench against the model card's reported numbers; (iii) product-specific eval (your customer use cases). (e) Day-zero deployments often use **pre-release engine builds** that may be buggy; pin the build hash and plan a rebuild on the stable release within the first 1-2 weeks. Add extra observability around quality and crash rates.

---

# Appendix — Difficulty, Prerequisites, and Back-of-Envelope Drills

This appendix layers three things onto the problem sets above:

1. A **per-problem-set index** showing difficulty (★ required / ☆ stretch), prerequisite concept IDs (from `docs/kb/concepts.json`), and an expected time-to-solve so students can budget a study session.
2. One additional **back-of-envelope numerical drill** per problem set (D1–D8), built around real GPU/model specs, with full worked solution. These are the "if you only do 10 extra problems all semester, do these" set.
3. A **midterm and final difficulty index** so instructors can target review sessions to the items their class actually struggled on.

Conventions:

- ★ = required for course mastery; you should be able to solve unaided within the time bound.
- ☆ = stretch; tests synthesis or speed. Acceptable to skip on a first pass.
- "Time" is *median* solve time for a prepared student. Add 50% if you're rusty.

---

## Per-problem-set index

### Problem Set 1 — What is Inference? (target 30 min)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 1 | ★ | 3 min | `inference-vs-training` |
| 2 | ★ | 4 min | `ai-stack-overview` |
| 3 | ★ | 6 min | (all 6 runtime techniques) |
| 4 | ★ | 4 min | `ai-stack-overview` |
| 5 | ★ | 5 min | `ai-stack-overview`, `inference-cost` |
| 6 | ☆ | 5 min | `ai-stack-overview` |
| 7 | ★ | 1 min | (six techniques) |
| 8 | ★ | 1 min | `inference-cost` |

### Problem Set 2 — Prerequisites (target 45 min)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 9 | ★ | 2 min | `latency-throughput`, `token` |
| 10 | ★ | 4 min | `latency-throughput` |
| 11 | ★ | 4 min | `latency-throughput` |
| 12 | ★ | 6 min | `latency-throughput`, `inference-cost` |
| 13 | ★ | 7 min | `inference-cost` |
| 14 | ★ | 3 min | `latency-throughput` |
| 15 | ☆ | 6 min | `latency-throughput` |
| 16 | ★ | 1 min | `latency-throughput` |
| 17 | ★ | 1 min | `inference-cost` |

### Problem Set 3 — Models, Attention, Bottlenecks (target 60 min — most calculation-heavy)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 18 | ★ | 4 min | `transformer-architecture` |
| 19 | ★ | 5 min | `self-attention` |
| 20 | ★ | 7 min | `kv-cache` |
| 21 | ★ | 7 min | `kv-cache` |
| 22 | ★ | 8 min | `self-attention`, `flash-attention` |
| 23 | ☆ | 8 min | `flash-attention`, `gpu-memory-hierarchy` |
| 24 | ★ | 6 min | `transformer-architecture` |
| 25 | ★ | 1 min | `self-attention` |

### Problem Set 4 — GPU Hardware (target 30 min)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 26 | ★ | 4 min | `gpu-memory-hierarchy` |
| 27 | ★ | 5 min | `gpu-generations` |
| 28 | ★ | 5 min | `gpu-memory-hierarchy` |
| 29 | ☆ | 6 min | `gpu-generations`, `tensor-parallelism` |
| 30 | ★ | 4 min | `gpu-generations` |
| 31 | ★ | 1 min | `gpu-memory-hierarchy` |

### Problem Set 5 — Software Stack (target 30 min)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 32 | ★ | 4 min | `cuda-stack` |
| 33 | ★ | 5 min | `inference-engines` |
| 34 | ★ | 5 min | `inference-engines`, `continuous-batching` |
| 35 | ★ | 5 min | `inference-engines` |
| 36 | ☆ | 5 min | `cuda-stack` |
| 37 | ★ | 1 min | `inference-engines` |

### Problem Set 6 — Performance Techniques (target 75 min — half-course capstone)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 38 | ★ | 6 min | `quantization` |
| 39 | ★ | 7 min | `speculative-decoding` |
| 40 | ★ | 7 min | `paged-attention`, `kv-cache` |
| 41 | ★ | 6 min | `tensor-parallelism` |
| 42 | ★ | 8 min | `moe`, `tensor-parallelism` |
| 43 | ★ | 9 min | `disaggregated-serving` |
| 44 | ☆ | 10 min | `mla`, `kv-cache` |
| 45 | ★ | 6 min | (synthesis of all Ch.5 techniques) |
| 46 | ★ | 1 min | `quantization` |

### Problem Set 7 — Modalities (target 30 min)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 47 | ★ | 5 min | (image gen) |
| 48 | ★ | 5 min | (embeddings) |
| 49 | ★ | 5 min | (ASR) |
| 50 | ☆ | 6 min | (video gen, context parallelism) |
| 51 | ★ | 1 min | (modality bottlenecks) |

### Problem Set 8 — Production (target 45 min)

| Q# | Difficulty | Time | Concept IDs |
|---|---|---|---|
| 52 | ★ | 5 min | `inference-cost` |
| 53 | ★ | 6 min | `inference-cost` |
| 54 | ★ | 6 min | `inference-cost` |
| 55 | ★ | 7 min | `inference-cost`, `ai-stack-overview` |
| 56 | ☆ | 8 min | `inference-cost` |
| 57 | ★ | 1 min | `inference-cost` |

### Midterm (Chapters 0–4) — target 90 min

- Conceptual section: ★ required, ~2 min/question.
- Calculation section: ★ required, ~5 min/question (mostly Chapter 2 material — KV cache, arithmetic intensity).
- Design section: 1 ★ required, 1 ☆ stretch; ~15 min each.
- Topic emphasis: KV cache sizing, arithmetic intensity, latency metric conversions, three-layer model. **If your class struggled on PS-3, the midterm will hurt.**

### Final (Full Course) — target 150 min

- F1–F15: rapid-fire MCQ, ★ required, ~1 min each.
- F16–F25: short answer, mix ★/☆, ~5 min each.
- F26–F28: full design problems, ★ required for F26, ★ for F27, ☆ for F28; ~25–35 min each.
- Topic emphasis: Chapter 5 (performance techniques) and Chapter 7 (production) carry the most weight. F28 is the one that separates A-grades from A+s.

---

## Drill problems — one extra back-of-envelope per module

These eight drills are designed to be quick — 8–12 minutes each — but force you to *commit to a number* using only what's in your head. Don't open a calculator until you've made a guess.

### D1. Cost crossover, training vs. inference

A startup spends **$300K** to train a 13B model. After launch, they serve **2 million daily users**, each issuing **3 chat turns/day** averaging **600 tokens output** per turn. A single H100 at FP8 serves their model at **~3,500 output tokens/sec**. H100 rate: **$2/hr**.

(a) Daily output tokens? (b) H100s needed for steady-state load? (c) Daily inference cost? (d) After how many days does cumulative inference cost equal the one-time training cost?

**Solution.**

(a) 2M users × 3 turns × 600 tokens = **3.6 B tokens/day**.

(b) Tokens/H100/day = 3500 × 86,400 = ~3.02 × 10⁸ ≈ **302 M tokens/H100/day**. Needed: 3.6 × 10⁹ / 3.02 × 10⁸ ≈ **12 H100s** (round up for headroom: ~15).

(c) 12 × 24 × $2 = **$576/day** (or $720 with headroom).

(d) $300K / $576 ≈ **521 days ≈ 17 months**. With headroom: ~14 months. Inference passes training cost in the second year.

*Concept IDs: `inference-vs-training`, `inference-cost`.*

### D2. Tail-latency arithmetic

A chat API has these per-request latencies measured over 10K requests, sorted ascending: P50 = 180 ms, P90 = 360 ms, P99 = 920 ms, P99.9 = 2400 ms. Your product SLA is "**P99 < 800 ms**." A new feature adds **120 ms** to every request, uniformly.

(a) New P50, P90, P99, P99.9? (b) SLA status? (c) Customer support reports complaints from "about 1 in 100 users." Which percentile are those users seeing?

**Solution.**

(a) Uniform shift: just add 120. P50 = 300, P90 = 480, **P99 = 1040**, P99.9 = 2520.

(b) **SLA BROKEN** at P99 (1040 > 800).

(c) "1 in 100" = the P99. They're seeing ~1 sec responses, which is the visible boundary where chat starts to feel laggy.

*Concept IDs: `latency-throughput`.*

### D3. KV cache scaling

Llama-3.1 70B has **80 layers, 64 attention heads (8 KV heads after GQA), head dim 128, FP16**. You want to serve it on a node of **8 H100s (640 GB total HBM)** with FP16 weights.

(a) Weight bytes? (b) Bytes of free HBM for KV cache? (c) KV cache bytes per token? (d) Max concurrent 8K-context requests? (e) If you switch weights and KV cache to FP8, how does (d) change?

**Solution.**

(a) 70B × 2 bytes = **140 GB**.

(b) 640 − 140 = **500 GB free** (real value lower after activations + framework overhead; call it ~420 GB).

(c) 2 (K+V) × 80 layers × 8 KV-heads × 128 dim × 2 bytes = **327,680 bytes/token ≈ 320 KiB/token**.

(d) At 8K tokens/request: 320 KiB × 8192 ≈ 2.5 GiB/request. 420 / 2.5 ≈ **~165 concurrent requests**.

(e) FP8 weights: 70 GB (saves 70 GB). FP8 KV: 160 KiB/token → 1.25 GiB/request. New free HBM ≈ 490 GB → **~390 concurrent requests** (~2.4× more). FP8 roughly doubles throughput on this workload — typical reported speedup.

*Concept IDs: `kv-cache`, `quantization`, `gpu-memory-hierarchy`.*

### D4. NVLink vs. InfiniBand penalty

An 80-layer model does Tensor-Parallel all-reduce **once per layer per token**. NVLink 4: **900 GB/s** between GPUs in a node. InfiniBand HDR: **50 GB/s** between nodes. Each all-reduce moves **~16 KB** per GPU per layer (typical hidden-state slice).

(a) Time per all-reduce on NVLink? On InfiniBand? (b) Total per-token all-reduce time, intra-node TP vs. cross-node TP? (c) At a 10 ms/token decode budget, is cross-node TP viable?

**Solution.**

(a) 16 KB / 900 GB/s ≈ **17 ns**. 16 KB / 50 GB/s ≈ **320 ns**. Plus latency floor (~1 µs each).

(b) Realistic per-reduce (latency-dominated, not bandwidth at this size): **~2 µs** on NVLink, **~10 µs** across IB. Per token (80 layers): **~160 µs** on NVLink, **~800 µs** across IB. With contention and synchronization it's typically several times this — call it ~0.5 ms intra-node vs. ~3-5 ms cross-node.

(c) 10 ms budget: intra-node TP fits easily; cross-node TP eats **30–50% of your token budget on communication alone**. This is why production capstones TP at 8 (one node) and use pipeline or expert parallelism for cross-node scaling.

*Concept IDs: `tensor-parallelism`, `gpu-memory-hierarchy`.*

### D5. Kernel launch overhead vs. CUDA graphs

A naive PyTorch transformer forward launches **~30 kernels per layer × 32 layers = 960 kernels per token**. H100 kernel launch overhead: **~5 µs**.

(a) Launch overhead per token? (b) If decode target is 10 ms/token, what fraction is launch overhead? (c) Fused kernels collapse 30→4 launches/layer. New overhead per token? (d) CUDA graphs eliminate per-step launch overhead almost entirely. Realistic benefit on top of fused kernels?

**Solution.**

(a) 960 × 5 µs = **4.8 ms/token** of pure launch overhead.

(b) **48% of the token budget** is dispatch overhead, before any compute happens. Naive PyTorch decode is non-viable in production.

(c) 4 × 32 × 5 µs = **0.64 ms/token** (6% of budget — acceptable).

(d) CUDA graphs save the residual ~0.5 ms, getting overhead near-zero. The big win was already from kernel fusion; CUDA graphs are the polish. This is why every production engine uses fused kernels + CUDA graphs.

*Concept IDs: `cuda-stack`, `inference-engines`, `continuous-batching`.*

### D6. Quantization × speculation stacked speedup

Baseline: **Llama-3.1 70B FP16** on H100, decode = **40 ms/token**. Apply each optimization in sequence:

1. FP8 weights + KV cache → typical 2.5× decode speedup.
2. Add speculative decoding, draft = 1B model at 2 ms/token, 5-token speculation, 3/5 acceptance rate.

(a) Post-quantization decode latency? (b) Per-spec-cycle wall time? (c) Effective time per accepted token? (d) Total speedup vs. baseline? (e) Quality risk to flag?

**Solution.**

(a) 40 / 2.5 = **16 ms/token** (FP8 target verify).

(b) 5 draft tokens × 2 ms + 1 target verify × 16 ms = 10 + 16 = **26 ms/cycle**. Yields 3 accepted tokens.

(c) 26 / 3 = **~8.7 ms/accepted token**.

(d) 40 / 8.7 ≈ **4.6× speedup vs. FP16 baseline**. Real-world: 3.5–4.5× is typical (acceptance rate varies).

(e) FP8 typically costs **0.1–0.3 MMLU points** — verify on your eval suite. Speculation is *lossless* by construction (target model verifies every draft token).

*Concept IDs: `quantization`, `speculative-decoding`.*

### D7. ASR Real-Time Factor and chunking

Whisper-large-v3 on H100: **1 min audio → 3 sec compute**. For **real-time captioning** (live stream), you process **100 ms audio chunks** and need each chunk's transcription back within **300 ms** to feel natural.

(a) Baseline RTF? (b) Per-chunk compute time (linear scaling)? (c) Does baseline meet the 300 ms target? (d) Distil-Whisper-large is ~2× faster. Does it meet the target? (e) Why is the model+chunking decision THE engineering question for ASR?

**Solution.**

(a) RTF = 3 / 60 = **0.05** (20× faster than real-time).

(b) 100 ms audio × 0.05 = **5 ms compute** for the audio processing alone — but each chunk re-runs an encoder pass plus partial decode. Realistic per-chunk wall time: **~200–250 ms** including engine overhead.

(c) **Barely** — you have ~50 ms margin. Any network jitter blows it.

(d) **Yes**, comfortably — Distil-Whisper cuts the wall-time to ~100–120 ms per chunk, giving ~180 ms margin.

(e) Because RTF alone doesn't capture it: you need *chunk-level* latency, which depends on encoder overhead per call. The decision is "small-model + small-chunks" vs. "big-model + bigger-chunks." Get it wrong and your caption lags the speaker by a sentence.

*Concept IDs: (see Glossary B.18 on memory-bound vs compute-bound).*

### D8. Multi-cloud capacity arbitrage

You run **100 H100s** continuously for a year. Pricing (mid-2026): **AWS on-demand $98/hr per 8-GPU p5** (≈ $12.25/GPU-hr), **Lambda 1-yr reserved $2/GPU-hr**, **CoreWeave 1-yr reserved $2.50/GPU-hr**. You want to keep **20%** of capacity on AWS for burst/region redundancy and split the rest 60/40 Lambda/CoreWeave for vendor diversity.

(a) Annual cost on all-AWS? (b) Annual cost on the mixed plan? (c) Savings, absolute and percentage? (d) What's the hidden cost of the multi-cloud plan that the spreadsheet doesn't show?

**Solution.**

(a) 100 × $12.25 × 24 × 365 = **$10.73 M/yr**.

(b) AWS: 20 × $12.25 × 24 × 365 = $2.15 M. Lambda: 48 × $2 × 24 × 365 = $0.84 M. CoreWeave: 32 × $2.50 × 24 × 365 = $0.70 M. Total = **$3.69 M/yr**.

(c) Saves **$7.04 M/yr** = **~66% reduction**. Real-world numbers regularly come out in this range.

(d) Hidden costs: (i) engineering time to maintain multi-cloud orchestration; (ii) cross-cloud data egress (small but real); (iii) on-call expanded across 3 providers; (iv) feature parity gaps (one cloud may lack a specific GPU SKU or networking feature). Rule of thumb: the savings are real but the engineering team grows by ~1–2 SREs to manage it.

*Concept IDs: `inference-cost`, `ai-stack-overview`.*

---

## Recommended drill schedule

If you've finished all 8 problem sets and want to drill before the final exam, do these 8 drills in this order over **two evenings**:

| Evening 1 (~50 min) | Evening 2 (~50 min) |
|---|---|
| D1 (cost crossover) | D5 (kernel launches) |
| D2 (tail latency) | D6 (quant × spec) |
| D3 (KV scaling) | D7 (ASR RTF) |
| D4 (NVLink vs. IB) | D8 (multi-cloud) |

If you can solve any 6 of the 8 without a calculator in under 12 minutes each, you're in good shape for the final.
