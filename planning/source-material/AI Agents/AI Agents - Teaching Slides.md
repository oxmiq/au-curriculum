<!-- Slide number: 1 -->

AI AGENTS
The 5-Layer Stack
An Introductory Course
Five modules • One course • From first principles
Based on Social Capital's “A Primer on AI Agents” (2026), with primary-source references.

### Notes:

<!-- Slide number: 2 -->

ROADMAP
What we'll cover

Five layers, one closed loop

0
Why Now?
The agentic explosion and what changed.

1
Intelligence
Reasoning, memory, knowledge: MoE, MLA, RAG.

2
Action
Tool use, ReAct loops, protocols (MCP, A2A), observability.

3
Governance
Prompt injection, machine-checkable security.

4
Orchestration
The control plane: which model, which tool, which agent.

5
Economics
Price per completed task, weak points, the frontier.

AI Agents — The 5-Layer Stack
Roadmap

### Notes:

<!-- Slide number: 3 -->

INSTRUCTOR
How to use this deck

Pair with the Student Guide, Lesson Plan, and Worksheets.

Per session
~90 minutes • 5–7 slides each module
Live discussion built in
One worksheet per module
Worked example drives every concept

What students leave with
A 5-layer mental model of agent systems
Working vocabulary: MoE, RAG, ReAct, MCP
The four weak points current agents have
A defensible view on where value accrues

AI Agents — The 5-Layer Stack
Instructor notes

### Notes:

<!-- Slide number: 4 -->

MODULE 0
Why Now? The Agentic Explosion
What changed, and why the loop is the agent.

### Notes:

<!-- Slide number: 5 -->

MODULE 0
From calculator to strategist

Chatbot
Prompt → Response
Probabilistic, one-shot
Treats every request as a fresh start
Bounded by design — no actions on the world
Useful, but limited

Agent
Perceive → Plan → Act → Observe → Repeat
Sets a goal, picks tools, takes action
Observes the result and revises the plan
Iterates until the goal is reached, or declared unreachable
The loop is the agent
If you remember one thing from Module 0, remember this: the loop is the structural property that separates an agent from a chatbot.

AI Agents — The 5-Layer Stack
Module 0 — Why Now?

### Notes:

<!-- Slide number: 6 -->

MODULE 0
Four capabilities, suddenly arriving together

AI progress was steady but incremental — until the last four years.

1
Foundational models
Pretrained giants that reason in natural language.

2
New architectures
MoE, MLA, and others make models cheaper to run.

3
Reasoning
Step-by-step thinking (CoT, inference-time models like o1).

4
Action + correction
ReAct + tool use lets the model take and verify steps.
Bundled into a closed loop → AI agents.

AI Agents — The 5-Layer Stack
Module 0 — Why Now?

### Notes:

<!-- Slide number: 7 -->

MODULE 0
The numbers (and a health warning)

Some are well-documented; some are Social Capital's projections.

28.6M
agents inside enterprises today (IDC, 2025)

2.2B
agents projected by 2030 (IDC)

$44B
Anthropic ARR by May 2026 (estimated)

~$5B → $236B
agent infra market: 2024 → 2034

Caveat: revenue and growth forecasts are the primer's estimates. The institutional facts (IDC's survey, coding-agent adoption) are well-documented; the precise figures are not audited.

AI Agents — The 5-Layer Stack
Module 0 — Why Now?

### Notes:

<!-- Slide number: 8 -->

MODULE 1
The Intelligence Layer
Reasoning, memory, and knowledge — the three pillars.

### Notes:

<!-- Slide number: 9 -->

MODULE 1
Three pillars of agentic intelligence

Each fixes a distinct weakness in the original LLMs.

Reasoning
Sparse MoE
Solves:  Compute cost
Result:  ~72% less inference compute (Mixtral)

Memory
MLA / KV-cache compression
Solves:  Long-context cost
Result:  5–13× compression (DeepSeek-V2)

Knowledge
RAG / GraphRAG
Solves:  Knowledge staleness
Result:  Live, cited, auditable answers
None substitutes for another. The intelligence layer is all three together.

AI Agents — The 5-Layer Stack
Module 1 — Intelligence

### Notes:

<!-- Slide number: 10 -->

MODULE 1
Mixture of Experts: don't fire the whole brain

A learned router activates only a few specialists per token.
Original LLMs: every parameter fires for every query.
Asking the time used the same compute as writing code.
MoE borrows from neuroscience: different regions for different tasks.
A router picks a small subset of expert sub-networks per token.
Mixtral 8x7B: ~47B total params, but only ~13B activate per token.
≈ 72% reduction in active inference compute vs. dense equivalent.

