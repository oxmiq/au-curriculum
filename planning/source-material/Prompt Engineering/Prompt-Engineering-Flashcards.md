# Prompt Engineering — Flashcards

*Spaced-repetition flashcards for Week 6. Format: `Q` on one side, `A` on the other. Use Anki, Mochi, or any SR tool — or just cover the answer column and self-test. ~60 cards organized by day.*

---

## Day 26 — Prompt Structure & Clarity

| # | Q | A |
|---|---|---|
| 1 | What are the two structural slots in a chat-completion API call? | System prompt (instructions for the whole conversation) and user turn(s) (per-turn content). |
| 2 | Why use a system prompt instead of putting everything in the user turn? | (1) Prefix caching saves tokens at scale. (2) Convention discipline: separating rules from data prevents accidentally rewriting rules every turn. |
| 3 | What is the Anthropic tutorial's Chapter 2 motto for prompt clarity? | "Specificity beats vagueness." |
| 4 | Name the three vagueness traps. | Undefined audience, undefined format, undefined success criteria. |
| 5 | A vague prompt produces what kind of output distribution? | A broad one — many different completions are about equally likely. |
| 6 | True or false: model `messages` are completely separate channels; system messages are processed differently from user messages by the model. | False. They're concatenated with role markers. The distinction is conventional and operational (caching, discipline), not architectural. |
| 7 | Why does putting the actual question in the middle of a long prompt hurt? | Models attend to position; instructions in the middle of long contexts are more likely to be missed ("lost in the middle"). |
| 8 | One concrete fix for an "explain X" prompt that gives generic answers? | Specify the audience: who is reading this, what do they already know, what depth do they need. |

---

## Day 27 — Roles, Data Separation & Output Formatting

| # | Q | A |
|---|---|---|
| 9 | What does "role prompting" do, mechanically? | Shifts the output distribution toward the part of the training corpus where that persona writes. |
| 10 | System prompt vs. inline persona — when to use which? | System prompt for personas that should persist across the whole conversation; inline for one-shot persona switches mid-conversation. |
| 11 | What is prompt injection? | An attack where adversary-supplied data contains instructions the model obeys as if they were part of the system prompt. |
| 12 | What's the first-line defense against prompt injection? | Wrap user-supplied data in unambiguous delimiters (typically XML tags like `<input>...</input>`) and instruct the model to treat that content as data, not commands. |
| 13 | Direct vs. indirect prompt injection? | Direct: the user themselves writes the injection. Indirect: the model retrieves attacker-controlled content (web page, document) that contains the injection. |
| 14 | What is "prefill" / "speaking for Claude"? | Supplying an assistant-role message yourself; the model continues from where you stopped. Commits the model to a specific opening. |
| 15 | Most reliable technique for forcing structured (JSON) output? | Prefill with `{` plus an explicit "JSON only, no commentary" instruction. |
| 16 | "Schema by example" — what is it? | Showing the model the exact shape of the desired output (often with placeholder values), instead of describing the schema in prose. |
| 17 | Why does asking for JSON in prose sometimes fail? | The instruction gets buried, the model wraps JSON in markdown fences, or it adds prose around it. Put the format instruction on its own line, last, in code font, and use prefill. |

---

## Day 28 — Chain-of-Thought & Few-Shot

| # | Q | A |
|---|---|---|
| 18 | Why does chain-of-thought (CoT) improve multi-step reasoning? | The model has no separate working memory. Writing out reasoning makes those tokens part of the context the final answer is conditioned on. |
| 19 | What's the Anthropic tutorial's word for chain-of-thought? | "Precognition." |
| 20 | Explicit CoT vs. structured CoT — what's the difference? | Explicit: "think step by step" in prose. Structured: wrap reasoning in `<scratchpad>...</scratchpad>` tags so downstream code can strip it. |
| 21 | When does CoT *hurt* performance? | Simple factual recall, single-token answers, tasks where the model's first instinct is already correct, latency-sensitive contexts. |
| 22 | What is few-shot prompting? | Providing 2–5+ input/output examples in the prompt before the real query, so the model infers the task from examples. |
| 23 | How many examples is "few-shot"? | 2–5 typically; one is "one-shot" (teaches format but not range); large counts (20+) start to look like fine-tuning. |
| 24 | Three rules for choosing few-shot examples? | (1) Cover edge cases you care about. (2) Show the full range of variation. (3) Be consistent in labels, format, and style. |
| 25 | Does example order matter in few-shot prompts? | Slightly — recent examples weigh more. Put your hardest/most-important example last. |
| 26 | Few-shot + CoT — what does it look like? | Each example includes the reasoning steps (not just input → output, but input → reasoning → output). |
| 27 | When is few-shot preferred over CoT? | Tasks that need pattern recognition more than reasoning steps: classification, formatting, style mimicry. |

