# AI Agents — Glossary

*Vocabulary reference for Week 7. Each term has a one-line "field definition," a paragraph of explanation, and a cross-reference to where it's introduced in the Student Guide / curriculum schedule.*

---

### A2A (Agent-to-Agent protocol)
**Field:** An emerging protocol for one agent to invoke another agent as a tool, with discovery, capability advertisement, and result handling.

A2A is to multi-agent systems what MCP is to tool calls: the standard that lets agents built by different teams interoperate without bespoke glue. As of mid-2026, A2A specifications are competing (Anthropic's draft, Google's variant, the open A2A working group). Treat it as "MCP for delegation." *Introduced: Day 32.*

### Agent
**Field:** An LLM-driven system that runs in a loop — perceiving an environment, planning a next step, taking an action through a tool, observing the result, and iterating until a goal is reached or declared unreachable.

The single structural property that separates an agent from a chatbot is **the loop**. A chatbot returns one response per request and stops. An agent returns a response, takes an action, observes, and returns to the planning step. Everything else (memory, tools, governance, orchestration) is scaffolding to keep the loop running reliably. *Introduced: Day 31.*

### Agent loop (ReAct loop)
**Field:** The canonical control flow of an agent: Perceive → Plan → Act → Observe → Repeat.

Named after Yao et al.'s 2022 *ReAct* paper, which fused chain-of-thought reasoning with tool use. The loop terminates when the goal is reached, a maximum step count is hit, or the agent declares failure. Step caps are a governance control, not a performance tuning knob. *Introduced: Day 31.*

### Blast radius
**Field:** The maximum harm an agent can cause if compromised, measured as a function of the tools it can call and the credentials it holds.

A read-only RAG agent has near-zero blast radius. A deployment agent with cloud admin credentials has near-infinite blast radius. The single best lever for shrinking blast radius is *least-privilege tool design* — give the agent the narrowest tool that does the job, not the most general one. *Introduced: Day 33.*

### Chain-of-thought (CoT)
**Field:** Prompting technique where the model produces intermediate reasoning before its final answer.

Within an agent, CoT is what produces the *Plan* step of the loop. The "Thought:" line in a ReAct trace is literally CoT. *Cross-reference: Week 6 Day 28.* *Used: Day 31.*

### EchoLeak (CVE-2025-32711)
**Field:** A 2025 indirect-prompt-injection vulnerability in Microsoft 365 Copilot's email/document pipeline that allowed adversary-controlled documents to exfiltrate organizational data via the agent's own tool calls.

The canonical worked example for indirect prompt injection. Attackers planted instructions in shared documents; when Copilot summarized them, the instructions executed in the user's privilege context. Fix required scoping the agent's outbound tools, not patching the model. *Introduced: Day 33.*

### Governance layer
**Field:** The set of controls — sandboxing, blast-radius limits, observability, audit logs, human-in-the-loop gates — that bound what an agent can do and produce evidence of what it did.

Distinct from the *security* of the model itself (which is the prompt-injection problem). Governance is concerned with *consequences* of correct-looking actions: who approved this deployment, where is the receipt, what was the diff. *Introduced: Day 33.*

### Indirect prompt injection
**Field:** Prompt injection where the attacker controls *data* the agent retrieves (web page, document, email) rather than the prompt the user types.

Far more dangerous than direct injection because the user's intent is benign — they asked the agent to read a document — and the attack rides on the agent's normal tool use. EchoLeak is the prototype example. *Introduced: Day 33. Cross-reference: Week 6 Day 29.*

### Intelligence layer
**Field:** The foundational model (and its reasoning capabilities) at the core of the agent — the component that does the *Plan* step.

Models in this layer are mostly substitutable in 2026 — Claude, GPT-4o/5, Gemini, open-weight Mixtral / DeepSeek / Llama all support tool use and reasoning. The substitutability is what pushes value accrual toward the layers *above* this one. *Introduced: Day 31.*

### LangGraph
**Field:** A graph-based orchestration framework for multi-step / multi-agent workflows, built on top of LangChain.

Models the agent or multi-agent system as an explicit state machine. Strength: makes control flow inspectable and debuggable. Tradeoff: more upfront design than smolagents-style flat loops. *Introduced: Day 34.*

### Long-horizon drift
**Field:** The compounding-error problem in multi-step agent plans: even if each step succeeds with high probability, the joint success probability of a long chain collapses fast.

Example: 10 steps at 90% each ⇒ 0.9¹⁰ ≈ 35% joint success. The math is unforgiving. Defenses: shorten the chain (decompose differently), raise per-step reliability (better prompts/tools), checkpoint and resume, human gates at high-stakes steps. *Cross-reference: Week 6 Day 30 chain-reliability calculation.* *Introduced: Day 34.*

### MCP (Model Context Protocol)
**Field:** Anthropic-originated open protocol for exposing tools, data sources, and prompts to LLM clients via a structured manifest and JSON-RPC endpoints.

Solves the "every framework reinvented its own tool-calling format" problem by standardizing the *interface*. A tool published as an MCP server can be consumed by any MCP-aware client (Claude Desktop, Cursor, VS Code Copilot, custom agents). `capsule mcp` exports the Capsule CLI as an MCP server — same protocol, different tools. *Introduced: Day 32.*

### Multi-agent system
**Field:** A system of two or more agents that coordinate to accomplish a task, typically via routing (one agent dispatches to specialists) or workflow (a fixed sequence of agents).

The strongest argument *against* multi-agent is "you've added an orchestration problem to your reasoning problem." The strongest argument *for* it is "specialized agents with narrow blast radii are safer and more debuggable than one omni-agent with admin rights." Most production systems converge on routed-specialist designs. *Introduced: Day 34.*