Router

E1

E2

E3

E4

E5

E6

E7

E8
2 of 8 experts active

AI Agents — The 5-Layer Stack
Module 1 — Intelligence

### Notes:

<!-- Slide number: 11 -->

MODULE 1
Retrieval-Augmented Generation (RAG)

Live external memory for a frozen model.
Models are snapshots. The world keeps changing.
Before answering, the agent retrieves relevant passages from a knowledge base and injects them into the prompt.
Citations are auditable — critical for enterprise use.
Long context (2M–10M tokens) absorbs some of RAG's use case…
…but enterprise corpora run to billions or trillions of tokens. Cost, latency, freshness, auditability still favour retrieval.
GraphRAG = retrieval over a graph of connected facts.

1
Query

2
Embed

3
Search vector DB

4
Inject context

5
Generate

AI Agents — The 5-Layer Stack
Module 1 — Intelligence

### Notes:

<!-- Slide number: 12 -->

MODULE 1
Recap — the intelligence layer

Technology
Problem solved
Result

Sparse MoE
Compute efficiency
75–95% fewer compute ops per token
MLA / KV cache compression
Long-context memory cost
5–13× compression (DeepSeek-V2)
RAG / GraphRAG
Knowledge staleness
Lower cost, latency; auditable citations
Next: how thinking becomes doing.

AI Agents — The 5-Layer Stack
Module 1 — Intelligence

### Notes:

<!-- Slide number: 13 -->

MODULE 2
The Action Layer
From thinking to doing: tools, ReAct, protocols.

### Notes:

<!-- Slide number: 14 -->

MODULE 2
The execution gap

Knowing what to do ≠ doing it. The harness bridges the gap.

LLM output
"Search flights to BER"
"Email Tom the agenda"
"Run npm test"
✕  Execution gap

Real-world tools
APIs
Browser, shell, file system
Messaging, payments
ReAct closes the gap:

Perceive

Plan

Act

Observe

AI Agents — The 5-Layer Stack
Module 2 — Action

### Notes:

<!-- Slide number: 15 -->

MODULE 2
The ReAct loop

Yao et al., ICLR 2023 — the canonical agent architecture.

PERCEIVE

PLAN

ACT

OBSERVE

LOOP
Perceive — read inputs, conversation, sensor data.
Plan — decide the next step given the goal.
Act — call a tool through the agent harness.
Observe — read the tool's output.
Repeat — feed the observation back to the planner.
Without this loop, an agent can't recover from errors, adapt mid-task, or chain complex actions.

AI Agents — The 5-Layer Stack
Module 2 — Action

### Notes:

<!-- Slide number: 16 -->

MODULE 2
Three protocols, three layers

How agents talk to tools and to each other.

A2A
Agent-to-Agent
Coordination between agents (delegation, voting, hand-off).

MCP
Model Context Protocol (Anthropic, Nov 2024)
“USB-C for AI.” Any compliant client talks to any compliant tool.

API
Application Programming Interface
The foundation. Built by each company for its own engineers.
One task can flow through all three: A2A coordinates → MCP reaches a tool → which wraps a REST API.

AI Agents — The 5-Layer Stack
Module 2 — Action

### Notes:

<!-- Slide number: 17 -->

MODULE 2
Observability

Silent failure is the most expensive kind. Three metrics define agent health.

1
Task completion rate
Did the agent actually finish the job?

2
Intervention rate
How often did a human have to step in?

3
Decision latency
How long between key decision and execution?
Built into the harness, not the model. Without these, silent failure stays silent until a customer complains.

AI Agents — The 5-Layer Stack
Module 2 — Action

### Notes:

<!-- Slide number: 18 -->

MODULE 3
The Governance Layer
What an agent is permitted to do — enforced in code.

### Notes:

<!-- Slide number: 19 -->

MODULE 3
The ambient AI problem

An always-on agent is an attack surface that never sleeps.

Traditional software
Executes when invoked
User reviews each input
Permissions narrow and explicit
Failure surfaces are bounded

Ambient AI agent
Runs continuously, multi-channel
Processes inputs the user never sees
Broad, accumulating permissions
Opaque internal decision chains

AI Agents — The 5-Layer Stack
Module 3 — Governance

### Notes:

<!-- Slide number: 20 -->

MODULE 3
Prompt injection — and EchoLeak

