---
title: AI Agents — Pre-Lecture Reading
---

# AI Agents — Pre-Lecture Reading

> **Week 6, Days 27–30.** For each day, this file lists the required pre-reading + three reflection questions to write up the evening before class. Pre-reading is mandatory; reflection answers are checked at the start-of-day readiness check.
>
> **The AI Agents week assumes** you have completed the Inference Engineering phase (Weeks 2–5) and the Prompt Engineering phase (Week 6). If a concept here surprises you, the appendix at the back of the Student Guide cross-references it back to the earlier week where it first appeared.

---

## Day 27 — The Agent Loop

**Pre-reading (≈ 25 min total):**
- *AI Agents — Student Guide*, **Module 0 "Why Now? The Agentic Explosion"** (20 min). Pay special attention to the ReAct loop definition and the "Four Converging Capabilities" list.
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (2022) — read **the abstract + Figure 1 only** (5 min). [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

**Reflection questions (write up the evening before; bring with you):**

1. In your own words, what structural property separates an agent from a chatbot? One sentence. (If your answer uses the word "smart" or "better," try again.)
2. Of the four converging capabilities (foundational models, new architectures, reasoning, ability to act and course-correct), which one do you think was the *last* to mature, and why does its lateness explain why agents only became viable in ~2023?
3. Pick any non-trivial task you did this week (e.g., "debugged a failing benchmark"). Sketch the same task as an agent loop: list 3 *Perceive* signals, 3 *Plan* steps, 3 *Act* tool calls, and 1 *Observe* check.

---

## Day 28 — Tools & MCP

**Pre-reading (≈ 30 min total):**
- *AI Agents — Student Guide*, **Module 2 "The Action Layer"** (25 min). Read in full.
- [Anthropic — Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (5 min, blog post).

**Reflection questions:**

1. Define "tool" in the agent sense in one sentence. Then list 3 concrete tools the Capsule CLI (`capsule list`, `capsule deploy`, `capsule benchmark`) exposes — what does each let an agent *do*?
2. Before MCP, every agent framework re-implemented its own tool-calling format (OpenAI functions, LangChain tools, etc.). Why does a *protocol* (rather than a library) solve the problem better? (Hint: think about who the producers and consumers are.)
3. Draft an MCP-style manifest entry (just the JSON sketch) for one Capsule tool. Required fields: name, description, parameters (with types), and an example invocation.

---

## Day 29 — Governance & Security

**Pre-reading (≈ 35 min total):**
- *AI Agents — Student Guide*, **Module 3 "The Governance Layer"** (25 min). Read in full; the EchoLeak case study is required.
- [MITRE — Brief on CVE-2025-32711 ("EchoLeak")](https://www.cve.org/CVERecord?id=CVE-2025-32711) (5 min — read the description + the impact section).
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — scan the **LLM01 (Prompt Injection)** and **LLM02 (Insecure Output Handling)** sections (5 min).

**Reflection questions:**

1. Distinguish *direct* vs *indirect* prompt injection in one sentence each. Then say which one EchoLeak was, and why that mattered for what the attackers could exfiltrate.
2. "Blast radius" is the central design idea of the Governance Layer. For the deployment agent you sketched on Day 27, what is the worst thing it could do if compromised? What's one design change that would shrink that blast radius by an order of magnitude?
3. Week 6 Day 29 covered hallucination defenses (abstain when uncertain, cite sources). Pick one of those defenses and explain how it *also* serves as a governance control against injected instructions.

---

## Day 30 — Orchestration & Multi-Agent

**Pre-reading (≈ 30 min total):**
- *AI Agents — Student Guide*, **Module 4 "The Orchestration Layer"** (20 min).
- [HuggingFace Agents Course — Unit 2: Frameworks (smolagents intro)](https://huggingface.co/learn/agents-course/unit2/introduction) (10 min, read the intro page only).

**Reflection questions:**

1. State the single strongest argument *against* multi-agent systems. (If you can't, you're not ready to design one.) Then state the single strongest argument *for* one.
2. "Long-horizon drift" — what is it, and why does it make 10-step plans much riskier than 3-step ones? Estimate the success probability of a 10-step plan where each step succeeds 90% of the time. (You did this calculation in Prompt Engineering Day 30 — recall it.)
3. The "value-accrual" question: of the three layers (model / infra / app), which do you currently think captures the most economic value in the agent era, and why? You'll defend this answer in class — be ready to change your mind.

---

## Consolidation & Phase 2 Wrap

**Pre-reading (≈ 20 min total):**
- *AI Agents — Student Guide*, **Module 5 "The Economic Layer (and What Comes Next)"** (15 min). Read for the big picture; we won't quiz the speculative numbers.
- Re-skim **Appendix A (Glossary)** of the Student Guide (5 min) — circle 5 terms you couldn't define cold.

**Reflection questions:**

1. The 5 layers of the stack are: Intelligence / Action / Governance / Orchestration / Economic. In one sentence per layer, say what it contributes that the layer below it cannot provide.
2. Pick the *one* concept from Days 27–30 you'd most want to teach back to a peer. Why that one? (Teaching back is how facilitators identify candidates for ML-eng vs systems tracks.)
3. Looking ahead to the Capsule Power-User weeks (Days 32 onward), what's one connection you already see between agent design and how a user would orchestrate Capsule operations? (You'll revisit this on Day 45.)

---

## Reflection-question grading rubric (so you know what facilitators look for)

| Tier | What facilitators see |
|---|---|
| Excellent | Specific, numerical where possible. References a real product / CVE / paper. Acknowledges uncertainty when warranted. |
| Proficient | Correct, complete, but generic. No real examples. |
| Developing | Partially correct. Confuses two adjacent concepts. |
| Below | Skipped, or answers a different question. |

You can answer at "Proficient" by doing the reading. You reach "Excellent" by connecting the reading to something *you* actually did this internship — your Capsule benchmarks, your prompt evals, your agent sketches. That's the bar.
