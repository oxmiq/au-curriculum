# Day 40 · Known Quirks

> **Concept of the day:** every system has failure modes that look mysterious until you've seen them once. Today you learn Capsule's known-quirks list from the Lab Guide so you never waste 30 minutes on a problem that has a 10-second fix.<br> **Pre-reading:** <a href="../../../readings/capsule/#day-40-consolidation-reliability-diagnostics">Capsule Power-User Pre-Lecture Reading — Day 40 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-10-scheduled-jobs-agents-and-the-reliability-toolkit">Capsule Lab Guide</a> Module 10 — Known Quirks.

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
    {status:week-08/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: The Triage Decision Tree |
| Part 3 | Deep Dive: The Known-Quirks Table |
| Part 4 | Core Concepts: The Bug-Report Rubric |
| Part 5 | Hands-On: Reproduce Three Quirks |
| Part 6 | Hands-On: File a Proper Bug Report |
| Part 7 | Wrap-up & Connection |
| **Total** | |

---

## Part 1 — Pre-Reading Review

### Reading —

Before continuing, you should have read **Lab Guide Module 10 (Known Quirks)**. It covers:

- The 4-step triage decision tree
- The known-quirks table (all 8 rows)
- The bug-report rubric (6 required fields)
- `capsule session endall` — when and why

### Exercise:

Answer from memory:

1. What is the first command you run when any Capsule operation fails?
2. What is `capsule session endall` and what state does it tear down?
3. Name four rows from the known-quirks table (symptom + fix).
4. How many fields does a proper bug report require? Name three of them.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m4-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 10">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "`capsule list` shows completely different machines than yesterday. Which two commands do you check FIRST?",
    "options": [
      "capsule status and capsule auth login",
      "capsule --version and capsule update",
      "capsule env show and capsule config customer show",
      "capsule session endall and capsule list --json"
    ],
    "answer": 2,
    "explain": "Per the known-quirks table, 'capsule list shows wrong machines' is fixed by checking 'capsule env show' and 'capsule config customer show' before anything else — one of them is pointed at the wrong environment or customer fleet. Both settings persist across sessions, which is why a single accidental switch explains 'everything stopped working'."
  },
  {
    "stem": "SshRTC won't connect. Per the Capsule troubleshooting steps, what is the first thing you do to reset connection state?",
    "options": [
      "Reinstall the Capsule CLI",
      "Immediately file a bug report",
      "Switch to `capsule stream`",
      "Run `capsule session endall`, then retry the connection"
    ],
    "answer": 3,
    "explain": "USAGE.md's 'SshRTC Connection Issues' recipe is: (1) run 'capsule session endall' to reset connection state, (2) retry the connection, (3) if it still fails, use '--direct' as a fallback. 'capsule session endall' ends every active SshRTC data-channel tunnel without disturbing anything on the remote machine."
  },
  {
    "stem": "You ran `capsule session endall` and retried, but SshRTC still won't connect. What is the documented fallback?",
    "options": [
      "Add the `--direct` flag to bypass the WebRTC data channel",
      "Run `capsule auth login` again",
      "Delete your entire ~/.ssh/config file",
      "Downgrade with `capsule update --pre-release`"
    ],
    "answer": 0,
    "explain": "The known-quirks fix for 'SshRTC won't connect' is: cleanup/endall, retry, then '--direct' as a fallback, and capture logs. The '--direct' flag uses a traditional direct SSH connection instead of the SshRTC (WebRTC) data channel. If '--direct' succeeds, the problem is in the WebRTC path — a network/infrastructure issue worth escalating."
  },
  {
    "stem": "When you capture data for a Capsule bug report / triage, how many pieces of information does the Lab Guide's reliability-lens list say to gather?",
    "options": [
      "4",
      "5",
      "6",
      "8"
    ],
    "answer": 2,
    "explain": "The Lab Guide (Module 10, reliability lens) lists exactly 6 things to capture: (1) 'capsule --version', (2) 'capsule env show', (3) 'capsule config customer show', (4) the exact failing command, (5) the timestamp, and (6) the unique ID of the machine (from 'capsule list --all'). Not 8."
  },
  {
    "stem": "Which set is the Lab Guide's list of what to capture for a good triage / bug report?",
    "options": [
      "CPU, RAM, GPU model, disk, OS, kernel version",
      "capsule --version, env show, config customer show, the exact command, the timestamp, the machine unique ID",
      "title, severity, component, assignee, labels, status",
      "symptom, expected behavior, actual behavior, priority, owner, ETA"
    ],
    "answer": 1,
    "explain": "The Lab Guide's reliability-lens capture list is exactly: 'capsule --version', 'capsule env show', 'capsule config customer show', the exact command, the timestamp, and the machine unique ID (via 'capsule list --all'). Get the unique ID from 'capsule list --all', not the display name — a config tag names a pool, not a specific box."
  },
  {
    "stem": "VS Code Remote-SSH errors appear after a Capsule session ends. What is the fix?",
    "options": [
      "Reinstall the VS Code Remote-SSH extension",
      "Run `capsule auth login`",
      "Clear the macOS Keychain",
      "Remove the `capsule-<uniqueId>` blocks from ~/.ssh/config"
    ],
    "answer": 3,
    "explain": "This is a known quirk: old sessions leave stale 'capsule-<uniqueId>' blocks in ~/.ssh/config, and VS Code Remote-SSH picks up those stale entries and fails. Remove the blocks manually. (The Lab Guide's Module 5 reliability lens gives the same advice: don't leave stale capsule-<uniqueId> entries in your local ~/.ssh/config.)"
  },
  {
    "stem": "On macOS, a Keychain prompt appears on every Capsule command. What is the fix?",
    "options": [
      "Run every Capsule command with sudo",
      "Uninstall and reinstall Capsule",
      "Click 'Always Allow' once in the Keychain dialog",
      "Disable the SshRTC data channel"
    ],
    "answer": 2,
    "explain": "The known-quirks table fix for 'macOS Keychain prompts every command' is to click 'Always Allow' once in the Keychain dialog — it then remembers the permission and stops prompting. (USAGE.md also documents the equivalent 'security set-generic-password-partition-list' command as an alternative.)"
  },
  {
    "stem": "`gh release download` returns 401/403. Per the known-quirks table, what is the most likely cause?",
    "options": [
      "Your GH_TOKEN is missing one or more required scopes",
      "Your Capsule version is outdated",
      "You are pointed at the wrong environment",
      "The GitHub release was deleted"
    ],
    "answer": 0,
    "explain": "The known-quirks table fix for 'gh release download 401/403' is to re-check your GH_TOKEN scopes. The GitHub token is used during installation and updates to fetch releases, so a missing scope surfaces as a 401/403 on download — not as a Capsule auth failure."
  },
  {
    "stem": "Which four scopes must the GitHub token (GH_TOKEN) carry for Capsule installs and release downloads?",
    "options": [
      "admin, write, delete, read",
      "repo, gist, notifications, admin:org",
      "read:user, read:packages, workflow, repo",
      "repo, read:org, workflow, user"
    ],
    "answer": 3,
    "explain": "The Lab Guide (Module 2) and the known-quirks table both state the GH_TOKEN needs scopes 'repo', 'read:org', 'workflow', and 'user'. The token is used only during installation and updates — not at runtime — but a 'gh release download 401/403' almost always traces back to one of these four being absent."
  },
  {
    "stem": "On Windows PowerShell, a filter using `>` (e.g. vram>=24) fails. What is the fix?",
    "options": [
      "Run the command with sudo and the `cap` shortcut",
      "Use `capsule` (not the `cap` shortcut) and quote the whole filter, e.g. capsule list --filter \"vram>=24\"",
      "Switch to the demo environment first",
      "Add the `--direct` flag to the command"
    ],
    "answer": 1,
    "explain": "The known-quirks table fix for 'Windows PowerShell filter with > fails' is to use 'capsule' (not the 'cap' shortener) and quote the whole filter argument. PowerShell interprets an unquoted '>' as output redirection; quoting the filter and avoiding the 'cap' wrapper prevents the shell from creating a file instead of running the filter."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: The Triage Decision Tree

### Reading —

Before filing a bug or escalating to support, run through this 4-step decision tree. In order:

**Step 1: `capsule status`**

Check: is auth valid? Is identity correct? Is the token expiry in the future?

- If "unauthorized": re-run `capsule auth login`
- If "clock skew": sync NTP (`sudo sntp -sS time.apple.com`)
- If token shows expired: re-run `capsule auth login`

**Step 2: `capsule env show` + `capsule config customer show`**

Check: are you pointed at the right environment and customer?

- Wrong environment → `capsule env set <correct-env>` (then re-run `capsule auth login`, since the token is scoped per environment)
- Wrong customer → `capsule config customer set <correct-customer>`
- Both of these settings persist across sessions; getting them wrong once explains why "everything stopped working"

**Step 3: `capsule session endall`**

Ends every active SshRTC data-channel tunnel on your machine at once, resetting stale connection state. Retry the failing operation.

- This fixes many "SshRTC won't connect" and "session hung" issues
- Does **not** affect your running processes on the remote machine or anyone else's sessions — it only closes your local tunnels (`capsule session list` shows them; `capsule session end` closes just one)

**Step 4: `--direct` flag + collect logs**

If Steps 1–3 don't fix it: retry the command with `--direct` to bypass WebRTC. If `--direct` succeeds, the issue is in the WebRTC/SshRTC path (a network or infrastructure issue). Capture the exact command, its full output, and your `capsule --version` / `capsule env show` / `capsule config customer show`, then escalate.

**The rule:** if you're going to file a bug, you must have tried all 4 steps first. Step 4's captured command and full output are the most important data for the engineering team.

### Exercise:

Walk through the decision tree for each scenario below. State which step catches the issue and what the fix is:

1. `capsule term <tag>` hangs. `capsule status` shows valid token. `capsule env show` shows the correct env.
2. `capsule list` shows 0 machines. `capsule status` shows valid token.
3. `capsule term <tag>` returns "connection refused" immediately (not hanging — fast failure).
4. Everything worked yesterday. Today `capsule status` says "unauthorized" with no code changes.

---

## Part 3 — Deep Dive: The Known-Quirks Table

### Reading —

These are all 8 known quirks from Lab Guide Module 10. Memorize every row — symptom and fix.

| # | Symptom | Fix |
|---|---|---|
| 1 | Auth fails in browser flow | CLI falls back to a manual token: run `capsule auth login`, go to `https://oxmiq.ai/oxcapsule/auth` in a browser when prompted, and paste the token |
| 2 | `capsule list` shows wrong machines | Check `capsule env show` and `capsule config customer show` — one of them is wrong |
| 3 | SshRTC won't connect | Run `capsule session endall`, retry; if still failing, use `--direct` as fallback; capture the command output and escalate |
| 4 | VS Code Remote-SSH errors after a session | Remove `capsule-<uniqueId>` blocks from `~/.ssh/config` — old sessions leave stale config blocks |
| 5 | macOS Keychain prompts on every command | Click "Always Allow" once in the Keychain dialog — it remembers and stops prompting |
| 6 | Windows PowerShell filter with `>` fails | Use `capsule` (not the `cap` alias) and quote the entire filter: `capsule list --filter "vram>=24"` |
| 7 | `capsule update` fails | Your auth token must be valid (check `capsule status`); close all active SshRTC sessions before retrying |
| 8 | `gh release download` returns 401/403 | Re-check `GH_TOKEN` scopes: all four must be present (`repo`, `read:org`, `workflow`, `user`). Regenerate the token if in doubt. |

**Why you must know all 8:**

Users will report these as "Capsule is broken." You need to immediately recognize the symptom and give the fix in one message, without debugging. Every row in this table represents a real support ticket that was escalated unnecessarily because the person didn't know the fix.

### Exercise:

**Part A — Recall drill:**

Cover the table. For each symptom below, write the fix from memory:

1. "I run `capsule list` and it shows completely different machines than yesterday."
2. "I'm on macOS and Keychain pops up every time I run any capsule command."
3. "VS Code Remote-SSH is failing to connect to my node and showing config errors."
4. "`capsule update` exits with an error about permissions or auth."

**Part B — Root cause analysis:**

For each quirk, identify which layer of the triage decision tree would catch it (Step 1 / 2 / 3 / 4 / none — it's a client-side config issue):

| Quirk # | Triage step that catches it | Reasoning |
|---|---|---|
| 2 (wrong machines) | | |
| 3 (SshRTC won't connect) | | |
| 4 (VS Code SSH config) | | |
| 6 (Windows filter) | | |

**Part C — Memorization test:**

Close the table. Write all 8 rows from memory. Check. Repeat for any you missed.

---

## Part 4 — Core Concepts: The Bug-Report Rubric

### Reading —

A bug report that is missing any of these 6 fields will be sent back to you for more information. The engineering team cannot reproduce an issue without them.

**Required fields — all 6 must be present:**

| Field | What to include | Why it matters |
|---|---|---|
| 1 | `capsule --version` output | Different versions have different bugs |
| 2 | `capsule env show` output | "Wrong machines" bugs are actually env bugs half the time |
| 3 | `capsule config customer show` output | Same reason as env |
| 4 | The exact command that failed + its full error output | Copy-paste — not paraphrased. "I ran capsule term" and "it said unauthorized" are not enough. Include the full config-tag, all flags, and the complete output. |
| 5 | Timestamp of the failure | Correlates with server-side logs |
| 6 | Unique ID of the machine (from `capsule list --all`) | The unique ID, not the display name — a config tag names a pool, not a specific box |

**The "specificity test":** Read your bug report. Could a stranger who has never seen your machine reproduce the issue from your report alone? If not, it's not complete.

### Exercise:

You receive a bug report from a colleague:

> "Hi, Capsule isn't working. I tried to connect to my machine and it gave an error about SSH. I tried a few things but nothing worked."

1. List every field from the rubric that is missing from this report.
2. Write a follow-up message asking for exactly the fields that are missing (use the exact field names from the rubric).
3. Based on the symptoms described, which triage step would you recommend they run first?

---

## Part 5 — Hands-On: Reproduce Three Quirks

### Exercise:

Reproduce three quirks deliberately. You remember what you reproduce far better than what you read.

**Quirk 2 — Wrong machines:**

1. Check your current env: `capsule env show`. Note it.
2. Switch to a different env: `capsule env set public` (or another env you're not normally in), then re-authenticate with `capsule auth login`.
3. Run `capsule list`. Observe — the machines shown are different (or none).
4. Fix: `capsule env set <your-correct-env>` and re-authenticate. Confirm `capsule list` shows your fleet again.

**Quirk 6 — Windows filter with `>` (or macOS equivalent):**

On macOS/Linux, test the filter quoting behavior:

1. Run: `capsule list --filter vram>=16` (no quotes). Observe the error (zsh may interpret `>=` differently, or capsule may complain about filter format).
2. Run: `capsule list --filter "vram>=16"` (quoted). Observe this works correctly.
3. The lesson: always quote filter arguments. This applies on any shell, not just Windows PowerShell.

**Quirk 3 — SshRTC won't connect (simulate):**

1. Set a bad proxy: `export HTTPS_PROXY=http://127.0.0.1:9999`
2. Attempt to connect: `capsule term <your-dev-node-config-tag>`. Observe the hang or connection error.
3. Fix:
   ```bash
   unset HTTPS_PROXY
   capsule session endall
   capsule term <your-dev-node-config-tag>
   ```

4. Confirm the connection succeeds.
5. Note: `capsule session endall` was essential here — it cleared the stale connection state before retrying.

---

## Part 6 — Hands-On: File a Proper Bug Report

### Exercise:

Using the bug-report rubric, draft a complete bug report for the issue you reproduced in Quirk 2 or Quirk 3. Every field must be present.

**Template:**

```
Bug report: [brief description]

1. capsule --version: [paste output]
2. capsule env show: [paste output]
3. capsule config customer show: [paste output]
4. Exact command that failed + full error output: [copy-paste]
5. Timestamp: [YYYY-MM-DD HH:MM UTC]
6. Machine unique ID: [from capsule list --all]
```

**Peer review (if possible):** Exchange your bug report with a partner. Apply the specificity test: could they reproduce the issue from your report alone, without asking you any follow-up questions? Mark any field that is too vague.

**Solo review:** Read your bug report aloud as if you are the support engineer receiving it. Is every field specific enough? If you would ask a follow-up question, the field is incomplete.

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 40 · Known Quirks &amp; Diagnostics">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the 4 steps of the Capsule triage decision tree in order?",
    "options": [
      "Reboot → reinstall → contact support → escalate",
      "Identify symptom → check known quirks table → run capsule session endall → escalate if unresolved",
      "Check network → check auth → check node status → retry",
      "Read logs → check GPU → check storage → check network"
    ],
    "answer": 1,
    "explain": "The lesson's triage decision tree: (1) Identify symptom precisely; (2) Match symptom against the known quirks table; (3) Apply the fix (often `capsule session endall` or a specific command); (4) Escalate with a complete bug report if unresolved. This order prevents unnecessary reinstalls and captures enough information to get help."
  },
  {
    "stem": "What does `capsule session endall` NOT affect?",
    "options": [
      "The active SshRTC data-channel tunnels open on your machine",
      "Your local tunnel and port state for open sessions",
      "Processes and files on the remote machine, and other users' sessions",
      "The list of open tunnels shown by `capsule session list`"
    ],
    "answer": 2,
    "explain": "`capsule session endall` ends every active SshRTC data-channel tunnel on your machine at once. It does NOT kill processes running on the remote, delete remote files, or disturb other users' sessions (USAGE.md: it terminates tunnels 'without affecting other sessions'). That's why it's safe as a first diagnostic step — you won't lose remote work."
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
    "stem": "What are the 6 fields of a complete Capsule bug report (per the Lab Guide's reliability lens)?",
    "options": [
      "Date, time, user, command, output, OS version",
      "capsule --version, capsule env show, capsule config customer show, the exact failing command (with full output), the timestamp, and the machine unique ID from capsule list --all",
      "Error code, stack trace, version, platform, priority, assignee",
      "Title, description, severity, component, environment, assignee"
    ],
    "answer": 1,
    "explain": "The Lab Guide's reliability lens lists exactly 6 things to capture: `capsule --version`, `capsule env show`, `capsule config customer show`, the exact failing command (copy-pasted with its full output), the timestamp, and the machine unique ID (from `capsule list --all`, not the display name). The 'specificity test': could a support engineer reproduce it without asking follow-ups?"
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
