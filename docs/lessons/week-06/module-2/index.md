# Day 27 · Agent Fundamentals (The Agent Loop)

> **Concept of the day:** an **agent** is an LLM in a loop that **Perceives → Plans → Acts → Observes → Repeats** until a goal is met. **ReAct** = Reason + Act, the simplest viable pattern. Phase 1's faster decode + Week 6's reliable prompts are *what makes this work at all*.<br>
> **Pre-reading:** <a href="../../../readings/prompt-engineering/#day-27-primer-roles-walls-and-shapes">Prompt Engineering Pre-Lecture Reading - Day 27 primer (Roles, walls, and shapes)</a>. Supplement: <a href="https://github.com/anthropics/prompt-eng-interactive-tutorial" target="_blank" rel="noopener">Anthropic tutorial</a> Ch 3–5.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 6 - Prompt Engineering + AI Agents</a>
    <span class="sep">/</span>
    <span>Day 27 · Agent Fundamentals</span>
    {status:week-06/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours are organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: The Agent Loop |
| Part 3 | Deep Dive: ReAct Pattern |
| Part 4 | The Phase-1 Connection |
| Part 5 | Hands-On: Trace a ReAct Loop |
| Part 6 | Hands-On: Chain-Reliability Math |
| Part 7 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: AI Agents Student Guide **Module 0 - Why Now?**.

### Quick Self-Check

Answer these questions from memory:

1. What is an AI agent and how does it differ from a chatbot?
2. What are the four capabilities whose convergence made agents possible?
3. What is the agent loop?

If you couldn't answer all three, review the Student Guide again before proceeding.

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m2-readiness" data-kind="readiness" data-draw="5" data-source="Anthropic Prompt Engineering Interactive Tutorial Ch 3-5">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the ReAct pattern in AI agents?",
    "options": [
      "A way to react to user inputs faster",
      "Reason + Act: the agent reasons about the situation and then takes action",
      "A method for reducing response latency",
      "A technique for training models"
    ],
    "answer": 1,
    "explain": "ReAct (Reason + Act) is the simplest viable agent pattern. The agent: (1) reasons about the current state, (2) decides on an action, (3) acts, (4) observes the result, and (5) repeats until the goal is met. It's the core pattern behind most agent implementations."
  },
  {
    "stem": "What are the steps in the agent loop?",
    "options": [
      "Input, Processing, Output, Storage",
      "Perceive → Plan → Act → Observe → Repeat",
      "Start, Continue, Stop, Error",
      "Initialize, Execute, Validate, Return"
    ],
    "answer": 1,
    "explain": "The agent loop is: Perceive (get input/observation) → Plan (decide what to do) → Act (take action) → Observe (see result) → Repeat (continue until goal is met). This is the fundamental cycle that makes agents different from stateless chatbots."
  },
  {
    "stem": "What is the key difference between a chatbot and an AI agent?",
    "options": [
      "Chatbots are faster",
      "Agents can take actions and iterate; chatbots are single-shot",
      "Chatbots are more intelligent",
      "There is no difference"
    ],
    "answer": 1,
    "explain": "A chatbot is single-shot: one prompt in, one response out. An agent is in a loop; it can take multiple actions, observe results, and iterate until a goal is met. Agents have 'agency'; they can act on the world, not just respond."
  },
  {
    "stem": "What does 'giving an agent a role' mean in prompting?",
    "options": [
      "Assigning the agent to a specific team",
      "Using the system prompt to define who the agent is (e.g., 'You are a Python expert')",
      "Making the agent follow human instructions",
      "Preventing the agent from making decisions"
    ],
    "answer": 1,
    "explain": "Giving an agent a role means using the system prompt to define who the agent is and how it should behave. For example, 'You are a Python expert specializing in performance optimization' gives the agent context about its capabilities and focus area."
  },
  {
    "stem": "What is 'chain reliability' in the context of agent systems?",
    "options": [
      "The reliability of the model itself",
      "The probability that a multi-step agent task succeeds: drops exponentially with each step",
      "How fast the agent can process requests",
      "The number of agents working together"
    ],
    "answer": 1,
    "explain": "Chain reliability is the probability that a multi-step agent task succeeds. If each step has 90% reliability, a 5-step chain has only 0.9^5 = 59% reliability. This is a fundamental challenge in agent systems; adding more steps makes failures more likely."
  },
  {
    "stem": "What does 'shaping' mean in prompt engineering for agents?",
    "options": [
      "Making the output shorter",
      "Structuring prompts to guide the agent toward desired behaviors without overly restrictive rules",
      "Removing unnecessary words from prompts",
      "Formatting the response as JSON"
    ],
    "answer": 1,
    "explain": "'Shaping' is structuring prompts to guide the agent toward desired behaviors. It's like 'herding'; you set up the right context, role, and examples so the agent naturally goes in the right direction, rather than using overly restrictive rules that might backfire."
  },
  {
    "stem": "What is a 'wall' in the context of agent prompting?",
    "options": [
      "A type of agent architecture",
      "A hard constraint that the agent must not violate (e.g., 'never reveal API keys')",
      "The maximum number of tokens in a response",
      "A connection between two agents"
    ],
    "answer": 1,
    "explain": "A 'wall' is a hard constraint that the agent must not violate: like 'never reveal API keys' or 'never provide medical advice'. These are placed in the system prompt to ensure the agent has clear boundaries on what it can and cannot do."
  },
  {
    "stem": "Why does Phase 1's faster decode matter for agents?",
    "options": [
      "It doesn't matter",
      "Faster decode means the agent loop can run more times per second, completing tasks faster",
      "It reduces the cost of API calls",
      "It makes the model more accurate"
    ],
    "answer": 1,
    "explain": "Faster decode (from Phase 1 optimizations like Tensor Parallelism, quantization, better engines) means the agent loop can run more iterations per second. Since agents make many sequential LLM calls, faster decode directly translates to faster agent task completion."
  }
]
</script>
</div>

