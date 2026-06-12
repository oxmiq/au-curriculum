<!-- Slide number: 1 -->

INFERENCE
ENGINEERING
A 10-week course for undergraduate CS / ML students
Companion to Inference Engineering by Philip Kiely (Baseten Books, 2026)
Lecture 1 → 10  ·  ~10 slides per lecture

> **Source & permitted use.** This slide deck is an instructor-authored companion derived from *Inference Engineering* by Philip Kiely (Baseten Books, 2026). It paraphrases and adapts material from that book for internal use within the Andhra University / Oxmiq curriculum only. **Do not redistribute, mirror, or publish outside this course.** Students and instructors should obtain the original book for canonical text, code samples, and references. If a formal license or permission grant for this material is established, replace this notice with a pointer to the source agreement.

### Notes:
Open with this slide on screen as students walk in. While you're waiting, mention you'll spend a few minutes orienting them to the discipline before getting to the technical content.

This deck is designed for ~50 minute lectures. Slides progress one concept per slide; expect to spend 3-5 minutes on each on average, more on calculations.

Reading prerequisites for this lecture are in the Pre-Lecture Reader, Chapter 1 ("AI in production"). Confirm students have skimmed it.

<!-- Slide number: 2 -->

Course agenda
Lecture 1 — What is Inference? The three-layer model
Lecture 2 — Prerequisites: scale, evals, latency metrics
Lecture 3 — Neural networks and LLM mechanics
Lecture 4 — Image generation, bottlenecks, attention
Lecture 5 — GPU hardware: architectures and generations
Lecture 6 — The software stack: CUDA to inference engines
Lecture 7 — Quantization and speculative decoding
Lecture 8 — Caching, parallelism, disaggregation
Lecture 9 — Modalities: vision, embedding, audio, video
Lecture 10 — Production: containers, autoscaling, multi-cloud

### Notes:
Walk through the agenda quickly. Highlight the spine: Lectures 1-2 = orientation, Lectures 3-4 = how models actually work, Lectures 5-6 = hardware and software stack, Lectures 7-8 = optimization techniques, Lectures 9-10 = beyond LLMs and beyond one box.

Two transitions to call out: Lecture 4 is where the math starts to bite (arithmetic intensity), and Lecture 7 is where you go from understanding inference to optimizing it. Tell students those are the two weeks they should clear their calendars.

Mention that problem sets parallel the lectures one-for-one and the midterm covers Lectures 0-4.

<!-- Slide number: 3 -->

LECTURE 01
What is Inference?
Training vs. inference. The three-layer model. The six runtime techniques.
Inference Engineering · Philip Kiely

### Notes:
LECTURE 1 START. Use this slide as a moment to set tone. The point of today is: inference engineering is a real discipline with a real surface area, and three layers separate the concerns.

Optional opening question: "How many of you have used ChatGPT today?" (most). "How many of you can explain what happened on the server side between when you hit enter and when the first word appeared?" (almost none). That's what this course is for.

Today is mostly definitions and framing. The pace will pick up next week.

<!-- Slide number: 4 -->

Learning objectives
Define inference and contrast it with training.
Name the three layers of an inference stack.
List the six runtime techniques used to optimize a single instance.
Explain why infrastructure is a separate problem from runtime optimization.

### Notes:
Read these out one by one. The third one (six runtime techniques) is the one to memorize — they'll come back every week.

Note: the order matters. We start with definitions (1, 2), then the conceptual model (3 = three layers, 4 = six techniques), and finally the why-this-matters (5 = infrastructure). If any single student walks out remembering only one thing, it should be the six techniques.

<!-- Slide number: 5 -->

Training vs. inference

Training
Learns model weights from data
One-time / periodic (capital expense)
Massive compute clusters
Backpropagation

Inference
Serves the trained model to users
Continuous (operational expense)
Production GPUs near users
Forward passes only
Once you ship, almost every GPU-hour your company pays for is spent on inference.

### Notes:
Most students intuitively think training is harder than inference because it requires GPUs, expensive datasets, careful experimentation. That's true, but it's only half the story.

The framing to hammer: training is a capital expense (one-time per model); inference is an operational expense (every request, every day, forever). For a company like OpenAI, well over 90% of their compute spend is on inference, not training.

A useful analogy: building a factory vs. running it. Building is expensive, but the bills come from running. Same with models.

Discussion prompt: "Why do AI companies have inference engineering teams but not training engineering teams in the same way?" Answer: because every product company runs inference; only a handful train.

<!-- Slide number: 6 -->

The three layers of an inference stack
Runtime — make one model on one GPU as fast as possible
CUDA → PyTorch → inference engines (vLLM, SGLang, TensorRT-LLM)
Infrastructure — scale across clusters, regions, clouds
Autoscaling, load balancing, multi-cloud capacity, GPU procurement
Tooling — the right level of developer abstraction
Too low: drowning in YAML. Too high: can't optimize mission-critical work.
All three matter. Optimizing one while the others are broken is wasted effort.

### Notes:
The three-layer model is the spine of the course. Almost every concept later in the course belongs to exactly one of these three layers.

Runtime = one GPU, one model, "make it fast." This is where CUDA kernels, FlashAttention, quantization, speculation live. Lectures 3-7.
Infrastructure = many GPUs, many regions, "make it scale." This is autoscaling, load balancing, multi-cloud. Lectures 8 and 10.
Tooling = the developer abstraction. This is which inference engine you pick, which platform you deploy on. Lectures 6 and 10.

Common mistake: thinking only runtime matters because it's the most technically deep. In practice, infrastructure problems sink more products than runtime ones.

<!-- Slide number: 7 -->

The six runtime techniques (memorize these)
Batching
Run requests in parallel, weaving them at the token level → higher throughput
Caching
Reuse the KV cache for shared prefixes across requests → better TTFT
Quantization
Lower numeric precision → more FLOPS and less memory bandwidth needed
Speculation
Draft + validate multiple tokens per forward pass during decode → higher TPS
Parallelism
Split a model across GPUs to fit larger models or run faster
Disaggregation
Separate prefill and decode onto independent workers
These techniques generalize beyond LLMs to VLMs, image gen, ASR, TTS, embeddings, video.

### Notes:
This slide is the most important slide in the entire course. The six techniques recur in every following lecture. If students remember nothing else from today, they should remember this list and what each one does.

Walk through each one with a one-sentence motivation:
- Batching: GPUs are great at parallel work; serve many requests at once.
- Caching: don't redo the same prefill twice; reuse the KV cache.
- Quantization: lower precision = more FLOPS, less memory traffic.
- Speculation: generate cheap draft tokens; validate with the real model.
- Parallelism: when one GPU isn't enough, use many.
- Disaggregation: prefill and decode have different needs; separate them.

The footer (these generalize beyond LLMs) is a tease for Lecture 9.

<!-- Slide number: 8 -->

Why infrastructure matters
A perfectly optimized single replica is still finite — it hits a traffic ceiling.
Phases of infrastructure growth as you scale:
Small scale — autoscaling: spin replicas up and down with traffic.
A few hundred GPUs — capacity becomes the constraint; spread across regions.
Largest scale — silos kill you. Treat all GPUs across clouds as one pool.
Why this matters: a faster GPU doesn't solve a region-out-of-capacity problem.

### Notes:
The point of this slide: a single replica is finite. Even a maxed-out B200 will eventually be overwhelmed by traffic. Solving that is a systems problem, not a CUDA problem.

The three phases on the slide map roughly to startup-vs-mid-stage-vs-enterprise concerns:
- Small scale: autoscaling. Most teams stop here.
- A few hundred GPUs: GPU capacity becomes the actual constraint. You can't just "buy more" — vendors are sold out.
- Largest scale: silos kill you. Multi-cloud is mandatory.

Cite the Llama 3 failure number from the book if you want a hard data point: 419 failures in 54 days on 16K GPUs = 1 per 50K GPU-hours. Failure is the default at scale.

<!-- Slide number: 9 -->

Recap — Lecture 1
Inference = serving trained models in production.
Three layers: runtime, infrastructure, tooling. Each is a separate discipline.
Six runtime techniques: Batching, Caching, Quantization, Speculation, Parallelism, Disaggregation.
Infrastructure problems start at hundreds of GPUs. Multi-cloud is the endgame.
Next time: how to measure what you're optimizing.

### Notes:
Recap. The 30-second version of today: inference is the half of AI that lives in production. It splits into three layers. Six runtime techniques are the verbs of the rest of the course.

End-of-lecture question: "Of the six runtime techniques, which two do you think apply to image generation? Which three apply to embedding models?" Don't expect right answers; we cover this in Lecture 9. The point is to plant the question.

For next time: pre-lecture reader chapter 2 (Latency, probability, percentiles). Probably the most math-heavy reader of the course.

<!-- Slide number: 10 -->

LECTURE 02
Prerequisites Before You Optimize
Scale and specialization · model selection · TTFT, TPS, percentiles
Inference Engineering · Philip Kiely

### Notes:
LECTURE 2 START. Today is metrics — how to measure what you're optimizing. Without these definitions, the rest of the course is unfalsifiable.

The lecture has two halves. First half (slides 11-15): qualitative — what kind of app, what kind of model. Second half (16-19): quantitative — latency formulas, percentiles, end-to-end vs. inference time.

If you have time, demo a latency dashboard at the end. Showing P50 vs P99 on real traffic drives the point home in a way slides can't.

<!-- Slide number: 11 -->

Learning objectives
Decide between shared APIs and dedicated deployments.
Pick the smallest model that passes your evals.
Differentiate fine-tuning from distillation.
Compute TTFT, ITL, and perceived TPS. Read latency percentiles correctly.
Separate inference time from end-to-end time.

### Notes:
Quick read-through. Emphasize the latency-formula one (item 4) — that's a calculation we will use in every problem set.

<!-- Slide number: 12 -->

Shared inference vs. dedicated deployments

Shared inference (APIs)
Pay per million tokens
Zero engineering overhead
No control over latency
Provider uptime caps you
Cost scales linearly with usage

Dedicated deployment
Per-GPU-hour pricing
Tunable latency + uptime
Custom / fine-tuned models
Engineering surface area grows
Cheaper at scale
Switch to dedicated when scale, specialization, or orchestration demand it.

### Notes:
The shared-vs-dedicated dichotomy is something every team faces. Frame it as a maturity arc:
1. Early stage / proof-of-concept: shared APIs. Pay per token.
2. Product-market fit, growing usage: still shared, but bill is becoming significant.
3. Predictable usage, clear quality bar: switch to dedicated.

The switch is rarely a clean victory. You trade per-token cost for per-GPU-hour cost (sometimes higher in absolute dollars), but you gain control over latency, model choice, and uptime.

Class discussion: "Imagine you're a YC startup at $50K/month on OpenAI's API. Is it time to switch?" Real answer: "It depends on whether your scale will keep growing and whether you need a custom model." Don't conflate cost with the only consideration.

<!-- Slide number: 13 -->

App type → what to optimize

| Application | Online or offline? | Optimize for |
| --- | --- | --- |
| Customer-support chat | Online | Latency |
| Code completion in IDE | Online | Latency |
| Real-time voice agent | Online | Latency |
| Back-catalog transcription | Offline | Throughput |
| Document embedding for RAG | Offline | Throughput |
| Catalog moderation | Offline | Throughput |

### Notes:
Quick reference. Walk through 2-3 examples per row.

Online → latency = users are waiting. Customer support, code completion, voice. Halving latency makes the product feel better.

Offline → throughput = no human in loop. Catalog transcription, document embeddings, batch moderation. Halving throughput means halving GPU bill.

Common confusion: "isn't lower latency always better?" Answer: yes for the user, but optimizing latency usually costs throughput. You can't have both.

<!-- Slide number: 14 -->

