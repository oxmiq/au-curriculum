# Day 7 · Meet the GPU

> **Concept of the day:** GPU anatomy. SMs, Tensor Cores, CUDA Cores, HBM, L2 cache. Analogy: SM = factory floor, Tensor Core = specialized machine, HBM = warehouse.<br>
> **Pre-reading:** <a href="https://resources.nvidia.com/en-us-hopper-architecture/nvidia-tensor-core-gpu-datasheet" target="_blank" rel="noopener">NVIDIA H100 GPU Datasheet</a> (focus on SMs, memory, bandwidth, FLOPS).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 - The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 7 · Meet the GPU</span>
    {status:week-02/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: GPU Anatomy |
| Part 3 | The Mental Model |
| Part 4 | GPU Classes Comparison |
| Part 5 | Hands-On: Calculate Bandwidth |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: Pre-Lecture Reading **Reader 5 - Computer architecture primer** + H100 1-page spec.

### Quick Self-Check

Answer these questions from memory:

1. What does "80 GB HBM3" mean? (Memory technology + capacity)
2. What's an SM? What's a Tensor Core?
3. Why is intra-GPU memory faster than GPU-to-GPU?

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m2-readiness" data-kind="readiness" data-draw="5" data-source="NVIDIA H100 GPU Datasheet">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What does '80 GB HBM3' mean in the context of the H100 GPU?",
    "options": [
      "80 gigabytes of DDR5 memory",
      "80 gigabytes of High Bandwidth Memory, version 3",
      "80 gigabytes of shared system memory",
      "80 gigabytes of NVMe storage"
    ],
    "answer": 1,
    "explain": "HBM3 is High Bandwidth Memory version 3. The H100 SXM5 variant has 80 GB of HBM3, providing massive memory bandwidth for GPU workloads. This is distinct from traditional DDR/GDDR memory."
  },
  {
    "stem": "What is an SM (Streaming Multiprocessor) in GPU architecture?",
    "options": [
      "A single compute unit that processes one instruction at a time",
      "A cluster of CUDA cores that executes a warp together",
      "The memory controller that manages HBM",
      "The power management unit"
    ],
    "answer": 1,
    "explain": "An SM is a streaming multiprocessor: a cluster of CUDA cores that executes threads in warps (32 threads at a time). Think of an SM as a 'factory floor' where the actual compute happens."
  },
  {
    "stem": "What is a Tensor Core and how does it differ from a CUDA Core?",
    "options": [
      "Tensor Cores are for text processing; CUDA Cores are for graphics",
      "Tensor Cores are specialized for matrix multiplication (the core operation in neural networks); CUDA Cores are general-purpose ALUs",
      "Tensor Cores run at higher clock speeds than CUDA Cores",
      "There is no difference; they are the same thing"
    ],
    "answer": 1,
    "explain": "Tensor Cores are specialized matrix-multiply-accumulate units. A CUDA Core is a general-purpose ALU. Tensor Cores can do a 4x4 matrix multiply in one cycle that would take many CUDA Cores; they're the key to H100's AI performance."
  },
  {
    "stem": "Why is HBM (High Bandwidth Memory) important for GPUs?",
    "options": [
      "It is cheaper than DDR memory",
      "It provides massively higher bandwidth than traditional memory, critical for feeding the compute units",
      "It stores more data than DDR",
      "It uses less power than DDR"
    ],
    "answer": 1,
    "explain": "HBM provides terabytes/second of memory bandwidth (H100: ~3.35 TB/s). Traditional DDR is limited to tens of GB/s. The GPU's compute units (Tensor Cores) are starved without this bandwidth; it's the memory wall problem."
  },
  {
    "stem": "What is the approximate memory bandwidth of an H100 SXM5?",
    "options": [
      "~100 GB/s",
      "~500 GB/s",
      "~1 TB/s",
      "~3.35 TB/s"
    ],
    "answer": 3,
    "explain": "The H100 SXM5 has ~3.35 TB/s of memory bandwidth. This is enabled by HBM3 and the wide memory interface. This bandwidth is what makes H100 suitable for large model inference."
  },
  {
    "stem": "What does intra-GPU memory refer to, and why is it faster than inter-GPU (GPU-to-GPU) communication?",
    "options": [
      "CPU memory - it is faster than GPU memory",
      "HBM within a single GPU - it doesn't need to cross the PCIe bus",
      "System RAM - it is directly connected",
      "NVMe storage - it is faster than networking"
    ],
    "answer": 1,
    "explain": "Intra-GPU memory (HBM) is within a single GPU and doesn't need to cross PCIe or networking. Inter-GPU communication goes over PCIe or NVLink: slower due to physical distance and protocol overhead."
  },
  {
    "stem": "What are TFLOPS and how are they measured for H100?",
    "options": [
      "Trillions of Floating-point Operations Per Second - measured using INT8 for H100's Tensor Cores",
      "Trillions of Floating-point Operations Per Second - measured using FP16 or FP32 for H100's Tensor/CUDA Cores",
      "Terabytes of Free Memory Per Second",
      "Time For Large-scale Object Processing and Retrieval System"
    ],
    "answer": 1,
    "explain": "TFLOPS measures compute throughput. H100 delivers ~1,000 TFLOPS (1 PetaFLOPS) with FP16 Tensor Cores. Different precisions give different numbers; the key is matching precision to your workload."
  },
  {
    "stem": "What is the L2 cache on a GPU used for?",
    "options": [
      "Storing the final output before sending to the user",
      "Caching frequently accessed model weights and KV caches to reduce memory bandwidth pressure",
      "Running the operating system",
      "Managing power consumption"
    ],
    "answer": 1,
    "explain": "L2 cache sits between the compute units and HBM. It caches model weights and KV cache entries to reduce the number of expensive HBM accesses. More L2 = better cache hit rate = less memory bandwidth bottleneck."
  }
]
</script>
</div>

