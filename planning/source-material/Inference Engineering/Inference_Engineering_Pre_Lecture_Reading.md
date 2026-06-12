**Inference Engineering**

Pre-Lecture Reading

*Background concepts to read before each lecture*

*If you walk in cold, the lecture will feel like reading a foreign language.*

> **Source & permitted use.** This document is an instructor-authored companion derived from *Inference Engineering* by Philip Kiely (Baseten Books, 2026). It paraphrases and adapts material from that book for internal use within the Andhra University / Oxmiq curriculum only. **Do not redistribute, mirror, or publish outside this course.** Students and instructors should obtain the original book for canonical text, code samples, and references. If a formal license or permission grant for this material is established, replace this notice with a pointer to the source agreement.

Spend 30-60 minutes on the relevant chapter before each session.

How to use this reader

This document collects the **background concepts** you should be comfortable with **before** walking into each of the ten lectures. It is not a summary of the lectures — that's what the Study Guide is for. This is the bridge between general CS / ML coursework and the specific vocabulary, math, and systems intuition the course assumes.

Each chapter is structured the same way. **Why you need this** explains how the material connects to the lecture. **Concepts to know** are the must-haves; if any term is unfamiliar, slow down and read its section carefully. **A worked example** walks through one or two of the most important calculations end-to-end. **Self-check** is three to five questions you should be able to answer in your head before class. **Suggested external resources** point to canonical references if you want more depth.

If you've recently finished a strong undergraduate ML course or you have professional experience, you can skim. If you're coming from a different track (web dev, mobile, data analytics), please read carefully — the concepts in here are not optional.

| **Reader chapter** | **Pairs with** | **Estimated reading time** |
|----|----|----|
| 1\. AI in production | Lecture 1 | 30 min |
| 2\. Latency, probability, percentiles | Lecture 2 | 45 min |
| 3\. Vectors, matrices, neural networks | Lecture 3 | 75 min |
| 4\. Complexity, memory, attention math | Lecture 4 | 75 min |
| 5\. Computer architecture primer | Lecture 5 | 45 min |
| 6\. Software stack for ML | Lecture 6 | 45 min |
| 7\. Numerical precision and floating point | Lecture 7 | 45 min |
| 8\. Parallel computing primer | Lecture 8 | 45 min |
| 9\. Modalities and signal processing | Lecture 9 | 45 min |
| 10\. Distributed systems for production | Lecture 10 | 45 min |

## Learning goals at a glance

Use this table as a pre-flight check. If you can confidently say "yes" to every goal for the reader you're about to study, you can skim; if any goal feels vague, slow down on that reader's *Concepts to know* section.

| # | Reader | After this reader you should be able to… |
|---|---|---|
| 1 | AI in production | (a) State the difference between training and inference in one sentence; (b) trace a chat request from browser to inference server and back; (c) explain why production-scale changes the engineering problem; (d) distinguish open vs. closed models with one example of each. |
| 2 | Latency, probability, percentiles | (a) Convert between TTFT, ITL, and perceived TPS; (b) read a latency distribution and pick the right percentile to optimize; (c) explain why mean latency is misleading; (d) name three causes of P99 tail. |
| 3 | Vectors, matrices, neural networks | (a) Do a 2×2 matmul by hand; (b) draw the forward pass of a 1-layer MLP; (c) define what "weights" are, in bytes, for a 7B FP16 model; (d) state what a softmax does in one sentence. |
| 4 | Complexity, memory, attention math | (a) Write the attention formula from memory; (b) explain why attention is O(N²); (c) calculate KV-cache size for a small model at a given context length; (d) state the arithmetic intensity of a matmul and compare it to a GPU's ops:byte ratio. |
| 5 | Computer architecture primer | (a) Name the four tiers of the GPU memory hierarchy and their relative speeds; (b) explain what a Tensor Core does that a CUDA core doesn't; (c) tell the difference between intra-node (NVLink) and inter-node (InfiniBand) interconnects; (d) explain why this matters for parallelism choices. |
| 6 | Software stack for ML | (a) Name the four layers from CUDA to inference engine; (b) state what PyTorch's autograd does and why inference doesn't need it; (c) explain what an inference engine adds on top of a deep-learning framework; (d) compare vLLM, SGLang, and TensorRT-LLM at one-line resolution. |
| 7 | Numerical precision and floating point | (a) Define mantissa and exponent; (b) explain why FP8 has 4 exponent bits and what that buys you; (c) state the sensitivity ordering for quantization (weights → activations → KV cache → attention); (d) explain why integer formats fail for attention softmax. |
| 8 | Parallel computing primer | (a) Define data, tensor, pipeline, and expert parallelism; (b) explain why TP stays inside a node; (c) describe all-reduce in one sentence; (d) name the bottleneck that pipeline parallelism creates. |
| 9 | Modalities and signal processing | (a) Explain why image generation is compute-bound while LLM decode is memory-bound; (b) state what a VAE does in image inference; (c) define a mel-spectrogram and why ASR uses it; (d) explain Real-Time Factor (RTF) for ASR. |
| 10 | Distributed systems for production | (a) Name the three pillars of observability; (b) distinguish active-active from active-passive failover; (c) explain why autoscale signals beyond CPU% matter on GPU servers; (d) state one reason scale-to-zero is the wrong default for chat. |

## Before you arrive — universal checklist (every lecture)

Independent of the specific reader, you should always arrive having:

- **Skimmed the matching study-guide chapter.** Even if you don't fully understand it yet, you'll know what questions to bring.
- **Read the matching Pre-Lecture Reader.** Slow on unfamiliar terms; skim familiar ones.
- **Looked up any concept word you couldn't define.** The glossary is your friend — don't walk in with vague mental models of vocabulary you'll be asked about.
- **Eaten and hydrated.** This sounds silly. It isn't. These lectures are dense and a tired brain learns nothing.

|  |  |  |
|----|----|----|

Reader 1 — AI in production

**Pairs with Lecture 1 — What is Inference?**

Why you need this

Lecture 1 introduces the three-layer model of inference engineering — runtime, infrastructure, and tooling — and the six runtime techniques that recur throughout the course. To get value from those abstractions, you need to know roughly what a generative AI model is, what "production" means in a software-engineering context, and why running a model at scale is materially different from running it once on your laptop.

Concepts to know

Generative AI in 90 seconds

**Generative AI** refers to a class of machine-learning models that, given some input, produce new content — text, images, audio, video, or code — that didn't exist before. These are distinct from **predictive ML** models (like a credit-card fraud classifier) that emit a class label or score from a fixed set.

The current generation of generative AI is dominated by **transformers**, a neural-network architecture introduced in 2017 (Vaswani et al., "Attention Is All You Need"). Transformers underlie almost every modern model: ChatGPT and Claude (text), Midjourney and Stable Diffusion (images), Whisper (speech-to-text), and so on. Different modalities specialize the architecture, but the foundations are the same.

A model has **weights**, which are billions to trillions of numerical parameters set during a long, expensive process called **training**. Training a frontier model can cost tens or hundreds of millions of dollars in compute. Once weights are trained, they are frozen — and the act of using those frozen weights to answer a user's request is called **inference**.

Inference vs. training in one paragraph

Imagine you are studying for an exam. **Training** is the time you spent learning the material over a semester — slow, expensive, done once. **Inference** is taking the exam — you've already learned the material; now you're applying it. In an AI company, training happens occasionally and expensively. Inference happens billions of times a day, every day, on every user request. Almost all the GPU-hours a deployed AI company pays for go to inference. This is why a discipline has grown up around making inference fast, cheap, and reliable.

Open vs. closed models

Models split into two camps based on whether their weights are public:

- **Closed models** — weights are proprietary. You access them only through the provider's API. Examples: OpenAI's GPT-5, Anthropic's Claude, Google's Gemini. You can't run them on your own hardware.

- **Open models** — weights are released publicly, usually on Hugging Face. You can download them and run them on your own GPUs. Examples: Meta's Llama, DeepSeek, Alibaba's Qwen, Mistral. Most are released under permissive licenses like MIT or Apache 2.0, but always check.

As of late 2024 / early 2025, the quality gap between open and closed models has narrowed to weeks. Open models like DeepSeek V3 / R1 and Kimi K2 sometimes match or exceed closed models on specific benchmarks. This shift is central to the rise of inference engineering as a discipline: every company can now run its own intelligence rather than rent it.

What "production" means

**Production** in software engineering means "the system that real users actually depend on," as opposed to development, testing, or staging environments. Production has properties that toy systems don't:

- **Uptime** — production systems have **Service Level Agreements (SLAs)** promising specific availability (e.g., 99.9% uptime = ~9 hours of downtime per year). Falling short of an SLA can cost contracts.

- **Scale** — production systems handle many users at once. "Many" can mean 10 concurrent users or 10 million depending on the product.

- **Latency expectations** — humans have measurable patience limits. Most interactive products target sub-second response times.

- **Monitoring and observability** — you need to know when production breaks, ideally before users do.

- **Cost discipline** — at scale, every wasted millisecond costs real money.

APIs, requests, and responses