### Observability (agent traces)
**Field:** Structured logs of every loop iteration — prompts, model responses, tool calls, tool outputs, errors — captured for debugging, audit, and post-mortem.

The agent equivalent of distributed-system tracing. Without it, "the agent did something weird" is unrecoverable. With it, you can replay the exact loop and find the step where things went sideways. Tools: LangSmith, Helicone, OpenTelemetry-for-LLM (emerging standards). *Introduced: Day 33.*

### Orchestration layer
**Field:** The control layer above individual agents that handles routing, workflow, retry, fallback, and human gates.

Where the Action layer is "what *can* this agent do," the Orchestration layer is "what *should* happen, in what order, with what guardrails." The workflow definition is also the *control point* for governance — it's where you wire in approvals and audits. *Introduced: Day 34.*

### Perceive / Plan / Act / Observe
**Field:** The four canonical steps of the agent loop. *Perceive*: read environment state. *Plan*: reason about the next step (CoT). *Act*: invoke a tool. *Observe*: read the tool's output and update state.

Not every framework names them this way, but every framework implements them. When debugging a misbehaving agent, identify which step failed before guessing at the fix. *Introduced: Day 31.*

### Prompt injection (direct)
**Field:** An attack where the user (or anyone with input access) embeds instructions in their prompt that override the system prompt's intent.

Direct injection is the easier case — defenses are mostly delimiter discipline and instruction hierarchies. *Cross-reference: Week 6 Day 27.* See also *Indirect prompt injection*. *Introduced: Day 33.*

### ReAct
**Field:** A 2022 prompting/architecture pattern (Yao et al., arXiv:2210.03629) that interleaves *Reasoning* (CoT-style thoughts) with *Acting* (tool invocations) in a single trace.

The first published demonstration that LLMs could reliably take actions in the world and recover from errors, and the conceptual ancestor of every modern agent framework. The pattern's trace format (`Thought: … / Action: … / Observation: …`) is still the default lingua franca. *Introduced: Day 31.*

### Routing (agent routing)
**Field:** The orchestration pattern where an upstream agent (or rule) dispatches a request to one of several downstream specialist agents based on the request's category.

The simplest multi-agent design that adds value over a single agent. Tradeoff: the router itself becomes a single point of failure and a privilege concentrator. *Introduced: Day 34.*

### Sandboxing
**Field:** Confining an agent's tool execution to an environment where the maximum possible harm is bounded — ephemeral containers, scoped credentials, read-only filesystems, network egress allow-lists.

Sandboxing is the operational expression of blast-radius limits. Cheaper than getting the agent to refuse correctly 100% of the time. Both should be in place. *Introduced: Day 33.*

### smolagents
**Field:** A minimal-API agent framework from HuggingFace; flat-loop ReAct with Python code as the tool-calling language.

Strength: very small surface area, easy to read end-to-end. Weakness: less structure than LangGraph for complex workflows. Good first framework when teaching the loop because almost nothing is hidden. *Introduced: Day 34.*

### Tool
**Field:** A function exposed to the agent — with a name, description, typed parameters, and a return type — that the model can invoke during the *Act* step of the loop.

Tools can be local (filesystem read, shell exec), networked (HTTP API, database query), or other agents (via A2A). The art of tool design is making tools *narrow* (one job each) and *self-describing* (the description is what the model reasons over). *Introduced: Day 32.*

### Value accrual
**Field:** The strategic question of which layer of the agent stack (model / infra / app) captures the most economic value as the market matures.

The Social Capital primer's claim — and one of the open debates of 2026 — is that value is migrating up from the model layer (which is becoming commoditized) toward infrastructure (where Capsule, MCP servers, observability platforms compete) and applications (vertical agents in finance, legal, ops). The cohort should form their own view by Day 35. *Introduced: Day 34.*

### Workflow (vs. agent loop)
**Field:** A *fixed, predefined* sequence of steps — sometimes with branches and loops, but the topology is authored, not discovered at runtime.

Workflows are *more reliable* than open-ended agent loops because the control flow doesn't depend on model judgment. They are *less flexible* because they can only handle pre-anticipated paths. The right answer for most production systems is "workflow for the spine, agent loops at the leaves." *Introduced: Day 34.*

---

## Acronyms (quick reference)

| Acronym | Expansion | Note |
|---|---|---|
| A2A | Agent-to-Agent | Emerging protocol for inter-agent calls |
| CoT | Chain-of-thought | Reasoning-before-answer pattern |
| CVE | Common Vulnerabilities and Exposures | e.g., CVE-2025-32711 (EchoLeak) |
| HITL | Human-in-the-loop | Governance pattern: human approval gate |
| MCP | Model Context Protocol | Anthropic-originated tool-exposure standard |
| MoE | Mixture-of-Experts | Sparse model arch; from Phase 1 |
| ReAct | Reasoning + Acting | The canonical agent loop pattern (Yao 2022) |

---

## Concept-graph anchors

Glossary terms are also nodes in `docs/kb/concepts.json` (v0.1). Use the IDs below to follow cross-references through the curriculum:

| Concept-graph ID | Glossary term |
|---|---|
| `agent.loop` | Agent loop |
| `agent.react` | ReAct |
| `agent.tool` | Tool |
| `agent.mcp` | MCP |
| `agent.governance.blast_radius` | Blast radius |
| `agent.governance.sandbox` | Sandboxing |
| `agent.injection.indirect` | Indirect prompt injection |
| `agent.injection.echoleak` | EchoLeak (CVE-2025-32711) |
| `agent.multi.routing` | Routing |
| `agent.drift.long_horizon` | Long-horizon drift |
| `agent.value_accrual` | Value accrual |