---

## Part 2 - Core Concepts: The Agent Loop
### Reading - From Calculator to Strategist

Until roughly 2022, working with a language model meant one prompt in, one response out. The interaction was probabilistic, single-shot, and bounded by design: every request started fresh, and the model never acted on anything. Useful, but limited: a kind of fast, articulate calculator.

An AI agent is different in one crucial way: **it runs in a loop.**

### The Five-Step Loop

```
┌────────┐
│ Goal   │  (from user or upstream agent)
└───┬────┘
    ▼
┌────────────────────────────────────┐
│ 1. Perceive   - read inputs + state │
│ 2. Plan       - decide next action  │
│ 3. Act        - call a tool         │
│ 4. Observe    - read the result     │
│ 5. Reflect    - update state, check │
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

## Part 3 - Deep Dive: ReAct Pattern
### Reading - Reason + Act

The most common agent pattern is **ReAct** (Reason + Act). Each step the agent produces:

```
Thought: (reasoning about what to do next)
Action: tool_name(arguments)
Observation: (result of the tool call, fed back in)
```

This continues until the agent emits `Final Answer:` (or hits a step limit).

### Why ReAct Works

The **explicit reasoning** (`Thought:`) is just Chain-of-Thought (Day 28) applied between actions. The model writes its rationale, which becomes context for the next step.

> **Key insight:** The model doesn't just act; it thinks out loud about what it's going to do, then does it, then observes the result. That observation feeds back into the next round of thinking.

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

## Part 4 - The Phase-1 Connection
### Reading - Why Agents Work NOW

The Social Capital primer identifies four capabilities that converged to make agents viable:

1. **Foundational models**, GPT-class, Claude, Gemini, open-weight Mixtral, DeepSeek, that can reason about complex problems.
2. **New architectures**, Sparse MoE, Multi-head Latent Attention (MLA), that make models cheaper and faster.
3. **Reasoning**, Chain-of-thought, inference-time reasoning models, that let models think before answering.
4. **Tool use**, ReAct, MCP, and other protocols, that let models act and observe.

### The Inference Engineering Connection

| Phase 1 Insight | Why it Enables Agents |
|-----------------|----------------------|
| Decode is memory-bound | Per-step latency must be low: drives FP8 + speculative + small models |
| Continuous batching | Multi-step agents = bursty traffic; static batching would queue forever |
| KV-cache prefix sharing | Agent loops repeat 90% of the same system prompt; prefix caching is huge |
| Cost/token | Agents make 10–50 LLM calls per task; cost scales linearly with depth |
| MoE/smaller models | Cheaper per-step cost makes deeper loops affordable |

> *"MoE = cheaper, FlashAttention = faster; that's why agents work now."*

---

## Part 5 - Hands-On: Trace a ReAct Loop
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

## Part 6 - Hands-On: Chain-Reliability Math
### Reading - Long-Horizon Drift

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

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-06-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 27 · Agent Fundamentals">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the five steps of the agent loop in order?",
    "options": [
      "Plan → Perceive → Act → Repeat → Observe",
      "Perceive → Plan → Act → Observe → Repeat",
      "Act → Observe → Plan → Perceive → Repeat",
      "Observe → Perceive → Plan → Act → Repeat"
    ],
    "answer": 1,
    "explain": "The five-step agent loop: Perceive (gather inputs from environment/tools), Plan (decide what action to take), Act (execute the chosen action), Observe (read the result of the action), Repeat (loop until task complete or goal achieved). This is the fundamental ReAct-style agent architecture."
  },
  {
    "stem": "In a ReAct loop, what are the three alternating elements?",
    "options": [
      "Input, Output, Feedback",
      "Thought, Action, Observation",
      "Question, Reasoning, Answer",
      "Perceive, Execute, Learn"
    ],
    "answer": 1,
    "explain": "ReAct (Reasoning + Acting) loops interleave: Thought (the model's internal reasoning about what to do), Action (the tool call or response to execute), and Observation (the result returned by the tool or environment). This pattern makes agent reasoning transparent and debuggable."
  },
  {
    "stem": "If each step in a 5-step agent chain has 95% reliability, what is the end-to-end reliability?",
    "options": [
      "95%",
      "90%",
      "77%",
      "50%"
    ],
    "answer": 2,
    "explain": "Chain reliability = 0.95^5 ≈ 0.774 = ~77%. Each step's failure probability compounds: if step 1 fails 5% of the time AND step 2 fails 5% of the time, the chance both succeed is 0.95 × 0.95 = 0.90. Five steps: 0.95^5 ≈ 0.77. This is why reliability engineering matters for agents."
  },
  {
    "stem": "Why does MoE + FlashAttention enable economically viable agents?",
    "options": [
      "MoE reduces model size; FlashAttention reduces GPU count",
      "MoE lowers cost per token (sparse activation = less compute per call); FlashAttention enables long-context processing (agents need large context for tool history); together they make multi-step agent loops affordable",
      "MoE allows agents to run without GPUs; FlashAttention eliminates KV cache overhead",
      "MoE handles multiple agent instances in parallel; FlashAttention handles single-agent tasks"
    ],
    "answer": 1,
    "explain": "Agent chains make many LLM calls (sometimes dozens per user request). MoE reduces cost per call (Phase 1 Week 4). FlashAttention handles the long contexts agents need (tool outputs + conversation history). Without both, the economics of multi-step agents at scale wouldn't work."
  },
  {
    "stem": "What is the difference between the Plan step and the Act step in the agent loop?",
    "options": [
      "Plan creates the agent's memory; Act reads from it",
      "Plan uses a different model than Act",
      "Plan decides what to do (internal reasoning, choosing which tool to call); Act executes the decision (actually calls the tool or produces output)",
      "Plan is done by the user; Act is done by the model"
    ],
    "answer": 2,
    "explain": "Plan = the model reasons about the current state and decides the next action (which tool, which arguments). Act = the model actually emits the action (a function call, a JSON tool invocation, or a final response). The ReAct loop makes this split explicit as Thought (Plan) and Action (Act)."
  },
  {
    "stem": "For a 10-step agent chain with 95% reliability per step, approximately what end-to-end reliability should you expect?",
    "options": [
      "~95%",
      "~85%",
      "~60%",
      "~40%"
    ],
    "answer": 2,
    "explain": "0.95^10 ≈ 0.60. A 10-step chain that's 95% reliable per step has only ~60% end-to-end reliability. This is why production agents must have retry logic, error handling, and fallback paths; and why keeping chains short where possible matters."
  },
  {
    "stem": "According to the Assistant vs Agent table, how many LLM calls does a typical agent make per task versus an assistant?",
    "options": [
      "Both make exactly 1 call per task",
      "Assistant: 1 call; Agent: 5–50+ calls",
      "Assistant: 5–50+ calls; Agent: 1 call",
      "Both make 5–50+ calls per task"
    ],
    "answer": 1,
    "explain": "The lesson's Assistant vs Agent table lists 1 call per task for an assistant (single-shot, stateless) versus 5–50+ calls for an agent (a stateful loop). This is why the cost model shifts from '$ per query' for assistants to '$ per task' for agents."
  },
  {
    "stem": "Roughly what per-step reliability is needed for a 20-step loop to succeed at least 80% of the time?",
    "options": [
      "~90%",
      "~95%",
      "~98.9%",
      "~99.9%"
    ],
    "answer": 2,
    "explain": "0.80^(1/20) ≈ 0.989, so about 98.9% per step. Because reliability compounds multiplicatively (r^N), long chains demand very high per-step reliability: the lesson's core 'long-horizon drift' point."
  }
]
</script>
</div>

### Connect Forward

Tomorrow: **tools and MCP**: how the `Action:` step actually executes, and the protocol that's standardizing it across the industry.

### Pre-read for tomorrow (Day 28 · Tools & MCP)

- **Resource:** <a href="../../../readings/ai-agents/#day-28-tools-mcp">AI Agents Pre-Lecture Reading - Tools & MCP section</a>. Supplement: <a href="https://www.anthropic.com/news/model-context-protocol" target="_blank" rel="noopener">Anthropic - Introducing the Model Context Protocol</a>.
- **Reflection questions:**
  1. What problem do **tools** solve that prompts alone can't?
  2. What is **MCP** (Model Context Protocol)? Why does it matter for interoperability?
  3. If you write a tool with side effects (sends an email, writes to a DB), what safety pattern must wrap it?

---

## Stuck?

Ask **oxtutor** to re-explain the agent loop or chain-reliability math, or to generate extra practice questions.