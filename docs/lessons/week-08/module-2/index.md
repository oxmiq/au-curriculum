---
drift: |
  Authored as a combined "Files + Storage + Streaming" day (former wk8 day 39). New graph
  splits this into two consecutive modules: week-08/module-2 (Files & Storage) and
  week-08/module-3 (Streaming). For now this lesson covers BOTH concepts in a single page;
  module-3 is a redirect stub pointing to the streaming section below. Future authoring
  should extract the streaming material into its own page.
---

# Day 38 · Files & Storage (with streaming primer)

> **Concept of the day:** **`capsule cp`** for small files. **Shared storage pool** for big artifacts (models, datasets, results). **Streaming output** (`capsule run --stream`) for live logs without scraping after-the-fact. Per-user home is fast but ephemeral relative to the cluster lifecycle.
> **Pre-reading:** Lab Guide **Modules 6 + 7** (~30 min).
> **Source:** [Lab Guide Modules 6 + 7](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md). The streaming portion of this lesson is *also* the source for the next module ([Day 39 · Streaming](../module-3/index.md)).

---

## Why this matters

This is the most-used set of operations in daily life on Capsule. Pick the wrong tool — copy a 50 GB checkpoint with `cp` instead of using shared storage, or scrape logs after the fact instead of streaming — and you waste hours. Pick right and you have an enjoyable benchmarking rhythm.

## Readiness check

1. Which tool for a 50 MB Python script: `capsule cp` or shared storage?
2. Which tool for a 50 GB model checkpoint?
3. What's the difference between per-user home dir and the shared storage pool?
4. Why stream benchmark output instead of `tail -f`-ing a log after disconnect?
5. What command runs a one-off remote command and streams its stdout to your laptop?

## Core concept

### File transfer commands

| Command | When |
|---|---|
| `capsule cp ./local.py <node>:./remote.py` | Small files, scripts, configs |
| `capsule cp <node>:./results.json ./` | Pull a single artifact |
| `capsule cp -r ./mydir <node>:./` | Recursive (modest size) |
| `capsule storage put ./big.bin /shared/models/` | Large files → shared pool |
| `capsule storage get /shared/results/run-42 ./` | Pull from shared pool |
| `capsule storage ls /shared/models` | List shared pool |

### Per-user home vs shared storage

| Property | `$HOME` on node | Shared storage `/shared/...` |
|---|---|---|
| Speed | Local NVMe, fastest | Networked, slower |
| Lifetime | Lease-bound or longer (env-dependent) | Cluster-bound, durable |
| Quota | Small (10–50 GB) | Large (TB+) |
| Visibility | This node only | All nodes in env |
| Use for | Source code, venvs, scratch | Models, datasets, results, anything you want to keep |

> **Rule:** if losing this on a node reboot would hurt, put it in shared.

### Why shared storage matters

A 70B FP16 model = 140 GB. Copying that with `capsule cp` over your laptop's network? **Take a break, see you in 3 hours.** Pre-staging into shared once, then mounting on any node? **Seconds.**

The Week 9 benchmark workflow:

1. Models live in `/shared/models/` (pre-staged once, by the platform team or you).
2. Each benchmark run lives in `/shared/runs/<date>-<config>/`.
3. Your laptop never moves model bytes — only the run reports.

### Streaming — see logs live

```
capsule run <node> --stream -- ./run_benchmark.sh
```

vs the wrong way:

```
capsule connect <node>
nohup ./run_benchmark.sh > /tmp/out.log 2>&1 &
exit                                          # connection drops
# 4 hours later...
capsule connect <node>
tail -f /tmp/out.log                          # too late to react
```

With `--stream`, you see output in real time and can Ctrl-C to abort if you spot an obvious failure 30 seconds in. Don't waste GPU-hours on a typo'd config.

### The full daily file workflow

```
# Once, pre-stage:
capsule storage put llama-3-70b-fp8.tar /shared/models/

# Each benchmark session:
capsule node lease --gpu h100 --min-gpus 8 --duration 4h
capsule cp ./benchmark.yaml <node>:./
capsule run <node> --stream -- ./run.sh ./benchmark.yaml /shared/runs/$(date +%F)/
capsule storage get /shared/runs/$(date +%F)/report.json ./
capsule lease release
```

That's the rhythm. Memorize it.

### Etiquette

- Clean up your `/shared/runs/<old>` directories monthly.
- Don't put junk in `/shared/models/`.
- Don't `chmod 777 -R` shared storage out of frustration — ask for the right group.
- Log your large operations (uploads / deletes) — it's polite.

## Practice (90 min)

1. (15 min) Copy a small file (a config you wrote) to your dev node and back. Time it.
2. (15 min) Run `capsule storage ls /shared/`. Note what's pre-staged. Read one or two `README`s if present.
3. (25 min) Run a small benchmark (or any long command — e.g. `seq 1 10 | xargs -I{} sleep 1`) with `--stream`. Verify you can Ctrl-C cleanly.
4. (25 min) Pair: design a daily file workflow for your Week 9 benchmark plan. Map each artifact (config, model, results, report) to the right storage.
5. (10 min) Write your personal "files cheat sheet."

## Wrap-up

Cohort agrees on the storage convention for Week 9 runs.

## Connect forward

Friday: **reliability & diagnostics** — known quirks, how to diagnose breakages, how to file a bug report that gets fixed. Then **[the canonical quiz](knowledge-check.html)**.

---

## Pre-read for Friday (Day 40 · Reliability & Diagnostics)

- **Resource:** Lab Guide **Module 10 known-quirks table** + Glossary (~10 min).
- **Reflection questions:**
  1. What's the diagnostic sequence when a node "doesn't connect"?
  2. What's the diagnostic sequence when a GPU "isn't seen" by your container?
  3. What information must a good bug report contain?
