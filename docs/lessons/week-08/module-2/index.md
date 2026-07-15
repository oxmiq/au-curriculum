---
drift: |
  Authored as a combined "Files + Storage + Streaming" day (former wk8 day 39). New graph
  splits this into two consecutive modules: week-08/module-2 (Files & Storage) and
  week-08/module-3 (Streaming). For now this lesson covers BOTH concepts in a single page;
  module-3 is a redirect stub pointing to the streaming section below. Future authoring
  should extract the streaming material into its own page.
---

# Day 37 · Files & Storage (with streaming primer)

> **Concept of the day:** **`capsule scp upload/download`** for one-off transfers to a specific machine. **The auto-mounted OneDrive (`~/OneDrive`)** for artifacts (models, datasets, results) you want available on every machine. **`capsule exec`** to run a one-off remote command and see its output without holding an interactive session. Per-user `$HOME` is node-local and `/tmp` is ephemeral; only `~/OneDrive` follows you across machines.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#files-storage-streaming">Capsule Power-User Pre-Lecture Reading - Files, Storage & Streaming</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-6-files-storage-and-the-onedrive-mount">Capsule Lab Guide</a> Modules 6 + 7.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 8 - Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <span>Day 37 · Files & Storage</span>
    {status:week-08/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Three Transfer Mechanisms |
| Part 3 | Core Concepts: Storage Scopes |
| Part 4 | Deep Dive: OneDrive & Daily Workflow |
| Part 5 | Hands-On: Upload / Download Drill |
| Part 6 | Hands-On: Remote Execution & Daily Rhythm |
| Part 7 | Wrap-up & Connection |

**Total: ~140 min**

---

## Part 1 - Pre-Reading Review

### Reading - Why this matters

This is the most-used set of operations in daily life on Capsule. Pick the wrong tool, `scp` a 50 GB checkpoint onto one machine when you actually want it on every machine via OneDrive, or scrape logs after the fact instead of watching a command's output as it runs, and you waste hours. Pick right and you have an enjoyable benchmarking rhythm.

### Exercise: Self-Check

Answer before reading on:

1. Which tool for a one-off copy of a 50 MB Python script to one machine: `capsule scp upload` or the `~/OneDrive` mount?
2. Which tool for a 50 GB model checkpoint you'll use on several machines this week?
3. What's the difference between per-user `$HOME` on a machine and the `~/OneDrive` mount?
4. Why watch benchmark output live (via `capsule exec`) instead of `tail -f`-ing a log after you've disconnected?
5. What command runs a one-off remote command and returns its stdout to your laptop?

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m2-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Modules 6-7">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "You want to do a one-off transfer of a dataset from your laptop to a specific remote machine. Which command is correct?", "options": ["capsule scp upload <tag> ./data/ /workspace/data/", "capsule cp ./data/ <tag>:/workspace/data/", "capsule storage put ./data/ /shared/data/", "capsule run --stream -- cp ./data/ /workspace/data/"]},
  {"stem": "You want a file to be available on every machine you connect to, without re-copying it each time. What should you use?", "options": ["A shared storage pool at /shared/", "capsule storage put to a cluster-wide pool", "The auto-mounted OneDrive (~/OneDrive)", "capsule scp upload to each machine individually"]},
  {"stem": "What does `capsule stream` actually do?", "options": ["Streams a command's stdout/stderr back to your local terminal in real time", "Opens a hardware-encoded WebRTC stream of the remote desktop (or a single app with --app)", "Uploads files to storage in a continuous stream", "Streams benchmark logs to the Capsule dashboard"]},
  {"stem": "Which command runs a single command on a remote machine non-interactively and then exits?", "options": ["capsule run --stream -- <command>", "capsule stream <tag> -- <command>", "capsule cp <tag> <command>", "capsule exec <tag> \"<command>\""]},
  {"stem": "You want your .gitconfig and .vimrc copied to the remote home directory automatically each time you connect. What's the mechanism?", "options": ["File passthrough: capsule config files add .gitconfig ~/.gitconfig", "capsule scp upload for each dotfile on every connect", "Put them in the /shared/ pool so all nodes read them", "capsule storage put ~/.gitconfig /shared/dotfiles/"]},
  {"stem": "Before the OneDrive mount will appear on remote machines, what one-time step is required?", "options": ["Create a shared storage pool with capsule storage init", "Run capsule auth storage and complete the OneDrive consent flow", "Run capsule config files add for OneDrive", "Nothing: OneDrive is always mounted by default"]},
  {"stem": "You connect to a machine and find ~/OneDrive is empty. What's the recommended recovery?", "options": ["Run capsule storage get to re-download the pool", "Manually scp your files back onto the node", "Re-run capsule auth storage, then reconnect", "Switch to the /shared/ pool instead"]},
  {"stem": "In the storage-scope experiment, you write the same file to /tmp, ~/, and ~/OneDrive on machine A, then check machine B. Which file is visible from machine B?", "options": ["The file in ~/OneDrive", "The file in ~/ (home directory)", "The file in /tmp", "All three, since nodes share a filesystem"]}
]
</script>
</div>

