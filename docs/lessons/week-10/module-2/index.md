# Day 48 · Execute

> **Concept of the day:** today the charter becomes data. Deploy your chosen model on Capsule, run the benchmark sweep, run the interactive eval. Document obsessively — Day 49 cannot reconstruct what Day 48 forgot to write down.<br>
> **Source template:** [Day-47 Execution Checklist](../../../../planning/source-material/Capstone/Day-47-Execution-Checklist.md) (source filename is `Day-47-...` from upstream capstone-relative naming; this is program Day 48).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 10 — Capstone Project</a>
    <span class="sep">/</span>
    <span>Day 48 · Execute</span>
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
| 4 | Documentation cleanup — log finalized, run dirs named |

## Why this matters

This is the day you put Weeks 1–9 to work. The benchmark workflow you sprinted in Week 9 Day 45 runs at production discipline today. Everything you log here becomes evidence on Thursday.

## Today's milestones

1. **Lease appropriate hardware** for your charter's plan (Day 36–37 skills).
2. **Deploy your model.** Stand it up on the leased node (Week 4 Day 19 serving-engine choice → Week 8 Day 38 connect → Week 9 Day 41 first benchmark).
3. **Run the benchmark sweep** from your charter. Multiple configs as planned. **Stream output** (Day 39).
4. **Pull results to `/shared/runs/capstone/<team>/<config>/`.** Stable, named, dated.
5. **Run the interactive eval** (Day 43) — your 10-prompt suite against each config.
6. **Log everything** — see "Execution log" below.
7. **End of day: a complete data set** sufficient to write the recommendation tomorrow.

## Execution log — what to capture

For every run, the log entry has:

| Field | Why |
|---|---|
| Config (model, engine, quant, TP, concurrency) | Reproducibility |
| Node ID + GPU | Hardware confound check |
| Command run | Reproducibility |
| Start / end time | Cost calculation later |
| Outcome (success / fail / partial) | Status |
| `report.json` path | Evidence link |
| Eval pass/fail per prompt | Quality evidence |
| Notes / surprises | Day 48 narrative seed |

Keep this in a single markdown file in your run dir. **No log = the run didn't happen.**

## Suggested execution shape (per config)

```
# 1. Lease (or reuse)
capsule node lease --gpu <type> --duration 4h --reason "capstone team <X> config <Y>"

# 2. Stage config
capsule cp ./config.yaml <node>:./

# 3. Benchmark (stream + record)
capsule run <node> --stream -- \
  capsule benchmark --model <M> --engine <E> --concurrency <C> \
    --duration 60s --out /shared/runs/capstone/teamX/configY/

# 4. Eval (interactive — open chat tab, run 10 prompts, record pass/fail)

# 5. Pull report
capsule storage get /shared/runs/capstone/teamX/configY/report.json ./teamX/configY/

# 6. Log it
```

## Time budget for today

| Block | Minutes |
|---|---|
| Deploy + first run + sanity check | 60 |
| Benchmark sweep (per config × N configs) | 150 |
| Interactive eval | 90 |
| Documentation cleanup + log finalization | 30 |

If a config blows up, **don't debug forever** — note it, move on, come back if time. The deliverable rewards evidence, not perfection.

## When you're stuck

- "Model won't load" → memory math (Week 3 Day 12); maybe wrong GPU or wrong quant.
- "Benchmark stalls at 0 RPS" → engine config; check `stdout.log`.
- "Numbers don't match yesterday" → confound (Day 42); check warmup, neighbor processes, thermal.
- "Eval is subjective" → write the criterion down *before* you grade; have a teammate grade independently.

## Wrap-up

End of Day 48: every team has at least 2 configs benchmarked + evaluated with full logs. The recommendation writes itself if today's data is clean.

