# Day 34 · Orchestration & Multi-Agent

> **Concept of the day:** **multi-agent** systems split work across specialized agents communicating through a structured protocol. **Planner-worker** (decomposer + executors) and **supervisor-worker** (delegating manager) are the two dominant patterns. The cost: more LLM calls, more failure modes. The benefit: parallelism, specialization, and the ability to scale beyond a single context window.
> **Pre-reading:** Student Guide **Module 4 — Orchestration Layer** (~20 min).
> **Source:** [Student Guide Module 4](../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Student%20Guide.md).

---

## Why this matters

Most production "agent systems" are actually **multi-agent**. Single-agent loops hit context limits, can't parallelize, and can't specialize. By Week 9 your benchmark-runner agent will likely delegate to specialized sub-agents (config validator, results analyst, report generator). The patterns here determine whether that's a clean architecture or a tangled mess.

## Readiness check

1. Why split work across agents instead of one big loop?
2. What's the **planner-worker** pattern? Who decides task decomposition?
3. What's the **supervisor-worker** pattern? How is it different?
4. What's the communication overhead of multi-agent vs single-agent (in LLM calls per task)?
5. When is single-agent the right answer?

## Core concept

### Why multi-agent

| Reason | Example |
|---|---|
| **Context-window limits** | Single agent's history exceeds 200K tokens after many steps. Spawn workers with fresh contexts. |
| **Parallelism** | 5 independent web searches in parallel vs sequential. |
| **Specialization** | A "code-writer" prompt and a "code-reviewer" prompt are easier than one prompt doing both well. |
| **Tool segregation** | Limit blast radius — only the "deploy" agent gets deploy tools. |
| **Reliability** | A failing sub-agent doesn't kill the parent's state. |

### The two dominant patterns

**Planner-Worker** (a.k.a. plan-and-execute):

```
Planner: decomposes goal into subtasks
   ├──> Worker A: subtask 1 (own loop, own tools)
   ├──> Worker B: subtask 2
   └──> Worker C: subtask 3
Planner: aggregates results, decides if more work needed
```

- Planner has the **strategic view**; workers have the **tactical execution**.
- Workers are usually **stateless** between subtasks — fresh context each.
- Communication: JSON task spec → JSON result.

**Supervisor-Worker** (a.k.a. delegation):

```
Supervisor: receives goal, holds full context
   ├──> Worker A: "do step 1, report back" → result
   ├──> Worker B: "do step 2 with result from A" → result
   └──> Worker C: "summarize" → final
```

- Supervisor stays in the loop; workers are short-lived RPC-style.
- Better for **sequential dependent steps**.
- Supervisor's context grows; workers' don't.

### Other useful patterns

| Pattern | When |
|---|---|
| **Debate / critic** | One agent proposes, another critiques, third arbitrates. Quality lift on subjective tasks. |
| **Pipeline** | Fixed sequence: scrape → extract → classify → write. No dynamic planning. |
| **Swarm / parallel sampling** | N agents solve in parallel; pick best by judge or majority vote. |
| **Hierarchical** | Planner → sub-planners → workers. Three levels rarely beats two. |

### Communication protocols

| Channel | Use |
|---|---|
| Structured messages (JSON / XML) | Default. Parseable, auditable. |
| Shared scratchpad (file, DB row) | When agents need to read each other's work |
| MCP **sampling** primitive | Agent A asks Agent B's host for a completion |
| Pub/sub (queue) | Loosely-coupled, scale-out workloads |

### Costs to count

A multi-agent system multiplies LLM calls:

- Single agent for a task: ~15 calls.
- Planner + 3 workers, each with ~10 calls: **~45 LLM calls** for the same task — **3× cost**.

> **Rule:** Only go multi-agent when **specialization, parallelism, or context limits** clearly justify the cost. Don't multi-agent because it sounds sophisticated.

### When single-agent wins

- Task is naturally linear / short.
- Context comfortably fits one window.
- No parallelism opportunities.
- Latency-sensitive (each handoff adds round-trips).
- Debugging is hard enough already.

### The failure-mode tax

Multi-agent introduces new failures:
- **Handoff drift** — Worker A misinterprets Planner's spec.
- **Coordination loops** — Supervisor and Worker ping-pong.
- **Inconsistent assumptions** — workers reach different conclusions on shared inputs.

Mitigations: typed message schemas, idempotent worker contracts, explicit success criteria per subtask, max-step bounds at every level.

## Practice (90 min)

1. (15 min) Re-design yesterday's example agent as either planner-worker or supervisor-worker. Justify the choice.
2. (25 min) Cost math: single-agent 15 calls @ $0.005 vs planner + 3 workers @ 10 calls each. Per task, per 1000 tasks. Is the lift worth it?
3. (25 min) Pair drill: design message schemas (JSON) for planner → worker and worker → planner.
4. (15 min) Identify two real workflows in this curriculum (e.g. quiz-generation, progress-recording) that could be planner-worker. Sketch.
5. (10 min) Write the rule: *"Go multi-agent only when ___."*

## Wrap-up

Cohort agrees on **the team-project agent architecture** for Friday's 10% Phase-2 assessment.

## Connect forward

Friday: **case studies + design synthesis**. The team project drops; Phase 2 wraps; we shift to **building** the inference stack in Phase 3 (Capsule). Then **[the canonical quiz](knowledge-check.html)**.

---

## Pre-read for Friday (Day 35 · Consolidation)

- **Resource:** Klarna AI assistant case study + a coding-agent case study (Cursor, OxCode, or Claude Code). One blog or talk each (~20 min).
- **Reflection questions:**
  1. For each case study: what's the agent's task? Single or multi? Read or write tools?
  2. What governance pattern is visible in the public information?
  3. What would you ask the team that built it?
