---
drift: |
  Originally Day 44 of the former Capsule wk9. Now Day 45 of the new week
  (week-09/module-4), unchanged in scope. The Week-7 reference in the lesson body now
  points to Week 6 (agents) under the new architecture; copy edits welcome. Source-material
  link paths bumped one level deeper.
---

# Day 45 · Scheduling & MCP

> **Concept of the day:** stop running benchmarks by hand. **Schedule** them nightly with `capsule schedule`. Expose Capsule's surface via **MCP** so the agents you designed in Week 6 can run, monitor, and report on benchmarks autonomously. This is where Phase 2 (agents) and Phase 3 (Capsule) compose.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#day-44-scheduling-mcp">Capsule Power-User Pre-Lecture Reading — Day 44 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-10-scheduled-jobs-agents-and-the-reliability-toolkit">Capsule Lab Guide</a> Module 10.

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
    {status:week-09/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: capsule schedule |
| Part 3 | Core Concepts: MCP for Capsule |
| Part 4 | Deep Dive: Phase 1 + 2 + 3 Composition |
| Part 5 | Hands-On: Create & Monitor a Schedule |
| Part 6 | Hands-On: Sketch the Nightly Agent |
| Part 7 | Wrap-up & Connection |

**Total: ~145 min**

---

## Part 1 — Pre-Reading Review

### Reading — Why this matters

Manual benchmarks don't catch regressions. A scheduled nightly sweep does. And once you've got scheduling, the next step is letting an agent *react* to the results — file an issue when a regression appears, re-run with new params, summarize the trend. This day knits together everything you've built.

### Exercise: Self-Check

Answer before reading on:

1. What's the difference between `capsule benchmark` and `capsule schedule`?
2. Why is nightly benchmarking the minimum useful cadence for catching regressions?
3. What's MCP? (recall Week 6 Day 28)
4. Name three tools a benchmark-running agent would need.
5. What audit trail does a scheduled run produce?

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m4-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 10">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the key difference between `capsule benchmark` and `capsule schedule`?",
    "options": [
      "capsule benchmark is for GPU nodes; capsule schedule is for CPU nodes",
      "capsule benchmark runs once manually; capsule schedule runs benchmarks automatically on a cron-style schedule",
      "capsule schedule is just an alias for capsule benchmark --repeat",
      "capsule benchmark measures quality; capsule schedule measures performance"
    ],
    "answer": 1,
    "explain": "'capsule benchmark' is a one-off manual run. 'capsule schedule create' sets up a recurring job using cron syntax (e.g., '0 2 * * *' for 2am nightly). The schedule auto-leases a node matching your filter, runs the command, and releases the lease."
  },
  {
    "stem": "Why is nightly benchmarking the MINIMUM useful cadence for catching regressions?",
    "options": [
      "Because benchmarks take 24 hours to complete",
      "Because hardware changes only happen daily",
      "A nightly sweep catches regressions within one day — before anyone ships a new config to production based on stale results",
      "Because capsule schedule only supports daily cron jobs"
    ],
    "answer": 2,
    "explain": "If you only benchmark weekly, a regression introduced on Monday isn't caught until the weekend — by then it may have reached production or influenced other decisions. Nightly means you know within 24 hours if a config change, engine update, or node health issue changed your numbers."
  },
  {
    "stem": "What is MCP in the context of AI agents? (Recall Week 6 Day 28)",
    "options": [
      "Model Control Protocol — a way to fine-tune models remotely",
      "Model Context Protocol — a standard for exposing tools and data sources to AI agents",
      "Multi-Core Processing — a GPU scheduling technique",
      "Managed Container Platform — a Capsule deployment feature"
    ],
    "answer": 1,
    "explain": "MCP (Model Context Protocol) is a standard for exposing tools and data sources to AI agents. When Capsule exposes an MCP surface, agents can call Capsule commands (lease, benchmark, schedule) as tools — enabling autonomous benchmark agents."
  },
  {
    "stem": "Which three tools would a benchmark-running Capsule agent minimally need?",
    "options": [
      "read_file, write_file, execute_shell",
      "lease_node, run_benchmark, read_results (or equivalents that map to capsule lease, capsule benchmark, capsule storage get)",
      "create_schedule, delete_schedule, list_schedules",
      "get_gpu_info, set_quantization, deploy_model"
    ],
    "answer": 1,
    "explain": "An autonomous benchmark agent needs to: (1) lease a node (or verify a schedule ran), (2) run or trigger a benchmark, (3) read the results. These three tools map to 'capsule lease', 'capsule benchmark' (or checking schedule output), and 'capsule storage get'. Additional tools for filing issues or sending notifications are optional."
  },
  {
    "stem": "What audit trail does a scheduled capsule benchmark run produce?",
    "options": [
      "Only a log entry in ~/.capsule/logs/",
      "report.json, stdout.log, and config.yaml written to the configured --out directory, timestamped per run",
      "A Git commit with the results",
      "A Slack notification only"
    ],
    "answer": 1,
    "explain": "Each scheduled run writes report.json, stdout.log, and config.yaml to the --out directory, with the date embedded in the path (e.g., /shared/runs/nightly/2026-06-27/). This creates a time-series of results you can diff, plot, and alert on — the foundation of regression detection."
  },
  {
    "stem": "What does the `--filter` flag in `capsule schedule create` do?",
    "options": [
      "Filters which metrics to include in the report",
      "Specifies node requirements (GPU type, minimum GPUs) so the scheduler picks the right hardware automatically",
      "Filters which benchmark prompts to use",
      "Limits the schedule to specific hours of the day"
    ],
    "answer": 1,
    "explain": "'--filter' passes node selection criteria to the scheduler so it automatically leases the right hardware. For example, '--gpu h100 --min-gpus 1' ensures the benchmark always runs on an H100. This means you don't need to manually find and lease a node for each nightly run."
  },
  {
    "stem": "How does Phase 2 (agents from Week 6) compose with Phase 3 (Capsule benchmarking) on Day 45?",
    "options": [
      "They don't compose — agents and benchmarking are separate concerns",
      "An agent can use Capsule's MCP surface to autonomously run benchmarks, read results, and react — e.g., file a regression issue or re-run with different params",
      "Phase 2 agents can only read benchmark results, not trigger new runs",
      "Composition requires a separate orchestration service outside Capsule"
    ],
    "answer": 1,
    "explain": "Day 45 is where phases compose: a Week-6 agent (Phase 2) uses Capsule's MCP tools (Phase 3) to autonomously lease, benchmark, read results, and react. Example: nightly regression detected → agent files a GitHub issue with the delta and re-runs with the previous config to confirm."
  },
  {
    "stem": "What cron expression schedules a job at 2am every night?",
    "options": [
      "2 0 * * *",
      "0 2 * * *",
      "* * 2 * *",
      "0 0 2 * *"
    ],
    "answer": 1,
    "explain": "Cron format is: minute hour day-of-month month day-of-week. '0 2 * * *' means minute=0, hour=2, every day. So: 2:00am nightly. The first field is minutes (0–59), the second is hours (0–23)."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: capsule schedule

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

## Part 3 — Core Concepts: MCP for Capsule

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

## Part 4 — Deep Dive: Phase 1 + 2 + 3 Composition

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

## Part 5 — Hands-On: Create & Monitor a Schedule

### Exercise: Test Schedule Lifecycle

1. Create a test schedule that runs at the shortest allowable cadence (e.g. every 15 minutes) on a small benchmark.
2. Wait for the next run. Watch it trigger in `capsule schedule runs`.
3. Inspect the run log. Trace the full lifecycle: scheduler → lease → node → benchmark → output.
4. Disable the test schedule.
5. Pull the output from the run. Verify it matches what `capsule benchmark` would produce directly.

---

## Part 6 — Hands-On: Sketch the Nightly Agent

### Exercise: Nightly Agent Blueprint

1. Expand your 5-layer map from Part 4 into a complete written plan (bullets, not code):
   - What does the planner decide each morning?
   - What tools does it call, in what order?
   - What's the condition that triggers a GitHub issue?
   - What's the condition that triggers a re-run?
   - What's in the audit log?
2. Pair: present to a partner. They find one hole. You fix it.

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 45 · Scheduling &amp; MCP">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Why schedule benchmarks instead of running them manually?",
    "options": [
      "Scheduled benchmarks always produce better results than manual ones",
      "Scheduling enables consistent, automated, unattended runs at fixed intervals — catching regressions before they reach production users, without requiring manual attention",
      "Manual benchmarks cannot measure TTFT accurately",
      "Scheduling reduces GPU cost by running benchmarks at off-peak hours"
    ],
    "answer": 1,
    "explain": "Manual benchmarks are run only when someone remembers. Scheduled benchmarks run at defined intervals (nightly, weekly) and alert automatically on regression. A new model version that degrades P99 TTFT by 30% is caught by the scheduled run, not discovered by a user complaint. This is the core value of automated regression testing."
  },
  {
    "stem": "What does an MCP surface for Capsule unlock that the CLI alone cannot?",
    "options": [
      "Access to faster GPU hardware",
      "The ability for AI agents to programmatically trigger benchmarks, read results, lease machines, and respond to regressions — automation that was previously only possible via manual CLI use",
      "Encrypted communication with the control plane",
      "Support for more concurrency levels than the standard CLI"
    ],
    "answer": 1,
    "explain": "The Capsule MCP server exposes Capsule operations as MCP tools. An agent can call `lease_node`, `run_benchmark`, `get_report`, and `release_node` programmatically. The Week 6 agent you designed can now actually run benchmarks, read the results, and take action — capabilities that required human CLI use before."
  },
  {
    "stem": "Which Capsule MCP tools are 'write' tools requiring human-in-the-loop approval?",
    "options": [
      "All Capsule MCP tools are read-only",
      "Write tools include: lease_node (allocates a GPU), run_benchmark (executes a workload), release_node (deallocates) — these have side effects on real infrastructure",
      "Only tools that cost money require approval",
      "Write tools are not available in the MCP surface — only the CLI supports writes"
    ],
    "answer": 1,
    "explain": "From Day 28's safety rule: write tools must be wrapped in confirmation. Capsule MCP write tools include leasing (spends GPU-hours), running workloads (executes code on machines), and releasing (frees resources that others might be waiting for). Read tools like list_nodes and get_report are safe to call automatically."
  },
  {
    "stem": "What are the five layers of an agent blueprint for a nightly benchmark regression watcher?",
    "options": [
      "Database, API, Business Logic, UI, Auth",
      "Intelligence (model reasoning), Observation (benchmark results + history), Action (lease/run/release Capsule tools), Orchestration (schedule and trigger logic), Safety (approval gates for write actions)",
      "Cron job, script, HTTP client, data store, alerting",
      "Input, Processing, Output, Storage, Monitoring"
    ],
    "answer": 1,
    "explain": "The 5-layer agent stack applied to the benchmark watcher: Intelligence (LLM decides if regression is significant), Observation (reads current + historical benchmark results), Action (Capsule MCP tools: lease, run, release), Orchestration (nightly schedule, multi-step workflow), Safety (human approval before leasing, audit log of all actions)."
  },
  {
    "stem": "How do Phase 1, Phase 2, and Phase 3 compose into a real product?",
    "options": [
      "They are independent — each phase stands alone",
      "Phase 1 (inference fundamentals) explains why the benchmark numbers are what they are; Phase 2 (agents) provides the architecture to automate benchmarks and respond to them; Phase 3 (Capsule operations) provides the infrastructure to run them",
      "Phase 1 is theory; Phases 2 and 3 are practice with no connection to theory",
      "Phase 3 replaces Phases 1 and 2 — the operational knowledge supersedes the theoretical"
    ],
    "answer": 1,
    "explain": "The lesson synthesis: 'Phase 1 explains the numbers; Phase 2 provides the agent architecture; Phase 3 provides the infrastructure.' A nightly regression watcher uses: H100 bandwidth to explain TTFT (P1), a ReAct agent to interpret and respond to results (P2), and Capsule MCP tools to automate the execution (P3). All three phases are necessary."
  }
]
</script>
</div>

### Connect forward

Friday: **timed sprint** + [the canonical quiz](knowledge-check.md). Cold-run the full benchmark workflow in 20 min. The capstone begins Monday.

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
