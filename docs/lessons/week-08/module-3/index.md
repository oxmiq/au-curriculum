# Day 39 · Streaming

> **Concept of the day:** `capsule stream` gives you a live hardware-encoded desktop or single-app view of a remote machine. Know when to use it vs `capsule term`, how GPU hardware encoding works, and what backpressure / network sensitivity looks like.<br> **Pre-reading:** Capsule Power User Lab Guide **Module 7** (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 8 — Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <span>Day 39 · Streaming</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-08/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Streaming Architecture | 25 min |
| Part 3 | Core Concepts: When to Stream vs Term/Exec | 20 min |
| Part 4 | Hands-On: Launch Desktop Stream | 25 min |
| Part 5 | Hands-On: App Streaming & Containers | 25 min |
| Part 6 | Core Concepts: Network Sensitivity & Failure Modes | 20 min |
| Part 7 | Wrap-up & Connection | 10 min |
| **Total** | | **~140 min + pre-reading** |

---

## Part 1 — Pre-Reading Review · 15min

### Reading —

Before continuing, you should have read **Lab Guide Module 7** (Streaming). It covers:

- The `capsule stream` command and its flags
- The `capsule docker` companion command for container workflows
- Hardware encoder options and their GPU requirements
- WebRTC transport and TURN relay fallback
- Common network failure modes

### Exercise:

Answer from memory:

1. What command opens a streaming session in Capsule? What flag limits it to a single app?
2. Name three hardware encoder options. Which GPU vendor does each correspond to?
3. What is the transport protocol for Capsule streaming?
4. What does TURN relay fallback mean and when does it activate?
5. Name one scenario where streaming is clearly better than `capsule term`, and one where term is clearly better.

---

## Part 2 — Core Concepts: Streaming Architecture · 25min

### Reading —

**`capsule stream <config-tag>`** opens a hardware-encoded WebRTC stream of the remote machine's desktop (full desktop by default; single app with `--app <name>`).

**Hardware encoding pipeline:**

```
Remote GPU → Hardware Encoder → Encoded frames
                                      ↓
                              WebRTC transport
                                      ↓
                            Client browser / viewer
                                      ↓
                              Hardware Decoder (client GPU)
```

Hardware encoders:

| Encoder | GPU requirement | OS |
|---|---|---|
| NVENC | NVIDIA GPU (any modern) | Linux, Windows |
| VAAPI | Intel or AMD GPU | Linux only |
| VideoToolbox | Apple Silicon (M1+) | macOS only |

The GPU does all encoding work — **negligible performance impact** on running workloads. Even with a stream open at 1080p/60fps, a training job on the same GPU loses < 1% throughput (encoder uses dedicated silicon, separate from compute cores).

**WebRTC transport:**

Same channel as SshRTC but for video frames. Peer-to-peer by default (best latency). Falls back to TURN relay if direct peer-to-peer is blocked (corporate firewall, symmetric NAT). You can force TURN with `--turn` for testing.

**`capsule docker <config-tag>` — companion command:**

Launches an Ubuntu container on the remote machine, drops you into a shell. By default, the container has no GPU access:

```bash
capsule docker <config-tag>           # → container, no GPU
nvidia-smi                             # → Error: no NVIDIA devices found

capsule docker <config-tag> -- --gpus all   # → container with GPU
nvidia-smi                             # → shows GPU info
```

The `-- --gpus all` passes Docker flags through the Capsule CLI to the container runtime.

### Exercise:

1. Why is NVENC hardware encoding on the GPU preferred over software encoding (CPU)?
2. A user reports that streaming uses too much of the GPU. How would you verify whether this is actually the encoder or a workload issue?
3. When does WebRTC fall back to TURN relay? What is the tradeoff (latency vs connectivity)?
4. Run `capsule docker <config-tag>` on a machine you have access to. Confirm you can reach the shell. Then exit and re-launch with `-- --gpus all`. What does `nvidia-smi` show?

---

## Part 3 — Core Concepts: When to Stream vs Term/Exec · 20min

### Reading —

**Decision table:**

| Use `capsule stream` | Use `capsule term` / `capsule exec` |
|---|---|
| GUI application (ComfyUI, Blender, browser-based debugger) | CLI command or script |
| Visual output (rendered images, model outputs in a GUI app) | Log collection / monitoring |
| Clipboard-heavy workflow (copy between remote and local) | File transfer |
| Debugging front-end / rendering on remote GPU | Running benchmarks |
| Interactive desktop app configuration | Unattended batch jobs |

**The key question:** *Does the task require a human to see and interact with a GUI?*

- Yes → stream
- No → term or exec

**Cost of streaming:**

Streaming keeps a persistent video channel open. This costs:
- ~5–15 Mbps downlink bandwidth (1080p/30fps, variable by content)
- Latency adds: ~20–50ms for local network; ~100–200ms if TURN relay

**Clipboard sync:**

`capsule stream` includes bidirectional clipboard sync by default. Text copied in a local terminal is pasteable on the remote desktop, and vice versa. This is often the main reason to use streaming even for apps that could run headless — the clipboard workflow is faster than `capsule scp` for small snippets.

### Exercise:

For each task, choose `stream` or `term/exec` and write one-sentence justification:

1. Run a PyTorch training script overnight and collect the loss curve.
2. Use ComfyUI to test a new ControlNet model with visual feedback.
3. Check whether a CUDA kernel is producing NaN values by inserting print statements.
4. Debug a React frontend rendering artifact that only appears on the GPU machine.
5. Copy a Jupyter notebook's output image to your local clipboard.

---

## Part 4 — Hands-On: Launch Desktop Stream · 25min

### Exercise:

Work through the desktop streaming flow end-to-end.

**Step 1 — Open a full desktop stream (5 min):**

```bash
capsule stream <your-config-tag>
```

Verify the desktop loads. Note the GPU listed in the stream quality overlay (if shown).

**Step 2 — Test clipboard sync (5 min):**

1. In a local terminal, copy a short text string.
2. Paste it on the remote desktop (right-click → paste, or Ctrl+V).
3. On the remote desktop, copy a different string.
4. Paste it in your local terminal. Confirm bidirectional sync works.

**Step 3 — Single-app stream (5 min):**

1. Stop the full desktop stream.
2. Launch with an installed application: `capsule stream <config-tag> --app firefox` (or another installed app on your machine).
3. Verify the app opens in the stream window.

**Step 4 — Comparison test (10 min):**

1. Stop the stream.
2. Open the same application via `capsule term`: SSH in, launch the app from the command line.
3. For your specific use case, which approach felt faster and more natural? Write one sentence comparing the two.

---

## Part 5 — Hands-On: App Streaming & Containers · 25min

### Exercise:

**Part A — Container GPU access (12 min):**

1. `capsule docker <config-tag>` — enter an Ubuntu container. Run `nvidia-smi`. Record the output (should fail or show no devices).
2. Exit. Re-launch with `-- --gpus all`. Run `nvidia-smi` again. Record the output (should show GPU).
3. Confirm GPU access with a minimal PyTorch check:

```python
python3 -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

4. What would you change if you needed a specific Docker image instead of the default Ubuntu? (Hint: `--image` flag.)

**Part B — Port forwarding alternative to streaming (13 min):**

For web-based tools (JupyterLab, ComfyUI, Gradio), you can often use `capsule term` with port forwarding instead of full streaming:

1. On the remote machine (via `capsule term`), start a simple HTTP server: `python3 -m http.server 8080`
2. In a second local terminal, set up port forwarding: `capsule port-forward <config-tag> 8080:localhost:8080`
3. Open `http://localhost:8080` in your local browser. Confirm it shows the remote machine's directory listing.
4. Stop the port forward and the server.
5. For this use case (a web UI), which is better — `capsule stream` or port forwarding? Why?

---

## Part 6 — Core Concepts: Network Sensitivity & Failure Modes · 20min

### Reading —

WebRTC streaming is bandwidth-sensitive. Know the failure modes before users report them.

| Symptom | Most likely cause | Diagnostic step | Fix |
|---|---|---|---|
| Video stutters / drops frames | Insufficient downlink bandwidth | Run a local speed test | Reduce stream quality or move to wired network |
| Input lag > 200ms | TURN relay is active (latency to relay) | `capsule stream --no-turn` — does lag drop? | Check if direct P2P is possible; contact IT to unblock |
| Stream freezes, requires reconnect | Idle timeout or network hiccup | Check `--idle-timeout` setting | Add `--idle-timeout 30m`; reconnect manually |
| GPU shows 90%+ in `nvidia-smi` during what should be idle | Normal for active stream + no workload | Confirm with `nvidia-smi dmon -s u` | This is expected; launch a real workload |
| Stream opens but shows black screen | Display compositor not running on remote | SSH in; check if X server / Wayland is running | `systemctl status display-manager` on remote |

**Reliability rule:** When users report "input lag," always run a local speed test first before assuming the encoder or relay is at fault. 80% of "streaming is slow" reports are actually a local network problem, not a Capsule problem.

**Bandwidth requirements (approximate):**

| Quality | Resolution | FPS | Downlink needed |
|---|---|---|---|
| Low | 720p | 30 | ~5 Mbps |
| Medium | 1080p | 30 | ~10 Mbps |
| High | 1080p | 60 | ~15–20 Mbps |
| Ultra | 1440p | 60 | ~25–30 Mbps |

### Exercise:

1. You receive a ticket: "streaming is choppy and video freezes every 10 seconds." Walk through the diagnostic steps in order. What is your first diagnostic command?
2. A user says "input lag makes streaming unusable." You check: P2P is working (no TURN relay). What do you check next?
3. Why does `nvidia-smi` showing 90% GPU utilization during an "idle" stream not necessarily mean the encoder is hurting your training job?

---

## Part 7 — Wrap-up & Connection · 10min

### Self-check

Before closing, tick each item:

- [ ] I can explain the hardware encoding pipeline from GPU to client browser.
- [ ] I can make the correct stream vs term decision for any given task.
- [ ] I have successfully launched a full desktop stream and a single-app stream.
- [ ] I have confirmed GPU access inside a container with `-- --gpus all`.
- [ ] I can work through the network failure mode table from memory.
- [ ] I know the `--turn` flag and what it tests.
- [ ] I know the first diagnostic step for "input lag" reports.

### Connect Forward

Streaming is the gateway to interactive GPU workloads. When you run benchmarks next week (Day 42) or monitor training runs, you'll often have a stream open alongside a terminal — the combination of visual feedback + CLI control is the daily workflow.

### Pre-read for tomorrow (Day 40 · Known Quirks)

- **Resource:** Capsule Power User Lab Guide **Module 10 (Known Quirks)** (~15 min).
- **Reflection questions:**
  1. What is `capsule cleanup` and when do you run it?
  2. Name two symptoms whose first diagnostic step is `capsule config customer show`.
  3. What is the 4-step triage decision tree for any Capsule failure?

---

## Stuck?

Ask **oxtutor** to walk through the streaming architecture, explain the TURN relay tradeoff, or quiz you on the stream vs term decision table.
