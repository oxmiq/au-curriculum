---
drift: |
  Originally Day 44 of the former Capsule wk9. Now Day 44 of the new week
  (week-09/module-4), unchanged in scope. The Week-7 reference in the lesson body now
  points to Week 6 (agents) under the new architecture; copy edits welcome. Source-material
  link paths bumped one level deeper.
---

# Day 44 · Scheduling & MCP

> **Concept of the day:** stop babysitting benchmarks in an interactive terminal. Hand a long run to `capsule schedule` and it executes unattended on a remote node as a detached job; drive the *nightly* cadence from an external trigger (cron/CI). Expose Capsule's surface via **MCP** so the agents you designed in Week 6 can run, monitor, and report on benchmarks autonomously. This is where Phase 2 (agents) and Phase 3 (Capsule) compose.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#day-44-scheduling-mcp">Capsule Power-User Pre-Lecture Reading - Day 44 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-10-scheduled-jobs-agents-and-the-reliability-toolkit">Capsule Lab Guide</a> Module 10.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 - Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 44 · Scheduling & MCP</span>
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

## Part 1 - Pre-Reading Review

### Reading - Why this matters

Manual benchmarks don't catch regressions. A scheduled nightly sweep does. And once you've got scheduling, the next step is letting an agent *react* to the results: file an issue when a regression appears, re-run with new params, summarize the trend. This day knits together everything you've built.

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
    "stem": "What kind of tool is `capsule schedule`?",
    "options": [
      "A cron-style recurring scheduler: you register a command and it re-runs on a fixed calendar (e.g. `--cron '0 2 * * *'` for nightly).",
      "A job queue: you submit a long-running one-shot shell script that runs on a remote node as a detached daemon, without you holding an SSH session open.",
      "A calendar reservation system that books a GPU node for a future time slot.",
      "A wrapper that reruns `capsule benchmark` in a loop until you cancel it."
    ],
    "answer": 1,
    "explain": "`capsule schedule` is a batch job queue: jobs are queued, dispatched to an available node, and run as a detached (`setsid`) daemon that survives SSH/session teardown: the right tool for anything longer than a coffee break. It is NOT a cron/recurring scheduler; there is no `--cron` surface and jobs run once."
  },
  {
    "stem": "Which command submits a benchmark script to run on any machine in a pool?",
    "options": [
      "`capsule schedule create --cron '0 3 * * *' --command './eval.sh'`",
      "`capsule schedule submit ./eval.sh --pool <tag>`",
      "`capsule schedule start <tag> --script ./eval.sh`",
      "`capsule schedule run --filter '--gpu h100' ./eval.sh`"
    ],
    "answer": 2,
    "explain": "The real subcommand is `capsule schedule start <tag> --script <file>` (script is required, `-s` for short). With a config tag it does pool dispatch; the first available responder wins. There is no `create`/`submit`/`run` form, and no `--cron` or `--filter` on schedule."
  },
  {
    "stem": "A scheduled job has finished. How do you read its output?",
    "options": [
      "`capsule schedule logs <job-id>` (add `--tail N` for the last N lines).",
      "Open `report.json` in the `--out` directory you passed to `schedule create`.",
      "`capsule schedule show <job-id> --output` prints the captured stdout.",
      "It is committed to your repo automatically as `stdout.log`."
    ],
    "answer": 0,
    "explain": "The node streams `output.log` to Azure Blob Storage during the run (re-uploaded periodically), and you retrieve it with `capsule schedule logs <job-id>`, optionally `--tail N`. There is no `--out` audit directory and no `report.json`/`config.yaml` artifact set; that surface was fabricated."
  },
  {
    "stem": "Which flags does `capsule schedule start` accept to shape a job?",
    "options": [
      "`--cron`, `--filter`, `--out`",
      "`--gpu`, `--min-gpus`, `--vram`",
      "`--interval`, `--repeat`, `--calendar`",
      "`--name`, `--timeout`, `--retry`, `--env`, `--with-file`"
    ],
    "answer": 3,
    "explain": "Documented `schedule start` flags include `--name`/`-n` (label), `--timeout`/`-t` (max runtime, default 24h), `--retry` (max retries), `--env KEY=VAL` (repeatable), `--with-file` (companion file uploaded alongside the script), and `--machine-name` (target a specific box). `--cron`/`--filter`/`--out` do not exist on schedule."
  },
  {
    "stem": "How do you check the state of your queued and running scheduled jobs?",
    "options": [
      "`capsule schedule list` shows every schedule and its next cron fire time.",
      "`capsule schedule status` (filter with `--me`, `--state pending|running|completed|failed`, `--show-start`).",
      "`capsule schedule ps --watch` tails a live table of jobs.",
      "`capsule schedule runs <name>` prints the run history with outcomes."
    ],
    "answer": 1,
    "explain": "`capsule schedule status` lists jobs and their current state; you can filter by `--me`/`--user`, by `--state pending|running|completed|failed`, and add `--show-start` for an ETA on queued work. Jobs move PENDING -> RUNNING -> COMPLETED/FAILED/CANCELLED. There is no `schedule list` or `schedule runs` subcommand."
  },
  {
    "stem": "How do you stop a scheduled job you no longer need?",
    "options": [
      "`capsule schedule disable <name>` pauses the recurring schedule.",
      "Delete the entry from `~/.capsule/crontab`.",
      "`capsule schedule cancel <job-id>` (or `capsule schedule cancel --all`).",
      "You can't interrupt it; wait for `--timeout` to expire."
    ],
    "answer": 2,
    "explain": "Cancel by job id, or use `--all`. A pending job is simply marked Cancelled; for a running job the orchestration solicits the node by its NodeId and kills the process. There is nothing to 'disable' because a scheduled job is a one-shot, not a recurring cron entry."
  },
  {
    "stem": "What does `capsule mcp` do?",
    "options": [
      "Installs a Model Context Protocol server config into Claude Desktop / Claude Code so the assistant can drive Capsule (`--output` dumps the config without installing; `--uninstall` removes it).",
      "Starts a cron daemon that runs MCP-defined jobs on a schedule.",
      "Opens an interactive natural-language chat session with your fleet.",
      "Exports benchmark results in a Model Context Protocol file format."
    ],
    "answer": 0,
    "explain": "`capsule mcp` wires Capsule into MCP-capable assistants (Claude Desktop / Claude Code) so they can call Capsule actions as tools. MCP is the Model Context Protocol from Week 6. `--output` writes the config for inspection; `--uninstall` removes it."
  },
  {
    "stem": "What is `capsule agent`?",
    "options": [
      "A cron scheduler for autonomous benchmark reruns.",
      "The MCP server that Claude Desktop connects to.",
      "A local REST gateway that proxies `capsule benchmark`.",
      "A natural-language fleet-management agent (powered by Google ADK) that talks to an OpenAI-compatible endpoint and calls Capsule tools like `capsule_list`, `capsule_exec`, and `capsule_scp_upload`."
    ],
    "answer": 3,
    "explain": "`capsule agent` gives a natural-language surface over the fleet. It is built on Google ADK, requires `OXMIQ_AGENT_API_BASE`/`_API_KEY`/`_MODEL` pointing at any OpenAI-compatible endpoint, and exposes tools such as `capsule_list`, `capsule_filter`, `capsule_exec`, and `capsule_scp_upload`/`_download`. It explains its intent before running action tools."
  }
]
</script>
</div>