---

## Day 29 — Hallucinations & Complex Prompts

| # | Q | A |
|---|---|---|
| 28 | True or false: hallucinations are a bug in LLMs. | False. They are the default behavior of a probabilistic model operating on questions it doesn't reliably know how to answer. |
| 29 | Three structural causes of hallucination? | (1) Confabulation — no permission to abstain. (2) False-premise acceptance. (3) Mid-generation drift. |
| 30 | Defense against confabulation? | Explicitly authorize abstention: "If you do not know with high confidence, reply exactly: I don't know. Do not guess." |
| 31 | Defense against false-premise traps? | Frame questions to allow rejection: "Did X do Y? Answer yes or no, then justify." Don't ask "Why did X do Y?" if X did not. |
| 32 | Defense against mid-generation drift in long outputs? | Require citations or quoted evidence for every factual claim — "no claim without a quote." |
| 33 | Strict refusal vs. hedged answer vs. confidence rating — when to use which? | Strict for high-stakes (legal, medical, customer-facing claims). Hedged for brainstorming. Confidence rating for downstream code that can act on it. |
| 34 | Five techniques that should appear in a complex production prompt? | Clarity (specific audience/format), role, data separation (delimiters), output formatting (schema), hallucination guard (permission to abstain). |
| 35 | One thing a "production" prompt typically has that a "playground" prompt doesn't? | A defined hallucination guard, a strict output schema, and accompanying evals. |

---

## Day 30 — Chaining, Tools, Search, Evals

| # | Q | A |
|---|---|---|
| 36 | What problem does prompt chaining solve? | A single prompt trying to do multiple distinct phases (parse → reason → format) fails opaquely; chaining isolates phases so failures localize and each phase can be tested independently. |
| 37 | What is the "handoff format" in a prompt chain? | The structured data format (usually JSON) that one prompt emits and the next consumes — the contract between chain steps. |
| 38 | When *not* to chain? | When the task is simple enough for one prompt; when phases are tightly coupled and information leaks; when added latency/cost outweighs the benefit. |
| 39 | What is tool use, structurally? | Structured output (the model emits a function-call description) plus a driver loop in your code (execute the function, send result back as a new message). |
| 40 | Why does tool use work using only prompting techniques you already know? | Because it's just structured output (Day 27) — the model emits JSON describing a call; your code does the rest. The agent is the loop, not the model. |
| 41 | What does RAG stand for, and what does it do? | Retrieval-Augmented Generation. Retrieves relevant passages from a corpus before sending the prompt, so the model answers from those passages instead of from its parametric memory. |
| 42 | Why does RAG reduce hallucination? | The source of truth is in the prompt, not in the model's weights. The model can quote and cite. |
| 43 | What is a prompt eval? | An automated test suite for a prompt: (input, expected, pass-criterion) tuples run against the prompt, with a tracked pass rate. |
| 44 | Why are prompt evals important? | Without them, prompt engineering is vibes-driven. With them, you have regression protection, cross-model comparison, and confidence to ship. |
| 45 | Common pass-criterion types in prompt evals? | Exact match, regex match, JSON schema validity, semantic equivalence (LLM-as-judge), human grading. |
| 46 | Why is `temperature=0` recommended when running evals? | Removes sampling noise so changes in pass rate reflect prompt changes, not random variation. |
| 47 | Name one open-source prompt eval tool. | promptfoo (others: OpenAI Evals, Anthropic eval framework, LangSmith). |
| 48 | One-sentence summary of why Week 6 is the bridge to Week 7 (Agents)? | Every agent is a chain of prompts with tool calls and an eval suite — exactly the things you learned on Day 30. |

