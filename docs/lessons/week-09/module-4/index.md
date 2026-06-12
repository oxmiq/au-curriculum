---
drift: |
  Originally Day 44 of the former Capsule wk9. Now Day 45 of the new week
  (week-09/module-4), unchanged in scope. The Week-7 reference in the lesson body now
  points to Week 6 (agents) under the new architecture; copy edits welcome. Source-material
  link paths bumped one level deeper.
---

# Day 45 · Scheduling & MCP

> **Concept of the day:** stop running benchmarks by hand. **Schedule** them nightly with `capsule schedule`. Expose Capsule's surface via **MCP** so the agents you designed in Week 6 can run, monitor, and report on benchmarks autonomously. This is where Phase 2 (agents) and Phase 3 (Capsule) compose.
> **Pre-reading:** Lab Guide **Module 10** (~15 min).
> **Source:** [Lab Guide Module 10](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md).

---

## Why this matters

Manual benchmarks don't catch regressions. A scheduled nightly sweep does. And once you've got scheduling, the next step is letting an agent *react* to the results — file an issue when a regression appears, re-run with new params, summarize the trend. This day knits together everything you've built.

## Readiness check

1. What's the difference between `capsule benchmark` and `capsule schedule`?
2. Why is nightly benchmarking the minimum useful cadence for catching regressions?
3. What's MCP (recall Week 7 Day 32)?
4. Name three tools a benchmark-running agent would need.
5. What audit trail does a scheduled run produce?

## Core concept

### Scheduling — the cron of Capsule

```
capsule schedule create \
  --name nightly-llama8b-h100 \
  --cron '0 2 * * *' \
  --env production \
  --filter '--gpu h100 --min-gpus 1' \
  --command 'capsule benchmark --model meta-llama/Llama-3.1-8B-Instruct --engine vllm --concurrency 8 --duration 60s --out /shared/runs/nightly/$(date +%F)/'
```

What this does:

1. Every night at 02:00 UTC, the scheduler picks an available H100 node from production.
2. Runs the benchmark with your config.
3. Writes results to `/shared/runs/nightly/<date>/`.
4. Logs the entire run + outcome.
5. Releases the lease.

**No human required.** Comes free with an audit trail.

### Reading the schedule status

```
capsule schedule list                              # all your schedules
capsule schedule show nightly-llama8b-h100         # details + last 10 runs
capsule schedule runs nightly-llama8b-h100         # history with outcomes
capsule schedule disable nightly-llama8b-h100      # pause
```

Each run logs:

| Field | Example |
|---|---|
| Started at | `2025-09-15 02:00 UTC` |
| Node | `nv-h100-04-1` |
| Status | `success` / `failed` / `timed-out` |
| Duration | `4m 32s` |
| Outputs | `/shared/runs/nightly/2025-09-15/` |

### MCP for Capsule — Week 7 closing the loop

Recall Week 7 Day 32: **MCP** lets any compatible agent host (Claude Desktop, OxCode, Cursor) call your tool surface.

Capsule exposes (or will expose) an MCP server. Conceptually it provides tools like:

| Tool | Type | Purpose |
|---|---|---|
| `capsule_list_nodes` | read | Discover available capacity |
| `capsule_benchmark_run` | write | Kick off a benchmark on a leased node |
| `capsule_results_get` | read | Pull `report.json` |
| `capsule_schedule_list` | read | Inspect scheduled runs |
| `capsule_lease` / `capsule_release` | write | Lease management |

An agent designed in Week 7 (planner-worker, governance layer, audit) can now:

> "Every morning at 09:00, compare last night's benchmark against the 7-day baseline. If TTFT p99 regressed >15%, file a GitHub issue with the diff and the run links."

That's a fully realized Phase 1 + 2 + 3 product. **You have the design vocabulary from Week 7's 5-layer map and the operational primitives from Weeks 8–9 — you could build it.**

### What governance applies (Week 7 Day 33 recap)

Because some of the MCP tools are *write* (lease, benchmark-run = consumes GPU time), the agent needs:

| Control | Why |
|---|---|
| Lease-time cap | Agent can't reserve a node forever |
| Cost budget | Agent's nightly burn must be bounded |
| Approval gate for new schedules | Don't let the agent self-propagate cron jobs |
| Audit log piped to humans | Weekly review |
| Least-privilege creds | Agent token scoped to one env, read+benchmark only |

This is the same 5-layer-map you designed in Week 7 — now grounded in actual tools you've used all week.

### Phase 1 ↔ Phase 2 ↔ Phase 3 — the full picture

```
Phase 1 (Weeks 1–5)    Phase 2 (Weeks 6–7)        Phase 3 (Weeks 8–10)
─────────────────       ─────────────────          ─────────────────
metrics, batching,      prompts + agents +         Capsule fleet +
quant, TP, eval         tools + governance         benchmarks + MCP
        │                       │                          │
        └───────────┬───────────┴──────────┬───────────────┘
                    ▼                      ▼
            "I can defend a       "An agent runs my
            benchmark result"     benchmarks for me"
```

Tomorrow's Friday consolidation is a **timed sprint** — find machine → benchmark → evaluate → record — in 20 minutes. Cold. The capstone follows on Monday.

## Practice (90 min)

1. (15 min) Create a *test* schedule that runs every 15 min (use shortest allowable cadence) of a tiny benchmark. Verify the next run lands.
2. (15 min) Inspect the run log. Trace: scheduler → lease → node → benchmark → output. Disable the test schedule.
3. (20 min) Read the MCP surface docs for Capsule (or stub from Module 10). Identify which tools are read vs write.
4. (25 min) Sketch (no code) the 5-layer-map for "nightly regression-watching agent" — reuse your Week 7 template. Identify each tool, governance control, and the orchestration pattern.
5. (15 min) Pair: present the sketch to a partner. Find one hole. Fix it.

## Wrap-up

Cohort can articulate how Phases 1, 2, 3 compose into a real product. Schedule + MCP demystified.

## Connect forward

Friday: **timed sprint** + [the canonical quiz](knowledge-check.html). Cold-run the full benchmark workflow in 20 min. The capstone begins Monday.

---

## Pre-read for Friday (Day 45 · Timed Sprint + Phase 3 wrap)

- **Resource:** Problem Sets § Set 45 (sprint protocol + phase-timing rubric) + Flashcards command-recall tier.
- **Reflection questions:**
  1. What's your personal sequence: lease → connect → ??? → record?
  2. Which command did you forget the most this week?
  3. Where would you be slowest in a cold-start, and how do you fix that overnight?
