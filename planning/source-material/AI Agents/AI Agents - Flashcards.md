# AI Agents — Flashcards

*Spaced-repetition flashcards for Week 7. Format: `Q` on one side, `A` on the other. Use Anki, Mochi, or any SR tool — or just cover the answer column and self-test. ~55 cards organized by day, plus a numerical-anchor set for high-yield facts.*

---

## Day 31 — The Agent Loop

| # | Q | A |
|---|---|---|
| 1 | What is the single structural property that separates an agent from a chatbot? | The agent runs in a loop (Perceive → Plan → Act → Observe → Repeat). A chatbot returns one response per request and stops. |
| 2 | Name the four steps of the ReAct / agent loop in order. | Perceive → Plan → Act → Observe. (Then repeat.) |
| 3 | What does the *Plan* step of the loop usually consist of, technically? | A chain-of-thought (CoT) reasoning pass: the model writes its next intent in natural language before emitting a tool call. |
| 4 | What paper introduced the ReAct pattern? | Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," arXiv:2210.03629 (2022). |
| 5 | Name the "four converging capabilities" that made agents viable. | Foundational models, new architectures (MoE/MLA), reasoning (CoT + o1-style inference-time), ability to act and course-correct (ReAct + tool protocols). |
| 6 | Of the four capabilities above, which was the *last* to mature? | Ability to act and course-correct — late 2022/2023 with ReAct + first tool-use APIs. The other three had matured earlier. |
| 7 | When does an agent loop terminate? | When goal reached, max step count hit, or agent declares failure. Step caps are a governance control. |

---

## Day 32 — Tools & MCP

| # | Q | A |
|---|---|---|
| 8 | Define "tool" in the agent sense, in one sentence. | A function exposed to the agent — with name, description, typed parameters, return type — that the model can invoke in the *Act* step. |
| 9 | What does MCP stand for and who originated it? | Model Context Protocol; originated by Anthropic; now an open standard. |
| 10 | What concrete problem does MCP solve? | Every framework re-implemented its own tool-calling format. MCP standardizes the *interface*, so a tool published once can be consumed by any MCP-aware client. |
| 11 | Name three MCP-aware clients (mid-2026). | Claude Desktop, Cursor, VS Code Copilot (others: custom agents using the MCP SDKs). |
| 12 | What does `capsule mcp --output` produce? | An MCP server manifest exposing Capsule CLI commands as agent-callable tools (list-machines, deploy-model, benchmark, etc.). |
| 13 | What is A2A, and how does it relate to MCP? | Agent-to-Agent protocol. A2A is to multi-agent delegation what MCP is to tool calls — a standard interface so agents from different teams interoperate. |
| 14 | Two rules of good tool design? | (1) Narrow — one job per tool. (2) Self-describing — the description field is what the model reasons over; write it as if a junior dev had to use the tool. |

---

## Day 33 — Governance & Security

| # | Q | A |
|---|---|---|
| 15 | Define "blast radius" in one sentence. | The maximum harm an agent can cause if compromised, as a function of its tools and credentials. |
| 16 | What is direct vs indirect prompt injection? | Direct: the user themselves embeds instructions to override the system prompt. Indirect: the attacker controls *retrieved data* (doc, web page, email) the agent reads. |
| 17 | Why is indirect injection more dangerous than direct? | The user's intent is benign — they only asked the agent to read a document — so the attack rides on the agent's normal operation. No suspicious user behavior to flag. |
| 18 | What is EchoLeak? | CVE-2025-32711 — an indirect-prompt-injection vulnerability in Microsoft 365 Copilot. Adversary-controlled documents triggered exfiltration via Copilot's own tools. |
| 19 | EchoLeak: was it fixed by patching the model or by scoping the tools? | Scoping the tools (and the outbound capabilities of the agent), not the model. The model behaved as designed; the *blast radius* was the bug. |
| 20 | One concrete sandboxing technique for a deployment agent? | Ephemeral containers with scoped credentials and a network-egress allow-list. |
| 21 | What are agent "traces"? | Structured logs of every loop iteration: prompts, model responses, tool calls, tool outputs, errors. Required for debugging and audit. |
| 22 | Why doesn't training the model to "refuse harmful requests" solve the injection problem? | Because injected instructions look like *normal data* to the model. The classification problem ("is this an instruction I should obey?") is exactly what the model is bad at. Governance constrains *what tools the model can call*, not *what it tries to do*. |
| 23 | One hallucination defense from Week 6 Day 29 that also functions as governance? | Requiring citations / quoted evidence. If the agent must point to source text for every claim, injected instructions that aren't in the source can't be obeyed without breaking the citation contract. |

