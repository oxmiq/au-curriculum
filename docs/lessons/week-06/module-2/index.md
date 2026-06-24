# Day 27 · Agent Fundamentals (The Agent Loop)

> **Concept of the day:** an **agent** is an LLM in a loop that **Perceives → Plans → Acts → Observes → Repeats** until a goal is met. **ReAct** = Reason + Act, the simplest viable pattern. Phase 1's faster decode + Week 6's reliable prompts are *what makes this work at all*.<br>
> **Pre-reading:** AI Agents Student Guide **Module 0 — Why Now?** (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 6 — Prompt Engineering + AI Agents</a>
    <span class="sep">/</span>
    <span>Day 27 · Agent Fundamentals</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-06/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: The Agent Loop | 20 min |
| Part 3 | Deep Dive: ReAct Pattern | 20 min |
| Part 4 | The Phase-1 Connection | 15 min |
| Part 5 | Hands-On: Trace a ReAct Loop | 25 min |
| Part 6 | Hands-On: Chain-Reliability Math | 20 min |
| Part 7 | Wrap-up & Connection | 15 min |

---

## Part 1 — Pre-Reading Review · 15 min
### Before You Start

You should have already read: AI Agents Student Guide **Module 0 — Why Now?** (~20 min).

### Quick Self-Check

Answer these questions from memory:
1. What is an AI agent and how does it differ from a chatbot?
2. What are the four capabilities whose convergence made agents possible?
3. What is the agent loop?

If you couldn't answer all three, review the Student Guide again before proceeding.

---

## Part 2 — Core Concepts: The Agent Loop · 20 min
### Reading — From Calculator to Strategist

Until roughly 2022, working with a language model meant one prompt in, one response out. The interaction was probabilistic, single-shot, and bounded by design: every request started fresh, and the model never acted on anything. Useful, but limited — a kind of fast, articulate calculator.

An AI agent is different in one crucial way: **it runs in a loop.**

### The Five-Step Loop

```
┌────────┐
│ Goal   │  (from user or upstream agent)
└───┬────┘
    ▼
┌────────────────────────────────────┐
│ 1. Perceive   — read inputs + state │
│ 2. Plan       — decide next action  │
│ 3. Act        — call a tool         │
│ 4. Observe    — read the result     │
│ 5. Reflect    — update state, check │
│                if goal achieved     │
└───┬────────────────────────────────┘
    │  loop until done or max steps
    ▼
┌────────┐
│ Result │
└────────┘
```

A bare LLM is **single-shot**: one input → one output. An agent is the loop.

### Assistant vs Agent

| Property | Assistant | Agent |
|----------|-----------|-------|
| Calls per task | 1 | 5–50+ |
| State | Stateless (per turn) | Stateful loop |
| Tool use | Optional / single | Central / multiple |
| Failure mode | One bad answer | Compounding drift, infinite loops |
| Cost model | $ per query | $ per *task* |

---

## Part 3 — Deep Dive: ReAct Pattern · 20 min
### Reading — Reason + Act

The most common agent pattern is **ReAct** (Reason + Act). Each step the agent produces:

```
Thought: (reasoning about what to do next)
Action: tool_name(arguments)
Observation: (result of the tool call, fed back in)
```

This continues until the agent emits `Final Answer:` (or hits a step limit).

### Why ReAct Works

The **explicit reasoning** (`Thought:`) is just Chain-of-Thought (Day 28) applied between actions. The model writes its rationale, which becomes context for the next step.

> **Key insight:** The model doesn't just act — it thinks out loud about what it's going to do, then does it, then observes the result. That observation feeds back into the next round of thinking.

### ReAct Loop Pseudocode

```python
def react_loop(goal, max_steps=10):
    history = [f"Goal: {goal}"]
    for step in range(max_steps):
        out = llm(history + [REACT_TEMPLATE])
        if out.startswith("Final Answer:"):
            return out
        thought, action = parse(out)
        observation = run_tool(action)
        history.append(f"Thought: {thought}\nAction: {action}\nObservation: {observation}")
    return "FAIL: step limit reached"
```

That's it. Everything else in this module is decoration on this skeleton.

---

## Part 4 — The Phase-1 Connection · 15 min
### Reading — Why Agents Work NOW

The Social Capital primer identifies four capabilities that converged to make agents viable:

1. **Foundational models** — GPT-class, Claude, Gemini, open-weight Mixtral, DeepSeek — that can reason about complex problems.
2. **New architectures** — Sparse MoE, Multi-head Latent Attention (MLA) — that make models cheaper and faster.
3. **Reasoning** — Chain-of-thought, inference-time reasoning models — that let models think before answering.
4. **Tool use** — ReAct, MCP, and other protocols — that let models act and observe.

### The Inference Engineering Connection

| Phase 1 Insight | Why it Enables Agents |
|-----------------|----------------------|
| Decode is memory-bound | Per-step latency must be low — drives FP8 + speculative + small models |
| Continuous batching | Multi-step agents = bursty traffic; static batching would queue forever |
| KV-cache prefix sharing | Agent loops repeat 90% of the same system prompt — prefix caching is huge |
| Cost/token | Agents make 10–50 LLM calls per task; cost scales linearly with depth |
| MoE/smaller models | Cheaper per-step cost makes deeper loops affordable |

> *"MoE = cheaper, FlashAttention = faster — that's why agents work now."*

---

## Part 5 — Hands-On: Trace a ReAct Loop · 25 min
### Exercise: Trace a 3-Step ReAct Loop

On paper (or a whiteboard), trace a 3-step ReAct loop for:

> **Task:** "Find the current weather in Hyderabad and convert it to Fahrenheit if it's in Celsius."

For each step, fill in:

| Step | Thought | Action | Observation |
|------|---------|--------|-------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

**What to identify:**
- Which tools would be called?
- What data flows between steps?
- When does the loop terminate?

### Exercise: Identify Real Tasks

List 3 real tasks that **need** an agent (vs. an assistant). For each, sketch the loop:

1. Task: _______________
   - Steps needed: _______________
   - Why agent > assistant: _______________

2. Task: _______________
   - Steps needed: _______________
   - Why agent > assistant: _______________

3. Task: _______________
   - Steps needed: _______________
   - Why agent > assistant: _______________

---

## Part 6 — Hands-On: Chain-Reliability Math · 20 min
### Reading — Long-Horizon Drift

Every prompt in an agent loop must be **≥95% reliable**. At 5 steps × 0.90 = 59% success; at 5 steps × 0.95 = 77%; at 5 steps × 0.99 = 95%.

**Long-horizon drift** is just multiplicative unreliability over time.

### Exercise: Calculate Reliability

**Question 1:** At what per-step reliability does a 20-step loop succeed at least 80%?

```
Reliability needed: 0.80^(1/20) = ?
Answer: ~98.9% per step
```

**Question 2:** At what per-step reliability does a 20-step loop succeed at least 95%?

```
Reliability needed: 0.95^(1/20) = ?
Answer: ~99.7% per step
```

### Exercise: Cost Math

If each LLM call costs $0.005 and a task averages 15 steps:

1. What's the cost per task?
2. At 1000 tasks/day, what's the monthly cost?

---

## Part 7 — Wrap-up & Connection · 15 min
### Self-Check

Can you recite these from memory?
- [ ] The five-step agent loop (Perceive → Plan → Act → Observe → Repeat)
- [ ] ReAct pattern structure (Thought / Action / Observation)
- [ ] The Phase-1 connection (why MoE + FlashAttention = agents work)
- [ ] Chain-reliability math (95% per-step → 77% at 5 steps)

### Connect Forward

Tomorrow: **tools and MCP** — how the `Action:` step actually executes, and the protocol that's standardizing it across the industry.

### Pre-read for tomorrow (Day 28 · Tools & MCP)

- **Resource:** Student Guide **Module 2 — Action Layer** + Anthropic MCP spec overview (~25 min).
- **Reflection questions:**
  1. What problem do **tools** solve that prompts alone can't?
  2. What is **MCP** (Model Context Protocol)? Why does it matter for interoperability?
  3. If you write a tool with side effects (sends an email, writes to a DB), what safety pattern must wrap it?

---

## Stuck?

Ask **oxtutor** to re-explain the agent loop or chain-reliability math, or to generate extra practice questions.