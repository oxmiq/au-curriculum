# Week 6 Module 6 — AI Agents · Phase 2 Wrap Assignment (10% Phase-2 Team Assessment)

> **Weight:** 10% of overall grade. **Team project** (groups of 3–4).

## What you submit

A **team presentation + design document** for a complete agent system you've designed (not necessarily fully built) for a real problem. Two pieces:

### Artifact 1 — Design document (3–5 pages)

Required sections:

1. **Problem statement.** What user-facing task does this agent solve? Who's the user?
2. **Why an agent.** Justify vs a single-shot prompt or a deterministic pipeline. Cite the Day 31 "assistant vs agent" rubric.
3. **The 5-layer map** (Problem Set 35.1 rubric):
   - **Foundation layer** — model choice + inference backend (Phase 1 connection). Defend with TTFT/cost/quality numbers.
   - **Reasoning layer** — prompt structure, CoT/few-shot, schema, guardrails (Week 6).
   - **Action layer** — tools (read/write split), schemas, MCP if applicable (Day 32).
   - **Governance layer** — least-privilege, audit, human-in-loop, defenses against EchoLeak-class attacks (Day 33).
   - **Orchestration layer** — single, planner-worker, or supervisor-worker; why (Day 34).
4. **Reliability budget.** Per-step expected reliability, max steps, end-to-end success target. Show the multiplication.
5. **Cost model.** Calls per task × $/call × tasks/month. Justify the spend.
6. **Failure-mode analysis.** Three plausible failure modes, three mitigations. Include at least one *security* failure mode.
7. **What you'd build vs ship.** Honest: would you put this in production today? What's gating?

### Artifact 2 — 15-minute team presentation

Live walkthrough of the design document for the cohort + instructor. Each team member must own and present at least one of the 5 layers.

**Q&A:** 10 minutes from instructor + peers. Expect challenges on cost, security, and "why agent vs prompt" justification.

## Suggested project categories

Pick one, or propose your own:

- **Capsule onboarding helper** — agent that walks a new user through environment selection, model deploy, first benchmark (preps Weeks 8–9).
- **Curriculum study buddy** — agent over the AU-curriculum content that handles quiz remediation, progress tracking, scheduling practice.
- **Incident triage** — agent that ingests an alert, queries logs, classifies, drafts a postmortem.
- **PR reviewer** — agent that reads a PR, runs lint/tests via tools, leaves structured comments.
- **Research summarizer** — agent that scrapes papers, extracts claims, builds a comparison table.

## Grading rubric

| Layer | Pass requires |
|---|---|
| Problem statement clear | A specific user with a real task |
| 5-layer map | All 5 layers present with at least 1 paragraph of reasoning each |
| Phase-1 connection | Foundation layer cites real inference numbers (TTFT / cost / model size) |
| Governance layer | Names at least 1 specific attack (e.g. EchoLeak class) and the defense |
| Orchestration justified | Single vs multi-agent choice defended against the cost-multiplier rule |
| Reliability math | Per-step + end-to-end numbers, max-steps bounded |
| Honesty | "What's gating production deployment" answered truthfully |

**Pass 6/7 layers to pass the assignment.** Team grade applies to all members; instructor reserves right to adjust based on individual presentation contribution.

## Why this assignment exists

This is **the integration test of Phases 1+2**. Phase 1 gave you the foundation, Phase 2 gave you prompts + agents. Designing a real system end-to-end is the only way to know if those parts compose. By Week 8 you'll be standing on Capsule machines — having drawn the architecture for what you'll later actually build.
