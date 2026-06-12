# AI Agents — Problem Sets

*Graded exercises for Week 7. Each day has 5 problems of increasing difficulty. Problems marked ★ are required; ☆ are stretch. Most problems involve building or red-teaming a real agent — use smolagents, LangGraph, or a hand-rolled loop, as you prefer. All artifacts (manifests, traces, scripts) should be committed.*

**Submission format:** one markdown file per problem set, with each problem's solution including (a) the prompt(s) / code, (b) the trace or output, (c) your analysis. Commit to your `practice/week-07/` folder.

---

## Problem Set 31 — The Agent Loop

### Problem 31.1 ★ — Loop dissection

Take any prebuilt agent demo (HuggingFace Agents Course Unit 1 demo, smolagents quickstart, or LangGraph hello-world). Run it on one task. Capture the full trace. Annotate each line as Perceive / Plan / Act / Observe. Identify any line that doesn't cleanly fit one of the four — explain why.

### Problem 31.2 ★ — Sketch a real-world loop

Pick a task you yourself did this internship (e.g., "ran a benchmark on a quantized model"). Sketch it as a 5-step agent loop. For each step, write the Perceive input, the Plan reasoning, the Act tool call, and the Observe check. Estimate per-step success probability (be honest) and compute joint success of the whole 5-step plan.

### Problem 31.3 ★ — The chatbot/agent boundary

Find a tool you use that you're not sure whether to call an "agent" or a "chatbot" (e.g., ChatGPT with web search, Cursor's chat panel, Claude with computer-use). Apply the loop test: does it run in a loop without your intervention? Make the call. Defend with one paragraph citing the loop's presence or absence.

### Problem 31.4 ☆ — Step-cap experiment

Build the simplest possible ReAct loop (≤30 lines, smolagents or vanilla). Cap it at 3 steps, run a task that needs 5+. Now cap it at 20, run the same task. Report what happens at each cap. Argue: should step caps be configured by the developer or learned by the model?

### Problem 31.5 ☆ — The "four capabilities" stress test

Of the four converging capabilities (foundational models, new architectures, reasoning, tool use), remove one mentally and predict what would break. Then find a *real published agent failure* from the last 12 months and argue which of the four was insufficient. Cite the source.

---

## Problem Set 32 — Tools & MCP

### Problem 32.1 ★ — Write a tool description

