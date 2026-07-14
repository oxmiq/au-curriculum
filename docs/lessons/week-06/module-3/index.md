# Day 28 · Tools & MCP

> **Concept of the day:** **tools** = functions the agent can call to act on the world. Each call has a **schema** the model must respect. **MCP (Model Context Protocol)** is the emerging standard for exposing tools across model providers: write once, plug into any compatible agent.<br>
> **Pre-reading:** <a href="../../../readings/ai-agents/#day-28-tools-mcp">AI Agents Pre-Lecture Reading - Tools & MCP section</a>. Supplement: <a href="https://www.anthropic.com/news/model-context-protocol" target="_blank" rel="noopener">Anthropic - Introducing the Model Context Protocol</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 6 - Prompt Engineering + AI Agents</a>
    <span class="sep">/</span>
    <span>Day 28 · Tools & Action Layer</span>
    {status:week-06/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do |
|------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Tool Anatomy |
| Part 3 | Deep Dive: Read vs Write & Safety |
| Part 4 | Core Concepts: MCP & A2A |
| Part 5 | Hands-On: Design Tool Schemas |
| Part 6 | Hands-On: Reliability Math |
| Part 7 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review

### Before You Start

You should have already read: AI Agents Student Guide **Module 2 - Action Layer** and the Anthropic MCP overview.

### Quick Self-Check

Answer these questions from memory before continuing:

1. What is a **tool** in the context of an AI agent, and why does it need a schema?
2. What does **MCP** stand for, and what problem does it solve?
3. What's the difference between a **read** tool and a **write** tool?
4. Why must a write tool never be called "because the agent decided to"?

If you couldn't answer all four, re-read the Student Guide Module 2 before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m3-readiness" data-kind="readiness" data-draw="5" data-source="AI Agents Pre-Lecture Reading - Tools & MCP + Anthropic MCP">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is a tool in the context of an AI agent?",
    "options": [
      "A software library",
      "A function the agent can call to act on the world (e.g., search, calculate, API call)",
      "A type of prompt",
      "A model configuration"
    ],
    "answer": 1,
    "explain": "A tool is a function the agent can call to act on the world: like search, calculate, make an API call, read a file, or send an email. Tools extend what the agent can do beyond just generating text."
  },
  {
    "stem": "Why does a tool need a schema?",
    "options": [
      "To make it run faster",
      "So the model knows what arguments to provide and what the tool does",
      "To secure the tool",
      "Schemas are optional"
    ],
    "answer": 1,
    "explain": "A tool schema tells the model: (1) what the tool does, (2) what arguments are required, (3) what each argument means. Without a schema, the model can't correctly invoke the tool; it doesn't know what to pass or how."
  },
  {
    "stem": "What does MCP stand for and what problem does it solve?",
    "options": [
      "Model Call Protocol: standardizes how models make API calls",
      "Model Context Protocol: standardizes how agents connect to tools and data sources",
      "Multi-Channel Processing: improves response speed",
      "Main Control Panel: a UI component"
    ],
    "answer": 1,
    "explain": "MCP (Model Context Protocol) standardizes how agents connect to tools and data sources. Before MCP, every agent had custom integrations for each tool. With MCP, you write the tool once and it works with any compatible agent: like USB-C for AI."
  },
  {
    "stem": "What is the difference between a read tool and a write tool?",
    "options": [
      "There is no difference",
      "Read tools retrieve information; write tools modify state or take actions",
      "Read tools are slower than write tools",
      "Write tools don't need schemas"
    ],
    "answer": 1,
    "explain": "Read tools retrieve information (search, read file, query database) without changing state. Write tools modify state or take actions (send email, write file, make payment). Write tools are riskier because they can cause real-world effects."
  },
  {
    "stem": "Why must a write tool never be called 'because the agent decided to'?",
    "options": [
      "It's inefficient",
      "The agent needs to provide a reasoned justification traceable to user intent, not just its own decision",
      "Write tools don't support that parameter",
      "It's against the MCP specification"
    ],
    "answer": 1,
    "explain": "Write tools must have a reasoned justification traceable to user intent. The agent saying 'I decided to send this email' is not acceptable; it must say 'I'm sending this because the user asked to...'. This ensures human oversight and auditability."
  },
  {
    "stem": "What is tool selection in the context of agents?",
    "options": [
      "Choosing which programming language to use",
      "The agent deciding which tool(s) to call from a available set",
      "Installing tools on a computer",
      "A security feature"
    ],
    "answer": 1,
    "explain": "Tool selection is the agent deciding which tool(s) to call from the available set. The model sees the tool schemas and chooses the appropriate tool(s) based on the user's request and its reasoning."
  },
  {
    "stem": "What is the relationship between MCP and tool integration?",
    "options": [
      "MCP replaces tools",
      "MCP provides a standard way to expose tools to agents so they work across different frameworks",
      "MCP is a type of tool",
      "MCP and tools are unrelated"
    ],
    "answer": 1,
    "explain": "MCP provides a standard way to expose tools to agents. Instead of writing custom integrations for each agent framework (LangChain, Claude Code, etc.), MCP lets tool developers write once and have their tools work across all compatible frameworks."
  },
  {
    "stem": "What is the key safety consideration for write tools?",
    "options": [
      "Write tools should not be used",
      "Write tools must require explicit user authorization, not just agent decision",
      "Write tools are always safe",
      "Write tools don't need any special handling"
    ],
    "answer": 1,
    "explain": "Write tools must require explicit user authorization. The agent can't just decide to write/change something; the user's intent must be clear and traceable. This is why write tools have stricter requirements than read tools."
  }
]
</script>
</div>

