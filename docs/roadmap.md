# Roadmap

The full 50-day path through the curriculum. Each box is a session — click to open the lesson. Colour marks the phase. Solid arrows are the day-to-day sequence; dotted arrows are cross-phase prereqs (a later session that builds on an earlier one outside the immediate week).

If you want the narrative version with rationale, see [Curriculum](curriculum.md) and [Why this curriculum](rationale.md). For the interactive explorable graph, see [Interactive Graph](kb/interactive-graph.html).

```mermaid
flowchart TD
  subgraph W01["Week 01 · Orientation & Foundations"]
    direction TB
    W01M1["Day 01 · Welcome & Context"]
    W01M2["Day 02 · Shell & Linux"]
    W01M1 --> W01M2
    W01M3["Day 03 · Git Workflow"]
    W01M2 --> W01M3
    W01M4["Day 04 · How Computers Run AI"]
    W01M3 --> W01M4
    W01M5["Day 05 · Consolidation"]
    W01M4 --> W01M5
  end
  subgraph W02["Week 02 · The GPU & Memory"]
    direction TB
    W02M1["Day 06 · What Happens When You Send a Prompt"]
    W02M2["Day 07 · Meet the GPU"]
    W02M1 --> W02M2
    W02M3["Day 08 · Memory Is the Bottleneck"]
    W02M2 --> W02M3
    W02M4["Day 09 · Compute-Bound vs Memory-Bound"]
    W02M3 --> W02M4
    W02M5["Day 10 · Consolidation"]
    W02M4 --> W02M5
  end
  subgraph W03["Week 03 · Attention & KV Cache"]
    direction TB
    W03M1["Day 11 · Prefill vs Decode"]
    W03M2["Day 12 · KV Cache"]
    W03M1 --> W03M2
    W03M3["Day 13 · FlashAttention"]
    W03M2 --> W03M3
    W03M4["Day 14 · Quantization"]
    W03M3 --> W03M4
    W03M5["Day 15 · Consolidation"]
    W03M4 --> W03M5
  end
  subgraph W04["Week 04 · Scaling & Stacks"]
    direction TB
    W04M1["Day 16 · Multi-GPU Parallelism"]
    W04M2["Day 17 · Pipeline Parallelism + MoE"]
    W04M1 --> W04M2
    W04M3["Day 18 · Speculative Decoding"]
    W04M2 --> W04M3
    W04M4["Day 19 · vLLM Introduction"]
    W04M3 --> W04M4
    W04M5["Day 20 · Consolidation"]
    W04M4 --> W04M5
  end
  subgraph W05["Week 05 · Metrics & Production"]
    direction TB
    W05M1["Day 21 · Latency vs Throughput"]
    W05M2["Day 22 · Production Deployment"]
    W05M1 --> W05M2
    W05M3["Day 23 · LLM Evaluation"]
    W05M2 --> W05M3
    W05M4["Day 24 · Inference Economics"]
    W05M3 --> W05M4
    W05M5["Day 25 · Consolidation + Phase 1 Problem Set"]
    W05M4 --> W05M5
  end
  subgraph W06["Week 06 · Prompt Engineering"]
    direction TB
    W06M1["Day 26 · Prompt Structure & Clarity"]
    W06M2["Day 27 · Roles, Data Separation & Output Formatting"]
    W06M1 --> W06M2
    W06M3["Day 28 · Chain-of-Thought & Few-Shot Prompting"]
    W06M2 --> W06M3
    W06M4["Day 29 · Avoiding Hallucinations & Complex Prompts"]
    W06M3 --> W06M4
    W06M5["Day 30 · Consolidation: Chaining, Tool Use & Evals"]
    W06M4 --> W06M5
  end
  subgraph W07["Week 07 · AI Agents"]
    direction TB
    W07M1["Day 31 · The Agent Loop"]
    W07M2["Day 32 · Tools & MCP"]
    W07M1 --> W07M2
    W07M3["Day 33 · Governance & Security"]
    W07M2 --> W07M3
    W07M4["Day 34 · Orchestration & Multi-Agent"]
    W07M3 --> W07M4
    W07M5["Day 35 · Consolidation: Agent Case Studies + Design"]
    W07M4 --> W07M5
  end
  subgraph W08["Week 08 · Capsule: Foundations & Operations"]
    direction TB
    W08M1["Day 36 · Capsule Architecture & Installation"]
    W08M2["Day 37 · Environments & Fleet Discovery"]
    W08M1 --> W08M2
    W08M3["Day 38 · Connecting to Machines"]
    W08M2 --> W08M3
    W08M4["Day 39 · Files, Storage & Streaming"]
    W08M3 --> W08M4
    W08M5["Day 40 · Consolidation: Reliability & Diagnostics"]
    W08M4 --> W08M5
  end
  subgraph W09["Week 09 · Capsule: Benchmarking & Evaluation"]
    direction TB
    W09M1["Day 41 · Your First Benchmark"]
    W09M2["Day 42 · Varying Parameters"]
    W09M1 --> W09M2
    W09M3["Day 43 · Interactive Evaluation"]
    W09M2 --> W09M3
    W09M4["Day 44 · Scheduling & MCP"]
    W09M3 --> W09M4
    W09M5["Day 45 · Consolidation: End-to-End Eval Sprint"]
    W09M4 --> W09M5
  end
  subgraph W10["Week 10 · Capstone Project"]
    direction TB
    W10M1["Day 46 · Kickoff & Planning"]
    W10M2["Day 47 · Execute"]
    W10M1 --> W10M2
    W10M3["Day 48 · Analyze & Recommend"]
    W10M2 --> W10M3
    W10M4["Day 49 · Present"]
    W10M3 --> W10M4
    W10M5["Day 50 · Close"]
    W10M4 --> W10M5
  end
  W01M5 --> W02M1
  W02M5 --> W03M1
  W03M5 --> W04M1
  W04M5 --> W05M1
  W05M5 --> W06M1
  W06M5 --> W07M1
  W07M5 --> W08M1
  W08M5 --> W09M1
  W09M5 --> W10M1
  %% cross-phase shortcuts
  W01M4 -.-> W02M1
  W02M4 -.-> W03M1
  W02M3 -.-> W03M3
  W02M3 -.-> W03M4
  W02M2 -.-> W04M1
  W03M1 -.-> W04M3
  W03M2 -.-> W04M4
  W05M1 -.-> W05M4
  W08M3 -.-> W09M1
  W05M1 -.-> W09M1
  W09M1 -.-> W09M3
  W05M3 -.-> W09M3
  W09M1 -.-> W10M1
  W05M3 -.-> W10M1
  W09M3 -.-> W10M1

  classDef orientation fill:#1f2937,stroke:#7c8aa0,color:#e7e9ee;
  classDef inference fill:#0e2a32,stroke:#22d3ee,color:#e7f7fb;
  classDef prompting fill:#2a1e3d,stroke:#a78bfa,color:#efeaff;
  classDef agents fill:#3b2d10,stroke:#fbbf24,color:#fdf3d4;
  classDef capsule fill:#0f2f25,stroke:#34d399,color:#dff9ee;
  classDef capstone fill:#3a1320,stroke:#fb7185,color:#ffe2e8;
  class W01M1,W01M2,W01M3,W01M4,W01M5 orientation;
  class W02M1,W02M2,W02M3,W02M4,W02M5,W03M1,W03M2,W03M3,W03M4,W03M5,W04M1,W04M2,W04M3,W04M4,W04M5,W05M1,W05M2,W05M3,W05M4,W05M5 inference;
  class W06M1,W06M2,W06M3,W06M4,W06M5 prompting;
  class W07M1,W07M2,W07M3,W07M4,W07M5 agents;
  class W08M1,W08M2,W08M3,W08M4,W08M5,W09M1,W09M2,W09M3,W09M4,W09M5 capsule;
  class W10M1,W10M2,W10M3,W10M4,W10M5 capstone;

  click W01M1 "../lessons/module-01/01-welcome-and-context/" "Welcome & Context"
  click W01M2 "../lessons/module-01/02-shell-and-linux/" "Shell & Linux"
  click W01M3 "../lessons/module-01/03-git-workflow/" "Git Workflow"
  click W01M4 "../lessons/module-01/04-how-computers-run-ai/" "How Computers Run AI"
  click W01M5 "../lessons/module-01/quiz.html" "Consolidation"
  click W02M1 "../lessons/module-02/01-prompt-pipeline/" "What Happens When You Send a Prompt"
  click W02M2 "../lessons/module-02/02-meet-the-gpu/" "Meet the GPU"
  click W02M3 "../lessons/module-02/03-memory-bottleneck/" "Memory Is the Bottleneck"
  click W02M4 "../lessons/module-02/04-compute-vs-memory-bound/" "Compute-Bound vs Memory-Bound"
  click W02M5 "../lessons/module-02/quiz.html" "Consolidation"
  click W03M1 "../lessons/module-03/01-prefill-and-decode/" "Prefill vs Decode"
  click W03M2 "../lessons/module-03/02-kv-cache/" "KV Cache"
  click W03M3 "../lessons/module-03/03-flash-and-paged-attention/" "FlashAttention"
  click W03M4 "../lessons/module-03/04-quantization/" "Quantization"
  click W03M5 "../lessons/module-03/quiz.html" "Consolidation"
  click W04M1 "../lessons/module-04/01-tensor-parallelism/" "Multi-GPU Parallelism"
  click W04M2 "../lessons/module-04/02-pipeline-expert-parallelism/" "Pipeline Parallelism + MoE"
  click W04M3 "../lessons/module-04/03-speculative-decoding/" "Speculative Decoding"
  click W04M4 "../lessons/module-04/04-serving-engines/" "vLLM Introduction"
  click W04M5 "../lessons/module-04/quiz.html" "Consolidation"
  click W05M1 "../lessons/module-05/01-metrics/" "Latency vs Throughput"
  click W05M2 "../lessons/module-05/02-production-patterns/" "Production Deployment"
  click W05M3 "../lessons/module-05/03-evaluation-quality/" "LLM Evaluation"
  click W05M4 "../lessons/module-05/04-cost-economics/" "Inference Economics"
  click W05M5 "../lessons/module-05/quiz.html" "Consolidation + Phase 1 Problem Set"
  click W06M1 "../lessons/module-06/01-prompt-structure/" "Prompt Structure & Clarity"
  click W06M2 "../lessons/module-06/02-roles-data-formatting/" "Roles, Data Separation & Output Formatting"
  click W06M3 "../lessons/module-06/03-cot-few-shot/" "Chain-of-Thought & Few-Shot Prompting"
  click W06M4 "../lessons/module-06/04-hallucinations-evals/" "Avoiding Hallucinations & Complex Prompts"
  click W06M5 "../lessons/module-06/quiz.html" "Consolidation: Chaining, Tool Use & Evals"
  click W07M1 "../lessons/module-07/01-agent-loop/" "The Agent Loop"
  click W07M2 "../lessons/module-07/02-tools-and-mcp/" "Tools & MCP"
  click W07M3 "../lessons/module-07/03-governance-security/" "Governance & Security"
  click W07M4 "../lessons/module-07/04-orchestration-multi-agent/" "Orchestration & Multi-Agent"
  click W07M5 "../lessons/module-07/quiz.html" "Consolidation: Agent Case Studies + Design"
  click W08M1 "../lessons/module-08/01-architecture-install/" "Capsule Architecture & Installation"
  click W08M2 "../lessons/module-08/02-environments-fleet/" "Environments & Fleet Discovery"
  click W08M3 "../lessons/module-08/03-connecting/" "Connecting to Machines"
  click W08M4 "../lessons/module-08/04-files-storage-streaming/" "Files, Storage & Streaming"
  click W08M5 "../lessons/module-08/quiz.html" "Consolidation: Reliability & Diagnostics"
  click W09M1 "../lessons/module-09/01-first-benchmark/" "Your First Benchmark"
  click W09M2 "../lessons/module-09/02-varying-parameters/" "Varying Parameters"
  click W09M3 "../lessons/module-09/03-interactive-eval/" "Interactive Evaluation"
  click W09M4 "../lessons/module-09/04-scheduling-mcp/" "Scheduling & MCP"
  click W09M5 "../lessons/module-09/quiz.html" "Consolidation: End-to-End Eval Sprint"
  click W10M1 "../lessons/module-10/01-kickoff-and-planning/" "Kickoff & Planning"
  click W10M2 "../lessons/module-10/02-execute/" "Execute"
  click W10M3 "../lessons/module-10/03-analyze-recommend/" "Analyze & Recommend"
  click W10M4 "../lessons/module-10/04-present/" "Present"
  click W10M5 "../lessons/module-10/05-close/" "Close"
```

## Legend

| Colour | Phase | Weeks |
|--------|-------|-------|
| ▣ | Orientation | Week 1 |
| ▣ | Inference Engineering | Week 2, 3, 4, 5 |
| ▣ | Prompt Engineering | Week 6 |
| ▣ | AI Agents | Week 7 |
| ▣ | Capsule Hands-On | Week 8, 9 |
| ▣ | Capstone | Week 10 |

Day 05 of weeks 1–9 is the Friday quiz (`quiz.html` in each module folder). Day 50 closes the program.