Model selection — first principles
All else equal, smaller models are faster and cheaper.
Most important model-performance decision: which model you pick at all.
Practical rules:
Start on frontier APIs while finding product-market fit.
At scale, pick the smallest model that still passes your evals.
Stick with popular architectures — best inference engine support.

### Notes:
Single most important slide for model selection. The biggest decision is NOT engine, NOT quantization — it's which model to use at all.

The "smallest model that passes your evals" framing matters because students often overshoot. They reach for frontier 671B-param models when a 7B fine-tune would suffice for the task.

Counter-example to drive the point: a fine-tuned Llama 3 8B for SQL generation will outperform GPT-5 zero-shot on schema-specific queries. Smaller, faster, cheaper, and better.

The "popular architectures" advice is practical: vLLM and SGLang have day-zero integrations for Llama, Qwen, DeepSeek. If you pick a niche architecture, you'll be writing custom kernels.

<!-- Slide number: 15 -->

Fine-tuning vs. distillation

Fine-tuning
Same architecture, new weight values
Adapts a model to a domain
Best for narrow domains (e.g., text-to-SQL)
Needs labeled data

Distillation
Different (smaller) architecture
Student emulates teacher distributions
Best when only a huge teacher exists
Example: DeepSeek-R1 distilled onto Llama 3
Both inherit some teacher behavior. Distillation captures probability surfaces, not just answers.

### Notes:
Both adapt a pretrained model, but in different ways:

Fine-tuning = same model, new weights. Targets a domain (text-to-SQL, medical chat). Best when you have a good dataset and a narrow scope.

Distillation = smaller model, mimics teacher's probability distributions. Targets size reduction. Best when only a huge model exists and you need cheap inference.

DeepSeek-R1's 671B-param release was distilled onto Llama 3 8B and Qwen 2.5 7B because nobody wanted to serve a 671B model. Those distilled versions still demonstrate strong reasoning despite being a fraction of the size.

Common confusion: students think LoRAs are a third method. LoRA is actually a fine-tuning *technique* — low-rank adapter weights. We mention it in Lecture 7's caching discussion.

<!-- Slide number: 16 -->

LLM latency metrics

TTFT  — Time to First Token (latency, prefill-driven)
TPS   — Tokens Per Second (latency or throughput depending on which)
ITL   — Inter-Token Latency (ms between tokens during decode)

perceived TPS = 1000 / ITL_ms

Example: ITL = 10 ms  →  100 TPS per user
Perceived TPS = one user's experience. Total TPS = whole-service throughput.
TTFT comes from prefill (compute-bound). TPS comes from decode (memory-bound).
These are the two metrics every LLM product tracks.

### Notes:
The latency-metrics formula slide. Step through it slowly. Math will appear here.

TTFT vs. TPS is the central duality of LLM inference. They map to prefill (compute-bound) and decode (memory-bandwidth-bound) — we cover this in Lecture 3 and again in Lecture 4. For now: TTFT is "how snappy did the app feel?" TPS is "how fast does it stream after that?"

ITL = inter-token latency = milliseconds between tokens. Convert via TPS = 1000 / ITL. This is the most common calculation on problem sets.

Do an example aloud: "If ITL is 10 ms, what's TPS? 100. If TPS is 80, what's ITL? 12.5 ms."

