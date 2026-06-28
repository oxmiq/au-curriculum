---
drift: |
  Originally Day 38 of the former Capsule wk8. Now Day 37 of the new Ops week
  (week-08/module-1), unchanged in scope. Source-material link paths bumped one level deeper.
---

# Day 37 · Connecting to Machines

> **Concept of the day:** `capsule connect <node>` opens a brokered shell — identity-aware, audited, no key management. Session state lives in your home dir on the node and persists across reconnects. **Detach early, detach often** with `tmux` / `screen` — don't lose work to network blips.<br>
> **Pre-reading:** <a href="../../../readings/capsule/">Capsule Power-User Pre-Lecture Reading — Day 38 section</a> (~25 min). Supplement: <a href="../../../readings/capsule/lab-guide/">Capsule Lab Guide</a> Module 5.

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
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-08/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: The Connect Command | 20 min |
| Part 3 | Core Concepts: Session State & What Persists | 20 min |
| Part 4 | Deep Dive: tmux for Reliable Sessions | 20 min |
| Part 5 | Hands-On: Connect, Detach, Reconnect | 30 min |
| Part 6 | Hands-On: Tunneling & Multi-User Etiquette | 25 min |
| Part 7 | Wrap-up & Connection | 10 min |

**Total: ~140 min** (leaves buffer for reading the Lab Guide pre-read)

---

## Part 1 — Pre-Reading Review · 15 min

### Reading — Why this matters

This is the moment you're actually *on* a GPU machine. Everything else — env, lease, install — was setup. Get the connection workflow right and you save hours per week; get it wrong and you'll lose 4-hour benchmark runs to network hiccups.

### Exercise: Self-Check

Before reading on, answer from memory:

1. What command connects you to a leased node?
2. How does `capsule connect` differ from raw `ssh`?
3. What persists on the node between sessions? What doesn't?
4. Why does every long-running command belong in `tmux`?
5. How do you copy a file *out* of a node? (Preview of Day 38.)

