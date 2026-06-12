# Day 48 · Execute

> **Concept of the day:** today the charter becomes data. Deploy your chosen model on Capsule, run the benchmark sweep, run the interactive eval. Document obsessively — Day 49 cannot reconstruct what Day 48 forgot to write down.
> **Source template:** [Day-47 Execution Checklist](../../../../planning/source-material/Capstone/Day-47-Execution-Checklist.md) (source filename is `Day-47-...` from upstream capstone-relative naming; this is program Day 48).

---

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