Distinguish *perceived* TPS (one user's experience) from *total* TPS (whole service throughput). These are constantly confused in industry blog posts.

<!-- Slide number: 17 -->

Latency percentiles

| Percentile | Meaning | Interpretation |
| --- | --- | --- |
| P50 (median) | Half are faster, half slower | 1 in 2 is slower |
| P90 | 90% are faster | 1 in 10 is slower |
| P95 | 95% are faster | 1 in 20 is slower |
| P99 | 99% are faster | 1 in 100 is slower |
Latency is right-skewed. The mean is misleading. Optimize P90 and P99, not just P50.

### Notes:
The percentile table is the heart of "how to read a latency dashboard." Most students have seen percentiles in stats class; few have used them in performance contexts.

The footer is the important takeaway: don't average. The mean is misleading because latency is right-skewed. P99 is what your worst customers feel.

War-story moment: tell about a time you (or anyone you know) chased a P50 improvement that was indistinguishable to users while P99 stayed bad. The team that prioritizes P99 over P50 ships a more reliable product.

If interactive, ask: "Why P99 and not P50? What is gained?" Answer: knowing what 1-in-100 users see. At scale, that's a lot of users.

<!-- Slide number: 18 -->

Inference time vs. end-to-end time
Inference time = on-GPU time only.
End-to-end time = what the user actually experiences.
End-to-end = inference time + network + queueing + client overhead.
Diagnostic heuristic:
If inference time is fast but end-to-end is slow → the bottleneck is in infrastructure or client, not the model.

### Notes:
Inference time vs end-to-end time — the distinction that lets you debug latency problems.

Inference time = on-GPU time only. Measured server-side. What kernel optimizations affect.

End-to-end time = what the user experiences. Includes network, queueing, client, TLS handshake.

The diagnostic heuristic is gold: if your inference time is fast but end-to-end is slow, stop optimizing kernels and look at infrastructure. We come back to this in Lecture 10.

A concrete example: a team measures 80 ms TTFT on the server but 400 ms TTFT from the user's browser. That 320 ms gap is network, TLS, load balancer queueing. None of which CUDA can fix.

<!-- Slide number: 19 -->

Recap — Lecture 2
Shared vs. dedicated: switch when scale, specialization, or orchestration require it.
Smaller models that pass your evals beat bigger models for inference.
TTFT + perceived TPS are the two core LLM metrics. Track them at P50/P90/P99.
Inference time ≠ end-to-end time. Diagnose the gap.
Next time: under the hood — neural nets and LLM internals.

### Notes:
Recap of Lecture 2. End-of-lecture exercise to assign as homework: Problem Set 2 in the problem-set packet. Especially the latency-conversion problems.

For next time: pre-lecture reader chapter 3 (Vectors, matrices, neural networks). This is the heaviest reader of the course. Students who haven't seen matmul in a while should set aside real time.

Bridge to next week: Now that you know what to measure, let's look at what we're actually measuring.

<!-- Slide number: 20 -->

LECTURE 03
Neural Networks and LLM Mechanics
Linear layers · attention · KV cache · MoE
Inference Engineering · Philip Kiely

### Notes:
LECTURE 3 START. This is where we open up the model and look inside. The next 3 lectures are technical-dense.

Today: neural network basics → LLM mechanics → attention. Two big concepts to land:
1. LLM inference splits into prefill and decode, with very different bottleneck profiles.
2. Attention is what makes transformers work and is the single most important operation to understand.

If students are coming in cold (haven't read the prerequisite chapter), spend an extra few minutes on slide 22 (linear layer).

<!-- Slide number: 21 -->

Learning objectives
Describe a neural network in terms of layers, weights, and hidden states.
Walk through tokenization → prefill → decode → logits.
Write the scaled dot-product attention formula and explain Q, K, V.
Explain why the KV cache exists.
Compare dense models to Mixture of Experts (MoE).

### Notes:
Quick read.

<!-- Slide number: 22 -->

Linear layer (the building block)

y = xW + b

x = input vector
W = weight matrix (set during training)
b = bias vector
Matrix multiplication (matmul) is the most-used operation in deep learning.
An LLM has dozens to hundreds of such layers stacked.
Activations (ReLU, SwiGLU) break linearity between them.

### Notes:
Linear layer = the fundamental building block. y = xW + b.

Walk through with a small example. Suppose x is a 3-dim vector [1, 2, 3] and W is a 3x2 matrix. The output y is a 2-dim vector — each output dimension is a dot product of x with one column of W.

Why we need activation functions: without them, two linear layers collapse into one (W3 = W1 * W2). ReLU(x) = max(0, x) introduces the nonlinearity that makes deep networks more expressive than shallow ones.

If time permits, draw the ReLU graph on the board. It's the simplest activation and the most useful intuitive picture.

<!-- Slide number: 23 -->

LLM inference: two phases
Prefill
Process the entire input sequence in parallel.
Build the KV cache.
Compute-bound. Drives TTFT.
Decode
Forward pass per token: read all weights, compute one logit vector.
Memory-bandwidth-bound. Drives TPS.
Output = softmax(logits) → sample (temperature, top-k, top-p).

### Notes:
The prefill/decode split is the single most important thing students need to know about LLM inference. Drill it in.

Prefill: takes the input sequence (say 1000 tokens), processes them all in parallel, builds the KV cache. Big matmuls, lots of math, GPU compute saturated → compute-bound. Determines TTFT.

Decode: one token at a time, one forward pass per token, must load all the weights each pass. Vector-matrix multiplications, lots of memory traffic but not much computation per byte → memory-bandwidth-bound. Determines TPS.

This duality drives:
- Why quantization helps decode (less memory traffic).
- Why batching helps both (amortizes weight loading across requests).
- Why disaggregation exists (different bottlenecks → different optimal hardware).

<!-- Slide number: 24 -->

Scaled dot-product attention

                     QK^T
Attention(Q, K, V) = softmax( ───── ) V
                     √(d_k)
Q (query) — representation of the token being generated.
K (keys) — representations of all prior tokens.
V (values) — what to pull from each prior token if it attends.
softmax normalizes the dot products into probabilities.
Multi-head attention runs many of these in parallel; each head specializes.

### Notes:
The attention formula. Write it on the board if you can, then walk through Q, K, V.

The intuition: each token (Q) looks at every other token (via Q·K^T) and decides how much to pay attention to each one. Softmax normalizes the dot products into probabilities. Then it weighs the V vectors by those probabilities.

Multi-head attention: do this 8 or 16 times in parallel with different learned weights. Each head can specialize in a different relationship (syntactic agreement, co-reference, etc.).

Self-attention = Q, K, V all from the same sequence. Cross-attention = Q from one, K/V from another (used in image gen for text conditioning).

<!-- Slide number: 25 -->

Why the KV cache is essential
Without it: each new token recomputes attention over all prior tokens → O(N²).
With it: K and V stored for each prior token → each new token does O(N) work.
Quadratic → linear. The reason modern LLMs are usable.
Cost: VRAM. Often 50%+ of remaining memory after weights.
Built during prefill. Used + updated during decode.

### Notes:
KV cache: easy to underestimate how central this is. Without it, every new generated token would have to recompute attention from scratch. With it, you just append the latest K and V and reuse the old ones.

This turns attention from O(N²) to O(N) per generated token. Without the KV cache, even basic chat would be unusable.

Cost: VRAM. For a 70B model with 4K context, the KV cache can be tens of GB. This is why long-context inference is hard, why we quantize KV cache, why we cache offload to CPU RAM. All in Lecture 8.

<!-- Slide number: 26 -->

Mixture of Experts (MoE)
Dense linear layers replaced by hundreds of "expert" matrices.
A small router picks a few experts per token per layer.
Example: Qwen3-235B-A22B
235B total parameters
22B active per token
8 of 128 experts per layer × 94 layers
Single-user inference: very efficient (sparse activation).
Batched production: different requests activate different experts → almost everything active.
Fix: Expert Parallelism (covered in Lecture 8).

### Notes:
MoE = adds sparsity. A 235B model has 235B params, but only 22B activate for any one token.

Walk through the example. Qwen3-235B-A22B: 128 experts per layer, router picks top 8. Across 94 layers, each token traverses a different path through the experts.

Critical caveat for production: in a batch of N different requests, each request activates different experts. By N=10 or so, almost every expert is active. So the memory savings from MoE only fully materialize with very low batch sizes — OR with Expert Parallelism that splits experts across GPUs (Lecture 8).

Why MoE is popular: lets you scale model capacity without paying full inference cost on every token. DeepSeek-V3 (671B) is MoE for this reason.

<!-- Slide number: 27 -->

Recap — Lecture 3
Linear layers + activations + attention + FFN = transformer block.
Prefill is compute-bound; decode is memory-bandwidth-bound.
Attention is Q·K^T → softmax → V. KV cache turns it from quadratic to linear.
MoE adds sparsity. Brilliant for single requests; tricky at batch.
Next time: image generation, bottlenecks, and optimizing attention.

### Notes:
Recap of Lecture 3.

Send-off: today was the model. Next week is the math of bottlenecks — when is a kernel compute-bound vs memory-bound, and how do we tell quantitatively?

Pre-lecture reader 4 (Complexity, memory, attention math) is required reading.

<!-- Slide number: 28 -->

LECTURE 04
Image Generation, Bottlenecks, and Attention
Iterative denoising · arithmetic intensity · FlashAttention
Inference Engineering · Philip Kiely

### Notes:
LECTURE 4 START. Today is the most quantitative lecture. We compute arithmetic intensity for standard attention and verify that decode is memory-bound on H100.

This is also the lecture where students realize all the words from Lecture 3 (compute-bound, memory-bound) have specific numerical meanings.

<!-- Slide number: 29 -->

Learning objectives
Explain iterative denoising and the three components of an image gen pipeline.
Define arithmetic intensity and the ops:byte ratio.
Use the roofline model to classify a kernel as compute- or memory-bound.
Compute arithmetic intensity for a small attention example.
Compare FlashAttention, PagedAttention, and sliding-window attention.

### Notes:
Quick read. The fourth objective (worked example) is what most students will struggle with — set the expectation that we'll do it on the board.

<!-- Slide number: 30 -->

Image generation pipeline
Three components:
Text encoder — turns prompt into latent instructions (CLIP, or full LLM in modern models).
Denoising model — iteratively refines noise in low-dimensional latent space.
VAE — decodes final latent back into pixel-space image.
30-50 denoising steps; each runs 2 forward passes (with prompt + without).
→ Total: ~100 forward passes per image.
Few-step models (≤8 steps) trade quality for 80-90% speedup.

### Notes:
Image generation pipeline. Three components: text encoder, denoiser, VAE. The key number to remember: 30-50 denoising steps × 2 forward passes per step (classifier-free guidance) = ~100 forward passes per image.

That ~100 number explains a lot. It's why image generation is so much slower than a single LLM forward pass even though the models are smaller. It's also why "few-step" models (8 steps or fewer) are so attractive — they trade quality for ~10× speedup.

Tease: we'll come back to image gen in Lecture 9 with the "one weird trick" of skipping guidance late in the schedule.

<!-- Slide number: 31 -->

Three core bottlenecks
3
Memorize these.
LLM prefill → compute-bound (big matmuls in parallel)
LLM decode → memory-bandwidth-bound (weights loaded per token)
Image / video generation → compute-bound (attention dominates)

### Notes:
The three bottlenecks. Cardinal rule of inference engineering: know which bottleneck you're hitting before optimizing.

Memorize:
- LLM prefill = compute-bound.
- LLM decode = memory-bound.
- Image / video gen = compute-bound.

A surprising consequence: the same model on the same GPU can be compute-bound during one phase and memory-bound the next. This is why disaggregation (Lecture 8) helps — each engine can be sized for its bottleneck.

<!-- Slide number: 32 -->

Arithmetic intensity & ops:byte ratio

intensity = work (ops) / memory_traffic (bytes)

ops:byte = GPU peak compute / memory bandwidth

H100 (FP16):  989 TFLOPS / 3.35 TB/s ≈ 295
Compare a kernel's arithmetic intensity to the GPU's ops:byte:
intensity > ops:byte  →  compute-bound
intensity < ops:byte  →  memory-bound
FP8 halves bytes per value → effectively doubles both bandwidth and FLOPS.

### Notes:
The math gets real. Two formulas:

1. Arithmetic intensity = ops per byte of memory traffic, for a SPECIFIC kernel.
2. Ops:byte ratio = GPU's peak compute / memory bandwidth, intrinsic to the HARDWARE.

If kernel's intensity > GPU's ops:byte → compute-bound (math is the limit). If less → memory-bound (memory is the limit).

For H100 at FP16: 989 TFLOPS / 3.35 TB/s ≈ 295 ops/byte. Memorize this number; it'll come up in problem sets.

Show on the board: 989 × 10^12 / 3.35 × 10^12 ≈ 295. Walk through the unit cancellation.

<!-- Slide number: 33 -->

Worked example: standard attention

N = 4096 (sequence)   d = 128 (head dim)   FP16 (2 bytes/value)

memory  = 8N^2 + 8Nd       bytes
compute = 4N^2·d + 3N^2    ops

→ intensity ≈ 62 ops/byte

H100 ops:byte = 295  →  MEMORY-bound
Standard decode attention is firmly memory-bound on H100.
Why decode TPS is bandwidth-limited and why attention optimization matters.
FlashAttention, PagedAttention, and variants all attack this number.

### Notes:
The worked example slide. The most important calculation in the course.

For N=4096, d=128, FP16: standard attention has 8N²+8Nd ≈ 540 MiB memory traffic and 4N²d+3N² ≈ 35 GFLOPS compute → intensity ≈ 62 ops/byte.

62 < 295. Therefore standard decode attention is firmly memory-bound on an H100.

Two implications:
1. FlashAttention's gains come mostly from reducing memory traffic (not compute).
2. Bigger memory bandwidth (H200, B200) helps decode more than more FLOPS does.

If you can, derive 8N² + 8Nd on the board. Show how each step in the attention algorithm (compute S, write S, read S, compute P...) contributes to the byte count.

<!-- Slide number: 34 -->

Two strategies for attention

Implementation improvements (lossless)
Same math, fewer HBM reads
FlashAttention — fused per-GPU kernels
FA-3 = Hopper, FA-4 = Blackwell
PagedAttention — fragmented KV cache pages

New algorithms (lossy)
Different math, breaks quadratic
Sliding-window attention: O(Nw) where w ≈ 8K-32K
Sparse / compressed attention variants
Need model training to support it
Use FlashAttention always. Use lossy variants only when trained for them.

### Notes:
Two strategies for attention optimization.

Implementation: FlashAttention, PagedAttention. Lossless — same math, fewer HBM round-trips. Use these always.

Algorithms: sliding-window attention (each token attends to only the last w tokens). Lossy — changes the math, requires training support. Use only when needed (very long context).

If asked "should I use FlashAttention 2 or 3 or 4?": FA-3 is Hopper-tuned, FA-4 is Blackwell-tuned. Pick the version matching your GPU. They're not backward-compatible because the kernels are hand-fused for specific hardware.

<!-- Slide number: 35 -->

Recap — Lecture 4
Image gen ≈ 50 steps × 2 passes = 100 forward passes per image.
Three bottlenecks: prefill = compute. decode = memory. image gen = compute.
Arithmetic intensity vs. ops:byte ratio classifies a kernel.
Standard attention at N=4096 is memory-bound on H100 (62 << 295).
FlashAttention and PagedAttention are lossless wins. Sliding-window is a lossy alternative.
Next time: the GPUs all this runs on.

### Notes:
Recap of Lecture 4. End of the math-heavy section.

Pre-lecture reader 5 (Computer architecture primer) covers CPU/GPU and memory hierarchy. Lighter reading than this week.

<!-- Slide number: 36 -->

LECTURE 05
GPU Hardware
SMs · HBM · Hopper · Blackwell · NVLink · InfiniBand
Inference Engineering · Philip Kiely

### Notes:
LECTURE 5 START. Today is hardware. We've used GPU specs (3.35 TB/s, 989 TFLOPS, etc.) without explaining what makes them what they are. Today we open the box.

Tone: this lecture is less abstract than the last two. The goal is fluency with hardware vocabulary — when you read a GPU spec sheet, you know what each number means and why it matters.

<!-- Slide number: 37 -->

Learning objectives
Describe GPU architecture: SMs, Tensor Cores, CUDA Cores.
Compare NVIDIA generations: Hopper, Lovelace, Blackwell, Rubin.
Differentiate NVLink, NVSwitch, InfiniBand.
Explain MIG and when to use it.
Identify when alternative accelerators (TPU, MI300, etc.) make sense.

### Notes:
Quick read. Item 5 is increasingly relevant — alternatives like AMD MI350 and Google TPU are real options today.

<!-- Slide number: 38 -->

GPU compute hierarchy
Streaming Multiprocessor (SM) — building block. H100 has 132.
Each SM contains:
Tensor Cores — Matrix Multiply-Accumulate (MMA). Dominant for inference.
CUDA Cores — scalar arithmetic.
Special Function Units — sin, cos, log (used by softmax).
FLOPS roughly double with each halving of precision.
(1 PFLOPS FP16 ≈ 2 PFLOPS FP8.)

### Notes:
GPU compute breakdown. Three kinds of cores:
- CUDA cores: scalar arithmetic (the general-purpose workhorse).
- Tensor cores: matrix multiply-accumulate (MMA). For inference, these are THE important ones.
- Special Function Units: sine, cosine, log, exp. Used in softmax.

Modern GPUs are dominated by Tensor cores in terms of FLOPS. An H100 has 528 Tensor cores. They are why GPUs are 10-100× faster than CPUs for matmul.

FLOPS roughly doubles with each halving of precision. So FP8 has 2× the FLOPS of FP16, FP4 has 2× the FLOPS of FP8. This is the foundation of the quantization wins we cover in Lecture 7.

<!-- Slide number: 39 -->

GPU memory hierarchy (fastest first)
L0 — instruction cache per Tensor Core
L1 — shared memory per SM (256 KB on H100)
L2 — global on-chip cache (50 MB on H100)
HBM — off-chip main memory (the GPU's VRAM)
VRAM size limits the model size you can serve.
Memory bandwidth (TB/s) is the bottleneck for LLM decode.

### Notes:
Memory hierarchy. Drill the order: HBM (off-chip, GB) → L2 (on-chip, MB) → L1 (per-SM, KB) → registers (per-core, bytes).

Each tier is smaller but faster. HBM bandwidth is ~3.35 TB/s on H100; L1 is roughly an order of magnitude faster.

VRAM size limits what model you can serve. H100 = 80 GB. A 70B FP8 model = 70 GB of weights + needs ~50% headroom for KV cache → you need an H200 (141 GB) or quantize to FP4.

Bandwidth is the bottleneck for LLM decode. This is why H200 (4.8 TB/s) beats H100 for decode despite same FLOPS.

<!-- Slide number: 40 -->

NVIDIA generations at a glance

| Architecture | Year | Key features | Best for |
| --- | --- | --- | --- |
| Ampere (A100) | 2020 | FP16 / FP32 | Legacy |
| Lovelace (L4, L40) | 2022 | FP8; no NVLink | Small models |
| Hopper (H100, H200) | 2022 | FP8; FlashAttention 3 | Production today |
| Blackwell (B100, B200, B300) | 2024 | FP4 + microscaling; FA-4 | New gold standard |
| Rubin | 2026 | HBM4; CPX prefill chip | Bandwidth-bound decode |

### Notes:
NVIDIA generations. Walk through:
- Ampere (A100): legacy. Don't deploy new workloads on these.
- Lovelace (L4, L40): graphics-oriented. Good for embedding-size models.
- Hopper (H100, H200): the production workhorse today. Mature kernel ecosystem.
- Blackwell (B100, B200, B300): the new gold standard. FP4 support, MXFP8, NVFP4.
- Rubin: 2026. HBM4. The new CPX chip is dedicated to compute-bound prefill workloads.

The Lovelace caveat: no NVLink. So you can't scale Lovelace cards for parallelism. L4 is good for solo small models; L40 is rarely the right choice.

<!-- Slide number: 41 -->

Datacenter GPU specs

| GPU | FP8 dense | VRAM | Bandwidth |
| --- | --- | --- | --- |
| H100 | 1,979 TFLOPS | 80 GB | 3.35 TB/s |
| H200 | 1,979 TFLOPS | 141 GB | 4.8 TB/s |
| B200 | ~5 PFLOPS | 192 GB | ~8 TB/s |
| B300 | ~5 PFLOPS | 288 GB | ~8 TB/s |
| L4 | 242 TFLOPS | 24 GB | 300 GB/s |
| L40 | 362 TFLOPS | 48 GB | 864 GB/s |

### Notes:
Datacenter GPU specs. Memorize H100 and B200 by heart:
- H100: 80 GB / 3.35 TB/s / ~1,979 TFLOPS FP8.
- B200: 192 GB / ~8 TB/s / ~5 PFLOPS FP8.

H200 is the H100 with more memory and bandwidth: 141 GB / 4.8 TB/s / same FLOPS. Useful for memory-bound workloads (decode).

B200 is roughly 2-3× the compute and bandwidth of H100. For most production workloads, this is the platform you should target if you're starting fresh.

<!-- Slide number: 42 -->

Interconnect speed hierarchy

| Tier | Interconnect | Bandwidth | Scope |
| --- | --- | --- | --- |
| Fastest | NVLink (Blackwell) | Up to 1,800 GB/s | GPU ↔ GPU within node |
| Fast | NVLink (Hopper) | 900 GB/s | GPU ↔ GPU within node |
| Medium | NVSwitch | All-to-all on NVLink | All GPUs in a node |
| Slow | InfiniBand | Up to 400 Gb/s per NIC | Node ↔ Node |
| Slowest | Ethernet | Up to 100 Gb/s per NIC | Generic networking |
InfiniBand is dramatically slower than NVLink. This shapes parallelism strategy choices.

### Notes:
Interconnect speed hierarchy. Critical for Lecture 8's parallelism discussion.

Within a node: NVLink (Blackwell: 1,800 GB/s, Hopper: 900 GB/s). Fast enough that Tensor Parallelism works.

NVSwitch: all-to-all comms on top of NVLink. Lets all 8 GPUs in a node coordinate.

Between nodes: InfiniBand at ~400 Gb/s. Drastically slower than NVLink. Tensor Parallelism breaks down here — you need Expert or Pipeline Parallelism.

Ethernet: even slower. Generic networking, not used for fast intra-cluster.

Frame this slide as: "Why parallelism strategy depends on hardware topology." The fact that InfiniBand is 30-50× slower than NVLink is why a lot of clever decisions in Lecture 8 exist.

<!-- Slide number: 43 -->

MIG, alternative accelerators, local inference
Multi-Instance GPU (MIG)
Split one GPU into up to 7 compute slices / 8 memory slices.
Useful for serving multiple small models (TTS, embeddings).
Alternative accelerators
AMD MI350, Google TPU, AWS Inferentia/Trainium, Groq LPU, Cerebras WSE-3, etc.
All face software, manufacturing, and distribution challenges.
Local inference (edge / device)
Zero network latency, privacy, free for developer.
But: weaker hardware, thermal limits, battery drain, fragmented software.

### Notes:
MIG and alternative accelerators.

MIG = Multi-Instance GPU. Splits one H100 / H200 / B200 into up to 7 compute slices and 8 memory slices. Useful for serving small models (a 3B TTS model would waste a full H100).

Alternative accelerators are real but face three challenges: software (no CUDA), manufacturing (extreme complexity), distribution (capacity). AMD MI350 is the most credible competitor today; Google TPU is great if you're on GCP; Groq is intriguing for batch=1 latency. Mention 1-2 examples per audience interest.

<!-- Slide number: 44 -->

Recap — Lecture 5
GPUs = SMs × (CUDA + Tensor + SFU cores). Tensor cores rule inference.
Memory hierarchy: HBM → L2 → L1 → registers. Bandwidth → decode bottleneck.
Hopper is today's workhorse; Blackwell is the new gold standard; Rubin lands soon.
NVLink intra-node is fast; InfiniBand inter-node is slow. Plan parallelism around it.
Next time: the software stack that makes the hardware sing.

### Notes:
Recap of Lecture 5. The big takeaway: hardware is part of the engineering surface area, not a black box.

Bridge to next week: now we've covered hardware and the model, let's stack the software in between. Pre-lecture reader 6 covers the software stack.

<!-- Slide number: 45 -->

LECTURE 06
The Software Stack
CUDA · PyTorch · vLLM · SGLang · TensorRT-LLM · Dynamo
Inference Engineering · Philip Kiely

### Notes:
LECTURE 6 START. The software stack — CUDA up to NVIDIA Dynamo.

Today's goal: when a student reads about a new inference tool, they can place it in the stack and reason about its purpose. The vocabulary is dense, but the layering principle makes it manageable.

<!-- Slide number: 46 -->

Learning objectives
Describe the CUDA stack: kernels, graphs, driver, runtime.
Explain kernel fusion and why it matters for decode.
Differentiate PyTorch from inference engines.
Choose between vLLM, SGLang, and TensorRT-LLM.
Use benchmarking and profiling correctly.

### Notes:
Read through.

<!-- Slide number: 47 -->

CUDA in one slide
CUDA kernel
A user-defined function that runs in parallel on the GPU.
CUDA graph
A DAG of kernels and ops for repeated workflows.
CUDA driver + runtime
Driver = hardware interface. Runtime = developer-facing API.
Libraries built on CUDA:
cuBLAS (linear algebra), cuDNN (NN primitives), CUTLASS (custom GEMM), FlashInfer (LLM kernels).

### Notes:
CUDA in one slide. Four pieces:
- Kernel: function running on GPU in parallel.
- Graph: DAG of kernels for repeated workflows.
- Driver: hardware interface.
- Runtime: developer-facing API.

Libraries on top of CUDA do most of the heavy lifting:
- cuBLAS = linear algebra.
- cuDNN = NN primitives.
- CUTLASS = building blocks for hand-written kernels.
- FlashInfer = LLM-specific kernels.

Most ML code never directly writes CUDA. PyTorch and inference engines wrap these libraries.

<!-- Slide number: 48 -->

Kernel fusion — why it matters
Two pointwise kernels back-to-back waste HBM round trips.
Without fusion:
Read [1,2,3] → write [2,4,6] → read [2,4,6] → write [6,12,18]
Two HBM round trips. Half the bandwidth wasted.
With fusion: one kernel does both ops in registers. One round trip.
Critical during decode (memory-bandwidth-bound).
torch.compile fuses automatically; FlashAttention is hand-fused for specific GPUs.

### Notes:
Kernel fusion. Critical concept.

Two kernels back-to-back means data writes to HBM and then reads from HBM in between. That round trip is wasted bandwidth.

Fusion: combine into one kernel that keeps intermediate values in registers. No HBM round trip.

In decode (memory-bound), every saved HBM trip directly improves TPS. This is why FlashAttention's fused implementation is so much faster than vanilla attention.

torch.compile does automatic fusion. Custom kernels (FlashAttention) hand-fuse for specific GPUs.

<!-- Slide number: 49 -->

The three inference engines

|  | vLLM | SGLang | TensorRT-LLM |
| --- | --- | --- | --- |
| Performance | Good | Good | Best |
| Ease of use | Easy | Easy | Hard |
| Hardware | NVIDIA, AMD, Intel, TPU | NVIDIA, AMD | NVIDIA only |
| Model support | Most (day-zero) | Most | Some |
| License | Apache 2.0 | Apache 2.0 | Apache 2.0 |

### Notes:
The three engines. Frame as a tradeoff between ease of use and performance.

vLLM: broadest hardware, broadest model support, easiest to stand up. Default choice.
SGLang: strong for MoE, Chinese models, image/video gen. Flexible frontend.
TensorRT-LLM: best perf on Hopper/Blackwell, hardest to use. Native NVFP4 support.

All three support continuous batching, KV caching, quantization, speculation, parallelism, disaggregation out of the box.

Common question: "When should I write my own engine?" Answer: almost never. These three engines cover 95% of production use cases.

<!-- Slide number: 50 -->

When to pick which engine
vLLM
Rapid stand-up, broadest model + hardware, multimodal Omni.
SGLang
Large MoE LLMs (DeepSeek, Kimi), Chinese-model day-zero, image/video gen.
TensorRT-LLM
Best perf on Hopper/Blackwell, NVFP4 native, time to invest in tuning.
NVIDIA Dynamo
Orchestration above engines: KV reuse, disaggregation, multi-node parallelism.
Skip Dynamo unless you have huge model + huge traffic.

### Notes:
When to pick which engine. Use the rules of thumb on the slide.

NVIDIA Dynamo sits ABOVE the engines — it orchestrates many replicas. Don't use it unless you have very large model + very large traffic. The complexity isn't worth it for smaller deployments.

<!-- Slide number: 51 -->

Benchmarking and profiling
Benchmarking tells you WHAT (e.g., P90 TTFT = 350 ms).
Profiling tells you WHY (kernel X dominates).
Benchmarking tips:
Shadow real production traffic when possible.
Always establish a baseline before optimizing.
Change ONE variable at a time.
Speculation and large batch sizes fight each other — test together too.
Tools: SGLang Genai-bench, NVIDIA GenAI-Perf, Locust, PyTorch Profiler.

### Notes:
Benchmarking and profiling. Two different operations.

Benchmarking: measures WHAT. Run varied traffic, observe latency and throughput.

Profiling: measures WHY. Drills into per-kernel time, memory usage.

Tips:
- Use real traffic (shadow production if possible).
- Establish a baseline before optimizing.
- Change ONE variable at a time.
- Some optimizations interact (speculation + large batch sizes fight).

Tooling: SGLang Genai-bench, NVIDIA GenAI-Perf, Locust, PyTorch Profiler.

<!-- Slide number: 52 -->

Recap — Lecture 6
CUDA = NVIDIA's programming layer. PyTorch wraps it. Engines orchestrate.
Kernel fusion eliminates HBM round-trips — critical for decode.
vLLM = anywhere fast. SGLang = MoE + image/video. TensorRT-LLM = best perf.
Dynamo lives above engines for very large deployments.
Benchmark with realistic traffic. Profile when needed. Change one variable at a time.
Next time: the performance techniques themselves — quantization and speculation.

### Notes:
Recap of Lecture 6. We've covered the entire stack from CUDA up. Now we move into the techniques themselves.

Pre-lecture reader 7 (Numerical precision and floating point) — required because quantization is a precision question.

<!-- Slide number: 53 -->

LECTURE 07
Quantization and Speculative Decoding
FP16 → FP8 → FP4 · microscaling · EAGLE · n-gram
Inference Engineering · Philip Kiely

### Notes:
LECTURE 7 START. We've reached the optimization techniques themselves. Today is quantization and speculative decoding.

These are the two most-discussed optimization techniques in the literature. Almost every production deployment uses both.

<!-- Slide number: 54 -->

Learning objectives
Compare FP16, BF16, FP8, FP4, INT8, INT4 — and the microscaling formats.
Explain why quantization helps both prefill and decode.
Describe four speculation methods: draft-target, Medusa, EAGLE, n-gram.
Validate quantization quality with multiple methods.
Know when to disable speculation.

### Notes:
Read through. The first objective (compare formats) is essential; we'll spend time on the table.

<!-- Slide number: 55 -->

Why quantization helps both bottlenecks
Lower precision wins both ways:
Prefill (compute-bound)
Lower-precision Tensor Cores deliver 2× FLOPS
Decode (memory-bound)
Half the bytes per value → effectively 2× memory bandwidth
Real-world: dropping one precision level → 30-50% better LLM perf.
(Overhead eats some of the theoretical 2×.)

### Notes:
Quantization helps both bottlenecks simultaneously, which is rare.

Prefill (compute-bound): FP8 Tensor Cores deliver 2× the FLOPS of FP16. Direct win.

Decode (memory-bound): half the bytes per value means half the memory traffic per token. Effectively doubles memory bandwidth.

In practice, you don't get the full 2× because of overhead (scale factors, dequant ops). 30-50% real speedup per precision level is typical.

<!-- Slide number: 56 -->

Number formats

| Format | Bits | First seen on | Use case |
| --- | --- | --- | --- |
| FP32 | 32 | Kepler (2012) | Training (rare for inference) |
| FP16 / BF16 | 16 | Pascal / Ampere | Default training + inference |
| FP8 (E4M3) | 8 | Hopper (2022) | Sweet spot for inference |
| MXFP8 | 8 | Blackwell (2024) | Microscaled FP8 |
| FP4 / MXFP4 / NVFP4 | 4 | Blackwell (2024) | Aggressive perf, careful work |
| INT8 / INT4 | 8 / 4 | Pascal / Turing | Avoid for LLMs — no exponent |

### Notes:
Number formats table. Walk through:

FP16 / BF16: 16 bits. Default for training. BF16 has more exponent (wider range), less mantissa.

FP8: 8 bits. Hopper introduced. The sweet spot for inference — minimal quality loss, 2× speed.

MXFP8: 8 bits with microscaling (block of 32 shares a scale factor). Better outlier preservation.

FP4 / NVFP4: 4 bits. Blackwell. Aggressive — quality risk. NVFP4 uses block size 16 plus global 32-bit factor.

INT8 / INT4: 8 or 4 bits, no exponent. Bad for LLMs because no dynamic range for outliers.

<!-- Slide number: 57 -->

Why float beats int for inference
Floating-point values: sign + EXPONENT + mantissa.
Integers: just sign + value bits — no exponent.
Exponent gives dynamic range — express very large + very small values.
Attention has outliers. Outliers matter.
INT8/INT4 clip outliers → quality loss. FP8/FP4 preserve them.
Microscaling formats (MXFP8/4, NVFP4) add per-block scale factors.
NVFP4: 16-element blocks + a global 32-bit scale → highest 4-bit granularity.

### Notes:
Why float beats int for inference. The exponent gives dynamic range.

Neural network values are not uniformly distributed. Most weights cluster near zero with rare outliers (the famous "outlier features" in LLMs). Floating-point's logarithmic spacing captures both regimes; integers waste representation on the empty middle and clip outliers.

This is why FP8 outperforms INT8 for LLM inference even though they're the same bit count.

<!-- Slide number: 58 -->

What to quantize (and what NOT to)
Component sensitivity, least → most sensitive:
1. Weights (linear layers) — least sensitive.
2. Activations — somewhat sensitive.
3. KV cache — moderately sensitive; helpful for prefix caching + disaggregation.
4. Attention components — most sensitive. Errors compound over thousands of tokens.
Softmax is almost always left in original precision, even in aggressive schemes.
Starter recipe: FP8 on linear layers + activations + KV cache. Skip attention.

### Notes:
Sensitivity hierarchy. Memorize:
1. Weights (least sensitive) — quantize freely.
2. Activations — somewhat sensitive.
3. KV cache — moderately sensitive but unlocks lots of memory.
4. Attention components (most sensitive) — avoid.

Why attention is so risky: every token's attention output depends on every prior token's. Errors compound across thousands of tokens.

Softmax is almost always left in original precision even in the most aggressive schemes.

Recommended starter: FP8 on linear layers + activations + KV cache. Skip attention.

<!-- Slide number: 59 -->

Speculative decoding
Decode is memory-bound — compute sits idle.
Speculation uses that spare compute:
1. Speculator generates draft tokens (cheap).
2. Target model validates them in one forward pass.
3. Accept the verified prefix + generate one extra token.
Result: N+1 tokens per forward pass.
Analogy: solving a sudoku is hard; checking one is easy.
Improves TPS, not TTFT. Disable at high batch sizes (no spare compute).

### Notes:
Speculative decoding. The core idea: decode is memory-bound, so compute is idle. Use that idle compute to generate cheap draft tokens that the real model then validates.

The validate step is much cheaper than generating from scratch — like checking a sudoku solution is easier than solving one.

Improves TPS, not TTFT.

Disable at high batch sizes — when compute is saturated, speculation just steals from real generation.

<!-- Slide number: 60 -->

Four speculation methods

| Method | How it works | Best fit |
| --- | --- | --- |
| Draft-target | Small separate draft model (≥10× smaller, same family) | Quick OOTB; no training |
| Medusa | Fine-tune extra decoder heads onto target (2-4 drafts) | Simple, limited adoption |
| EAGLE | Purpose-built draft trained on target's hidden states (up to 8 drafts) | Production go-to |
| N-gram / Lookahead | Build dictionary at prefill; match suffixes during decode | Code completion |

### Notes:
Four speculation methods.

Draft-target: separate small draft model (≥10× smaller, same family). Easy to deploy, but most overhead.

Medusa: fine-tune extra decoder heads onto the target. Simpler than draft-target but limited.

EAGLE: purpose-built draft model trained on the target's hidden states. Up to 8 draft tokens. Production go-to.

N-gram / Lookahead: build dictionary at prefill, match suffixes during decode. Excellent for code completion where output looks like input.

Recommended starter: EAGLE if you have training infrastructure, n-gram for code use cases, draft-target for quick experiments.

<!-- Slide number: 61 -->

Validating quantization quality
Standard: zero perceptible quality loss.
Run all three quality checks:
1. Perplexity — quantized vs. original on representative sequences. Look for minimal increase.
2. Intelligence benchmarks — MMLU, SWE-bench, HumanEval.
3. Custom evals — your product-specific test suite.
LLMs are non-deterministic — differences should be indistinguishable from noise.
Tooling: NVIDIA TensorRT Model Optimizer (ModelOpt) is the leading PTQ library.

### Notes:
Quality validation for quantization. Standard is zero perceptible quality loss.

Run all three checks:
1. Perplexity comparison on representative sequences.
2. Intelligence benchmarks (MMLU, SWE-bench, HumanEval).
3. Custom evals (your product-specific tests).

LLMs are non-deterministic — your "noise floor" matters. Differences smaller than that are statistically meaningless.

NVIDIA TensorRT Model Optimizer (ModelOpt) is the leading open-source PTQ library. Outputs work with all three engines.

<!-- Slide number: 62 -->

Recap — Lecture 7
Quantization gives both 2× FLOPS and 2× effective bandwidth — both bottlenecks win.
Floats > ints because of exponent → dynamic range → outlier preservation.
Microscaling formats add per-block scale factors. NVFP4 is the new fine-grained 4-bit.
Quantize weights freely. Quantize KV cache carefully. Avoid attention.
Speculation: N+1 tokens per pass. EAGLE = production; n-gram = code completion.
Next time: caching, parallelism, and disaggregation.

### Notes:
Recap of Lecture 7. Quantization and speculation cover roughly 80% of practical performance wins.

Next time: caching, parallelism, disaggregation. Pre-lecture reader 8 (Parallel computing primer) is required.

<!-- Slide number: 63 -->

LECTURE 08
Caching, Parallelism, and Disaggregation
Prefix caching · TP · EP · PP · prefill/decode splits
Inference Engineering · Philip Kiely

### Notes:
LECTURE 8 START. Today is the remaining big optimization levers — KV cache reuse, multi-GPU parallelism, and prefill/decode disaggregation.

These come into play at scale. A 7B model doesn't need parallelism; a 700B model can't avoid it.

<!-- Slide number: 64 -->

Learning objectives
Identify when prefix caching helps and where to store the KV cache.
Choose between Tensor, Expert, and Pipeline Parallelism.
Estimate VRAM requirements for large models.
Decide when to use disaggregation.
Read xPyD notation.

### Notes:
Read through.

<!-- Slide number: 65 -->

Prefix caching
Two requests with the same prefix can skip prefill for the shared part.
Example:
"Weather in SF ?" and "Weather in NYC ?" share "Weather in".
The shared KV cache is reused — better TTFT.
Hard rule:
Prefix caching works ONLY until the first non-repeated token.
Place novel tokens as late as possible in your context.
High-value domains: system prompts, code completion, RAG, multi-turn chat.

### Notes:
Prefix caching. Two requests sharing a prefix can skip the prefill for the shared portion.

Hard rule: caching breaks at the first non-repeated token. If novel content appears at position 2, anything after position 2 in those requests can't be cached — even if it happens to match.

Context engineering rule: put novel tokens (user's question, dynamic data) AS LATE AS POSSIBLE. System prompt and shared scaffolding first.

High-value domains: complex system prompts, RAG, code completion (same codebase context), multi-turn chat (history grows by appending).

<!-- Slide number: 66 -->

Where to store the KV cache

| Tier | Storage | Speed | Size | When to use |
| --- | --- | --- | --- | --- |
| G1 | GPU VRAM | TB/s | 10s-100s GB | Hot active prefixes |
| G2 | CPU RAM | 100s GB/s | 100s GB - TB | GB200 NVLink-C2C offload |
| G3 | Local SSD | 5-10 GB/s | TB | Medium-warm caches |
| G4 | Networked SSD | GB/s | 10s TB | Global cross-replica cache |

### Notes:
KV cache storage tiers. Walk through:

G1 (GPU VRAM): TB/s bandwidth. Default. Hot active prefixes.
G2 (CPU RAM): 100s GB/s. Useful with GB200's NVLink Chip-to-Chip.
G3 (Local SSD): GB/s. For medium-warm caches.
G4 (Networked SSD): GB/s. Global KV cache across replicas.

NVIDIA Dynamo's KV Block Manager (KVBM) handles tier movement.

<!-- Slide number: 67 -->

VRAM sizing rule of thumb

vram_required = (bits/8) × params × kv_overhead

kv_overhead ≈ 1.8 (production headroom)

Example: DeepSeek-V3, 671B params, FP8
vram = (8/8) × 671 × 1.8 ≈ 1,208 GB
→ requires 8 × B200 = 1,440 GB (full node)
Single B200 = 180 GB. A node = 8 × B200 = 1,440 GB.
Frontier LLMs require multi-GPU. Sometimes multi-node.
If model + KV doesn't truly need a second node, scale replicas horizontally instead.

### Notes:
VRAM sizing rule of thumb. Critical for capacity planning.

Formula: VRAM = (bits/8) × params × kv_overhead. kv_overhead ≈ 1.8 for production.

Walk through DeepSeek-V3 example: 671B params at FP8 → 1,208 GB. Needs 8 × B200 (1,440 GB). A full node minimum.

Most frontier LLMs are multi-GPU. Sometimes multi-node. Plan capacity from the model up.

<!-- Slide number: 68 -->

Three parallelism strategies

| Strategy | What splits | Strength | Weakness |
| --- | --- | --- | --- |
| Tensor Parallelism (TP) | Each layer's weights | Lowest latency | All-reduce heavy — no multi-node |
| Expert Parallelism (EP) | MoE experts | Highest throughput | Only for MoE |
| Pipeline Parallelism (PP) | Successive layers | Multi-node fallback | Pipeline bubbles |
TP within a node; EP across MoE; PP for multi-node dense. Combine as needed (e.g., TP8 + EP across nodes).

### Notes:
Three parallelism strategies. Walk through:

Tensor Parallelism (TP): split each layer's weights. Lowest latency. But heavy all-reduce — limited to within a node by NVLink.

Expert Parallelism (EP): split MoE experts. Highest throughput. Low communication. Multi-node friendly.

Pipeline Parallelism (PP): split successive layers. Multi-node fallback for dense models. Has bubbles (some GPUs idle while others work).

Real production: combine. TP8 within a node + EP across nodes. Or TP8PP2 for dense multi-node.

<!-- Slide number: 69 -->

Disaggregation
Separate prefill and decode onto independent engines.
Three reasons it helps:
Prefill (compute) and decode (memory) interfere under high load.
Each engine sized for its bottleneck (lower TP for prefill, higher TP for decode).
Independent scaling based on traffic shape.
xPyD notation: 5P3D = 5 prefill engines + 3 decode engines for one model.
Conditional disaggregation: requests try decode first, forwarded to prefill only if needed.

### Notes:
Disaggregation. Separate prefill and decode onto independent engines.

Why: prefill (compute-bound) and decode (memory-bound) interfere when run together at high load.

Each engine can be sized for its bottleneck. Prefill wants more compute, lower TP. Decode wants more memory, higher TP.

xPyD notation: x prefill engines + y decode engines. e.g., 5P3D = 5 prefill + 3 decode.

Conditional disaggregation: requests try decode first; only forwarded to prefill if input is large and uncached.

<!-- Slide number: 70 -->

When to disaggregate
Only when ALL THREE are true:
1. Heavy traffic (~100M to 1B tokens/day for the model size)
2. Large model (≥100B params)
3. Prefill-heavy workload (long input sequences)
Otherwise, use the GPUs for horizontal replica scaling — simpler and often better.
Textbook fit: a frontier LLM in a code editor — many long contexts, mostly prefill.

### Notes:
When to disaggregate. All THREE must be true:
1. Heavy traffic (100M to 1B tokens/day for the model size).
2. Large model (≥100B params).
3. Prefill-heavy workload (long input sequences).

If any of these fail, use the GPUs for horizontal replica scaling instead. Disaggregation has real complexity cost — don't reach for it casually.

Textbook fit: a frontier LLM in a code editor — many developers passing large/varied chunks of code as context. Mostly prefill, lots of tokens, trillion-param model.

<!-- Slide number: 71 -->

Recap — Lecture 8
Prefix caching: huge TTFT win, but only up to the first novel token. Place novel last.
VRAM ≈ (bits/8) × params × 1.8. Frontier LLMs = full node minimum.
TP = latency. EP = throughput on MoE. PP = multi-node fallback.
Disaggregation: only at large scale on large prefill-heavy models.
Next time: modalities beyond text.

### Notes:
Recap of Lecture 8. This concludes the optimization-techniques arc.

Next time: modalities beyond text. Pre-lecture reader 9 (Modalities and signal processing).

<!-- Slide number: 72 -->

LECTURE 09
Modalities Beyond Text
VLMs · embeddings · ASR · TTS · image · video
Inference Engineering · Philip Kiely

### Notes:
LECTURE 9 START. We've covered LLMs in depth. Today we generalize to other modalities — vision, embeddings, audio, image generation, video.

The high-level takeaway: most LLM optimizations transfer, but each modality has quirks. Some break the model entirely (embeddings have no decode phase).

<!-- Slide number: 73 -->

Learning objectives
Describe how each modality differs from LLM inference.
Identify which LLM optimizations transfer and which don't.
Define modality-specific metrics (time to first sentence, RTF).
Explain why image and video are compute-bound, not memory-bound.
Describe Context Parallelism and ring attention.

### Notes:
Read through.

<!-- Slide number: 74 -->

Modality cheat sheet

| Modality | Archetype | Bottleneck | Key optimization |
| --- | --- | --- | --- |
| LLM | Autoregressive | Decode = memory | Speculation, KV cache |
| VLM | Autoregressive + vision enc | Long context | Prefix caching, downsampling |
| Embedding | Encoder-only | Throughput | Big batches, scale horizontally |
| ASR (Whisper) | Encoder-decoder | Decode (LLM-like) | TensorRT-LLM, WebSockets, VAD |
| TTS | LLM-style + audio decoder | Audio decoder | FP8, in-flight batching, MIG |
| Image gen | Iterative denoising | Compute | Kernel fusion, guidance trick |
| Video gen | Iterative denoising (XYT) | Compute (attention) | Context Parallelism |

### Notes:
Modality cheat sheet. The defining table of the lecture. Walk through one row at a time.

LLM: autoregressive, decode is memory-bound. Optimization toolkit: speculation, KV cache, quantization.

VLM: LLM + vision encoder. Long context is the challenge. Same toolkit + downsampling.

Embedding: encoder-only. Big batches, scale horizontally. Prefix caching is irrelevant (no decode).

ASR/TTS: encoder-decoder, decoder is LLM-like. TensorRT-LLM is the optimization tool.

Image / video gen: iterative denoising. Compute-bound. Different toolkit entirely.

<!-- Slide number: 75 -->

VLMs — long context is the challenge
A 1024×1024 image ≈ 1,000 visual tokens.
A 4-second video at 24 fps × 1,000 tokens ≈ ~100,000 tokens. Downsampling is mandatory.
Transfers from LLM:
KV cache quantization, EAGLE speculation, prefix caching, TP, disaggregation.
New tradeoff: input resolution and frame rate.
Modern reality: production pipelines mix VLMs with specialized models (OCR, VAD) for cost and quality.

### Notes:
VLMs. The defining number: 1,000 visual tokens per 1024×1024 image.

4 seconds of 24 fps video = 96,000 tokens. Long context becomes critical fast.

Transfers from LLM: KV cache quantization, EAGLE speculation, prefix caching, Tensor Parallelism, disaggregation.

New tradeoff: input resolution + frame rate. Lower-res, lower-fps = fewer tokens = faster + cheaper, but quality risk. Production pipelines often mix VLMs with specialized models (dedicated OCR, dedicated VAD).

<!-- Slide number: 76 -->

Embeddings — different rules
Tokens process in parallel → no prefill/decode split.
Consequences:
Prefix caching and disaggregation are irrelevant.
Models are small (<8B) → multi-GPU parallelism is wasted.
Scale horizontally; one replica per GPU.
Batching is HUGE — dozens to hundreds of inputs per request.
Robust queueing is essential for surges.
Quality check for FP8 quantization: cosine similarity between original and quantized outputs ≥99%.

### Notes:
Embeddings. The "wait, this is different" modality.

Tokens process in parallel. No prefill / decode split. Therefore:
- Prefix caching irrelevant.
- Disaggregation irrelevant.
- Multi-GPU parallelism wasted (models are small).
- Scale horizontally instead.

Embedding inference is throughput-dominated. Big batches (dozens to hundreds per request), one replica per GPU, robust queuing for surges.

FP8 quantization works well. Validate with cosine similarity ≥99% to original.

<!-- Slide number: 77 -->

Whisper RTF
1,000×
Real-Time Factor — transcribe an hour in seconds
Optimized Whisper pipelines hit ~1,000× Real-Time Factor.
An hour of audio transcribed in under 4 seconds.
Pipeline: VAD chunking → distribute across MIG slices → stitch by timestamp.

### Notes:
Whisper RTF. The audio metric.

RTF = real-time factor. RTF 1× = transcribes audio as fast as it plays. RTF 1000× = an hour of audio in 4 seconds.

For real-time dictation: RTF ≥ 1× per chunk. For batch transcription: higher RTF = lower cost.

Pipeline: VAD chunks → distribute across MIG slices → stitch by timestamp.

The 1,000× figure is real — optimized Whisper deployments hit it.

<!-- Slide number: 78 -->

ASR and TTS in real time
Both work in real time via WebSocket streaming + VAD.
ASR (live dictation):
Target ~200 ms per chunk. Runtime is nearly maxed; gains come from infrastructure.
TTS:
TTFB and "time to first sentence" — the latter is more user-meaningful.
Token rate capped at real-time playback (~80-100 TPS).
Excess capacity → more concurrent users per GPU.
Voice products today: cascading VAD → ASR → LLM → TTS pipelines.

### Notes:
ASR and TTS in real time. Both leverage:
- WebSocket streaming for bidirectional audio.
- VAD (Voice Activity Detection) for chunking.
- TensorRT-LLM under the hood (Whisper decoder is LLM-like).

ASR live dictation: target ~200 ms per chunk. Most runtime gains exhausted; gains now come from infrastructure (WebSockets, VAD, queue management).

TTS: TPS capped at real-time audio playback (~80-100 TPS). Anything faster is wasted. Excess capacity → more concurrent users.

Voice products today are cascading: VAD → ASR → LLM → TTS. Unified speech-to-speech models are coming but not yet commercially viable.

<!-- Slide number: 79 -->

Image gen — "one weird trick"
Each denoising step runs 2 passes (with prompt + without).
50 steps × 2 passes = 100 forward passes.
The trick: skip guidance for the last ~20 steps.
→ 80 passes instead of 100.
Quality holds because the model isn't repainting a cat as a dog at step 30.
Kernel choices matter: FlashAttention 3/4, fused RMSNorm, 8-bit GEMM.

### Notes:
Image gen — "one weird trick." Skip classifier-free guidance for the last ~20 of 50 steps.

Drops total forward passes from 100 to 80. Quality usually fine because the model isn't going to fundamentally redraw the image at step 30+.

Other kernel choices: FlashAttention 3/4 for attention, fused RMSNorm, 8-bit GEMM where viable.

Compile with torch.compile or use SGLang Diffusion / TensorRT for production. Engines must be compiled per-GPU.

<!-- Slide number: 80 -->

Video gen — context parallelism
Attention is 70-80% of compute time.
Run on full 8-GPU nodes. Batch size 1.
Context Parallelism (CP), not Tensor Parallelism:
Weights are replicated across all 8 GPUs (small enough).
Attention computation is split via ring attention.
Each GPU holds a piece of context and passes intermediates around the ring.
Caching: reuse attention outputs across timesteps or layers (30-40% speedup, test for quality).

### Notes:
Video generation. The most demanding modality.

Attention is 70-80% of compute time. Run on Blackwell (or Rubin), full 8-GPU nodes, batch size 1.

Context Parallelism (CP), not Tensor Parallelism:
- Weights are SMALL enough to replicate across all 8 GPUs.
- Attention computation is split via ring attention.
- Each GPU holds a piece of context and passes intermediates around the ring.

Attention caching: reuse outputs across timesteps or layers. 30-40% speedup but quality varies — test carefully.

<!-- Slide number: 81 -->

Recap — Lecture 9
LLM optimizations transfer broadly to VLM, ASR, TTS.
Embeddings break the rules: big batches, no caching, no parallelism.
Image and video gen are compute-bound. Different bottleneck → different toolkit.
Video uses Context Parallelism (replicate weights, split attention).
Next time: production — containers, autoscaling, multi-cloud.

### Notes:
Recap of Lecture 9. Diversity of modalities, common core of techniques.

Next time: production. Pre-lecture reader 10 (Distributed systems for production).

<!-- Slide number: 82 -->

LECTURE 10
Production
Containers · autoscaling · cold starts · multi-cloud · canary deploys
Inference Engineering · Philip Kiely

### Notes:
LECTURE 10 START. The final lecture. We move from "make one box fast" to "run a production service that real users depend on."

This lecture borrows heavily from distributed systems engineering. Half the slides describe concepts that aren't specific to ML; the other half describe how ML inference twists those concepts.

<!-- Slide number: 83 -->

Learning objectives
Build a production container for an inference workload.
Configure autoscaling with concurrency and batch sizing in mind.
Diagnose and mitigate cold starts.
Explain multi-cloud capacity and GPU procurement modes.
Compare blue-green and canary deployment strategies.

### Notes:
Read through.

<!-- Slide number: 84 -->

Containerization
Standard packages: container, image, Dockerfile, registry.
Production inference container bundles:
CUDA toolkit + cuDNN + driver versions (must match GPU)
Python packages — torch, transformers, diffusers
Inference engine — vLLM / SGLang / TensorRT-LLM
System packages — ffmpeg, etc.
PIN exact versions.
Day-zero model launches → expect to rebuild against stable releases over the following weeks.

### Notes:
Containerization. Standard packages: container, image, Dockerfile, registry.

For inference, the container bundles:
- CUDA toolkit + cuDNN + driver versions.
- Python packages (torch, transformers, diffusers).
- Inference engine (vLLM, SGLang, TRT-LLM).
- System packages (ffmpeg, etc.).

PIN exact versions. Day-zero model launches mean using pre-release builds — plan to rebuild against stable releases over the following weeks.

<!-- Slide number: 85 -->

Autoscaling signals
Two signals — use BOTH.
Utilization (GPU mem + compute) → lagging indicator.
Traffic (incoming RPS) → proactive indicator.
They diverge:
A few requests with 100K uncached tokens spike utilization without traffic volume.
Concurrency target MUST match the inference engine's batch size.
Mismatch = wasted GPU (too low) or queued requests (too high).

### Notes:
Autoscaling signals. Use BOTH utilization and traffic.

Utilization (GPU mem + compute) → lagging indicator. Already saturated by the time you see it.

Traffic (incoming RPS) → proactive indicator. Scale before saturation.

They can diverge. A few requests with 100K uncached tokens spike utilization without high traffic count.

Concurrency target MUST match the inference engine's batch size. Mismatch = wasted GPU (too low) or queueing (too high).

<!-- Slide number: 86 -->

Cold starts — four contributors
1. GPU procurement
Cloud provider problem; negotiable in contracts.
2. Image loading
Slim images load faster. Keep them lean.
3. Model loading
Don't bake huge weights into the image. Load from storage near the GPU.
4. Engine startup
TensorRT-LLM compilation takes minutes. Cache compiled engines.

### Notes:
Cold starts. Four contributors:
1. GPU procurement (cloud-provider problem).
2. Image loading (slim images load faster).
3. Model loading (don't bake huge weights into the image; load from storage near GPU).
4. Engine startup (cache compiled engines for TensorRT-LLM and torch.compile).

A 90-second cold start on a scale-to-zero deployment + traffic burst = disaster. We'll see why on the next-but-one slide.

<!-- Slide number: 87 -->

Llama 3 training reliability data
1 / 50,000
Failure rate observed in production at frontier scale
419 unexpected interruptions in 54 days on 16,000 GPUs (Llama 3 training).
Roughly 1 failure per 50,000 GPU-hours.
A single 8-GPU node running for a year ≈ 70,000+ GPU-hours.
Build for failure. It's the default.

### Notes:
Llama 3 reliability data. The headline number: 419 unexpected interruptions on 16,000 GPUs over 54 days = roughly 1 failure per 50,000 GPU-hours.

A single 8-GPU node running for a year ≈ 70,000+ GPU-hours. So a single-node deployment expects multiple failures per year.

Build for failure. Active-active multi-region, health checks, retries with backoff, circuit breakers. These aren't bonus features; they're table stakes.

<!-- Slide number: 88 -->

Multi-cloud postures

Active-active
Multiple regions serve live traffic at once
Failures transparent to users
Higher cost, more complexity
Right for global consumer chat apps

Active-passive
Hot standby idle until failover
Failover takes seconds-to-minutes
Lower cost
Right for internal / compliance-critical work
GPU procurement: reserved (long-term discount) + on-demand + spot (preemptible). Most production mixes all three.

### Notes:
Two multi-cloud postures.

Active-active: multiple regions serve live traffic. Failures transparent. Higher complexity, higher cost. Best for global consumer products.

Active-passive: hot standby idle until failover. Failover takes seconds-to-minutes. Cheaper. Best for compliance-critical batch.

Procurement: mix reserved (long-term discount) + on-demand (flexibility) + spot (cheap, preemptible). Production runs all three simultaneously.

<!-- Slide number: 89 -->

Deployment strategies

Blue-green
Two identical environments, cut over fully
Doubles GPU spend during cutover
Doesn't scale for inference
Classic for stateless web apps

Canary (preferred for inference)
Route small % to new deployment first
Autoscaling shrinks old as traffic moves
Incremental cost is manageable
Easy rollback if metrics regress

### Notes:
Deployment strategies.

Blue-green: doubles GPU spend during cutover. Bad for inference.

Canary (preferred): route small % to new deployment first, monitor metrics, gradually shift more. Autoscaling shrinks the old as traffic moves. Incremental cost stays manageable.

<!-- Slide number: 90 -->

Cost: dedicated vs. per-token

Per-token (1B input + 500M output):
  1B × $1.25/M + 500M × $10/M = $6,250

Dedicated (1,600 GPU-hours × $3.50/hr):
  = $5,600

Savings: $650/month (~10%) — BEFORE engineering cost
Use ≥1 week time horizons to smooth variance.
Add engineering time + on-call TCO to the dedicated side.
Translate per-token to a total dollar amount and compare like-for-like.

### Notes:
Cost: dedicated vs. per-token. The math works out closer than students expect.

Example: 1B input + 500M output tokens.
Per-token: 1B × $1.25/M + 500M × $10/M = $6,250.
Dedicated: 1,600 GPU-hours × $3.50/hr = $5,600.

Savings: $650/month (~10%) — BEFORE engineering cost.

The engineering cost is the kicker. A senior inference engineer at $300K/year + benefits costs ~$25K/month. Don't switch to dedicated to save $650/month unless the strategic reasons are strong.

For >$100K/month workloads, dedicated savings become meaningful even after engineering costs.

<!-- Slide number: 91 -->

Don't forget the client
TLS handshake takes ~30 ms — that's 10%+ of a 300 ms P95 budget.
Reuse sessions. The OpenAI SDK does this silently — your custom client must too.
Async inference for throughput-not-latency workloads (bulk processing, embedding backfills).
Streaming protocols:
LLMs over HTTP streaming is enough.
Voice / video: WebSockets (unstructured) or gRPC (schema-enforced).

### Notes:
Don't forget the client. TLS handshake takes ~30 ms — that's 10%+ of a 300 ms P95 budget.

Reuse sessions. The OpenAI SDK does this silently.

Async inference for throughput-not-latency workloads.

Streaming protocols:
- LLMs over HTTP streaming = sufficient.
- Voice/video real-time = WebSockets (unstructured) or gRPC (schema-enforced).

<!-- Slide number: 92 -->

Recap — Lecture 10
Containers bundle the stack. Pin versions; rebuild on stable releases.
Autoscale on traffic AND utilization. Concurrency must match batch size.
Cold starts: slim image, weights nearby, cache compiled engines.
Build for failure (1 per 50K GPU-hours). Multi-cloud active-active for global consumer.
Canary deployment beats blue-green for GPU workloads.
Client overhead is real — reuse sessions, stream when it matters.

### Notes:
Recap of Lecture 10. The full course is now behind you.

For the final exam: design questions are the highest-weight section. Practice them with study partners.

<!-- Slide number: 93 -->

THANK YOU
You're now ready to dig into the book and the open-model ecosystem.
Next steps:  explore Hugging Face · benchmark a model · stand up vLLM on a rented GPU · contribute to an open inference engine.

### Notes:
Closing slide. Use this to send students off with concrete next steps.

The "next steps" mentioned in the bullet are real:
- Hugging Face has 2 million+ models. Browse, download, run.
- vLLM is open source. Read it.
- Rent a GPU on Lambda, RunPod, Coreweave, etc. Most have introductory free credits.
- The book (Inference Engineering by Philip Kiely) is the canonical reference.

---

# Instructor Appendix — Per-Lecture Delivery Kit

The slide-by-slide notes above tell you *what* to say. This appendix tells you *how to run the room* — engagement prompts to drop in, numerical anchors to keep at hand, and time-budget targets so you don't blow past the 50-minute clock. Use it as a pre-lecture cheat sheet; print it or keep it on a second screen during delivery.

## How to use the engagement prompts

Each lecture has 4–6 "ask the room" prompts. Drop them in roughly every 4–5 slides. They are deliberately concrete: a number to estimate, a trade-off to defend, or a war story to predict. The goal is not to test recall — it's to force students to *commit to a mental model* before you reveal the answer. A wrong commitment is far more memorable than a passive listen.

Three rules:

1. **Give think-time.** 10 seconds of silence feels like a year but is what separates the prompt from rhetorical filler.
2. **Take 2–3 answers before resolving.** Different wrong answers reveal different mental models.
3. **Tie the answer back to a specific slide or concept ID** so students can find it in their notes later.

---

## Lecture 1 — What is Inference?

**Numerical anchors to keep at hand:**

- Training a 7B model: ~100K H100-hours × $2/hr = **$200K one-time**.
- Serving 100K daily users at 5K tokens/day each = **500M tokens/day** → ~2 H100s 24/7 → **~$1M/yr recurring**.
- Inference passes training in cost at **~3 months post-launch** for a typical 7B-class product.
- >90% of production AI GPU-hours go to inference, not training.

**Ask the room (drop one every ~10 minutes):**

- *(after Slide 5, Training vs. inference)* "Estimate: for a chat startup with 10,000 daily active users, what fraction of their AWS bill is inference vs. training in year 1?" Expected guesses: 50/50. Reality: ~90/10.
- *(after Slide 6, Three layers)* "Pick one of the three layers — runtime, infrastructure, tooling — and name a real product whose failures you've personally seen at that layer."
- *(after Slide 7, Six runtime techniques)* "Without looking back, name as many of the six as you can." Pair-share for 60 seconds. The students who blank are flagged for office hours.
- *(closing)* "Which of the six techniques have you encountered the name of before this class?" Show of hands. Calibrates instructor on prior exposure.

**Time budget (50 min):** Slides 1–2 = 5 min orientation. Slides 3–7 = 25 min concept introduction. Slides 8–10 = 15 min framing for the course. 5 min Q&A buffer.

---

## Lecture 2 — Prerequisites, Latency Metrics

**Numerical anchors:**

- TTFT target for chat UX: **<500 ms** (anything above feels laggy).
- TPS perceptual threshold: **>15 tokens/sec** (human reading speed ≈ 5 tps; 3× faster feels "instant").
- P50 vs. P99 latency: typically **5–10× ratio** on a healthy system; 20×+ means coordination problems.
- Shared API → dedicated crossover for popular models: **~100M tokens/day**.

**Ask the room:**

- "ChatGPT shows you the first word in roughly 300 ms. Break that 300 ms down: how much is network, how much is queuing, how much is prefill compute?"
- "A vendor says their model does '120 TPS average.' What's missing from that claim?" (Percentile, batch size, prompt length, hardware.)
- "Your boss says 'our API is too slow, optimize latency.' What's the next question you ask?" (Which percentile? Whose latency — end-to-end or server-side?)
- "Estimate: at $0.50 per million input tokens and $1.50 per million output tokens (typical 2026 frontier API pricing), what does it cost to summarize 1,000 customer support tickets averaging 2K tokens each?" (~$2 input + ~$0.30 output ≈ $2.30.)

**Time budget:** 10 min on shared-vs-dedicated. 25 min on latency metrics (the heart of the lecture). 15 min on evaluation frameworks and Q&A.

---

## Lecture 3 — Neural Networks and LLM Mechanics

**Numerical anchors:**

- Llama-3.1 8B: 32 layers, 32 heads (8 KV heads after GQA), head dim 128, FP16.
- KV cache per token (Llama-3.1 8B FP16): **128 KiB**. At 8K context: **1 GiB per request.**
- A single H100 (80 GB), after ~16 GB for weights, fits **~60 concurrent 8K-context requests**.
- Softmax is the precision floor: even in INT8/FP8 deployments, attention softmax stays in FP32 or BF16.

**Ask the room:**

- *(early)* "Without thinking too hard: an 8B model running in FP16 — how much GPU memory just for the weights?" (8B × 2 bytes = 16 GB.)
- *(mid)* "If you double the context length, what happens to KV-cache size?" (Doubles linearly.) "What happens to attention compute?" (Quadruples — O(N²).)
- *(after the transformer block diagram)* "Where in this diagram does inference *not* go that training does?" (Backward pass / loss / optimizer state.)
- "What part of the transformer would you guess is the slowest? Why?" Collect guesses, then show: depends on phase. Prefill = matmuls. Decode = attention + memory traffic.

**Time budget:** 20 min on the transformer block. 20 min on KV cache and why it dominates memory. 10 min on attention math + Q&A.

---

## Lecture 4 — Image Generation, Bottlenecks, Attention

**Numerical anchors:**

- H100 SXM FP16 ops:byte ratio (ridge point): **~295**. FP8: ~590.
- Prefill arithmetic intensity (typical LLM, batch 1, prompt 1K): **several hundred** ops/byte → **compute-bound**.
- Decode arithmetic intensity (single token): **~1** ops/byte → **memory-bound** by ~300×.
- SDXL 1024×1024, 30 steps: **~1.8 s/image** on H100 baseline; ~700 ms with TP=4 + guidance skipping.

**Ask the room:**

- "Same model, same GPU. Prefill is compute-bound. Decode is memory-bound. How can this be true?" (Force them to derive: many tokens vs. one token; weights read once either way.)
- "If you doubled the HBM bandwidth on an H100 but kept the FLOPS the same, what speedup would you expect on decode? On prefill?" (2× decode, ~no change to prefill.)
- "Image generation has no decode phase. Why?" (Diffusion uses fixed N steps, each a full UNet forward pass; no autoregressive sampling.)
- *(closing)* "Predict: in 5 years, will LLM decode still be memory-bound on the latest GPUs?" Argue both sides.

**Time budget:** 15 min on the bottleneck framing — this is THE lecture for the ridge-point picture. 20 min on attention math. 15 min on image-gen-specific patterns.

---

## Lecture 5 — GPU Hardware

**Numerical anchors:**

- H100 SXM: **80 GB HBM3, 3.35 TB/s, 989 TFLOPS FP16, 1979 TFLOPS FP8**.
- B200: **192 GB HBM3e, 8 TB/s** — ~2.4× H100 decode bandwidth.
- NVLink 4: **900 GB/s** GPU-to-GPU. InfiniBand HDR: **50 GB/s** across nodes. Ratio: **18×**.
- L4: ~24 GB, ~300 GB/s — wins $/token for small models, loses absolute latency to H100.

**Ask the room:**

- "Why do production deployments cap tensor parallelism at TP=8?" (One DGX/HGX node holds 8 GPUs; TP across nodes crosses InfiniBand and pays the 18× penalty per layer.)
- "Your CFO asks: 'can we get the same throughput from 10 L4s as one H100 for cheaper?'. What do you say?" (Depends on model size — L4 can't hold 70B+ FP16 in one card; bandwidth ratio matters too.)
- "Estimate: how many tokens/sec can a single H100 do on Llama-3.1 8B FP8 decode?" Bracket guesses, then reveal (typically 4K–8K TPS for the engine, depending on batch).
- "What changes about your inference architecture when you go from H100s to B200s?" (Bigger batches, longer contexts fit, fewer cards needed, but $/card is higher.)

**Time budget:** 15 min on memory hierarchy. 15 min on the generations table. 15 min on interconnects (critical for Lecture 8). 5 min Q&A.

---

## Lecture 6 — The Software Stack

**Numerical anchors:**

- Naive PyTorch transformer: ~30 kernels/layer × 30 layers × **5 µs/launch = 4.5 ms launch overhead per token** before any compute.
- Decode latency target: **10 ms/token** → naive launch overhead alone eats half the budget.
- Fused kernels collapse 30 launches → 3–5 launches per layer.
- CUDA graphs: capture-once, replay-many; removes per-step launch overhead almost entirely.

**Ask the room:**

- "Why isn't PyTorch enough for production inference?" (No continuous batching, no paged KV, no fused kernels by default.)
- "A new engine claims 2× speedup over vLLM. What three questions do you ask before believing it?" (On what model? Which GPU? Which batch size and context length?)
- "If you had to write one CUDA kernel for an inference engine, which one would buy you the most?" (Fused attention — it's where the time lives at long contexts.)
- "Pick one: vLLM, SGLang, TensorRT-LLM. When does it win?" Force them to commit before you reveal the cheatsheet.

**Time budget:** 10 min on the four-layer stack picture. 15 min on what an inference engine actually does. 15 min on engine comparison. 10 min Q&A.

---

## Lecture 7 — Quantization and Speculative Decoding

**Numerical anchors:**

- FP8 vs. FP16 on H100: **2× peak compute + 2× memory savings ≈ 4× decode throughput**, typical quality cost **0.1–0.3 MMLU points**.
- Speculative decoding speedup: with 5-token draft + 3/5 acceptance on Llama-70B target + 1B draft: **(5+25 ms)/3 = ~11.7 ms per accepted token vs. 25 ms baseline = 2.1× speedup**.
- Sensitivity ordering for quantization (most to least tolerant): **weights → activations → KV cache → attention softmax**.
- INT4 weight-only is safe for most models; INT4 KV cache loses quality on long contexts.

**Ask the room:**

- "FP8 is 2× the FLOPS of FP16 on H100 — but production teams often see 3× or 4× speedup, not 2×. Why?" (Memory savings stack on top of FLOPS for memory-bound decode.)
- "What's the worst layer to quantize aggressively? Why?" (Attention softmax — numerical sensitivity.)
- "Why does speculative decoding speed up *decode* but not *prefill*?" (Prefill processes all tokens in parallel already — no autoregressive bottleneck to break.)
- "Estimate: if your draft model has 50% acceptance instead of 60%, by how much does the speedup drop?" Force them to redo the arithmetic live.

**Time budget:** 20 min on quantization (heart of the lecture). 15 min on speculative decoding. 10 min on combined effect + Q&A.

---

## Lecture 8 — Caching, Parallelism, Disaggregation

**Numerical anchors:**

- Paged attention page size: typically **16 tokens**. Eliminates ~60% of fragmentation vs. contiguous allocation.
- Prefix cache hit rate for chat (shared system prompt): often **>80%** of input tokens.
- TP all-reduce cost per layer: bandwidth-bound at **~1–2 ms** within a node on H100s.
- Disaggregation breakeven: ≥100M tokens/day AND ≥100B-param model AND prefill-heavy traffic. All three.

**Ask the room:**

- "Why does a chatbot with a long system prompt benefit massively from prefix caching but a code-completion tool benefits less?" (Shared prefix structure; code-completion prompts are mostly unique per request.)
- "What's the cost of tensor parallelism that pipeline parallelism avoids?" (All-reduce per layer.) "What's the cost of PP that TP avoids?" (Pipeline bubbles.)
- "Disaggregation sounds free — separate prefill and decode workers, scale independently. Why isn't every system disaggregated?" (KV-cache transfer cost between workers; complexity tax; only wins past a scale threshold.)
- "MoE models are 'sparse.' Does that make them cheaper or more expensive to serve?" (Cheaper per active param, more expensive per total param; need EP for routing.)

**Time budget:** 15 min on caching (prefix + KV). 15 min on parallelism varieties. 15 min on MoE/disaggregation. 5 min Q&A.

---

## Lecture 9 — Modalities

**Numerical anchors:**

- Whisper-large-v3 on H100: 1 min audio → ~3 sec → **RTF = 0.05** (20× faster than real-time).
- SDXL 1024×1024 30 steps: **~1.8 s** baseline; **~700 ms** with TP=4 + guidance skipping.
- Embedding models (BGE, E5): typically **<10 ms/query** on T4 — cheap, embarrassingly parallel.
- Video generation (Sora-class): single 5-sec clip = **multi-minute single-GPU latency**; uses Context Parallelism.

**Ask the room:**

- "Image generation is compute-bound. What does that imply about which optimizations help?" (Better kernels, FP8, larger batches — not memory-class tricks like paged attention.)
- "ASR has a streaming requirement chat doesn't. How does that change engine design?" (Chunk-based processing, low chunk-latency models, partial-result emission.)
- "Embeddings cost almost nothing per query. Why is embedding-at-scale still hard?" (It's not the embed step — it's the vector DB / ANN index / sharding.)
- "What's the next modality you'd bet will mainstream by 2027?" Open discussion — likely candidates: long-form video, real-time multimodal agents.

**Time budget:** 15 min on image gen. 10 min on ASR. 10 min on embeddings. 10 min on video. 5 min Q&A.

---

## Lecture 10 — Production

**Numerical anchors:**

- HPA autoscale target: **in-flight requests per pod ≈ 75% of engine max batch** (not CPU%).
- Cold start budget: **<90 s** ideal for chat; pre-warm with `minReplicas=2`.
- Multi-cloud arbitrage: 100 GPUs 24/7/365 — AWS on-demand ≈ **$10.7M/yr**, Lambda+reserved mix ≈ **$1.75M/yr** → **~$9M/yr savings**.
- Failure budget: **~1 GPU failure per 50K GPU-hours** — plan for it, never assume away.

**Ask the room:**

- "Why is `target_cpu_utilization=80` the wrong autoscale signal for a GPU inference pod?" (CPU isn't the bottleneck; GPU is.)
- "Your cold start is 3 minutes. Name three places to attack." (Container image size, weight loading, engine compilation/CUDA graph capture.)
- "Estimate the dollar gap between running 100 H100s on AWS on-demand vs. on a reserved hyperscaler-alternative." (~$8–10M/year.)
- *(closing)* "If you take one lesson from this whole course into your first inference job, what is it?" Collect answers as a verbal recap.

**Time budget:** 15 min on autoscaling. 10 min on cold starts. 15 min on multi-cloud + reliability. 10 min on synthesis + Q&A.

---

## Mid-lecture energy checks (use any lecture)

If the room is fading around minute 30:

- **Stand-up / sit-down vote**: "Stand up if you've ever rented a GPU for a personal project." Visualization wakes the room.
- **One-minute pair-share**: "Turn to your neighbor and explain [last concept] in your own words." Better than another slide.
- **Live numerical estimate**: Pick the next numerical anchor from this appendix and have students estimate before you reveal. Engagement spike, every time.

## Calibrating to your class

- **First-year CS students**: spend more time on Lectures 1, 3, 5 (foundations). Cut Lecture 8 in half — disaggregation is too advanced.
- **Senior CS / ML students**: speedrun Lectures 1, 3, 5. Spend full sessions on 4 (bottlenecks), 7 (quantization+spec), 8 (parallelism).
- **Industry workshop / professional audience**: skip Lectures 3 and 5 entirely; assume prior knowledge. Start at Lecture 4 (bottlenecks) and go deep on 7, 8, 10.

## Concept-graph cross-references

Every lecture maps to concepts in `docs/kb/concepts.json`:

| Lecture | Primary concept IDs |
|---|---|
| 1 | `inference-vs-training`, `ai-stack-overview` |
| 2 | `latency-throughput`, `inference-cost`, `token`, `context-window`, `temperature` |
| 3 | `transformer-architecture`, `self-attention`, `kv-cache` |
| 4 | `flash-attention`, `paged-attention` |
| 5 | `gpu-memory-hierarchy`, `gpu-generations` |
| 6 | `cuda-stack`, `inference-engines`, `continuous-batching` |
| 7 | `quantization`, `speculative-decoding` |
| 8 | `tensor-parallelism`, `moe`, `mla`, `disaggregated-serving` |
| 9 | (modality concepts; see Glossary B.6, B.18) |
| 10 | `inference-cost` |

Hand this table to students at week 1 as a course-tracker; revisit it at week 10 as a self-assessment checklist.

Open the floor for questions. End with: "Inference engineering is one of the highest-leverage technical skills in software today. You're now equipped to participate. Go build something."