---

## Part 2 - Core Concepts: Three Transfer Mechanisms

### Reading - File transfer commands

There are three orthogonal mechanisms; pick by *where the bytes need to end up*.

| Mechanism | Command | When |
|---|---|---|
| SCP | `capsule scp upload <config-tag> ./local.py /workspace/remote.py` | One-off push of a file/dir to a specific machine |
| SCP | `capsule scp download <config-tag> /workspace/results.json ./` | Pull a single artifact off a specific machine |
| SCP | `capsule scp upload -u <unique-id> ./mydir /workspace/` | Same, but target a specific box by unique ID |
| OneDrive mount | `cp ./big.bin ~/OneDrive/models/` *(run inside a session)* | Stage large artifacts you want on **every** machine |
| OneDrive mount | `ls ~/OneDrive/models/` *(run inside a session)* | Browse your cross-machine OneDrive folder |
| File passthrough | `capsule config files add .gitconfig ~/.gitconfig` | Auto-copy a small dotfile to the remote home on every connect |

The OneDrive mount requires a one-time `capsule auth storage` (the OneDrive consent flow); after that your `OxCapsule` folder auto-mounts at `~/OneDrive` on every `term`/`code`/`cursor`/`claude`/`stream` session. Manage passthrough with `capsule config files list` / `capsule config files remove`.

### Exercise: Choose the Right Tool

For each scenario, write the correct command (or mechanism):

1. Copy your `benchmark.yaml` (2 KB) from your laptop to machine `nv-h100-04-1`.
2. Make a 70B model checkpoint (140 GB) available on every machine you connect to.
3. Pull the `report.json` that a benchmark left on machine `nv-h100-04-1` onto your laptop.
4. List everything in your cross-machine OneDrive `models/` folder.

---

## Part 3 - Core Concepts: Storage Scopes

### Reading - Three storage scopes: `/tmp`, `$HOME`, `~/OneDrive`

| Property | `/tmp` on machine | `$HOME` on machine | `~/OneDrive` mount |
|---|---|---|---|
| Speed | Local, fast | Local NVMe, fastest | Networked, slower (cloud-synced) |
| Lifetime | Ephemeral - gone on restart/cleanup | Survives restart, but node-local | Durable, cloud-backed |
| Visibility | This machine only | This machine only | Every machine you connect to |
| Use for | Throwaway scratch | Source code, venvs, per-machine scratch | Models, datasets, results: anything you want across machines or want to keep |

> **Rule:** if losing it on a restart would hurt, or you need it on more than one machine, put it in `~/OneDrive`.

### Reading - Why the OneDrive mount matters

A 70B FP16 model = 140 GB. Re-uploading that to each machine with `scp` every time you switch boxes? **Take a break, see you in 3 hours.** Stage it into `~/OneDrive` once and it's already there, under the same path, on every machine you connect to.

The Week 9 benchmark workflow:

1. Models live in `~/OneDrive/models/` (staged once).
2. Each benchmark run writes its report to `~/OneDrive/runs/<date>-<label>/`.
3. Your laptop never re-moves model bytes: only run reports, and only when you want a local copy.

### Exercise: Lifetime Reasoning

For each artifact, decide: `/tmp`, `$HOME`, or `~/OneDrive`? Justify in one sentence.

1. A Python venv you'll reuse tomorrow on the *same* machine.
2. A 70B model checkpoint you'll use across multiple machines this week.
3. A `run.sh` script you're actively editing.
4. The `report.json` output of today's benchmark (you want it next week, from any machine).
5. A `scratch.bin` you need only for the next 5 minutes.

