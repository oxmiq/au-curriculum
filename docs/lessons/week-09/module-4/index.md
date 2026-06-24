---
drift: |
  Originally Day 44 of the former Capsule wk9. Now Day 45 of the new week
  (week-09/module-4), unchanged in scope. The Week-7 reference in the lesson body now
  points to Week 6 (agents) under the new architecture; copy edits welcome. Source-material
  link paths bumped one level deeper.
---

# Day 45 · Scheduling & MCP

> **Concept of the day:** stop running benchmarks by hand. **Schedule** them nightly with `capsule schedule`. Expose Capsule's surface via **MCP** so the agents you designed in Week 6 can run, monitor, and report on benchmarks autonomously. This is where Phase 2 (agents) and Phase 3 (Capsule) compose.<br>
> **Pre-reading:** Lab Guide **Module 10** (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 — Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 45 · Scheduling & MCP</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-09/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: capsule schedule | 25 min |
| Part 3 | Core Concepts: MCP for Capsule | 20 min |
| Part 4 | Deep Dive: Phase 1 + 2 + 3 Composition | 20 min |
| Part 5 | Hands-On: Create & Monitor a Schedule | 35 min |
| Part 6 | Hands-On: Sketch the Nightly Agent | 20 min |
| Part 7 | Wrap-up & Connection | 10 min |

**Total: ~145 min**

---

## Part 1 — Pre-Reading Review · 15 min

### Reading — Why this matters

Manual benchmarks don't catch regressions. A scheduled nightly sweep does. And once you've got scheduling, the next step is letting an agent *react* to the results — file an issue when a regression appears, re-run with new params, summarize the trend. This day knits together everything you've built.

### Exercise: Self-Check

Answer before reading on:

1. What's the difference between `capsule benchmark` and `capsule schedule`?
2. Why is nightly benchmarking the minimum useful cadence for catching regressions?
3. What's MCP? (recall Week 6 Day 28)
4. Name three tools a benchmark-running agent would need.
5. What audit trail does a scheduled run produce?

---

## Part 2 — Core Concepts: capsule schedule · 25 min

### Reading — The cron of Capsule

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

### Reading — Reading the schedule status

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

### Exercise: Schedule Design

1. Write the `capsule schedule create` command for a sweep that runs every day at 03:00 UTC on any available T4 node, benchmarks `Qwen2.5-7B-Instruct` at concurrency 4, duration 60s.
2. What happens if no T4 node is available at 03:00? (Check the docs or make a reasonable assumption.)
3. Write the command to disable this schedule.

---

## Part 3 — Core Concepts: MCP for Capsule · 20 min

### Reading — Week 6 closing the loop

Recall Week 6 Day 28: **MCP** lets any compatible agent host (Claude Desktop, OxCode, Cursor) call your tool surface.

Capsule exposes an MCP server. Conceptually it provides tools like:

| Tool | Type | Purpose |
|---|---|---|
| `capsule_list_nodes` | read | Discover available capacity |
| `capsule_benchmark_run` | write | Kick off a benchmark on a leased node |
| `capsule_results_get` | read | Pull `report.json` |
| `capsule_schedule_list` | read | Inspect scheduled runs |
| `capsule_lease` / `capsule_release` | write | Lease management |

An agent designed in Week 6 (planner-worker, governance layer, audit) can now:

> "Every morning at 09:00, compare last night's benchmark against the 7-day baseline. If TTFT p99 regressed >15%, file a GitHub issue with the diff and the run links."

That's a fully realized Phase 1 + 2 + 3 product.

### Reading — What governance applies (Week 6 Day 29 recap)

Because some of the MCP tools are *write* (lease, benchmark-run = consumes GPU time), the agent needs:

| Control | Why |
|---|---|
| Lease-time cap | Agent can't reserve a node forever |
| Cost budget | Agent's nightly burn must be bounded |
| Approval gate for new schedules | Don't let the agent self-propagate cron jobs |
| Audit log piped to humans | Weekly review |
| Least-privilege creds | Agent token scoped to one env, read+benchmark only |

### Exercise: Tool Classification

For each MCP tool listed in the table above, classify it:

1. Read or write?
2. Does it require a governance control? If yes, what?
3. Could a malicious agent abuse it without the governance control? How?

---

## Part 4 — Deep Dive: Phase 1 + 2 + 3 Composition · 20 min

### Reading — The full picture

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

### Exercise: Map Your 5-Layer Agent

Using the 5-layer map from Week 6 Day 31, design the "nightly regression-watching agent" (no code, just the map):

| Layer | What goes here for the nightly agent? |
|---|---|
| 1 · Goal / Task definition | |
| 2 · Planner | |
| 3 · Tools (read + write) | |
| 4 · Governance controls | |
| 5 · Orchestration pattern | |

---

## Part 5 — Hands-On: Create & Monitor a Schedule · 35 min

### Exercise: Test Schedule Lifecycle

1. (5 min) Create a test schedule that runs at the shortest allowable cadence (e.g. every 15 minutes) on a small benchmark.
2. (10 min) Wait for the next run. Watch it trigger in `capsule schedule runs`.
3. (10 min) Inspect the run log. Trace the full lifecycle: scheduler → lease → node → benchmark → output.
4. (5 min) Disable the test schedule.
5. (5 min) Pull the output from the run. Verify it matches what `capsule benchmark` would produce directly.

---

## Part 6 — Hands-On: Sketch the Nightly Agent · 20 min

### Exercise: Nightly Agent Blueprint

1. Expand your 5-layer map from Part 4 into a complete written plan (bullets, not code):
   - What does the planner decide each morning?
   - What tools does it call, in what order?
   - What's the condition that triggers a GitHub issue?
   - What's the condition that triggers a re-run?
   - What's in the audit log?
2. Pair: present to a partner. They find one hole. You fix it.

---

## Part 7 — Wrap-up & Connection · 10 min

### Self-check

- [ ] I created a test schedule, confirmed it ran, and disabled it
- [ ] I can trace the full schedule lifecycle from trigger to output
- [ ] I can identify the MCP tools for Capsule and classify them as read/write
- [ ] I have a complete 5-layer agent blueprint for the nightly regression watcher
- [ ] I understand how Phase 1, 2, and 3 compose into a real product

### Connect forward

Friday: **timed sprint** + [the canonical quiz](knowledge-check.html). Cold-run the full benchmark workflow in 20 min. The capstone begins Monday.

---

## Pre-read for Friday (Day 46 · Timed Sprint + Phase 3 wrap)

- **Resource:** Problem Sets § Set 45 (sprint protocol + phase-timing rubric) + Flashcards command-recall tier.
- **Reflection questions:**
  1. What's your personal sequence: lease → connect → ??? → record?
  2. Which command did you forget the most this week?
  3. Where would you be slowest in a cold-start, and how do you fix that overnight?

---

## Stuck?

Ask **oxtutor** — share your 5-layer agent blueprint and it can identify governance gaps before you encounter them in the capstone.
