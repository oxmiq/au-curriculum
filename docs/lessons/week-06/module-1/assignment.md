# Week 6 — Prompt Engineering · Module Assignment (5% PE Assessment)

> **Source:** Mindmap Week 6 Day 30 + Prompt Engineering Problem Sets §Set 30 (chaining drill) + Worksheets.
> **Weight:** 5% of overall grade.

## What you submit

**Two artifacts**, both in a single ZIP or PR:

### Artifact 1 — A 2-step chained prompt

A small task that requires two LLM calls in sequence. Examples:

- **Extract → classify:** extract structured fields from a support ticket; then classify priority based on those fields.
- **Plan → execute:** generate a step-plan to solve a problem; then produce the final answer following the plan.
- **Draft → review:** write a first draft; then self-critique against a rubric and produce a revised draft.

**Required:**

1. Both prompts in version-controlled files (markdown or plain text), with explicit role + context + delimiters + schema + guardrails.
2. The "glue" — a 30-line script (Python, Node, or even a shell + curl) that runs prompt 1, parses, feeds into prompt 2, and prints the final result.
3. A **README** explaining the chain's purpose and what each step contributes.
4. A reliability note: each prompt's expected per-step reliability (your honest estimate) and the resulting end-to-end success rate (multiplicative).

### Artifact 2 — A 5-prompt eval suite

For **prompt 2** of your chain (the one whose output is user-visible), build a small eval suite:

| Field | Notes |
|---|---|
| 5 input cases | Mix of 3 easy + 1 hard + 1 edge case (empty, malformed, off-topic, or adversarial) |
| Expected output / rubric | Reference answer OR a list of "must contain X" / "must not contain Y" rules per input |
| Eval runner | A script that runs the prompt on each input and reports pass / fail with a one-line reason |
| Pass criterion | At least **4 / 5** must pass |

## What "good" looks like

- Each prompt has all the Day 26–27 components.
- Output of prompt 1 is **structured** (JSON or XML-tagged) so prompt 2 can consume it deterministically.
- At least one **guardrail** present: "I don't know" clause OR self-check pass OR schema validation OR citation requirement.
- Your eval suite **catches** something — at least one of the 5 inputs initially fails, and you iterate to fix.
- Reliability math is honest (no claiming 99% without measurement).

## Grading rubric

| Criterion | Pass requires |
|---|---|
| Prompts well-formed | All 6 components present in both prompts |
| Chain works end-to-end | Demonstrably runs on at least 3 real inputs |
| Guardrail present | At least one explicit guardrail named & implemented |
| Eval suite | 5 inputs, all run, 4+ pass on the final version |
| Reliability note | Per-step + end-to-end numbers reported with honest reasoning |

Pass 4/5 criteria to pass the assignment. **Pass the assignment to earn the 5% weight.**

## Why this assignment exists

This is the **smallest possible production prompt system** — chain + eval. Every agent in Week 7 is structurally this same thing with tools added. If you can't do this cleanly here, the agent assignment in Week 7 will collapse.