---

## Part 2 - Core Concepts: Tool Anatomy

### Reading - From ReAct Skeleton to Real Action

Yesterday's ReAct loop had a placeholder: `run_tool(action)`. Today you fill that in.

A **tool** is a function the agent runtime exposes to the model. The model does not run code directly; it **emits a structured tool-call**, the runtime validates it, runs the actual function, and feeds the result back as an `Observation`.

### Tool Anatomy

Every tool exposed to an agent carries six fields:

| Field | Purpose |
|---|---|
| `name` | Unique identifier: this is the exact string the model writes in `Action:` |
| `description` | One-paragraph explanation the model uses to *choose* this tool over alternatives |
| `parameters` | JSON Schema defining argument names, types, constraints |
| `returns` | Schema of the result fed back as `Observation:` |
| `side_effects` | `none` (read-only) vs `write`: gates safety policies |
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

The runtime, not the model, executes tools. The model only emits a structured request:

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

The model uses `description`, not `name`, to decide which tool to call. A vague or misleading description is the most common source of tool-selection errors. Rule of thumb: the description should answer "when would I pick this tool over the others?"

---

## Part 3 - Deep Dive: Read vs Write & Safety

### Reading - The Most Important Distinction

Tools fall into two classes. This distinction controls almost every safety decision in agent design:

| Read Tools | Write Tools |
|---|---|
| `search_docs`, `get_weather`, `read_file`, `query_database` | `send_email`, `create_ticket`, `write_file`, `transfer_money`, `delete_record` |
| Safe to call freely | Need approval / dry-run / audit log / rate-limiting |
| Reversible: world is unchanged | Often irreversible: real effects in the real world |
| Pre-deployment testing easy | Must test in a sandbox first |
| Failure = bad observation | Failure = real-world harm |

> **Rule:** Write tools require a **human-in-the-loop confirmation** step, OR a **pre-validated allowlist**, OR a **sandboxed dry-run**: never "the agent decided to."

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

## Part 4 - Core Concepts: MCP & A2A

### Reading - Why MCP Exists

Pre-MCP, every model provider had its own tool-calling format:
- OpenAI: `functions` / `tools` JSON
- Anthropic: `tool_use` content blocks
- Local engines: ad-hoc formats

Build your tools for OpenAI agents, and porting to Claude meant rewriting the entire tool layer. **5 integrations × 2 engineer-weeks bespoke = 10 weeks of work.** With existing MCP servers: **~2 weeks**.

### What MCP Standardizes

**Model Context Protocol** (Anthropic-originated, November 2024, "the USB-C for AI") defines a server-client protocol:

