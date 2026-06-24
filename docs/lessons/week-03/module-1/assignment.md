# Week 3 — KV Cache, Attention, Quantization · Module Assignment


## What you submit

A working **memory-budget calculator** (Python script *or* spreadsheet) plus a **short written analysis** (≤ 300 words).

## The calculator — inputs

- `gpu_hbm_gb` — e.g. 80 for H100.
- `num_gpus` — for tensor parallelism.
- `model_weights_gb` — at the chosen precision (FP16/FP8/INT4 — pass as a setting).
- `num_layers`, `num_kv_heads`, `head_dim`, `kv_dtype_bytes` — KV cache shape.
- `context_length` — max sequence length the deployment will support.
- `batch_size` — concurrent requests served at full context.
- `overhead_gb` — fixed reserve for activations, framework, fragmentation (use 4 GB default).

## The calculator — outputs

For the given config, print:

1. Per-GPU weight memory (GB).
2. Per-token KV cache size (KB).
3. Total KV cache memory at full context × batch (GB).
4. **Fits or doesn't fit** verdict, and how much HBM is left over.
5. If it doesn't fit: suggest the smallest single change that makes it fit (drop batch, drop context, quantize KV, add a GPU).

## Test cases your calculator must handle

| Config | Expected verdict |
|---|---|
| Llama-3-8B FP16, 1×H100, 32K context, batch=8 | Fits |
| Llama-3-8B FP16, 1×H100, 128K context, batch=1 | Just barely fits |
| Llama-3-70B FP16, 8×H100, 32K context, batch=8 | Fits |
| Llama-3-70B FP16, 8×H100, 128K context, batch=8 | Doesn't fit — suggest FP8 KV |
| Llama-3-70B FP8 weights + FP8 KV, 8×H100, 128K, batch=8 | Fits |

## The written analysis (≤ 300 words)

Pick one config that *doesn't* fit naively, and walk through the reasoning chain: **what's the dominant cost, which lever do you pull first, and why.**

## What "good" looks like

- The calculator runs from the CLI / opens cleanly in Sheets, and prints all 5 outputs.
- All five test cases produce the expected verdict (verified against the reference solution in `planning/source-material/Inference Engineering/Inference_Engineering_Worksheets.md`).
- The written analysis uses Week 3 vocabulary correctly (KV cache scaling, quantization tradeoff, memory-bound decode).

## Grading

- Calculator works on 4/5 test cases — pass.
- Written analysis identifies the right dominant cost — pass.
- Both required to pass the assignment.

## Why this assignment exists

A serving engineer's first job is **"can it fit?"** Everything downstream — engine choice, parallelism, precision, autoscaling — branches off that one calculation. Build it once, by hand, and you will never again misjudge whether a deployment is feasible.
