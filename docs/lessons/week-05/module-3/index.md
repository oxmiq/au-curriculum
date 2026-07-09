# Day 23 · Evaluation & Quality

> **Concept of the day:** **perplexity** for sanity, **benchmarks** for comparison, **task evals** for production decisions. Public benchmarks are gameable; your own eval suite is the only one that matters. **Quantization quality must be measured, not assumed.**
> **Pre-reading:** "Evaluating LLMs" overview — <a href="https://huggingface.co/docs/evaluate/index" target="_blank" rel="noopener">Hugging Face — Evaluate</a> + <a href="https://eugeneyan.com/writing/llm-evaluations/" target="_blank" rel="noopener">Eugene Yan — How to Evaluate LLMs</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 5 — Metrics &amp; Production</a>
    <span class="sep">/</span>
    <span>Day 23 · Evaluation & Quality</span>
    {status:week-05/module-3}
  </div>
  <div class="ox-lesson-header__cta">
    <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
    <a class="md-button md-button--primary" href="knowledge-check/">Knowledge check</a>
    <a class="md-button" href="assignment/">Assignment</a>
    <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| # | What you do |
|---|-------------|
| 1 | Why Evaluation Matters |
| 2 | Three Evaluation Layers |
| 3 | Build a Task Eval Suite |
| 4 | Quantization Quality Check |
| 5 | LLM-as-a-Judge |
| 6 | Design Your Eval Pipeline |
| 7 | Wrap-up & Connection |

---

## Part 1 — Why Evaluation Matters

### Before You Start

You should have already read: <a href="https://huggingface.co/docs/evaluate/index" target="_blank" rel="noopener">Hugging Face — Evaluate</a> + <a href="https://eugeneyan.com/writing/llm-evaluations/" target="_blank" rel="noopener">Eugene Yan — How to Evaluate LLMs</a>.

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m3-readiness" data-kind="readiness" data-draw="5" data-source="Hugging Face Evaluate + Eugene Yan — Evaluating LLMs">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is perplexity in LLM evaluation?",
    "options": [
      "A measure of how confused the model is about its predictions",
      "The exponential of cross-entropy loss; lower is better",
      "A benchmark for coding tasks",
      "The number of parameters in the model"
    ],
    "answer": 1,
    "explain": "Perplexity is the exponential of cross-entropy loss. It measures how well the model predicts the next token — lower perplexity means the model is more certain (less confused) about its predictions. It's primarily used as a sanity check, not a final measure of quality."
  },
  {
    "stem": "Why are public benchmarks like MMLU sometimes insufficient for evaluating LLMs in production?",
    "options": [
      "They are too expensive to run",
      "They can be gameable and may not reflect performance on your specific task",
      "They require special hardware",
      "They are only available for English"
    ],
    "answer": 1,
    "explain": "Public benchmarks (MMLU, HumanEval, etc.) can be 'gamed' — models can be trained specifically to perform well on these benchmarks without having genuine capability. For production, you need task-specific evals that measure actual performance on your use case."
  },
  {
    "stem": "What is 'LLM-as-a-Judge' in evaluation?",
    "options": [
      "Using another LLM to evaluate the outputs of the model being tested",
      "Having human experts judge model outputs",
      "A benchmark specifically for legal tasks",
      "A method for comparing two models directly"
    ],
    "answer": 0,
    "explain": "LLM-as-a-Judge uses a separate LLM (often GPT-4 or similar) to evaluate and score the outputs of the model being tested. It's useful for evaluating open-ended tasks where traditional metrics don't work well, though it has biases."
  },
  {
    "stem": "What is the key insight about quantization quality mentioned in the pre-read?",
    "options": [
      "Quantization always improves quality",
      "Quantization quality must be measured, not assumed",
      "Quantization has no impact on quality",
      "Higher quantization always causes more quality loss"
    ],
    "answer": 1,
    "explain": "Quantization quality must be measured, not assumed. Different models and quantization methods affect quality differently. A 5% quality regression on your specific task might be acceptable, but it must be measured — you can't assume FP16→INT8 is lossless."
  },
  {
    "stem": "What is a task-specific eval suite?",
    "options": [
      "A suite of benchmarks that are publicly available",
      "A custom set of evaluations designed for your specific use case",
      "A method for testing model speed",
      "The standard evaluation framework for all models"
    ],
    "answer": 1,
    "explain": "A task-specific eval suite is a custom set of evaluations designed for your specific use case or task. While public benchmarks are useful for comparison, your own eval suite is what actually matters for production decisions."
  },
  {
    "stem": "What are the 'Three Evaluation Layers' typically used for LLM quality assessment?",
    "options": [
      "Training, validation, testing",
      "Perplexity, benchmarks, and task evals",
      "Input, processing, output",
      "Pre-training, fine-tuning, deployment"
    ],
    "answer": 1,
    "explain": "The three evaluation layers are: (1) Perplexity — for sanity checking during training, (2) Benchmarks — for comparing models on standard tasks, (3) Task evals — for measuring actual performance on your specific use case."
  },
  {
    "stem": "Why might a model that scores well on MMLU still be unsuitable for your production use case?",
    "options": [
      "MMLU scores are always wrong",
      "MMLU measures general knowledge, not task-specific capability",
      "MMLU is only for English models",
      "MMLU is not a real benchmark"
    ],
    "answer": 1,
    "explain": "MMLU measures general knowledge and reasoning, not task-specific capability. A model that scores well on MMLU might still perform poorly on your specific task (e.g., code generation, instruction following, domain-specific Q&A). Task-specific evals are essential."
  },
  {
    "stem": "What is the relationship between evaluation metrics and business outcomes in ML systems?",
    "options": [
      "There is no relationship",
      "Eval metrics connect engineering speedups to business outcomes",
      "Business outcomes are more important than metrics",
      "Metrics are only for research, not production"
    ],
    "answer": 1,
    "explain": "Evaluation metrics are what close the loop between engineering (faster models, quantization, etc.) and business outcomes (user satisfaction, task completion, revenue). Without good evals, you can't quantify whether your optimizations actually improve the product."
  }
]
</script>
</div>