Modern software systems communicate over **APIs** (Application Programming Interfaces). An **API** is a contract that defines what you can ask a system to do and what it will return. The most common pattern is **HTTP REST**: a client sends a structured request to a URL, and the server returns a structured response.

A user-facing AI product like ChatGPT typically works like this:

1.  The user types a question in the browser.

2.  The browser sends an HTTP request to the chat backend.

3.  The backend assembles a prompt (system prompt + chat history + user message) and forwards it to the **inference server** that runs the model.

4.  The inference server generates tokens one at a time and streams them back to the backend, which streams them to the browser, which renders them on screen.

5.  When the model emits a stop token, the response is complete.

All of the inference engineering you'll learn in this course happens in step 3-4 — the inference server side.

A worked example: how a chat response moves through the stack

Suppose you ask ChatGPT "What is the capital of France?" Here is what's happening behind the scenes, in roughly chronological order:

6.  **0 ms** — your browser sends a request to chat.openai.com. TLS handshake takes ~30 ms (we'll cover this in Lecture 10).

7.  **30 ms** — the request reaches an OpenAI load balancer, which routes it to a specific data center based on your location.

8.  **40 ms** — the chat backend assembles the input: a system prompt (telling the model how to behave), your previous messages, and your new question. This becomes the **input sequence**.

9.  **45 ms** — the backend forwards the input sequence to an **inference server**. The inference server is a process running on a GPU node loaded with model weights.

10. **45-200 ms** — the inference server runs **prefill** on the input sequence. This is the compute-intensive phase that processes your entire question at once.

11. **200 ms** — the first output token ("Paris") is generated and starts streaming back.

12. **200-300 ms** — subsequent tokens ("is", "the", "capital", etc.) are generated one at a time during **decode**, each taking roughly 5-15 ms.

13. **300 ms** — the model emits a stop token. Response is complete.

The user saw a response start to appear after 200 ms (the **time to first token**) and saw it complete after 300 ms (the **end-to-end latency**). Lecture 2 will teach you to measure and optimize both.

Self-check

14. Can you explain to a non-technical friend what "inference" is, in two sentences?

15. Roughly what is the difference between a closed model and an open model? Can you name one of each?

16. Why do AI companies spend more on inference than on training, despite training being incredibly expensive?

17. In the example above, what happens during the 45-200 ms window? What about 200-300 ms?

Suggested external resources

- 3Blue1Brown's series "Neural Networks" on YouTube — 4 short videos that build intuition for what a network is doing.

- Andrej Karpathy, "Intro to Large Language Models" (1-hour YouTube talk) — the best non-technical overview of how LLMs actually work.

- Hugging Face's "Models" page (huggingface.co/models) — browse 2+ million open models. Pick one and read its model card.

Reader 2 — Latency, probability, percentiles

**Pairs with Lecture 2 — Prerequisites Before You Optimize**

Why you need this

Lecture 2 introduces the metrics that every inference engineer uses every day: TTFT, TPS, ITL, latency percentiles, throughput. These all come from basic probability and statistics. If you've taken a statistics class, you'll recognize most of this. If you haven't, or if it's been a while, this reader is essential — the lecture moves fast and uses percentile language without re-deriving it.

Concepts to know

Distributions, mean, median, mode

A **distribution** describes how values are spread out. If you measured the response time of every API call to a service over a day and made a histogram, you'd see a distribution. The shape of that distribution tells you a lot.

Three measures of central tendency:

- **Mean** (average) — sum of values divided by count. Sensitive to outliers.

- **Median** — middle value when sorted. Half of values fall below, half above. Robust to outliers.

- **Mode** — most common value. Useful when the data has clusters.

For a **symmetric distribution** like a bell curve, mean ≈ median ≈ mode. For a **skewed distribution**, they diverge. **Latency distributions are almost always right-skewed**: most requests are fast, but a long tail of slow requests pulls the mean upward.

> **Worked example:** A service handles requests in \[100, 100, 100, 100, 100, 100, 100, 100, 100, 10000\] ms (one outlier). Mean = 1,090 ms. Median = 100 ms. The mean is dominated by a single bad request. If a stakeholder asks "how fast is the service?", "100 ms" (median) is honest; "1,090 ms" (mean) is misleading.

Percentiles

A **percentile** is a value below which a given proportion of the data falls. The 90th percentile (P90) is the value such that 90% of observations are at or below it.

Percentile language is the standard for reporting latency because it directly maps to user experience. P50 (median) tells you what a typical user sees. P95 tells you what your **second-worst-in-twenty** user sees. P99 tells you what your **worst-in-one-hundred** user sees.

| **Percentile** | **Frequency "how often is it worse?"** | **When to track** |
|----|----|----|
| P50 | 1 in 2 requests is slower | Sanity-check normal experience |
| P90 | 1 in 10 is slower | Routine quality measurement |
| P95 | 1 in 20 is slower | User-facing SLA target |
| P99 | 1 in 100 is slower | Worst-case detection |
| P999 | 1 in 1000 is slower | Rare disasters, scale-out signals |

> **Why this matters:** If P50 = 200 ms and P99 = 4,000 ms, an average user is happy but 1% of users see a four-second wait. At a million daily users, that's ten thousand frustrated people per day. Optimizing only the mean leaves them in the dark.

Streaming and incremental output

Many AI applications stream output token by token rather than waiting for the full response. The user sees text appear progressively, like watching someone type. This changes how you think about latency. There's no single "response time" — there's:

- **Time to first token (TTFT)** — how long until the first piece of output appears? Lower = the app feels snappy.

- **Inter-token latency (ITL)** — the gap between consecutive tokens. Lower = output flows smoothly.

- **Total response time** — first byte to last byte. For long outputs this can be many seconds even with low TTFT and ITL.

> perceived_TPS_per_user = 1000 / ITL_in_ms Example: ITL = 25 ms → TPS = 40 tokens per second per user

Throughput vs. latency

These two concepts are perpetually confused. They are different ends of a tradeoff.

- **Latency** is **how long a single request takes**. Measured in milliseconds. Lower is better. Latency matters when a user is waiting.

- **Throughput** is **how many requests a system completes per unit time**. Measured in requests per second, tokens per second, etc. Higher is better. Throughput matters when you're billing for total work.

Many optimizations improve one at the expense of the other. **Batching** is the canonical example: bundling many requests together lets you process them in parallel (high throughput) but each user must wait for the batch to fill (high latency). An online chat product cares about latency. A nightly document-embedding job cares about throughput. Choosing correctly is half the battle.

Long-tail thinking

Latency distributions in distributed systems have heavy tails. There's a famous saying among performance engineers: "The tail is the experience." A single slow link, a garbage-collection pause, a cold cache miss, a noisy neighbor on shared hardware — all can cause one request in a hundred to be ten times slower than average.

Inference engineering treats P95/P99 latency as first-class targets. Halving the mean is impressive on a slide but invisible to users; halving the P99 is what they actually feel.

A worked example: converting between metrics

Your team's monitoring dashboard reports:

- TTFT (P95) = 280 ms

- ITL (P95) = 12 ms

- Average output length = 150 tokens

**Q1: What is perceived TPS at P95?** perceived_TPS = 1000 / 12 = ~83 tokens/sec/user.

**Q2: What is the expected end-to-end latency for a typical response at P95?** TTFT + N × ITL = 280 + 150 × 12 = 280 + 1,800 = **2,080 ms ≈ 2.1 seconds**.

**Q3: Where is most of the time spent?** Decode (1,800 ms) dominates TTFT (280 ms) for outputs of this length. To make the app feel faster, **TPS gains matter more than TTFT gains** for this workload. If outputs were much shorter (say 10 tokens), TTFT would dominate, and optimizing prefill would matter more.

This single calculation tells you what to optimize. We'll use it constantly in Lectures 7 and 8.

Self-check

18. Latency = 200 ms ITL is reported. What's the perceived TPS?

19. A service reports mean latency 350 ms and P50 = 200 ms. What does the gap tell you about the distribution? About the user experience?

20. In one sentence, why does a B2B SaaS product typically care more about P99 latency than a consumer app does?

21. Define throughput. Give an example of a workload where throughput matters more than latency.

Suggested external resources

- Gil Tene, "How Not to Measure Latency" — classic 40-min talk on percentiles and coordinated omission. Free on YouTube.

- Brendan Gregg's "Systems Performance" — chapter 2 on methodology is gold for diagnosing latency problems.

Reader 3 — Vectors, matrices, neural networks

**Pairs with Lecture 3 — Neural Networks and LLM Mechanics**

Why you need this

Lecture 3 walks through linear layers, attention, KV caches, and MoE in technical detail. Every one of those concepts is built on **matrix multiplication**. If you can't read y = xW + b and immediately picture what's happening, please slow down on this reader.

Concepts to know

Vectors

A **vector** is an ordered list of numbers, written as a column or a row:

> v = \[3, 1, 4, 1, 5, 9, 2, 6\]

The number of entries is the vector's **dimension**. In machine learning, vectors often have hundreds to thousands of dimensions, each one representing some aspect of an input.

Key operations:

- **Addition** — component-wise. \[1,2\] + \[3,4\] = \[4,6\].

- **Scalar multiplication** — multiply every entry by a number. 2 × \[1,2,3\] = \[2,4,6\].

- **Dot product** — multiply corresponding entries and sum: \[a,b,c\]·\[d,e,f\] = ad + be + cf. The result is a single number.

The dot product measures **similarity**: large positive when vectors point the same direction, negative when opposite, zero when perpendicular. Attention is fundamentally a clever use of dot products to measure how related two pieces of context are.

Matrices and matrix multiplication

A **matrix** is a grid of numbers — a rectangle of rows and columns. The shape is written as rows × columns. A vector is just a matrix with one row (or one column).

**Matrix multiplication (matmul)** combines two matrices to produce a third. If A is m × k and B is k × n, then A × B is m × n. The inner dimensions (k and k) must match, and they disappear. Each entry of the result is a dot product between a row of A and a column of B.

> A is 2x3, B is 3x2: \[a b c\] \[g h\] \[ag+bi+ck ah+bj+cl\] \[d e f\] × \[i j\] = \[dg+ei+fk dh+ej+fl\] \[k l\]

**Matmul is the dominant operation in deep learning.** Every linear layer in a neural network is one matmul. The reason GPUs dominate this field is that they are extraordinarily good at doing matmul fast on big matrices.

Tensors

A **tensor** is a generalization of vectors and matrices to higher dimensions. A 1D tensor is a vector. A 2D tensor is a matrix. A 3D tensor is a stack of matrices. PyTorch and friends use the word "tensor" for any multi-dimensional array, no matter how many dimensions.

Inference computations operate on tensors. For example, a transformer might process a batch of 32 sequences, each of length 4096, with each token represented as a 4096-dimensional vector. That's a 3D tensor of shape \[32, 4096, 4096\] — 32 batches × 4096 tokens × 4096 features.

Neural networks as compositions of matmuls

A neural network is a chain of operations. The simplest is a **linear layer**:

> y = xW + b x ∈ R^n (input vector, size n) W ∈ R^{n×m} (weight matrix, learned during training) b ∈ R^m (bias vector) y ∈ R^m (output vector)

Stack two of these and you get a deeper network — but as Lecture 3 will show, you also need a nonlinear **activation function** between them, otherwise the whole thing collapses to a single matmul. ReLU is the simplest activation:

> ReLU(x) = max(0, x)

Anywhere the input is positive, it passes through unchanged. Anywhere it's negative, it gets zeroed out. This little nonlinearity is what makes deep neural networks more expressive than shallow ones.

Embeddings and the meaning of dimensions

Why do vectors have hundreds or thousands of dimensions? Because deep learning works by **encoding semantic meaning as direction in high-dimensional space**. A model's first layer takes a token ID (an integer like 15009) and looks up a learned vector of, say, 4096 numbers. That vector is the token's **embedding** — a learned representation where similar tokens end up near each other.

Embeddings have remarkable properties. The classic example is:

> embedding("king") - embedding("man") + embedding("woman") ≈ embedding("queen")

Directions in embedding space encode meaning. The model learns these embeddings during training by adjusting them so that words used in similar contexts get similar vectors.

Attention — the headline operation

Attention is the mechanism that lets a transformer relate each token in a sequence to every other token. Its formula will appear constantly in this course:

> Attention(Q, K, V) = softmax( Q × K^T / sqrt(d_k) ) × V

Each of Q, K, V is a matrix derived from the input by multiplying it by learned weights. The shape of Q × K^T is N × N where N is the sequence length — every token's query is dotted against every other token's key. The result is a matrix of similarity scores. **Softmax** normalizes each row into probabilities (each row sums to 1). Multiplying that by V weights and aggregates the values.

You will see this formula again and again. For now, the intuition is: **attention is a content-based lookup. Each token decides how much to listen to each other token, based on how their queries and keys align.**

A worked example: small matmul by hand

Let's do one matrix multiplication by hand so you've felt the gears turn. Compute A × B where:

> A = \[1 2\] B = \[5 6\] \[3 4\] \[7 8\]

The result will be 2×2. Each entry is a dot product:

> (A×B)\[0,0\] = row 0 of A · col 0 of B = 1·5 + 2·7 = 19 (A×B)\[0,1\] = row 0 of A · col 1 of B = 1·6 + 2·8 = 22 (A×B)\[1,0\] = row 1 of A · col 0 of B = 3·5 + 4·7 = 43 (A×B)\[1,1\] = row 1 of A · col 1 of B = 3·6 + 4·8 = 50 A × B = \[19 22\] \[43 50\]

A modern transformer doing inference performs trillions of multiplications like these every second. The hardware design of a GPU (Lecture 5) is fundamentally about doing this exact operation as fast as possible.

Self-check

22. If A is 8×16 and B is 16×4, what shape is A × B?

23. Can you multiply a 5×3 matrix by a 4×7 matrix? Why or why not?

24. What does softmax do to a vector? Why is it used in attention?

25. Why do neural networks need activation functions between linear layers?

26. In one sentence, describe what an embedding is.

Suggested external resources

- 3Blue1Brown, "The Essence of Linear Algebra" series — 14 short videos that build geometric intuition for matrices and vectors. Highly recommended.

- Jay Alammar, "The Illustrated Transformer" — best visual explanation of attention available online.

- Andrej Karpathy, "The spelled-out intro to neural networks and backpropagation" — a 2.5-hour video where you build a network from scratch in Python.

Reader 4 — Complexity, memory, attention math

**Pairs with Lecture 4 — Image Generation, Bottlenecks, and Attention**

Why you need this

Lecture 4 introduces the **arithmetic intensity** and **ops:byte ratio** machinery you'll use to diagnose bottlenecks for the rest of the course. The math isn't hard, but it requires comfort with big-O thinking, byte-counting, and reading kernel pseudocode. This reader gets you fluent in those moves.

Concepts to know

Big-O notation

**Big-O notation** describes how the cost of an algorithm grows with the size of its input. We write O(N) to mean "cost grows linearly with N" and O(N²) to mean "cost grows quadratically." Big-O ignores constants and lower-order terms — it captures the asymptotic shape, not the exact runtime.

| **Order** | **Name** | **What it means** | **Example** |
|----|----|----|----|
| O(1) | Constant | Cost doesn't depend on N | Array index lookup |
| O(log N) | Logarithmic | Cost grows very slowly | Binary search |
| O(N) | Linear | Cost grows in proportion | Loop through a list |
| O(N log N) | Linearithmic | Slightly worse than linear | Mergesort, FFT |
| O(N²) | Quadratic | Cost grows fast | Nested loop over N items |
| O(2^N) | Exponential | Catastrophic for large N | Brute-force subset search |

Attention is naively O(N²) in sequence length — every token attends to every other token. At N = 1,000 that's a million dot products. At N = 100,000 (long context) that's 10 billion. This is why attention optimization is such a central topic in inference engineering.

Bytes, kilobytes, megabytes, gigabytes

Modern GPU memory is measured in **gigabytes (GB)**. Let's get the scale straight:

| **Unit**        | **Bytes**      | **Notes**                           |
|-----------------|----------------|-------------------------------------|
| 1 byte (B)      | 8 bits         | One ASCII character, one INT8 value |
| 1 kilobyte (KB) | 1,024 B (~10³) | Small text file                     |
| 1 megabyte (MB) | ~10⁶ B         | Photo, short audio clip             |
| 1 gigabyte (GB) | ~10⁹ B         | HD movie                            |
| 1 terabyte (TB) | ~10¹² B        | Large hard drive                    |

To estimate model size: each parameter is typically stored in **2 bytes (FP16/BF16)**, **1 byte (FP8)**, or **0.5 bytes (FP4)**. So a 70-billion-parameter model at FP8 needs 70 GB just for weights. An H100 has 80 GB VRAM — barely enough, with no room for KV cache. Quantization to FP4 cuts this to 35 GB, leaving headroom.

Bandwidth and throughput in the small

**Bandwidth** is the rate at which data moves through a channel, measured in bytes per second. An H100 has **3.35 TB/s** of HBM bandwidth — that's 3.35 trillion bytes streaming from VRAM to the compute units every second. Sounds like a lot, until you realize a single forward pass through a 70B-parameter FP8 model reads 70 GB of weights, taking ~21 ms just for the memory transfer.

> time_to_load_weights = weight_bytes / bandwidth = 70 GB / 3.35 TB/s = 70 × 10^9 / 3.35 × 10^12 s ≈ 0.021 s = 21 ms

If you're generating one token per forward pass, you can do **at most 1000 / 21 ≈ 47 tokens per second per user** — and that's only if memory bandwidth is the only constraint. This is exactly the kind of "napkin calculation" you'll do constantly.

Compute vs. memory: the dual constraint

Every algorithm running on a GPU is limited by **either** how much arithmetic it can do per second **or** how much data it can move per second. Whichever runs out first is the **bottleneck**. The other is wasted.

- **Compute-bound** — the GPU's compute units are saturated, but memory bandwidth has spare capacity.

- **Memory-bound** — memory bandwidth is saturated, compute units sit idle.

To predict which side you're on, you compare the **arithmetic intensity** of your algorithm (ops per byte moved) to the **ops:byte ratio** of the hardware (peak ops per byte the hardware can sustain).

> intensity \> ops:byte → COMPUTE-bound intensity \< ops:byte → MEMORY-bound intensity = ops:byte → perfectly balanced (ideal)

Lecture 4 walks through this for the standard attention algorithm and gets ~62 ops/byte at sequence length 4096, head dim 128, FP16. The H100's FP16 ops:byte ratio is ~295. 62 \< 295 → attention during decode is **memory-bound** on H100. This single calculation drives an enormous fraction of inference engineering decisions.

Reading a kernel pseudocode

A **kernel** is a function that runs on the GPU. You'll see pseudocode like:

> Kernel: SimpleAttention INPUT: Q, K, V ∈ R^{N×d} in HBM 1. Load Q, K from HBM, compute S = Q K^T, write S to HBM. 2. Read S from HBM, compute P = softmax(S), write P to HBM. 3. Load P, V from HBM, compute O = P V, write O to HBM. RETURN: O

To compute total memory traffic, count every load and every write. Each load/write of an m × n matrix in FP16 (2 bytes per value) moves 2mn bytes. Total compute is harder — it depends on whether you're counting multiplies, adds, or both. A standard convention: each multiply-add counts as 2 operations.

Once you can do this counting fluently, you can predict performance before even running a kernel. That skill is at the heart of inference engineering.

A worked example: counting flops in a small matmul

Compute the cost of A × B where A is 1000×500 and B is 500×200.

**Result shape:** 1000 × 200 = 200,000 entries.

**Per entry:** 500 multiplies + 499 adds ≈ 1,000 operations (treating multiply-add as 2 ops, so 500 MAC × 2 = 1,000).

**Total:** 200,000 × 1,000 = 200,000,000 = **2 × 10⁸ ops = 0.2 GFLOPs**.

**Memory:** Read A = 1000 × 500 × 2 bytes = 1 MB. Read B = 500 × 200 × 2 bytes = 0.2 MB. Write result = 1000 × 200 × 2 bytes = 0.4 MB. Total memory traffic = 1.6 MB.

**Arithmetic intensity:** 2 × 10⁸ ops / 1.6 × 10⁶ bytes = **125 ops/byte**.

On an H100 (ops:byte = 295), this matmul is **memory-bound**. To make it compute-bound, you'd need to do more ops per byte — perhaps by reusing the loaded data, which is exactly what kernel fusion does.

Self-check

27. Why is attention O(N²) and not O(N)? Where does the squaring come from?

28. How many bytes does a 50B-parameter model take at FP8? At FP4?

29. A kernel has arithmetic intensity 400 ops/byte on a GPU with ops:byte = 295. Compute- or memory-bound?

30. In one sentence, explain why FP8 quantization gives both more FLOPS and effectively more memory bandwidth than FP16.

Suggested external resources

- Horace He, "Making Deep Learning Go Brrrr From First Principles" — landmark blog post on compute vs. memory bottlenecks.

- NVIDIA's "GPU Performance Background" white paper — clear discussion of roofline model.

- Tri Dao et al., "FlashAttention" paper — the standard reference for fast attention. Skim the figures.

Reader 5 — Computer architecture primer

**Pairs with Lecture 5 — GPU Hardware**

Why you need this

Lecture 5 dives into GPU architecture: SMs, Tensor Cores, HBM, NVLink, InfiniBand. These terms are meaningless without a working mental model of how computers move data around at all. This reader is a refresher on CPU-vs-GPU architecture and the **memory hierarchy** that both have.

Concepts to know

Why we care about hardware

Software doesn't run in the abstract — it runs on hardware. Inference engineering is one of those rare software fields where you can't safely ignore hardware. The difference between a fast and slow implementation often comes down to whether you're using the hardware as intended. The goal of this reader is to build enough hardware vocabulary to follow the lecture comfortably.

CPUs in one paragraph

A **CPU (Central Processing Unit)** is a general-purpose processor. It has a small number of **cores** (typically 4-64 today) that execute instructions one at a time per core. CPUs are designed for **low-latency, branchy, sequential** workloads — they have deep instruction pipelines, branch prediction, and large caches optimized for irregular memory access patterns. A modern CPU is extremely fast at any one thing but doesn't scale well to thousands of parallel operations.

GPUs in one paragraph

A **GPU (Graphics Processing Unit)** was originally designed to render graphics — to color millions of pixels in parallel. That same architecture turned out to be perfect for the matrix math underlying neural networks. A GPU has thousands of simple cores that run the same operation on different data simultaneously. This is called **SIMD** (Single Instruction, Multiple Data) or, more accurately for NVIDIA, **SIMT** (Single Instruction, Multiple Threads). A GPU is **slow at any one thing** compared to a CPU but **extraordinarily fast at doing the same thing to many things at once**.

The memory hierarchy

Computers use a hierarchy of memory technologies, fast and small to slow and large. This is a fundamental trade-off: the fastest memory is too expensive to make big.

| **Tier** | **Technology** | **Typical size** | **Typical latency** |
|----|----|----|----|
| Registers | Tiny on-chip storage | Bytes per core | Sub-ns |
| L1 cache | SRAM, on-chip | 10s of KB per core | ~1 ns |
| L2 cache | SRAM, on-chip | MBs | ~5 ns |
| L3 cache (CPU) | SRAM, on-chip | 10s of MB | ~20 ns |
| DRAM / VRAM | DRAM, off-chip | 10s-100s of GB | ~80 ns |
| SSD storage | Flash | TBs | ~50,000 ns |
| Network / disk | Various | Effectively unlimited | ms+ |

**SRAM (Static RAM)** is fast but expensive — it needs ~6 transistors per bit. **DRAM (Dynamic RAM)** is denser but slower — one transistor and one capacitor per bit, and it has to be periodically refreshed ("dynamic").

Bandwidth, latency, and locality

Three properties matter when reading/writing memory:

- **Bandwidth** — bytes per second. How much data can flow.

- **Latency** — time to start receiving data. How long the first byte takes.

- **Locality** — does my program reuse data, or scan through giant arrays once?

Caches exist to exploit **locality**. If you read a value, you probably want it again soon (**temporal locality**) or want nearby values (**spatial locality**). Caches transparently keep recently/nearby data in fast memory.

In GPU inference, **temporal locality of the KV cache** is why prefix caching across requests is a huge win (Lecture 8). **Spatial locality of weights** is why kernel fusion matters.

Multi-core, multi-socket, multi-node

Computers can be scaled in three ways:

31. **More cores per chip** — modern CPUs have dozens of cores; GPUs have thousands.

32. **More chips per server** — a server might have 2 CPUs ("sockets") or 8 GPUs.

33. **More servers per cluster** — connected by a fast network.

Each level of scaling adds **communication overhead**. Two cores on the same chip can share cache. Two chips in the same server share memory through a bus. Two servers must talk over a network, which is many times slower. **This is the source of most parallel-computing pain.**

Buses and interconnects

Components inside a computer are connected by **buses** — shared lanes for data. The most important ones for inference:

- **PCIe** (Peripheral Component Interconnect Express) — the standard for connecting CPUs to peripherals like GPUs. Bandwidth: ~32-128 GB/s on modern generations.

- **NVLink** — NVIDIA's proprietary GPU-to-GPU interconnect, much faster than PCIe. 900 GB/s on Hopper, 1,800 GB/s on Blackwell.

- **InfiniBand** — high-speed networking technology used inside datacenters. ~400 Gb/s per NIC on modern systems.

- **Ethernet** — generic networking. Slower than InfiniBand.

**Big takeaway:** intra-GPU memory is the fastest. Intra-node GPU-to-GPU is fast (NVLink). Inter-node is much slower (InfiniBand). This **bandwidth hierarchy** drives the entire parallelism strategy discussion in Lecture 8.

A worked example: estimating cache hit benefit

Imagine your code reads a 4 KB block of data 1,000 times. The first read is a **cache miss** — data comes from DRAM (~80 ns). Subsequent reads are **cache hits** — data comes from L1 (~1 ns).

> All-miss time: 1000 × 80 ns = 80,000 ns = 80 µs Cache-friendly: 1 × 80 ns + 999 × 1 ns ≈ 1,079 ns ≈ 1 µs Speedup: ~75×

This is why **kernel fusion** is so important. Without fusion, intermediate results get written to DRAM (slow) and read back (slow). With fusion, intermediates live in registers (instant). The math is the same — it's just memory choreography.

Self-check

34. Why is a GPU faster than a CPU for matrix multiplication despite each individual GPU core being slower?

35. What's the difference between SRAM and DRAM? Which is used for caches? Which is used for HBM?

36. List the four common interconnect types from fastest to slowest.

37. If two cores share an L2 cache but not L1, what implication does that have for performance?

Suggested external resources

- Patterson & Hennessy, "Computer Organization and Design" — the canonical textbook. Chapters on memory hierarchy and parallelism.

- NVIDIA's H100 white paper — heavy but authoritative on modern GPU architecture.

- "What every programmer should know about memory" by Ulrich Drepper — classic, slightly dated.

Reader 6 — Software stack for ML

**Pairs with Lecture 6 — The Software Stack**

Why you need this

Lecture 6 covers CUDA, PyTorch, ONNX, TensorRT, vLLM, SGLang, TensorRT-LLM, and NVIDIA Dynamo. Knowing where each tool sits in the stack is what lets you reason about new tools without reading every doc page. This reader builds that mental hierarchy.

Concepts to know

Layers of software abstraction

Most software systems are built as **layered abstractions**. Each layer hides the complexity of the layer below it and exposes a simpler interface to the layer above. The classic example is the networking stack: applications talk to TCP, TCP talks to IP, IP talks to Ethernet, etc.

ML inference has a similar layering, from hardware up:

38. **GPU hardware** — Tensor Cores, SMs, HBM. (Lecture 5.)

39. **CUDA** — NVIDIA's GPU programming layer. Provides primitives (kernels, memory management, synchronization).

40. **CUDA libraries** — cuBLAS, cuDNN, CUTLASS — pre-built high-performance kernels for linear algebra and neural network ops.

41. **Deep learning frameworks** — PyTorch, JAX, TensorFlow. Define and run model graphs using CUDA libraries underneath.

42. **Inference engines** — vLLM, SGLang, TensorRT-LLM. Wrap frameworks with optimizations specific to LLM serving (batching, KV caching, etc.).

43. **Orchestration** — NVIDIA Dynamo, Kubernetes-based platforms. Distribute work across many inference-engine replicas.

44. **Client SDKs / APIs** — OpenAI SDK, LangChain. What application developers actually call.

Why so many layers?

Each layer addresses a different audience:

- CUDA = systems programmers writing GPU code.

- Frameworks = ML researchers training and prototyping.

- Inference engines = production ML engineers scaling serving.

- Orchestration = SREs running clusters.

- Client SDKs = product developers.

You'll work mostly in the **inference engine** and **orchestration** layers, but you need to understand the layers below to debug effectively.

CUDA in two paragraphs

**CUDA** is NVIDIA's proprietary platform for writing programs that run on GPUs. The key concept is the **kernel** — a function you write in CUDA C++ that runs in parallel across thousands of threads. A kernel call says "launch N threads, each running this same function, and tell each thread its index."

Most ML code never directly writes CUDA kernels. Instead, it uses pre-built kernels packaged in libraries like **cuBLAS** (linear algebra) and **cuDNN** (neural network primitives). These libraries are NVIDIA-tuned C++ that gets installed alongside CUDA. When you call torch.matmul(A, B) in PyTorch, it ultimately invokes a cuBLAS kernel.

PyTorch and the framework wars

**PyTorch** is the dominant deep learning framework today. It's a Python library that lets you build, train, and run neural networks with clean syntax and automatic differentiation. Originally built at Meta, it's now governed by the Linux Foundation.

Competitors:

- **TensorFlow** — Google's first framework. Once dominant; now niche outside Google.

- **JAX** — Google's research framework. Powerful but sharp edges; used in research.

- **MLX** — Apple's framework for Apple Silicon.

PyTorch's combination of pythonic API + GPU acceleration + huge ecosystem makes it the default choice. Every inference engine you'll learn about is built on PyTorch underneath.

Inference engines: what they actually do

A naive PyTorch deployment is slow because PyTorch is built for flexibility, not for the specific patterns of LLM serving. An **inference engine** is a specialized server that re-implements model execution with LLM-specific optimizations:

- **Continuous batching** — token-level interleaving of many requests.

- **KV cache management** — efficient memory layout for cached attention state.

- **Custom kernels** — hand-written fused kernels (e.g., FlashAttention) for attention.

- **Quantization support** — running models at FP8 or FP4.

- **Speculative decoding** — generating multiple tokens per pass.

All three major engines (vLLM, SGLang, TensorRT-LLM) provide these. They differ in performance, ease of use, and supported hardware — which is why the choice matters.

File formats: where models live on disk

Models are distributed as files. The most common formats:

- **safetensors** — Hugging Face's safe weight format. Simple, fast, can't execute code on load. The default for open models today.

- **GGUF** — used by llama.cpp and the local-inference ecosystem. Bundles weights + tokenizer + config.

- **ONNX** — Open Neural Network Exchange. Includes weights AND the execution graph. Portable across hardware.

- **.pt / .bin / .pkl** — older Python pickle-based formats. Can execute arbitrary code on load — avoid for unknown sources.

When you download Llama 3 from Hugging Face, you get a directory containing many safetensors files (split for parallel download) plus a config.json describing the architecture.

A worked example: tracing a request through the stack

You call OpenAI's API with client.chat.completions.create(model="gpt-5", messages=\[...\]). Here's the layered journey:

45. **Client SDK** (OpenAI Python SDK) — serializes your request to JSON, sends HTTPS POST.

46. **Load balancer** — routes to a backend region.

47. **API gateway** — authenticates, rate-limits, logs.

48. **Orchestration layer** (something like Dynamo) — routes to an inference-engine replica based on which one has the right LoRA / cached prefix / available capacity.

49. **Inference engine** (e.g., TensorRT-LLM) — manages the active batch, schedules your request, runs prefill, starts decode.

50. **Custom kernels** (e.g., FlashAttention) — fused CUDA kernels for the attention sublayer.

51. **cuBLAS / cuDNN** — invoked for the standard linear layers.

52. **CUDA runtime** — launches threads, manages GPU memory.

53. **GPU** — actually does the math on Tensor Cores.

Each layer is a potential source of latency. Lecture 6 will teach you to find and fix bottlenecks in any of them.

Self-check

54. What is the lowest-level layer of the stack you'd typically need to know about as an inference engineer?

55. Why might you choose vLLM over TensorRT-LLM, or vice versa?

56. Why is safetensors safer than Python pickle for distributing model weights?

57. Where do CUDA kernels fit in this layered model?

Suggested external resources

- PyTorch's official tutorial "Deep Learning with PyTorch: A 60 Minute Blitz" — quick familiarization.

- The vLLM blog (blog.vllm.ai) — readable posts on continuous batching and PagedAttention.

- NVIDIA's CUDA Programming Guide — Chapter 2 is enough.

Reader 7 — Numerical precision and floating point

**Pairs with Lecture 7 — Quantization and Speculative Decoding**

Why you need this

Lecture 7 spends most of its time on **quantization** — running models at lower numerical precision (FP8, FP4) for speed and memory. To follow it, you need to know what "precision" means, how floating-point numbers are stored, and why low precision causes quality issues. This reader brings that into focus.

Concepts to know

Why precision matters

Numbers in computers are stored using a fixed number of bits. The more bits, the more values you can represent and the more precisely you can approximate real numbers. But more bits also means more memory and more compute. Inference engineering constantly balances precision vs. cost.

Floating-point representation

Most ML uses **floating-point** numbers, which are stored in scientific-notation-like form. A floating-point number has three pieces:

- **Sign bit** (1 bit) — positive or negative.

- **Exponent** (some bits) — the order of magnitude.

- **Mantissa / fraction** (the remaining bits) — the significant digits.

In FP16 (the 16-bit "half precision" used everywhere in ML), this is 1 + 5 + 10 = 16 bits. The value is roughly sign × mantissa × 2^exponent.

> FP16 layout: \[sign\]\[5-bit exponent\]\[10-bit mantissa\] FP32 layout: \[sign\]\[8-bit exponent\]\[23-bit mantissa\] FP8 (E4M3): \[sign\]\[4-bit exponent\]\[3-bit mantissa\] FP4: \[sign\]\[2-bit exponent\]\[1-bit mantissa\]

Dynamic range vs. precision

The **exponent bits** determine **dynamic range** — the gap between the smallest and largest representable values. The **mantissa bits** determine **precision** — how finely values are spaced within that range.

- **FP16** has 5 exponent bits → range ~10^-8 to 10^4, with ~3 decimal digits of precision.

- **BF16** ("brain float 16") uses 8 exponent bits, only 7 mantissa bits — same range as FP32, less precision. Useful for training because outliers don't overflow.

- **FP8 E4M3** has 4 exponent + 3 mantissa bits — small range, ~1 decimal digit. Surprisingly enough for inference quality.

- **FP4** has 2 exponent + 1 mantissa bit — tiny range, very low precision.

Why integer formats are different

**Integer formats** (INT8, INT4) have no exponent — just sign and value bits. They represent evenly spaced values across a fixed range.

| **Format** | **Total values** | **Spacing** | **Best for** |
|----|----|----|----|
| INT8 | 256 | Uniform | Image classification, simple tasks |
| INT4 | 16 | Uniform | Aggressive compression, quality risk |
| FP8 | 256 | Logarithmic (wider near zero) | LLM inference (sweet spot) |
| FP4 | 16 | Logarithmic | Aggressive LLM compression |

**Why this matters for ML:** neural network values are not uniformly distributed. Most weights and activations cluster near zero, with rare large outliers. Floating-point's logarithmic spacing captures both regimes; integer's uniform spacing wastes representation on the empty middle while clipping the outliers. This is why FP8 beats INT8 for transformer inference.

Quantization, scale factors, and granularity

**Quantization** is the process of converting high-precision values to low-precision ones. The simplest scheme:

58. Find the maximum absolute value in a tensor: max_val = max(\|x\|).

59. Compute a **scale factor**: scale = max_val / max_representable_value (e.g., max_representable_value = 127 for INT8).

60. Quantize: x_quant = round(x / scale).

61. Dequantize when needed: x_approx = x_quant × scale.

**Granularity** is how often you compute a new scale factor:

- **Per-tensor** — one scale factor for the whole tensor. Simple but loses precision in tensors with mixed magnitudes.

- **Per-channel** — one scale factor per channel (row or column). Better.

- **Block-wise** (microscaling) — one scale factor per N values (e.g., per 32). Best for outlier preservation. Used in MXFP8, NVFP4.

Error accumulation

Quantization introduces small rounding errors. In a single multiplication, the error is tiny. But neural networks chain thousands of multiplications. Errors compound. The book uses Pi as an example:

| **Precision** | **Pi**  | **Pi²**  | **Pi³**   |
|---------------|---------|----------|-----------|
| Full          | 3.14159 | 9.869588 | 31.006198 |
| 3 decimals    | 3.14    | 9.8596   | 30.959144 |
| 1 decimal     | 3       | 9        | 27        |

Notice how a 0.5% rounding error in Pi (3.14 vs 3.14159) became a 0.2% error in Pi² but blew up to 14% in lower-precision Pi³. **The deeper the network, the more errors compound.** This is why attention (which conditions every later output on every earlier output) is the most sensitive component to quantize.

Quantization-aware training vs. post-training quantization

Two ways to quantize:

- **Quantization-aware training (QAT)** — train the model with quantization in the loop. Weights are optimized to be robust to the quantized representation. Best quality, but requires the original training infrastructure.

- **Post-training quantization (PTQ)** — take an existing model and convert its weights using calibration data. Much easier; the only option when you didn't train the model.

Most production quantization is PTQ. Frontier labs increasingly ship models with QAT for specific low-precision formats (GPT-OSS in MXFP4, Kimi K2 Thinking in INT4).

A worked example: quantizing a single tensor

Suppose your tensor is x = \[0.1, -0.5, 1.2, -0.05, 0.8\] and you want INT8 (representing values in \[-127, 127\]).

62. Find max abs value: \|1.2\| = 1.2.

63. Scale: scale = 1.2 / 127 ≈ 0.00945.

64. Quantize each: round(x / scale) = round(\[10.6, -52.9, 127.0, -5.3, 84.7\]) = \[11, -53, 127, -5, 85\].

65. Dequantize: x_approx = x_int8 × scale ≈ \[0.104, -0.501, 1.200, -0.047, 0.803\].

Errors: roughly 0.003 per element. Tiny — but if this tensor is the output of one layer of a 100-layer network, the next layer is now multiplying by *those* slightly-wrong values. Hence the importance of careful schemes.

Self-check

66. Why does FP8 give roughly 2× the FLOPS of FP16? Why does it also give 2× effective bandwidth?

67. Why does FP8 work better than INT8 for LLM inference?

68. Why is attention more sensitive to quantization than weight matrices?

69. What is a scale factor? When would you use per-tensor vs. block-wise?

Suggested external resources

- Hugging Face's "Quantization for Beginners" blog series — gentle entry.

- NVIDIA TensorRT Model Optimizer (ModelOpt) GitHub repo — examples worth running locally.

- Tim Dettmers, "LLM.int8()" paper — readable academic intro to LLM quantization issues.

Reader 8 — Parallel computing primer

**Pairs with Lecture 8 — Caching, Parallelism, and Disaggregation**

Why you need this

Lecture 8 covers Tensor Parallelism, Expert Parallelism, Pipeline Parallelism, Context Parallelism, and Disaggregation. All five concepts come from the broader field of **parallel computing**. This reader gives you the vocabulary.

Concepts to know

Three flavors of parallelism

Software can be parallelized in three fundamentally different ways. Most real systems mix them.

Task parallelism

**Task parallelism** = different units do different jobs simultaneously. Think of a kitchen with one cook chopping vegetables, another stirring the pot, a third plating finished dishes. Each is doing different work at the same time. In computing: an OS running a web browser, a music player, and a code editor on different CPU cores is task-parallel.

**Pipeline parallelism** — a special case where the "different jobs" form a sequential pipeline. The output of stage 1 feeds stage 2 feeds stage 3. The same data passes through each stage, but multiple items can be in flight simultaneously (one in stage 3, the next in stage 2, the next in stage 1). Pipeline parallelism in inference splits a model's layers into stages and pipelines requests through them.

Data parallelism

**Data parallelism** = many units do the **same job** on **different data**. The most common pattern in deep learning. To process 1,000 images, you give 100 images to each of 10 GPUs; each runs the same model on its share.

Inference uses data parallelism implicitly when you scale horizontally: 10 replicas of a model server each handle a fraction of incoming traffic.

Model parallelism (tensor parallelism)

**Model parallelism** = different units handle **different parts of the same model**. You split a single model's parameters across multiple devices. The data flows through them all to complete one forward pass.

Tensor parallelism is the dominant form: split each layer's weight matrix across GPUs. Each GPU computes its slice and the partial results are combined via an **all-reduce** operation.

Synchronization primitives

When parallel units must agree on results, they synchronize via **collective operations**:

- **Broadcast** — one unit's data is copied to all others.

- **Gather** — each unit's partial data is collected to one place.

- **Scatter** — opposite of gather; one unit distributes pieces.

- **Reduce** — partial results are combined (sum, max, etc.) into one final result on one unit.

- **All-reduce** — like reduce, but every unit ends up with the final result. The most common in deep learning.

All-reduce is the bottleneck in Tensor Parallelism. Every layer's output requires every GPU to share data with every other. This is why TP is bounded by NVLink bandwidth and doesn't extend cleanly to multi-node.

Amdahl's Law

**Amdahl's Law** says that the speedup from parallelization is limited by the sequential portion of your program. If 10% of your code can't be parallelized, even infinite parallelism gets you at most a 10× speedup.

> speedup = 1 / ((1 - p) + p / n) p = parallelizable fraction n = number of processors Example: p = 0.95, n = 100 → speedup ≈ 17×, not 100×.

This is why all-reduce overhead matters. The communication time is the unparallelizable part of each layer.

Locality and communication cost

Parallel computing has a brutal rule of thumb: **moving data between units is expensive**. The cost grows as you go from registers → cache → DRAM → other GPU on the same node → other GPU on another node. Effective parallel design minimizes inter-unit communication.

| **Communication scope** | **Speed** | **Inference use case** |
|----|----|----|
| Intra-core (registers/cache) | Sub-nanosecond | Kernel fusion |
| Intra-GPU (HBM) | Hundreds of GB/s | Standard model execution |
| Inter-GPU intra-node (NVLink) | Hundreds-Thousands of GB/s | Tensor Parallelism |
| Inter-node (InfiniBand) | Tens of GB/s | Pipeline / Expert Parallelism |
| Inter-datacenter (network) | GB/s or less | Multi-cloud only |

Workload imbalance and stragglers

If you split work across 100 GPUs and 99 finish in 100 ms but 1 takes 500 ms, the whole job takes 500 ms. The slowest unit is the **straggler**, and it pins overall performance. Real systems must handle this via load balancing, queueing, and timeouts. (Llama 3 training had 419 failures in 54 days, per Lecture 10 — failure handling is part of "workload imbalance" at scale.)

A worked example: where does TP's all-reduce cost come from?

Imagine an 8-GPU Tensor Parallel setup serving Llama 3 70B. Each forward pass through one transformer layer:

70. Each GPU computes its slice of the layer (~1/8 of the matmul). Fast.

71. All-reduce: every GPU must combine partial outputs with every other GPU. A 70B-param model has ~80 layers, so this all-reduce happens 80 times per forward pass.

72. On NVLink (900 GB/s), each all-reduce of a hidden-state vector takes ~microseconds.

73. Total per forward pass: ~milliseconds of pure NVLink traffic.

Now imagine you tried TP across two nodes via InfiniBand (~50 GB/s). Same 80 all-reduces, but each is ~18× slower. The forward pass would be choked by communication. This is why TP doesn't extend to multi-node, and why you use EP or PP instead.

Self-check

74. What's the difference between data parallelism and model parallelism?

75. Which of TP / EP / PP requires the most inter-GPU communication?

76. State Amdahl's Law in your own words. Why does it limit Tensor Parallelism's scalability?

77. Why does NVLink bandwidth shape parallelism strategy choices?

Suggested external resources

- PyTorch's distributed training docs — although they're training-focused, the parallelism primitives are identical.

- Hugging Face's "Performance and Scalability" guide — covers tensor, pipeline, and expert parallelism cleanly.

- Bill Dally's lectures on GPU parallelism (Stanford CS 149) — free on YouTube.

Reader 9 — Modalities and signal processing

**Pairs with Lecture 9 — Modalities Beyond Text**

Why you need this

Lecture 9 covers vision, audio, image generation, and video. Each has its own representations — pixels, spectrograms, latents — and its own measurement conventions. This reader fills in the gaps.

Concepts to know

How computers represent images

An **image** is a 2D grid of **pixels**, each pixel being three numbers: the intensities of red, green, and blue. A 1024×1024 RGB image is therefore a 3D array of shape \[1024, 1024, 3\], holding 3.1 million numbers. If each is a 1-byte value (0-255), the raw image is 3 MB.

ML models can't operate on raw 3.1-million-element vectors easily — that's where **latent space** comes in. A trained encoder compresses an image into a much smaller representation (e.g., \[128, 128, 4\] ≈ 65K numbers, 1% of pixel space) that retains the semantic content. Lecture 4 covered this: image generation works in latent space, then a VAE decoder converts back to pixels.

How computers represent audio

An **audio signal** is a 1D sequence of amplitude values — samples taken many times per second (e.g., 16,000 samples/sec). One minute of audio at 16 kHz mono is 960,000 numbers.

Working directly with raw samples is awkward. Instead, audio ML uses **spectrograms** — 2D representations where one axis is time and the other is frequency. Computed via **Fourier transforms**. A **mel spectrogram** is a perceptually-weighted version aligned with human hearing. Whisper's encoder takes a log-mel spectrogram as input.

How computers represent video

**Video** = a sequence of images, typically 24-30 frames per second. One second of HD video at 30 fps is 30 × 1024 × 1024 × 3 = 94 million numbers. Latent representations are essential — even more so than for static images.

Video latent space is 3D: width × height × time. Video models like Sora and Veo work entirely in this 3D latent space. The latent for a 5-second 1024×1024 video might be \[128, 128, 16\] (16 latent time slices), still 260K numbers.

Diffusion and iterative denoising

**Diffusion models** generate images (or video) by starting from random noise and iteratively cleaning it up. The model is trained to predict what the next "cleaner" version looks like given the current noisy version. After 30-50 steps, the noise has been transformed into a coherent image.

Each step calls the **denoising model** (a neural network) twice — once with the prompt as conditioning, once without — and combines the results via **classifier-free guidance**. So 50 denoising steps = ~100 forward passes through the network.

Encoders and embeddings — generalizing beyond text

In Lecture 3 you saw text embeddings. The same idea generalizes to any modality:

- **Text embeddings** — variable-length text → fixed vector. Used for search, RAG, memory.

- **Image embeddings** — image → vector. Used for image search, content moderation.

- **Audio embeddings** — audio clip → vector. Used for music recommendation, sound matching.

Embedding models share architecture patterns with generative models but produce a single vector rather than a sequence. This makes them fast and parallelizable — Lecture 9 will spend time on the implications.

ASR, TTS, and the speech ecosystem

**ASR (Automatic Speech Recognition)** = speech-to-text. The standard open model is **Whisper** from OpenAI. Architecturally it's encoder-decoder: the encoder converts log-mel spectrogram to features, and the decoder generates tokens like an LLM.

**TTS (Text-to-Speech)** = the reverse: text → audio waveform. Modern TTS models (e.g., Orpheus) are based on LLMs with an expanded vocabulary that includes audio tokens. A separate **audio decoder** (e.g., SNAC) converts those tokens to waveform.

**Voice Activity Detection (VAD)** — a small auxiliary model that detects speech vs. silence in an audio stream. Used to chunk audio into pieces for streaming ASR. Real-time voice products are typically cascading pipelines: VAD → ASR → LLM → TTS.

Real-Time Factor (RTF) — the audio metric

**RTF (Real-Time Factor)** measures how fast an audio model can process audio relative to its duration. RTF 1× means "transcribes audio at real-time speed" (1 minute of audio in 1 minute). Optimized Whisper deployments hit RTF ~1,000× — transcribing an hour of audio in under 4 seconds.

For interactive speech, RTF must be ≥1× per chunk. For batch processing, higher RTF = more throughput per GPU = lower cost.

A worked example: estimating video latent dimensions

Suppose you want to generate a 5-second 1024×1024 video at 24 fps. What does the latent representation look like?

78. Total frames: 5 × 24 = 120 frames.

79. Latent compression: typical 8× spatial, 4× temporal.

80. Spatial latent: 1024/8 = 128, so each frame's latent is 128×128.

81. Temporal latent: 120/4 = 30 time slices.

82. Channels: typically 4 latent channels.

83. Latent shape: \[30, 128, 128, 4\] = 1,966,080 values.

Versus the pixel representation: \[120, 1024, 1024, 3\] = 377 million values. Latent space is ~190× smaller — and you still attend over it, which is why video gen is so compute-intensive. Lecture 9 explains why batch size 1 is the norm and why Context Parallelism exists.

Self-check

84. Why do image and video generation models work in latent space rather than pixel space?

85. What is a log-mel spectrogram and why is it useful for speech models?

86. Why is RTF the natural latency metric for audio rather than TPS?

87. Explain in one sentence why cascading voice pipelines (VAD → ASR → LLM → TTS) still beat unified speech-to-speech models for most products.

Suggested external resources

- OpenAI's Whisper paper ("Robust Speech Recognition via Large-Scale Weak Supervision") — readable and influential.

- Sander Dieleman's blog "Diffusion models are autoencoders" — best conceptual intro to diffusion.

- Hugging Face's transformers documentation pages for vision and audio models.

Reader 10 — Distributed systems for production

**Pairs with Lecture 10 — Production**

Why you need this

Lecture 10 covers containers, Kubernetes, autoscaling, multi-cloud, canary deploys, and the cost / observability discipline of running real systems. Most of this comes from general distributed systems engineering. This reader sets the foundations.

Concepts to know

What "distributed" actually means

A **distributed system** is any system whose components run on multiple machines and coordinate over a network. Your phone talking to a cloud backend is one. A datacenter with 16,000 GPUs is one. Distributed systems have fundamental properties that single-machine programs don't:

- **Partial failure** — any one component can fail while others keep running.

- **Latency** — communication is much slower than local memory access.

- **No global clock** — different machines disagree about "now" by milliseconds.

- **Concurrency** — many requests in flight simultaneously.

"You can't tell the difference between a slow response and a failed one" — the **FLP impossibility result** in distributed systems. Production engineering is largely about working around this.

Containers and Docker

A **container** packages an application with all its dependencies (libraries, configs, system tools) into a portable, isolated unit. Containers share the host OS kernel (unlike full virtual machines), making them lightweight and fast to start.

**Docker** is the most widespread containerization technology. Vocabulary:

- **Container** — a running instance of an image.

- **Image** — the packaged executable artifact. Immutable.

- **Dockerfile** — text-file recipe for building an image.

- **Registry** — server that stores images (Docker Hub, NVIDIA NGC, GitHub Container Registry).

In ML inference, container images bundle the CUDA toolkit, the inference engine, the model weights or weight-loading scripts, and the serving code. They guarantee that what runs in dev also runs in production.

Kubernetes in 200 words

**Kubernetes ("K8s")** is an orchestration system for running containers at scale. You describe what you want ("3 replicas of this inference server, with these resources, behind this load balancer") and Kubernetes makes it happen — scheduling pods to nodes, restarting failed ones, scaling up under load.

Key concepts:

- **Pod** — the smallest deployable unit; one or more containers sharing networking and storage.

- **Node** — a physical or virtual machine in the cluster.

- **Cluster** — a set of nodes managed together.

- **Deployment** — declarative spec for a set of pods (with replica count, image, resources).

- **Service** — stable network identity in front of a changing set of pods.

- **Control plane** — the brain (scheduler, API server, etc.).

- **Worker plane** — where pods actually run.

All modern inference platforms run on Kubernetes underneath. You don't need to be a K8s expert, but you should recognize these terms when they appear in lecture and docs.

Load balancing and routing

When you have many replicas of a service, you need to decide which replica handles each incoming request. This is the job of a **load balancer**. Simple strategies:

- **Round-robin** — alternate replicas in order.

- **Least-connections** — pick the replica with the fewest in-flight requests.

- **Random** — uniformly random replica selection.

For inference, smarter strategies pay off:

- **KV-cache-aware** — send a user's chat to the replica that already has their prefix cached.

- **LoRA-aware** — send to a replica that has the right adapter loaded.

- **Geo-aware** — send to the replica closest to the user.

Autoscaling

**Autoscaling** means adjusting the number of replicas based on current demand. Scale up when traffic rises, down when it falls.

Three knobs that always need tuning:

- **Trigger signal** — utilization (lagging) and/or traffic (proactive).

- **Window** — how long to observe before deciding.

- **Cooldown / scale-down delay** — how long to wait before honoring a scale-down (avoids thrashing on bursty traffic).

For inference, autoscaler concurrency targets must match the engine's batch size. A mismatch means either wasted GPU (too low) or queueing (too high).

Deployment strategies

Shipping new versions of a service in production:

- **Hard cutover** — replace v1 with v2 instantly. Risky: bugs hit everyone.

- **Blue-green** — run v1 (blue) and v2 (green) in parallel; switch all traffic at once. Doubles capacity cost during the switch. Bad for GPU inference.

- **Canary** — gradually shift a percentage of live traffic to v2 (1%, 5%, 25%, 100%). Catches regressions early at low blast radius. Good for GPU inference.

Observability: logs, metrics, traces

Production systems need **observability** — visibility into what they're doing right now. Three pillars:

- **Logs** — text events emitted by the system. Detailed but slow to search at scale.

- **Metrics** — numerical time-series (requests/sec, P99 latency, GPU utilization). Cheap, queryable, the backbone of dashboards and alerts.

- **Traces** — follow a single request through every component it touches. Invaluable for finding bottlenecks across services.

Industry-standard tools: Grafana (dashboards), Prometheus (metrics), Datadog / New Relic (commercial), Sentry (errors), PagerDuty (paging humans for incidents). Every production system needs all of these.

Reliability and the cost of failure

Hardware fails. Networks partition. Datacenters lose power. Your code has bugs. Production engineering accepts these facts and designs around them:

- **Redundancy** — multiple replicas in multiple zones / regions.

- **Health checks** — automatic detection of broken pods.

- **Retries with backoff** — transient failures are common; retry with exponential delay.

- **Circuit breakers** — stop sending traffic to a service that's clearly failing.

- **Postmortems** — after every incident, document the cause and the fix.

A worked example: cost of cold starts in autoscaling

Your service has minimum 0 replicas (scale to zero) and bursty traffic. A new replica's cold start time is 90 seconds (image pull + weight load + engine compile + first request handled). A surge of 100 requests hits an empty system.

88. **0 s:** request 1 arrives. Autoscaler triggers; replica 1 starts.

89. **0-90 s:** replica 1 booting. Requests queue.

90. **90 s:** replica 1 ready. Starts handling. Backlog of ~100 requests.

91. **90 s onward:** users see 90-second response times. Disastrous.

**Mitigations:** keep min replicas \> 0 (sacrifice some cost savings for SLA), pre-warm replicas before predicted spikes, parallelize cold starts (autoscale faster), reduce cold-start time (cache engines, slim images).

Lecture 10 will walk through these in detail. Be ready to think in seconds, dollars, and user experience all at once.

Self-check

92. What's the difference between blue-green and canary deployment?

93. Why is scale-to-zero a bad idea for latency-sensitive consumer products?

94. Name the three pillars of observability and what each is good for.

95. Why must autoscaler concurrency target match the inference engine's batch size?

Suggested external resources

- Martin Kleppmann, "Designing Data-Intensive Applications" — the standard reference for production distributed systems.

- Google's SRE book (free online at sre.google/books) — the canonical guide to operating real systems.

- Kubernetes' own "Concepts" docs — best free tutorial on K8s vocabulary.

After the course

If you've worked through this reader before each lecture and through the study guide and problem sets along the way, you'll come out of this course ready to read the book *Inference Engineering* end to end with comprehension, contribute to open-source inference engines, and ask sharp questions in interviews at any AI infrastructure company.

Areas to deepen after the course:

- **Run your own inference server.** Rent a GPU on RunPod, Vast, or Lambda. Deploy a Llama or Qwen model with vLLM. Benchmark it. Quantize it. Try speculation. Watch the metrics move.

- **Read code, not just papers.** vLLM, SGLang, and llama.cpp are all open source. Reading their source teaches more in a week than any book chapter.

- **Follow the open-model release cadence.** New frontier-class models drop almost monthly. Reading their release notes is the fastest way to stay current.

- **Build something users will pay for.** Inference engineering is dual-purpose: it's a research interest, but it's also the most-demanded production skill in tech today. Nothing forces clarity like running a service real customers depend on.

---

## Appendix — If you have extra time (per-reader deeper-dive pointers)

The main reader bodies give you the *minimum*. This appendix is for students who finish the reader with time left over. Each pointer is one rabbit hole — not a syllabus. Pick whichever one looks most interesting; don't try to do all of them.

### Reader 1 deeper dive — the inference economy

Read a16z's *State of AI Inference 2025* report (or whatever the latest annual is). Notice three things: (1) how fast cost-per-million-tokens is dropping (~10×/year); (2) how rapidly open-model quality is closing on closed-model quality; (3) which companies are positioning at each layer (chip → cloud → inference → app). The macro trend is the *why* behind this entire course existing. ~30 min.

### Reader 2 deeper dive — percentile arithmetic for engineers

Watch Gil Tene's classic talk "How NOT to measure latency" (search YouTube; ~40 min). The takeaway you'll carry forever: averages lie, and most latency dashboards in industry are wrong. After watching, look at any production dashboard you have access to and ask: "if this graph said the truth, what would it look like?" Bonus: read about *coordinated omission* and why most load generators undercount tail latency. ~60 min total.

### Reader 3 deeper dive — see a real transformer in 200 lines

Karpathy's *nanoGPT* repo (github.com/karpathy/nanoGPT) implements a complete GPT-style transformer in fewer lines than this reader. Read `model.py` top to bottom — you will see *every* concept from Reader 3 in real code: linear layers, multi-head attention, the residual stream, the LM head, the loss. If you only do one deeper dive in the whole course, do this one. ~90 min.

### Reader 4 deeper dive — the FlashAttention paper

Read the original FlashAttention paper (Dao et al., 2022 — arXiv:2205.14135). You don't need to follow every equation. Focus on Section 1 (the IO-aware framing) and Figure 1 (the tiling diagram). Understanding *why* FlashAttention works will deepen your intuition for the memory-bound nature of attention and the arithmetic-intensity calculations from this reader. ~60 min.

### Reader 5 deeper dive — read an H100 whitepaper

NVIDIA publishes detailed architecture whitepapers (search "H100 architecture whitepaper PDF"). Read the first ~20 pages. Notice how much of the design is about *moving data* rather than computing on it — caches, HBM, NVLink, NVSwitch. This will reinforce why memory hierarchy dominates inference performance. The math sections you can skim. ~75 min.

### Reader 6 deeper dive — vLLM's continuous batching, in code

Clone the vLLM repo (github.com/vllm-project/vllm). Open `vllm/core/scheduler.py` (or whatever the current path is). Read the `Scheduler` class. You don't need to understand every line — just see the data structures (waiting queue, running queue, swapped queue) and the *shape* of how requests get scheduled at token granularity. This is what "continuous batching" actually looks like in production code. ~75 min.

### Reader 7 deeper dive — visualize FP8 outliers

Find a small open model on Hugging Face. Use `bitsandbytes` or `torch.quantization` to quantize the weights to FP8 and INT8. Plot the per-tensor value distributions before and after. You'll *see* why floats preserve outliers and integers clip them — the long tails matter for attention. This is a 1-hour Python exercise that will give you durable intuition for the rest of the course. ~60 min.

### Reader 8 deeper dive — a one-pager on all-reduce

Read the NCCL documentation on collective operations (search "NCCL all-reduce"). Pay attention to the *ring* and *tree* algorithms. Understanding why all-reduce gets expensive at scale is the unifying mental model for why TP stays inside a node and why pipeline-bubble overhead is real. ~30 min.

### Reader 9 deeper dive — read the Whisper paper

Read OpenAI's Whisper paper (Radford et al., 2022 — arXiv:2212.04356). Focus on Section 3 (the encoder-decoder architecture) and Section 5 (real-world robustness). You'll see how ASR borrows the transformer recipe but adapts it for audio: mel-spectrogram input, encoder over audio frames, decoder over text tokens. Helps demystify the modality-specific tweaks the lecture will cover. ~60 min.

### Reader 10 deeper dive — a real postmortem

Read one public outage postmortem from a major AI provider (e.g., OpenAI's status.openai.com or Anthropic's status page archives). Notice three things: (1) what triggered the outage; (2) what monitoring caught it (and what didn't); (3) what changes shipped after. Real-world distributed systems engineering is mostly about *what went wrong* and how to never do that exact thing again. ~45 min.

---

## Cross-reference — readers and the concept graph

If you're using `docs/kb/concepts.json` as a knowledge map, here's which Inference-phase concepts each reader prepares you to learn:

| Reader | Concepts unlocked |
|---|---|
| 1 | `inference-vs-training`, `ai-stack-overview` |
| 2 | `latency-throughput`, `token`, `context-window`, `temperature` |
| 3 | `transformer-architecture`, `self-attention` |
| 4 | `kv-cache`, `flash-attention`, `paged-attention` |
| 5 | `gpu-memory-hierarchy`, `gpu-generations` |
| 6 | `cuda-stack`, `inference-engines`, `continuous-batching` |
| 7 | `quantization` |
| 8 | `tensor-parallelism`, `moe`, `mla`, `disaggregated-serving`, `speculative-decoding` |
| 9 | (modality-specific concepts — see Glossary B.6 on Decode and B.18 on memory-bound vs compute-bound) |
| 10 | `inference-cost` |

If you finish a reader and want to test your readiness, the matching Glossary extended-entry (Appendix B in the Glossary file) is the right next stop — it goes one level deeper on the most important concept for that lecture.
