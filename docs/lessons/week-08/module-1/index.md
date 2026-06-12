---
drift: |
  Originally Day 38 of the former Capsule wk8. Now Day 37 of the new Ops week
  (week-08/module-1), unchanged in scope. Source-material link paths bumped one level deeper.
---

# Day 37 · Connecting to Machines

> **Concept of the day:** `capsule connect <node>` opens a brokered shell — identity-aware, audited, no key management. Session state lives in your home dir on the node and persists across reconnects. **Detach early, detach often** with `tmux` / `screen` — don't lose work to network blips.
> **Pre-reading:** Lab Guide **Module 5** (~15 min).
> **Source:** [Lab Guide Module 5](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md).

---

## Why this matters

This is the moment you're actually *on* a GPU machine. Everything else — env, lease, install — was setup. Get the connection workflow right and you save hours per week; get it wrong and you'll lose 4-hour benchmark runs to network hiccups.

## Readiness check

1. What command connects you to a leased node?
2. How does `capsule connect` differ from raw `ssh`?
3. What persists on the node between sessions? What doesn't?
4. Why does every long-running command belong in `tmux`?
5. How do you copy a file *out* of a node? (Preview of Day 39.)

## Core concept

### The connect command

```
capsule connect <node-id>           # opens an interactive shell
capsule connect <node-id> --command 'nvidia-smi'   # one-off command
capsule connect <node-id> --tunnel 8080:localhost:8080   # port-forward
```

Internally: the CLI asks the control plane to broker; control plane verifies your lease; node agent opens a session bound to your identity. No SSH keys exchanged, no `known_hosts` to manage.

### Why not raw SSH?

| Raw SSH | `capsule connect` |
|---|---|
| Manage keys per user per node | Identity from CLI auth, automatic |
| Per-host port forwards by hand | `--tunnel` flag with policy checks |
| No audit | Every session logged |
| Direct network exposure | Brokered through control plane |
| Per-host `known_hosts` churn | None |
| Multi-user etiquette: ad-hoc | Per-lease boundaries |

### Session state — what persists

| Persists across reconnects | Lost on disconnect |
|---|---|
| Files in your `$HOME` | Foreground processes |
| Files in shared storage (Day 39) | Shell history per-pane (unless saved) |
| `tmux` sessions | Untracked shell jobs |
| Installed packages (within your home dir / conda env) | Background jobs not in tmux/nohup |
| Container images cached on node | Running containers (unless detached) |

**Rule:** anything you don't want to lose to a network blip goes in **`tmux`**.

### tmux quick survival

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

### Tunneling for local UIs

If you launch a vLLM server on the node listening on `:8000`:

```
capsule connect <node> --tunnel 8000:localhost:8000
# then in another local terminal:
curl localhost:8000/v1/models
```

Same pattern for Jupyter, Grafana, any HTTP UI. The tunnel terminates when you disconnect.

### Multi-user etiquette

Even on a leased node, you're sharing with the platform:

- Don't `sudo` install system packages unless your lease says you may.
- Use user-space Python (conda, venv) for project deps.
- Clean up large temp files in `/tmp` before releasing.
- Leave the node "no worse than you found it."

### Connection failure modes

| Symptom | Fix |
|---|---|
| `connect` hangs | Corporate proxy; set `HTTPS_PROXY` and `WSS_PROXY` |
| `permission denied` after lease | Lease expired between list & connect; re-lease |
| `unhealthy node` mid-session | Network or agent crash; reconnect after agent recovers, your tmux survives if it had been running |
| Tunnel refuses port | Port already in use on local or remote; pick another |

## Practice (90 min)

1. (10 min) Connect to your dev node. Verify identity with `whoami` on the remote.
2. (20 min) Start a tmux session, run a long command (e.g. `find / 2>/dev/null | wc -l`), detach, disconnect, reconnect, reattach. Confirm output is still there.
3. (20 min) Start `python -m http.server 8001` on the node. Tunnel `8001:localhost:8001`. Hit it from your laptop. Disconnect — confirm tunnel drops.
4. (25 min) Pair: take turns walking the partner through a session start checklist: connect → tmux → workdir → first command.
5. (15 min) Write your personal "connect checklist" — pin it.

## Wrap-up

Cohort agrees: **first command after `capsule connect` is `tmux a || tmux new -s work`.** Cohort no longer loses work to network blips.

## Connect forward

Tomorrow: **files, storage, streaming** — getting code in, getting results out, the shared storage pool, when to use what.

---

## Pre-read for tomorrow (Day 39 · Files, Storage, Streaming)

- **Resource:** Lab Guide **Modules 6 + 7** (~30 min).
- **Reflection questions:**
  1. How do you copy a small file to / from a node? A 50 GB model checkpoint?
  2. What's the difference between per-user home dir and the shared storage pool?
  3. Why is streaming output from the node back to your laptop the default for benchmarks?
