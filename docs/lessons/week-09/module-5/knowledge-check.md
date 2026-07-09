<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 9 — Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <a href="../">Day 45 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-09/module-5}
  </div>
</div>

# Week 9 Knowledge Check

**Week 9 · Capsule Benchmarking & Evaluation.** 15 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 9 · Capsule Benchmarking &amp; Evaluation" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "A benchmark run consists of three pieces:",
    "options": [
      "GPU / CPU / RAM",
      "Load generator / serving engine / metric collection",
      "Prompt / response / score",
      "Frontend / API / DB"
    ],
    "answer": 1,
    "explain": "Plus the report.json output."
  },
  {
    "stem": "After one benchmark run completes, you can claim:",
    "options": [
      "This config beats all others",
      "This config, this load, this moment produced these numbers — nothing more",
      "The model is good",
      "The engine is bad"
    ],
    "answer": 1,
    "explain": "One data point isn't a comparison or a scaling law."
  },
  {
    "stem": "A saturation curve plots:",
    "options": [
      "Memory vs time",
      "Throughput vs concurrency",
      "Quality vs cost",
      "TTFT vs model size"
    ],
    "answer": 1,
    "explain": "The elbow = max useful concurrency before TTFT explodes."
  },
  {
    "stem": "Past the elbow of a saturation curve, the metric that degrades fastest is:",
    "options": [
      "Throughput",
      "TTFT p99",
      "GPU util",
      "Memory"
    ],
    "answer": 1,
    "explain": "Requests queue → TTFT explodes; throughput stays flat."
  },
  {
    "stem": "Doubling TP from 1 to 2 on a large model usually produces:",
    "options": [
      "Exactly 2× throughput",
      "Sub-linear throughput gain due to comm overhead",
      "No change",
      "2× latency"
    ],
    "answer": 1,
    "explain": "Comm cost eats some of the parallelism win — Week 4."
  },
  {
    "stem": "FP8 vs FP16 typically:",
    "options": [
      "Lowers throughput",
      "Raises throughput ~1.5–2× and may slightly reduce quality",
      "Improves quality",
      "No effect"
    ],
    "answer": 1,
    "explain": "Memory bandwidth + compute density up; precision down a bit."
  },
  {
    "stem": "The single most common confounding variable in back-to-back benchmarks on one node is:",
    "options": [
      "Phase of the moon",
      "Thermal throttling / no warmup / cache reuse / other users",
      "Internet speed",
      "Your laptop"
    ],
    "answer": 1,
    "explain": "Mitigate with pauses, warmups, cache clears, lease verification."
  },
  {
    "stem": "Throughput is not quality because:",
    "options": [
      "Throughput is always wrong",
      "A fast config that gives worse answers is a worse config",
      "Quality is faster",
      "They mean the same thing"
    ],
    "answer": 1,
    "explain": "Run a 5–10 prompt eval suite alongside every config change."
  },
  {
    "stem": "The minimum useful prompt-eval suite size is approximately:",
    "options": [
      "1",
      "5–10 curated probes covering correctness, refusals, safety, format, hallucination",
      "100",
      "1000"
    ],
    "answer": 1,
    "explain": "Enough for a smoke test that catches regressions."
  },
  {
    "stem": "For a human-facing chat product, target TTFT and ITL are roughly:",
    "options": [
      "Doesn't matter",
      "TTFT < ~600 ms, ITL ~30–60 tok/s (reading pace)",
      "TTFT < 10 ms always",
      "Match a database"
    ],
    "answer": 1,
    "explain": "Felt latency differs from measured latency."
  },
  {
    "stem": "<code>capsule schedule</code> lets you:",
    "options": [
      "Nothing",
      "Run benchmarks on a cron, on auto-leased nodes, with audit",
      "Order pizza",
      "Replace MCP"
    ],
    "answer": 1,
    "explain": "Cron + auto-lease + audit + log per run."
  },
  {
    "stem": "Nightly scheduled benchmarks primarily catch:",
    "options": [
      "Cosmic rays",
      "Regressions between commits, model versions, or infra changes",
      "User complaints",
      "Sales spikes"
    ],
    "answer": 1,
    "explain": "Without a baseline you only learn about regressions from users."
  },
  {
    "stem": "Capsule's MCP surface lets:",
    "options": [
      "Only humans use it",
      "An agent (Claude/OxCode/Cursor) call benchmark + lease tools through a standard protocol",
      "Capsule reach the internet",
      "More GPUs appear"
    ],
    "answer": 1,
    "explain": "Week 7's tool-design vocabulary applies directly."
  },
  {
    "stem": "A benchmark-running agent needs which Week-7 governance controls (most critical)?",
    "options": [
      "None",
      "Lease-time cap, cost budget, scoped credentials, audit trail",
      "Bigger model",
      "More GPUs"
    ],
    "answer": 1,
    "explain": "Write tools (lease, kick benchmark) need bounded blast radius."
  },
  {
    "stem": "By the end of Week 9 you can defend a benchmark result in:",
    "options": [
      "No vocabulary",
      "Phase 1 vocabulary (TTFT, ITL, throughput, memory vs compute bound, batching, TP, quant)",
      "Marketing language",
      "Random jargon"
    ],
    "answer": 1,
    "explain": "That's the whole point of Weeks 1–5 made operational."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 45 · Consolidation](index.md)

-   __Back to the week__

    [Week 9 — Capsule: Benchmarking &amp; Eval overview](../index.md)

-   __Continue the curriculum__

    [Day 46 · Kickoff &amp; Planning](../../week-10/module-1/index.md)

</div>
