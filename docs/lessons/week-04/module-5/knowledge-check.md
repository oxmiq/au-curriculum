<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 4 - Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <a href="../">Day 20 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-04/module-5}
  </div>
</div>

# Week 4 Knowledge Check

**Week 4 · Scaling & Stacks.** 27-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative, it never blocks you, but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 4 · Scaling &amp; Stacks" data-source="Canonical knowledge check">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "Tensor parallelism reduces decode latency mainly because it:", "options": ["Divides each GPU's per-token weight reads by the TP size", "Eliminates the KV cache entirely", "Replaces FlashAttention with a faster kernel", "Adds more total HBM to the cluster"]},
  {"stem": "Which components does TP leave replicated (not split) on every rank?", "options": ["The Q/K/V and output projection matrices", "The MLP up- and down-projection matrices", "LayerNorm parameters and the residual-stream activations", "The token embedding and unembedding tables"]},
  {"stem": "TP must stay within a single node because:", "options": ["NVIDIA's license forbids cross-node tensor parallelism", "The per-layer all-reduce needs NVLink-class bandwidth (~900 GB/s) that cross-node fabrics can't sustain", "CUDA contexts cannot be shared between two processes", "Pipeline parallelism is always faster than TP"]},
  {"stem": "For Llama-3-70B in FP16 at tp=8, the per-GPU weight shard is about:", "options": ["140 GB", "70 GB", "35 GB", "17.5 GB"]},
  {"stem": "After each layer's sharded matmul, TP performs which communication primitive?", "options": ["All-reduce", "Point-to-point send", "Broadcast from rank 0", "All-to-all"]},
  {"stem": "Raising TP from 4 to 8 sometimes lowers throughput. The most likely reason is:", "options": ["HBM bandwidth drops as more GPUs are added", "PyTorch silently caps TP at 4 ranks", "The per-layer all-reduce cost grows while per-GPU compute shrinks, so comms eventually dominate", "The KV cache disappears at tp=8"]},
  {"stem": "Pipeline parallelism splits the model:", "options": ["Width-wise, within each layer", "Depth-wise, across contiguous groups of layers (stages)", "By attention head", "By numerical precision"]},
  {"stem": "A 'pipeline bubble' is:", "options": ["A GPU manufacturing defect", "A KV-cache eviction event", "Idle time in a stage waiting for input from a prior stage", "An out-of-memory crash"]},
  {"stem": "With 4 pipeline stages, the bubble fraction is smallest when you run:", "options": ["1 micro-batch", "4 micro-batches", "16 micro-batches", "64 micro-batches"]},
  {"stem": "Compared with TP, pipeline parallelism between stages needs:", "options": ["Much higher bandwidth than TP", "Much lower bandwidth: it passes activations, not weights, at stage boundaries", "Exactly the same bandwidth as TP", "No inter-GPU communication at all"]},
  {"stem": "In an MoE model with top-2-of-8 routing, each token is processed by:", "options": ["All 8 experts", "4 experts", "2 experts", "1 expert"]},
  {"stem": "The operational risk unique to expert parallelism is:", "options": ["Hot experts: uneven routing overloads some GPUs while others idle", "The KV cache growing too large for HBM", "Quantization rounding error", "Weights loading slowly from disk"]},
  {"stem": "Expert parallelism routes tokens to their experts using which communication pattern?", "options": ["All-reduce, exactly like tensor parallelism", "Point-to-point activation passing, exactly like pipeline parallelism", "A single broadcast from a central parameter server", "All-to-all: activations are dispatched to the chosen experts and results returned"]},
  {"stem": "Why is Mixtral 8x7B only ~13B active parameters despite ~47B total?", "options": ["It quantizes ~34B of parameters down to zero", "Top-2-of-8 routing sends each token through only 2 of the 8 expert MLPs per layer", "~34B of parameters live on CPU and never run at inference", "Only the attention layers run per token; all experts are skipped"]},
  {"stem": "Speculative decoding works by:", "options": ["Skipping transformer layers for easy tokens", "A small draft model proposing K tokens that the target verifies in one parallel forward pass", "Pre-computing every possible output offline", "Lossily approximating the target model's logits"]},
  {"stem": "Under proper speculative sampling, output quality versus vanilla decoding is:", "options": ["Lower: it is an approximation", "Higher than the target alone", "Provably identical to sampling from the target alone", "Random and workload-dependent"]},
  {"stem": "How does the target model decide whether to accept a draft token?", "options": ["It accepts any token whose probability clears a fixed threshold the user sets", "It applies a rejection-sampling test: accept with probability min(1, p_target/p_draft), and resample on rejection", "It compares token embeddings for cosine similarity", "It takes a majority vote across several draft models"]},
  {"stem": "If the draft is wrong on token 3 of a 5-token proposal, what happens to tokens 1-2?", "options": ["They are kept (accepted); only token 3 onward is reconsidered", "All 5 tokens are discarded and redrafted", "Tokens 1-2 are also rejected", "The draft model is disabled for the rest of the request"]},
  {"stem": "What most commonly kills speculative decoding's speedup?", "options": ["High GPU temperature causing throttling", "The draft model using more memory than the target", "A low acceptance rate: the draft mismatches the target too often (e.g. creative / high-temperature text)", "Large batch sizes reducing output accuracy"]},
  {"stem": "Why is decode specifically the phase that benefits from speculative decoding?", "options": ["Decode is memory-bound and serial, so Tensor Cores sit idle; verification turns wasted compute into extra tokens", "Decode is compute-bound and needs additional FLOPs the draft supplies", "The draft model runs on the CPU, freeing GPU memory", "It shrinks the KV cache during generation"]},
  {"stem": "Static batching is wasteful primarily because:", "options": ["It only runs on CPU", "It cannot use tensor parallelism", "New requests wait for the whole batch to finish, and short outputs idle until the longest completes", "It always runs out of GPU memory"]},
  {"stem": "Continuous batching (iteration-level scheduling) means:", "options": ["The batch composition changes after every decode step; finished requests are evicted and new ones admitted", "Requests are sorted by length before one fixed batch runs to completion", "All requests must finish before any new one can start", "Each request is given its own dedicated GPU"]},
  {"stem": "Continuous batching relies structurally on:", "options": ["FP8 weights", "Speculative decoding", "CPU offload of the KV cache", "Block-based KV-cache allocation (PagedAttention)"]},
  {"stem": "PagedAttention reduces KV-cache waste by:", "options": ["Compressing the cache with FP8 quantization", "Storing the cache in fixed-size blocks (~16 tokens) allocated and freed independently, like OS virtual memory", "Offloading the cache to CPU RAM and paging it back on demand", "Discarding KV entries during the prefill phase"]},
  {"stem": "Plain PyTorch model.generate() is typically how much slower than vLLM for serving?", "options": ["No different", "About 5-10x", "About 100x", "It is actually faster than vLLM"]},
  {"stem": "Best default engine for an OSS deployment on NVIDIA with broad model support:", "options": ["vLLM", "TGI", "TensorRT-LLM", "SGLang"]},
  {"stem": "Which engine is best suited to heavy structured-output and tool-calling (agentic) workloads?", "options": ["TensorRT-LLM", "SGLang", "TGI", "Plain PyTorch"]}
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Back to today's lesson__

    [Day 20 · Consolidation](index.md)

-   __Back to the week__

    [Week 4 - Scaling &amp; Stacks overview](../index.md)

-   __Continue the curriculum__

    [Day 21 · Latency vs Throughput](../../week-05/module-1/index.md)

</div>
