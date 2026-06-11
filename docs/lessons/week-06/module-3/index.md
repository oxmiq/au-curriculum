# Day 32 · Tools & MCP

> **Concept of the day:** **tools** = functions the agent can call to act on the world. Each call has a **schema** the model must respect. **MCP (Model Context Protocol)** is the emerging standard for exposing tools across model providers — write once, plug into any compatible agent.
> **Pre-reading:** AI Agents Student Guide **Module 2 — Action Layer** + Anthropic MCP overview (~25 min).
> **Source:** [Student Guide Module 2](../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Student%20Guide.md) · [Glossary: MCP](../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Glossary.md).

---

## Why this matters

Tools are how agents stop being chatbots and start *doing things*. MCP is the protocol that lets your Capsule deployment, an OpenAI agent, and a local Claude all share the same tool definitions. Without tools, agents are limited to text reasoning over their training data — useful, but not transformative.

## Readiness check

1. Define a **tool** in one sentence. Why does it need a schema?
2. What's the difference between a **read** tool and a **write** tool? Why does the distinction matter for safety?
3. What does **MCP** stand for? What problem does it solve?
4. Why must tool calls be **idempotent** when possible?
5. What's a **tool dispatch loop** and where does it sit in the architecture?

## Core concept — tools

### Tool anatomy

A tool exposed to an agent has:

| Field | Purpose |
|---|---|
| `name` | Unique identifier the model writes in `Action:` |
| `description` | One-paragraph explanation the model uses to *choose* this tool |
| `parameters` | JSON schema for arguments |
| `returns` | Schema of the result fed back as `Observation:` |
| `side_effects` | Read-only vs write — gates safety policies |
| `cost` | (optional) so the agent can prefer cheaper tools |

Example:

```json
{
  "name": "search_docs",
  "description": "Search the company knowledge base for documents matching a query. Returns top-5 results with snippets.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Search query"},
      "limit": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20}
    },
    "required": ["query"]
  },
  "returns": {"type": "array", "items": {"type": "object"}},
  "side_effects": "none"
}
```

The agent loop:
1. Model emits `Action: search_docs({"query": "Q3 forecast"})`.
2. Runtime parses + validates against the schema.
3. Runtime executes the function.
4. Result is appended as `Observation: [...]`.

### Read vs write — the most important distinction

| Read tools | Write tools |
|---|---|
| `search_docs`, `get_weather`, `read_file` | `send_email`, `create_ticket`, `write_file`, `transfer_money` |
| Safe to call freely | Need approval / dry-run / audit log / rate-limiting |
| Reversible | Often irreversible |
| Pre-deployment testing easy | Must test in sandbox |

> **Rule:** Write tools require a **human-in-the-loop confirmation** step OR a **policy check** OR a **sandbox** — never just "the agent decided to."

### Tool dispatch loop

```python
while not done:
    response = llm.generate(messages, tools=TOOL_SCHEMAS)
    for tool_call in response.tool_calls:
        validate_against_schema(tool_call)
        check_policy(tool_call)            # write tools: extra checks
        result = TOOLS[tool_call.name](**tool_call.args)
        messages.append({"role": "tool", "content": result})
    done = response.is_final()
```

This is the production version of yesterday's ReAct skeleton.

## Core concept — MCP

### Why MCP exists

Pre-MCP, every model provider had their own tool-calling format:
- OpenAI's `functions` / `tools` JSON
- Anthropic's `tool_use` blocks
- Local engines' ad-hoc formats

If you built tools for OpenAI agents, porting to Claude meant rewriting all your tool layer.

### What MCP standardizes

**Model Context Protocol** (Anthropic-originated, now widely adopted) defines a server-client protocol:

- **MCP server** — exposes a set of tools (and resources like documents) via stdio or HTTP/SSE.
- **MCP client** — embedded in the agent runtime; discovers and calls server tools.
- **Transport** — JSON-RPC over a chosen channel.

A tool implemented as an MCP server can be consumed by any MCP-aware host: Claude Desktop, Cursor, OxCode, Capsule deployments, etc.

### Building blocks MCP standardizes

| Block | What |
|---|---|
| **Tools** | Function calls with schemas (most common) |
| **Resources** | Document-like objects the agent can read |
| **Prompts** | Server-provided prompt templates |
| **Sampling** | Servers can request LLM completions from the host (multi-agent enabler) |

### Practical impact

The OxCode workspace (`oxcode/`) and the agentic-workflows project both use MCP. By Week 9 your Capsule benchmarks will be triggered by an agent calling an MCP-exposed `run_benchmark` tool.

### When NOT to use MCP

- Internal-only tools tightly coupled to one app — direct function calls are simpler.
- Sub-millisecond latency requirements — protocol overhead matters.

## Practice (90 min)

1. (15 min) Take 3 functions you've written before. Draft their MCP tool schemas.
2. (25 min) Pair: classify these as read or write — `query_database`, `delete_user`, `send_slack`, `get_user_profile`, `update_config`, `restart_service`, `summarize_thread`. For each write, design the safety wrapper.
3. (25 min) Read a minimal MCP server example (Anthropic docs). Identify the four blocks (tools / resources / prompts / sampling).
4. (15 min) Failure-mode brainstorm: list 5 ways a tool-using agent can go wrong (bad schema, infinite loop, malicious tool result, etc.).
5. (10 min) Write the rule: *"Write tools always need ___."*

## Wrap-up

Cohort agrees on a **safety policy** for write tools in their Week 7 group project.

## Connect forward

Tomorrow: **governance & security** — prompt injection at the tool boundary, output filtering, audit trails, the EchoLeak case study.

---

## Pre-read for tomorrow (Day 33 · Governance & Security)

- **Resource:** Student Guide **Module 3 — Governance Layer** + Glossary entry on **EchoLeak** (~25 min).
- **Reflection questions:**
  1. **Tool output is untrusted.** What does that mean concretely?
  2. Name two real-world prompt-injection-via-tool attacks (look up "indirect prompt injection").
  3. What's an audit trail and why is it non-negotiable for write-tool agents?
