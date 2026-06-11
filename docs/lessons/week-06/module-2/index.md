# Day 31 · The Agent Loop (ReAct)

> **Concept of the day:** an **agent** is an LLM in a loop that **Perceives → Plans → Acts → Observes → Repeats** until a goal is met. **ReAct** = Reason + Act, the simplest viable pattern. Phase 1's faster decode + Week 6's reliable prompts are *what makes this work at all*.
> **Pre-reading:** AI Agents Student Guide **Module 0 — Why Now?** (~20 min).
> **Source:** [Student Guide Module 0](../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Student%20Guide.md) · [Pre-Lecture Reading](../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Pre-Lecture%20Reading.md).

---

## Why this matters

Every Capsule deployment in Weeks 8–9, every Phase-1 inference optimization, every Week-6 prompt — it all *converges here*. "Why now?" is answered by Phase 1 (cheaper, faster inference) + Phase 2 (reliable prompts). Without both, agents would still be a demo.

## Readiness check

1. State the agent loop in 5 words.
2. What does **ReAct** stand for? Why is it the simplest viable pattern?
3. Connect: which Week 2–4 optimization most enables agentic workloads, and why?
4. **Long-horizon drift** — what is it, and why does it scale with chain length?
5. What's the difference between an **assistant** and an **agent**?

## Core concept

### The five-step loop

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

### ReAct — Reason + Act

The most common pattern. Each step the agent produces:

```
Thought: (reasoning about what to do next)
Action: tool_name(arguments)
Observation: (result of the tool call, fed back in)
```

This continues until the agent emits `Final Answer:` (or hits a step limit).

Why ReAct works: the **explicit reasoning** (`Thought:`) is just CoT (Day 28) applied between actions. The model writes its rationale, which becomes context for the next step.

### The Phase-1 connection

| Phase 1 insight | Why it enables agents |
|---|---|
| Decode is memory-bound | Per-step latency must be low — drives FP8 + speculative + small models |
| Continuous batching | Multi-step agents = bursty traffic; static batching would queue forever |
| KV-cache prefix sharing | Agent loops repeat 90% of the same system prompt — prefix caching is huge |
| Cost / token | Agents make 10–50 LLM calls per task; cost scales linearly with depth |
| MoE / smaller models | Cheaper per-step cost makes deeper loops affordable |

> *"MoE = cheaper, FlashAttention = faster — that's why agents work now."*

### The Phase-2 connection

Every prompt in an agent loop must be **≥95% reliable** (Day 29's chain-reliability math). At 5 steps × 0.9 = 59% success; at 5 steps × 0.95 = 77%; at 5 steps × 0.99 = 95%. **Long-horizon drift** is just multiplicative unreliability over time.

This is why Week 6's eval suites, schemas, and guardrails are non-negotiable in agents.

### Assistant vs Agent

| Property | Assistant | Agent |
|---|---|---|
| Calls per task | 1 | 5–50+ |
| State | Stateless (per turn) | Stateful loop |
| Tool use | Optional / single | Central / multiple |
| Failure mode | One bad answer | Compounding drift, infinite loops |
| Cost model | $ per query | $ per *task* |

### A minimal ReAct loop in pseudocode

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

That's it. Everything else in Week 7 is decoration on this skeleton.

## Practice (90 min)

1. (15 min) Trace a 3-step ReAct loop on a whiteboard for "find the current weather in Hyderabad and convert it to Fahrenheit if it's in Celsius."
2. (25 min) Chain-reliability redux: at what per-step reliability does a 20-step loop succeed at least 80%? At least 95%?
3. (25 min) Pair drill: list 3 real tasks that *need* an agent (vs an assistant). For each, sketch the loop.
4. (15 min) Cost math: if each LLM call is $0.005 and a task averages 15 steps, what's the cost / task? At 1000 tasks/day, monthly?
5. (10 min) Write the rule: *"Use an agent when ___; don't when ___."*

## Wrap-up

Cohort can recite the 5-step loop and ReAct's structure cold.

## Connect forward

Tomorrow: **tools and MCP** — how the `Action:` step actually executes, and the protocol that's standardizing it across the industry.

---

## Pre-read for tomorrow (Day 32 · Tools & MCP)

- **Resource:** Student Guide **Module 2 — Action Layer** + Anthropic MCP spec overview (~25 min).
- **Reflection questions:**
  1. What problem do **tools** solve that prompts alone can't?
  2. What is **MCP** (Model Context Protocol)? Why does it matter for interoperability?
  3. If you write a tool with side effects (sends an email, writes to a DB), what safety pattern must wrap it?