---

## Cross-week / synthesis cards

| # | Q | A |
|---|---|---|
| 49 | If a prompt is "not working," what are the five diagnostic questions to ask? | (1) Is it vague? (2) Are instructions and data tangled? Is there a role? (3) Does it need scratchpad reasoning or examples? (4) Did I give permission to abstain? (5) Is one prompt trying to do three things? |
| 50 | Why does specifying audience usually help more than specifying format? | Audience implies all the other choices — register, depth, vocabulary, examples to use — which the model would otherwise pick from priors. |
| 51 | What's wrong with "Be concise but exhaustive"? | Conflicting instructions. Pick one. The model will pick one for you and you won't know which. |
| 52 | The difference between an instruction-tuned model and a base model? | Instruction-tuned models are trained to follow instructions; base models autocomplete your "instruction" as if it were the start of a document. All API models you use are instruction-tuned. |
| 53 | Why might `temperature=0.7` give better-feeling outputs than `temperature=0`? | At low temperature, the model picks the single most likely next token, which can be repetitive or overly cautious. Slight randomness produces more natural prose and avoids predictable phrasings. |
| 54 | If your prompt works on Claude but not on a smaller open model, what should you try first? | Add few-shot examples. Smaller models follow instructions less reliably; examples lower the difficulty. |
| 55 | What's the single most reliable structured-output technique across models? | Prefill (where supported) + schema-by-example + explicit "no commentary" instruction. |
| 56 | A prompt has a clear `<scratchpad>` section and a clear `<answer>` section. What does production code do with the scratchpad? | Strips it before showing the answer to the user. The reasoning costs tokens but isn't seen. |
| 57 | True or false: longer system prompts always hurt latency. | False. Cached system prompts (Anthropic prompt caching, OpenAI cached input) charge a fraction of the per-token rate after the first request and are very fast. Caching changes the math. |
| 58 | Roughly how many test cases is a "minimal serious" prompt eval? | 5–10 to start, 20–50 once the prompt stabilizes. Below 5 is vibes; above 100 is the next level of engineering investment. |
| 59 | If a prompt passes 80% of an eval and the threshold is 95%, what should you do? | Examine the failing cases for patterns. Often a single prompt change (an added example, a clarified instruction) fixes a cluster of failures. Iterate, re-run, repeat. |
| 60 | One thing that transfers from prompt engineering to *any* communication with a junior collaborator? | Specificity, role-setting, structured deliverables, and explicit permission to ask "I don't know." All four work on humans too. |

---

# Appendix A — Numerical anchors (25 cards)

*Memorize the numbers. In production conversations these are the load-bearing facts; the techniques are the explanation.*