---

## Part 2 - Core Concepts: capsule schedule

### Reading - A job queue, not cron

`capsule schedule` is a **one-shot job queue**, not a cron daemon. You hand it a shell script; it queues the job, dispatches it to an available node, and runs it there as a detached daemon that survives SSH/session teardown. The job runs **once** and finishes; there is no `--cron`, no recurring calendar, no `create` subcommand.

Put your benchmark in a script, `nightly-bench.sh`:

```bash
#!/usr/bin/env bash
capsule benchmark <config-tag> meta-llama/Llama-3.1-8B-Instruct \
  --backend vllm --concurrency 8 --input-length 256 --output-length 256 --num-prompts 80
```

Then submit it:

```bash
capsule schedule start <config-tag> \
  --script ./nightly-bench.sh \
  --name nightly-llama8b-h100 \
  --timeout 4h
```

What this does:

1. Queues the job; the scheduler dispatches it to the first available node in the `<config-tag>` pool (use `--machine-name` to pin a specific box).
2. Runs `nightly-bench.sh` on that node as a detached daemon; your laptop can close.
3. Streams the job's `output.log` to storage as it runs; the benchmark itself uploads to the dashboard.
4. Records the job's state (PENDING → RUNNING → COMPLETED/FAILED) and keeps its logs.