Hostile instructions hidden in content the agent reads.
Direct: user types instructions designed to override system policies.
Indirect: attacker hides instructions in a document, email, or webpage.
EchoLeak (CVE-2025-32711, June 2025): zero-click exploit of Microsoft 365 Copilot.
A crafted email could exfiltrate emails, OneDrive files, SharePoint docs, and Teams chats — silently, with no user interaction.
First publicly documented prompt-injection data exfiltration in a production LLM system.
Patched server-side same month — but the class of bug is here to stay.

DOCUMENT

EMAIL

WEB

INJECTED INSTRUCTIONS
ENTER AGENT CONTEXT

HIJACKED ACTION

AI Agents — The 5-Layer Stack
Module 3 — Governance

### Notes:

<!-- Slide number: 21 -->

MODULE 3
Machine-checkable security

Rules enforced in code that runs before any action — regardless of what the model says.

Whitelisted tool permissions
Only operator-approved tools. Hidden instructions cannot expand the list.

Action pre-validation
Destructive actions checked against a rulebook before they can run.

Runtime-enforced constraints
Limits applied by the runtime, regardless of the model's intent.

Small, readable codebase
Codebase the security team can verify end-to-end.
Governance is a property of the architecture, not the model. Code is harder to argue with.

AI Agents — The 5-Layer Stack
Module 3 — Governance

### Notes:

<!-- Slide number: 22 -->

MODULE 4
The Orchestration Layer
The control plane: which model, which tool, which agent.

### Notes:

<!-- Slide number: 23 -->

MODULE 4
Same model, different value

What orchestration decides between the user's request and the result.
Which model handles which task (cheap vs. frontier).
Which tools get called and in what order.
What state gets carried forward.
When to retry, escalate, or hand off.
When to put a human in the loop.

As models commoditize…
advantage shifts to whoever coordinates them best.

AI Agents — The 5-Layer Stack
Module 4 — Orchestration

### Notes:

<!-- Slide number: 24 -->

MODULE 4
Four approaches to orchestration

Different teams draw the line between harness, runtime, and orchestration in different places.

Claude Code
Developers

Developers
CLI wires Claude into terminal, files, dev tools. Dev runs the session.

Claude CoWork
Non-developers

Non-developers
Desktop app with skills, MCP connectors, scheduling baked in.

OpenAI Codex
Cloud teams

Cloud teams
Sandboxed cloud env per task; runs parallel agents; returns work.

OpenClaw
Builders

Builders
Open-source harness; local runtime; pulls model into messaging platforms.

AI Agents — The 5-Layer Stack
Module 4 — Orchestration

### Notes:

<!-- Slide number: 25 -->

MODULE 4
Agents are a new programmable computer

Sequoia's framing — same shape, different center.

Traditional computer
Processor
Silicon chip
Programming interface
Code
Operating system
Linux / Windows / macOS
I/O
Files, network, peripherals

Agent
Processor
Model (reasons)
Programming interface
Prompts + context window
Operating system
The agent harness
I/O
Tools, APIs, files, the world
"The model is the new processor; the harness is the new operating system."

AI Agents — The 5-Layer Stack
Module 4 — Orchestration

### Notes:

<!-- Slide number: 26 -->

MODULE 5
The Economic Layer
Cost, value, and what comes next.

### Notes:

<!-- Slide number: 27 -->

MODULE 5
Price per completed task, not per token

Three forces shape agent economics.

1
Licensing
Per-seat → per-token → per-task → per-outcome. Salesforce Headless 360 (Apr 2026) is a public turning point.

2
Build vs. buy
Owning hardware is high upfront, low per task. Renting cloud APIs is the reverse. Most serious deployments run both.

3
Failure costs
Retries, human cleanup ($50–$200/hr), idle compute, restart-from-step-1. Often dwarf the headline token cost.

AI Agents — The 5-Layer Stack
Module 5 — Economics

### Notes:

<!-- Slide number: 28 -->

MODULE 5
Why agents work now: deflationary inference

Cost per million tokens has fallen ~1,000× in three years.
~1,000×
cheaper inference, 2021 → 2024

GPT-3 (2021)
~$60 / M tokens

GPT-4 launch (2023)
~$30 / M tokens

GPT-4-class (2024)
~$0.30 / M tokens

Small frontier today
Pennies / M tokens

Caveat: today's headline prices are subsidized. Expect rebalancing as the buildout matures.

AI Agents — The 5-Layer Stack
Module 5 — Economics

### Notes:

<!-- Slide number: 29 -->

MODULE 5
Where agents break today

