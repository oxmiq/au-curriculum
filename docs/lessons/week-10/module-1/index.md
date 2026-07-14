# Day 46 · Kickoff & Planning

> **Concept of the day:** the capstone starts with a **charter**: a one-page commitment to use case, model, hardware, and eval plan. Today is when vague ideas become concrete decisions. Peer-review keeps everyone honest.<br>
> **Source template:** [Day-46 Charter Template](../../../../planning/source-material/Capstone/Day-46-Charter-Template.md) (source filename is `Day-46-...` from upstream capstone-relative naming; this is program Day 46).<br>
> **Input you walk in with:** your Week 9 Day 44 retrospective, specifically the "capstone seed" section.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 10 - Capstone Project</a>
    <span class="sep">/</span>
    <span>Day 46 · Kickoff & Planning</span>
    {status:week-10/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Time budget for today

| Block | Activity |
|---|---|
| Block 1 | Team formation + use-case brainstorm |
| Block 2 | Model + hardware + eval selection |
| Block 3 | Charter draft |
| Block 4 | Peer review (paired) |
| Block 5 | Revise + submit |

## Why this matters

The single biggest reason capstones fail is **vague scoping**. A 4-day window kills any project that isn't sharp by Monday lunch. The charter is the forcing function.

## Today's milestones

1. **Form teams** (2–3 people, instructor approval).
2. **Choose use case.** One sentence. A specific user with a specific task. *Not* "explore LLMs": "summarize bug reports for the QA team."
3. **Select model + hardware + quantization.** Defend each choice in 1 line using Phase-1 vocabulary.
4. **Design eval plan.** What does success look like? Borrow your 5–10 prompt suite from Week 6/9. Add quality + latency + cost criteria.
5. **Fill the charter template** (link above): every field, no `TBD`.
6. **Peer review**: pair with another team, find one fatal flaw in each other's charters, revise.
7. **Charter submitted to instructor by end of day.**

## The charter - what makes one strong

| Field | Weak | Strong |
|---|---|---|
| Use case | "Try Llama on Capsule" | "Generate weekly QA bug-triage summaries from JIRA tickets for QA lead Anita" |
| Model choice | "Llama because it's popular" | "Llama-3.1-8B-Instruct: small enough for one T4, instruct-tuned for the summarization task" |
| Hardware choice | "Whatever's free" | "Single T4: fits 8B FP16 in 16 GB, target cost $0.50/hour, sufficient for 7 tickets/day" |
| Eval plan | "Check the output" | "10-prompt suite: 5 real triage tickets with ground-truth summaries from Anita, judge by 3 criteria (factuality, brevity, action-orientation)" |
| Success criterion | "It works" | "8/10 prompts pass all 3 criteria; p99 TTFT < 2 s; cost < $0.10/triage" |

## How to use the rest of the week

| Day | What you'll do |
|---|---|
| 47 (Tue) | Execute: deploy on Capsule, run sweeps, run evals |
| 48 (Wed) | Analyze + build presentation |
| 49 (Thu) | Present (15 min + 10 min Q&A): assessed |
| 50 (Fri) | Retrospective + career conversation |

## Detailed time budget

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
| Solo "I'll cover everyone's role" | Teams of 1 burn out by Day 48 |
| Aspirational stack ("let's also try MoE") | One model, one config sweep. Cut everything else. |

## Wrap-up

Every team has a peer-reviewed, instructor-approved charter. Tomorrow you execute.

## Self-check before Day 47

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-10-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 46 · Capstone Kickoff">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What distinguishes a strong capstone use case from a weak one?",
    "options": [
      "Strong use cases test more models; weak ones test only one",
      "Strong: names a specific user (QA team) + specific task (summarize bug reports); weak: generic framing like 'explore LLMs for productivity'",
      "Strong use cases require the most expensive GPU configuration",
      "Strong use cases have longer time horizons: more days to work"
    ],
    "answer": 1,
    "explain": "The lesson's comparison table: 'summarize bug reports for the QA team' is strong (specific user + task, measurable outcome). 'Explore LLMs for the team' is weak; you can't define done, can't write eval prompts, can't fail. Specificity is what makes the eval plan, the success criterion, and the peer review possible."
  },
  {
    "stem": "Why must a success criterion be a number, not a description?",
    "options": [
      "Numbers are easier to put in slides",
      "A number (P95 TTFT < 800 ms, quality pass rate > 8/10) can be objectively evaluated on Day 49; a description like 'fast and accurate' cannot be tested or falsified",
      "Numbers make the charter longer and more impressive",
      "Descriptions are allowed if the team agrees on them informally"
    ],
    "answer": 1,
    "explain": "The lesson states: 'Success criterion must be a number.' If success criterion is '< 800 ms P95 TTFT', you can run the benchmark on Day 48 and know if you passed. If it's 'fast', reasonable people can disagree. The number also forces you to think about what actually matters for the use case."
  },
  {
    "stem": "What is the goal of peer review in the charter process?",
    "options": [
      "To assign grades to each charter",
      "To find one fatal flaw: an assumption, vague field, or missing eval plan that would make the capstone impossible to complete or evaluate by Day 49",
      "To suggest which model is best for the use case",
      "To compare which team has the most ambitious scope"
    ],
    "answer": 1,
    "explain": "Peer review has one job: find the flaw that will kill the capstone before it starts. Common fatal flaws: TBD fields ('model TBD'), unmeasurable success ('users will love it'), eval plan with no ground truth ('we'll know quality when we see it'). One flaw caught Monday saves four days of wasted work."
  },
  {
    "stem": "Why must every charter field be filled with no 'TBD' entries?",
    "options": [
      "It makes the charter look professional",
      "TBD fields are deferred decisions; each one is a future blocker that will stop progress mid-week when there is no time to recover",
      "Instructors won't accept TBD fields per grading rubric",
      "TBD fields break the charter template formatting"
    ],
    "answer": 1,
    "explain": "A TBD model choice means Day 47 starts with a decision that should have been made on Day 46: burning execution time. A TBD eval plan means Day 48 analysis has no quality criteria to apply. The charter is a commitment that removes ambiguity before execution, not a rough draft to refine later."
  },
  {
    "stem": "In a capstone charter, how should the model choice be justified?",
    "options": [
      "Choose the largest model available for the hardware",
      "Choose the most popular model in the benchmark leaderboard",
      "Justify model choice with the use case first: 'Task X requires Y context window and Z quality threshold; model A meets both while fitting in 40 GB HBM at FP8'",
      "The model choice doesn't need justification in the charter"
    ],
    "answer": 2,
    "explain": "The lesson's pattern: derive model from task requirements. Start with what the task needs (context length, quality level, latency target), then identify models that meet those constraints, then select the one that fits the available hardware at the target precision. Choosing the model first and fitting the task to it is backwards."
  },
  {
    "stem": "What is the recommended team size for the capstone project?",
    "options": [
      "1 person only: individual work for portfolio purposes",
      "2-3 people, with instructor approval",
      "4-6 people to distribute the workload across 4 days",
      "Any size: team size is not specified in the charter"
    ],
    "answer": 1,
    "explain": "The lesson specifies 'Form teams (2-3 people, instructor approval).' Small enough that everyone contributes substantively, large enough to parallelize benchmark runs and eval. Instructor approval prevents teams from forming around convenience rather than complementary skills."
  },
  {
    "stem": "What distinguishes an eval plan with ground truth from one without?",
    "options": [
      "Ground truth means using a larger model to evaluate responses",
      "Ground truth means each eval prompt has a pre-defined correct answer or pass criteria established before running: not 'we'll know quality when we see it'",
      "Ground truth means running the eval on the training data",
      "Ground truth is only possible for factual Q&A tasks, not for summarization"
    ],
    "answer": 1,
    "explain": "The lesson's example: '10-prompt suite: 5 real triage tickets with ground-truth summaries from Anita, judge by 3 criteria (factuality, brevity, action-orientation).' Ground truth = criteria defined before you run. 'Check the output' is not an eval plan; you can't tell if config A is better than config B without pre-defined pass criteria."
  },
  {
    "stem": "The charter's failure-mode table warns against an 'aspirational stack' (e.g., 'let's also try an MoE model'). What is the prescribed fix?",
    "options": [
      "Add a second GPU so the extra models fit",
      "Defer the extra models to Day 49 if time allows",
      "One model, one config sweep: cut everything else",
      "Split the team so each person tries a different model"
    ],
    "answer": 2,
    "explain": "The failure-mode table pairs 'Aspirational stack (\"let's also try MoE\")' with the fix 'One model, one config sweep. Cut everything else.' A 4-day window kills any project that isn't sharply scoped. Extra models multiply the benchmark + eval matrix beyond what the week allows, so the charter commits to exactly one model and one sweep."
  },
  {
    "stem": "After the Day 46 charter is approved, what does the rest of Week 10 look like?",
    "options": [
      "Day 47 execute (deploy + sweeps + evals), Day 48 analyze + build presentation, Day 49 present (assessed, 15 min + 10 min Q&A), Day 50 retrospective + career conversation",
      "Day 47 present, Day 48 execute, Day 49 analyze, Day 50 retrospective",
      "Days 47-50 are all execution days with a single presentation at the very end",
      "Day 47 peer review, Day 48 charter revision, Day 49 execute, Day 50 present"
    ],
    "answer": 0,
    "explain": "The 'How to use the rest of the week' table: Day 47 (Tue) execute: deploy on Capsule, run sweeps, run evals; Day 48 (Wed) analyze + build presentation; Day 49 (Thu) present (15 min + 10 min Q&A): assessed; Day 50 (Fri) retrospective + career conversation. The charter on Day 46 is the forcing function that makes the compressed rest of the week possible."
  }
]
</script>
</div>

- [ ] Charter is submitted and peer-reviewed (no TBD fields remaining)
- [ ] You can state the use case in one sentence naming a specific user + specific task
- [ ] Success criterion is a number, not a description ("< 800 ms p95 TTFT", not "fast")

## Stuck?

Ask **oxtutor** to review your charter against the "strong vs weak" comparison table; it can tell you which fields are vague before your peer reviewer does.
