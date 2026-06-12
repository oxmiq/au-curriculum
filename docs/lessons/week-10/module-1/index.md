# Day 47 · Kickoff & Planning

> **Concept of the day:** the capstone starts with a **charter** — a one-page commitment to use case, model, hardware, and eval plan. Today is when vague ideas become concrete decisions. Peer-review keeps everyone honest.
> **Source template:** [Day-46 Charter Template](../../../../planning/source-material/Capstone/Day-46-Charter-Template.md) (source filename is `Day-46-...` from upstream capstone-relative naming; this is program Day 47).
> **Input you walk in with:** your Week 9 Day 45 retrospective, specifically the "capstone seed" section.

---

## Why this matters

The single biggest reason capstones fail is **vague scoping**. A 4-day window kills any project that isn't sharp by Monday lunch. The charter is the forcing function.

## Today's milestones

1. **Form teams** (2–3 people, instructor approval).
2. **Choose use case.** One sentence. A specific user with a specific task. *Not* "explore LLMs" — "summarize bug reports for the QA team."
3. **Select model + hardware + quantization.** Defend each choice in 1 line using Phase-1 vocabulary.
4. **Design eval plan.** What does success look like? Borrow your 5–10 prompt suite from Week 6/9. Add quality + latency + cost criteria.
5. **Fill the charter template** (link above) — every field, no `TBD`.
6. **Peer review** — pair with another team, find one fatal flaw in each other's charters, revise.
7. **Charter submitted to instructor by end of day.**

## The charter — what makes one strong

| Field | Weak | Strong |
|---|---|---|
| Use case | "Try Llama on Capsule" | "Generate weekly QA bug-triage summaries from JIRA tickets for QA lead Anita" |
| Model choice | "Llama because it's popular" | "Llama-3.1-8B-Instruct — small enough for one T4, instruct-tuned for the summarization task" |
| Hardware choice | "Whatever's free" | "Single T4 — fits 8B FP16 in 16 GB, target cost $0.50/hour, sufficient for 7 tickets/day" |
| Eval plan | "Check the output" | "10-prompt suite: 5 real triage tickets with ground-truth summaries from Anita, judge by 3 criteria (factuality, brevity, action-orientation)" |
| Success criterion | "It works" | "8/10 prompts pass all 3 criteria; p99 TTFT < 2 s; cost < $0.10/triage" |

## How to use the rest of the week

| Day | What you'll do |
|---|---|
| 48 (Tue) | Execute — deploy on Capsule, run sweeps, run evals |
| 49 (Wed) | Analyze + build presentation |
| 50 (Thu) | Present (15 min + 10 min Q&A) — assessed |
| 51 (Fri) | Retrospective + career conversation |

## Time budget for today

| Block | Minutes |
|---|---|
| Team formation + use-case brainstorm | 30 |
| Model + hardware + eval selection | 45 |
| Charter draft | 45 |
| Peer review (paired) | 30 |
| Revise + submit | 30 |

If you're past the charter by 4 PM, you're ahead. If you're not, the rest of the week compresses fast.

## Common failure modes (don't)

| Failure | Fix |
|---|---|
| Use case too vague | Force a specific user + specific task |
| Model chosen first, justified later | Pick *because of* the task, not before |
| No eval plan | You can't recommend anything you can't measure |
| Solo "I'll cover everyone's role" | Teams of 1 burn out by Day 49 |
| Aspirational stack ("let's also try MoE") | One model, one config sweep. Cut everything else. |

## Wrap-up

Every team has a peer-reviewed, instructor-approved charter. Tomorrow you execute.