Four weak points = four categories of infrastructure waiting to be built.

Long-horizon drift
Errors compound across multi-step tasks. Anthropic data: 1,279 sessions with 50+ consecutive failures in a single month.

Edge cases
Confident wrong answers or silent abandonment. Agents often don't recognize they are in an edge case.

Security
Prompt injection makes the always-on surface a permanent attack vector.

Hidden human cleanup
Amazon Q outages (Mar 2026): 120,000 lost orders, 1.6M website errors — followed by a 6-hour outage taking 99% of North American orders.

AI Agents — The 5-Layer Stack
Module 5 — Economics

### Notes:

<!-- Slide number: 30 -->

MODULE 5
Where does value accrue?

As the agent stack matures, value moves from raw model access to the systems that turn models into reliable work.

Intelligence
Model labs capture value at the ceiling of capability.

Action
Tool ecosystems and protocols (MCP, A2A) become commodified infrastructure.

Governance
Regulated industries need this. Hardware enforcement matters.

Orchestration
The control plane. Likely a major value capture point.

Economics / Workflow
Whoever owns the workflow chooses the model, routes the task, governs the action, measures the result — and improves the system.
The workflow is the control point.

AI Agents — The 5-Layer Stack
Module 5 — Economics

### Notes:

<!-- Slide number: 31 -->

SYNTHESIS
The four foundational questions

Where you should be able to take a defensible position by the end of the course.

1
How is an AI agent different from a chatbot or static LLM?

2
What are the components of an agent, and how do they fit together?

3
Where are agents being deployed today, and where do they break?

4
Where does value accrue as the stack matures, and who controls it?

AI Agents — The 5-Layer Stack
Synthesis

### Notes:

<!-- Slide number: 32 -->

Thank you
Now go build something — or break something thoughtfully.
Companion materials: Student Guide • Facilitator Lesson Plan • Module Worksheets

---

# Instructor Appendix — Per-Module Delivery Kit

The slides above tell you *what* to put on screen. This appendix tells you *how to run the room* — engagement prompts to drop in, numerical anchors to keep at hand, and time-budget targets for a 90-minute session. Use it as a pre-class cheat sheet.

## How to use this appendix

Each module section below has four parts: **numerical anchors** (real numbers to cite if a student asks "is this big?"), **ask-the-room prompts** (drop one every ~15 minutes — give 10 sec of silence; take 2–3 wrong answers before resolving; tie answer back to a slide), **time budget** (so you finish in 90), and **calibration notes** (where to spend more or less time given your class).

---

## Module 0 — Why Now? (90 min)

**Numerical anchors:**

- Anthropic ARR: ~$1B (Dec 2024) → ~$44B (May 2026) — that's the agent commercial inflection.
- 28.6M enterprise agents deployed in 2025 (IDC); projected 2.2B by 2030.
- Agent infrastructure market: $5.4B (2024) → $11–12B (2026) → projected $236B (2034).
- >25% of new Google code is AI-generated (2024 CEO statement); higher in 2026.
- Per-task call multiplier: agents typically issue **8–20 model calls per user request** vs. ~1 for a chatbot.

**Ask the room:**

- *(opening)* "How many of you have used an AI tool today that did more than just answer a question — it actually *did something* for you?" Show of hands. Calibrates baseline.
- *(after the ReAct loop slide)* "If a chatbot is one function call, what's an agent in pseudocode?" (A `while not done:` loop with tool calls inside.)
- *(after the evidence slide)* "Anthropic went from $1B to $44B ARR in 18 months. What's the agent-specific reason — vs. just 'AI is hot'?" (Coding agents, Claude Code, enterprise consumption pricing.)
- *(closing)* "Predict: by 2030, what fraction of enterprise software will be agent-mediated rather than human-mediated?" Open vote. The point is the act of committing.

**Time budget:** 15 min orientation + agenda. 25 min on the chatbot-vs-agent distinction (THE module concept). 25 min on the four converging capabilities. 15 min on evidence + worked example. 10 min Q&A.

**Calibration:** Non-technical class? Spend extra time on the worked example (Berlin flight). Technical class? Push harder on "why now, not 2020" — the answer is the *combination* of MoE, MLA, reasoning, and tool protocols.

---

## Module 1 — Intelligence (90 min)

**Numerical anchors:**