### Reading

A quantized model that ships with 5% quality regression on *your task* will silently lose customers. A model that scores +2 on MMLU might be worse for *you*. Eval is the only thing that closes the loop between engineering speedups and business outcomes.

### Reflection (write your answer)

Take 2 minutes to write down:
> Why is "it scores 85% on MMLU" not enough to ship a model to production?

---

## Part 2 — Three Evaluation Layers

### Layer 1: Sanity (Perplexity)

**Perplexity** = exp(cross-entropy) on a held-out text set.

- **What it tells you:** The model still produces "reasonable" probability distributions
- **What it misses:** Task-specific quality
- **Goes up** = quality dropped

**Use for:** Catching catastrophic damage from a bad quantization or bug.

### Layer 2: Benchmarks (MMLU, etc.)

| Benchmark | What It Tests | Use For |
|-----------|---------------|---------|
| MMLU | Multi-subject knowledge (57 subjects) | Quick comparison |
| HellaSwag | Commonsense reasoning | Reasoning check |
| HumanEval / MBPP | Code generation | Code products |
| GSM8K / MATH | Math word problems | Math ability |
| HELM | Multi-task batteries | Comprehensive |

> **Goodhart again:** Model trainers know which benchmarks matter. They optimize for those. MMLU saturation has more to do with training data leakage than capability gains.

**Benchmarks are for comparing — never for declaring production ready.**

### Layer 3: Task Evals (Your Own Suite)

Build a suite of **50–200 prompts** that look like real production traffic.

For each prompt:
- Reference output (if available) OR
- Graded rubric (what makes a "good" response)

**Report:**
- Pass rate (binary correct/incorrect)
- Format compliance (valid JSON? structured output?)
- Safety / refusal behavior
- Side-by-side win rate vs previous deployment

> **Task evals are for shipping decisions — benchmarks are tiebreakers.**

---

## Part 3 — Build a Task Eval Suite

### Exercise: Create a 10-Prompt Eval Suite

**Use case:** "Summarize a Slack thread"

For each of these 10 scenarios, write a prompt and define what makes it "pass" or "fail":