**No SSH session required.** For a real *nightly* cadence, wrap `capsule schedule start` in your own cron entry or CI job; that external trigger is what recurs, not `capsule schedule`.

### Reading - Tracking a job

```
capsule schedule status                            # list your jobs + state
capsule schedule status --me --state running       # filter to your running jobs
capsule schedule logs <job-id>                     # fetch the job's output
capsule schedule logs <job-id> --tail 100          # just the last 100 lines
capsule schedule cancel <job-id>                   # stop a job (or --all)
```

`schedule status` reports each job and its current state:

| Field | Example |
|---|---|
| Job id | `a1b2c3d4-...` |
| Name | `nightly-llama8b-h100` |
| State | `PENDING` / `RUNNING` / `COMPLETED` / `FAILED` / `CANCELLED` |
| Node | `nv-h100-04-1` (set at dispatch) |

Output isn't written to a shared directory; the node streams `output.log` to storage during the run, and you read it back with `capsule schedule logs <job-id>`.

### Exercise: Schedule Design

1. Write a small `bench.sh` that benchmarks `Qwen/Qwen2.5-7B-Instruct` at concurrency 4, then the `capsule schedule start` command that submits it to any available T4 node with a name and a 1h timeout.
2. What happens if no T4 node is free when you submit? (Think about the PENDING state and how dispatch works.)
3. Write the command to cancel the job once you have its job id.

---

## Part 3 - Core Concepts: MCP for Capsule

### Reading - Week 6 closing the loop

Recall Week 6 Day 28: **MCP** lets any compatible agent host (Claude Desktop, OxCode, Cursor) call your tool surface.

Capsule exposes an MCP server that surfaces Capsule actions as tools. The Capsule agent (`capsule agent`, built on Google ADK) drives the same underlying tool set:

| Tool | Type | Purpose |
|---|---|---|
| `capsule_list` | read | Discover available machines / capacity |
| `capsule_filter` | read | Filter machines by vendor, VRAM, etc. |
| `capsule_exec` | write | Run a command on a machine (e.g. kick off a benchmark job) |
| `capsule_scp_upload` | write | Upload scripts or data to a machine |
| `capsule_scp_download` | read | Pull results back to your laptop |

An agent designed in Week 6 (planner-worker, governance layer, audit) can now:

> "Every morning at 09:00, compare last night's benchmark against the 7-day baseline. If TTFT p99 regressed >15%, file a GitHub issue with the diff and the run links."

That's a fully realized Phase 1 + 2 + 3 product.

### Reading - What governance applies (Week 6 Day 29 recap)

Because some of the Capsule tools are *write* (`capsule_exec` runs workloads, `capsule_scp_upload` writes files; both consume real resources), the agent needs:

| Control | Why |
|---|---|
| Session/runtime cap | Agent can't hold a node forever |
| Cost budget | Agent's nightly burn must be bounded |
| Approval gate for new jobs | Don't let the agent queue unbounded scheduled jobs |
| Audit log piped to humans | Weekly review |
| Least-privilege creds | Agent token scoped to one env, read+benchmark only |

### Exercise: Tool Classification

For each MCP tool listed in the table above, classify it:

1. Read or write?
2. Does it require a governance control? If yes, what?
3. Could a malicious agent abuse it without the governance control? How?

---

## Part 4 - Deep Dive: Phase 1 + 2 + 3 Composition

### Reading - The full picture

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

Tomorrow's Friday consolidation is a **timed sprint**, find machine → benchmark → evaluate → record, in 20 minutes. Cold. The capstone follows on Monday.

### Exercise: Map Your 5-Layer Agent

Using the 5-layer map from Week 6 Day 30, design the "nightly regression-watching agent" (no code, just the map):

| Layer | What goes here for the nightly agent? |
|---|---|
| 1 · Goal / Task definition | |
| 2 · Planner | |
| 3 · Tools (read + write) | |
| 4 · Governance controls | |
| 5 · Orchestration pattern | |

---

## Part 5 - Hands-On: Create & Monitor a Schedule

### Exercise: Test Job Lifecycle

