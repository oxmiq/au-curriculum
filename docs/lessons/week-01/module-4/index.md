# Day 4 · How Computers Run AI (GPU Primer)

> **Concept of the day:** CPU vs GPU. Matrix multiplication = parallelism. Training vs serving. The journey of a prompt.
> **Pre-reading:** 15-min video on what a GPU is (facilitator shares link).
> **Source:** [Week 1 Orientation Student Guide § Day 4](../../../../planning/source-material/Orientation/Orientation-Student-Guide.md).

---

## Why this matters

You don't need to know how a transistor works to be a good GPU engineer. You *do* need to know why a GPU exists, what makes it different from a CPU, and what kinds of work it's good at — because every design decision in Weeks 2–5 follows from those three facts.

## Readiness check

1. Name one reason GPUs are faster than CPUs for ML.
2. Roughly how many cores does an H100 have, vs a typical CPU?
3. What is matrix multiplication, in one sentence?
4. Name one structural difference between training and serving.
5. What's the first step that happens when you press Enter on a prompt?

## Core concept — Three facts to internalize

1. **A GPU has thousands of small cores; a CPU has a few big ones.** A modern CPU might have 8–96 powerful cores. An H100 GPU has 16,896 CUDA cores plus 528 Tensor Cores. CPUs are optimized for one big task fast; GPUs are optimized for many small tasks in parallel.
2. **Matrix multiplication is the workload neural networks demand, and it is embarrassingly parallel.** Multiplying a 4096×4096 matrix by a 4096×4096 matrix is ~68 billion multiply-adds — each one independent. A GPU can do them all at once (in batches). A CPU can't.
3. **Training and serving (inference) are different sports.** Training: rare, batch, throughput-only, can take weeks. Serving: continuous, per-user, latency-sensitive, must respond in milliseconds. Most of this program is about *serving*, which is the bigger and harder operational problem.

### Real numbers to remember

| Specification | NVIDIA H100 SXM5 |
|---|---|
| Tensor Cores | 528 |
| FP16 throughput | ~989 TFLOPs |
| HBM3 memory | 80 GB |
| Memory bandwidth | 3.35 TB/s |
| TDP | 700 W |
| Approx. cloud price | $2–4/hour per GPU |
| 8-GPU box price | ~$24/hour, ~$17K/month |

You'll see these numbers repeatedly in Week 2.

### The journey of a prompt (preview of Week 2 Day 6)

1. **Tokenize** — your text becomes a sequence of integers (token IDs).
2. **Embed** — each token ID becomes a vector (hundreds to thousands of floats).
3. **Layers** — the vectors pass through ~32–80 transformer layers. Each layer does attention + a feed-forward pass. This is where the GPU spends its time.
4. **Logits** — out comes a probability distribution over the entire vocabulary (~32K–200K tokens).
5. **Sample** — pick a token (greedy, top-p, etc.).
6. Loop steps 3–5 until you hit a stop condition. **Each loop = one output token.**

Everything in Weeks 2–5 is about making that loop faster and cheaper.

## Practice (90 min)

1. (15 min) On paper, draw the path of "Hello, world." from your keyboard to a response on screen. Label every box you can.
2. (25 min) Pair share: compare drawings. Which box does *neither* of you understand? Note it — that's a Week 2 question.
3. (20 min) Look up specs for one consumer GPU (e.g., RTX 4090) and one Tenstorrent chip (e.g., Wormhole n150). Write a 5-row comparison table.
4. (20 min) Discussion: why is a 4090 cheaper per FLOP than an H100, and why would anyone still buy H100s? (Bandwidth, memory capacity, NVLink, datacenter-grade reliability.)
5. (10 min) Write down one question about GPUs you want answered before Friday.

## Wrap-up

Collect the open GPU questions — those become Friday's open-lab agenda.

## Connect forward

Friday: consolidation. We make sure shell, git, and the GPU mental model all stuck — then take the [Week 1 quiz](knowledge-check.html). Monday we open the GPU and look inside.

---

## Pre-read for Friday (Day 5 · Consolidation)

- **Resource:** None. Review your notes from Days 1–4. Bring questions.
- **Reflection questions:**
  1. What concept from this week is least clear to you?
  2. What do you most want to clarify before Week 2 starts?
  3. Which of the three skills (shell / git / GPU mental model) do you feel weakest in?