---

## Part 4 - Deep Dive: OneDrive & Daily Workflow

### Reading - See output live with `capsule exec`

```
capsule exec <config-tag> "./run_benchmark.sh"
```

`capsule exec` runs a single command on the remote machine, returns its output to your terminal, then exits. Contrast the wrong way:

```
capsule term <config-tag>
nohup ./run_benchmark.sh > /tmp/out.log 2>&1 &
exit
# 4 hours later...
capsule term <config-tag>
tail -f /tmp/out.log   # too late to react
```

With `capsule exec`, you see the command's output as it comes back and can Ctrl-C to abort if you spot an obvious failure 30 seconds in. Don't waste GPU-hours on a typo'd config.

> **Note:** `capsule exec` is *not* the same as `capsule stream`. `capsule stream` opens a hardware-encoded WebRTC pixel stream of the remote *desktop* (or a single GUI app with `--app`) on Windows and Mac; that's Day 38's topic. For running a command and watching its stdout, you want `capsule exec`.

### Reading - The full daily file workflow

```
# Once, stage the model into OneDrive (inside any session):
capsule term <config-tag>
cp llama-3-70b-fp8.tar ~/OneDrive/models/
exit

# Each benchmark session, from your laptop:
capsule scp upload <config-tag> ./benchmark.yaml /workspace/benchmark.yaml
capsule exec <config-tag> "./run.sh /workspace/benchmark.yaml ~/OneDrive/runs/$(date +%F)/"
capsule scp download <config-tag> ~/OneDrive/runs/$(date +%F)/report.json ./
```

That's the rhythm. Memorize it.

### Reading - Etiquette & hygiene

- Clean up your old `~/OneDrive/runs/<old>` directories monthly; OneDrive quota is finite.
- Keep `~/OneDrive/models/` tidy; don't stage checkpoints you won't reuse.
- `~/OneDrive` is cloud-synced and slower than local disk; don't do heavy random I/O against it; copy to `$HOME` first if a job needs fast repeated reads.
- Remember `/tmp` and `$HOME` are node-local: anything you want to keep, or want on another machine, must land in `~/OneDrive`.

### Exercise: Workflow Gap-Fill

The following daily workflow has 3 mistakes. Find them:

```
capsule scp upload <config-tag> llama-70b.bin /workspace/       # (1)
capsule term <config-tag>                                       # (2)
nohup ./run.sh > /tmp/out.log 2>&1 & ; exit                     #     ...then disconnect
capsule scp download <config-tag> /tmp/report.json ./           # (3)
```

For each mistake: what's wrong, and what's the correct approach?

---

## Part 5 - Hands-On: Upload / Download Drill

### Exercise: File Round-Trip

1. Create a small test file on your laptop: `echo "hello capsule" > test.txt`
2. Upload it to your dev machine: `capsule scp upload <config-tag> ./test.txt /workspace/test.txt`
3. Verify it exists non-interactively: `capsule exec <config-tag> "cat /workspace/test.txt"`.
4. Modify it on the machine: `capsule exec <config-tag> "echo modified >> /workspace/test.txt"`.
5. Pull it back: `capsule scp download <config-tag> /workspace/test.txt ./test-returned.txt`.
6. Inside a session (`capsule term <config-tag>`), run `ls ~/OneDrive`. Note what's already there. Read a `README` if present.

---

## Part 6 - Hands-On: Remote Execution & Daily Rhythm

### Exercise: Running a Long Command Remotely

1. Run a long command with `capsule exec` (use a harmless 30-second sleep + echo loop):
   ```
   capsule exec <config-tag> "bash -c 'for i in \$(seq 1 6); do echo step \$i; sleep 5; done'"
   ```

2. Observe: you see output as it comes back.
3. After step 3 appears, press Ctrl-C. Verify the command aborts.
4. Now design your Week 9 benchmark artifact layout. Fill in:
   ```
   Model staged at:         ~/OneDrive/models/___________
   Each run goes to:        ~/OneDrive/runs/___________
   Config file stays in:    ~/___________
   Report available at:     ~/OneDrive/___________
   ```

---