1. Write a short script that runs a small `capsule benchmark`, and submit it with `capsule schedule start <config-tag> --script ./test.sh --name test-job --timeout 30m`.
2. Watch it move through states with `capsule schedule status --me`. Note the job id.
3. Tail the output with `capsule schedule logs <job-id> --tail 50`. Trace the full lifecycle: queue (PENDING) → dispatch → node (RUNNING) → benchmark → COMPLETED.
4. Submit a second test job and cancel it mid-run with `capsule schedule cancel <job-id>`; confirm it lands in CANCELLED.
5. Confirm the benchmark from your job shows up on the dashboard, just as a direct `capsule benchmark` run would.

---

## Part 6 - Hands-On: Sketch the Nightly Agent

### Exercise: Nightly Agent Blueprint

1. Expand your 5-layer map from Part 4 into a complete written plan (bullets, not code):
   - What does the planner decide each morning?
   - What tools does it call, in what order?
   - What's the condition that triggers a GitHub issue?
   - What's the condition that triggers a re-run?
   - What's in the audit log?
2. Pair: present to a partner. They find one hole. You fix it.

---

## Part 7 - Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 44 · Scheduling &amp; MCP">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Why hand a long benchmark to `capsule schedule` instead of running it in an interactive terminal?",
    "options": [
      "Scheduled jobs always produce better results than manual ones",
      "`capsule schedule` runs the job unattended on a remote node as a detached daemon; it survives SSH/session teardown, so a long run finishes without you holding a terminal open",
      "`capsule schedule` is a cron daemon that reruns the benchmark on a fixed calendar by itself",
      "Manual benchmarks cannot measure TTFT accurately"
    ],
    "answer": 1,
    "explain": "`capsule schedule` is a one-shot job queue: it dispatches your script to an available node and runs it as a detached (`setsid`) daemon that outlives your SSH session: ideal for anything longer than a coffee break. It does not recur on its own; a nightly cadence comes from an external trigger (cron/CI) that calls `capsule schedule start`. Automating the run is what lets a scheduled sweep catch a regression before a user does."
  },
  {
    "stem": "What does an MCP surface for Capsule unlock that the CLI alone cannot?",
    "options": [
      "Access to faster GPU hardware",
      "The ability for AI agents to call Capsule actions as tools, list and filter machines, run commands (e.g. kick off a benchmark job), move files, and act on results, automation that previously required a human at the CLI",
      "Encrypted communication with the control plane",
      "Support for more concurrency levels than the standard CLI"
    ],
    "answer": 1,
    "explain": "`capsule mcp` installs a Model Context Protocol config so an MCP-capable assistant (Claude Desktop / Claude Code) can call Capsule actions as tools: the same tool set `capsule agent` uses: `capsule_list`, `capsule_filter`, `capsule_exec`, `capsule_scp_upload`/`_download`. The Week 6 agent you designed can now discover machines, run a benchmark via `capsule_exec`, and pull results back: capabilities that required human CLI use before."
  },
  {
    "stem": "Which Capsule tools are 'write' tools that warrant human-in-the-loop approval?",
    "options": [
      "All Capsule tools are read-only",
      "The action tools with side effects: `capsule_exec` (runs a command / kicks off a workload on a machine) and `capsule_scp_upload` (writes files to a machine); the agent should confirm intent before calling them",
      "Only tools that cost money require approval",
      "Write tools are not available in the MCP surface; only the CLI supports writes"
    ],
    "answer": 1,
    "explain": "From Day 28's safety rule: action tools must be wrapped in confirmation. The Capsule agent even explains what it intends to do before calling `capsule_exec` or the `scp` tools. `capsule_exec` runs code on a machine and `capsule_scp_upload` writes files, both have real side effects, while read tools like `capsule_list` and `capsule_filter` are safe to call automatically."
  },
  {
    "stem": "In Part 4's '5-Layer Agent' map, which five layers do you fill in for the nightly regression-watching agent?",
    "options": [
      "Database, API, Business Logic, UI, Auth",
      "Intelligence, Observation, Action, Orchestration, Safety",
      "Goal / task definition, Planner, Tools (read + write), Governance controls, Orchestration pattern",
      "Input, Processing, Output, Storage, Monitoring"
    ],
    "answer": 2,
    "explain": "Part 4's map uses five layers: Goal / task definition (compare last night's run to the 7-day baseline), Planner (decide each morning whether a regression is significant), Tools: read + write (read tools like `capsule_list`/`capsule_filter` and `capsule_scp_download`; write tools like `capsule_exec`), Governance controls (session/cost caps, approval gate for new jobs, audit log, least-privilege creds), and the Orchestration pattern (an external nightly trigger driving the multi-step workflow). 'Intelligence/Observation/Action/Safety' is a different framing and is not this lesson's map."
  },
  {
    "stem": "How do Phase 1, Phase 2, and Phase 3 compose into a real product?",
    "options": [
      "They are independent; each phase stands alone",
      "Phase 1 (inference fundamentals) explains why the benchmark numbers are what they are; Phase 2 (agents) provides the architecture to automate benchmarks and respond to them; Phase 3 (Capsule operations) provides the infrastructure to run them",
      "Phase 1 is theory; Phases 2 and 3 are practice with no connection to theory",
      "Phase 3 replaces Phases 1 and 2; the operational knowledge supersedes the theoretical"
    ],
    "answer": 1,
    "explain": "The lesson synthesis: 'Phase 1 explains the numbers; Phase 2 provides the agent architecture; Phase 3 provides the infrastructure.' A nightly regression watcher uses: H100 bandwidth to explain TTFT (P1), a ReAct agent to interpret and respond to results (P2), and Capsule MCP tools to automate the execution (P3). All three phases are necessary."
  },
  {
    "stem": "Which command submits a benchmark script to a node pool as a one-shot detached job?",
    "options": [
      "`capsule schedule create --cron '0 2 * * *' --command ./bench.sh`",
      "`capsule schedule submit ./bench.sh --pool <config-tag>`",
      "`capsule schedule start <config-tag> --script ./bench.sh --name nightly --timeout 4h`",
      "`capsule benchmark schedule ./bench.sh --nightly`"
    ],
    "answer": 2,
    "explain": "The real form is `capsule schedule start <config-tag> --script <file>` (script required; `-n`/`--name`, `-t`/`--timeout` shape the job). With a config tag it dispatches to the first available node in the pool. `capsule schedule` is a one-shot job queue; there is no `create`, `submit`, or `--cron`; the recurring nightly cadence comes from an external cron/CI trigger that calls `schedule start`."
  },
  {
    "stem": "A scheduled job is still running and you no longer need it. How do you stop it?",
    "options": [
      "`capsule schedule cancel <job-id>` (or `--all`); a pending job is marked Cancelled; a running job is killed on its node",
      "`capsule schedule disable <name>` to pause the recurring schedule",
      "Delete the entry from `~/.capsule/crontab`",
      "You can't interrupt it; wait for `--timeout` to expire"
    ],
    "answer": 0,
    "explain": "`capsule schedule cancel <job-id>` stops a job, and `--all` cancels every one; the orchestration solicits the node and kills the process for a running job. There is nothing to 'disable' and no crontab, because a scheduled job is a one-shot, not a recurring cron entry."
  },
  {
    "stem": "How do you monitor a scheduled job's state and read its output after it runs?",
    "options": [
      "`capsule schedule list` shows the next cron fire time; open `report.json` in the `--out` directory",
      "`capsule schedule ps --watch` tails jobs, and logs auto-commit to your repo as `stdout.log`",
      "`capsule schedule runs <name>` prints run history; results save to `~/.capsule/results`",
      "`capsule schedule status` (filter with `--me` / `--state pending|running|completed|failed`) for state, and `capsule schedule logs <job-id> --tail N` for the streamed output"
    ],
    "answer": 3,
    "explain": "`capsule schedule status` lists jobs and their state (PENDING → RUNNING → COMPLETED/FAILED/CANCELLED), filterable by `--me` and `--state`. The node streams `output.log` to storage during the run; you read it back with `capsule schedule logs <job-id>`, optionally `--tail N`. There is no `schedule list`/`ps`/`runs` subcommand, no `--out` audit directory, and logs are not committed to your repo."
  }
]
</script>
</div>

### Connect forward

Friday: **timed sprint** + [the canonical quiz](knowledge-check.md). Cold-run the full benchmark workflow in 20 min. The capstone begins Monday.

---

## Pre-read for Friday (Day 45 · Timed Sprint + Phase 3 wrap)

- **Resource:** Problem Sets § Set 45 (sprint protocol + phase-timing rubric) + Flashcards command-recall tier.
- **Reflection questions:**
  1. What's your personal sequence: lease → connect → ??? → record?
  2. Which command did you forget the most this week?
  3. Where would you be slowest in a cold-start, and how do you fix that overnight?

---

## Stuck?

Ask **oxtutor**; share your 5-layer agent blueprint and it can identify governance gaps before you encounter them in the capstone.
