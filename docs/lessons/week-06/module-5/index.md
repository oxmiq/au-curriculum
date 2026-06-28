# Day 30 (Fri) · Orchestration + Consolidation + Phase 2 Assessment

> **Concept of the day:** **multi-agent** systems split work across specialized agents communicating through a structured protocol. **Planner-worker** (decomposer + executors) and **supervisor-worker** (delegating manager) are the two dominant patterns. The cost: more LLM calls, more failure modes. The benefit: parallelism, specialization, and the ability to scale beyond a single context window. **Friday:** Phase 2 assessment + consolidation.<br>
> **Pre-reading:** <a href="../../../readings/ai-agents/">AI Agents Pre-Lecture Reading — Orchestration & Multi-Agent section</a> (~30 min). Supplement: <a href="https://huggingface.co/learn/agents-course/unit2/introduction" target="_blank" rel="noopener">HuggingFace Agents Course — Unit 2 intro</a> (~10 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 6 — Prompt Engineering + AI Agents</a>
    <span class="sep">/</span>
    <span>Day 30 · Orchestration</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-06/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do | Time |
|------|---------------|----------|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Why Orchestration | 20 min |
| Part 3 | Deep Dive: Planner-Worker & Supervisor-Worker | 25 min |
| Part 4 | Core Concepts: Communication Protocols | 15 min |
| Part 5 | Hands-On: Architecture Decision | 25 min |
| Part 6 | Hands-On: Multi-Agent Cost Math | 25 min |
| Part 7 | Phase 2 Assessment | 30 min |
| Part 8 | Self-Assessment & Wrap-up | 15 min |

---

## Part 1 — Pre-Reading Review · 15 min

### Before You Start

You should have already read: Student Guide **Module 4 — Orchestration Layer** (~20 min).

### Quick Self-Check

Answer these questions from memory before continuing:

1. Why would you split work across multiple agents instead of using one big loop?
2. What is the **planner-worker** pattern? Who decides task decomposition?
3. What is the **supervisor-worker** pattern and how does it differ from planner-worker?
4. What's the approximate LLM call overhead of adding a planner + 3 workers vs single agent?
5. When is single-agent the right answer?

If you couldn't answer all five, re-read the Student Guide Module 4 before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m5-readiness" data-kind="readiness" data-draw="5" data-source="AI Agents Orchestration & Multi-Agent + HuggingFace Agents Course">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the planner-worker pattern in multi-agent systems?",
    "options": [
      "A single agent that plans and executes all tasks",
      "A planner agent decomposes tasks and worker agents execute the subtasks",
      "Workers that plan their own tasks",
      "A type of load balancing"
    ],
    "answer": 1,
    "explain": "The planner-worker pattern has a planner agent that decomposes the overall task into subtasks and assigns them to worker agents. The planner decides 'what goes where' and workers focus on execution. This is also called 'decomposer + executors' pattern."
  },
  {
    "stem": "What is the supervisor-worker pattern?",
    "options": [
      "Workers supervise each other",
      "A supervisor agent delegates tasks to workers based on their capabilities, acting as a central manager",
      "A single worker supervised by a human",
      "A pattern where workers plan for supervisors"
    ],
    "answer": 1,
    "explain": "The supervisor-worker pattern has a supervisor agent that acts as a central manager, delegating tasks to specialized workers based on their capabilities. The supervisor decides which worker should handle which subtask, unlike planner-worker where the planner does explicit decomposition."
  },
  {
    "stem": "What is the key difference between planner-worker and supervisor-worker?",
    "options": [
      "There is no difference",
      "Planner-worker does explicit task decomposition upfront; supervisor-worker delegates dynamically as tasks come in",
      "Planner-worker is faster; supervisor-worker is more accurate",
      "They use different LLM models"
    ],
    "answer": 1,
    "explain": "The key difference: Planner-worker does explicit task decomposition upfront (the planner breaks down the whole task into subtasks). Supervisor-worker delegates dynamically (the supervisor decides what to delegate as tasks come in). Planner is 'divide then conquer'; supervisor is 'delegate on demand'."
  },
  {
    "stem": "Why would you split work across multiple agents instead of one big loop?",
    "options": [
      "Multiple agents are always faster",
      "For parallelism, specialization, and scaling beyond a single context window",
      "Because one agent cannot think",
      "To save API costs"
    ],
    "answer": 1,
    "explain": "Multi-agent systems provide: (1) Parallelism — multiple workers can execute subtasks simultaneously, (2) Specialization — each worker can be optimized for a specific task type, (3) Scale beyond context window — the combined input might exceed what one model can handle."
  },
  {
    "stem": "What is the approximate LLM call overhead of adding a planner + 3 workers vs a single agent?",
    "options": [
      "No overhead",
      "Approximately 3-5x more LLM calls",
      "Approximately 10x more LLM calls",
      "It reduces LLM calls"
    ],
    "answer": 1,
    "explain": "Adding a planner + 3 workers adds significant overhead: the planner needs to decompose (1+ call), the supervisor needs to delegate (multiple calls), and each worker needs to execute (multiple calls). Approximate overhead is 3-5x more LLM calls than a single agent doing the same work. This directly impacts cost and latency."
  },
  {
    "stem": "When is single-agent the right answer?",
    "options": [
      "Always",
      "When the task fits in one context window, doesn't need parallelism, and doesn't require specialized skills",
      "Never",
      "When cost is not a concern"
    ],
    "answer": 1,
    "explain": "Single-agent is right when: (1) the task fits in one context window, (2) doesn't need parallelism (tasks are sequential), (3) doesn't require specialized skills. Multi-agent adds complexity (more failure modes, harder debugging) — only use it when the benefits (parallelism, specialization) outweigh the costs."
  },
  {
    "stem": "What is the main benefit of multi-agent systems despite the cost?",
    "options": [
      "They are always more accurate",
      "Parallelism, specialization, and ability to scale beyond a single context window",
      "They are cheaper",
      "They require less code"
    ],
    "answer": 1,
    "explain": "The main benefits of multi-agent systems are: (1) Parallelism — multiple agents can work simultaneously, (2) Specialization — each agent can be optimized for a specific task, (3) Scale beyond context window — the combined input might exceed what one model can handle. These benefits can justify the extra cost and complexity for the right use case."
  },
  {
    "stem": "What is communication protocol in multi-agent systems?",
    "options": [
      "The API used to call LLMs",
      "The structured way agents communicate with each other (e.g., message formats, coordination)",
      "A type of network protocol",
      "A security standard"
    ],
    "answer": 1,
    "explain": "Communication protocol defines how agents communicate with each other — message formats, coordination patterns, how to handle failures across agents. Without structured protocols, multi-agent systems become chaotic. Common patterns include message passing, shared state, and hierarchical reporting."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: Why Orchestration · 20 min

### Reading — The Control Plane for Agents

**Orchestration** is the control plane that answers: which model runs, which tools are available, in what order, when to retry, when to escalate, and when to bring a human in.

As agent systems grow, orchestration becomes the dominant engineering problem — not prompting, not tool design, but the plumbing that holds it all together.

### The "Agents Are the New Programmable Computer" Analogy

> *"The model is the processor. Prompts are the programming. The harness is the OS. Orchestration is the applications layer."*
> — paraphrased from Sequoia / Karpathy

| Old World | Agent World |
|---|---|
| Processor | Language model |
| Machine code / assembly | Raw token prediction |
| Programming language | Prompts + tool schemas |
| Operating system | Agent harness (runtime, tool dispatch, memory) |
| Applications | Orchestration layer |

Understanding orchestration = understanding how to build applications on top of this stack.

### Why Single-Agent Loops Hit Limits

| Limit | Effect |
|---|---|
| **Context-window ceiling** | After many steps, history exceeds 200K+ tokens. Worker spawning resets context. |
| **No parallelism** | Sequential tool calls can't be parallelized. Sub-agents run in parallel. |
| **No specialization** | One prompt trying to code + review + deploy = average quality on each. Separate prompts excel. |
| **Large blast radius** | One agent with all tools = full system exposure. Tool segregation across agents limits damage. |
| **Harder debugging** | A focused sub-agent's behavior is easier to test and reason about. |

---

## Part 3 — Deep Dive: Planner-Worker & Supervisor-Worker · 25 min

### Reading — The Two Dominant Patterns

**Planner-Worker** (a.k.a. plan-and-execute):

```
Planner: decomposes goal into subtasks
   ├──> Worker A: subtask 1 (own loop, own tools)
   ├──> Worker B: subtask 2
   └──> Worker C: subtask 3
Planner: aggregates results, decides if more work needed
```

Key properties:
- Planner has the **strategic view**; workers have **tactical execution**.
- Workers are usually **stateless** between subtasks — fresh context each time.
- Workers can run **in parallel** if subtasks are independent.
- Communication: JSON task spec → JSON result.

**Supervisor-Worker** (a.k.a. delegation):

```
Supervisor: receives goal, holds full context
   ├──> Worker A: "do step 1, report back" → result
   ├──> Worker B: "do step 2 with result from A" → result
   └──> Worker C: "summarize results" → final
```

Key properties:
- Supervisor **stays in the loop**; workers are short-lived RPC-style calls.
- Better for **sequential dependent steps** where each step depends on the previous.
- Supervisor's context grows; workers' don't.

### Comparing the Patterns

| Property | Planner-Worker | Supervisor-Worker |
|---|---|---|
| Task independence | Parallel-capable | Sequential by default |
| Who holds state | Planner | Supervisor (all of it) |
| Worker lifespan | Until subtask done | Per-call |
| Good for | Research, analysis, code gen | Approval flows, step-by-step workflows |
| Failure propagation | Worker failure → planner retries or skips | Worker failure → supervisor decides |

### Other Patterns Worth Knowing

| Pattern | When to Use |
|---|---|
| **Debate / Critic** | One agent proposes, another critiques, third arbitrates — quality lift on subjective tasks |
| **Pipeline** | Fixed sequence: scrape → extract → classify → write. No dynamic planning. |
| **Swarm / parallel sampling** | N agents solve in parallel; pick best by judge or majority vote |
| **Hierarchical** | Planner → sub-planners → workers. Three levels rarely beats two. |

### Failure Modes Introduced by Multi-Agent

- **Handoff drift** — Worker A misinterprets Planner's spec; output doesn't match what Planner expected.
- **Coordination loops** — Supervisor and Worker ping-pong on an ambiguous request.
- **Inconsistent assumptions** — Workers reach different conclusions on shared inputs.

Mitigations: typed message schemas, idempotent worker contracts, explicit success criteria per subtask, max-step bounds at every level.

---

## Part 4 — Core Concepts: Communication Protocols · 15 min

### Reading — How Agents Talk to Each Other

| Channel | Use Case |
|---|---|
| **Structured messages (JSON / XML)** | Default. Parseable, auditable, schema-validatable. |
| **Shared scratchpad (file, DB row)** | When agents need to read each other's work asynchronously. |
| **MCP Sampling primitive** | Agent A asks Agent B's host for a completion — the multi-agent enabler built into MCP. |
| **Pub/sub queue** | Loosely-coupled, scale-out workloads where workers pull from a job queue. |

### A2A — Agent-to-Agent Protocol

**A2A** is the protocol layer above MCP. Where MCP standardizes model ↔ tool communication, A2A standardizes **agent ↔ agent** communication:
- Goal delegation (pass a sub-goal to another agent)
- Result reporting (structured return value)
- Status polling (is the sub-agent done?)

A2A enables the planner-worker and supervisor-worker patterns to operate across runtimes and providers.

### Four Orchestration Approaches in the Wild

| Approach | What It Is |
|---|---|
| **Claude Code** | CLI harness; you write the prompt/tools, Claude runs the loop |
| **Claude CoWork** | Desktop tool with more baked-in orchestration + context management |
| **OpenAI Codex** | Cloud-fused harness + runtime; agent runs in a sandboxed cloud environment |
| **OpenClaw** | Open-source runtime; bring your own model, tools, and orchestration logic |

---

## Part 5 — Hands-On: Architecture Decision · 25 min

### Exercise: Single vs Multi — Make the Call

For each scenario below, decide: **single-agent** or **multi-agent**? If multi-agent, choose **planner-worker** or **supervisor-worker** and sketch the topology.

| Scenario | Single or Multi? | Pattern (if multi) | Sketch topology |
|---|---|---|---|
| Summarize one document | | | |
| Run 10 independent web searches in parallel | | | |
| Write code → run tests → fix failures → re-run | | | |
| Generate a report: research + outline + draft + proofread | | | |
| Answer a single Q&A question | | | |
| Triage and route 50 incoming support tickets | | | |

### Exercise: Design the Message Schema

For the "Generate a report" scenario above, design the JSON message that the Planner sends to each Worker and that each Worker returns.

**Planner → Worker message:**
```json
{
  "task_id": "",
  "subtask": "",
  "context": "",
  "tools_allowed": [],
  "max_steps": ,
  "success_criteria": ""
}
```

Fill in realistic values for the "outline" subtask. Then do the same for the "proofread" subtask.

**Worker → Planner result:**
```json
{
  "task_id": "",
  "status": "success | failure | needs_clarification",
  "output": "",
  "steps_taken": ,
  "error": null
}
```

### Exercise: Failure Mode Analysis

Pick the "Write code → run tests → fix failures → re-run" scenario.

1. List three specific failure modes for this multi-agent loop.
2. For each, write the mitigation (schema validation? max-retry count? human escalation?).
3. At what step count would you force a human-in-the-loop pause?

---

## Part 6 — Hands-On: Multi-Agent Cost Math · 25 min

### Reading — Cost Compounds with Complexity

Multi-agent systems multiply LLM calls. Every planner step costs tokens. Every worker loop costs tokens. Communication overhead costs tokens.

Reference numbers:
- Single-agent for a task: ~15 LLM calls.
- Planner + 3 workers, each with ~10 calls: **45 LLM calls** — **3× cost**.

### Exercise: Cost Model

Assume each LLM call costs $0.005 (average blended rate at current prices).

**Single-agent baseline:**
1. Cost per task (15 calls): ___
2. Cost for 1,000 tasks/day: ___
3. Monthly cost (30 days): ___

**Multi-agent (planner + 3 workers, 10 calls each):**
1. Cost per task (45 calls): ___
2. Cost for 1,000 tasks/day: ___
3. Monthly cost: ___
4. Cost increase vs single-agent: ___×

**Break-even analysis:**
5. If the multi-agent system produces work of twice the quality, how much more should it be worth per task?
6. At what quality multiplier is the 3× cost justified?

### Exercise: Reliability Math for Multi-Agent

In a planner-worker system:
- Planner makes 5 planning calls at 99% per-call reliability.
- 3 workers each make 10 calls at 97% per-call reliability.
- Planner makes 3 aggregation calls at 99%.

1. Probability all planner calls succeed: ___
2. Probability all calls for one worker succeed: ___
3. Probability all three workers complete successfully: ___
4. End-to-end probability the full task completes: ___
5. Compare to a single-agent making 15 calls at 97% reliability: ___

### Exercise: When to Go Multi-Agent

Complete this decision rule:

> Go multi-agent when **at least one** of the following is true:
> 1. ___
> 2. ___
> 3. ___
>
> Stay single-agent when **all** of the following are true:
> 1. ___
> 2. ___
> 3. ___

---

## Part 7 — Phase 2 Assessment · 30 min

### Exercise: Take the Knowledge Check

[Take the Phase 2 assessment](knowledge-check.html) — questions covering Week 6 Days 26–30 (prompt engineering + four agent layers).

**Passing score:** 10/15 (67%)

This is **10% of the program grade**. The quiz is open-book — reasoning-focused, not recall.

### If You Score Below Passing

1. Review the questions you got wrong.
2. Find the relevant day's content (Day 26–30).
3. Re-read that section of the lesson.
4. Retake the quiz after reviewing.

---

## Part 8 — Self-Assessment & Wrap-up · 15 min

### Self-Check List

Go through each item. Mark ✓ if you can do it **without notes**, ✗ if you need to review.

**Day 26 — Prompt Engineering Fundamentals**
- [ ] Name five prompting techniques (zero-shot, few-shot, chain-of-thought, role, structured output)
- [ ] Explain what chain-of-thought does mechanically to model output
- [ ] Write a well-structured prompt with role + context + task + constraints + format

**Day 27 — Agent Fundamentals (The Agent Loop)**
- [ ] Recite the five-step agent loop (Perceive → Plan → Act → Observe → Repeat)
- [ ] Sketch a ReAct loop (Thought / Action / Observation structure)
- [ ] Explain why MoE + FlashAttention = agents work economically

**Day 28 — Tools & MCP**
- [ ] Name the six fields of a tool schema
- [ ] Distinguish read tools from write tools and state the safety rule
- [ ] Name the four MCP building blocks and explain what MCP solves
- [ ] Calculate end-to-end reliability for a 10-call chain at 95% per-call

**Day 29 — Governance & Security**
- [ ] Explain indirect prompt injection with one concrete example
- [ ] Describe EchoLeak: CVE, date, target, mechanism, remediation
- [ ] List the three governance classes: Preventive, Detective, Corrective
- [ ] Name four components of machine-checkable security

**Day 30 — Orchestration & Multi-Agent**
- [ ] Compare planner-worker vs supervisor-worker with one scenario each
- [ ] State the cost multiplier: planner + 3 workers vs single agent
- [ ] List three multi-agent failure modes and their mitigations
- [ ] State the rule: "go multi-agent only when..."

### Connect Forward

Tomorrow (Day 31): **Bridge week begins** — Agent Case Studies, Capsule Foundations, Installation. The week's four agent layers (loop, tools, governance, orchestration) come together in a system design exercise.

### Pre-read for tomorrow (Day 31 · Bridge Week)

- **Resource:** AI Agents Student Guide **Module 0 "Why Now?"** (~20 min).
- **Reflection questions:**
  1. If you had to design an agent for one task in this curriculum (e.g., quiz generation, progress tracking), which pattern would you pick?
  2. What's the governance minimum you would require before deploying it to real interns?
  3. Which Phase 1 insight (latency, cost, batching) matters most for your agent's inference choice?

---

## Stuck?

Ask **oxtutor** — describe your multi-agent design (what the planner does, what each worker does, what tools they have) and ask for a review of the topology and cost model.
