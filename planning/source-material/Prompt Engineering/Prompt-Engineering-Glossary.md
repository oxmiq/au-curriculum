# Prompt Engineering — Glossary

*Vocabulary reference for Week 6. Each term has a one-line "field definition," a paragraph of explanation, and a cross-reference to where it's introduced. Use this to look things up during reading or while doing the exercises.*

---

### Assistant turn
**Field:** A message in the `messages` array with `role: "assistant"`, representing something the model produced (or that you're putting in its mouth via prefill).

In a multi-turn conversation, assistant turns are interleaved with user turns. In a fresh request, you can also supply an assistant turn as a **prefill** to commit the model to a specific opening (see *Prefill*). *Introduced: Day 26.*

### Chain-of-thought (CoT)
**Field:** A prompting technique that asks the model to produce intermediate reasoning steps before its final answer.

Because the model has no separate working memory, its previously generated tokens are the only "scratchpad" it has. Forcing it to write out reasoning means the final answer is conditioned on that reasoning. Improves multi-step reasoning quality dramatically; adds latency and token cost. Variants: explicit ("think step by step"), structured (`<scratchpad>...</scratchpad>` tags), and few-shot CoT (examples that include reasoning). *Introduced: Day 28.*

### Chaining (prompt chaining)
**Field:** Decomposing a complex task into a sequence of 2–N simpler prompts with explicit handoff format between them.

Each prompt in the chain has one job, can be tested in isolation, and can fail in localized ways. Handoff format is usually JSON. Different prompts in the chain can use different models. The agent loop in Week 7 is a generalization of chaining. *Introduced: Day 30.*

### Completion
**Field:** The text the model produces in response to a prompt. Same as "response" or "output."

Older API terminology (pre-chat models) called the whole API call a "completion endpoint." The modern terminology is "chat completion" or just "response." *Introduced: Day 26.*

### Confabulation
**Field:** A subtype of hallucination where the model produces a plausible-sounding but unsupported answer because it has no permission to say "I don't know."

Distinct from hallucination caused by false-premise traps or mid-generation drift. The defense is to explicitly authorize abstention in the prompt. *Introduced: Day 29.*

### Context window
**Field:** The maximum number of tokens (input + output) a model can process in a single request.

Modern frontier models have 200K–1M token windows. Prompt-engineering implications: very long contexts are expensive, suffer from "lost in the middle" attention degradation, and may push you toward chaining or RAG instead of stuffing everything in one prompt. *Cross-reference: Week 2 (Inference Engineering).* *Used: Day 30.*

### Delimiter
**Field:** A marker (typically XML tags like `<input>...</input>`, but also triple backticks, `---`, or any unambiguous string) used to mark the boundary between instructions and data inside a prompt.

The primary purpose is **data separation** (see entry) — telling the model "everything between these markers is content to operate on, not commands to obey." XML-style tags are preferred because models are trained on substantial amounts of XML and respect the structure. *Introduced: Day 27.*

### Eval (prompt evaluation)
**Field:** An automated test suite for a prompt, consisting of (input, expected-output, pass-criterion) tuples that can be run against any version of the prompt.

The same discipline as unit testing, applied to prompts. Pass criteria range from exact match to regex to JSON-schema validation to LLM-as-judge to human grading. Tools: promptfoo, OpenAI Evals, Anthropic eval framework, homegrown YAML+driver scripts. Eval-driven prompt development is the difference between vibes-driven and engineering. *Introduced: Day 30.*

### Few-shot prompting
**Field:** Providing 2–5+ input/output examples in the prompt before the real query, so the model infers the task from the examples rather than from prose description.

Effective for classification, formatting, style mimicry, edge-case handling. Composes well with CoT (examples include reasoning). Choosing examples is itself a skill: cover edge cases, show variation, be label-consistent, place hardest example last. *Introduced: Day 28.*

### Hallucination
**Field:** Model output that is factually wrong, fabricated, or unsupported by source material, presented as if it were correct.

Hallucinations are the *default* behavior of a language model operating on a question whose answer it doesn't reliably know. Three structural causes: confabulation (no permission to abstain), false-premise acceptance, and mid-generation drift. Defenses: authorize abstention, avoid leading questions, require citations or quoted evidence. None are bulletproof; combine them. *Introduced: Day 29.*

### Handoff format
**Field:** The structured data format (typically JSON) that one prompt in a chain emits and that the next prompt in the chain consumes.

A sharply defined handoff is the contract between chain steps. Without it, errors propagate invisibly. With it, you can validate at each boundary and localize failures. *Introduced: Day 30.*

### Instruction following
**Field:** The quality of a model in obeying explicit prompt instructions (vs. defaulting to its prior).

Instruction-tuned models (e.g. Claude, GPT-4-Instruct, Llama-Instruct, Nemotron) are explicitly trained to follow instructions. Base models (raw next-token predictors) are not — they will autocomplete your "instruction" as if it were the start of a document. All modern API models you'll use are instruction-tuned. *Used: Day 26.*

### JSON mode
**Field:** A model-provider feature that constrains the model's output to syntactically valid JSON.

OpenAI calls it `response_format: {"type": "json_object"}`. Anthropic doesn't have a dedicated mode but achieves the same via prefill (`{`) + clear instruction. Different from "guaranteed JSON against a schema" — JSON mode ensures parseability but not schema compliance; for that, combine with a Pydantic/JSON Schema validator on your side. *Introduced: Day 27.*

### Latency
**Field:** Time from sending the prompt to receiving the (full or first-token) response.

Prompt-engineering choices that increase latency: longer outputs (CoT, verbose formats), larger system prompts (one-time cost per request unless cached), chained calls (latency sums across the chain). Generally a tradeoff against quality. *Cross-reference: Week 2 (Inference Engineering).* *Used: Day 28, Day 30.*

### MCP (Model Context Protocol)
**Field:** An open standard for describing tools and resources that any LLM can use, in a model-agnostic way.

You'll meet MCP properly in Week 7. For Day 30, the relevant idea is: MCP is the standard for **tool manifests** — descriptions of available tools and their schemas — that supersedes each provider's bespoke format. *Introduced: Day 30, expanded Week 7.*

### Persona
**Field:** A role or character the model is told to adopt for the conversation. Synonym: role.

Personas measurably shift the output distribution because the model has seen many examples of each persona's writing style in its training data. Place stable personas in the system prompt; use inline persona instructions for one-shot persona switches. *Introduced: Day 27.*

### Prefill (speaking for the model)
**Field:** Supplying an assistant-role message yourself, which the model then continues from.

The single most reliable technique for forcing structured output: put `{` as a prefill and the model is committed to continuing JSON. Or put `<verdict>` and the model is committed to filling in your output schema. Not all APIs expose prefill — Anthropic's Messages API does; OpenAI's does not directly but you can simulate. *Introduced: Day 27.*

### Prompt injection
**Field:** An attack where an adversary embeds instructions inside user-supplied data, hoping the model will follow them as if they were part of the system prompt.

Two flavors: **direct** (the user themselves writes the injection: "ignore previous instructions and...") and **indirect** (the model retrieves attacker-controlled content from elsewhere — a webpage, a document, a database — that contains an injection). The first line of defense is delimiter discipline (see *Delimiter*). The second is input validation. The third is output review. None alone is sufficient; defense is layered. *Introduced: Day 27, revisited Day 33 (Week 7).*

### Prompt template
**Field:** A prompt with variable slots (e.g. `{{ user_question }}`, `{{ retrieved_docs }}`) that get filled in at request time.

The basis of any production prompt system. Standard formats: Jinja, f-strings, Mustache, LangChain's `PromptTemplate`. Keep templates in version control; treat changes the way you treat code changes. *Used: Day 29.*

### RAG (Retrieval-Augmented Generation)
**Field:** A pattern that retrieves relevant passages from a corpus and includes them in the prompt as context, so the model answers from those passages rather than from its parametric memory.

Reduces hallucination dramatically because the source of truth is in the prompt. The prompt-engineering piece is one instruction ("answer only from the documents below"); the harder engineering is the retrieval (embeddings, vector DBs, chunking, reranking — a topic for another week). *Introduced: Day 30.*

### Role
**Field:** (1) In the API: the `role` field on a message — `"system" | "user" | "assistant" | "tool"`. (2) In prompting: synonym for persona — the character the model is told to adopt.

Don't confuse these uses. API roles are structural; prompting roles are content. *Introduced: Day 26 (API sense), Day 27 (persona sense).*

### Scratchpad
**Field:** An explicit space (often wrapped in `<scratchpad>...</scratchpad>` tags) where the model is instructed to do its reasoning before giving the final answer.

A structured form of chain-of-thought that allows downstream code to strip the reasoning and ship only the final answer. The model still pays the token cost of generating the scratchpad, but end users never see it. *Introduced: Day 28.*

### Schema-by-example
**Field:** A technique for forcing structured output by showing the model the exact shape (often with placeholder values) of the desired output.

More reliable than a prose description like "return a JSON object with the fields." Example: `Return JSON matching: { "city": "string", "population": integer }`. Combines well with prefill for the highest reliability. *Introduced: Day 27.*

### Specificity
**Field:** The opposite of vagueness. A specific prompt narrows the model's output distribution by giving the model unambiguous information about audience, format, scope, and success criteria.

The Anthropic tutorial's Chapter 2 motto: "specificity beats vagueness." The single highest-leverage fix for "the model isn't giving me what I want." *Introduced: Day 26.*

### System prompt
**Field:** Instructions and context that apply to the whole conversation, sent with `role: "system"` in the messages array.

Stable across turns. Conventionally used for persona, rules, style, and constraints. Caching of system-prompt prefixes is a major cost-reduction technique at scale (Anthropic's prompt caching, OpenAI's `cached_input` pricing). *Introduced: Day 26.*

### Temperature
**Field:** A sampling parameter controlling the randomness of the model's output. `0` is deterministic (always pick the most likely next token); higher values flatten the distribution and produce more varied outputs.

Typical defaults: `0` for structured output and reproducibility; `0.7` for chat and creative generation; rarely above `1.0`. Prompt-engineering implication: when running evals or A/B-testing prompts, fix `temperature=0` to remove sampling noise from your comparison. *Cross-reference: Week 1 (Inference Engineering).* *Used: Day 26.*

### Token
**Field:** The unit the model processes — roughly a word fragment. English text averages ~4 characters per token. "Hello world" is 2 tokens; "antidisestablishmentarianism" is 6.

Prompt-engineering implications: billing is per token (input and output usually priced differently), context windows are measured in tokens, and "the model is slow" usually means "the model is generating a lot of output tokens." *Cross-reference: Week 1 (Inference Engineering).* *Used: throughout.*

### Tool use
**Field:** A pattern where the model produces structured output describing a function call, your code executes the actual function, and the result is returned to the model as a new turn.

Mechanically: tool use is structured output (Day 27) plus a small driver loop. Every "AI agent" you encounter is built on this pattern. MCP standardizes the manifest format. *Introduced: Day 30, expanded Week 7.*

### Turn
**Field:** A single entry in the `messages` array — one user turn, one assistant turn, etc.

Multi-turn conversations alternate user and assistant turns; the model receives the full history and conditions its next reply on all of it. Important: multi-turn does *not* mean "the model remembers" — there is no server-side memory; you re-send the full history every request. *Introduced: Day 26.*

### User turn
**Field:** A message in the `messages` array with `role: "user"`, representing the actual question, data, or task for that step of the conversation.

Where dynamic per-request content goes. Should contain instructions and data the model needs *for this turn*; stable rules go in the system prompt. *Introduced: Day 26.*

### Vagueness traps
**Field:** Three patterns that consistently produce unreliable prompts: undefined audience, undefined format, undefined success criteria.

A diagnostic checklist for any prompt you're not happy with. Almost every "the model is dumb" complaint maps to one of these three. *Introduced: Day 26.*

### Zero-shot
**Field:** A prompt with no examples — just the instruction and the input.

Contrasts with few-shot (2–5+ examples). Zero-shot is the default; few-shot is the upgrade path when zero-shot is unreliable. Most chat conversations are zero-shot. *Used: Day 28.*

---

# Appendix A — Production Vocabulary (additions)

The terms above cover everything in the week's lectures. This appendix adds vocabulary you'll need on the job — terms that appear in production incident reports, model cards, and on-call handoffs but didn't fit in the main lessons.

### Abstention
**Field:** Authorized refusal — the model declines to answer because the question is unanswerable from the provided context.

A defense against hallucination. Without explicit permission to abstain, the model answers anyway with whatever is most-probable, leading to ~46% hallucination rates on unanswerable questions. With explicit permission ("If the context does not contain the answer, respond exactly: 'I don't know based on the provided context.'"): <5%. *Cross-reference: Day 29.*

### Attention position bias
**Field:** The empirical pattern where instructions placed in the middle of a long prompt are followed 15-25 percentage points less reliably than the same instructions at the top or bottom.

Same root cause as "lost in the middle" in long-context RAG. Practical rule: put the most important instruction at the top *or* the bottom, never in the middle of a 4K+ token prompt. *Cross-reference: Day 26.*

### Citation discipline
**Field:** A prompting pattern requiring the model to cite the chunk number (or other identifier) for every factual claim, with explicit instruction to omit claims it cannot cite.

Drops fabrication rate from ~12% to <1% at a cost of ~30% more output tokens for the citation markers themselves. Prerequisite for any production prompt that touches regulated content (medical, legal, financial). *Cross-reference: Day 29.*

### Constrained decoding
**Field:** A sampling-time mechanism (grammar-based, regex-based, or finite-state-machine-based) that forces the model to emit tokens that conform to a target grammar.

Used to guarantee valid JSON, valid SQL, valid function-call syntax. Differs from "JSON mode" in that constrained decoding is grammar-aware; JSON mode is brace-balancing. Cost: ~10-20% latency overhead, and the model can be forced into syntactically valid but semantically wrong output. Implementations: outlines, guidance, vllm structured outputs, llama.cpp grammars. *Cross-reference: Day 27.*

### Direct vs. indirect injection
**Field:** Two flavors of prompt injection. **Direct**: the user themselves writes the malicious instruction. **Indirect**: the model retrieves attacker-controlled content (a webpage, a document, a database row, an email) that contains the injection.

Indirect is far more dangerous because the user is unaware the injection exists. EchoLeak (CVE-2025-32711, Microsoft 365 Copilot, mid-2025) is the canonical real-world example: emails containing injection payloads were summarized by Copilot, leading to data exfiltration. *Cross-reference: Day 27.*

### Distribution shift
**Field:** Any change to the conditioning context that moves the model's output probability distribution. The mechanism by which roles, examples, delimiters, and instructions all "work."

Frame everything you do in prompting as a distribution shift. There is no magic instruction channel; there is only conditioning. *Cross-reference: throughout.*

### Eval-driven development
**Field:** A workflow discipline where every prompt change is gated by a regression run of the eval suite. The prompt is "code"; the eval is "tests"; you don't ship if a test fails.

Break-even point: a 4-engineer-hour eval suite pays for itself the first time it catches a regression. Most teams catch the first regression within a month of writing the suite. *Cross-reference: Day 30.*

### Function calling (legacy term)
**Field:** OpenAI's pre-MCP name for tool use, where the model emits a JSON object specifying a function name and arguments.

Same concept as tool use; older vocabulary. Most provider docs now say "tool calling" or "tool use." *Cross-reference: Day 30.*

### Guardrails
**Field:** Pre- or post-processing checks that validate model input (against allowlists) or output (against safety classifiers, regex denylists, schema validators).

Distinct from prompt-level defenses (delimiters, abstention). Guardrails are *external* to the model and run as separate components. Tools: NeMo Guardrails, Guardrails-AI, Lakera, custom code. *Used in: Day 27 discussions, Week 7 deepens.*

### LLM-as-judge
**Field:** A pattern where one LLM grades another LLM's output, used as the "pass criterion" in an eval suite.

Useful for evaluating subjective qualities (helpfulness, conciseness, tone). Known limitations: judges have position bias (prefer first answer), self-bias (prefer outputs from the same model), and verbosity bias (prefer longer answers). Mitigations: use a different model than the one being evaluated, randomize order, include rubric. *Cross-reference: Day 30.*

### Negative case
**Field:** An eval case where the *correct* output is a refusal, an abstention, or a "not applicable" — used to test that the prompt doesn't over-comply.

Eval suites that consist only of positive cases miss the most important failures: false positives, over-eager tool calls, hallucinated answers to unanswerable questions. A healthy suite is 70% positive / 30% negative. *Cross-reference: Day 30.*

### Prefix caching
**Field:** A provider-side optimization that caches the KV-state of the prompt prefix (typically the system prompt) so subsequent requests with the same prefix skip recomputation.

Anthropic charges 10% of normal input price for cached prefix tokens (90% discount on hit). At 10M requests/month with a 2K-token system prompt, savings: ~$54K/month vs. uncached. The caching boundary is the *exact* prefix; any change invalidates the cache. *Cross-reference: Day 26.*

### Reasoning model
**Field:** A model trained or fine-tuned to do extended chain-of-thought internally before producing its final answer. Examples: OpenAI o1/o3, Anthropic Claude Sonnet thinking, DeepSeek R1.

Where ordinary CoT pays the reasoning-token cost on every call, reasoning models amortize it into a (more expensive) per-call price. Useful when you need consistent reasoning without writing the CoT prompt yourself. *Cross-reference: Day 28.*

### Self-consistency
**Field:** A technique where you run the same CoT prompt N times at non-zero temperature, then take the majority vote of the *final answers* (not the reasoning chains).

Lifts accuracy ~+11 points over single CoT at a cost of 5× compute. Worth it on high-value decisions; wasteful on bulk processing. *Cross-reference: Day 28.*

### Sliding-window context
**Field:** A pattern for multi-turn conversations where, when the cumulative context approaches the model's window limit, older turns are dropped or summarized.

The wrong way: drop oldest turns blindly. The right way: summarize the dropped span into a single condensed turn ("Summary of earlier conversation: ..."). Required for any chat product that supports long sessions. *Used in: Day 30 discussion.*

### Stop sequences
**Field:** Strings that, when emitted by the model, cause sampling to halt immediately. Configured per-request.

Use cases: stopping after a closing tag in a multi-section output (`</answer>`), stopping before the model emits a "Q:" that would invite a follow-up question, enforcing a single-turn output. Provider-specific syntax. *Used in: structured-output exercises.*

### Top-p / nucleus sampling
**Field:** A sampling parameter (also `top_p`) that restricts the next-token candidate set to the smallest set whose cumulative probability exceeds `p`.

Less commonly tuned than temperature, but useful: `top_p=0.1` is essentially deterministic without the kernel-determinism quirks of `temperature=0`. Most production code leaves it at the default (1.0) and tunes temperature only. *Cross-reference: Week 1 (Inference Engineering).*

---

# Appendix B — Acronyms & quick-reference

| Acronym | Expansion | First appearance |
|---|---|---|
| CoT | Chain-of-Thought | Day 28 |
| CSV | Comma-Separated Values (a structured-output target) | Day 27 |
| FSM | Finite-State Machine (constrained-decoding mechanism) | Appendix A |
| JSON | JavaScript Object Notation | Day 27 |
| KV cache | Key-Value cache (the transformer state cached for prefix reuse) | Appendix A |
| LLM | Large Language Model | throughout |
| MCP | Model Context Protocol | Day 30 |
| OSL | Output Sequence Length (token count) | Day 30 evals |
| ISL | Input Sequence Length (token count) | Day 30 evals |
| RAG | Retrieval-Augmented Generation | Day 30 |
| RLHF | Reinforcement Learning from Human Feedback | Week 4 (IE) |
| RTF | Real-Time Factor (audio/speech context) | Week 5 (IE) |
| TTFT | Time-To-First-Token | Day 30, Capsule M8 |
| XML | eXtensible Markup Language (delimiter convention) | Day 27 |

---

# Appendix C — Concept-Graph Anchors

For each term in this glossary, the concept ID in `docs/kb/concepts.json` (when present). The knowledge-base file is introduced in PR-C of the reorg; references may be unresolved until that PR merges.

| Term | Concept ID |
|---|---|
| Abstention | `abstention` |
| Attention position bias | `attention-position-bias` |
| Chain-of-Thought | `chain-of-thought` |
| Chaining | `prompt-chaining` |
| Citation discipline | `citation-discipline` |
| Constrained decoding | `constrained-decoding` |
| Delimiter | `delimiter-discipline` |
| Eval | `eval-suite`, `prompt-as-code` |
| Few-shot | `few-shot-learning`, `in-context-learning` |
| Grounding | `grounding`, `rag-trust` |
| Hallucination | `hallucination` |
| LLM-as-judge | `llm-as-judge` |
| MCP | `mcp` |
| Prefix caching | `prompt-caching` |
| Prompt injection | `prompt-injection` |
| Reasoning model | `reasoning-models` |
| Role | `role-prompting` |
| Self-consistency | `self-consistency` |
| Structured output | `structured-output` |
| System prompt | `system-prompt` |
| Temperature | `temperature-determinism` |
| Tool use | `tool-use` |