- Frontier model output: Claude Opus ~$15/M tokens; Haiku ~$1/M; open Llama 70B ~$0.30/M (mid-2026).
- 1M-token context input cost: ~$3/call → ~$60/task at 20 calls — non-viable for most consumer products.
- Model-routing savings: typical 3–5× cost reduction by sending the right step to the right model.
- MoE active-vs-total params: DeepSeek-V3 = 37B active / 671B total — pay for active, store for total.

**Ask the room:**

- "Why doesn't an agent just use the biggest, smartest model for every step?" (Cost, latency, overkill for routine steps.)
- "When would you choose a 7B open-weight model over GPT-5?" (Tool-call formatting, classification, sub-100ms latency steps.)
- "RAG was invented in 2020. Why is it suddenly central to every agent in 2026?" (Long-context models exist but cost ~$3/call; RAG gives 90% of the benefit at 1% of the cost.)
- "If memory is just 'a database of past turns', what's hard about it?" (Relevance retrieval, summarization to fit context, when-to-forget.)

**Time budget:** 10 min framing (the model is the brain). 25 min on the model menu (frontier vs. open vs. specialized). 20 min on context / memory / RAG. 20 min on reasoning models (o1, R1). 15 min Q&A.

**Calibration:** If your class skipped the IE phase, spend 5 extra min on MoE/MLA basics. If they've done IE, fast-forward and spend that time on retrieval design.

---

## Module 2 — Action (90 min)

**Numerical anchors:**

- Tool-call success compounding: 95% per-call × 10 calls = 60% end-to-end; 99% × 10 = 90%. The leverage is enormous.
- MCP-server count: ~50 official + ~500 community by Q2 2026.
- MCP vs. bespoke: ~80% integration-time savings when an MCP server already exists.
- Indirect prompt injection: first CVE in production agent (EchoLeak / CVE-2025-32711) cost an enterprise customer ~$2M in remediation.

**Ask the room:**

