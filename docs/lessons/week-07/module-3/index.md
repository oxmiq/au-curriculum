# Day 34 · Installation

> **Concept of the day:** **install once, use every day.** A clean Capsule install takes under 15 minutes; a botched one loses you a day. Today you install the CLI, complete the auth flow, run `capsule status`, and memorise the four most-asked support questions.<br> **Pre-reading:** <a href="../../../readings/capsule/#day-36-capsule-architecture-installation">Capsule Power-User Pre-Lecture Reading — Day 36 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-2-installation-first-login">Capsule Lab Guide</a> Module 2.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 7 — Bridge: Theory Meets Tooling</a>
    <span class="sep">/</span>
    <span>Day 34 · Installation</span>
    {status:week-07/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: What the Install Actually Does |
| Part 3 | Core Concepts: Authentication Flow |
| Part 4 | Hands-On: Install on Your Laptop |
| Part 5 | Core Concepts: Four Common Gotchas |
| Part 6 | Hands-On: Gotcha Reproduction Lab |
| Part 7 | Wrap-up & Connection |
| **Total** | |

---

## Part 1 — Pre-Reading Review

### Reading —

Before continuing, you should have read **Lab Guide Module 2** (Installation). It covers:

- Prerequisites: GH_TOKEN scopes, brew tap command, rclone dependency
- The install steps for macOS and Windows
- The `capsule --version` → `capsule auth login` → `capsule status` verification sequence
- Common install gotchas

If you haven't read it yet, stop and read it now.

### Exercise:

Answer from memory:

1. What GitHub token scopes are required for the install? List all four.
2. What directory does Capsule store config and tokens in after install?
3. What is `rclone` and why does Capsule install it?
4. What is the exact command sequence to verify a successful install?
5. Name one of the four common install gotchas.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m3-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 2">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What GitHub token scopes are required for Capsule install?",
    "options": [
      "Only repo scope",
      "repo, read:org, workflow, admin:repo_hook",
      "gist and user scopes",
      "No scopes needed"
    ],
    "answer": 1,
    "explain": "The required GitHub token scopes are: (1) repo, (2) read:org, (3) workflow, (4) admin:repo_hook. These are needed for Capsule to access repositories, read organization membership, manage workflows, and set up webhook integrations."
  },
  {
    "stem": "What directory does Capsule store config and tokens in after install?",
    "options": [
      "/usr/local/bin",
      "~/.capsule (the Capsule config directory in home)",
      "/etc/capsule",
      "The current working directory"
    ],
    "answer": 1,
    "explain": "Capsule stores config and tokens in ~/.capsule (the Capsule config directory in your home directory). This includes authentication tokens, configuration files, and other runtime data."
  },
  {
    "stem": "What is rclone and why does Capsule install it?",
    "options": [
      "A text editor",
      "A file transfer tool used for model caching and data movement",
      "A Python package manager",
      "A type of GPU driver"
    ],
    "answer": 1,
    "explain": "rclone is a file transfer tool used for model caching and data movement. Capsule uses it to efficiently move models and data between local storage, cloud storage, and the GPU fleet."
  },
  {
    "stem": "What is the exact command sequence to verify a successful Capsule install?",
    "options": [
      "capsule init",
      "capsule --version → capsule auth login → capsule status",
      "capsule check",
      "capsule verify"
    ],
    "answer": 1,
    "explain": "The verification sequence is: (1) capsule --version to check the CLI is installed, (2) capsule auth login to authenticate, (3) capsule status to verify the connection to the control plane."
  },
  {
    "stem": "Which of the following is a common install gotcha for Capsule?",
    "options": [
      "Installing in /usr/local/bin requires sudo",
      "Wrong GitHub token scopes, rclone not in PATH, stale cached credentials, or proxy issues",
      "Installing on Linux instead of macOS",
      "Using the wrong GPU model"
    ],
    "answer": 1,
    "explain": "Common install gotchas include: (1) Wrong GitHub token scopes, (2) rclone not in PATH after installation, (3) Stale cached credentials causing auth failures, (4) Proxy/network issues. These are the most common issues that cause install failures."
  },
  {
    "stem": "What is the recommended way to install Capsule on macOS?",
    "options": [
      "Download from website",
      "brew tap and brew install",
      "pip install",
      "Download tarball"
    ],
    "answer": 1,
    "explain": "The recommended way to install Capsule on macOS is via Homebrew: 'brew tap' to add the repository and 'brew install' to install the CLI. This handles dependencies and PATH setup automatically."
  },
  {
    "stem": "What does 'capsule auth login' do?",
    "options": [
      "Installs the CLI",
      "Opens a browser flow to authenticate with GitHub and store credentials",
      "Checks GPU availability",
      "Deploys a model"
    ],
    "answer": 1,
    "explain": "'capsule auth login' opens a browser flow to authenticate with GitHub and store credentials. This is required before you can interact with the Capsule control plane."
  },
  {
    "stem": "What happens if you skip the 'capsule status' verification after install?",
    "options": [
      "Nothing",
      "You might have installation issues that cause failures later when trying to use Capsule",
      "The CLI will stop working",
      "You lose your license"
    ],
    "answer": 1,
    "explain": "Skipping 'capsule status' verification means you might have undetected installation issues. These will cause confusing failures later when you try to deploy models or interact with the fleet. Always verify with 'capsule status' after install."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: What the Install Actually Does

### Reading —

Running the Capsule install does four things:

**1. Places the CLI binary on PATH**

- macOS: `brew tap mihira-ai/software-packages` → `brew install capsule` places the binary at `/usr/local/bin/capsule` (Intel) or `/opt/homebrew/bin/capsule` (Apple Silicon)
- Windows: `winget install` or `gh release download` → binary placed in a directory that must be on PATH

After install, `capsule --version` should return the version string. If it doesn't, PATH is the problem.

**2. Creates the config directory `~/.capsule/`**

Contents after first run:
```
~/.capsule/
  credentials        ← auth tokens (encrypted on macOS Keychain)
  config.json        ← default env, default customer, cached metadata
  logs/              ← debug logs for support
```

**3. Installs `rclone` alongside**

Capsule uses `rclone` under the hood for cloud storage mounts (OneDrive). You don't invoke rclone directly — `capsule auth storage` and `capsule mount` handle it — but rclone must be on PATH. The brew formula handles this automatically on macOS.

**4. Requires GH_TOKEN during tap**

The software-packages repo is private. `brew tap` must authenticate via GITHUB_API_TOKEN. The token needs these scopes:

- `repo` — read private repos (for the tap and release downloads)
- `read:org` — verify org membership
- `workflow` — allow workflow-triggered releases
- `user` — read user profile for identity

**Post-install verification sequence:**

```bash
capsule --version        # → "capsule version 1.x.x"
capsule auth login       # → opens browser, complete OAuth
capsule status           # → prints identity + token expiry
capsule auth storage     # → opens browser, complete OneDrive OAuth
capsule list | head      # → shows first few machines in your fleet
```

If any step fails, see Part 5.

### Exercise:

Without looking at the above:

1. List the 4 things the install does, in order.
2. What is in `~/.capsule/credentials`?
3. Why is `rclone` needed?
4. What 4 GH_TOKEN scopes are needed and why does each matter?

---

## Part 3 — Core Concepts: Authentication Flow

### Reading —

**`capsule auth login` — the main auth flow:**

1. The CLI opens a browser tab to `https://login.oxmiq.ai` (Azure B2C tenant)
2. You complete the OAuth flow (sign in with your org account)
3. Azure B2C returns an authorization code
4. The CLI exchanges the code for refresh + access tokens
5. Tokens are stored in `~/.capsule/credentials`, encrypted using macOS Keychain (macOS) or Windows DPAPI (Windows)
6. `capsule status` shows: identity (email), token type, and expiry timestamp

**Token lifecycle:**

| Token | TTL | What it controls |
|---|---|---|
| Access token | ~60 minutes | API calls to control plane |
| Refresh token | ~30 days | Mint new access tokens without browser re-auth |

When the access token expires, Capsule uses the refresh token automatically. When the refresh token expires (30 days of inactivity), you must re-run `capsule auth login`.

**`capsule auth storage` — separate OneDrive consent:**

OneDrive requires a separate OAuth consent because it's a Microsoft Graph permission. Run once after login:

```bash
capsule auth storage   # opens browser → consent to OneDrive access → stores token
```

**Headless / CI authentication:**

In headless terminals (no browser), two options:

1. `capsule auth login --device-code` — prints a URL and a code; you open the URL on any browser, enter the code, and the CLI polls for completion
2. Set `CAPSULE_AUTH_TOKEN=<access_token>` environment variable — the CLI uses this token directly (useful in CI pipelines)

**Clock skew causes silent auth failures:**

If your system clock is more than 5 minutes ahead of UTC, the access token will be rejected by the server even if it hasn't expired locally. Symptom: `capsule status` shows valid token, but all API calls fail with "unauthorized."

Fix: sync NTP — `sudo sntp -sS time.apple.com` (macOS) or `w32tm /resync` (Windows).

### Exercise:

1. Draw the auth flow as a sequence diagram: CLI → Browser → Azure B2C → CLI → `~/.capsule/credentials`.
2. What is the difference between an access token and a refresh token? What happens when each expires?
3. You are setting up Capsule in a GitHub Actions CI workflow. Which auth method do you use and why?
4. A colleague says "I logged in fine but now all commands say unauthorized." What is the most likely cause and how do you diagnose it?

---

## Part 4 — Hands-On: Install on Your Laptop

### Exercise:

Complete the full Capsule install on your machine. Follow these exact steps and record the output of each command.

**macOS:**

```bash
# Step 1: Set your GH_TOKEN (get it from github.com/settings/tokens/new)
export GH_TOKEN=<your_token>
export HOMEBREW_GITHUB_API_TOKEN=$GH_TOKEN

# Step 2: Tap the private formula repo
brew tap mihira-ai/software-packages \
  https://$GH_TOKEN@github.com/mihira-ai/software-packages.git

# Step 3: Install
brew install capsule

# Step 4: Verify binary
capsule --version

# Step 5: Authenticate
capsule auth login    # complete the browser flow

# Step 6: Check status
capsule status        # copy the output here

# Step 7: Storage auth
capsule auth storage  # complete the browser flow

# Step 8: Confirm fleet visibility
capsule list | head -10
```

**Deliverables — paste into your lab notes:**

1. Output of `capsule --version`
2. Output of `capsule status` (redact your full email if sharing)
3. Output of `capsule list | head -10` (confirm you can see machines)
4. Time taken: _____ minutes

If any step failed, jump to Part 5 for the gotcha table.

---

## Part 5 — Core Concepts: Four Common Gotchas

### Reading —

These are the four most common support questions after a new install. Memorize them — you'll answer at least one of these per week of the internship.

**Gotcha 1: `capsule: command not found`**

- **Symptom:** `zsh: command not found: capsule` or `bash: capsule: command not found`
- **Cause:** The install directory is not on PATH. brew may have printed "capsule was successfully installed but may not be linked" — or you installed but haven't restarted the shell.
- **Fix:** `source ~/.zshrc` or `source ~/.bashrc`, or open a new terminal window. If still not found: `echo $PATH` — verify `/usr/local/bin` (Intel Mac) or `/opt/homebrew/bin` (Apple Silicon) is included.

**Gotcha 2: `capsule auth login` browser doesn't open**

- **Symptom:** The command runs but no browser opens; it prints a URL but hangs.
- **Cause:** Headless terminal (remote SSH session, tmux with no display), or browser association is broken.
- **Fix:** Use `--device-code` flag: `capsule auth login --device-code`. Copy the printed URL + code to any browser.

**Gotcha 3: `capsule status` shows "unauthorized" after successful login**

- **Symptom:** `capsule status` shows "Token expired" or "Unauthorized" immediately after `capsule auth login` succeeded.
- **Cause:** System clock is skewed by more than 5 minutes from UTC. The token is technically valid locally but fails server-side validation.
- **Diagnosis:** `date -u` — compare to actual UTC time.
- **Fix:** Sync NTP: `sudo sntp -sS time.apple.com` (macOS) or `sudo ntpdate -s time.nist.gov` (Linux).

**Gotcha 4: SSH to a node hangs after `capsule connect`**

- **Symptom:** `capsule term <config-tag>` prints "connecting..." and hangs indefinitely.
- **Cause:** Corporate proxy is intercepting the WebRTC / SSH traffic. Capsule SshRTC uses non-standard ports that some proxies block.
- **Diagnosis:** Check `echo $HTTPS_PROXY` — if set, it may be blocking Capsule's traffic.
- **Fix:** Set `HTTPS_PROXY` to your organization's proxy if needed, or ask IT to whitelist `*.oxmiq.ai` and `*.capsuleapp.cloud`. As a fallback: `capsule term <config-tag> --direct` bypasses WebRTC.

### Exercise:

For each gotcha, fill in this table from memory (no notes):

| Gotcha | Exact symptom | First diagnostic command | Fix command |
|---|---|---|---|
| 1. command not found | | | |
| 2. browser doesn't open | | | |
| 3. unauthorized after login | | | |
| 4. SSH hangs | | | |

---

## Part 6 — Hands-On: Gotcha Reproduction Lab

### Exercise:

Reproduce three of the four gotchas deliberately and fix them. You will remember what you reproduce much better than what you only read.

**Reproduce Gotcha 1:**

1. Temporarily remove the capsule binary directory from PATH: `export PATH=$(echo $PATH | tr ':' '\n' | grep -v capsule | tr '\n' ':')`
2. Run `capsule --version`. Observe the "command not found" error.
3. Fix: add the directory back, or run `source ~/.zshrc`.
4. Confirm `capsule --version` works again.

**Reproduce Gotcha 2:**

1. Run `capsule auth login --device-code`. Observe that it prints a URL + code instead of opening a browser.
2. Copy the URL. Open it in a browser. Enter the code. Confirm auth completes.
3. This is exactly what you'll do in any headless environment.

**Reproduce Gotcha 3:**

1. Set your system clock 10 minutes ahead (macOS System Preferences → Date & Time → uncheck "Set automatically" → advance by 10 minutes).
2. Run `capsule status`. Observe the unauthorized error.
3. Fix: re-enable automatic time sync. Run `sudo sntp -sS time.apple.com`.
4. Confirm `capsule status` works again.
5. **Important:** Re-enable automatic time sync — don't leave it off.

**Reproduce Gotcha 4 (8 min — simulate):**

1. Set a bad proxy: `export HTTPS_PROXY=http://127.0.0.1:9999`
2. Attempt to connect: `capsule term <your-dev-node-config-tag>`. Observe the hang or error.
3. Fix: `unset HTTPS_PROXY && capsule cleanup && capsule term <config-tag>`.
4. Confirm connection succeeds.

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 34 · Capsule Install &amp; Auth">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the `--device-code` flag used for in Capsule authentication?",
    "options": [
      "It specifies which GPU device to authenticate against",
      "It enables headless authentication (for machines without a browser) by displaying a code you enter on a separate device",
      "It generates a device-specific license key for Capsule",
      "It disables multi-factor authentication for faster login"
    ],
    "answer": 1,
    "explain": "`--device-code` enables OAuth device-code flow: the CLI displays a short code and URL. You open that URL on any browser (your laptop while the CLI runs on a headless server), enter the code, and authenticate. The CLI then receives the token. Essential for remote or server-only environments."
  },
  {
    "stem": "What does `capsule cleanup` do and when should you run it?",
    "options": [
      "It deletes all files from the remote node — run it when you're done with a session",
      "It clears stale local state (cached connections, hung processes, corrupt config entries) — run it as the first step when Capsule commands hang or behave unexpectedly",
      "It logs you out of Capsule and removes your auth token",
      "It releases all your active leases and disconnects all sessions"
    ],
    "answer": 1,
    "explain": "`capsule cleanup` clears local state that may be stale or corrupted — hung connection processes, cached socket files, partial config entries. It does NOT release your leases or delete remote files. It's the go-to first diagnostic step when Capsule seems stuck: run cleanup, then retry the command."
  },
  {
    "stem": "What is the typical TTL difference between an access token and a refresh token in Capsule?",
    "options": [
      "Access token: 1 year; Refresh token: 30 days",
      "Access token: short-lived (hours); Refresh token: long-lived (days to weeks)",
      "Access token: 5 minutes; Refresh token: 1 hour",
      "Both tokens have the same TTL of 24 hours"
    ],
    "answer": 1,
    "explain": "Access tokens are short-lived (typically hours) for security — if stolen, they expire quickly. Refresh tokens are long-lived (days to weeks) and are used to obtain new access tokens without re-authenticating. This pattern minimizes the window for access token misuse while maintaining session continuity."
  },
  {
    "stem": "What is the first diagnostic step when a Capsule command appears stuck or hangs?",
    "options": [
      "Restart the GPU machine",
      "Run `capsule cleanup` to clear stale local state, then retry",
      "Re-install the Capsule CLI",
      "Contact support immediately"
    ],
    "answer": 1,
    "explain": "The lesson states: 'capsule cleanup as the first step when something is stuck.' Hung connections, stale socket files, or corrupt local config entries cause most hangs. `capsule cleanup` resolves these without affecting your leases or remote data. After cleanup, retry the failing command."
  },
  {
    "stem": "Which of the following is a common install gotcha for Capsule on Linux?",
    "options": [
      "Capsule requires Python 3.11 or higher",
      "PATH not updated after install — `capsule` command not found until the shell is restarted or PATH is sourced",
      "Capsule requires a GPU in the local machine for installation",
      "Capsule must be installed as root"
    ],
    "answer": 1,
    "explain": "A common install gotcha: the install script adds Capsule to a PATH directory but the current shell session doesn't see it yet. Fix: run `source ~/.bashrc` (or `~/.zshrc`) or open a new terminal. This is one of the four gotchas the lesson enumerates — check the gotchas table for the full list."
  }
]
</script>
</div>

### Connect Forward

You've installed the tool. The next two days build the daily workflow: environments and fleet discovery (Day 35), and then the Week 7 Friday wrap (Day 36) to cement everything before Week 8's operational deep-dives.

### Pre-read for tomorrow (Day 35 · Environments & Fleet Discovery)

- **Resource:** <a href="../../../readings/capsule/#day-37-environments-fleet-discovery">Capsule Power-User Pre-Lecture Reading — Day 37 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-3-environments-customers-and-why-your-fleet-looks-wrong">Capsule Lab Guide</a> Module 3.
- **Reflection questions:**
  1. How do you list available machines? What command shows machine details?
  2. What fields distinguish an `available` machine from a `leased` one?
  3. What does `capsule config customer set` do and when do you need it?

---

## Stuck?

Ask **oxtutor** to walk through the install steps, explain the auth flow, or quiz you on the four gotchas and their fixes.