| # | Q | A |
|---|---|---|
| N1 | At 10M requests/month with a 2K-token system prompt, what's the savings from Anthropic prompt caching vs. uncached? | ~$54K/month (cached prefix priced at ~10% of normal input). |
| N2 | What discount does Anthropic prompt caching apply to cached prefix tokens? | ~90% off normal input price (cached at ~10% of normal rate). |
| N3 | Same instruction placed mid-prompt vs. top-or-bottom of a 4K+ token prompt — what's the follow-rate gap? | 15–25 percentage points worse in the middle ("lost in the middle"). |
| N4 | Prompt-injection success rate: undefended prompt vs. delimiter + role + abstention defense? | ~38% → <5%. |
| N5 | Role prompting on domain tasks — typical lift on a 100-point rubric? | ~+42 points vs. no role. |
| N6 | Cost multiplier of chain-of-thought vs. direct answer (per call)? | ~4.4× output tokens. |
| N7 | Few-shot accuracy curve: 0-shot / 1-shot / 3-shot / 5-shot / 10-shot? | 62 / 73 / 84 / 87 / 88%. |
| N8 | At what example count does few-shot start hitting diminishing returns? | ~5 examples (5 → 10 only buys ~1 point). |
| N9 | Self-consistency: typical accuracy lift over single CoT, and at what compute cost? | ~+11 points at ~5× compute. |
| N10 | Abstention permission: hallucination rate on unanswerable questions, before vs. after? | ~46% → <5%. |
| N11 | Citation discipline: fabrication rate before vs. after, and the output-token overhead? | ~12% → <1%, at ~30% more output tokens. |
| N12 | Three-step prompt chain where each step is 90% reliable — end-to-end reliability? | 0.9³ ≈ 73%. |
| N13 | Same chain at 95% per step? | 0.95³ ≈ 86%. |
| N14 | Same chain at 99% per step? | 0.99³ ≈ 97%. |
| N15 | What's the typical break-even point on an eval suite (hours to write vs. first regression caught)? | ~4 engineer-hours to write; pays for itself the first regression caught (usually within a month). |
| N16 | Healthy eval-suite mix of positive vs. negative cases? | ~70% positive / ~30% negative (cases where the correct output is "I don't know" or a refusal). |
| N17 | Real-world indirect-injection CVE you should be able to name? | EchoLeak — CVE-2025-32711, Microsoft 365 Copilot, mid-2025. |
| N18 | Constrained-decoding latency overhead? | ~10–20% vs. unconstrained sampling. |
| N19 | Anthropic input price (Sonnet-tier) you can quote as a benchmark? | ~$3 per million input tokens. |
| N20 | Batched/cheap-tier output price you can quote? | ~$0.05 per million tokens (batched inference). |
| N21 | When does `temperature=0.7` beat `temperature=0` on subjective quality? | When users perceive repetitiveness or canned phrasing at T=0 (most prose-generation tasks). |
| N22 | Output-token premium of reasoning models (o1/o3/Sonnet-thinking) vs. non-reasoning peers? | Roughly 3–10× per call depending on problem; reasoning tokens billed. |
| N23 | Minimum eval-suite size to stop being vibes? | ≥5 cases (10–20 is the "serious" floor; 50+ is engineering investment). |
| N24 | LLM-as-judge known biases (name three)? | Position bias (prefers first), self-bias (prefers same-model output), verbosity bias (prefers longer). |
| N25 | Three-defense stack against prompt injection (in order)? | (1) Delimiters wrapping untrusted input, (2) explicit role for the model ("you are X and only do X"), (3) explicit abstention permission with refusal phrasing. |

---

# Appendix B — Recommended self-test order

You have 60 main cards + 25 numerical anchors = 85 total. Don't review them in order — review by **difficulty tier** and **purpose**, then mix.

### Tier 1 — Vocabulary (cards 1–17, 22–27, 36–47)
Fact recall. Get to 100% in one or two passes; these unlock everything else.

### Tier 2 — Defenses & guards (cards 11–13, 28–35, N4, N10, N11, N17, N25)
The mistakes that get you fired or breached. Drill until reflexive. If you can't list the three-defense stack against injection (N25) and name EchoLeak (N17) cold, keep drilling.

### Tier 3 — Numerical anchors (N1–N24)
Numbers are how senior engineers talk about prompts. "It hallucinated" loses an argument; "abstention drops the rate from 46% to under 5% at zero extra cost" wins it. Memorize the dozen most useful: N1, N3, N4, N6, N7, N9, N10, N11, N12, N15, N17, N19.

### Tier 4 — Synthesis (cards 48–60)
Apply across days. If you can't answer card 49 (the five diagnostic questions) in 30 seconds, you're not yet ready to ship prompts solo.

### Mixed review (after first pass)
Anki/Mochi will shuffle automatically. If self-testing on paper: cover the answer column, then shuffle the card numbers. Spend more time on cards you got wrong yesterday than on cards you got right last week.

### Calibration check
At the end of the week, you should be able to:
- Define every term in the **Glossary** without looking.
- Recite the dozen numerical anchors above without looking.
- Diagnose a failing prompt using card 49 in under one minute.
- Name three real provider features (prefix caching, structured outputs, prompt caching pricing) and at least one real CVE.

If yes: you've earned the depth bar this curriculum aims for. If no: another pass through Tiers 2 and 3 is the highest-leverage thing you can do.