- "A tool call has 95% success. That sounds great. Why is it actually terrible?" (Compounding — 10 calls collapse to 60%.)
- "Function calling is the model speaking JSON. What does MCP add on top?" (Standardized transport, discovery, schemas, security model.)
- "Why doesn't every team just write bespoke integrations? They have more control." (Engineering tax scales linearly with surface area; MCP collapses it to a one-time investment per server.)
- "If you could only invest in *one* thing to improve a production agent, would it be model quality or tool reliability?" (Tool reliability — it's the multiplicative bottleneck.)

**Time budget:** 10 min ReAct refresher. 20 min on tool-call mechanics + failure modes. 25 min on MCP (the big idea of the module). 15 min on observability and tracing. 10 min on A2A preview. 10 min Q&A.

**Calibration:** Have students with a software-engineering background? Push the compounding-failure-rate math hard — they'll find it counterintuitive and memorable. ML-only background? Spend extra time on the wire-protocol idea.

---

## Module 3 — Governance (90 min)

**Numerical anchors:**

- EchoLeak (CVE-2025-32711): first zero-click prompt-injection exploit in a production LLM system (Microsoft 365 Copilot, June 2025).
- Sandbox overhead: ~200 ms container start + ~$0.001/run — a trivial tax for a transformative blast-radius reduction.
- Least-privilege scoping: typically removes 90%+ of the consequence of a successful injection.
- Insurance market: AI-incident insurance products started shipping in late 2025 (~$50–500K/yr policies for mid-market enterprises).

**Ask the room:**

- "Prompt injection has been known since 2022. Why is it still the #1 agent vulnerability in 2026?" (Fundamental: instructions and data share one channel. No 'fix' on horizon.)
- "Your agent reads emails and can run shell commands. Walk through what *could* happen if I email it a malicious instruction." (Indirect prompt injection.) Then: "How do you sandbox this without breaking the product?"
- "An auditor asks: 'who made this decision and why?' for an agent action. Can your system answer?" (Tests audit-trail design.)
- "If your product launches without an emergency-stop button, what's your CISO going to say?" (Tests human-in-the-loop intuition.)

**Time budget:** 10 min framing (governance is the brakes). 25 min on prompt injection (deep dive — show real EchoLeak walkthrough if class is technical enough). 20 min on sandboxing + least privilege. 15 min on audit trails + human-in-the-loop. 10 min on compliance/insurance horizon. 10 min Q&A.

**Calibration:** Security-aware class? Use EchoLeak as a 20-min mini-lecture. Beginner class? Stick with concept-level treatment and focus on the *mental model* of "instructions and data share one channel."

---

## Module 4 — Orchestration (90 min)

**Numerical anchors:**

- Multi-agent latency: naive serial 50s → orchestrated parallel 30s → with caching 20s (typical 2.5× wall-clock win).
- Handoff cost: ~2K tokens × $0.001/K = $0.002 per inter-agent handoff. At 20 handoffs/workflow, handoff cost ≈ $0.04.
- A2A protocol adoption: ~12 frameworks announced support by Q2 2026 (LangGraph, AutoGen, CrewAI, etc.).
- Production agent fleets at hyperscalers: 10K+ concurrent agents per cluster is now table stakes.

**Ask the room:**

- "Why doesn't a single mega-agent do everything? Why split into a team?" (Specialization, parallelism, easier debugging, cost routing.)
- "What's the multi-agent equivalent of a deadlock?" (Agent A waiting for B's output while B waits for A.) "How do you prevent it?"
- "If MCP standardizes agent-to-tool, why do we need A2A for agent-to-agent? Can't agents just be tools to each other?" (They can — A2A standardizes the *semantics* of long-running, stateful, multi-turn agent collaboration; tool-calling is one-shot.)
- "Predict: in 5 years, will most production agent systems be single-agent or multi-agent?" Open argument.

**Time budget:** 15 min framing (orchestration = Kubernetes for agents). 25 min on patterns (planner-executor, supervisor-worker, blackboard). 20 min on A2A protocol. 15 min on observability + cost control. 15 min Q&A.

**Calibration:** Distributed-systems-aware class? Map directly to Kubernetes / actor model concepts. ML-only class? Lean on the worked example walkthrough.

---

## Module 5 — Economics (90 min)

**Numerical anchors:**

- Customer-support per-ticket cost: human ~$7 → agent ~$0.30 (~20× cheaper, even after overhead).
- Per-seat pricing trap: power user at 200 tasks/day costs ~$72/month, breaks $50/seat pricing.
- Salesforce Agentforce: consumption-based pricing announced 2024, scaled in 2025.
- Anthropic / OpenAI 2026 enterprise pricing: typically $0.005–$0.05 per agent task (depending on complexity).

**Ask the room:**

- "You charge $50/seat/month. A user runs your agent 200 times/day. What's your gross margin?" (Negative — work through it on the whiteboard.)
- "Salesforce moved to consumption pricing in 2024. Why was that a forced move, not a choice?" (Per-seat breaks when agent cost scales with usage.)
- "Where do moats come from in the agent stack?" (Distribution, integrations, governance, brand — not the model itself.)
- *(closing)* "If you started an agent company tomorrow, what's the first business-model question you'd answer?" (How do you avoid losing money on heavy users.)

**Time budget:** 10 min framing (everything you've learned, viewed through P&L). 25 min on unit-economics deep-dive. 20 min on pricing models (per-seat, per-task, per-outcome, hybrid). 15 min on the four weak points. 10 min on the frontier (AGI, regulation). 10 min Q&A + course recap.

**Calibration:** Business-oriented class? Spend 30+ min on pricing-model walkthroughs. Engineering class? Keep the pricing brisk; spend more on the four weak points (governance, trust, integration breadth, vertical depth).

---

## Mid-session energy checks (any module)

If the room fades around minute 50:

- **Stand-up vote**: "Stand up if you've shipped an agent (or agent-adjacent feature) at work." Visualization wakes the room.
- **One-minute pair-share**: "Explain [last concept] to your neighbor in your own words." Often better than another slide.
- **Live numerical estimate**: Pick the next anchor and have students guess before you reveal.

## Course-wide ask-the-room ladder

Use these in the final 10 min of the last session for a synthesis discussion:

1. "Walk me through how you'd design a customer-support agent." (Tests all 5 layers.)
2. "What's the most likely way your agent fails in week 1 of production?" (Tests Module 3 + 2.)
3. "Who captures the long-term value in this stack?" (Tests Module 5.)
4. "What's the equivalent of the 'Linux moment' for the agent stack — and when does it happen?" (Synthesis + speculation.)

## Concept-graph cross-references

| Module | Primary concept IDs (in `docs/kb/concepts.json`) |
|---|---|
| 0 | `agent-loop`, `react-pattern` |
| 1 | `agent-loop`, `inference-cost` (cross-phase) |
| 2 | `mcp`, `tool-use`, `function-calling` |
| 3 | `prompt-injection`, `sandboxing`, `least-privilege` |
| 4 | `orchestration`, `a2a-protocol`, `multi-agent-systems` |
| 5 | `agent-economics`, `inference-cost` (cross-phase) |

Print this table at the start of the course as a tracker; revisit it at the end as a self-assessment.

### Notes: