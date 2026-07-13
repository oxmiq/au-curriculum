---
drift: |
  Originally Day 38 of the former Capsule wk8. Now Day 37 of the new Ops week
  (week-08/module-1), unchanged in scope. Source-material link paths bumped one level deeper.
---

# Day 37 · Connecting to Machines

> **Concept of the day:** `capsule term <config-tag>` opens a shell over the SshRTC data channel — no public-facing port needed, and Capsule auto-generates and manages the SSH keys for you. Session state lives in your home dir on the node and persists across reconnects. **Detach early, detach often** with `tmux` / `screen` — don't lose work to network blips.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#day-38-connecting-to-machines">Capsule Power-User Pre-Lecture Reading — Day 38 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-5-connecting-to-machines">Capsule Lab Guide</a> Module 5.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 8 — Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <span>Day 37 · Connecting</span>
    {status:week-08/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: The Connect Command |
| Part 3 | Core Concepts: Session State & What Persists |
| Part 4 | Deep Dive: tmux for Reliable Sessions |
| Part 5 | Hands-On: Connect, Detach, Reconnect |
| Part 6 | Hands-On: Tunneling & Multi-User Etiquette |
| Part 7 | Wrap-up & Connection |

**Total: ~140 min** (leaves buffer for reading the Lab Guide pre-read)

---

## Part 1 — Pre-Reading Review

### Reading — Why this matters

This is the moment you're actually *on* a GPU machine. Everything else — env, lease, install — was setup. Get the connection workflow right and you save hours per week; get it wrong and you'll lose 4-hour benchmark runs to network hiccups.

### Exercise: Self-Check

Before reading on, answer from memory:

1. What command connects you to a leased node?
2. How does `capsule term` differ from raw `ssh`?
3. What persists on the node between sessions? What doesn't?
4. Why does every long-running command belong in `tmux`?
5. How do you copy a file *out* of a node? (Preview of Day 38.)

If you can answer all five without scrolling down — skip to Part 5.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m1-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 5">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What connection method does `capsule term` use by default?",
    "options": [
      "A direct TCP SSH connection that requires a public-facing port on the remote",
      "Telnet over the control plane",
      "The SshRTC data channel (SSH over WebRTC), which works without any public-facing ports",
      "A VNC desktop session"
    ],
    "answer": 2,
    "explain": "`capsule term` connects over the SshRTC data channel (SSH tunneled through a WebRTC peer connection) by default. Because NAT traversal is handled by WebRTC, the remote machine never needs a publicly reachable SSH port."
  },
  {
    "stem": "Which connection command uses a direct SSH connection by default (and therefore needs a firewall-exposed port)?",
    "options": [
      "capsule term",
      "capsule ssh",
      "capsule exec",
      "capsule stream"
    ],
    "answer": 1,
    "explain": "`capsule ssh` uses a traditional direct TCP SSH connection by default, which requires a reachable/open SSH port on the remote. For the SshRTC data channel (no public port needed), use `capsule term` instead."
  },
  {
    "stem": "What does adding the `--direct` flag to a connection command do?",
    "options": [
      "It tears down stale WebRTC and SSH state before connecting",
      "It opens a remote VS Code window",
      "It records the session for auditing",
      "It bypasses the SshRTC/WebRTC overlay and forces a traditional TCP SSH connection (which needs a reachable port)"
    ],
    "answer": 3,
    "explain": "`--direct` skips the SshRTC/WebRTC data channel and forces plain TCP SSH. It's faster and easier to debug (and needed for clean port-forwarding), but the remote must have a reachable SSH port. It's the standard fallback when WebRTC negotiation fails."
  },
  {
    "stem": "How do you run a single one-off command on a remote machine without opening an interactive shell?",
    "options": [
      "capsule exec <config-tag> \"nvidia-smi\"",
      "capsule term <config-tag>",
      "capsule code <config-tag>",
      "capsule stream <config-tag>"
    ],
    "answer": 0,
    "explain": "`capsule exec <config-tag> \"<command>\"` runs one command on the remote and exits — ideal for scripted checks like `capsule exec gpu-server \"nvidia-smi\"`. `capsule term` opens a full interactive shell instead."
  },
  {
    "stem": "Which two commands open a remote IDE attached to the machine over Remote-SSH?",
    "options": [
      "capsule term and capsule ssh",
      "capsule exec and capsule stream",
      "capsule code (VS Code) and capsule cursor (Cursor)",
      "capsule session and capsule env"
    ],
    "answer": 2,
    "explain": "`capsule code` opens VS Code and `capsule cursor` opens Cursor, each with Remote-SSH attached to the machine. Both default to the SshRTC data channel; add `--direct` if you need repository (`--repo`) functionality."
  },
  {
    "stem": "What does `capsule stream` do, and what is its platform limitation?",
    "options": [
      "It streams log output; available on Linux only",
      "It opens a hardware-encoded WebRTC desktop (or single-app) pixel stream, and is available only on Windows and Mac",
      "It uploads files to the remote; available on all platforms",
      "It runs a benchmark and streams the results; NVIDIA machines only"
    ],
    "answer": 1,
    "explain": "`capsule stream` opens a hardware-encoded WebRTC pixel stream of the remote desktop (or a single app), for GUI work like ComfyUI or Blender. Per the usage guide it is available only on Windows and Mac and requires a machine that can pixel stream."
  },
  {
    "stem": "How do you close every active SshRTC data channel tunnel at once (e.g. to reset connection state when SshRTC is misbehaving)?",
    "options": [
      "capsule cleanup --all",
      "capsule term --end",
      "capsule exit",
      "capsule session endall"
    ],
    "answer": 3,
    "explain": "`capsule session endall` ends every active SshRTC tunnel at once. (`capsule session end` closes just one by unique id, port, or session id.) Running `session endall` and retrying is the first recommended step when SshRTC connections stall."
  },
  {
    "stem": "On a Capsule machine, which storage persists across sessions and which does not?",
    "options": [
      "/tmp persists; your $HOME directory is wiped each session",
      "Files in your $HOME directory persist; files written to /tmp do not survive a reconnect",
      "Neither persists — every session starts empty",
      "Both persist permanently, so cleanup is never needed"
    ],
    "answer": 1,
    "explain": "Files in your $HOME survive a reconnect (or container restart), while /tmp is ephemeral and disappears. If you write benchmark output to /tmp it will be gone after cleanup — use $HOME (or the OneDrive mount) for anything you want to keep."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: The Connect Command

### Reading — The connect command

```
capsule term <config-tag>                         # opens an interactive shell (SshRTC)
capsule exec <config-tag> "nvidia-smi"            # one-off command, then exit
capsule ssh <config-tag> --options "-L 8080:localhost:8080"   # direct SSH + port-forward
```

Internally: the CLI asks the control plane to broker; control plane verifies your lease; node agent opens a session bound to your identity. No SSH keys exchanged, no `known_hosts` to manage.

### Reading — Why not raw SSH?

| Raw SSH | `capsule term` |
|---|---|
| Manage keys per user per node | Keys auto-generated and managed by Capsule |
| Public SSH port must be reachable | SshRTC data channel — no public-facing port needed |
| Per-host port forwards by hand | `capsule ssh --options "-L …"` for clean forwarding |
| Per-host `known_hosts` churn | None |
| Multi-user etiquette: ad-hoc | Per-lease boundaries |

### Exercise: Command Anatomy

Look at `capsule exec <config-tag> "nvidia-smi"`:

1. What does `capsule exec` do vs a bare `capsule term`?
2. What's the exit code when the command finishes?
3. Write the command to check GPU memory on machine `nv-h100-04-1` without opening an interactive shell.

---

## Part 3 — Core Concepts: Session State & What Persists

### Reading — What persists across reconnects

| Persists across reconnects | Lost on disconnect |
|---|---|
| Files in your `$HOME` | Foreground processes |
| Files in the OneDrive mount (Day 38) | Shell history per-pane (unless saved) |
| `tmux` sessions | Untracked shell jobs |
| Installed packages (within your home dir / conda env) | Background jobs not in tmux/nohup |
| Container images cached on node | Running containers (unless detached) |

**Rule:** anything you don't want to lose to a network blip goes in **`tmux`**.

### Exercise: Persistence Quiz

For each item, answer "persists" or "lost on disconnect":

1. A 4-hour benchmark running in a foreground shell
2. A conda environment you installed in `~/miniconda3`
3. A file you saved to `/tmp/results.json`
4. A tmux session named `bench` running `watch nvidia-smi`
5. A Docker container you started with `docker run --rm`

---

## Part 4 — Deep Dive: tmux for Reliable Sessions

### Reading — tmux quick survival

```
tmux new -s work          # start a named session
tmux ls                   # list sessions
tmux attach -t work       # attach to it (after reconnect)
# inside tmux:
#   Ctrl-b d                # detach (session keeps running)
#   Ctrl-b c                # new window
#   Ctrl-b "                # split horizontally
#   Ctrl-b %                # split vertically
#   Ctrl-b [                # scrollback (q to exit)
```

Every Capsule shell session: **first command is `tmux a || tmux new -s work`**.

### Reading — The daily session pattern

```
capsule term nv-h100-04-1
$ tmux a || tmux new -s work     ← first command, always
$ nvidia-smi                     ← verify GPU visible
$ cd ~/myproject && ./run.sh     ← start work
# Ctrl-b d                       ← detach when done or if network flakes
```

The benchmark job keeps running. You can disconnect, commute, sleep — reconnect later and it's still there.

### Exercise: tmux Sequence

Without looking at reference material:

1. Write the full sequence to: connect → start tmux → run `sleep 3600` → detach → disconnect → reconnect → reattach and verify `sleep` is still running.
2. What key combination creates a new window inside tmux?
3. You have 3 windows open. How do you navigate between them?

---

## Part 5 — Hands-On: Connect, Detach, Reconnect

### Exercise: The Full Detach Test

**Goal:** lose zero work to a simulated network blip.

1. Connect to your dev node.
2. Start a tmux session named `work`. Inside it, start: `while true; do echo $(date); sleep 5; done`
3. Detach from tmux (`Ctrl-b d`). Exit the shell (`exit`). You are now fully disconnected.
4. Reconnect with `capsule term <same-node>`. Run `tmux a`. Verify your date-printing loop is still running.
5. Start a *second* window in the same tmux session (`Ctrl-b c`). Verify both windows are visible with `tmux ls` showing 1 session, 2 windows.
6. Stop the loop (`Ctrl-c`). Note the behaviour. Clean up.

**Success criterion:** you completed steps 1–4 without any work loss — the loop was still running when you reattached.

---

## Part 6 — Hands-On: Tunneling & Multi-User Etiquette

### Reading — Tunneling for local UIs

If you launch a vLLM server on the node listening on `:8000`:

```
capsule ssh <config-tag> --options "-L 8000:localhost:8000"
# then in another local terminal:
curl localhost:8000/v1/models
```

Same pattern for Jupyter, Grafana, any HTTP UI. The tunnel terminates when you disconnect.

### Reading — Multi-user etiquette

Even on a leased node, you're sharing with the platform:

- Don't `sudo` install system packages unless your lease says you may.
- Use user-space Python (conda, venv) for project deps.
- Clean up large temp files in `/tmp` before releasing.
- Leave the node "no worse than you found it."

### Reading — Connection failure modes

| Symptom | Fix |
|---|---|
| `capsule term` hangs | Corporate proxy; set `HTTPS_PROXY` and `WSS_PROXY` |
| `permission denied` after lease | Lease expired between list & connect; re-lease |
| `unhealthy node` mid-session | Network or agent crash; reconnect after agent recovers, your tmux survives if it had been running |
| Tunnel refuses port | Port already in use on local or remote; pick another |

### Exercise: Tunnel Drill

1. Start `python -m http.server 8001` on the node (in a tmux window).
2. In a *separate* local terminal, run `capsule ssh <config-tag> --options "-L 8001:localhost:8001"`.
3. From your laptop: `curl http://localhost:8001/` — you should see a directory listing.
4. Disconnect the tunnel shell. Verify the tunnel drops (curl fails).
5. Write your personal "connect checklist" — what do you do every time you connect? (3–5 steps.)

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 38 · Connecting to Machines">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Why should you always start tmux before running any long job on a Capsule node?",
    "options": [
      "tmux provides GPU monitoring built-in",
      "If your connection drops, tmux keeps the session running on the server — you can reconnect and reattach without losing work",
      "tmux is required by Capsule for logging purposes",
      "tmux enables multiple users to share the same GPU"
    ],
    "answer": 1,
    "explain": "Network connections can drop — VPN timeout, laptop sleep, ISP hiccup. Without tmux, a dropped connection kills your running process. With tmux, the session lives on the server. You reconnect with `capsule term` and reattach with `tmux attach`. Your benchmark keeps running."
  },
  {
    "stem": "What is the correct tmux sequence to detach from a session without stopping it?",
    "options": [
      "Ctrl+C then exit",
      "Ctrl+B then D (detach)",
      "Ctrl+Z then bg",
      "Close the terminal window"
    ],
    "answer": 1,
    "explain": "tmux prefix is Ctrl+B. Ctrl+B then D detaches from the session — the session keeps running on the server. To reattach: `tmux attach` or `tmux attach -t <session_name>`. Ctrl+C would send interrupt to the running process; Ctrl+Z suspends it; closing the terminal would kill a non-tmux session."
  },
  {
    "stem": "What is the command to open a port tunnel from a node to your local machine?",
    "options": [
      "`capsule ssh <config-tag> --options \"-L <local_port>:localhost:<remote_port>\"`",
      "`capsule connect <node> --tunnel <remote_port>:<local_host>:<local_port>`",
      "`capsule port-forward <node> <port>`",
      "`capsule tunnel open --from <node>:<port> --to localhost:<port>`"
    ],
    "answer": 0,
    "explain": "Port-forwarding rides on a direct SSH connection: `capsule ssh <config-tag> --options \"-L <local_port>:localhost:<remote_port>\"`. Example: `--options \"-L 8080:localhost:8080\"` makes the node's port 8080 reachable at your local port 8080 — used for Jupyter notebooks, web UIs, and API servers on the GPU node. There is no `capsule port-forward`, `capsule tunnel`, or `--tunnel` flag."
  },
  {
    "stem": "What are the four connection failure modes and their first diagnostic step?",
    "options": [
      "Hardware failure, software crash, network outage, auth expiry — restart the machine for all four",
      "Auth errors (re-run `capsule auth login`), wrong env/customer (check `capsule env show` and `capsule config customer show`), SshRTC won't connect (run `capsule session endall`, then retry), still failing (fall back to `--direct` and capture logs)",
      "GPU driver error, CUDA version mismatch, memory error, thermal throttling — reboot for all four",
      "DNS failure, TLS error, firewall block, rate limit — contact support for all four"
    ],
    "answer": 1,
    "explain": "The four connection failure modes: (1) Auth errors → re-run `capsule auth login` to refresh the token; (2) Wrong environment/customer → `capsule env show` and `capsule config customer show`; (3) SshRTC won't connect → `capsule session endall` to reset tunnel state, then retry; (4) Still failing → fall back to `--direct` and capture logs. Check in this order."
  },
  {
    "stem": "After a successful connection, what is the first thing you should verify on the node?",
    "options": [
      "Check disk space with `df -h`",
      "Verify your identity with `whoami` and check GPU availability with `nvidia-smi`",
      "Run a benchmark to confirm performance",
      "Install the latest system updates"
    ],
    "answer": 1,
    "explain": "After connecting: (1) `whoami` confirms you're running as the right user; (2) `nvidia-smi` confirms GPU access, shows GPU count and memory availability. Both together verify the connection is healthy and the hardware is as expected. Do this in < 30 seconds before starting any real work."
  }
]
</script>
</div>

### Connect forward

Tomorrow: **files, storage** — getting code in, getting results out, the auto-mounted OneDrive folder, when to use what.

### Pre-read for tomorrow (Day 38 · Files & Storage)

- **Resource:** <a href="../../../readings/capsule/#day-39-files-storage-streaming">Capsule Power-User Pre-Lecture Reading — Day 39 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-6-files-storage-and-the-onedrive-mount">Capsule Lab Guide</a> Modules 6 + 7.
- **Reflection questions:**
  1. How do you copy a small file to / from a node? A 50 GB model checkpoint?
  2. What's the difference between the per-user home dir and the auto-mounted OneDrive folder?
  3. Why is streaming output from the node back to your laptop the default for benchmarks?

---

## Stuck?

Ask **oxtutor** — describe the exact symptom (what command you ran, what output you got) and it will walk you through the failure-modes table.
