# Day 4 · How Computers Run AI (GPU Primer)

> **Concept of the day:** CPU vs GPU. Matrix multiplication = parallelism. Training vs serving. The journey of a prompt.<br>
> **Pre-reading:** 15-min video on what a GPU is (facilitator shares link).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 — Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 4 · How Computers Run AI</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-01/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts: CPU vs GPU | 20 min |
| Part 3 | Deep Dive: The Numbers | 15 min |
| Part 4 | Deep Dive: Journey of a Prompt | 20 min |
| Part 5 | Hands-On: GPU Comparison | 25 min |
| Part 6 | Hands-On: Draw the Path | 20 min |
| Part 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have watched the GPU video (15 min) from your facilitator.

### Quick Self-Check

Answer these questions from memory:
1. Name one reason GPUs are faster than CPUs for ML.
2. Roughly how many cores does an H100 have?
3. What is matrix multiplication, in one sentence?

---

## Part 2 — Core Concepts — CPU vs GPU · 20 min
### Reading — Three Facts to Internalize

You don't need to know how a transistor works to be a good GPU engineer. You *do* need to know why a GPU exists, what makes it different from a CPU, and what kinds of work it's good at — because every design decision in Weeks 2–5 follows from those three facts.

### Fact 1: Thousands of Small Cores vs Few Big Cores

| Component | Typical CPU | NVIDIA H100 GPU |
|----------|-------------|-----------------|
| Cores | 8–96 | 16,896 CUDA cores + 528 Tensor Cores |
| Design | Few powerful cores | Many small cores |
| Optimization | One big task fast | Many small tasks in parallel |

**Why it matters:** Neural networks do the same operation (matrix multiplication) on thousands of data points simultaneously. GPUs excel at this.

### Fact 2: Matrix Multiplication is Embarrassingly Parallel

- Multiplying a 4096×4096 matrix by a 4096×4096 matrix = ~68 billion multiply-adds
- Each operation is independent
- A GPU can do them all at once (in batches)
- A CPU cannot — it's designed for sequential tasks

### Fact 3: Training vs Serving Are Different Sports

| Aspect | Training | Serving (Inference) |
|--------|----------|----------------------|
| Frequency | Rare (once) | Continuous (always) |
| Batch size | Large batches | Often single request |
| Objective | Throughput | Latency |
| Duration | Can take weeks | Must respond in ms |
| Memory | Can pre-allocate | Variable |

Most of this program is about *serving*, which is the bigger and harder operational problem.

---

## Part 3 — Deep Dive — The Numbers · 15 min
### Reading — Real Numbers to Remember

You'll see these numbers repeatedly in Week 2. Memorize what you can:

| Specification | NVIDIA H100 SXM5 |
|---|---|
| Tensor Cores | 528 |
| FP16 throughput | ~989 TFLOPs |
| HBM3 memory | 80 GB |
| Memory bandwidth | 3.35 TB/s |
| TDP | 700 W |
| Approx. cloud price | $2–4/hour per GPU |
| 8-GPU box price | ~$24/hour, ~$17K/month |

**Key insight:** The 80GB memory and 3.35 TB/s bandwidth are just as important as the TFLOPs. Memory bottlenecks matter more than compute.

---

## Part 4 — Deep Dive — Journey of a Prompt · 20 min
### Reading — What Happens When You Send a Prompt

This previews Week 2 (Day 6). Understanding this path is crucial:

```
You type "Explain quantum tunneling in one sentence" and press Enter.
```

Here's what happens:

| Step | What Happens | Where it Runs |
|------|--------------|---------------|
| 1. **Tokenize** | Your text becomes integers (token IDs) | CPU |
| 2. **Embed** | Each token ID → vector (hundreds to thousands of floats) | GPU |
| 3. **Layers** | Vectors pass through ~32–80 transformer layers. Each does attention + feed-forward | GPU (this is where GPU spends time) |
| 4. **Logits** | Probability distribution over vocabulary (~32K–200K tokens) | GPU |
| 5. **Sample** | Pick a token (greedy, top-p, etc.) | CPU/GPU |
| 6. **Loop** | Repeat steps 3–5 until stop condition | GPU |

**Each loop = one output token.**

Everything in Weeks 2–5 is about making that loop faster and cheaper.

---

## Part 5 — Hands-On — GPU Comparison · 25 min
### Exercise: Compare GPUs

Look up specs for these GPUs and create a comparison table:

1. **Consumer GPU:** NVIDIA RTX 4090
2. **Datacenter GPU:** NVIDIA H100
3. **Alternative:** Tenstorrent Wormhole n150

**Use these resources:**
- NVIDIA.com (specsheets)
- Tenstorrent.com
- TechPowerUp (for consumer GPUs)

**Create a table with:**
| GPU | Memory | Bandwidth | TFLOPs (FP16) | Price (approx) |

**Then answer:**
- Why is a 4090 cheaper per FLOP than an H100?
- Why would anyone still buy H100s?

---

## Part 6 — Hands-On — Draw the Path · 20 min
### Exercise: Visualize the Prompt Journey

On paper, draw the path of "Hello, world." from your keyboard to a response on screen.

1. **Start:** Keyboard input
2. **Step 1:** Tokenization
3. **Step 2:** Embedding
4. **Step 3-N:** Transformer layers (show 2-3 for simplicity)
5. **Step N+1:** Sampling
6. **Step N+2:** Output to screen

**Label each box:**
- Where does the GPU work?
- Where does the CPU work?
- What data moves between components?

### Self-Reflection

Which box do you understand least? That's a question for Week 2.

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you explain these from memory?
- [ ] Why are GPUs faster than CPUs for neural networks?
- [ ] What is "embarrassingly parallel" about matrix multiplication?
- [ ] What's the difference between training and serving?
- [ ] What are the three numbers you should remember about H100?

### Collect Questions

Write down one question about GPUs you want answered before Friday.

### Connect Forward

Friday: consolidation. We make sure shell, git, and the GPU mental model all stuck — then take the [Week 1 quiz](knowledge-check.html). Monday we open the GPU and look inside.

---

## Pre-read for Friday (Day 5 · Consolidation)

- **Resource:** None. Review your notes from Days 1–4. Bring questions.
- **Reflection questions:**
  1. What concept from this week is least clear to you?
  2. What do you most want to clarify before Week 2 starts?
  3. Which of the three skills (shell / git / GPU mental model) do you feel weakest in?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
