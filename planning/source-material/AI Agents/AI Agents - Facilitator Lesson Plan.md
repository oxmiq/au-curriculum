**AI Agents**

**The 5-Layer Stack**

*Facilitator Lesson Plan*

5 modules • 90 minutes each • intro-level students

*Pair with the Student Guide and module Worksheets.*

**Course Overview**

**Audience**

Intro-level students with limited or no prior machine-learning background. Comfortable with computers but not necessarily programmers. Adult learners or upper-undergraduate.

**Format**

Five 90-minute modules, designed for one session per week (5 weeks). Each module follows the same structural rhythm so students know what to expect:

| **Time** | **Segment** | **Purpose** |
|----|----|----|
| 10 min | Recap & framing | Connect to prior module; state today's objectives. |
| 20 min | Core concept lecture | Deliver the durable ideas. Use slides 1–8 of the module. |
| 15 min | Worked example | Walk through the case study in the Student Guide. |
| 20 min | Exercise or discussion | Worksheet activity or structured pairs/groups. |
| 15 min | Critical analysis | Push-back; opposing views; what could be wrong. |
| 10 min | Synthesis & preview | Tie back to objectives; preview next module. |

**Materials Per Session**

- Slide deck (one master .pptx with all 5 modules; advance to the module's section).

- Printed or digital copies of the Student Guide chapter for that module.

- Printed Worksheet for the module's exercise.

- Whiteboard or shared digital canvas for the discussion segment.

**Facilitator Mindset**

The goal is not to make students experts; it is to give them a durable conceptual map and the confidence to keep learning. Three practical tips:

- Push back on hype. The primer's revenue numbers and growth curves are useful for framing but speculative. Encourage students to ask "what would change my mind?"

- Make abstractions concrete. Every concept (MoE, ReAct, MCP) has a worked example. Use it; don't define and move on.

- Reward good questions over right answers. The field changes monthly; students who learn to ask good questions will outlast students who memorize today's facts.

**Reading Assignments**

Before each module, students should read the corresponding chapter in the Student Guide (~6–8 pages). Optionally, they can dip into one of the primary sources in Appendix B.

**Assessment (Suggested)**

- Weekly worksheet completion (30%).

- Module-end short-answer reflection (30%).

- Final project: design an agent system for a real-world workflow, with at-risk weak points identified and architectural mitigations proposed (40%).

**Module 0: Why Now? The Agentic Explosion**

**Objectives**

- Students can define an agent and contrast it with a chatbot.

- Students can name the four converging capabilities behind the agentic explosion.

- Students can cite three pieces of evidence the era has begun.

**Timed Agenda**

| **Time** | **Segment** | **Activity** |
|----|----|----|
| 0–10 | Welcome & framing | Introduce the course arc (5 layers + this intro). Show the 5-layer overview slide. Ask: "What's the difference between Siri and an AI agent?" Collect 4–5 answers on the board. |
| 10–30 | Lecture: Calculator → Strategist | Walk through the agent loop diagram (Perceive/Plan/Act/Observe). Contrast chatbot (one prompt → one response) with agent (closed loop). Cover the four capabilities: foundational models, new architectures, reasoning, action+correction. |
| 30–45 | Worked example | Flight-booking scenario from the Student Guide. Solo (3 min) then pair (5 min): write what a chatbot would do vs. what an agent would do. Debrief together (7 min). |
| 45–65 | Exercise — Worksheet 0 | Students complete Worksheet 0 in pairs. Walk the room; answer questions; pull two pairs to share answers at minute 60. |
| 65–80 | Critical analysis | Show the Anthropic ARR slide and the IDC projections. Ask: "What numbers do you trust? What would you want to verify?" Hold a 10-minute structured discussion using the questions in the Student Guide. |
| 80–90 | Synthesis & preview | Revisit objectives. Preview Module 1 (Intelligence Layer). Assign reading. |

**Talking Points the Facilitator Should Land**

- "The loop is the agent." If students remember nothing else, they should remember this.

- Hype is real; capability is also real. Don't dismiss either.

- Coding is the first scaled domain because it has fast, verifiable feedback (the code compiles or it doesn't). Other domains will follow as their feedback signals get better.

**Common Misconceptions**

- "An agent is just a smarter chatbot." — No. The structural property that defines an agent is the loop and the ability to act on the world.

- "AGI is here." — No. Agents are narrow, brittle, and break in predictable ways (which we'll cover in Module 5).

- "My company should adopt agents everywhere." — Almost certainly no. McKinsey 2025 found fewer than 10% of organizations have scaled agents in any single function.

**Discussion Prompts**

- If you could deploy one agent at your school or workplace this week, what task would it do? What could go wrong?

- Whose interest is best served by the framing that "AI agents are inevitable"? Whose interest is harmed?

> *Tip: end this discussion before it becomes a referendum on AI in general. Keep it task-focused.*

**Module 1: The Intelligence Layer**

**Objectives**

- Students can identify the three pillars: reasoning, memory, knowledge.

- Students can explain MoE, MLA, and RAG in their own words.

- Students can decide when RAG is preferable to a long context window.

**Timed Agenda**

| **Time** | **Segment** | **Activity** |
|----|----|----|
| 0–10 | Recap & framing | Quick recap: "What is an agent loop?" One-word answers around the room. Today: what's inside the box that the loop wraps. |
| 10–35 | Lecture: Three pillars | Use the temple diagram (3 pillars holding up Agent Action). Cover MoE with the Mixtral 47B/13B example. Cover MLA with the KV-cache cost-explosion framing. Cover RAG with the company-knowledge example. |
| 35–50 | Worked example | Tax-research agent from the Student Guide. Walk through how each pillar contributes. |
| 50–70 | Exercise — Worksheet 1 | Map a real model (Mixtral) to the three pillars. Then: "You have a 1B-token corpus of medical documents. Long context window or RAG — defend your answer." |
| 70–85 | Critical analysis | Discuss: are these architectural innovations durable advantages, or are they commodities? (Hint: the primer argues they're becoming commodities. Push students to find counter-evidence.) |
| 85–90 | Synthesis & preview | Recap objectives. Preview Module 2. |

**Talking Points**

- Each technology fixes one specific weakness; none substitutes for another.

- Sparse MoE is borrowed from neuroscience — specialization saves energy in brains and models alike.

- RAG is not magic; it's a search problem with a generation step at the end. The quality of the search dominates.

**Common Misconceptions**

- "Bigger model = better." Not always; routing the right model to the right task matters more (foreshadows orchestration).

- "A long context window replaces RAG." In some workflows, yes. For enterprise corpora that exceed any feasible context, no.

**Discussion Prompts**

- If the model layer is becoming a commodity, where in the stack would you invest your career?

- Citations are touted as RAG's safety feature. What attacks on citations can you imagine?

**Module 2: The Action Layer**

**Objectives**

- Students can define the execution gap and the ReAct loop.

- Students can distinguish API, MCP, and A2A.

- Students can list the three observability metrics.

**Timed Agenda**

| **Time** | **Segment** | **Activity** |
|----|----|----|
| 0–10 | Recap & framing | Recap Module 1's three pillars. Question: "What's the difference between thinking and doing?" Today's module is the bridge. |
| 10–35 | Lecture: From thinking to doing | Walk through the execution-gap diagram, then the ReAct loop. Explain how an LLM's text becomes a tool call via the agent harness. Cover APIs / MCP / A2A with the "USB-C for AI" metaphor for MCP. |
| 35–50 | Worked example | Continue the flight-booking agent from Module 0, but now show the full ReAct trace with tool calls and observations. |
| 50–70 | Exercise — Worksheet 2 | In pairs, students trace a ReAct loop for a different task (e.g., "summarize my unread emails and draft a reply to the most urgent"). They identify each Act step and which protocol it uses. |
| 70–85 | Critical analysis | MCP is described as a universal standard. What's the historical track record of "universal standards"? (Hint: USB-C took 10+ years; HTTPS took longer.) Why might MCP succeed faster? |
| 85–90 | Synthesis & preview | Preview Module 3. Teaser: if agents can act, what stops them from acting wrongly? |

**Talking Points**

- "The model never runs anything directly. It writes an instruction. The harness interprets it." Drill this point — students often imagine the model as a hands-on actor.

- Observability is not a feature of the model — it has to be built into the harness deliberately.

- Tools that fail silently are the most expensive failure mode at scale.

**Common Misconceptions**

- "MCP is a new programming language." No — it's a protocol for exposing functions to agents.

- "Multi-agent systems are smarter." Sometimes. Often they multiply errors. Discuss carefully.

**Discussion Prompts**

- If a tool returns wrong data, who is responsible — the tool owner, the agent operator, or the model provider?

- What's the smallest agent you could build today that would be genuinely useful in your daily life?

**Module 3: The Governance Layer**

**Objectives**

- Students can explain why governance must be architectural, not just trained-in.

- Students can describe prompt injection (direct and indirect) with at least one real example.

- Students can name and justify the four components of machine-checkable security.

**Timed Agenda**

| **Time** | **Segment** | **Activity** |
|----|----|----|
| 0–10 | Recap & framing | Yesterday's tools gave the agent hands. Today: what stops it from doing harm? Prime the class with: "An ambient agent with broad permissions is an attack surface that never sleeps." |
| 10–35 | Lecture: Ambient AI and prompt injection | Cover the ambient AI problem. Walk through direct vs. indirect prompt injection with the EchoLeak case study (CVE-2025-32711, June 2025). Use the attack-flow diagram. |
| 35–50 | Worked example | Legal-team contract-summary agent from the Student Guide. Show the attack and the architectural defenses side by side. |
| 50–70 | Exercise — Worksheet 3 | Students take a sample document and identify possible prompt-injection vectors. Then they list the architectural controls that would block each. Time-box hard: 8 min individual, 8 min pairs, 4 min debrief. |
| 70–85 | Critical analysis | Debate (5 min in pairs, 10 min plenary): "Resolved: alignment training will eventually make architectural governance unnecessary." Assign sides randomly. |
| 85–90 | Synthesis & preview | Preview Module 4. Teaser: if governance constrains what agents may do, orchestration decides what they actually do. |

**Talking Points**

- "Code is harder to argue with than a model." — a phrase students should leave with.

- EchoLeak is not theoretical; it was zero-click, in a flagship product, in 2025. The threat is here.

- Whitelisting tools is restrictive on purpose. Permissive defaults are the bug.

**Common Misconceptions**

- "Just train the model better." Training is necessary but never sufficient. A model can always be talked out of a preference; code cannot.

- "My company doesn't have sensitive data." Everyone does — customer lists, payroll, contracts, internal communications.

**Discussion Prompts**

- Whose job is it to design the governance layer — engineering, security, legal, or product? Defend your choice.

- If governance is layered, where would you place the strictest controls — closest to the model, closest to the tool, or in between?

> *Sensitive topic note: students may share personal experiences with AI-related security incidents. Be supportive but keep the discussion architectural, not anecdotal.*

**Module 4: The Orchestration Layer**

**Objectives**

- Students can define orchestration as the control plane of an agentic system.

- Students can compare the four orchestration approaches along key dimensions.

- Students can argue why orchestration may accrue durable value.

**Timed Agenda**

| **Time** | **Segment** | **Activity** |
|----|----|----|
| 0–10 | Recap & framing | Recap governance. Today: the layer that decides what the agent actually does. Show "agents are a new programmable computer" framing. |
| 10–35 | Lecture: Control plane and four approaches | Cover the responsibilities of orchestration. Compare Claude Code, Claude CoWork, OpenAI Codex, OpenClaw — emphasize what each prioritizes. Touch on NemoClaw for hardware-level enforcement. |
| 35–50 | Worked example | Multi-agent customer-service system. Walk through the four-agent design and how state moves between them. |
| 50–70 | Exercise — Worksheet 4 | Pairs: design an orchestration plan for a 5-step customer-onboarding workflow. Decide which steps use a cheap model, which use a frontier model, where to put human review. |
| 70–85 | Critical analysis | If models commoditize, what stops the model labs from absorbing orchestration themselves? Discuss the historical analogue (cloud providers absorbing developer tools). |
| 85–90 | Synthesis & preview | Preview Module 5: the economics. |

**Talking Points**

- "Same model, different value." Repeat this. Two teams with identical models can have wildly different outcomes.

- Open-source orchestration is processing tens of trillions of tokens per month. The bet that orchestration is durable is being placed by serious people.

- Hardware-level security (NemoClaw) is the wedge into regulated industries — finance, healthcare, legal.

**Common Misconceptions**

- "More agents = better." Multi-agent systems compound errors; only use them when single-agent solutions are clearly insufficient.

- "Orchestration is just glue code." Glue code is hard. It's also where most of the production work lives.

**Discussion Prompts**

- If you could only own one layer of the stack — model, harness, governance, orchestration, or application — which would you pick and why?

- Where in the four orchestration approaches would you place your bet for the next 5 years?

**Module 5: The Economic Layer (and What Comes Next)**

**Objectives**

- Students can explain why price-per-completed-task is the right metric.

- Students can list the four weak points of current agents and map each to a category of infrastructure innovation.

- Students can form a defensible view on where value accrues.

**Timed Agenda**

| **Time** | **Segment** | **Activity** |
|----|----|----|
| 0–10 | Recap & framing | Recap all four prior layers. Today: the layer underneath everything — money. And what comes next. |
| 10–30 | Lecture: Economics | Cover the three forces: licensing shift (Salesforce Headless 360 / Agentforce), deflationary inference (1000× in 3 years), build vs. buy. Then walk through the cost of failure and the table comparing cloud/hybrid/local. |
| 30–50 | Lecture: Weak points + Frontier | Cover the four weak points (long-horizon drift, edge cases, security, hidden human cost). Use Amazon Q and Claude Code leak as case studies. Then the six frontier case studies: solo company formation (OpenClaw), Shopify agentic commerce, Klarna customer service, investment due diligence, SemiAnalysis, 8090. |
| 50–70 | Exercise — Worksheet 5 | Students compute cost-per-task for a 10-step agent given assumptions (token cost, failure rate, intervention cost). Then they propose one architectural change that lowers it. |
| 70–85 | Critical analysis | Final discussion: Where does value accrue? Use the Synthesis questions in the Student Guide. Frame as a five-minute opinion + five-minute pushback per student. |
| 85–90 | Course wrap | Tie back to the four foundational questions. Final project briefing: "Design an agent system for a real-world workflow you know. Identify the weak points and the architectural mitigations." |

**Talking Points**

- Token cost is a sliver of true cost. Retries, failures, human cleanup dominate.

- Deflationary inference is what makes today's agents viable that wouldn't have been viable in 2023. It also distorts pricing — providers are subsidizing the buildout.

- Every weak point is a category of infrastructure waiting to be built. This is the opportunity space.

**Common Misconceptions**

- "AI agents are cheap." They are, per token. Per completed task in production, they often aren't.

- "The model wins." The model still matters — it sets the ceiling — but the workflow owner captures the durable value.

**Final Discussion Prompts**

- If you had to start a company today building agent infrastructure, which weak point would you tackle? Why?

- In 10 years, will most knowledge workers be managing agents, or will most agents be managing other agents? Defend your view.

> *Reserve the final 5 minutes for student questions, gratitudes, and pointing to Appendix B for further reading. Don't end with a lecture.*

**Appendix: Practical Facilitation Notes**

**Adapting for Shorter Sessions**

If you must compress a module to 60 minutes:

- Cut the exercise portion to 10 minutes and assign the worksheet as homework.

- Keep the lecture, the worked example, and the critical analysis. These compound across the course.

- Reserve the synthesis + preview — it's the connective tissue that makes the course feel coherent.

**Adapting for Larger Cohorts**

With more than 30 students, switch from "raise your hand" to silent polling (Mentimeter, Slido) for the discussion segments. The point is to surface a distribution of views, not to perform for the room.

**Online / Remote Delivery**

- Use breakout rooms for the worksheet exercises. 3 students per room is ideal.

- Have students post answers in a shared doc rather than verbal-only sharing — it captures the conversation.

- Encourage video on for the discussion segments; off is fine for lecture.

**When the Class Pushes Back**

Some students will push back on the premise that agents are useful, or worth learning. Take it seriously. Two responses that work:

- "You may be right that today's agents are limited. The skill of understanding why they're limited is exactly what this course teaches."

- "If you're skeptical, build the strongest version of your skepticism. Where would it be wrong?"

**Suggested Final Project Rubric**

| **Criterion** | **Weight** | **What "excellent" looks like** |
|----|----|----|
| Workflow specificity | 20% | A real, named workflow with stakeholders, inputs, outputs. |
| 5-layer mapping | 30% | Every layer of the stack is addressed; concrete choices made and justified. |
| Weak-point identification | 20% | All four weak points considered; the relevant ones identified with reasoning. |
| Architectural mitigations | 20% | Specific defenses for each identified weak point, beyond "train the model better." |
| Clarity of writing | 10% | A non-expert could read it and act on it. |

---

# Appendix — Instructor Calibration & Failure-Mode Playbook

The body of this plan tells you *what* to teach. This appendix tells you *what tends to go wrong* in each module, what success looks like quantitatively, and how to compress when you lose time. Use this on Sunday night before the week's session.

## How to use this appendix

Each module gets four blocks:

1. **Top 3 student failure modes** — the misconceptions you'll see in worksheets and discussion. If you don't surface and correct them in class, they'll show up in the final project.
2. **Success metric checklist** — what you should hear/see by the end of the 90 minutes. If 3 of 5 items aren't visible, the module didn't land — plan a 10-minute fix at the start of the next session.
3. **Compression variants** — how to deliver the same module in 60 / 120 / 180 minutes.
4. **Numerical anchors to bring** — the 2–3 numbers worth writing on the board verbatim.

---

## Module 0 — Why Now?

**Top 3 failure modes**

1. *"An agent is just a fancier chatbot."* Students collapse the distinction. Fix: force them to draw the closed loop on paper. A chatbot is a function; an agent is a control loop. Don't move on until every student has drawn perceive→plan→act→observe.
2. *"The revenue numbers prove the market is real."* Students take Anthropic's $7B ARR uncritically. Fix: spend 5 minutes on the difference between *audited revenue*, *annualized run-rate*, and *committed-but-unrecognized*. Have them name the source they would *not* trust.
3. *"All four converging capabilities are equally important."* They aren't. Fix: ask which one, if removed, would kill agents today. (Answer: tool-use / action — without it, an agent is a reasoning toy.)

**Success metric checklist**

- [ ] At least 4 students can articulate the agent vs. chatbot distinction in 1 sentence without prompting.
- [ ] At least one student spontaneously asks "where does the revenue number actually come from?"
- [ ] Hands go up for *all four* capabilities when you ask which one is the bottleneck — heterogeneity means you've made it a real question.
- [ ] Worksheet 0 Part B (Tokyo trip table) has visibly different chatbot vs. agent columns in 80%+ of completed worksheets.
- [ ] Two students reference a *specific real-world agent product* (Cursor, Claude Code, Agentforce, Devin) in discussion.

**Compression variants**

- **60 min**: drop worked example (assign as homework); 15-min lecture; 20-min worksheet pairs; 15-min critical analysis; 10-min synthesis.
- **120 min**: add a 30-min "agent product gallery" — show 4 real products (Cursor, Claude Code, Salesforce Agentforce, Devin); students rate each on autonomy / tool use / loop depth.
- **180 min**: also assign a take-home pre-read of Anthropic's MCP announcement + 20 min in-class discussion of why a *protocol* (not a product) is the unlock.

**Numerical anchors**

- IDC: **28.6M agents projected by 2028** (write source on board).
- Anthropic: ARR **$1B (Dec 2024) → $7B (Aug 2025)** — call out 7× in 8 months.
- Per-task agent cost: ~**3.2× chatbot cost** (12 calls vs. 5, 800 vs. 600 tokens).

---

## Module 1 — The Intelligence Layer

**Top 3 failure modes**

1. *"Bigger model = better agent."* Students conflate model size with agent quality. Fix: show the model-routing example ($0.24 → $0.047 per task) — frontier models for hard sub-problems, small models for everything else.
2. *"RAG is just search."* Students miss that RAG is a *grounding* mechanism that constrains hallucination. Fix: walk through the hospital scenario from Worksheet 1B and ask what happens if the retrieval misses the relevant page.
3. *"Long context will obviate RAG."* Tempting, especially after Gemini 1.5's 2M context. Fix: discuss cost ($3/call at 200K tokens vs. $0.01 for a RAG query) and the **lost-in-the-middle** problem.

**Success metric checklist**

- [ ] Students can name the three pillars (foundation model / context / reasoning) without notes.
- [ ] At least 3 students correctly select small-model-for-routing in a verbal pop-quiz.
- [ ] The cost-of-context tradeoff is mentioned spontaneously in the RAG vs. long-context discussion.
- [ ] Mixture-of-Experts is recognized as a *sparsity* technique, not a "smarter ensemble."
- [ ] One student references a specific reasoning model (o1, o3, Claude Sonnet thinking, DeepSeek R1) by name.

**Compression variants**

- **60 min**: skip MoE deep-dive (mention as 1 slide); skip worksheet Part C; 25-min lecture, 20-min worked example, 15-min discussion.
- **120 min**: add a 30-min "spec a model router" exercise — given 5 sub-tasks, students pick model + justify cost/latency tradeoff using the published price sheet.
- **180 min**: add a hands-on lab — students use OpenRouter or Together AI to compare 3 models on the same prompt; bring laptops.

**Numerical anchors**

- Model-routing savings: naive **$0.24/task** → smart **$0.047/task** = **~5× cheaper**.
- Long-context cost: **$3 per 200K-token call**. RAG equivalent: **$0.01**.
- Mixture-of-Experts (DeepSeek V3): **671B total params, 37B active per token** — ~18× sparsity.

---

## Module 2 — The Tool & Protocol Layer

**Top 3 failure modes**

1. *"Tool use is just an API call."* Misses the loop. Fix: walk a ReAct trace on the board showing how the *result* of one tool call shapes the next plan.
2. *"MCP is just OpenAPI for AI."* Tempting framing, partly right. Fix: emphasize what's *different* — MCP is bidirectional, supports streaming notifications, and is designed for *the model* to discover and invoke tools (not for a human-written client).
3. *"99% tool reliability is plenty."* Misses compounding. Fix: do D2 from Worksheets live: 0.95⁸ = 66%; 0.99⁸ = 92%. The whiteboard moment changes how they design.

**Success metric checklist**

- [ ] Students can trace a 3-step ReAct loop on the board.
- [ ] At least one student correctly distinguishes MCP from a vanilla REST API.
- [ ] Compounding tool-call math (per-call p^N) appears in at least 2 worksheet answers.
- [ ] Students can name 2 real MCP servers from the open ecosystem (Anthropic's reference set: filesystem, github, postgres, slack, brave-search, puppeteer).
- [ ] Discussion surfaces idempotency / retry semantics without prompting.

**Compression variants**

- **60 min**: drop MCP server design exercise; spend full 25 min on ReAct + compounding math. Assign MCP reading + 1-pager as homework.
- **120 min**: add a 30-min "design an MCP server for X" exercise; pairs pick from a list (calendar, GitHub, Notion, internal wiki).
- **180 min**: hands-on — install Claude Desktop or Cursor; connect a public MCP server (filesystem or github); watch the model invoke it. Bring USB sticks with pre-downloaded installers (no wifi guarantees).

**Numerical anchors**

- Reference MCP servers: **~12 first-party** Anthropic ships + **hundreds** in the open ecosystem.
- Tool-call compounding: **0.95⁸ = 0.66**, **0.99⁸ = 0.92** — write this on the board.
- Per-tool latency budget: aim for **<200ms p50** if you want a sub-5-second agent turn with 10+ calls.

---

## Module 3 — Safety, Sandboxing & Trust

**Top 3 failure modes**

1. *"Prompt injection will be fixed soon."* It won't. Fix: cite Simon Willison and the EchoLeak CVE (**CVE-2025-32711**) — *indirect* injection from email is in production today.
2. *"Sandboxing means Docker."* Docker alone isn't enough. Fix: discuss the layers — process isolation, network egress filtering, filesystem scoping, time/CPU limits, ephemeral cleanup. Reference gVisor / Firecracker / E2B / Daytona.
3. *"Audit trails are nice-to-have."* They're regulatory. Fix: mention EU AI Act high-risk system requirements; have students design an audit log schema in 5 minutes.

**Success metric checklist**

- [ ] Students can name the difference between *direct* and *indirect* prompt injection.
- [ ] At least one real incident (EchoLeak, ChatGPT plugin exfiltration, Replit agent file-deletion) gets mentioned.
- [ ] The sandbox blast-radius math (D3 from Worksheets) is referenced — **$5M unmitigated → $50K with full sandbox**.
- [ ] Least-privilege is articulated as a *design* principle, not a "best practice."
- [ ] Worksheet 3 sandbox designs include ≥3 of {isolation primitive, network scope, FS scope, time/CPU limit, cleanup}.

**Compression variants**

- **60 min**: drop audit-trail design; lead with EchoLeak as the hook; 25-min lecture; 20-min sandbox design pairs; 15-min critical analysis.
- **120 min**: add a 30-min red-team — students try to write prompts that would smuggle data out via a tool call.
- **180 min**: add a live demo using a sandboxed environment (E2B or Daytona); have the agent run untrusted code; show the constraints in action.

**Numerical anchors**

- EchoLeak CVE: **CVE-2025-32711**, Microsoft 365 Copilot indirect injection via email, disclosed mid-2025.
- Unmitigated incident cost: **~$50K each**; at 1 per 10K invocations × 1M invocations/year = **$5M/yr** baseline.
- Sandboxing overhead: **<5% latency** on most modern container runtimes; pays back **~1000×**.

---

## Module 4 — Orchestration & Multi-Agent Systems

**Top 3 failure modes**

1. *"More agents = better system."* The opposite is usually true. Fix: each handoff is a serialization boundary and an error multiplier. Cite the Anthropic "Building Effective Agents" piece: start with a single agent + tools; add agents only when necessary.
2. *"Agents will negotiate among themselves."* They won't, reliably. Fix: discuss why deterministic orchestration (LangGraph, Inngest, Temporal) beats emergent coordination today.
3. *"Parallelism is free."* It isn't — handoff cost, merge cost, and consistency reconciliation eat the savings. Fix: walk D4 (40s serial → 32s parallel → 29.6s with caching) and discuss diminishing returns.

**Success metric checklist**

- [ ] Students can name at least one orchestration framework (LangGraph, CrewAI, AutoGen, Inngest, Temporal).
- [ ] The "single agent first" heuristic comes up unprompted.
- [ ] At least one student articulates handoff cost (serialization + context loss).
- [ ] Workshop 4 topology diagrams include a critique of failure modes (cycles, deadlocks, hallucinated handoffs).
- [ ] One student references a real multi-agent product (Devin, MultiOn, Manus, OpenAI Operator).

**Compression variants**

- **60 min**: drop failure-mode discussion; focus on the 5-agent worked example end-to-end.
- **120 min**: add a 30-min "redesign a serial pipeline to parallel" exercise using a real-world workflow (e.g., customer-support triage).
- **180 min**: hands-on — pairs sketch a LangGraph state machine for a chosen workflow and walk through one failure recovery path.

**Numerical anchors**

- Anthropic's guidance: most production agents are **1 agent + N tools**, not N agents.
- Multi-agent latency: serial **40s** → parallel **32s** → with cache **29.6s avg** over 100 runs.
- Per-handoff overhead: **0.5–2 sec** of network + context-rehydration cost on top of model time.

---

## Module 5 — The Business of Agents

**Top 3 failure modes**

1. *"Per-seat pricing will work for agents."* It breaks as soon as heavy users appear. Fix: walk D5 — heavy users are **−$30/month margin** at $50/seat with $0.04/task.
2. *"The moat is the model."* It isn't — models commoditize on a quarterly cadence. Fix: discuss data moats (proprietary corpora), distribution moats (existing user bases), and workflow moats (process embedding).
3. *"Agent economics will improve as inference gets cheaper."* True but misleading. Fix: agent *usage* grows faster than per-token cost falls. Net cost per user is rising for most agent products in 2025-2026.

**Success metric checklist**

- [ ] Students can name **3 pricing models** (per-seat, consumption, per-outcome, hybrid, usage cap).
- [ ] At least one student articulates the heavy-user margin trap with a number.
- [ ] Real-product references: Cursor ($20/mo + usage), Claude Code (consumption), Agentforce (per-conversation), Devin ($500/mo).
- [ ] Discussion surfaces non-model moats (data, distribution, workflow).
- [ ] At least 2 students push back on the "agents will replace all SaaS" thesis with specifics.

**Compression variants**

- **60 min**: drop the moat discussion; spend full time on pricing-model walk-through + worksheet.
- **120 min**: add a 30-min "price this product" exercise — pairs receive a hypothetical agent product spec and must propose pricing + justify it.
- **180 min**: full case study on one real product (Cursor or Agentforce) — read their public pricing pages, reverse-engineer unit economics.

**Numerical anchors**

- Margin trap: at $50/seat + $0.04/task, heavy user (**2000 tasks/mo**) = **−$30 margin**.
- Weighted margin shift: 20%→40% heavy users halves average margin (**+$31 → +$16/user**).
- Reference prices (mid-2026): Cursor **$20/mo**, Devin **$500/mo**, Claude Code **consumption-based**, Agentforce **$2 per conversation**.

---

## Cross-module instructor reminders

- **Every module**: open with one *real-world* incident or product from the last 30 days. Agents move fast; staleness erodes credibility. Subscribe to: Simon Willison's blog, Anthropic's engineering blog, Latent Space podcast, The Information's AI coverage.
- **Every module**: end with a number on the board. Numbers persist; prose doesn't.
- **Every two modules**: revisit the 5-layer diagram. Students forget structure; the recap costs 2 minutes and earns 30.
- **Final session**: end with the *limits* of today's agents, not the promise. Students leaving optimistic-but-naive will be disappointed in the field. Students leaving skeptical-but-curious will be its leaders.

## Pre-session 15-minute checklist

- [ ] Today's numerical anchors written on a sticky note.
- [ ] One news item from the past 7 days ready as a hook.
- [ ] Worksheets printed (or shared doc open).
- [ ] Backup activity ready if discussion stalls (the worksheets' Part C is always a safe fallback).
- [ ] Timer visible (phone or projected) — the 90-min budget only works if you respect it.
- [ ] First question ready for the silent student in the back row.
