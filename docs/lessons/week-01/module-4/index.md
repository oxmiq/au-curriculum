# Day 4 · How Computers Run AI (GPU Primer)

> **Concept of the day:** CPU vs GPU. Matrix multiplication = parallelism. Training vs serving. The journey of a prompt.<br>
> **Pre-reading:** <a href="https://www.youtube.com/watch?v=h9Z4oGN89MU" target="_blank" rel="noopener">GPU Explained</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 - Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 4 · How Computers Run AI</span>
    {status:week-01/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: CPU vs GPU |
| Part 3 | Deep Dive: The Numbers |
| Part 4 | Deep Dive: Journey of a Prompt |
| Part 5 | Hands-On: GPU Comparison |
| Part 6 | Hands-On: Draw the Path |
| Part 7 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have watched the GPU video from your facilitator.

### Quick Self-Check

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m4-readiness" data-kind="readiness" data-draw="5" data-source="GPU video from facilitator">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "Why are GPUs faster than CPUs for machine learning?", "options": ["They have fewer, more powerful cores", "They have thousands of small cores that run the same operation in parallel", "They use less power", "They have more cache memory"], "answer": 1, "explain": "GPUs have thousands of small cores that can all run the same operation (like matrix multiplication) simultaneously on different data points."},
  {"stem": "Roughly how many CUDA cores does an NVIDIA H100 have?", "options": ["1,000", "16,896", "528", "80"], "answer": 1, "explain": "The H100 has 16,896 CUDA cores plus 528 Tensor Cores for AI-specific operations."},
  {"stem": "What is matrix multiplication in one sentence?", "options": ["A way to sort data", "Multiplying two grids of numbers together where each row is multiplied by each column", "A type of sorting algorithm", "A compression technique"], "answer": 1, "explain": "Matrix multiplication multiplies two grids of numbers together; each element in the result depends on one row times one column."},
  {"stem": "What does 'embarrassingly parallel' mean?", "options": ["The problem is embarrassing to solve", "The operations can all run independently at the same time", "The problem requires sequential processing", "The GPU is embarrassed"], "answer": 1, "explain": "Embarrassingly parallel means all the calculations are independent; no data needs to be shared between them, so they can all run simultaneously."},
  {"stem": "What is the main difference between training and serving (inference)?", "options": ["Training happens once; serving happens continuously for every user request", "They are the same thing", "Training is faster than serving", "Serving only happens on CPUs"], "answer": 0, "explain": "Training happens once (batch process), while serving (inference) must respond to user requests in real-time with low latency."},
  {"stem": "What is a Tensor Core?", "options": ["A type of CPU core", "A specialized GPU core for matrix operations", "A memory module", "A cooling unit"], "answer": 1, "explain": "Tensor Cores are specialized GPU cores designed specifically for the matrix multiplications at the heart of neural network computations."},
  {"stem": "Why do neural networks need parallel processing?", "options": ["They don't; they run sequentially", "Because they perform the same operation on thousands of data points at once", "Because GPUs are cheaper", "Because CPUs are too fast"], "answer": 1, "explain": "Neural networks apply the same operations (matrix multiplications) to thousands of neurons/weights simultaneously."},
  {"stem": "What is the primary operation in a neural network layer?", "options": ["Sorting", "Matrix multiplication", "Encryption", "Compression"], "answer": 1, "explain": "The core operation in transformer layers is matrix multiplication: multiplying input vectors by weight matrices."},
  {"stem": "What does HBM stand for in GPU specs?", "options": ["High Bandwidth Memory", "Hyper Basic Memory", "High Binary Mode", "Host Buffer Memory"], "answer": 0, "explain": "HBM (High Bandwidth Memory) is stacked memory designed for high throughput, critical for GPU performance."},
  {"stem": "Why is memory bandwidth important for GPUs?", "options": ["It isn't important", "Because GPUs need to feed thousands of cores with data constantly", "Because it reduces power consumption", "Because it increases core count"], "answer": 1, "explain": "GPUs have thousands of cores that all need data. If memory can't feed them fast enough, the cores sit idle."},
  {"stem": "What is the typical batch size difference between training and serving?", "options": ["Same batch size", "Training uses large batches; serving often uses single requests", "Serving uses larger batches", "Batch size doesn't matter"], "answer": 1, "explain": "Training can batch thousands of examples together. Serving typically processes one user request at a time for low latency."},
  {"stem": "What is the main objective difference between training and serving?", "options": ["Both prioritize latency", "Training prioritizes throughput; serving prioritizes latency", "Both prioritize throughput", "Neither matters"], "answer": 1, "explain": "Training optimizes for throughput (many samples per second). Serving optimizes for latency (milliseconds per request)."},
  {"stem": "How long can training take for large models?", "options": ["Minutes", "Hours to weeks", "Seconds", "It doesn't take time"], "answer": 1, "explain": "Training large models can take days or weeks on hundreds of GPUs."},
  {"stem": "What must serving do that training doesn't?", "options": ["Process in batches", "Respond in milliseconds", "Use all GPU memory", "Run continuously"], "answer": 1, "explain": "Serving must respond to user requests in milliseconds; latency is critical."},
  {"stem": "What is the journey of a prompt? (Select the correct first step)", "options": ["Goes directly to GPU", "Tokenization on CPU", "Immediate output", "Matrix multiplication first"], "answer": 1, "explain": "The first step is tokenization, converting text into token IDs (integers), typically on the CPU."},
  {"stem": "Where does the embedding step happen?", "options": ["CPU only", "GPU", "Network", "Storage"], "answer": 1, "explain": "Embedding converts token IDs into vectors (arrays of numbers), typically done on the GPU."},
  {"stem": "What happens in the transformer layers?", "options": ["Data is stored", "Vectors pass through attention and feed-forward operations", "Data is compressed", "Nothing happens"], "answer": 1, "explain": "Transformer layers process vectors through attention mechanisms and feed-forward networks; this is where the GPU spends most time."},
  {"stem": "What is sampling in the prompt journey?", "options": ["Reading from disk", "Picking the next token from probability distribution", "Sending to CPU", "Saving to memory"], "answer": 1, "explain": "Sampling picks the next token from the probability distribution over the vocabulary (32K-200K tokens)."},
  {"stem": "Why do we care about GPU specs like TFLOPs?", "options": ["We don't", "Because they indicate how fast the GPU can do matrix operations", "Because they affect power consumption", "Because they determine price"], "answer": 1, "explain": "TFLOPs (tera floating-point operations per second) measure how many calculations the GPU can do per second."},
  {"stem": "What is the key insight about H100 memory?", "options": ["80GB doesn't matter", "80GB memory and 3.35 TB/s bandwidth are as important as TFLOPs", "Memory doesn't affect performance", "Less memory is better"], "answer": 1, "explain": "Memory capacity and bandwidth often bottleneck performance more than raw compute (TFLOPs)."}
]
</script>
</div>

