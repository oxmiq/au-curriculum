# Day 6 · What Happens When You Send a Prompt

> **Concept of the day:** the inference pipeline. Tokenize → embed → layers → logits → sample. One forward pass = one token out.<br>
> **Pre-reading:** <a href="https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices" target="_blank" rel="noopener">Databricks - LLM Inference Performance Engineering</a> (read the inference-pipeline overview: prefill/decode, KV cache, batching).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 - The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 6 · What Happens When You Send a Prompt</span>
    {status:week-02/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Inference Pipeline |
| Part 3 | Deep Dive: Prefill vs Decode |
| Part 4 | Worked Example Analysis |
| Part 5 | Hands-On: Trace the Pipeline |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: Inference Engineering Pre-Lecture Reading - **Reader 1 (AI in production)**.

### Quick Self-Check

Answer these questions from memory:

1. What's more expensive long-term: training or inference? Why?
2. What's the difference between a closed model and an open model? Name one of each.
3. What is a **token**?

If you couldn't answer all three, review the Pre-Lecture Reading again before proceeding.

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m1-readiness" data-kind="readiness" data-draw="5" data-source="Databricks - LLM Inference Performance Engineering">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "In LLM engineering, what is the fundamental difference between training and inference?", "options": ["Training is batch processing; inference is real-time", "Training updates model weights; inference only reads weights", "Training happens on GPUs; inference can happen on CPUs", "Training is done by researchers; inference is done by users"]},
  {"stem": "Why is inference often more expensive than training in the long run?", "options": ["Inference requires more compute per token", "Inference is done continuously for every user query, while training is one-time", "Training can be parallelized but inference cannot", "Inference models are always larger than training models"]},
  {"stem": "What is the tokenization step in the inference pipeline?", "options": ["Converting the model's output to text", "Breaking the input text into tokens (subword units) the model can process", "Compressing the model weights", "Encrypting the prompt for security"]},
  {"stem": "In the inference pipeline (tokenize → embed → layers → logits → sample), what do the 'layers' component do?", "options": ["They tokenize the input", "They run the transformer forward pass to process the embedded tokens", "They select the next token", "They store the conversation history"]},
  {"stem": "What is the 'sample' step in the inference pipeline?", "options": ["Loading the model into memory", "Selecting the next token from the logits using a sampling strategy", "Summarizing the output for the user", "Caching the response for future use"]},
  {"stem": "What does KV caching optimize in inference?", "options": ["It caches the final output text", "It caches key and value matrices from attention to avoid recomputing them for each generated token", "It compresses the model weights", "It stores user sessions"]},
  {"stem": "Why is batching important for inference cost?", "options": ["Batching reduces the number of model weights", "Batching amortizes the cost of a single forward pass across multiple requests", "Batching eliminates the need for GPUs", "Batching automatically optimizes the model size"]},
  {"stem": "What is quantization in the context of LLM inference?", "options": ["Converting tokens to text", "Reducing model weight precision (e.g., from 16-bit to 8-bit) to reduce memory and compute costs", "Encrypting the model for security", "Sampling multiple tokens at once"]}
]
</script>
</div>

---

## Part 2 - Core Concepts: Inference Pipeline
### Reading - Why This Matters

Phase 1 (Weeks 2–5) is a four-week zoom-in on the **inference loop**. Before we open up the GPU (Day 7), the cache (Week 3), or the cluster (Week 4), you need a working mental model of what *actually happens* when a user hits send.

### The Inference Pipeline

```
text  →  [tokenize]  →  token IDs  →  [embed]  →  vectors  →
        [transformer layers × N]  →  hidden states  →
        [LM head]  →  logits  →  [sample]  →  next token
```

Then **loop** the layers→logits→sample steps. Each loop = one output token.

### Five Stages, In One Sentence Each

