# Day 38 · Streaming

> **Concept of the day:** `capsule stream` gives you a live hardware-encoded desktop or single-app view of a remote machine. Know when to use it vs `capsule term`, how GPU hardware encoding works, and what backpressure / network sensitivity looks like.<br> **Pre-reading:** <a href="../../../readings/capsule/#day-39-files-storage-streaming">Capsule Power-User Pre-Lecture Reading - Day 39 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-7-streaming-containers">Capsule Lab Guide</a> Module 7.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 8 - Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <span>Day 38 · Streaming</span>
    {status:week-08/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Streaming Architecture |
| Part 3 | Core Concepts: When to Stream vs Term/Exec |
| Part 4 | Hands-On: Launch Desktop Stream |
| Part 5 | Hands-On: App Streaming & Containers |
| Part 6 | Core Concepts: Network Sensitivity & Failure Modes |
| Part 7 | Wrap-up & Connection |
| **Total** | |

---

## Part 1 - Pre-Reading Review

### Reading -

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

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m3-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 7">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What command opens a streaming session in Capsule?",
    "options": [
      "capsule term",
      "capsule stream",
      "capsule connect",
      "capsule watch"
    ],
    "answer": 1,
    "explain": "'capsule stream' opens a streaming session in Capsule, giving you a live hardware-encoded desktop or single-app view of a remote machine. Use the --app flag to limit it to a single app."
  },
  {
    "stem": "Which hardware encoder option corresponds to NVIDIA GPUs?",
    "options": [
      "h264_vaapi",
      "h264_nvenc",
      "h264_videotoolbox",
      "h264_software"
    ],
    "answer": 1,
    "explain": "h264_nvenc is the hardware encoder for NVIDIA GPUs. Different GPU vendors have different encoders: NVIDIA uses nvenc, AMD uses vaapi, Apple uses videotoolbox."
  },
  {
    "stem": "What is the transport protocol for Capsule streaming?",
    "options": [
      "RDP",
      "WebRTC",
      "VNC",
      "RTSP"
    ],
    "answer": 1,
    "explain": "Capsule streaming uses WebRTC as its transport protocol. WebRTC provides low-latency streaming and supports peer-to-peer connections."
  },
  {
    "stem": "What does TURN relay fallback mean?",
    "options": [
      "It automatically disconnects",
      "When direct peer-to-peer fails, traffic is relayed through a TURN server to ensure connectivity",
      "It switches to a different protocol",
      "It uses the GPU for relay"
    ],
    "answer": 1,
    "explain": "TURN relay fallback means when direct peer-to-peer WebRTC connection fails (e.g., due to NAT/firewall), traffic is relayed through a TURN server to ensure connectivity. This ensures streaming works even in restrictive network environments."
  },
  {
    "stem": "When is streaming clearly better than `capsule term`?",
    "options": [
      "For quick command execution",
      "When you need to see GPU utilization, desktop apps, or visual output",
      "When network is slow",
      "For file transfers"
    ],
    "answer": 1,
    "explain": "Streaming is better when you need to see visual output: GPU utilization graphs, desktop applications, TensorBoard, etc. Term is for quick command execution. Use streaming for visual/GUI tasks, term for shell commands."
  },
  {
    "stem": "When is `capsule term` clearly better than streaming?",
    "options": [
      "For GUI applications",
      "For quick command execution, scripts, and text-based workflows",
      "When you need hardware encoding",
      "For long-running tasks"
    ],
    "answer": 1,
    "explain": "'capsule term' is better for quick command execution, running scripts, and text-based workflows. It's lower bandwidth and more reliable than streaming for shell-based work."
  },
  {
    "stem": "What is the --app flag in capsule stream used for?",
    "options": [
      "Specifies the app name",
      "Limits streaming to a single application window instead of the full desktop",
      "Sets the application priority",
      "Launches a specific application"
    ],
    "answer": 1,
    "explain": "The --app flag limits streaming to a single application window instead of the full desktop. This reduces bandwidth and provides a cleaner view for focused work."
  },
  {
    "stem": "Why is streaming sensitive to network conditions?",
    "options": [
      "It is not sensitive",
      "Streaming sends constant video data; poor network causes lag, artifacts, or disconnection",
      "It uses more CPU",
      "It requires GPU"
    ],
    "answer": 1,
    "explain": "Streaming sends constant video data, so poor network conditions cause lag, visual artifacts, or disconnection. Unlike term where text is lightweight, streaming is bandwidth-intensive and network-sensitive."
  }
]
</script>
</div>

---

## Part 2 - Core Concepts: Streaming Architecture

### Reading -

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

The GPU does all encoding work: **negligible performance impact** on running workloads. Even with a stream open at 1080p/60fps, a training job on the same GPU loses < 1% throughput (encoder uses dedicated silicon, separate from compute cores).

**WebRTC transport:**

Same channel as SshRTC but for video frames. Peer-to-peer by default (best latency). Falls back to TURN relay if direct peer-to-peer is blocked (corporate firewall, symmetric NAT). You can force TURN with `--turn` for testing.

**`capsule docker <config-tag>` - companion command:**

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

## Part 3 - Core Concepts: When to Stream vs Term/Exec

### Reading -

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

`capsule stream` includes bidirectional clipboard sync by default. Text copied in a local terminal is pasteable on the remote desktop, and vice versa. This is often the main reason to use streaming even for apps that could run headless; the clipboard workflow is faster than `capsule scp` for small snippets.

### Exercise:

For each task, choose `stream` or `term/exec` and write one-sentence justification:

1. Run a PyTorch training script overnight and collect the loss curve.
2. Use ComfyUI to test a new ControlNet model with visual feedback.
3. Check whether a CUDA kernel is producing NaN values by inserting print statements.
4. Debug a React frontend rendering artifact that only appears on the GPU machine.
5. Copy a Jupyter notebook's output image to your local clipboard.

---

## Part 4 - Hands-On: Launch Desktop Stream

### Exercise:

Work through the desktop streaming flow end-to-end.

**Step 1 - Open a full desktop stream:**

```bash
capsule stream <your-config-tag>
```

Verify the desktop loads. Note the GPU listed in the stream quality overlay (if shown).

**Step 2 - Test clipboard sync:**

1. In a local terminal, copy a short text string.
2. Paste it on the remote desktop (right-click → paste, or Ctrl+V).
3. On the remote desktop, copy a different string.
4. Paste it in your local terminal. Confirm bidirectional sync works.

**Step 3 - Single-app stream:**

1. Stop the full desktop stream.
2. Launch with an installed application: `capsule stream <config-tag> --app firefox` (or another installed app on your machine).
3. Verify the app opens in the stream window.

**Step 4 - Comparison test:**

1. Stop the stream.
2. Open the same application via `capsule term`: SSH in, launch the app from the command line.
3. For your specific use case, which approach felt faster and more natural? Write one sentence comparing the two.

---

## Part 5 - Hands-On: App Streaming & Containers

### Exercise:

**Part A - Container GPU access:**

1. `capsule docker <config-tag>` - enter an Ubuntu container. Run `nvidia-smi`. Record the output (should fail or show no devices).
2. Exit. Re-launch with `-- --gpus all`. Run `nvidia-smi` again. Record the output (should show GPU).
3. Confirm GPU access with a minimal PyTorch check:

```python
python3 -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

4. What would you change if you needed a specific Docker image instead of the default Ubuntu? (Hint: `--image` flag.)

**Part B - Port forwarding alternative to streaming:**

For web-based tools (JupyterLab, ComfyUI, Gradio), you can often use a direct SSH port-forward instead of full streaming:

1. On the remote machine (via `capsule term`), start a simple HTTP server: `python3 -m http.server 8080`
2. In a second local terminal, set up port forwarding: `capsule ssh <config-tag> --options "-L 8080:localhost:8080"`
3. Open `http://localhost:8080` in your local browser. Confirm it shows the remote machine's directory listing.
4. Stop the port forward and the server.
5. For this use case (a web UI), which is better: `capsule stream` or port forwarding? Why?

---

## Part 6 - Core Concepts: Network Sensitivity & Failure Modes

### Reading -

WebRTC streaming is bandwidth-sensitive. Know the failure modes before users report them.

