---
drift: |
  Originally Day 38 of the former Capsule wk8. Now Day 37 of the new Ops week
  (week-08/module-1), unchanged in scope. Source-material link paths bumped one level deeper.
---

# Day 37 · Connecting to Machines

> **Concept of the day:** `capsule connect <node>` opens a brokered shell — identity-aware, audited, no key management. Session state lives in your home dir on the node and persists across reconnects. **Detach early, detach often** with `tmux` / `screen` — don't lose work to network blips.<br>
> **Pre-reading:** Lab Guide **Module 5** (~15 min).

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

- [ ] I can run `capsule connect` and verify my identity on the node in < 30 sec
- [ ] I always start tmux before running anything I don't want to lose
- [ ] I can detach, disconnect, reconnect, and reattach without losing a running job
- [ ] I know which port-tunnel command to use for local UIs
- [ ] I know the four connection failure modes and their fixes

### Connect forward

Tomorrow: **files, storage** — getting code in, getting results out, the shared storage pool, when to use what.

### Pre-read for tomorrow (Day 38 · Files & Storage)

- **Resource:** Lab Guide **Modules 6 + 7** (~30 min).
- **Reflection questions:**
  1. How do you copy a small file to / from a node? A 50 GB model checkpoint?
  2. What's the difference between per-user home dir and the shared storage pool?
  3. Why is streaming output from the node back to your laptop the default for benchmarks?

---

## Stuck?

Ask **oxtutor** — describe the exact symptom (what command you ran, what output you got) and it will walk you through the failure-modes table.