---

## Part 2 - Core Concepts - CPU vs GPU
### Reading - Three Facts to Internalize

You don't need to know how a transistor works to be a good GPU engineer. You *do* need to know why a GPU exists, what makes it different from a CPU, and what kinds of work it's good at: because every design decision in Weeks 2–5 follows from those three facts.

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
- A CPU cannot; it's designed for sequential tasks

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

## Part 3 - Deep Dive - The Numbers
### Reading - Real Numbers to Remember

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

## Part 4 - Deep Dive - Journey of a Prompt
### Reading - What Happens When You Send a Prompt

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

## Part 5 - Hands-On - GPU Comparison
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

## Part 6 - Hands-On - Draw the Path
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

## Part 7 - Wrap-up & Connection
### Self-Check

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Parts 2-6">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What is the key difference between CPU and GPU core design?", "options": ["They are the same", "CPU has few powerful cores; GPU has thousands of small cores", "GPU has fewer cores than CPU", "CPU cores are faster individually"], "answer": 1, "explain": "CPUs have 8-96 powerful cores for sequential tasks. GPUs have thousands of smaller cores for parallel operations."},
  {"stem": "How many CUDA cores does an H100 have?", "options": ["528", "16,896", "80", "3,000"], "answer": 1, "explain": "The H100 has 16,896 CUDA cores plus 528 Tensor Cores specialized for AI."},
  {"stem": "What is the H100's HBM3 memory capacity?", "options": ["16 GB", "80 GB", "32 GB", "256 GB"], "answer": 1, "explain": "The H100 SXM5 has 80 GB of HBM3 (High Bandwidth Memory)."},
  {"stem": "What is the H100's memory bandwidth?", "options": ["500 GB/s", "1 TB/s", "3.35 TB/s", "10 TB/s"], "answer": 2, "explain": "H100 has 3.35 TB/s memory bandwidth: critical for feeding the thousands of cores."},
  {"stem": "What is the approximate cloud price per hour for one H100?", "options": ["$0.50", "$2-4", "$10", "$50"], "answer": 1, "explain": "H100s cost approximately $2-4 per hour in cloud pricing."},
  {"stem": "What are the three key H100 specs to remember?", "options": ["Cores, price, color", "528 Tensor Cores, 80GB memory, 3.35 TB/s bandwidth", "Speed, size, weight", "Cores, price, power"], "answer": 1, "explain": "Memory (80GB) and bandwidth (3.35 TB/s) are as important as the core count for real-world performance."},
  {"stem": "What is the first step in the journey of a prompt?", "options": ["Matrix multiplication", "Tokenization", "Embedding", "Sampling"], "answer": 1, "explain": "The first step is tokenization: converting text into token IDs (integers) on the CPU."},
  {"stem": "Where does embedding happen?", "options": ["CPU", "GPU", "Network", "Disk"], "answer": 1, "explain": "Embedding converts token IDs into vectors (arrays of floats), typically on the GPU."},
  {"stem": "Where do transformer layers run?", "options": ["CPU only", "GPU", "Network", "RAM"], "answer": 1, "explain": "Transformer layers (attention + feed-forward) run on the GPU; this is where most GPU time is spent."},
  {"stem": "What is logits in the prompt journey?", "options": ["A type of GPU", "Probability distribution over vocabulary", "A memory type", "A network protocol"], "answer": 1, "explain": "Logits are the probability distribution over the vocabulary (32K-200K tokens) from which the next token is sampled."},
  {"stem": "What is sampling?", "options": ["Reading from disk", "Picking the next token from probability distribution", "Compressing data", "Sending to network"], "answer": 1, "explain": "Sampling selects the next token from the probability distribution (using greedy, top-p, etc.)."},
  {"stem": "Why is training different from serving?", "options": ["They are the same", "Training is batch processing for throughput; serving is real-time for latency", "Serving takes longer", "Training doesn't use GPUs"], "answer": 1, "explain": "Training optimizes for throughput (many samples/sec). Serving optimizes for latency (ms per request)."},
  {"stem": "What is the typical serving batch size?", "options": ["Thousands", "Often single request", "Millions", "Zero"], "answer": 1, "explain": "Serving typically processes one user request at a time for low latency."},
  {"stem": "Why is memory bandwidth important?", "options": ["It isn't", "Because thousands of cores need constant data flow", "Because it reduces heat", "Because it increases core count"], "answer": 1, "explain": "If memory can't feed the cores fast enough, they sit idle. Bandwidth bottlenecks matter more than compute."},
  {"stem": "What is FP16 throughput for H100?", "options": ["100 TFLOPs", "989 TFLOPs", "5,000 TFLOPs", "10 TFLOPs"], "answer": 1, "explain": "H100 has approximately 989 TFLOPs FP16 throughput."},
  {"stem": "What is the H100's TDP?", "options": ["100 W", "700 W", "1,000 W", "50 W"], "answer": 1, "explain": "The H100 has a TDP (Thermal Design Power) of 700W."},
  {"stem": "Why would someone buy an H100 over an RTX 4090?", "options": ["H100 is cheaper", "H100 has more memory, bandwidth, and Tensor Cores for datacenter workloads", "4090 is faster", "They are the same"], "answer": 1, "explain": "H100 has 80GB vs 24GB, better bandwidth, Tensor Cores, and is designed for 24/7 datacenter operation."},
  {"stem": "What is the approximate price of an 8-GPU H100 box?", "options": ["$1,000", "$24/hour, ~$17K/month", "$100", "$100K"], "answer": 1, "explain": "An 8-GPU H100 box costs approximately $24/hour or ~$17K/month."},
  {"stem": "What does 'embarrassingly parallel' refer to in matrix multiplication?", "options": ["The problem is embarrassing", "Each element calculation is independent: no data sharing needed", "The GPU is embarrassed", "The calculation is sequential"], "answer": 1, "explain": "Matrix multiplication is embarrassingly parallel because each output element can be calculated independently."},
  {"stem": "What is the key insight about GPU bottlenecks?", "options": ["Compute is always the bottleneck", "Memory bottlenecks matter more than compute", "Power is the bottleneck", "There are no bottlenecks"], "answer": 1, "explain": "Memory capacity and bandwidth often bottleneck performance more than raw compute (TFLOPs)."}
]
</script>
</div>

### Collect Questions

Write down one question about GPUs you want answered before Friday.

### Connect Forward

Friday: consolidation. We make sure shell, git, and the GPU mental model all stuck; then take the [Week 1 quiz](knowledge-check.md). Monday we open the GPU and look inside.

---

## Pre-read for Friday (Day 5 · Consolidation)

- **Resource:** None. Review your notes from Days 1–4. Bring questions.
- **Reflection questions:**
  1. What concept from this week is least clear to you?
  2. What do you most want to clarify before Week 2 starts?
  3. Which of the three skills (shell / git / GPU mental model) do you feel weakest in?

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
