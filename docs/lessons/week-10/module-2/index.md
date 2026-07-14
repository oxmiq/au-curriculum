# Day 47 · Execute

> **Concept of the day:** today the charter becomes data. Deploy your chosen model on Capsule, run the benchmark sweep, run the interactive eval. Document obsessively; Day 48 cannot reconstruct what Day 47 forgot to write down.<br>
> **Source template:** [Day-47 Execution Checklist](../../../../planning/source-material/Capstone/Day-47-Execution-Checklist.md) (source filename is `Day-47-...` from upstream capstone-relative naming; this is program Day 47).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 10 - Capstone Project</a>
    <span class="sep">/</span>
    <span>Day 47 · Execute</span>
    {status:week-10/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Execution checklist at a glance

| Step | Milestone |
|---|---|
| 1 | Lease hardware, deploy model, sanity-check server |
| 2 | Run benchmark sweep (all charter configs) |
| 3 | Run interactive eval (10-prompt suite, each config) |
| 4 | Documentation cleanup: log finalized, run dirs named |

## Why this matters

This is the day you put Weeks 1–9 to work. The benchmark workflow you sprinted in Week 9 Day 44 runs at production discipline today. Everything you log here becomes evidence on Thursday.

## Today's milestones

1. **Select appropriate hardware** from the fleet for your charter's plan: `capsule list --filter` (Day 35–36 skills).
2. **Deploy your model.** Stand it up on your chosen machine (Week 4 Day 19 serving-engine choice → Week 8 Day 37 connect → Week 9 Day 40 first benchmark).
3. **Run the benchmark sweep** from your charter: multiple configs as planned; watch the live run output.
4. **Results upload to the Capsule benchmark dashboard automatically** (unless `--no-upload`). Label each run so your team can find it.
5. **Run the interactive eval** (Day 42): your 10-prompt suite against each config.
6. **Log everything**: see "Execution log" below.
7. **End of day: a complete data set** sufficient to write the recommendation tomorrow.

## Execution log - what to capture

For every run, the log entry has:

| Field | Why |
|---|---|
| Config (model, engine, quant, TP, concurrency) | Reproducibility |
| Node ID + GPU | Hardware confound check |
| Command run | Reproducibility |
| Start / end time | Cost calculation later |
| Outcome (success / fail / partial) | Status |
| Dashboard run link | Evidence link |
| Eval pass/fail per prompt | Quality evidence |
| Notes / surprises | Day 47 narrative seed |

Keep this in a single markdown file in your run dir. **No log = the run didn't happen.**

## Suggested execution shape (per config)

```
# 1. Pick your machine from the fleet (Day 35-36)
capsule list --filter "vendor=nvidia,vram>=80"

# 2. Benchmark against that config tag; results upload to the dashboard
capsule benchmark <config-tag> <model> \
  --backend <vllm|llamacpp|mlx|oxpython> --concurrency <C> \
  --input-length 256 --output-length 256 --num-prompts <N>

# 3. Interactive eval (Day 42): run your 10-prompt suite against this config

# 4. Read results on the Capsule benchmark dashboard
#    (throughput, latency percentiles, cost-per-token).
#    Add --no-upload to step 2 only while iterating.

# 5. Log it (config tag, machine unique ID, exact command, dashboard link)
```

## Time budget for today

| Block | Minutes |
|---|---|
| Deploy + first run + sanity check | 60 |
| Benchmark sweep (per config × N configs) | 150 |
| Interactive eval | 90 |
| Documentation cleanup + log finalization | 30 |

If a config blows up, **don't debug forever**: note it, move on, come back if time. The deliverable rewards evidence, not perfection.

## When you're stuck

- "Model won't load" → memory math (Week 3 Day 12); maybe wrong GPU or wrong quant.
- "Benchmark stalls at 0 RPS" → serving-engine config didn't come up; check the run's engine startup output / dashboard run status.
- "Numbers don't match yesterday" → confound (Day 41); check warmup, neighbor processes, thermal.
- "Eval is subjective" → write the criterion down *before* you grade; have a teammate grade independently.

## Wrap-up

End of Day 47: every team has at least 2 configs benchmarked + evaluated with full logs. The recommendation writes itself if today's data is clean.

## Self-check before Day 48

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-10-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 47 · Execute">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the 8 fields of the execution log table?",
    "options": [
      "Config, GPU, command, time, error, log, eval, notes",
      "Config, node-ID, command, start time, end time, outcome, report-path, eval pass/fail and notes",
      "Model, quantization, TP, PP, concurrency, TTFT, throughput, cost",
      "Team, task, hardware, model, start, end, status, blockers"
    ],
    "answer": 1,
    "explain": "The 8-field execution log: (1) config (model + quant + TP + PP), (2) node-ID, (3) exact command run, (4) start time, (5) end time, (6) outcome (success/OOM/timeout/error), (7) report-path in shared storage, (8) eval pass/fail with notes. Every field must be filled; 'no log = run didn't happen.'"
  },
  {
    "stem": "Why is 'no log = run didn't happen' such an important principle?",
    "options": [
      "It is a grading rule; unlogged runs receive zero credit",
      "Memory is unreliable; without a log, you can't reproduce what you did, can't report exact results, and can't defend your recommendation on Day 50 under Q&A",
      "Logs are required for the benchmark to run correctly",
      "It prevents duplicate runs by checking if a run already exists"
    ],
    "answer": 1,
    "explain": "The lesson says: 'No execution log means the run didn't happen.' Memory is unreliable for exact commands, exact node-IDs, and exact error messages. Panel reviewers on Day 49 will ask 'what was your exact command?' and 'what error did config B throw?' You need the log to answer precisely. Unlogged runs can't be defended."
  },
  {
    "stem": "When a config blows up (OOM error, timeout, model fails to load), what should you do?",
    "options": [
      "Immediately restart and retry the same config until it works",
      "Note the failure in the log (config, error, outcome), move on to the next config, and come back if time permits; don't let one failure consume the execution day",
      "Skip that config and pretend it wasn't planned",
      "Request a different GPU and restart from the beginning"
    ],
    "answer": 1,
    "explain": "The lesson's execution advice: 'Note the failure, move on.' Record what happened (OOM at batch size 32, FP16 runs out of memory at 70B). A logged failure is a data point. Move to the next config. If you have time at the end, come back to the failed one. Don't let one bad run turn a 4-config plan into a 1-config day."
  },
  {
    "stem": "After a `capsule benchmark` run completes, how are its results preserved for Day 48 analysis?",
    "options": [
      "They are copied to /tmp on the node and pulled with `capsule storage get`",
      "`capsule benchmark` uploads results to the Capsule benchmark dashboard automatically unless you pass `--no-upload`; the dashboard is the durable, shareable record",
      "They persist only in the node's local /shared/runs directory until the lease ends",
      "Results are printed to stdout only; you must copy-paste them into your log"
    ],
    "answer": 1,
    "explain": "In the real Capsule CLI, `capsule benchmark` uploads its results to the benchmark dashboard by default; add `--no-upload` only if you want to suppress the upload. The dashboard is the durable record that survives the node lease, so Day 48 analysis pulls from it. Node-local paths disappear when the lease ends, which is why you never rely on them for evidence."
  },
  {
    "stem": "What does the interactive eval on Day 47 add that the benchmark run alone doesn't provide?",
    "options": [
      "Lower latency numbers",
      "Human-verified quality judgment per config: the 10-prompt suite with binary pass/fail tells you which config gives correct, well-formatted, on-topic answers, not just which is fastest",
      "More concurrency levels for the throughput curve",
      "Confirmation that the GPU hardware is working correctly"
    ],
    "answer": 1,
    "explain": "The benchmark measures speed (TTFT, throughput). The interactive eval measures quality (does it answer correctly, in the right format, without hallucinating). Day 47 does both: benchmark ALL charter configs (latency data), then run the 10-prompt eval suite against each (quality data). Both datasets are required for the Day 48 recommendation."
  },
  {
    "stem": "What should the 'outcome' field in the execution log capture?",
    "options": [
      "Only 'success' or 'failure' with no further detail",
      "The specific result: success, OOM (out of memory), timeout, model failed to load, partial (ran but numbers look wrong): with enough detail to diagnose without re-running",
      "The number of tokens generated per second",
      "The cost in GPU-hours for the run"
    ],
    "answer": 1,
    "explain": "The outcome field is your post-mortem in the log. 'Failure' tells you nothing when reviewing on Day 48. 'OOM at batch size 32, FP16, 70B model' tells you exactly what to adjust. 'Timeout after 8 minutes, benchmark never produced output' tells you the serving engine crashed. Specific outcomes make the log diagnostic, not just a record that something ran."
  },
  {
    "stem": "With 30 minutes left in Day 47 and one charter config still not benchmarked, what is the correct action?",
    "options": [
      "Skip the config entirely and don't mention it in the analysis",
      "Rush through a partial benchmark run and accept incomplete numbers",
      "Run the benchmark if it fits in 30 minutes; if not, log it as 'not run - time constraint' in the execution log with a note on what you'd expect and why",
      "Ask the instructor for an extension before attempting the run"
    ],
    "answer": 2,
    "explain": "The lesson's execution advice: 'note what didn't happen.' A logged 'not run - time constraint' entry is honest and useful for Day 48 analysis. You can still make a recommendation from the configs you did run, noting the gap. A rushed partial run with bad numbers is worse than a clean 'not run' entry; it introduces noise you have to explain on Day 49."
  },
  {
    "stem": "In the real Capsule CLI, which flag selects the serving backend for `capsule benchmark`?",
    "options": [
      "--backend <vllm|llamacpp|mlx|oxpython>",
      "--engine <vllm|llamacpp|mlx|oxpython>",
      "--duration <seconds>",
      "--out <path>"
    ],
    "answer": 0,
    "explain": "The real command is `capsule benchmark <config-tag> <model> --backend <vllm|llamacpp|mlx|oxpython> --num-prompts <N>`. The serving backend is chosen with `--backend`, and that choice maps directly to your Week 4 Day 19 serving-engine decision. There is no `--engine`, `--duration`, or `--out` flag on the real benchmark command."
  },
  {
    "stem": "Per the lesson's 'When you're stuck' table, what should you check first when the benchmark stalls at 0 RPS?",
    "options": [
      "The GPU's thermal throttling",
      "Whether the node lease has expired",
      "The serving-engine configuration: inspect stdout.log for engine startup errors",
      "The charter's success criterion"
    ],
    "answer": 2,
    "explain": "The debugging table maps 'Benchmark stalls at 0 RPS' to 'engine config; check stdout.log.' A 0-RPS stall means the serving engine never came up to accept requests. For contrast, 'Model won't load' points to memory math (wrong GPU or wrong quant, Week 3 Day 12), and 'Numbers don't match yesterday' points to a confound (warmup, neighbor processes, thermal - Day 41)."
  }
]
</script>
</div>

- [ ] At least 2 configs benchmarked with full execution logs (no TBD fields)
- [ ] Interactive eval completed for each config (pass/fail per prompt recorded)
- [ ] Run results in stable named directories (not `/tmp`)
- [ ] You can answer: "What surprised you?" with a specific observation

## Stuck?

Ask **oxtutor**; the debugging hints table (model won't load, benchmark stalls, numbers don't match) should unblock you in < 5 minutes if you share the exact error.