## Part 7 - Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 39 · Files &amp; Storage">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What is the difference between `capsule scp upload` and the `~/OneDrive` mount?", "options": ["They are identical; both copy files", "`capsule scp upload` does a one-off transfer to a specific machine's local disk; `~/OneDrive` is a cloud-synced folder that auto-mounts at the same path on every machine you connect to", "`capsule scp upload` is for large files; `~/OneDrive` is only for small files", "Both push to a cluster-wide `/shared/` pool via `capsule storage put`"]},
  {"stem": "What is the recommended artifact layout for benchmark runs?", "options": ["Store everything in `/tmp` for fast access", "Stage models in `~/OneDrive/models/`, write run outputs to `~/OneDrive/runs/<date-label>/`, keep config in `$HOME`, and pull results to your laptop", "Store all artifacts in a machine's home directory for simplicity", "Push everything to a `/shared/` pool with `capsule storage put`"]},
  {"stem": "You want to run a benchmark command on a remote machine and watch its stdout come back to your terminal. Which command do you use?", "options": ["`capsule run --stream -- <command>`", "`capsule exec <config-tag> \"<command>\"`", "`capsule stream <config-tag>`", "`capsule storage get <command>`"]},
  {"stem": "What is the hygiene rule for your `~/OneDrive/models/` folder?", "options": ["Store all your working files there for fast access from any machine", "Keep only checkpoints you'll actually reuse and clean up old artifacts; OneDrive quota is finite and the mount is slower than local disk", "Never read from OneDrive; always copy everything to a `/shared/` pool first", "Prefix every file with your username to avoid conflicts in the shared pool"]},
  {"stem": "When should you stage model weights into `~/OneDrive` instead of `capsule scp upload`-ing them to a machine?", "options": ["Always: `~/OneDrive` is faster for all file sizes", "When you'll use the weights from multiple machines or need them to survive a restart: `~/OneDrive` follows you across machines, whereas an `scp`'d copy lives only on that one machine's local disk", "When the model is larger than 1 GB", "When you need the model on your laptop, not on a machine"]},
  {"stem": "A benchmark left `report.json` at `/workspace/report.json` on `nv-h100-04-1`. Which command pulls it onto your laptop?", "options": ["capsule scp download nv-h100-04-1 /workspace/report.json ./", "capsule scp upload nv-h100-04-1 ./report.json /workspace/", "capsule storage get /workspace/report.json ./", "capsule cp nv-h100-04-1:/workspace/report.json ./"]},
  {"stem": "OneDrive isn't mounting at `~/OneDrive` on your sessions yet. What one-time step enables it?", "options": ["Create a /shared/ pool with `capsule storage init`", "Run `capsule auth storage` and complete the OneDrive consent flow; after that your OxCapsule folder auto-mounts at ~/OneDrive on every term/code/cursor/stream session", "Add it with `capsule config files add OneDrive`", "Nothing: reboot the node and it appears"]},
  {"stem": "You want your `.gitconfig` copied into the remote home directory automatically every time you connect. Which mechanism does the lesson use?", "options": ["`capsule scp upload` it by hand on every connect", "Put it in a cluster-wide /shared/ pool", "File passthrough: `capsule config files add .gitconfig ~/.gitconfig`; the mapping lives in config-files.json and is copied to the remote home on connect", "`capsule storage put ~/.gitconfig /shared/dotfiles/`"]},
  {"stem": "A teammate claims `capsule stream` streams a command's stdout back to your terminal. How should you correct them?", "options": ["They're right; it's just `capsule exec` running continuously", "`capsule stream` opens a hardware-encoded WebRTC pixel stream of the remote desktop (or one app with `--app`) on Windows/Mac; for a command's stdout you want `capsule exec`", "They're right; but it only works for benchmark logs", "`capsule stream` uploads files in a continuous stream to OneDrive"]}
]
</script>
</div>

### Connect forward

Tomorrow (Day 38): **streaming** - the full `capsule stream` workflow for GPU-accelerated desktop output. Day 39 (Friday): reliability & diagnostics.

---

### Looking ahead to next week

**Thursday (Day 39)** is module-4 and is **not** a pre-read day; Friday (Day 40) is consolidation.

**Monday (Day 41):** Next week's first lesson has a pre-read; see [Week 9 Day 1](../../../readings/capsule/).

---

## Stuck?

Ask **oxtutor**; share which command you ran, what error you got, and which storage scope (home vs shared) you were targeting.
