# Week 6 · Phase 2 — Prompt Engineering + AI Agents

> **Goal of the week:** in one week, learn how to *talk* to a model effectively (prompt engineering) and how to *build* with one as the orchestrator (agents). This bridges Phase 1's "how inference works" into Phase 3's "drive it from real infrastructure."
> **Note:** This week combines what used to be two separate weeks. Day 26 is a one-day overview of prompt engineering (deep-dive supplementary readings live alongside the lesson); Days 27–30 walk the four agent layers. Day 30 includes consolidation and the Phase 2 assessment.

<!-- AUTO-GEN:CARD-GRID:START -->
<div class="ox-card-grid" markdown="0">
  <a class="ox-card" href="module-1/" style="--i:26">
    {status:week-06/module-1}
    <span class="ox-card__eyebrow">Day 26</span>
    <h3 class="ox-card__title">Prompt Engineering</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-2/" style="--i:27">
    {status:week-06/module-2}
    <span class="ox-card__eyebrow">Day 27</span>
    <h3 class="ox-card__title">Agent Fundamentals</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-3/" style="--i:28">
    {status:week-06/module-3}
    <span class="ox-card__eyebrow">Day 28</span>
    <h3 class="ox-card__title">Tools & Action Layer</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-4/" style="--i:29">
    {status:week-06/module-4}
    <span class="ox-card__eyebrow">Day 29</span>
    <h3 class="ox-card__title">Governance</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
  <a class="ox-card" href="module-5/" style="--i:30">
    {status:week-06/module-5}
    <span class="ox-card__eyebrow">Day 30</span>
    <h3 class="ox-card__title">Orchestration + Consolidation</h3>
    <span class="ox-card__cta">Open lesson →</span>
  </a>
</div>
<!-- AUTO-GEN:CARD-GRID:END -->

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 26 (Mon) | Prompt Engineering (overview + supplementary deep-dives) | Anthropic Prompt Engineering Tutorial Ch1+Ch2 (~20 min) | [module-1/index.md](module-1/index.md) |
| 27 (Tue) | Agent Fundamentals — The Agent Loop (ReAct) | AI Agents Student Guide Module 0 (~20 min) | [module-2/index.md](module-2/index.md) |
| 28 (Wed) | Tools & Action Layer (MCP) | AI Agents Student Guide Module 2 + Anthropic MCP (~25 min) | [module-3/index.md](module-3/index.md) |
| 29 (Thu) | Governance & Security | Student Guide Module 3 Governance + EchoLeak (~25 min) | [module-4/index.md](module-4/index.md) |
| 30 (Fri) | **Orchestration + Consolidation** — Phase 2 assessment (10%) | Student Guide Module 4 Orchestration (~20 min) | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **Phase 2 assessment (10%, team agent design).** Integration exercise — present an agent system: loop + tools + governance + orchestration + inference choice.
- See [module-5](module-5/index.md) for the assessment knowledge check.

## Big-picture connect

"MoE = cheaper, FlashAttention = faster — *that's* why agents work now." This week is where Phase 1's hardware + prompt engineering converge into shippable systems.

## Stuck?

Ask **oxtutor** — the agent loop (Perceive → Plan → Act → Observe → Repeat) is the single mental model that holds the whole week together.