| Stage | What Happens | Input → Output |
|-------|--------------|-----------------|
| **1. Tokenize** | Text becomes integers (typically BPE-encoded, vocabulary 32K–200K) | "Hello world" → [1234, 5678] |
| **2. Embed** | Each token ID becomes a dense vector (the model's hidden size, e.g. 4096) | [1234] → [0.1, -0.3, 0.5, ...] |
| **3. Layers** | Vectors pass through N transformer blocks (attention + MLP), each refining the representation. *This is where the GPU spends its time.* | [vector] × 32-80 layers |
| **4. Logits** | The final hidden state is projected to a probability distribution over the entire vocabulary | [hidden state] → [0.001, 0.023, ...] |
| **5. Sample** | Pick one token (greedy, top-k, top-p, temperature). That's your next output. | [logits] → "Paris" |

---

## Part 3 - Deep Dive: Prefill vs Decode
### Reading - Two Phases of Inference

### Prefill

- **What:** Run all your *input* tokens through the layers in one shot
- **How:** Parallel - all tokens processed simultaneously
- **What it does:** Computes the initial hidden states for each input token
- **Bottleneck:** Compute-bound (GPU is fully busy)
- **Drives:** **TTFT** (Time To First Token)

### Decode

- **What:** Generate output tokens one at a time
- **How:** Sequential - each token depends on all previous tokens
- **What it does:** Uses KV cache from prefill to predict the next token
- **Bottleneck:** Memory-bound (waiting for KV cache reads)
- **Drives:** **TPS** (Tokens Per Second)

### Key Insight

> **Prefill = compute-bound** (GPU is the bottleneck)
> **Decode = memory-bound** (KV cache reads are the bottleneck)

This distinction drives everything in Weeks 2-4.

---

## Part 4 - Worked Example Analysis
### Reading - Timeline of a Chat Request

From the Pre-Lecture Reading:

> Suppose you ask "What is the capital of France?" Here is what's happening behind the scenes:

| Time | What Happens |
|------|--------------|
| 0 ms | Your browser sends a request to the server |
| 30 ms | Request reaches load balancer, routed to data center |
| 40 ms | Backend assembles prompt (system + history + question) |
| 45 ms | Backend forwards input to inference server |
| **45-200 ms** | **Prefill** - process all input tokens at once |
| **200 ms** | **First token** ("Paris") is generated - TTFT |
| 200-300 ms | **Decode** - generate remaining tokens one at a time |
| 300 ms | Stop token emitted, response complete |

### Annotate the Timeline

1. **Where does TTFT live?** (Answer: 45-200 ms)
2. **Where does end-to-end latency live?** (Answer: 45-300 ms)
3. **What's happening in the 45-200 ms window?** (Answer: Prefill - compute-intensive)
4. **What's happening in the 200-300 ms window?** (Answer: Decode - memory-intensive)

---

## Part 5 - Hands-On: Trace the Pipeline
### Exercise 1: Trace a Prompt

On paper, trace a 5-word prompt through the pipeline. For each stage, annotate:
- Input shape
- Output shape
- What changed

**Example:**
```
Input: "What is AI?"

Tokenize: "What" → 1234, "is" → 567, "AI" → 8901, "?" → 42
Embed: [1234] → [0.1, -0.3, 0.5, ...] (4096 floats)
Layers: 32 layers of attention + MLP
Logits: [0.001, 0.023, ...] (vocabulary size, e.g., 50K)
Sample: "Artificial" (next token)
```

### Exercise 2: Calculate Forward Passes

Given:
- 1000 input tokens
- 500 output tokens
- Model: 32 layers, hidden size 4096

**Calculate:**

1. How many total forward passes? (Answer: 1000 + 500 = 1500)
2. How many prefill passes? (Answer: 1000)
3. How many decode passes? (Answer: 500)

---

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 6 · What Happens When You Send a Prompt">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What is the correct order of the five stages in the LLM inference pipeline?", "options": ["Embed → Tokenize → Layers → Logits → Sample", "Tokenize → Embed → Layers → Logits → Sample", "Tokenize → Layers → Embed → Sample → Logits", "Layers → Tokenize → Embed → Logits → Sample"]},
  {"stem": "What is the key difference between the prefill phase and the decode phase?", "options": ["Prefill generates tokens one at a time; decode processes all input tokens at once", "Prefill processes all input tokens in parallel; decode generates output tokens one at a time", "Prefill is memory-bound; decode is compute-bound", "Prefill happens on the CPU; decode happens on the GPU"]},
  {"stem": "What drives TTFT (Time To First Token)?", "options": ["The decode phase - how fast individual output tokens are generated", "The prefill phase - how fast all input tokens are processed", "The sampling step - how quickly the logits are converted to a token", "The embedding step - how fast token IDs become vectors"]},
  {"stem": "Why is inference more expensive than training over a model's lifetime?", "options": ["Inference requires more memory than training", "Training is a one-time cost; inference costs accumulate with every user query across the model's lifetime", "Inference hardware is more expensive than training hardware", "Inference cannot be parallelized, unlike training"]},
  {"stem": "In the worked example timeline (Part 4), what is happening during the 45–200 ms window?", "options": ["Decode - generating output tokens one at a time", "Prefill - processing all input tokens in parallel", "Network transit from the user's browser to the data center", "Sampling - selecting the final token from logits"]},
  {"stem": "Why is KV caching critical for decode performance?", "options": ["It compresses the model weights to save memory", "It caches key and value matrices from previous tokens so they don't need to be recomputed each decode step", "It reduces the number of output tokens generated", "It stores the final output to avoid re-running inference for repeated queries"]},
  {"stem": "Which phase of inference is compute-bound and which is memory-bound?", "options": ["Both prefill and decode are compute-bound", "Both prefill and decode are memory-bound", "Prefill is compute-bound; decode is memory-bound", "Prefill is memory-bound; decode is compute-bound"]},
  {"stem": "In the Part 5 exercise (1000 input tokens, 500 output tokens), how many decode forward passes are required?", "options": ["500 - one decode pass per output token", "1000 - one per input token", "1500 - one per input and output token combined", "1 - decode processes all output tokens in parallel"]},
  {"stem": "Which throughput metric does the decode phase drive?", "options": ["TTFT (Time To First Token)", "The model's vocabulary size", "TPS (Tokens Per Second)", "The embedding dimension"]}
]
</script>
</div>

### Connect Forward

Tomorrow: we crack open the GPU itself: SMs, Tensor Cores, HBM. Today's "layers spend GPU time" becomes tomorrow's "*here's exactly where in the chip that time goes*."

### Pre-read for tomorrow (Day 7 · Meet the GPU)

- **Resource:** <a href="https://resources.nvidia.com/en-us-hopper-architecture/nvidia-tensor-core-gpu-datasheet" target="_blank" rel="noopener">NVIDIA H100 GPU Datasheet</a> (focus on: SMs, memory capacity, bandwidth, peak FLOPS).
- **Reflection questions:**
  1. What does "80 GB HBM3" mean? (Memory technology + capacity.)
  2. What's an SM? What's a Tensor Core?
  3. Why is intra-GPU memory faster than GPU-to-GPU which is faster than node-to-node?

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
