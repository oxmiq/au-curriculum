# Day 6 · What Happens When You Send a Prompt

> **Concept of the day:** the inference pipeline. Tokenize → embed → layers → logits → sample. One forward pass = one token out.<br>
> **Pre-reading:** Inference Engineering Pre-Lecture Reading — **Reader 1 (AI in production)** (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 — The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 6 · What Happens When You Send a Prompt</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-02/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Inference Pipeline | 20 min |
| Part 3 | Deep Dive: Prefill vs Decode | 20 min |
| Part 4 | Worked Example Analysis | 25 min |
| Part 5 | Hands-On: Trace the Pipeline | 30 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review · 15 min
### Before You Start

You should have already read: Inference Engineering Pre-Lecture Reading — **Reader 1 (AI in production)** (~15 min).

### Quick Self-Check

Answer these questions from memory:
1. What's more expensive long-term: training or inference? Why?
2. What's the difference between a closed model and an open model? Name one of each.
3. What is a **token**?

If you couldn't answer all three, review the Pre-Lecture Reading again before proceeding.

---

## Part 2 — Core Concepts — Inference Pipeline · 20 min
### Reading — Why This Matters

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

## Part 3 — Deep Dive — Prefill vs Decode · 20 min
### Reading — Two Phases of Inference

### Prefill

- **What:** Run all your *input* tokens through the layers in one shot
- **How:** Parallel — all tokens processed simultaneously
- **What it does:** Computes the initial hidden states for each input token
- **Bottleneck:** Compute-bound (GPU is fully busy)
- **Drives:** **TTFT** (Time To First Token)

### Decode

- **What:** Generate output tokens one at a time
- **How:** Sequential — each token depends on all previous tokens
- **What it does:** Uses KV cache from prefill to predict the next token
- **Bottleneck:** Memory-bound (waiting for KV cache reads)
- **Drives:** **TPS** (Tokens Per Second)

### Key Insight

> **Prefill = compute-bound** (GPU is the bottleneck)
> **Decode = memory-bound** (KV cache reads are the bottleneck)

This distinction drives everything in Weeks 2-4.

---

## Part 4 — Worked Example Analysis · 25 min
### Reading — Timeline of a Chat Request

From the Pre-Lecture Reading:

> Suppose you ask "What is the capital of France?" Here is what's happening behind the scenes:

| Time | What Happens |
|------|--------------|
| 0 ms | Your browser sends a request to the server |
| 30 ms | Request reaches load balancer, routed to data center |
| 40 ms | Backend assembles prompt (system + history + question) |
| 45 ms | Backend forwards input to inference server |
| **45-200 ms** | **Prefill** — process all input tokens at once |
| **200 ms** | **First token** ("Paris") is generated — TTFT |
| 200-300 ms | **Decode** — generate remaining tokens one at a time |
| 300 ms | Stop token emitted, response complete |

### Annotate the Timeline

1. **Where does TTFT live?** (Answer: 45-200 ms)
2. **Where does end-to-end latency live?** (Answer: 45-300 ms)
3. **What's happening in the 45-200 ms window?** (Answer: Prefill — compute-intensive)
4. **What's happening in the 200-300 ms window?** (Answer: Decode — memory-intensive)

---

## Part 5 — Hands-On — Trace the Pipeline · 30 min
### Exercise 1: Trace a Prompt (15 min)

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

### Exercise 2: Calculate Forward Passes (15 min)

Given:
- 1000 input tokens
- 500 output tokens
- Model: 32 layers, hidden size 4096

**Calculate:**
1. How many total forward passes? (Answer: 1000 + 500 = 1500)
2. How many prefill passes? (Answer: 1000)
3. How many decode passes? (Answer: 500)

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you explain these from memory?
- [ ] What's the difference between tokenize, embed, layers, logits, sample?
- [ ] What's the difference between prefill and decode?
- [ ] What drives TTFT? What drives TPS?
- [ ] Why is inference more expensive than training in production?

### Connect Forward

Tomorrow: we crack open the GPU itself — SMs, Tensor Cores, HBM. Today's "layers spend GPU time" becomes tomorrow's "*here's exactly where in the chip that time goes*."

### Pre-read for tomorrow (Day 7 · Meet the GPU)

- **Resource:** Inference Engineering Pre-Lecture Reading — **Reader 5 (Computer architecture primer)** (~10 min). H100 1-page spec summary (facilitator-provided).
- **Reflection questions:**
  1. What does "80 GB HBM3" mean? (Memory technology + capacity.)
  2. What's an SM? What's a Tensor Core?
  3. Why is intra-GPU memory faster than GPU-to-GPU which is faster than node-to-node?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