---

## Part 2 - Core Concepts: GPU Anatomy
### Reading - Why GPU Anatomy Matters

Every optimization in Weeks 3–5, KV cache layout, FlashAttention, tensor parallelism, batching, is a response to the *physical* GPU. You can't reason about the optimization without the hardware.

### The H100 SXM5 In One Table

| Component | What it is | H100 numbers | Speed |
|---|---|---|---|
| **SM (Streaming Multiprocessor)** | A "factory floor" - the unit of work scheduling | 132 SMs | - |
| **CUDA Core** | General-purpose ALU within an SM | 16,896 total | - |
| **Tensor Core** | Specialized matrix-multiply unit (the workhorse for AI) | 528 total | - |
| **Register file** | Per-thread scratch (sub-ns) | KBs per SM | ~0 ns |
| **L1 / Shared memory** | Per-SM SRAM (~1 ns) | ~256 KB per SM | ~1 ns |
| **L2 cache** | Chip-wide SRAM (~5 ns) | 50 MB | ~5 ns |
| **HBM3** | Off-chip "warehouse" DRAM (~80 ns, but very wide) | 80 GB @ 3.35 TB/s | ~80 ns |
| **NVLink** | GPU↔GPU interconnect | 900 GB/s | - |
| **PCIe** | CPU↔GPU | ~64 GB/s | - |

### Key Numbers to Memorize

- **80 GB HBM3** - the memory capacity
- **3.35 TB/s** - the memory bandwidth
- **132 SMs** - the compute units
- **528 Tensor Cores** - the specialized AI accelerators

---

## Part 3 - The Mental Model
### Reading - Factory Floor Analogy

> **SM = factory floor. Tensor Core = specialized machine on the floor. HBM = warehouse across the road. L2 = on-site storage. Registers = workbench.**

### How This Analogy Works

| GPU Component | Factory Analogy | Why it Matters |
|---------------|-----------------|----------------|
| SM (Streaming Multiprocessor) | Factory floor | Where work is scheduled |
| Tensor Core | Specialized machine | Does the actual matrix multiplication |
| Register file | Workbench | Ultra-fast, per-thread scratch space |
| L1 / Shared memory | On-site storage | Fast access for frequently-used data |
| L2 cache | Warehouse storage | Larger but slower than L1 |
| HBM (High Bandwidth Memory) | Warehouse across the road | Large capacity but slow to access |

### You Produce More By:

1. **(a)** Putting more machines on each floor (more Tensor Cores per SM)
2. **(b)** Keeping the workbench full (locality, kernel fusion)
3. **(c)** **Not running back to the warehouse on every move** (bandwidth-bound = "you're stuck walking to the warehouse")

---

## Part 4 - GPU Classes Comparison
### Reading - Three GPU Classes to Remember

| Class | Example | Memory | Bandwidth | Where You See It |
|---|---|---|---|---|
| Datacenter flagship | H100 SXM5 | 80 GB HBM3 | 3.35 TB/s | Large model serving |
| Consumer / workstation | RTX 4090 | 24 GB GDDR6X | 1 TB/s | Prototyping, ≤13B serving |
| Next-gen / accelerator | Tenstorrent Wormhole n150 | 12 GB GDDR6 | ~0.27 TB/s | Cost-effective MoE, ARM hosts |