---

## Day 34 — Orchestration & Multi-Agent

| # | Q | A |
|---|---|---|
| 24 | One sentence: why use multiple agents instead of one? | Specialized agents with narrow blast radii are safer and more debuggable than one omni-agent with admin rights across every domain. |
| 25 | One sentence: why *not* use multiple agents? | You add an orchestration problem to your reasoning problem; coordination failures often dwarf the per-agent wins. |
| 26 | What is "long-horizon drift"? | The compounding-error problem: per-step success probability multiplies across the chain, so long plans collapse fast. |
| 27 | A 10-step plan with 90% per-step success — joint success rate? | 0.9¹⁰ ≈ 35%. |
| 28 | Same plan but 95% per-step success — joint rate? | 0.95¹⁰ ≈ 60%. |
| 29 | Same plan at 99% per-step — joint rate? | 0.99¹⁰ ≈ 90%. |
| 30 | Four defenses against long-horizon drift? | (1) Shorten the chain (decompose differently). (2) Raise per-step reliability (better prompts/tools). (3) Checkpoint + resume. (4) Human gates at high-stakes steps. |
| 31 | "Workflow" vs "agent loop" — one-line difference? | Workflow has *authored* control flow. Agent loop has control flow *discovered at runtime* by model judgment. |
| 32 | Pragmatic production pattern using both? | Workflow for the spine, agent loops at the leaves. |
| 33 | Name two agent frameworks from the HuggingFace Agents Course Unit 2. | smolagents (minimal flat-loop) and LangGraph (graph-based state machine). LlamaIndex agents also covered. |
| 34 | What is the "value-accrual" debate, in one sentence? | Where does economic value land as the agent market matures: in the model layer, the infra layer, or the application layer? |

---

## Day 35 — Phase 2 Synthesis

| # | Q | A |
|---|---|---|
| 35 | Name the 5 layers of the agent stack. | Intelligence → Action → Governance → Orchestration → Economic. |
| 36 | What does the Action layer add that the Intelligence layer cannot? | The ability to *do* things in the world. Tools, MCP, side effects, observable outcomes. |
| 37 | What does the Governance layer add that the Action layer cannot? | Bounds on consequences. Blast-radius limits, sandboxes, audit trails, human gates. |
| 38 | What does the Orchestration layer add that the Governance layer cannot? | Coordination across multiple agents / multiple steps. Routing, workflows, retries, fallback. |
| 39 | What does the Economic layer add that the Orchestration layer cannot? | Sustainability — business models, pricing, value capture across the stack. |
| 40 | What's the connection between agent design (Day 34) and Capsule operations (Day 36+)? | Capsule exposes operations as MCP tools (`capsule mcp`). An agent driving Capsule *is* a deployment agent. The Action layer for that agent is the Capsule CLI. |

---

## Numerical-anchor cards (high-yield facts)

| # | Q | A |
|---|---|---|
| N1 | Year and arXiv ID of the ReAct paper. | 2022; arXiv:2210.03629. |
| N2 | CVE ID and year of EchoLeak. | CVE-2025-32711; disclosed 2025. |
| N3 | Joint success of a 10-step plan at 90% per step. | ~35% (0.9¹⁰). |
| N4 | Joint success of a 10-step plan at 95% per step. | ~60% (0.95¹⁰). |
| N5 | Joint success of a 10-step plan at 99% per step. | ~90% (0.99¹⁰). |
| N6 | Joint success of a 3-step plan at 90% per step. | ~73% (0.9³). |
| N7 | The originator and year of MCP. | Anthropic, late 2024 announcement; broad adoption through 2025. |
| N8 | Two of the most-cited agent frameworks taught in HuggingFace Agents Course. | smolagents, LangGraph. |
| N9 | One framework not from Anthropic that adopted MCP. | Cursor (also VS Code Copilot, plus many self-hosted clients). |
| N10 | The four converging capabilities — what year was the *latest* of them broadly available? | 2022–2023 (ReAct + first tool-use APIs). The other three were earlier. |

---

## How to use these cards

- **Day-tier (1–40):** spaced repetition, daily review during Week 7. Aim for ≥85% recall by Day 35.
- **Numerical-anchor tier (N1–N10):** these are the facts that pass the "would an Oxmiq engineer expect a recent grad to know this cold?" test. If you can't answer N3–N6 instantly, you don't yet have the long-horizon-drift intuition you need.
- **Calibration check (end of week):** if your self-rated confidence on a card is high but you got it wrong, mark it; those cards are your real study set for Day 35 consolidation.
