# Day 6 · What Happens When You Send a Prompt

> **Concept of the day:** the inference pipeline. Tokenize → embed → layers → logits → sample. One forward pass = one token out.
> **Pre-reading:** Inference Engineering Pre-Lecture Reading — **Reader 1 (AI in production)** (~15 min).
> **Source:** [Pre-Lecture Reading § Reader 1](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Pre_Lecture_Reading.md) · [Study Guide Ch 0 + §A.0](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md).

---

## Why this matters

Phase 1 (Weeks 2–5) is a four-week zoom-in on the **inference loop**. Before we open up the GPU (Day 7), the cache (Week 3), or the cluster (Week 4), you need a working mental model of what *actually happens* when a user hits send.

## Readiness check

1. What's more expensive long-term: training or inference? Why?
2. Roughly what's the difference between a closed model and an open model? Name one of each.
3. What is a **token**?
4. What does "one forward pass" mean?
5. In the worked example from Reader 1 ("What is the capital of France?"), what's happening between 45 ms and 200 ms? What about 200–300 ms?

## Core concept — the inference pipeline

```
text  →  [tokenize]  →  token IDs  →  [embed]  →  vectors  →
        [transformer layers × N]  →  hidden states  →
        [LM head]  →  logits  →  [sample]  →  next token
```

Then **loop** the layers→logits→sample steps. Each loop = one output token.

### Five stages, in one sentence each

1. **Tokenize** — text becomes integers (typically BPE-encoded, vocabulary 32K–200K).
2. **Embed** — each token ID becomes a dense vector (the model's hidden size, e.g. 4096).
3. **Layers** — the vectors pass through N transformer blocks (attention + MLP), each refining the representation. *This is where the GPU spends its time.*
4. **Logits** — the final hidden state is projected to a probability distribution over the entire vocabulary.
5. **Sample** — pick one token (greedy, top-k, top-p, temperature). That's your next output.

### Prefill vs decode (preview of Day 11)

- **Prefill** = run all your *input* tokens through the layers in one shot. Parallel, compute-bound. Drives **TTFT** (time to first token).
- **Decode** = generate output tokens one at a time. Sequential, memory-bound. Drives **TPS** (tokens per second).

### Why "inference > training" in production cost

Training is rare and expensive but happens once. Inference happens **billions of times a day** on every user request. Almost all GPU-hours a deployed AI company pays for go to inference — which is why this discipline exists.

## Practice (90 min)

1. (20 min) Trace a 5-word prompt through the pipeline on paper. Annotate each stage with: input shape, output shape, what changed.
2. (25 min) Worked numerical example: 1000 input tokens, 500 output tokens, model with 32 layers, hidden size 4096. Roughly how many forward passes total? Prefill = how many? Decode = how many?
3. (20 min) Pair share: each partner explains one of {prefill, decode, sample}. Other partner asks "why does that matter?" until you hit a "because the GPU…" answer.
4. (15 min) Read Reader 1's "worked example" timeline. Annotate where on the timeline TTFT lives and where end-to-end latency lives.
5. (10 min) Write down one question for Week 2 office hours.

## Wrap-up

Each pair states one sentence: *"The most important fact from today is…"* — the cohort cheat-sheet starts here.

## Connect forward

Tomorrow: we crack open the GPU itself — SMs, Tensor Cores, HBM. Today's "layers spend GPU time" becomes tomorrow's "*here's exactly where in the chip that time goes*."

---

## Pre-read for tomorrow (Day 7 · Meet the GPU)

- **Resource:** Inference Engineering Pre-Lecture Reading — **Reader 5 (Computer architecture primer)** (~10 min). H100 1-page spec summary (facilitator-provided).
- **Reflection questions:**
  1. What does "80 GB HBM3" mean? (Memory technology + capacity.)
  2. What's an SM? What's a Tensor Core?
  3. Why is intra-GPU memory faster than GPU-to-GPU which is faster than node-to-node?
