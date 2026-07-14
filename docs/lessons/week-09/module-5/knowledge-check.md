<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 9 - Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <a href="../">Day 45 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-09/module-5}
  </div>
</div>

# Week 9 Knowledge Check

**Week 9 · Capsule Benchmarking & Evaluation.** 26-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative, it never blocks you, but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 9 · Capsule Benchmarking &amp; Evaluation" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "A `capsule benchmark` run is built from three pieces. Which set names them?",
    "options": [
      "GPU, CPU, and RAM",
      "Prompt, response, and score",
      "A load generator, a serving engine, and metric collection",
      "Frontend, API, and database"
    ],
    "answer": 2,
    "explain": "Day 42's anatomy diagram breaks a run into three pieces: the load generator (what prompts, what concurrency, how long), the serving engine (vllm etc. running the model + config), and metric collection (TTFT, ITL, throughput, percentiles). The resulting numbers upload to the benchmark dashboard. The other options describe hardware, a single request, or web infrastructure."
  },
  {
    "stem": "You run one clean benchmark. What can you legitimately claim from that single run?",
    "options": [
      "This config beats every other config",
      "This model is good",
      "This serving engine is bad",
      "This config, under this load, at this moment produced these numbers: nothing more"
    ],
    "answer": 3,
    "explain": "Day 42: a single data point is not a comparison, a scaling law, or a saturation test. To claim one engine is faster you need a comparison run; to claim it scales you must vary the load; to judge quality you need the Day 44 eval. One run only pins down this exact config at this moment."
  },
  {
    "stem": "Which three metric families does a `capsule benchmark` report contain?",
    "options": [
      "Throughput, latency percentiles, and cost-per-token",
      "Training loss, validation loss, and epoch count",
      "CPU usage, disk I/O, and network latency",
      "Time-to-first-token only"
    ],
    "answer": 0,
    "explain": "capsule benchmark drives the inference server with InferenceMAX and reports throughput (tokens/sec), latency percentiles (TTFT/ITL p50/p99), and cost-per-token: exactly the Phase-1 vocabulary built up over prior weeks. Training metrics are a distractor: a benchmark drives inference, it does not train."
  },
  {
    "stem": "Which four serving backends does `capsule benchmark` support?",
    "options": [
      "vllm, sglang, tensorrt-llm, triton",
      "vllm, llamacpp, mlx, oxpython",
      "vllm, ollama, mlx, transformers",
      "llamacpp, exllama, mlx, deepspeed"
    ],
    "answer": 1,
    "explain": "The four backends are vllm (default on NVIDIA; batched serving with paged-attention), llamacpp (CPU-friendly, GGUF quants), mlx (Apple Silicon), and oxpython (the OXMIQ Python runtime for in-house eval). SGLang, TensorRT-LLM, and Ollama are common distractors but are not options."
  },
  {
    "stem": "Which flag selects the serving backend for a benchmark run?",
    "options": [
      "--engine",
      "--runtime",
      "--serve",
      "--backend"
    ],
    "answer": 3,
    "explain": "The backend is chosen with `--backend` (for example `--backend llamacpp`). There is no `--engine` flag in capsule benchmark; if you omit `--backend`, vllm is the default on an NVIDIA box."
  },
  {
    "stem": "In `capsule benchmark ... --concurrency 8 --num-prompts 80`, what does `--num-prompts` set?",
    "options": [
      "How many seconds the load runs before stopping",
      "The number of GPUs allocated to the run",
      "The total number of requests sent before the run stops",
      "The number of simultaneous in-flight requests"
    ],
    "answer": 2,
    "explain": "`--num-prompts` (`-n`) is the total number of requests sent; `--concurrency` is how many are in flight at once. Run size is set by `--num-prompts` (default: concurrency × 10), not by any duration flag; there is no `--duration` in capsule benchmark."
  },
  {
    "stem": "By default, where do the results of a `capsule benchmark` run go?",
    "options": [
      "To /shared/runs/<timestamp>/report.json",
      "They upload to the Capsule benchmark dashboard unless you pass --no-upload",
      "To ~/.capsule/results/ on the remote node",
      "They print to stdout and are then discarded"
    ],
    "answer": 1,
    "explain": "Every run uploads to the benchmark dashboard by default, keyed to the model + config: the durable, shareable home for throughput, latency, and cost-per-token. Pass `--no-upload` while iterating to keep noisy in-progress runs off the shared dashboard. There is no `/shared/runs/` directory convention."
  },
  {
    "stem": "What is the minimum-viable command to benchmark a model on a leased node?",
    "options": [
      "capsule benchmark <config-tag> meta-llama/Llama-3.1-8B-Instruct",
      "capsule benchmark --engine vllm --duration 60s meta-llama/Llama-3.1-8B-Instruct",
      "capsule bench meta-llama/Llama-3.1-8B-Instruct --backend auto --out /shared/runs/",
      "capsule benchmark run meta-llama/Llama-3.1-8B-Instruct --concurrency 8 --duration 60s"
    ],
    "answer": 0,
    "explain": "`capsule benchmark <config-tag> <model>` is the smallest form: it provisions a server on the target and drives it with InferenceMAX using defaults (vllm on NVIDIA, sensible TP/quant/prompt distribution). The distractors invent `--engine`, `--duration`, `--out`, a `bench` alias, and a `run` subcommand that do not exist."
  },
  {
    "stem": "How do you benchmark an OpenAI-compatible endpoint you already have, without provisioning a machine?",
    "options": [
      "You cannot; capsule benchmark always provisions a fresh server",
      "capsule benchmark --remote <url> --no-deploy <model>",
      "capsule benchmark --api-base <url> --api-key <key> <model>",
      "capsule benchmark --external-endpoint <url> <model>"
    ],
    "answer": 2,
    "explain": "`--api-base` plus `--api-key` skips provisioning entirely and benchmarks an existing OpenAI-compatible endpoint (for example a local `capsule chat` server). No config tag is needed in that form. `--remote`, `--no-deploy`, and `--external-endpoint` are fabricated."
  },
  {
    "stem": "A saturation curve from a concurrency sweep plots:",
    "options": [
      "Memory vs time",
      "Quality vs cost",
      "TTFT vs model size",
      "Throughput vs concurrency"
    ],
    "answer": 3,
    "explain": "Sweeping `--concurrency` and plotting throughput against it traces the saturation curve. The elbow marks the max useful concurrency: before it, throughput rises ~linearly; after it, throughput plateaus and TTFT explodes as requests queue."
  },
  {
    "stem": "Past the elbow of the throughput-vs-concurrency curve, which metric degrades fastest?",
    "options": [
      "Throughput",
      "TTFT p99",
      "GPU utilization",
      "GPU memory"
    ],
    "answer": 1,
    "explain": "Beyond the elbow the GPU is saturated, so new requests queue. Queue time adds directly to TTFT and the tail (p99) blows up first, while throughput merely plateaus. Flat throughput with an exploding tail latency is the signature of running past saturation."
  },
  {
    "stem": "Doubling tensor parallelism from TP=1 to TP=2 on a large model usually produces:",
    "options": [
      "A sub-linear throughput gain, because all-reduce comm overhead eats part of the win",
      "Exactly 2× throughput",
      "2× per-request latency",
      "No measurable change"
    ],
    "answer": 0,
    "explain": "TP splits each matmul across GPUs, but the all-reduce communication between them costs time that doesn't exist at TP=1, so throughput rises less than 2× (Week 4). For latency-bound small batches TP can still cut TTFT; the net effect must be measured, not assumed."
  },
  {
    "stem": "Switching from FP16 to FP8 at the same concurrency typically:",
    "options": [
      "Lowers throughput and improves quality",
      "Has no measurable effect on any metric",
      "Raises throughput ~1.5–2× and may slightly reduce quality",
      "Doubles per-request latency"
    ],
    "answer": 2,
    "explain": "FP8 doubles memory bandwidth and compute density, so throughput rises ~1.5–2× and smaller weights load faster (TTFT may drop). Precision loss can shave quality a little: which is exactly why you run the Day 44 eval suite alongside the speed numbers instead of trusting throughput alone."
  },
  {
    "stem": "Running benchmarks back-to-back on one node, which is a real confounding variable and its mitigation?",
    "options": [
      "The model's parameter count silently changing; re-download the weights",
      "Thermal throttling from the previous run; pause ~30s and check `nvidia-smi -q -d CLOCK`",
      "The CLI being out of date; run `capsule update` between runs",
      "The dashboard being offline; pass `--no-upload`"
    ],
    "answer": 1,
    "explain": "Day 43's confound table lists thermal throttling (pause ~30s, check clocks), cold warmup (pre-warm or discard the first request), noisy neighbors (verify idle GPU util = 0), drifted prompt distribution (fix the seed/prompt set), and reused quant cache (clear between fundamentally different configs)."
  },
  {
    "stem": "An 8B model at TP=4 shows throughput barely above TP=2 and GPU compute util of only 0.35. Which regime is this?",
    "options": [
      "Memory bandwidth-bound: quantization helps most",
      "Compute-bound: a faster GPU helps most",
      "I/O-bound: weight loading from disk dominates",
      "Communication-bound: drop TP or move to a larger model"
    ],
    "answer": 3,
    "explain": "Day 43's third regime: high TP on a small model. Adding GPUs barely improves per-step time because all-reduce overhead dominates, and compute util stays low because each GPU has too little work. The fix is fewer GPUs (lower TP) or a bigger model: not more quant or a faster GPU."
  },
  {
    "stem": "The sweep template varies one axis at a time and holds everything else fixed. Why?",
    "options": [
      "So any change in the metric can be attributed to the single axis you varied",
      "Because the serving engine only accepts one flag per invocation",
      "Because varying two parameters at once crashes the GPU",
      "Because the dashboard can only plot one run at a time"
    ],
    "answer": 0,
    "explain": "If you change concurrency AND quantization together, a throughput shift can't be pinned on either; the experiment is confounded. Isolating one variable is what lets each observed change map back to a single Phase-1 concept you can name."
  },
  {
    "stem": "A new config is 30% faster but fails your eval suite on medical prompts. The right conclusion is:",
    "options": [
      "Ship it; throughput is the SLA metric",
      "A fast config that gives worse answers is a worse config; throughput is not quality",
      "The eval suite must be wrong",
      "Add more GPU memory and re-run"
    ],
    "answer": 1,
    "explain": "Day 44's core lesson: throughput is not quality. A config that hallucinates dosages or refuses benign requests is a worse deployment however fast it is. Run the eval suite alongside every config change and weigh both dimensions before shipping."
  },
  {
    "stem": "The minimum useful interactive eval suite for catching regressions is about:",
    "options": [
      "1 prompt",
      "1000 prompts drawn from the training set",
      "5–10 curated probes across correctness, refusals, safety, format, and hallucination",
      "100+ prompts, always required for statistical significance"
    ],
    "answer": 2,
    "explain": "Day 44 frames 5–10 curated prompts as a smoke test: enough to flag when a config change breaks a capability you care about. It is NOT production certification; validating general quality needs the far broader eval setup from Week 5 Day 23."
  },
  {
    "stem": "In the eval suite, how do a 'refusal probe' and a 'safety probe' differ?",
    "options": [
      "They are the same test run twice for reliability",
      "The refusal probe checks GPU limits; the safety probe checks memory",
      "The safety probe measures TTFT; the refusal probe measures ITL",
      "The refusal probe is benign-but-edgy and should NOT be refused; the safety probe is out-of-bounds and SHOULD be refused"
    ],
    "answer": 3,
    "explain": "They probe opposite failure modes of the same safety boundary: the refusal probe catches over-refusal (the model wrongly declining a benign request), while the safety probe catches under-refusal (the model complying with something it should decline)."
  },
  {
    "stem": "For a human-facing chat product, roughly what TTFT and ITL do you target?",
    "options": [
      "TTFT < 10 ms always; ITL irrelevant",
      "TTFT < ~600 ms and ITL matched to reading pace (~30–60 tok/s)",
      "Whatever maximizes raw throughput",
      "Match a database query at < 1 ms"
    ],
    "answer": 1,
    "explain": "Day 44's felt-latency table: below ~600 ms TTFT feels snappy, and ~30–60 tok/s matches reading pace. For agent/tool calls with no human reading the stream you instead push throughput as high as possible; felt latency stops mattering."
  },
  {
    "stem": "What does 'streaming smoothness' in the chat UI reveal that a benchmark percentile can hide?",
    "options": [
      "Whether ITL is consistent enough to stream without a visible mid-response stutter",
      "The GPU temperature during inference",
      "The total number of tokens generated",
      "Network bandwidth to your laptop"
    ],
    "answer": 0,
    "explain": "ITL p50 might be 18 ms while p99 is 200 ms: an occasional jarring pause you only notice by watching the stream. Percentiles give you the numbers; the chat UI shows whether those numbers translate into a smooth felt experience."
  },
  {
    "stem": "What kind of tool is `capsule schedule`?",
    "options": [
      "A cron-style recurring scheduler you register with `--cron '0 2 * * *'`",
      "A calendar system that reserves a GPU node for a future time slot",
      "A one-shot job queue: it runs a submitted script once on a remote node as a detached daemon",
      "A wrapper that reruns `capsule benchmark` in a loop until cancelled"
    ],
    "answer": 2,
    "explain": "`capsule schedule` queues a script, dispatches it to an available node, and runs it once as a detached daemon that survives SSH/session teardown. It is NOT cron; there is no `--cron` and no recurrence. A real nightly cadence comes from an external cron/CI trigger that calls `capsule schedule start`."
  },
  {
    "stem": "Which command submits a benchmark script to a node pool as a one-shot detached job?",
    "options": [
      "capsule schedule create --cron '0 2 * * *' --command ./bench.sh",
      "capsule schedule submit ./bench.sh --pool <config-tag>",
      "capsule benchmark schedule ./bench.sh --nightly",
      "capsule schedule start <config-tag> --script ./bench.sh --name nightly --timeout 4h"
    ],
    "answer": 3,
    "explain": "The real form is `capsule schedule start <config-tag> --script <file>` (script required; `-n`/`--name`, `-t`/`--timeout` shape the job). With a config tag it dispatches to the first available node in the pool. There is no `create`, `submit`, or `--cron` on schedule."
  },
  {
    "stem": "A scheduled job has finished. How do you check its state and read its output?",
    "options": [
      "`capsule schedule list` for the next cron fire time, then open report.json in --out",
      "`capsule schedule status` (filter with --me/--state) for state, and `capsule schedule logs <job-id> --tail N` for output",
      "`capsule schedule ps --watch`; logs auto-commit to your repo as stdout.log",
      "`capsule schedule runs <name>`; results save to ~/.capsule/results"
    ],
    "answer": 1,
    "explain": "`capsule schedule status` lists jobs and their state (PENDING → RUNNING → COMPLETED/FAILED/CANCELLED), filterable by --me and --state. The node streams output.log to storage during the run; read it back with `capsule schedule logs <job-id>`, optionally --tail N. Cancel with `capsule schedule cancel <job-id>` (or --all). There is no list/ps/runs subcommand or --out directory."
  },
  {
    "stem": "What does Capsule's MCP surface (`capsule mcp`) unlock that the CLI alone does not?",
    "options": [
      "Access to faster GPU hardware",
      "Encrypted communication with the control plane",
      "An MCP-capable assistant can call Capsule actions as tools: list/filter machines, run a benchmark via capsule_exec, move files",
      "Support for more concurrency levels than the CLI"
    ],
    "answer": 2,
    "explain": "`capsule mcp` installs a Model Context Protocol config so an assistant (Claude Desktop / Claude Code) can drive Capsule as tools: the same set `capsule agent` uses: capsule_list, capsule_filter, capsule_exec, capsule_scp_upload/download. The Week 6 agent you designed can now discover a machine, kick a benchmark, and pull results back."
  },
  {
    "stem": "A benchmark-running agent calls write tools like `capsule_exec`. Which governance controls matter most?",
    "options": [
      "None: benchmark agents are read-only",
      "Runtime/session cap, cost budget, scoped least-privilege credentials, and an audit trail",
      "A bigger model for the agent",
      "More GPUs in the pool"
    ],
    "answer": 1,
    "explain": "Write tools (kick a workload, upload a script) consume real resources, so the Week 6 governance vocabulary applies: cap how long the agent holds a node, bound its spend, scope its token to one env with read+benchmark only, and pipe an audit log to humans. That bounds the blast radius of an autonomous nightly agent."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Back to today's lesson__

    [Day 45 · Consolidation](index.md)

-   __Back to the week__

    [Week 9 - Capsule: Benchmarking &amp; Eval overview](../index.md)

-   __Continue the curriculum__

    [Day 46 · Kickoff &amp; Planning](../../week-10/module-1/index.md)

</div>
