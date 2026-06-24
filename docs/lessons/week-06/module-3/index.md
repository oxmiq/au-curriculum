# Day 28 · Tools & MCP

> **Concept of the day:** **tools** = functions the agent can call to act on the world. Each call has a **schema** the model must respect. **MCP (Model Context Protocol)** is the emerging standard for exposing tools across model providers — write once, plug into any compatible agent.<br>
> **Pre-reading:** AI Agents Student Guide **Module 2 — Action Layer** + Anthropic MCP overview (~25 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 6 — Prompt Engineering + AI Agents</a>
    <span class="sep">/</span>
    <span>Day 28 · Tools & Action Layer</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-06/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do | Time |
|------|---------------|----------|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Tool Anatomy | 25 min |
| Part 3 | Deep Dive: Read vs Write & Safety | 20 min |
| Part 4 | Core Concepts: MCP & A2A | 20 min |
| Part 5 | Hands-On: Design Tool Schemas | 25 min |
| Part 6 | Hands-On: Reliability Math | 25 min |
| Part 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review · 15 min

### Before You Start

You should have already read: AI Agents Student Guide **Module 2 — Action Layer** and the Anthropic MCP overview (~25 min).

### Quick Self-Check

Answer these questions from memory before continuing:

1. What is a **tool** in the context of an AI agent, and why does it need a schema?
2. What does **MCP** stand for, and what problem does it solve?
3. What's the difference between a **read** tool and a **write** tool?
4. Why must a write tool never be called "because the agent decided to"?

If you couldn't answer all four, re-read the Student Guide Module 2 before continuing.

---

## Part 2 — Core Concepts: Tool Anatomy · 25 min

### Reading — From ReAct Skeleton to Real Action

Yesterday's ReAct loop had a placeholder: `run_tool(action)`. Today you fill that in.

A **tool** is a function the agent runtime exposes to the model. The model does not run code directly — it **emits a structured tool-call**, the runtime validates it, runs the actual function, and feeds the result back as an `Observation`.

### Tool Anatomy

Every tool exposed to an agent carries six fields:

| Field | Purpose |
|---|---|
| `name` | Unique identifier — this is the exact string the model writes in `Action:` |
| `description` | One-paragraph explanation the model uses to *choose* this tool over alternatives |
| `parameters` | JSON Schema defining argument names, types, constraints |
| `returns` | Schema of the result fed back as `Observation:` |
| `side_effects` | `none` (read-only) vs `write` — gates safety policies |
| `cost` | (optional) token/dollar cost hint so the agent can prefer cheaper tools |

### Example Tool Schema

```json
{
  "name": "search_docs",
  "description": "Search the company knowledge base for documents matching a query. Returns top-5 results with title, snippet, and URL.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural-language search query"
      },
      "limit": {
        "type": "integer",
        "default": 5,
        "minimum": 1,
        "maximum": 20
      }
    },
    "required": ["query"]
  },
  "returns": {
    "type": "array",
    "items": {"type": "object"}
  },
  "side_effects": "none"
}
```

### The Tool Dispatch Loop

The runtime — not the model — executes tools. The model only emits a structured request:

```python
while not done:
    response = llm.generate(messages, tools=TOOL_SCHEMAS)
    for tool_call in response.tool_calls:
        validate_against_schema(tool_call)   # types, required fields
        check_policy(tool_call)              # write tools: extra checks
        result = TOOLS[tool_call.name](**tool_call.args)
        messages.append({"role": "tool", "content": result})
    done = response.is_final()
```

Three critical steps before any execution: **validate → check policy → run**. Skip any one and you have a production bug.

### Why the Description Field Dominates

The model uses `description` — not `name` — to decide which tool to call. A vague or misleading description is the most common source of tool-selection errors. Rule of thumb: the description should answer "when would I pick this tool over the others?"

---

## Part 3 — Deep Dive: Read vs Write & Safety · 20 min

### Reading — The Most Important Distinction

Tools fall into two classes. This distinction controls almost every safety decision in agent design:

| Read Tools | Write Tools |
|---|---|
| `search_docs`, `get_weather`, `read_file`, `query_database` | `send_email`, `create_ticket`, `write_file`, `transfer_money`, `delete_record` |
| Safe to call freely | Need approval / dry-run / audit log / rate-limiting |
| Reversible — world is unchanged | Often irreversible — real effects in the real world |
| Pre-deployment testing easy | Must test in a sandbox first |
| Failure = bad observation | Failure = real-world harm |

> **Rule:** Write tools require a **human-in-the-loop confirmation** step, OR a **pre-validated allowlist**, OR a **sandboxed dry-run** — never "the agent decided to."

### Tool-Call Success Rate Compounds

This is the reliability math for tools:

- At **95% per-call** reliability, 10 tool calls in sequence → **0.95^10 ≈ 60%** end-to-end success.
- At **99% per-call** reliability, 10 tool calls → **0.99^10 ≈ 90%** end-to-end success.
- At **99.9% per-call**, 10 calls → **0.999^10 ≈ 99%**.

Each write tool in the chain multiplies the blast radius of any failure. Keep write-tool chains short.

### Tool-Count Degradation

More tools ≠ better. Model accuracy degrades noticeably when the tool list exceeds ~30 entries. The model spends too much attention on tool selection.

Solutions:
- **Tier tools**: load only tools relevant to the current task phase.
- **Tool-of-tools**: a meta-tool that dispatches to specialized sub-toolsets.
- **Semantic routing**: pick tools based on the task description before passing to the model.

---

## Part 4 — Core Concepts: MCP & A2A · 20 min

### Reading — Why MCP Exists

Pre-MCP, every model provider had its own tool-calling format:
- OpenAI: `functions` / `tools` JSON
- Anthropic: `tool_use` content blocks
- Local engines: ad-hoc formats

Build your tools for OpenAI agents, and porting to Claude meant rewriting the entire tool layer. **5 integrations × 2 engineer-weeks bespoke = 10 weeks of work.** With existing MCP servers: **~2 weeks**.

### What MCP Standardizes

**Model Context Protocol** (Anthropic-originated, November 2024, "the USB-C for AI") defines a server-client protocol:

- **MCP server** — exposes tools (and resources) via **stdio** or **HTTP/SSE**.
- **MCP client** — embedded in the agent runtime; discovers and calls server tools.
- **Transport** — **JSON-RPC** over the chosen channel.

A tool implemented as an MCP server is consumable by any MCP-aware host: Claude Desktop, Cursor, OxCode, Capsule deployments, and any future compatible agent.

### MCP Building Blocks

| Block | What It Is |
|---|---|
| **Tools** | Function calls with schemas — the most common block |
| **Resources** | Document-like objects the agent can read (e.g., files, DB rows) |
| **Prompts** | Server-provided prompt templates the agent can use |
| **Sampling** | Servers can request LLM completions from the host — the multi-agent enabler |

### A2A — Agent-to-Agent Protocol

**A2A** sits above MCP. Where MCP handles model ↔ tool communication, A2A handles **agent ↔ agent** communication — coordinating goals, passing sub-tasks, and receiving results between agents that may run on different runtimes.

```
User
  └──> Orchestrator Agent  (A2A: delegates sub-tasks)
         ├──> Search Agent      (MCP: uses search_docs tool)
         ├──> Writer Agent      (MCP: uses file_write tool)
         └──> Review Agent      (MCP: uses read_file tool)
```

By Week 9, your benchmark runner will use this pattern.

---

## Part 5 — Hands-On: Design Tool Schemas · 25 min

### Exercise: Write Three Tool Schemas

Pick **three functions** from any project you've worked on (or invent plausible ones). For each, write the full tool schema in JSON.

Requirements for each schema:
- `name` in snake_case
- `description` (1–2 sentences that answer "when would I pick this over the others?")
- `parameters` with at least 2 fields, one of which has a constraint (min/max, enum, or pattern)
- `side_effects` classified as `none` or `write`
- If `write`: write out the safety wrapper — what confirmation or policy check is required?

Use this template:

```json
{
  "name": "",
  "description": "",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": []
  },
  "returns": {},
  "side_effects": "none | write"
}
```

### Exercise: Classify & Design Safety Wrappers

Classify each tool as **read** or **write**, and for each write tool describe the safety wrapper:

| Tool | Read or Write? | Safety Wrapper (if write) |
|------|---------------|---------------------------|
| `query_database` | | |
| `delete_user` | | |
| `send_slack_message` | | |
| `get_user_profile` | | |
| `update_config` | | |
| `restart_service` | | |
| `summarize_thread` | | |
| `transfer_funds` | | |

### Exercise: Spot the Bug

This tool schema has at least two problems. Find and fix them:

```json
{
  "name": "do stuff",
  "description": "does things",
  "parameters": {
    "query": "string",
    "limit": "int"
  }
}
```

---

## Part 6 — Hands-On: Reliability Math · 25 min

### Reading — Compounding Over a Chain

Every tool call in a task chain multiplies the per-call reliability:

$$P(\text{all N calls succeed}) = r^N$$

where $r$ is per-call reliability and $N$ is the number of sequential calls.

### Exercise: Fill the Reliability Table

Complete this table (compute to one decimal place):

| Per-call reliability | N = 5 | N = 10 | N = 20 |
|---|---|---|---|
| 90% | ? | ? | ? |
| 95% | ? | ? | ? |
| 99% | ? | ? | ? |
| 99.9% | ? | ? | ? |

**Check your work:**
- 90%, N=10 → 34.9%
- 95%, N=10 → 59.9%
- 99%, N=10 → 90.4%
- 99.9%, N=10 → 99.0%

### Exercise: MCP vs Bespoke Cost

Your team needs to connect your agent to 5 external services (GitHub, Slack, Confluence, Jira, Google Calendar).

**Scenario A — Bespoke:** each integration takes 2 engineer-weeks.  
**Scenario B — MCP:** existing MCP servers exist for all 5; integration takes ~0.4 weeks each.

1. Total engineer-weeks for Scenario A: ___
2. Total engineer-weeks for Scenario B: ___
3. Time savings: ___
4. Name one downside of relying on existing MCP servers you didn't build yourself.

### Exercise: Tool-Count Threshold

You're designing an agent with 40 potential tools.

1. Why does providing all 40 tools at once degrade performance?
2. Sketch a tiering strategy: divide the 40 tools into 3 groups that get loaded at different task phases. Name the groups and give 2–3 example tools per group.
3. Describe the "tool-of-tools" pattern. When would you use it instead of tiering?

---

## Part 7 — Wrap-up & Connection · 10 min

### Self-Check

Can you recall these from memory?

- [ ] The six fields of a tool schema (`name`, `description`, `parameters`, `returns`, `side_effects`, `cost`)
- [ ] The three steps of the tool dispatch loop: validate → check policy → run
- [ ] Read vs write tool distinction and the safety rule for write tools
- [ ] What MCP stands for, when it was introduced, and the "USB-C for AI" analogy
- [ ] The four MCP building blocks (Tools, Resources, Prompts, Sampling)
- [ ] Tool-call reliability compounding: 95% per-call × 10 calls ≈ 60% end-to-end
- [ ] Tool-count degradation: >30 tools hurts model accuracy

### Connect Forward

Tomorrow: **governance & security** — prompt injection at the tool boundary, output filtering, audit trails, and the EchoLeak case study (a real-world agent exploit, June 2025).

### Pre-read for tomorrow (Day 29 · Governance & Security)

- **Resource:** Student Guide **Module 3 — Governance Layer** + Glossary entry on **EchoLeak** (~25 min).
- **Reflection questions:**
  1. What does "tool output is untrusted input" mean concretely? Give an example.
  2. How does indirect prompt injection differ from direct injection?
  3. What is the "blast radius" of an agent, and why does least-privilege reduce it?

---

## Stuck?

Ask **oxtutor** — describe the tool schema problem you're working on, including the `name`, `description`, and `parameters` you've drafted, and ask for a review.