If you can answer all five without scrolling down — skip to Part 5.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m1-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 5">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What command connects you to a leased node in Capsule?",
    "options": [
      "ssh <node>",
      "capsule connect <node>",
      "capsule login <node>",
      "telnet <node>"
    ],
    "answer": 1,
    "explain": "'capsule connect <node>' opens a brokered shell to the leased node. It's identity-aware and audited, meaning your identity is tracked and all sessions are logged for security."
  },
  {
    "stem": "How does `capsule connect` differ from raw `ssh`?",
    "options": [
      "It is the same as ssh",
      "It's identity-aware and audited; no key management required; handles authentication automatically",
      "It's slower than ssh",
      "It requires root access"
    ],
    "answer": 1,
    "explain": "Unlike raw ssh, capsule connect is: (1) identity-aware — your identity is tracked, (2) audited — all sessions are logged, (3) no key management — handles auth automatically. You don't need to manage SSH keys."
  },
  {
    "stem": "What persists on the node between sessions?",
    "options": [
      "Only /tmp",
      "Your home directory (~) persists; /tmp and environment variables do not",
      "Everything",
      "Nothing"
    ],
    "answer": 1,
    "explain": "Your home directory (~) persists on the node between sessions. However, /tmp and environment variables do not persist — they're reset on each connection. This is important for setting up your environment each time."
  },
  {
    "stem": "Why should every long-running command belong in `tmux`?",
    "options": [
      "Because tmux is required by Capsule",
      "Because tmux sessions persist even when your connection drops, protecting your work from network blips",
      "Because tmux is faster",
      "Because tmux is more secure"
    ],
    "answer": 1,
    "explain": "tmux (or screen) sessions persist even when your connection drops. This protects your 4-hour benchmark runs from network hiccups. If your laptop disconnects, tmux keeps running on the node and you can reattach later."
  },
  {
    "stem": "What does 'detach early, detach often' mean in the context of Capsule connections?",
    "options": [
      "You should disconnect frequently to save bandwidth",
      "You should use tmux and detach frequently so your work survives connection drops",
      "You should disconnect when not using the machine",
      "You should use screen instead of tmux"
    ],
    "answer": 1,
    "explain": "'Detach early, detach often' means you should use tmux and detach frequently. This ensures your work persists even if your connection drops. Don't run commands directly in the shell — run them in tmux so you can safely disconnect."
  },
  {
    "stem": "What happens when you reconnect to a node after a network blip?",
    "options": [
      "You lose all your work",
      "If you used tmux, your session is still running; if not, your work is lost",
      "The node is released",
      "You need to re-authenticate"
    ],
    "answer": 1,
    "explain": "If you used tmux, your session is still running when you reconnect — you can reattach and continue. If you didn't use tmux and your connection dropped, any running commands are terminated and your work is lost."
  },
  {
    "stem": "What is 'brokered shell' in Capsule?",
    "options": [
      "A type of SSH tunnel",
      "A shell connection where Capsule brokers the connection, providing identity tracking and auditing",
      "A premium shell option",
      "A deprecated connection method"
    ],
    "answer": 1,
    "explain": "A brokered shell means Capsule brokers the connection — it provides identity tracking (who connected), auditing (all commands logged), and automatic authentication. Your CLI connects to the control plane which then connects you to the node."
  },
  {
    "stem": "How do you copy a file out of a node in Capsule?",
    "options": [
      "Using scp directly",
      "Using capsule cp or capsule file transfer commands",
      "Using email",
      "You cannot copy files out"
    ],
    "answer": 1,
    "explain": "You copy files out of a node using 'capsule cp' or similar file transfer commands provided by Capsule. This is different from raw scp — Capsule handles the authentication and provides an audited file transfer mechanism."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: The Connect Command · 20 min

### Reading — The connect command

```
capsule connect <node-id>           # opens an interactive shell
capsule connect <node-id> --command 'nvidia-smi'   # one-off command
capsule connect <node-id> --tunnel 8080:localhost:8080   # port-forward
```

Internally: the CLI asks the control plane to broker; control plane verifies your lease; node agent opens a session bound to your identity. No SSH keys exchanged, no `known_hosts` to manage.

### Reading — Why not raw SSH?

| Raw SSH | `capsule connect` |
|---|---|
| Manage keys per user per node | Identity from CLI auth, automatic |
| Per-host port forwards by hand | `--tunnel` flag with policy checks |
| No audit | Every session logged |
| Direct network exposure | Brokered through control plane |
| Per-host `known_hosts` churn | None |
| Multi-user etiquette: ad-hoc | Per-lease boundaries |

### Exercise: Command Anatomy

Look at `capsule connect <node-id> --command 'nvidia-smi'`:

1. What does `--command` do vs a bare `capsule connect`?
2. What's the exit code when the command finishes?
3. Write the command to check GPU memory on node `nv-h100-04-1` without opening an interactive shell.

---

## Part 3 — Core Concepts: Session State & What Persists · 20 min

### Reading — What persists across reconnects

| Persists across reconnects | Lost on disconnect |
|---|---|
| Files in your `$HOME` | Foreground processes |
| Files in shared storage (Day 38) | Shell history per-pane (unless saved) |
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

## Part 4 — Deep Dive: tmux for Reliable Sessions · 20 min

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
capsule connect nv-h100-04-1
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

## Part 5 — Hands-On: Connect, Detach, Reconnect · 30 min

### Exercise: The Full Detach Test

**Goal:** lose zero work to a simulated network blip.

1. (5 min) Connect to your dev node.
2. (5 min) Start a tmux session named `work`. Inside it, start: `while true; do echo $(date); sleep 5; done`
3. (5 min) Detach from tmux (`Ctrl-b d`). Exit the shell (`exit`). You are now fully disconnected.
4. (5 min) Reconnect with `capsule connect <same-node>`. Run `tmux a`. Verify your date-printing loop is still running.
5. (5 min) Start a *second* window in the same tmux session (`Ctrl-b c`). Verify both windows are visible with `tmux ls` showing 1 session, 2 windows.
6. (5 min) Stop the loop (`Ctrl-c`). Note the behaviour. Clean up.

**Success criterion:** you completed steps 1–4 without any work loss — the loop was still running when you reattached.

---

## Part 6 — Hands-On: Tunneling & Multi-User Etiquette · 25 min

### Reading — Tunneling for local UIs

If you launch a vLLM server on the node listening on `:8000`:

```
capsule connect <node> --tunnel 8000:localhost:8000
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
| `connect` hangs | Corporate proxy; set `HTTPS_PROXY` and `WSS_PROXY` |
| `permission denied` after lease | Lease expired between list & connect; re-lease |
| `unhealthy node` mid-session | Network or agent crash; reconnect after agent recovers, your tmux survives if it had been running |
| Tunnel refuses port | Port already in use on local or remote; pick another |

### Exercise: Tunnel Drill

1. Start `python -m http.server 8001` on the node (in a tmux window).
2. In a *separate* local terminal, run `capsule connect <node> --tunnel 8001:localhost:8001`.
3. From your laptop: `curl http://localhost:8001/` — you should see a directory listing.
4. Disconnect the tunnel shell. Verify the tunnel drops (curl fails).
5. Write your personal "connect checklist" — what do you do every time you connect? (3–5 steps.)

---

## Part 7 — Wrap-up & Connection · 10 min

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
    "explain": "Network connections can drop — VPN timeout, laptop sleep, ISP hiccup. Without tmux, a dropped connection kills your running process. With tmux, the session lives on the server. You reconnect with `capsule connect` and reattach with `tmux attach`. Your benchmark keeps running."
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
      "`capsule connect <node> --tunnel <remote_port>:<local_host>:<local_port>`",
      "`ssh -L <local_port>:localhost:<remote_port> <node>`",
      "`capsule port-forward <node> <port>`",
      "`capsule tunnel open --from <node>:<port> --to localhost:<port>`"
    ],
    "answer": 0,
    "explain": "The Capsule tunnel command: `capsule connect <node> --tunnel <remote_port>:localhost:<local_port>`. Example: `--tunnel 8080:localhost:8080` makes the node's port 8080 accessible at your local port 8080. This is used for Jupyter notebooks, web UIs, and API servers running on the GPU node."
  },
  {
    "stem": "What are the four connection failure modes and their first diagnostic step?",
    "options": [
      "Hardware failure, software crash, network outage, auth expiry — restart the machine for all four",
      "Auth errors (check `capsule whoami`), network timeout (check VPN/proxy), node unhealthy (check `capsule node show`), hung local state (run `capsule cleanup`)",
      "GPU driver error, CUDA version mismatch, memory error, thermal throttling — reboot for all four",
      "DNS failure, TLS error, firewall block, rate limit — contact support for all four"
    ],
    "answer": 1,
    "explain": "The four connection failure modes: (1) Auth errors → `capsule whoami` to verify token validity; (2) Network/proxy issues → check VPN, unset proxy vars; (3) Node unhealthy → `capsule node show <id>` to check status; (4) Hung local state → `capsule cleanup` then retry. Check in this order."
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

Tomorrow: **files, storage** — getting code in, getting results out, the shared storage pool, when to use what.

### Pre-read for tomorrow (Day 38 · Files & Storage)

- **Resource:** <a href="../../../readings/capsule/">Capsule Power-User Pre-Lecture Reading — Day 39 section</a> (~40 min). Supplement: <a href="../../../readings/capsule/lab-guide/">Capsule Lab Guide</a> Modules 6 + 7.
- **Reflection questions:**
  1. How do you copy a small file to / from a node? A 50 GB model checkpoint?
  2. What's the difference between per-user home dir and the shared storage pool?
  3. Why is streaming output from the node back to your laptop the default for benchmarks?

---

## Stuck?

Ask **oxtutor** — describe the exact symptom (what command you ran, what output you got) and it will walk you through the failure-modes table.
