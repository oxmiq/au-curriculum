# Day 40 · Known Quirks

> **Concept of the day:** every system has failure modes that look mysterious until you've seen them once. Today you learn Capsule's known-quirks list from the Lab Guide so you never waste 30 minutes on a problem that has a 10-second fix.<br> **Pre-reading:** <a href="../../../readings/capsule/">Capsule Power-User Pre-Lecture Reading — Day 40 section</a> (~15 min). Supplement: <a href="../../../readings/capsule/lab-guide/">Capsule Lab Guide</a> Module 10 — Known Quirks.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 8 — Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <span>Day 40 · Known Quirks</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-08/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: The Triage Decision Tree | 20 min |
| Part 3 | Deep Dive: The Known-Quirks Table | 30 min |
| Part 4 | Core Concepts: The Bug-Report Rubric | 20 min |
| Part 5 | Hands-On: Reproduce Three Quirks | 35 min |
| Part 6 | Hands-On: File a Proper Bug Report | 20 min |
| Part 7 | Wrap-up & Connection | 10 min |
| **Total** | | **~150 min + pre-reading** |

---

## Part 1 — Pre-Reading Review · 15min

### Reading —

Before continuing, you should have read **Lab Guide Module 10 (Known Quirks)**. It covers:

- The 4-step triage decision tree
- The known-quirks table (all 8 rows)
- The bug-report rubric (8 required fields)
- `capsule cleanup` — when and why

### Exercise:

Answer from memory:

1. What is the first command you run when any Capsule operation fails?
2. What is `capsule cleanup` and what state does it tear down?
3. Name four rows from the known-quirks table (symptom + fix).
4. How many fields does a proper bug report require? Name three of them.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m4-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 10">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the FIRST command to run in the triage decision tree when a Capsule operation fails?",
    "options": [
      "capsule cleanup",
      "capsule status",
      "capsule env show",
      "capsule auth login"
    ],
    "answer": 1,
    "explain": "Step 1 is always 'capsule status'. It tells you whether your auth is valid, your identity is correct, and your token hasn't expired — the most common root causes of failures."
  },
  {
    "stem": "What does `capsule cleanup` do?",
    "options": [
      "Deletes your remote home directory and all benchmark results",
      "Tears down stale WebRTC sessions and SSH state on the local client",
      "Removes all your leases and frees the nodes",
      "Resets your environment and customer config to defaults"
    ],
    "answer": 1,
    "explain": "'capsule cleanup' tears down stale WebRTC sessions and SSH state on the local client only. It does NOT affect running processes on the remote machine. It fixes ~40% of 'SshRTC won't connect' and 'session hung' issues."
  },
  {
    "stem": "You run 'capsule list' and it shows completely different machines than yesterday. Which triage step catches this?",
    "options": [
      "Step 1 — capsule status (auth issue)",
      "Step 2 — capsule env show / capsule config customer show (wrong env or customer)",
      "Step 3 — capsule cleanup (stale state)",
      "Step 4 — --direct flag (WebRTC path issue)"
    ],
    "answer": 1,
    "explain": "Step 2 catches this. Run 'capsule env show' and 'capsule config customer show'. One of them is wrong — you're looking at a different environment or customer context than you think."
  },
  {
    "stem": "SshRTC won't connect. After Step 1 (status) and Step 2 (env/customer) are clean, what is Step 3?",
    "options": [
      "Re-install Capsule",
      "capsule cleanup, then retry",
      "File a bug report immediately",
      "Use capsule stream instead"
    ],
    "answer": 1,
    "explain": "Step 3 is 'capsule cleanup', then retry. This tears down stale local WebRTC/SSH state and fixes ~40% of SshRTC connectivity issues. Only proceed to Step 4 if cleanup + retry still fails."
  },
  {
    "stem": "A bug report must contain exactly how many required fields?",
    "options": [
      "4",
      "6",
      "8",
      "10"
    ],
    "answer": 2,
    "explain": "A proper bug report has exactly 8 required fields: (1) capsule --version, (2) capsule env show, (3) capsule config customer show, (4) exact command, (5) exact error output, (6) timestamp, (7) machine unique ID, (8) what you already tried."
  },
  {
    "stem": "macOS Keychain prompts appear on every Capsule command. What is the fix?",
    "options": [
      "Uninstall and reinstall Capsule",
      "Run 'capsule cleanup'",
      "Click 'Always Allow' once in the Keychain dialog",
      "Use sudo for all Capsule commands"
    ],
    "answer": 2,
    "explain": "This is Known Quirk #5. Click 'Always Allow' once in the Keychain dialog. It will remember the permission and stop prompting for subsequent commands."
  },
  {
    "stem": "VS Code Remote-SSH errors appear after a Capsule session. What is the fix?",
    "options": [
      "Run 'capsule cleanup' to clear local state",
      "Remove 'capsule-<uniqueId>' blocks from ~/.ssh/config",
      "Reinstall the VS Code Remote-SSH extension",
      "Re-authenticate with 'capsule auth login'"
    ],
    "answer": 1,
    "explain": "This is Known Quirk #4. Old Capsule sessions leave stale 'capsule-<uniqueId>' blocks in ~/.ssh/config. Remove them manually. VS Code Remote-SSH picks up stale entries and fails."
  },
  {
    "stem": "You must file a bug report. Which triage steps must you have completed BEFORE filing?",
    "options": [
      "Only Step 1 (capsule status)",
      "Steps 1 and 2 only",
      "All four steps — status, env/customer, cleanup, then --direct + logs",
      "None — file immediately to get faster support"
    ],
    "answer": 2,
    "explain": "You must complete all 4 steps before filing. Step 4 specifically requires trying '--direct' to bypass WebRTC and collecting logs from ~/.capsule/logs/. Those logs are the most important data for the engineering team."
  },
  {
    "stem": "`gh release download` returns 401/403. What is the most likely cause?",
    "options": [
      "Your Capsule version is outdated",
      "Your GH_TOKEN is missing one or more of the 4 required scopes",
      "You need to re-run 'capsule auth login'",
      "The GitHub release was deleted"
    ],
    "answer": 1,
    "explain": "This is Known Quirk #8. The GH_TOKEN must have all four scopes: repo, read:org, workflow, user. Regenerate the token if you're unsure. 401/403 almost always means missing scopes, not an invalid token."
  },
  {
    "stem": "The 'specificity test' for a bug report asks:",
    "options": [
      "Is the report under 500 words?",
      "Did you try capsule cleanup first?",
      "Could a stranger who has never seen your machine reproduce the issue from your report alone?",
      "Does the report include your Capsule version?"
    ],
    "answer": 2,
    "explain": "The specificity test: read your bug report and ask whether a stranger with no context could reproduce the issue. If you'd need to answer follow-up questions, the report is incomplete. This is the quality bar for every field."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: The Triage Decision Tree · 20min

### Reading —

Before filing a bug or escalating to support, run through this 4-step decision tree. In order:

**Step 1: `capsule status`**

Check: is auth valid? Is identity correct? Is the token expiry in the future?

- If "unauthorized": re-run `capsule auth login`
- If "clock skew": sync NTP (`sudo sntp -sS time.apple.com`)
- If token shows expired: re-run `capsule auth login`

**Step 2: `capsule env show` + `capsule config customer show`**

Check: are you pointed at the right environment and customer?

- Wrong environment → `capsule config env set <correct-env>`
- Wrong customer → `capsule config customer set <correct-customer>`
- Both of these settings persist across sessions; getting them wrong once explains why "everything stopped working"

**Step 3: `capsule cleanup`**

Tears down stale WebRTC sessions and SSH state. Retry the failing operation.

- This fixes ~40% of "SshRTC won't connect" and "session hung" issues
- Does **not** affect your running processes on the remote machine — it only cleans local state

**Step 4: `--direct` flag + collect logs**

If Steps 1–3 don't fix it: retry the command with `--direct` to bypass WebRTC. If `--direct` succeeds, the issue is in the WebRTC/SshRTC path (a network or infrastructure issue). Collect logs from `~/.capsule/logs/` and escalate.

**The rule:** if you're going to file a bug, you must have tried all 4 steps first. Step 4's logs are the most important data for the engineering team.

### Exercise:

Walk through the decision tree for each scenario below. State which step catches the issue and what the fix is:

1. `capsule term <tag>` hangs. `capsule status` shows valid token. `capsule env show` shows the correct env.
2. `capsule list` shows 0 machines. `capsule status` shows valid token.
3. `capsule term <tag>` returns "connection refused" immediately (not hanging — fast failure).
4. Everything worked yesterday. Today `capsule status` says "unauthorized" with no code changes.

---

## Part 3 — Deep Dive: The Known-Quirks Table · 30min

### Reading —

These are all 8 known quirks from Lab Guide Module 10. Memorize every row — symptom and fix.

| # | Symptom | Fix |
|---|---|---|
| 1 | Auth fails in browser flow | CLI falls back to manual token: go to `https://oxmiq.ai/oxcapsule/auth` in a browser, copy the token, run `capsule auth login --token <paste>` |
| 2 | `capsule list` shows wrong machines | Check `capsule env show` and `capsule config customer show` — one of them is wrong |
| 3 | SshRTC won't connect | Run `capsule cleanup`, retry; if still failing, use `--direct` as fallback; capture `~/.capsule/logs/` and escalate |
| 4 | VS Code Remote-SSH errors after a session | Remove `capsule-<uniqueId>` blocks from `~/.ssh/config` — old sessions leave stale config blocks |
| 5 | macOS Keychain prompts on every command | Click "Always Allow" once in the Keychain dialog — it remembers and stops prompting |
| 6 | Windows PowerShell filter with `>` fails | Use `capsule` (not the `cap` alias) and quote the entire filter: `capsule list --filter "vram>=24"` |
| 7 | `capsule update` fails | Your auth token must be valid (check `capsule status`); close all active SshRTC sessions before retrying |
| 8 | `gh release download` returns 401/403 | Re-check `GH_TOKEN` scopes: all four must be present (`repo`, `read:org`, `workflow`, `user`). Regenerate the token if in doubt. |

**Why you must know all 8:**

Users will report these as "Capsule is broken." You need to immediately recognize the symptom and give the fix in one message, without debugging. Every row in this table represents a real support ticket that was escalated unnecessarily because the person didn't know the fix.

### Exercise:

**Part A — Recall drill (10 min):**

Cover the table. For each symptom below, write the fix from memory:

1. "I run `capsule list` and it shows completely different machines than yesterday."
2. "I'm on macOS and Keychain pops up every time I run any capsule command."
3. "VS Code Remote-SSH is failing to connect to my node and showing config errors."
4. "`capsule update` exits with an error about permissions or auth."

**Part B — Root cause analysis (10 min):**

For each quirk, identify which layer of the triage decision tree would catch it (Step 1 / 2 / 3 / 4 / none — it's a client-side config issue):

| Quirk # | Triage step that catches it | Reasoning |
|---|---|---|
| 2 (wrong machines) | | |
| 3 (SshRTC won't connect) | | |
| 4 (VS Code SSH config) | | |
| 6 (Windows filter) | | |

**Part C — Memorization test (10 min):**

Close the table. Write all 8 rows from memory. Check. Repeat for any you missed.

---

## Part 4 — Core Concepts: The Bug-Report Rubric · 20min

### Reading —

A bug report that is missing any of these 8 fields will be sent back to you for more information. The engineering team cannot reproduce an issue without them.

**Required fields — all 8 must be present:**

| Field | What to include | Why it matters |
|---|---|---|
| 1 | `capsule --version` output | Different versions have different bugs |
| 2 | `capsule env show` output | "Wrong machines" bugs are actually env bugs half the time |
| 3 | `capsule config customer show` output | Same reason as env |
| 4 | The exact command that failed | Copy-paste — not paraphrased. "I ran capsule term" is not enough. Include the full config-tag, all flags. |
| 5 | The exact error output | Copy-paste — not paraphrased. "It said unauthorized" is not enough. Include the full output. |
| 6 | Timestamp of the failure | Correlates with server-side logs |
| 7 | Unique ID of the machine (if applicable) | `capsule list --all` — the unique ID, not the display name |
| 8 | What you already tried | Prevents the support team from suggesting things you've already done |

**The "specificity test":** Read your bug report. Could a stranger who has never seen your machine reproduce the issue from your report alone? If not, it's not complete.

### Exercise:

You receive a bug report from a colleague:

> "Hi, Capsule isn't working. I tried to connect to my machine and it gave an error about SSH. I tried a few things but nothing worked."

1. List every field from the rubric that is missing from this report.
2. Write a follow-up message asking for exactly the fields that are missing (use the exact field names from the rubric).
3. Based on the symptoms described, which triage step would you recommend they run first?

---

## Part 5 — Hands-On: Reproduce Three Quirks · 35min

### Exercise:

Reproduce three quirks deliberately. You remember what you reproduce far better than what you read.

**Quirk 2 — Wrong machines (10 min):**

1. Check your current env: `capsule env show`. Note it.
2. Switch to a different env: `capsule config env set public` (or another env you're not normally in).
3. Run `capsule list`. Observe — the machines shown are different (or none).
4. Fix: `capsule config env set <your-correct-env>`. Confirm `capsule list` shows your fleet again.

**Quirk 6 — Windows filter with `>` (or macOS equivalent) (10 min):**

On macOS/Linux, test the filter quoting behavior:

1. Run: `capsule list --filter vram>=16` (no quotes). Observe the error (zsh may interpret `>=` differently, or capsule may complain about filter format).
2. Run: `capsule list --filter "vram>=16"` (quoted). Observe this works correctly.
3. The lesson: always quote filter arguments. This applies on any shell, not just Windows PowerShell.

**Quirk 3 — SshRTC won't connect (simulate) (15 min):**

1. Set a bad proxy: `export HTTPS_PROXY=http://127.0.0.1:9999`
2. Attempt to connect: `capsule term <your-dev-node-config-tag>`. Observe the hang or connection error.
3. Fix:
   ```bash
   unset HTTPS_PROXY
   capsule cleanup
   capsule term <your-dev-node-config-tag>
   ```
4. Confirm the connection succeeds.
5. Note: `capsule cleanup` was essential here — it cleared the stale connection attempt state before retrying.

---

## Part 6 — Hands-On: File a Proper Bug Report · 20min

### Exercise:

Using the bug-report rubric, draft a complete bug report for the issue you reproduced in Quirk 2 or Quirk 3. Every field must be present.

**Template:**

```
Bug report: [brief description]

1. capsule --version: [paste output]
2. capsule env show: [paste output]
3. capsule config customer show: [paste output]
4. Exact command: [copy-paste]
5. Exact error output: [copy-paste]
6. Timestamp: [YYYY-MM-DD HH:MM UTC]
7. Machine unique ID: [from capsule list --all, if applicable]
8. What I already tried: [list each step]
```

**Peer review (if possible):** Exchange your bug report with a partner. Apply the specificity test: could they reproduce the issue from your report alone, without asking you any follow-up questions? Mark any field that is too vague.

**Solo review:** Read your bug report aloud as if you are the support engineer receiving it. Is every field specific enough? If you would ask a follow-up question, the field is incomplete.

---

## Part 7 — Wrap-up & Connection · 10min

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 40 · Known Quirks &amp; Diagnostics">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the 4 steps of the Capsule triage decision tree in order?",
    "options": [
      "Reboot → reinstall → contact support → escalate",
      "Identify symptom → check known quirks table → run capsule cleanup → escalate if unresolved",
      "Check network → check auth → check node status → retry",
      "Read logs → check GPU → check storage → check network"
    ],
    "answer": 1,
    "explain": "The lesson's triage decision tree: (1) Identify symptom precisely; (2) Match symptom against the known quirks table; (3) Apply the fix (often `capsule cleanup` or a specific command); (4) Escalate with a complete bug report if unresolved. This order prevents unnecessary reinstalls and captures enough information to get help."
  },
  {
    "stem": "What does `capsule cleanup` NOT affect?",
    "options": [
      "Stale socket files and hung connection processes",
      "Your auth token and local config",
      "Your active leases and remote files on nodes",
      "Cached connection state"
    ],
    "answer": 2,
    "explain": "`capsule cleanup` clears LOCAL stale state: hung processes, socket files, cached connection entries. It does NOT release leases, delete remote files, or modify your auth token. This is why it's safe to run as a first diagnostic step — you won't accidentally lose your GPU reservation."
  },
  {
    "stem": "Two symptoms in the known-quirks table have 'run `capsule config customer show`' as their first diagnostic step. What kind of symptom would trigger this?",
    "options": [
      "GPU compute errors and CUDA crashes",
      "Auth failures or 'fleet not found' errors where the wrong customer context might be configured",
      "Network timeouts and connection drops",
      "Streaming quality issues and encoder errors"
    ],
    "answer": 1,
    "explain": "`capsule config customer show` reveals the currently active customer context. Auth failures and 'fleet not found' errors are often caused by being in the wrong customer environment — you authenticated as the right user but the customer context points to a different fleet. Fixing the customer config resolves these without debugging auth itself."
  },
  {
    "stem": "What are the 8 fields of a complete bug report for Capsule?",
    "options": [
      "Date, time, user, command, output, hardware, network, OS version",
      "Symptom, expected behavior, actual behavior, command run, exact output/error, node ID/GPU, steps to reproduce, workarounds tried",
      "Error code, stack trace, version, platform, priority, assignee, status, resolution",
      "Title, description, severity, component, environment, attachments, labels, assignee"
    ],
    "answer": 1,
    "explain": "A good Capsule bug report captures: (1) exact symptom, (2) expected behavior, (3) actual behavior, (4) exact command run, (5) exact output/error text, (6) node ID and GPU type, (7) numbered reproduction steps, (8) workarounds already tried. The lesson's 'specificity test': could a support engineer reproduce it without asking follow-ups?"
  },
  {
    "stem": "Why is the known-quirks table valuable beyond just fixing current issues?",
    "options": [
      "It provides the official SLA for each issue type",
      "After a few weeks, you recognize symptoms instantly and become the person other interns ask when something breaks — it builds diagnostic fluency",
      "It automatically patches issues when run as a script",
      "It contains links to the model weights for common GPU configurations"
    ],
    "answer": 1,
    "explain": "The lesson says: 'After a few weeks, you'll recognize symptoms instantly. After a month, you'll be the person other interns ask when something breaks.' The table builds pattern recognition — each symptom + fix pair is a mental model. Experienced engineers debug by pattern-matching, not by systematic elimination."
  }
]
</script>
</div>

### Connect Forward

The known-quirks table and triage decision tree are the tools you'll reach for every time something stops working — not just in Week 8, but throughout the internship. After a few weeks, you'll recognize symptoms instantly. After a month, you'll be the person other interns ask when something breaks.

### Looking ahead to next week

**Friday (Day 41)** is consolidation — no new reading needed. Review Days 37–40.

**Monday (Day 42):** Next week's first lesson has a pre-read — see [Week 9 Day 1](../../../readings/capsule/).

---

## Stuck?

Ask **oxtutor** to quiz you on the known-quirks table, walk through the triage decision tree with a scenario, or generate extra bug-report practice exercises.