### Key Comparison Points

- **H100:** Massive memory (80 GB), massive bandwidth (3.35 TB/s), massive price (~$30K)
- **RTX 4090:** Good compute, limited memory (24 GB), good bandwidth (1 TB/s), consumer price (~$1.6K)
- **Wormhole n150:** Lower cost, lower bandwidth, good for MoE models

### Compute Throughput

- **H100 SXM5:** ~989 TFLOPs FP16 (dense, with Tensor Cores)
- **RTX 4090:** ~165 TFLOPs FP16 - but only **24 GB GDDR6X** and only **1 TB/s** bandwidth

**Key insight:** TFLOPs alone don't tell the whole story. Memory bandwidth often matters more.

---

## Part 5 - Hands-On: Calculate Bandwidth
### Exercise 1: Time to Load Weights

**Calculate:** How long would it take to move all 80 GB of H100 weights from HBM into the chip *once*?

**Formula:** Time = Size / Bandwidth

**Answer:**
- 80 GB ÷ 3.35 TB/s = 80 GB ÷ 3,350 GB/s = ~0.024 seconds = **24 ms**

**Now calculate for RTX 4090:**
- 24 GB ÷ 1 TB/s = 24 GB ÷ 1,000 GB/s = **24 ms**

**Why do these numbers matter for decode latency?**

Each decode step needs to read the KV cache from HBM. If each step takes ~10 ms and you need 500 tokens, that's 5 seconds just for memory reads!

### Exercise 2: Match GPU Specs

Given this stripped table, identify which row is which GPU:

| Memory | Bandwidth | TFLOPs | GPU |
|--------|-----------|--------|-----|
| 80 GB HBM3 | 3.35 TB/s | ~989 | ? |
| 24 GB GDDR6X | 1 TB/s | ~165 | ? |
| 12 GB GDDR6 | 0.27 TB/s | ~100 | ? |

**Answers:** Row 1 = H100, Row 2 = RTX 4090, Row 3 = Wormhole n150