- **MCP server** - exposes tools (and resources) via **stdio** or **HTTP/SSE**.
- **MCP client** - embedded in the agent runtime; discovers and calls server tools.
- **Transport** - **JSON-RPC** over the chosen channel.

A tool implemented as an MCP server is consumable by any MCP-aware host: Claude Desktop, Cursor, OxCode, Capsule deployments, and any future compatible agent.

### MCP Building Blocks

| Block | What It Is |
|---|---|
| **Tools** | Function calls with schemas: the most common block |
| **Resources** | Document-like objects the agent can read (e.g., files, DB rows) |
| **Prompts** | Server-provided prompt templates the agent can use |
| **Sampling** | Servers can request LLM completions from the host: the multi-agent enabler |

### A2A - Agent-to-Agent Protocol

**A2A** sits above MCP. Where MCP handles model ↔ tool communication, A2A handles **agent ↔ agent** communication: coordinating goals, passing sub-tasks, and receiving results between agents that may run on different runtimes.

```
User
  └──> Orchestrator Agent  (A2A: delegates sub-tasks)
         ├──> Search Agent      (MCP: uses search_docs tool)
         ├──> Writer Agent      (MCP: uses file_write tool)
         └──> Review Agent      (MCP: uses read_file tool)
```

By Week 9, your benchmark runner will use this pattern.

---

## Part 5 - Hands-On: Design Tool Schemas

### Exercise: Write Three Tool Schemas

Pick **three functions** from any project you've worked on (or invent plausible ones). For each, write the full tool schema in JSON.

Requirements for each schema:
- `name` in snake_case
- `description` (1–2 sentences that answer "when would I pick this over the others?")
- `parameters` with at least 2 fields, one of which has a constraint (min/max, enum, or pattern)
- `side_effects` classified as `none` or `write`
- If `write`: write out the safety wrapper: what confirmation or policy check is required?

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

## Part 6 - Hands-On: Reliability Math

### Reading - Compounding Over a Chain

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

**Scenario A - Bespoke:** each integration takes 2 engineer-weeks.  
**Scenario B - MCP:** existing MCP servers exist for all 5; integration takes ~0.4 weeks each.

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

## Part 7 - Wrap-up & Connection

### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 28 · Tools &amp; MCP">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the six fields of a tool schema?",
    "options": [
      "name, type, input, output, version, owner",
      "name, description, parameters, returns, side_effects, cost",
      "tool_id, endpoint, method, auth, timeout, retry",
      "action, object, arguments, result, error, log"
    ],
    "answer": 1,
    "explain": "The six fields from the lesson: name (unique identifier), description (what it does: the model reads this to decide when to call it), parameters (inputs with types/descriptions), returns (what comes back), side_effects (what it changes in the world), cost (tokens or money per call). Missing description is the most common mistake."
  },
  {
    "stem": "What is the safety rule for write tools (tools with side effects)?",
    "options": [
      "Write tools should only be called during business hours",
      "Write tools must be wrapped in a confirm/deny human-in-the-loop step before execution",
      "Write tools should not be included in the tool schema",
      "Write tools should always retry on failure"
    ],
    "answer": 1,
    "explain": "Read tools (query, fetch) are safe to call freely. Write tools (send email, write to DB, delete file) have irreversible side effects. The safety rule: wrap write tools in a confirmation step that requires human approval before execution. This prevents agent runaway and accidental data destruction."
  },
  {
    "stem": "What does MCP stand for and what problem does it solve?",
    "options": [
      "Multi-Call Protocol: it batches multiple tool calls into one network request",
      "Model Context Protocol: it provides a standard interface for connecting AI models to tools and resources, so tools built once work with any MCP-compatible model",
      "Managed Compute Pipeline: it optimizes GPU allocation for agent workloads",
      "Memory Cache Protocol: it caches tool outputs to reduce redundant calls"
    ],
    "answer": 1,
    "explain": "MCP = Model Context Protocol (Anthropic, Nov 2024). The problem: each model and each tool had custom integrations. MCP is the 'USB-C for AI': a standard protocol where any MCP server exposes tools/resources/prompts that any MCP-compatible client can consume without custom code."
  },
  {
    "stem": "What are the four MCP building blocks?",
    "options": [
      "Agents, Models, Tools, Memories",
      "Tools, Resources, Prompts, Sampling",
      "Context, Actions, Observations, Rewards",
      "Endpoints, Schemas, Auth, Logging"
    ],
    "answer": 1,
    "explain": "MCP exposes four building blocks: Tools (callable functions), Resources (files, DB rows, APIs the model can read), Prompts (reusable prompt templates), and Sampling (the model can ask the MCP client to call another model). These cover the full range of what an agent needs from its environment."
  },
  {
    "stem": "A pipeline makes 10 tool calls, each with 95% individual reliability. What is the approximate end-to-end reliability?",
    "options": [
      "~95%",
      "~90%",
      "~80%",
      "~60%"
    ],
    "answer": 3,
    "explain": "0.95^10 ≈ 0.60 = ~60% end-to-end reliability. The lesson states: 'Tool-call reliability compounding: 95% per-call × 10 calls ≈ 60% end-to-end.' This is why production agent pipelines need retry logic, circuit breakers, and graceful degradation for failed tool calls."
  },
  {
    "stem": "What happens to model accuracy when too many tools are provided simultaneously?",
    "options": [
      "Model accuracy improves because it has more options to choose from",
      "Model accuracy degrades; studies show providing more than ~30 tools hurts the model's ability to select the right tool",
      "Model accuracy is unaffected by tool count",
      "Model accuracy degrades only when tools have overlapping descriptions"
    ],
    "answer": 1,
    "explain": "The lesson states: 'Tool-count degradation: >30 tools hurts model accuracy.' When given too many tools, models struggle to select the right one and may hallucinate calls to non-existent tools. Mitigations: tool tiering (load only relevant tools), tool-of-tools (a dispatcher that selects subsets)."
  },
  {
    "stem": "Which of the following is a write tool (per the lesson's read-vs-write distinction)?",
    "options": [
      "search_docs",
      "get_weather",
      "send_email",
      "read_file"
    ],
    "answer": 2,
    "explain": "The lesson classifies send_email (along with create_ticket, write_file, transfer_money, delete_record) as write tools; they modify state and are often irreversible, so they need approval / dry-run / audit / rate-limiting. search_docs, get_weather, and read_file are read tools: they only retrieve information and are safe to call freely."
  },
  {
    "stem": "Which tool-schema field does the model primarily use to decide which tool to call?",
    "options": [
      "name",
      "cost",
      "returns",
      "description"
    ],
    "answer": 3,
    "explain": "The lesson's 'Why the Description Field Dominates' section: the model uses description, not name, to choose a tool. A vague or misleading description is the most common source of tool-selection errors. Rule of thumb: the description should answer 'when would I pick this tool over the others?'"
  }
]
</script>
</div>

### Connect Forward

Tomorrow: **governance & security**: prompt injection at the tool boundary, output filtering, audit trails, and the EchoLeak case study (a real-world agent exploit, June 2025).

### Pre-read for tomorrow (Day 29 · Governance & Security)

- **Resource:** <a href="../../../readings/ai-agents/#day-29-governance-security">AI Agents Pre-Lecture Reading - Governance & Security section</a>. Supplement: <a href="https://www.cve.org/CVERecord?id=CVE-2025-32711" target="_blank" rel="noopener">MITRE - CVE-2025-32711 (EchoLeak)</a> + <a href="https://owasp.org/www-project-top-10-for-large-language-model-applications/" target="_blank" rel="noopener">OWASP Top 10 for LLM Applications</a> (scan LLM01 + LLM02).
- **Reflection questions:**
  1. What does "tool output is untrusted input" mean concretely? Give an example.
  2. How does indirect prompt injection differ from direct injection?
  3. What is the "blast radius" of an agent, and why does least-privilege reduce it?

---

## Stuck?

Ask **oxtutor**; describe the tool schema problem you're working on, including the `name`, `description`, and `parameters` you've drafted, and ask for a review.