## Self-check before Day 49

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-10-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 48 · Execute">
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
    "explain": "The 8-field execution log: (1) config (model + quant + TP + PP), (2) node-ID, (3) exact command run, (4) start time, (5) end time, (6) outcome (success/OOM/timeout/error), (7) report-path in shared storage, (8) eval pass/fail with notes. Every field must be filled — 'no log = run didn't happen.'"
  },
  {
    "stem": "Why is 'no log = run didn't happen' such an important principle?",
    "options": [
      "It is a grading rule — unlogged runs receive zero credit",
      "Memory is unreliable — without a log, you can't reproduce what you did, can't report exact results, and can't defend your recommendation on Day 50 under Q&A",
      "Logs are required for the benchmark to run correctly",
      "It prevents duplicate runs by checking if a run already exists"
    ],
    "answer": 1,
    "explain": "The lesson says: 'No execution log means the run didn't happen.' Memory is unreliable for exact commands, exact node-IDs, and exact error messages. Panel reviewers on Day 50 will ask 'what was your exact command?' and 'what error did config B throw?' You need the log to answer precisely. Unlogged runs can't be defended."
  },
  {
    "stem": "When a config blows up (OOM error, timeout, model fails to load), what should you do?",
    "options": [
      "Immediately restart and retry the same config until it works",
      "Note the failure in the log (config, error, outcome), move on to the next config, and come back if time permits — don't let one failure consume the execution day",
      "Skip that config and pretend it wasn't planned",
      "Request a different GPU and restart from the beginning"
    ],
    "answer": 1,
    "explain": "The lesson's execution advice: 'Note the failure, move on.' Record what happened (OOM at batch size 32, FP16 runs out of memory at 70B). A logged failure is a data point. Move to the next config. If you have time at the end, come back to the failed one. Don't let one bad run turn a 4-config plan into a 1-config day."
  },
  {
    "stem": "Why must run artifacts go in stable named directories (not /tmp)?",
    "options": [
      "/tmp is read-only and cannot store benchmark artifacts",
      "/tmp is cleared on node reboot or release — artifacts in /tmp disappear when the node is gone; stable named paths in shared storage persist for analysis on Day 49",
      "Stable directories are faster for writing large files",
      "The benchmark tool only writes to /shared/ paths"
    ],
    "answer": 1,
    "explain": "Node-local /tmp is ephemeral — it disappears with the node. Your Day 48 run artifacts must survive to Day 49 analysis. Store in `/shared/runs/<YYYY-MM-DD-HHMM>-<label>/`. The lesson's rule: 'stable named directories in shared storage, not /tmp, not ~/, not anywhere ephemeral.'"
  },
  {
    "stem": "What does the interactive eval on Day 48 add that the benchmark run alone doesn't provide?",
    "options": [
      "Lower latency numbers",
      "Human-verified quality judgment per config — the 10-prompt suite with binary pass/fail tells you which config gives correct, well-formatted, on-topic answers, not just which is fastest",
      "More concurrency levels for the throughput curve",
      "Confirmation that the GPU hardware is working correctly"
    ],
    "answer": 1,
    "explain": "The benchmark measures speed (TTFT, throughput). The interactive eval measures quality (does it answer correctly, in the right format, without hallucinating). Day 48 does both: benchmark ALL charter configs (latency data), then run the 10-prompt eval suite against each (quality data). Both datasets are required for the Day 49 recommendation."
  },
  {
    "stem": "What should the 'outcome' field in the execution log capture?",
    "options": [
      "Only 'success' or 'failure' with no further detail",
      "The specific result: success, OOM (out of memory), timeout, model failed to load, partial (ran but numbers look wrong) — with enough detail to diagnose without re-running",
      "The number of tokens generated per second",
      "The cost in GPU-hours for the run"
    ],
    "answer": 1,
    "explain": "The outcome field is your post-mortem in the log. 'Failure' tells you nothing when reviewing on Day 49. 'OOM at batch size 32, FP16, 70B model' tells you exactly what to adjust. 'Timeout after 8 minutes, benchmark never produced output' tells you the serving engine crashed. Specific outcomes make the log diagnostic, not just a record that something ran."
  },
  {
    "stem": "With 30 minutes left in Day 48 and one charter config still not benchmarked, what is the correct action?",
    "options": [
      "Skip the config entirely and don't mention it in the analysis",
      "Rush through a partial benchmark run and accept incomplete numbers",
      "Run the benchmark if it fits in 30 minutes; if not, log it as 'not run — time constraint' in the execution log with a note on what you'd expect and why",
      "Ask the instructor for an extension before attempting the run"
    ],
    "answer": 2,
    "explain": "The lesson's execution advice: 'note what didn't happen.' A logged 'not run — time constraint' entry is honest and useful for Day 49 analysis. You can still make a recommendation from the configs you did run, noting the gap. A rushed partial run with bad numbers is worse than a clean 'not run' entry — it introduces noise you have to explain on Day 50."
  }
]
</script>
</div>

- [ ] At least 2 configs benchmarked with full execution logs (no TBD fields)
- [ ] Interactive eval completed for each config (pass/fail per prompt recorded)
- [ ] Run results in stable named directories (not `/tmp`)
- [ ] You can answer: "What surprised you?" with a specific observation

## Stuck?

Ask **oxtutor** — the debugging hints table (model won't load, benchmark stalls, numbers don't match) should unblock you in < 5 minutes if you share the exact error.
