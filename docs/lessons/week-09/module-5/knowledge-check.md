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
  {"stem": "A `capsule benchmark` run is built from three pieces. Which set names them?", "options": ["GPU, CPU, and RAM", "Prompt, response, and score", "A load generator, a serving engine, and metric collection", "Frontend, API, and database"]},
  {"stem": "You run one clean benchmark. What can you legitimately claim from that single run?", "options": ["This config beats every other config", "This model is good", "This serving engine is bad", "This config, under this load, at this moment produced these numbers: nothing more"]},
  {"stem": "Which three metric families does a `capsule benchmark` report contain?", "options": ["Throughput, latency percentiles, and cost-per-token", "Training loss, validation loss, and epoch count", "CPU usage, disk I/O, and network latency", "Time-to-first-token only"]},
  {"stem": "Which four serving backends does `capsule benchmark` support?", "options": ["vllm, sglang, tensorrt-llm, triton", "vllm, llamacpp, mlx, oxpython", "vllm, ollama, mlx, transformers", "llamacpp, exllama, mlx, deepspeed"]},
  {"stem": "Which flag selects the serving backend for a benchmark run?", "options": ["--engine", "--runtime", "--serve", "--backend"]},
  {"stem": "In `capsule benchmark ... --concurrency 8 --num-prompts 80`, what does `--num-prompts` set?", "options": ["How many seconds the load runs before stopping", "The number of GPUs allocated to the run", "The total number of requests sent before the run stops", "The number of simultaneous in-flight requests"]},
  {"stem": "By default, where do the results of a `capsule benchmark` run go?", "options": ["To /shared/runs/<timestamp>/report.json", "They upload to the Capsule benchmark dashboard unless you pass --no-upload", "To ~/.capsule/results/ on the remote node", "They print to stdout and are then discarded"]},
  {"stem": "What is the minimum-viable command to benchmark a model on a leased node?", "options": ["capsule benchmark <config-tag> meta-llama/Llama-3.1-8B-Instruct", "capsule benchmark --engine vllm --duration 60s meta-llama/Llama-3.1-8B-Instruct", "capsule bench meta-llama/Llama-3.1-8B-Instruct --backend auto --out /shared/runs/", "capsule benchmark run meta-llama/Llama-3.1-8B-Instruct --concurrency 8 --duration 60s"]},
  {"stem": "How do you benchmark an OpenAI-compatible endpoint you already have, without provisioning a machine?", "options": ["You cannot; capsule benchmark always provisions a fresh server", "capsule benchmark --remote <url> --no-deploy <model>", "capsule benchmark --api-base <url> --api-key <key> <model>", "capsule benchmark --external-endpoint <url> <model>"]},
  {"stem": "A saturation curve from a concurrency sweep plots:", "options": ["Memory vs time", "Quality vs cost", "TTFT vs model size", "Throughput vs concurrency"]},
  {"stem": "Past the elbow of the throughput-vs-concurrency curve, which metric degrades fastest?", "options": ["Throughput", "TTFT p99", "GPU utilization", "GPU memory"]},
  {"stem": "Doubling tensor parallelism from TP=1 to TP=2 on a large model usually produces:", "options": ["A sub-linear throughput gain, because all-reduce comm overhead eats part of the win", "Exactly 2× throughput", "2× per-request latency", "No measurable change"]},
  {"stem": "Switching from FP16 to FP8 at the same concurrency typically:", "options": ["Lowers throughput and improves quality", "Has no measurable effect on any metric", "Raises throughput ~1.5–2× and may slightly reduce quality", "Doubles per-request latency"]},
  {"stem": "Running benchmarks back-to-back on one node, which is a real confounding variable and its mitigation?", "options": ["The model's parameter count silently changing; re-download the weights", "Thermal throttling from the previous run; pause ~30s and check `nvidia-smi -q -d CLOCK`", "The CLI being out of date; run `capsule update` between runs", "The dashboard being offline; pass `--no-upload`"]},
  {"stem": "An 8B model at TP=4 shows throughput barely above TP=2 and GPU compute util of only 0.35. Which regime is this?", "options": ["Memory bandwidth-bound: quantization helps most", "Compute-bound: a faster GPU helps most", "I/O-bound: weight loading from disk dominates", "Communication-bound: drop TP or move to a larger model"]},
  {"stem": "The sweep template varies one axis at a time and holds everything else fixed. Why?", "options": ["So any change in the metric can be attributed to the single axis you varied", "Because the serving engine only accepts one flag per invocation", "Because varying two parameters at once crashes the GPU", "Because the dashboard can only plot one run at a time"]},
  {"stem": "A new config is 30% faster but fails your eval suite on medical prompts. The right conclusion is:", "options": ["Ship it; throughput is the SLA metric", "A fast config that gives worse answers is a worse config; throughput is not quality", "The eval suite must be wrong", "Add more GPU memory and re-run"]},
  {"stem": "The minimum useful interactive eval suite for catching regressions is about:", "options": ["1 prompt", "1000 prompts drawn from the training set", "5–10 curated probes across correctness, refusals, safety, format, and hallucination", "100+ prompts, always required for statistical significance"]},
  {"stem": "In the eval suite, how do a 'refusal probe' and a 'safety probe' differ?", "options": ["They are the same test run twice for reliability", "The refusal probe checks GPU limits; the safety probe checks memory", "The safety probe measures TTFT; the refusal probe measures ITL", "The refusal probe is benign-but-edgy and should NOT be refused; the safety probe is out-of-bounds and SHOULD be refused"]},
  {"stem": "For a human-facing chat product, roughly what TTFT and ITL do you target?", "options": ["TTFT < 10 ms always; ITL irrelevant", "TTFT < ~600 ms and ITL matched to reading pace (~30–60 tok/s)", "Whatever maximizes raw throughput", "Match a database query at < 1 ms"]},
  {"stem": "What does 'streaming smoothness' in the chat UI reveal that a benchmark percentile can hide?", "options": ["Whether ITL is consistent enough to stream without a visible mid-response stutter", "The GPU temperature during inference", "The total number of tokens generated", "Network bandwidth to your laptop"]},
  {"stem": "What kind of tool is `capsule schedule`?", "options": ["A cron-style recurring scheduler you register with `--cron '0 2 * * *'`", "A calendar system that reserves a GPU node for a future time slot", "A one-shot job queue: it runs a submitted script once on a remote node as a detached daemon", "A wrapper that reruns `capsule benchmark` in a loop until cancelled"]},
  {"stem": "Which command submits a benchmark script to a node pool as a one-shot detached job?", "options": ["capsule schedule create --cron '0 2 * * *' --command ./bench.sh", "capsule schedule submit ./bench.sh --pool <config-tag>", "capsule benchmark schedule ./bench.sh --nightly", "capsule schedule start <config-tag> --script ./bench.sh --name nightly --timeout 4h"]},
  {"stem": "A scheduled job has finished. How do you check its state and read its output?", "options": ["`capsule schedule list` for the next cron fire time, then open report.json in --out", "`capsule schedule status` (filter with --me/--state) for state, and `capsule schedule logs <job-id> --tail N` for output", "`capsule schedule ps --watch`; logs auto-commit to your repo as stdout.log", "`capsule schedule runs <name>`; results save to ~/.capsule/results"]},
  {"stem": "What does Capsule's MCP surface (`capsule mcp`) unlock that the CLI alone does not?", "options": ["Access to faster GPU hardware", "Encrypted communication with the control plane", "An MCP-capable assistant can call Capsule actions as tools: list/filter machines, run a benchmark via capsule_exec, move files", "Support for more concurrency levels than the CLI"]},
  {"stem": "A benchmark-running agent calls write tools like `capsule_exec`. Which governance controls matter most?", "options": ["None: benchmark agents are read-only", "Runtime/session cap, cost budget, scoped least-privilege credentials, and an audit trail", "A bigger model for the agent", "More GPUs in the pool"]}
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