1. Short thread (5 messages) → Summary < 50 words
2. Long thread (50 messages) → Summary captures all key points
3. Thread with decisions → Summary includes decisions made
4. Thread with questions → Summary identifies unanswered questions
5. Thread with code snippets → Code is preserved accurately
6. Thread with links → Links are preserved
7. Thread with emoji/reactions → Tone captured
8. Thread with a debate → Both sides summarized
9. Thread in another language → Language preserved appropriately
10. Thread with no clear content → Appropriate "nothing to summarize" response

### Write Your Rubric

For each prompt, define:
- **Input:** The Slack thread (simulated)
- **Expected output:** What a good summary looks like
- **Pass criteria:** 3-5 specific things that must be present

---

## Part 4 — Quantization Quality Check

### Scenario

A teammate proposes: "Let's quantize to INT4 — only 1% perplexity loss."

### Exercise: Your Counter-Checklist

Before approving any quantization change, you must verify:

1. **Perplexity check** — Run on a held-out set. Reject if Δ > ___%
2. **Task eval check** — Run your task eval suite. Reject if regression > ___ percentage points
3. **Side-by-side human eval** — Compare 50 outputs. Reject if win rate < ___%
4. **Refusal-rate sanity** — Did we break safety tuning?
5. **Format compliance** — Did we break JSON output?

**Fill in the thresholds** from Day 23's content.

### Discussion

**Why is perplexity not enough?**

Even with only 1% perplexity loss, the model could:
- Lose instruction-following capability
- Become worse at your specific task
- Have degraded safety behavior

**Fill in:** Perplexity catches ___% of problems; task eval catches the rest.

---

## Part 5 — LLM-as-a-Judge

### Reading — When It Works, When It Deceives

A bigger model (often GPT-4 or Claude) grades the smaller model's outputs. **Cheap to run, dangerous to trust.**

| Works Well | Works Poorly |
|------------|--------------|
| Format / structural checks | Subjective quality (length, style) |
| Factuality with reference | Math correctness without reference |
| Pairwise win-rate | Absolute scoring (judges are biased toward positive scores) |

**Always pair with human spot-checks** on ~10% of items.

### Exercise: Design a Judge Prompt

Design an LLM-as-a-judge prompt for grading:

> "Is this JSON valid and complete per the schema?"

**Potential deception points:**
- The judge might accept invalid JSON that "looks right"
- The judge might miss subtle schema violations
- The judge might be biased toward longer outputs

**How would you mitigate these?**

---

## Part 6 — Design Your Eval Pipeline

### The Quantization-Quality Contract

Standard process when you push FP16 → FP8 (or any precision change):