---

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-02-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 7 · Meet the GPU">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is a Streaming Multiprocessor (SM) in a GPU?",
    "options": [
      "A specialized unit that performs matrix multiplication",
      "A cluster of CUDA cores that executes threads in warps - the basic unit of work scheduling",
      "The memory controller that manages HBM reads and writes",
      "A power management unit that regulates clock speed"
    ],
    "answer": 1,
    "explain": "An SM (Streaming Multiprocessor) is like a 'factory floor': a cluster of CUDA cores that schedules and executes threads in warps of 32. The H100 has 132 SMs. Part 2 describes SMs as the fundamental compute units."
  },
  {
    "stem": "How does a Tensor Core differ from a CUDA Core?",
    "options": [
      "Tensor Cores are slower but more power-efficient than CUDA Cores",
      "Tensor Cores are specialized matrix-multiply-accumulate units; CUDA Cores are general-purpose ALUs",
      "Tensor Cores handle text operations; CUDA Cores handle graphics rendering",
      "There is no difference; they are the same hardware renamed"
    ],
    "answer": 1,
    "explain": "Tensor Cores perform a matrix multiply-accumulate in one operation that would take many CUDA Core cycles. They are the key to H100's AI performance. CUDA Cores are general-purpose but less efficient for the dense matrix math at the heart of transformers."
  },
  {
    "stem": "What are the two most important H100 SXM5 specifications for LLM inference?",
    "options": [
      "132 SMs and 528 Tensor Cores",
      "80 GB HBM3 and 3.35 TB/s memory bandwidth",
      "989 TFLOPs and 50 MB L2 cache",
      "NVLink 900 GB/s and PCIe 64 GB/s"
    ],
    "answer": 1,
    "explain": "Part 2 states: 'Key Numbers to Memorize: 80 GB HBM3 - the memory capacity; 3.35 TB/s - the memory bandwidth.' For LLM inference, memory capacity limits how large a model you can serve, and memory bandwidth determines how fast you can read weights during decode."
  },
  {
    "stem": "In the factory floor analogy, what does HBM represent?",
    "options": [
      "The workbench - ultra-fast per-thread scratch space",
      "The specialized machine that does the actual matrix multiplication",
      "The warehouse across the road - large capacity but slow to access",
      "The on-site storage - fast access for frequently used data"
    ],
    "answer": 2,
    "explain": "Part 3's factory analogy maps: SM = factory floor, Tensor Core = specialized machine, Registers = workbench, L1 = on-site storage, L2 = warehouse storage, HBM = warehouse across the road. HBM is large (80 GB) but has higher access latency (~80 ns) compared to on-chip memory."
  },
  {
    "stem": "What is the memory hierarchy from fastest to slowest in a GPU?",
    "options": [
      "HBM → L2 cache → L1/Shared memory → Registers",
      "Registers → L1/Shared memory → L2 cache → HBM",
      "L1 → Registers → L2 → HBM",
      "L2 cache → HBM → Registers → L1/Shared memory"
    ],
    "answer": 1,
    "explain": "Part 2 shows the latency order from fast to slow: Registers (~0 ns) → L1/Shared memory (~1 ns) → L2 cache (~5 ns) → HBM (~80 ns). Faster memory is smaller and closer to the compute units."
  },
  {
    "stem": "Why does the RTX 4090 have lower memory bandwidth than the H100, and why does this matter for decode?",
    "options": [
      "The 4090 has older memory technology; it matters because faster bandwidth means more Tensor Cores can run",
      "The 4090 has ~1 TB/s vs H100's 3.35 TB/s; for decode (memory-bound), bandwidth limits how fast KV cache can be read: directly limiting tokens-per-second",
      "The 4090 has lower clock speed; it matters because higher clocks mean faster sampling",
      "The 4090 uses DDR5 instead of HBM; this matters only for training, not inference"
    ],
    "answer": 1,
    "explain": "Part 4: 4090 = 1 TB/s vs H100 = 3.35 TB/s. Decode is memory-bound (Part 3 of module-1), meaning the bottleneck is reading KV cache from HBM. Lower bandwidth = slower token generation. This is why 'TFLOPs alone don't tell the whole story.'"
  },
  {
    "stem": "What is NVLink used for in a multi-GPU system?",
    "options": [
      "Connecting the GPU to the CPU at high bandwidth",
      "High-bandwidth GPU-to-GPU interconnect within a single server (~900 GB/s)",
      "Connecting the GPU to network storage over fiber",
      "Providing power to multiple GPUs from a shared supply"
    ],
    "answer": 1,
    "explain": "Part 2 shows NVLink provides 900 GB/s GPU↔GPU bandwidth, compared to PCIe at ~64 GB/s. NVLink enables tensor parallelism to work efficiently across GPUs on the same server. Without it, inter-GPU communication would bottleneck multi-GPU inference."
  },
  {
    "stem": "How many SMs and Tensor Cores does the H100 SXM5 have, according to Part 2?",
    "options": [
      "16,896 SMs and 132 Tensor Cores",
      "50 SMs and 989 Tensor Cores",
      "80 SMs and 3,350 Tensor Cores",
      "132 SMs and 528 Tensor Cores"
    ],
    "answer": 3,
    "explain": "Part 2's 'Key Numbers to Memorize': 132 SMs (the compute units) and 528 Tensor Cores (the specialized AI accelerators). The 16,896 figure is the CUDA Core count, and 989 TFLOPs is the FP16 compute throughput."
  },
  {
    "stem": "In the Part 5 exercise, roughly how long does it take to move all 80 GB of H100 weights from HBM into the chip once (at 3.35 TB/s)?",
    "options": [
      "~24 ms",
      "~2.4 ms",
      "~240 ms",
      "~24 seconds"
    ],
    "answer": 0,
    "explain": "Part 5 computes Time = Size / Bandwidth = 80 GB ÷ 3,350 GB/s ≈ 0.024 s = ~24 ms. Interestingly the RTX 4090 works out to the same 24 ms (24 GB ÷ 1,000 GB/s), because its smaller memory is paired with proportionally smaller bandwidth."
  }
]
</script>
</div>

### Connect Forward

Tomorrow: why those bandwidth numbers, not the TFLOPs, usually decide how fast your model goes.

### Pre-read for tomorrow (Day 8 · Memory Is the Bottleneck)

- **Resource:** "Why bandwidth matters more than compute" - <a href="https://horace.io/brrr_intro.html#bandwidth" target="_blank" rel="noopener">Horace He - Making Deep Learning Go Brrr (Bandwidth section)</a>
- **Reflection questions:**
  1. Which is faster: L2 cache or HBM? By roughly how much?
  2. What is **temporal locality**? **spatial locality**?
  3. Why does **kernel fusion** make things faster, given that the math is the same?

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