| Symptom | Most likely cause | Diagnostic step | Fix |
|---|---|---|---|
| Video stutters / drops frames | Insufficient downlink bandwidth | Run a local speed test | Reduce stream quality or move to wired network |
| Input lag > 200ms | TURN relay is active (latency to relay) | `capsule stream --no-turn` - does lag drop? | Check if direct P2P is possible; contact IT to unblock |
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

## Part 7 - Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 38 · Capsule Streaming">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the hardware encoding pipeline for Capsule streaming?",
    "options": [
      "CPU renders the frame, GPU compresses it, network sends it to the client browser",
      "GPU renders the frame, the GPU's NVENC hardware encoder compresses it, the encoded stream is sent to the client browser over WebRTC",
      "GPU renders and encodes; a separate relay server decodes and re-encodes for each client",
      "The CPU handles all encoding to avoid impacting GPU compute workloads"
    ],
    "answer": 1,
    "explain": "The Capsule streaming pipeline: GPU renders the frame (display output), the GPU's dedicated NVENC hardware encoder compresses it (separate silicon: doesn't impact compute), the H.264/H.265 stream is delivered over WebRTC to the client browser. This is why GPU utilization during streaming shows encoder activity separate from compute."
  },
  {
    "stem": "When would you use `capsule stream` instead of `capsule term`?",
    "options": [
      "stream for command-line work; term for graphical applications",
      "stream for graphical/interactive GPU applications (visual desktop, GUI tools, anything requiring display output); term for CLI-only work (scripts, benchmarks, file management)",
      "stream is always preferred over term for better performance",
      "stream for large files; term for small commands"
    ],
    "answer": 1,
    "explain": "The stream vs term decision: use `capsule stream` when you need to see graphical output (running a GUI application, visual debugging, interactive demos). Use `capsule term` for pure CLI work; it's lower overhead and more suitable for scripted commands, benchmarks, and file operations."
  },
  {
    "stem": "What does the `--turn` flag enable in `capsule stream`?",
    "options": [
      "It rotates the display output 90 degrees",
      "It forces traffic through a TURN relay server (for network environments where direct P2P WebRTC connections are blocked)",
      "It enables hardware-accelerated encoding",
      "It switches from H.264 to H.265 encoding"
    ],
    "answer": 1,
    "explain": "WebRTC tries direct peer-to-peer connection first (lower latency). If firewalls or NAT block direct connections, `--turn` forces routing through a TURN relay server. The lesson notes P2P working is the preferred path; TURN relay adds latency but ensures connectivity through restrictive networks."
  },
  {
    "stem": "Why does `nvidia-smi` showing high GPU utilization during an 'idle' stream not necessarily mean encoding is hurting your compute workload?",
    "options": [
      "nvidia-smi reports incorrect utilization for streaming workloads",
      "The GPU's NVENC hardware encoder is separate silicon from the compute units (CUDA/Tensor Cores); encoder utilization does not reduce compute throughput",
      "Streaming automatically throttles when GPU compute is high",
      "GPU utilization during streaming is always below 10% regardless of activity"
    ],
    "answer": 1,
    "explain": "Modern NVIDIA GPUs have dedicated NVENC encoder hardware separate from CUDA cores and Tensor Cores. Encoder activity shows in `nvidia-smi` but does NOT consume the compute resources your training/inference uses. High encoder utilization + high compute utilization can coexist without interference."
  },
  {
    "stem": "A user reports 'input lag makes streaming unusable.' Per the lesson's reliability rule, what is your FIRST diagnostic step?",
    "options": [
      "Restart the GPU and reconnect",
      "Run a local speed test first; ~80% of 'streaming is slow' reports are a local network problem, not Capsule; only after that do you check whether a TURN relay is adding latency",
      "Immediately disable hardware encoding and fall back to software encoding",
      "Force the resolution down to 720p without checking anything else"
    ],
    "answer": 1,
    "explain": "The Part 6 reliability rule: when users report input lag, always run a local speed test first before blaming the encoder or relay; 80% of 'streaming is slow' reports are a local network problem. Only after that do you test the transport: the failure-mode table maps 'input lag > 200ms' to an active TURN relay, diagnosed by forcing direct P2P with `capsule stream --no-turn` (does the lag drop?)."
  },
  {
    "stem": "You run `capsule docker <config-tag>` and `nvidia-smi` inside the container reports no NVIDIA devices. How do you get GPU access in the container?",
    "options": [
      "GPU access is impossible from a Capsule container",
      "Re-run `capsule auth login` first",
      "Relaunch with `capsule docker <config-tag> -- --gpus all`; the `-- --gpus all` passes the Docker flag through to the container runtime",
      "Add `--turn` to the command"
    ],
    "answer": 2,
    "explain": "By default `capsule docker` gives you an Ubuntu container with no GPU access, so `nvidia-smi` fails. Relaunch with `capsule docker <config-tag> -- --gpus all`; the `--` passes the `--gpus all` Docker flag through the Capsule CLI to the container runtime, and `nvidia-smi` then shows the GPU."
  },
  {
    "stem": "For which task should you reach for `capsule stream` rather than `capsule term`/`capsule exec`?",
    "options": [
      "Running an unattended overnight training benchmark and collecting the loss curve",
      "Pulling a report.json file back to your laptop",
      "Executing a one-off `nvidia-smi` check",
      "Interactively using ComfyUI with visual feedback on the remote GPU"
    ],
    "answer": 3,
    "explain": "The decision key is: does the task require a human to see and interact with a GUI? ComfyUI with visual feedback → yes → stream. Unattended benchmarks, file transfers, and one-off CLI checks are all text/CLI work → `capsule term` or `capsule exec`, which are lower overhead and more reliable."
  },
  {
    "stem": "Capsule streaming connects peer-to-peer by default. When does it fall back to a TURN relay, and what's the tradeoff?",
    "options": [
      "When direct P2P is blocked (corporate firewall, symmetric NAT), traffic relays through a TURN server; it guarantees connectivity but adds latency (~100–200ms via relay vs ~20–50ms local)",
      "Never: Capsule streaming is always peer-to-peer",
      "When the GPU is busy, it relays to save compute",
      "On every connection, purely to encrypt the stream"
    ],
    "answer": 0,
    "explain": "WebRTC tries direct peer-to-peer first (best latency, ~20–50ms local). If a corporate firewall or symmetric NAT blocks the direct path, it falls back to a TURN relay, which guarantees connectivity but adds a relay hop (~100–200ms). You can force relay with `--turn` for testing, or force direct P2P with `--no-turn` when diagnosing lag."
  },
  {
    "stem": "A stream opens but shows a black screen. Per the Part 6 failure-mode table, the most likely cause and check is?",
    "options": [
      "Insufficient downlink bandwidth; run a local speed test",
      "TURN relay latency; force P2P with `--no-turn`",
      "The display compositor (X server / Wayland) isn't running on the remote; SSH in and check with `systemctl status display-manager`",
      "The NVENC encoder is disabled; re-enable hardware encoding"
    ],
    "answer": 2,
    "explain": "The failure-mode table maps 'stream opens but shows a black screen' to the display compositor not running on the remote. The diagnostic is to SSH in and check whether the X server / Wayland session is up (`systemctl status display-manager`). Bandwidth issues cause stutter/dropped frames, and relay latency causes input lag: different rows."
  }
]
</script>
</div>

### Connect Forward

Streaming is the gateway to interactive GPU workloads. When you run benchmarks next week (Day 41) or monitor training runs, you'll often have a stream open alongside a terminal; the combination of visual feedback + CLI control is the daily workflow.

### Pre-read for tomorrow (Day 39 · Known Quirks)

- **Resource:** <a href="../../../readings/capsule/#day-40-consolidation-reliability-diagnostics">Capsule Power-User Pre-Lecture Reading - Day 40 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-10-scheduled-jobs-agents-and-the-reliability-toolkit">Capsule Lab Guide</a> Module 10 (Known Quirks).
- **Reflection questions:**
  1. What is `capsule session endall` and when do you run it?
  2. Name two symptoms whose first diagnostic step is `capsule config customer show`.
  3. What is the 4-step triage decision tree for any Capsule failure?

---

## Stuck?

Ask **oxtutor** to walk through the streaming architecture, explain the TURN relay tradeoff, or quiz you on the stream vs term decision table.