Pick one Capsule command (e.g., `capsule list --filter`). Write its MCP-style tool description from scratch: name, description (≥2 sentences, written for the model not the human), parameter schema with types, return type. Now have a peer read only your description (not the command's real docs) and try to use the tool. Note what they got wrong and what you'd revise.

### Problem 32.2 ★ — Narrow vs broad tools

Compare two tool designs for the same job:
- **Broad:** one tool `run_capsule(args: string)` that takes any CLI args.
- **Narrow:** five tools, one per Capsule sub-command (`list_machines`, `start_session`, `run_benchmark`, …).

Run the same agent task with each design. Which produced fewer wrong calls? Which produced better traces? Argue which design is appropriate when, in one paragraph.

### Problem 32.3 ★ — MCP server walkthrough

Spin up a minimal MCP server (any language; the [MCP Python SDK quickstart](https://modelcontextprotocol.io/quickstart) works). Expose two tools: `echo` and `current_time`. Connect it from Claude Desktop or Cursor. Make a screenshot of the model calling each tool. Submit screenshot + the server source.

### Problem 32.4 ☆ — The brittle-tool exercise

Design a tool that *looks* obviously good but breaks an agent. Possibilities: ambiguous name (`get_data`), overloaded parameter (a single string that's parsed several ways), silent failure on bad input. Demonstrate the failure mode in a trace. Propose the fix.

### Problem 32.5 ☆ — A2A sketch

Pick a two-agent system you would actually want (e.g., "researcher agent" + "writer agent"). Sketch the A2A-style interface between them: what does the researcher's "result" look like as a typed payload? What does the writer accept as input? Write the schemas and one paragraph on why this contract is the right granularity.

---

## Problem Set 33 — Governance & Security

### Problem 33.1 ★ — Three injection attacks

Design *three* prompt-injection attacks against a deployment agent that runs Capsule commands. One direct, one indirect (via a malicious document in OneDrive), one indirect via a malicious tool description from a third-party MCP server. For each, describe the attack surface, the payload, and what the attacker gets.

### Problem 33.2 ★ — Three defenses

For each attack from 33.1, design a defense. At least one defense should be a *governance* control (blast-radius reduction) and at least one should be an *observability* control (the attack is detectable post-hoc even if not prevented). For each defense, identify what it costs (latency, complexity, UX friction).

### Problem 33.3 ★ — EchoLeak post-mortem

Read the CVE entry for [CVE-2025-32711 (EchoLeak)](https://www.cve.org/CVERecord?id=CVE-2025-32711). Write a 1-page post-mortem: (a) the attack chain in plain English, (b) which layer of the agent stack should have caught it, (c) one Microsoft-side fix and one user-side mitigation an enterprise admin could have deployed before the patch.

### Problem 33.4 ☆ — Trace forensics

Take any agent trace (yours from 31.1 or any open dataset). Inject *plausible-looking but harmful* tool calls into the middle of the trace. Show the modified trace to a peer. Ask them to identify the injected calls. Report how long it took them, and what tell-tales gave it away.

### Problem 33.5 ☆ — The blast-radius worksheet

For an agent you'd actually deploy (pick one — customer support, code review, deployment, RAG over wiki), enumerate every tool it would have, every credential it would hold, and every external system it could affect. Write a 5-line "in the worst case, this agent could…" statement. Then propose 3 changes that reduce the radius without crippling the function.

---

## Problem Set 34 — Orchestration & Multi-Agent

### Problem 34.1 ★ — Two-agent routed system

Build a 2-agent system: a *router* that classifies incoming requests into "code question" vs "general question," and two specialist agents downstream. Use smolagents or LangGraph. Run 10 requests through it. Report: routing accuracy, latency overhead vs single-agent baseline, and one example where routing helped and one where it hurt.

### Problem 34.2 ★ — Long-horizon math

Compute the joint success probability for plans of length 3, 5, 10, and 20 steps at per-step success rates of 80%, 90%, 95%, and 99%. Produce a 4×4 table. Then circle the cell that represents the threshold where you'd say "this is no longer reliable enough to ship without human checkpoints." Defend your threshold.

### Problem 34.3 ★ — Workflow vs loop

Take one task that *should* be a workflow (e.g., "every nightly: pull data → run report → email it") and one that *should* be an open agent loop (e.g., "debug a failing test, the failure mode is unknown"). Argue why each is in its category. Then propose a *hybrid* design — workflow spine with an agent loop at one specific leaf node. Sketch it.

### Problem 34.4 ☆ — Drift-recovery experiment

Build an agent that does a 5-step plan with one deliberately flaky tool (e.g., 50% chance of returning a bad result). Run it 20 times. How often does the agent recover vs how often does it commit to a wrong intermediate result and never recover? What single prompt change most improved recovery?

### Problem 34.5 ☆ — Value-accrual essay

Write a 500-word memo (audience: a VC who has read Social Capital's primer): *Where will value accrue in the agent stack over the next 24 months — model, infra, or application layer?* Cite at least three real companies (e.g., Anthropic, Oxmiq, Cursor, Glean, Harvey, …) as evidence for your argument. Be willing to disagree with the primer.

---

## Problem Set 35 — Phase 2 Synthesis

### Problem 35.1 ★ — The 5-layer map

For the agent you sketched in 33.5, label *every component* with which of the 5 layers it lives in (Intelligence / Action / Governance / Orchestration / Economic). If a component spans two layers, say which two and why. Submit as a single annotated diagram.

### Problem 35.2 ★ — Connect to Phase 1

For your sketched agent: identify *three* Phase-1 (inference engineering) decisions that materially affect the agent's behavior (e.g., model choice → CoT quality; quantization → tool-call accuracy; KV-cache budget → context length per loop iteration). For each, explain the causal chain in one paragraph.

### Problem 35.3 ★ — The teach-back

Pick one concept from Days 31–34 you'd most want to teach a peer. Write a 5-minute mini-lesson: hook, definition, worked example, common confusion, one question to test understanding. (You may be asked to actually deliver it on Day 35.)

### Problem 35.4 ☆ — Pre-Phase-3 connection

Looking ahead to Capsule Power-User (Days 36–45), name *three* points where the agent-stack vocabulary will reappear. Be specific: "MCP from Day 32 reappears at Day 44 as `capsule mcp`" — but give your own three.

### Problem 35.5 ☆ — Open question for your future self

Write the *one* open question you have about agents that this curriculum did not answer. (We collect these and feed them into next year's curriculum design.)

---

## Appendix — Per-set difficulty index

| Set | Easiest | Hardest | Required total |
|---|---|---|---|
| 31 | 31.1 | 31.4 | 3 ★ |
| 32 | 32.1 | 32.4 | 3 ★ |
| 33 | 33.1 | 33.4 | 3 ★ |
| 34 | 34.2 | 34.5 | 3 ★ |
| 35 | 35.1 | 35.5 | 3 ★ |

Total required problems for the week: **15** (the ★ problems). Stretch problems are scored separately and contribute to the "engineering reasoning" rubric line in the capstone.

---

## Appendix — Concept-graph IDs covered

| Problem | Concept IDs |
|---|---|
| 31.1, 31.2 | `agent.loop`, `agent.react` |
| 32.1, 32.2, 32.3 | `agent.tool`, `agent.mcp` |
| 32.5 | `agent.a2a` |
| 33.1, 33.2 | `agent.injection.indirect`, `agent.governance.blast_radius`, `agent.governance.sandbox` |
| 33.3 | `agent.injection.echoleak` |
| 34.1, 34.3 | `agent.multi.routing`, `agent.workflow` |
| 34.2, 34.4 | `agent.drift.long_horizon` |
| 34.5 | `agent.value_accrual` |
| 35.x | (synthesis — all of the above) |