1. **Perplexity delta** on a held-out set. Reject if Δ > 1%.
2. **Task eval pass rate**. Reject if regression > 2 pp.
3. **Side-by-side human eval** on 50 prompts. Reject if win rate < 45%.
4. **Refusal-rate sanity** (didn't break safety tuning).

Document and ship.

### Reflection Question

Write one sentence:
> The quality contract ensures that ___ doesn't ship without measuring ___.

---

## Part 7 — Wrap-up & Connection

### Synthesis

Today's three layers — perplexity, benchmarks, task evals — form the quality axis of the SLO tripod. Tomorrow you tackle the third axis: **cost**. Every decision you make about quantization and serving has a dollar sign attached. The quality contract you built today is what protects you from optimizing cost at the expense of your users.

### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-05-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 23 · Evaluation &amp; Quality">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What does perplexity measure, and what does it miss?",
    "options": [
      "It measures user satisfaction; it misses factual accuracy",
      "It measures how well the model predicts the next token on a held-out text corpus; it misses whether the outputs are useful, factual, or safe for real tasks",
      "It measures inference latency; it misses memory usage",
      "It measures model size; it misses output diversity"
    ],
    "answer": 1,
    "explain": "Perplexity = average inverse probability of each next token on a reference corpus. Low perplexity = model assigns high probability to the correct next tokens. But a model can have low perplexity and still hallucinate, refuse questions, or produce outputs that fail on real tasks. Perplexity is a proxy, not a production quality measure."
  },
  {
    "stem": "Why might a high MMLU score be misleading about a model's production quality?",
    "options": [
      "MMLU is only available for English-language models",
      "MMLU measures multiple-choice academic knowledge, which may not reflect the specific tasks your users actually perform; high MMLU can coexist with poor task performance",
      "MMLU scores are too hard to compare across model families",
      "MMLU is not publicly reproducible"
    ],
    "answer": 1,
    "explain": "Goodhart's Law: when a measure becomes a target, it ceases to be a good measure. Models fine-tuned to maximize MMLU may regress on your specific use case. MMLU tests academic knowledge domains — your production task may be code generation, customer service, or medical Q&A, all requiring different capabilities."
  },
  {
    "stem": "What is a task eval and how does it differ from a benchmark like MMLU?",
    "options": [
      "A task eval is automated; MMLU requires human graders",
      "A task eval uses your actual use-case inputs and evaluates model outputs against task-specific criteria; MMLU uses standardized academic questions testing general knowledge",
      "A task eval is cheaper to run than MMLU",
      "A task eval uses larger context windows than MMLU"
    ],
    "answer": 1,
    "explain": "A task eval uses prompts drawn from your actual production distribution with criteria matched to what your users care about (accuracy, format, tone). MMLU is a general academic benchmark. The lesson states: 'task eval (your own use-case suite)' is more honest about production quality than generic benchmarks."
  },
  {
    "stem": "What is Goodhart's Law and why is it relevant to LLM evaluation?",
    "options": [
      "Models improve exponentially with scale — relevant because larger models don't always score better on benchmarks",
      "When a metric becomes a target, it ceases to be a good measure — relevant because optimizing for MMLU or other benchmarks doesn't guarantee production quality",
      "GPU compute doubles every 18 months — relevant because evaluation methods must keep pace with hardware",
      "A model's quality is bounded by its training data quality — relevant because evaluation must consider data provenance"
    ],
    "answer": 1,
    "explain": "Goodhart's Law states: 'When a measure becomes a target, it ceases to be a good measure.' In LLM evaluation, the lesson warns about 'MMLU saturating not actually being progress' — models fine-tuned to pass benchmarks may not improve on real tasks. This is why task evals > benchmarks for production decisions."
  },
  {
    "stem": "What are the three layers of the quality evaluation stack described in this lesson?",
    "options": [
      "Speed, accuracy, and cost",
      "Perplexity (language modeling proxy), benchmarks (standardized multi-domain tests), and task evals (use-case specific evaluation)",
      "Unit tests, integration tests, and end-to-end tests",
      "Offline eval, online eval, and human eval"
    ],
    "answer": 1,
    "explain": "The lesson's synthesis describes 'three layers — perplexity, benchmarks, task evals — form the quality axis of the SLO tripod.' Each layer has a different role: perplexity for relative comparison, benchmarks for cross-model comparison, task evals for production go/no-go decisions."
  },
  {
    "stem": "What is a quality contract in the context of LLM deployment?",
    "options": [
      "A legal agreement between the LLM vendor and the customer",
      "A pre-defined set of eval criteria that must pass before a model or configuration change ships to production",
      "A commitment to users about model uptime and availability",
      "A document specifying the model's training data sources"
    ],
    "answer": 1,
    "explain": "A quality contract specifies: which task eval suite runs, what pass criteria are (e.g., 8/10 prompts pass all criteria), and that the gate must clear before shipping. It protects against regressing quality while optimizing cost or latency — the lesson says it 'ensures that nothing ships without measuring quality.'"
  }
]
</script>
</div>

### Pre-read for tomorrow (Day 24 · Cost & Economics)

- **Resource:** <a href="https://a16z.com/the-economics-of-ai-inference/" target="_blank" rel="noopener">a16z — The Economics of AI Inference</a>.
- **Reflection questions:**
  1. What dominates cost: prefill tokens or decode tokens? Why?
  2. **Dedicated GPU** vs **token-priced API** — at what utilization does dedicated break even?
  3. Why does **GPU utilization** translate directly to cost-per-million-tokens?

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
