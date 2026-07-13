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
    "stem": "Which GitHub token (GH_TOKEN) scopes are required to install Capsule?",
    "options": [
      "Only `repo`",
      "`repo`, `read:org`, `workflow`, `admin:repo_hook`",
      "`repo`, `read:org`, `workflow`, `user`",
      "No token or scopes are required"
    ],
    "answer": 2,
    "explain": "The PAT needs `repo` (read the private tap and release downloads), `read:org` (verify org membership), `workflow` (workflow-triggered releases), and `user` (read the user profile for identity). Lab Guide Module 2 and Part 2 of this lesson both list exactly these four. The token is used at install/update time only, not at runtime."
  },
  {
    "stem": "What does `capsule auth login` actually do?",
    "options": [
      "Opens a browser to the Azure B2C login page (`https://login.oxmiq.ai`), completes OAuth, and caches the returned token",
      "Authenticates against GitHub and stores a GitHub token",
      "Installs the CLI binary and rclone",
      "Lists the machines in your fleet"
    ],
    "answer": 0,
    "explain": "`capsule auth login` opens a browser tab to the Azure B2C tenant, you sign in with your org account, and the CLI exchanges the returned authorization code for refresh + access tokens. It authenticates via Azure B2C, not GitHub. If the browser can't open (headless/remote), it falls back to a manual token flow."
  },
  {
    "stem": "Where does Capsule store its configuration, cached token, and SSH keys after install?",
    "options": [
      "`/etc/capsule/` on every platform",
      "The current working directory",
      "`~/.capsule/` on every OS",
      "macOS: `$HOME/Library/Application Support/Capsule/`; Windows: `%APPDATA%\\capsule`"
    ],
    "answer": 3,
    "explain": "The USAGE guide lists the config directory as `$HOME/Library/Application Support/Capsule/` on macOS and `%APPDATA%\\capsule` on Windows. It holds `capsule.conf`, the auto-generated `capsule_rsa`/`capsule_rsa.pub` SSH keypair, and `rclone.conf`."
  },
  {
    "stem": "What is `rclone` and why does the Capsule install include it?",
    "options": [
      "A GPU driver Capsule needs to run benchmarks",
      "A file-transfer tool Capsule uses under the hood for cloud storage mounts (OneDrive); it must be on PATH",
      "A Python package manager for installing model dependencies",
      "A terminal multiplexer for keeping sessions alive"
    ],
    "answer": 1,
    "explain": "Capsule uses `rclone` under the hood for cloud storage mounts (OneDrive). You never call it directly — `capsule auth storage` and the OneDrive mount handle it — but it must be on PATH. The brew formula installs it automatically on macOS; on Windows you run `winget install Rclone.Rclone`."
  },
  {
    "stem": "What is the post-install command sequence used to verify a working Capsule install?",
    "options": [
      "`capsule init`",
      "`capsule verify --all`",
      "`capsule --version` → `capsule auth login` → `capsule status`",
      "`capsule check`"
    ],
    "answer": 2,
    "explain": "Run `capsule --version` to confirm the binary is on PATH, `capsule auth login` to complete the browser auth flow, then `capsule status` to confirm your identity and a non-empty token expiry. Both the lesson and Lab Guide Module 2 use this exact sequence."
  },
  {
    "stem": "The Capsule CLI can be invoked as `capsule`. What is `cap`?",
    "options": [
      "A separate, lighter client that only supports a subset of commands",
      "A shortcut alias for `capsule`, created automatically during install",
      "A command that only exists on Windows",
      "There is no shortcut; you must always type `capsule`"
    ],
    "answer": 1,
    "explain": "`cap` is a shortcut for `capsule`, created during install as a symlink (Unix/macOS) or batch wrapper (Windows); `cap list` and `capsule list` are equivalent. One caveat: on PowerShell, `cap list --filter` with a `>` breaks, so use `capsule` and quote the filter argument there."
  },
  {
    "stem": "How do you check whether a newer Capsule version is available without installing it?",
    "options": [
      "`capsule update --dry-run`",
      "`capsule check-update`",
      "`capsule --version --remote`",
      "`capsule update --check-only`"
    ],
    "answer": 3,
    "explain": "`capsule update --check-only` reports whether a newer stable release exists without installing. `capsule update` installs the latest stable build, and `capsule update --pre-release` installs the latest pre-release. (Updates require a valid auth token and no in-use CLI files / open SshRTC sessions.)"
  },
  {
    "stem": "After `capsule auth login`, how do you grant Capsule access to your OneDrive cloud storage?",
    "options": [
      "Run `capsule auth storage` and complete the separate consent flow",
      "It is granted automatically as part of `capsule auth login`",
      "Edit `rclone.conf` by hand and paste your OneDrive password",
      "Run `capsule mount --login`"
    ],
    "answer": 0,
    "explain": "OneDrive access is a separate consent step: run `capsule auth storage` once and complete the browser consent flow. After that, connection commands auto-mount your OneDrive folder. Login and storage auth are distinct — logging in does not by itself grant storage access."
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

**2. Creates the OS-specific config directory**

There is no `~/.capsule/`. Capsule stores its state in the platform config directory — `$HOME/Library/Application Support/Capsule/` on macOS, `%APPDATA%\capsule` on Windows. Contents after first run:
```
Capsule/
  capsule.conf          ← config: default env, customer, settings
  capsule_rsa / .pub    ← auto-generated SSH keypair
  rclone.conf           ← cloud storage (OneDrive) config
```
The cached Azure B2C auth token lives alongside this config (held in the macOS Keychain where available).

**3. Installs `rclone` alongside**

Capsule uses `rclone` under the hood for cloud storage mounts (OneDrive). You don't invoke rclone directly — `capsule auth storage` and the automatic OneDrive mount handle it — but rclone must be on PATH. The brew formula handles this automatically on macOS.

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
2. Where does Capsule store its config and cached token, and what files does that directory contain?
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
5. The token is cached in Capsule's config directory (`$HOME/Library/Application Support/Capsule/` on macOS, `%APPDATA%\capsule` on Windows), held in the macOS Keychain where available
6. `capsule status` shows: identity (email), token type, and expiry timestamp

**Token lifecycle:**

| Token | TTL | What it controls |
|---|---|---|
| Access token | ~60 minutes | API calls to the Capsule backend |
| Refresh token | ~30 days | Mint new access tokens without browser re-auth |

When the access token expires, Capsule uses the refresh token automatically. When the refresh token expires (30 days of inactivity), you must re-run `capsule auth login`.

**`capsule auth storage` — separate OneDrive consent:**

OneDrive requires a separate OAuth consent because it's a Microsoft Graph permission. Run once after login:

```bash
capsule auth storage   # opens browser → consent to OneDrive access → stores token
```

**Headless / CI authentication:**

In headless terminals (no browser), two options:

1. **Manual token fallback** — when the browser can't open, `capsule auth login` automatically prints a URL (`https://oxmiq.ai/oxcapsule/auth`); open it on any browser, complete auth, then paste the token it gives you back into the CLI when prompted
2. Set the `CAPSULE_AUTH_TOKEN=<token>` environment variable — the CLI uses this token directly (this is how headless CI authenticates)

**Clock skew causes silent auth failures:**

If your system clock is more than 5 minutes ahead of UTC, the access token will be rejected by the server even if it hasn't expired locally. Symptom: `capsule status` shows valid token, but all API calls fail with "unauthorized."

Fix: sync NTP — `sudo sntp -sS time.apple.com` (macOS) or `w32tm /resync` (Windows).

### Exercise:

1. Draw the auth flow as a sequence diagram: CLI → Browser → Azure B2C → CLI → cached token in Capsule's config directory.
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
- **Fix:** Use the manual token fallback — `capsule auth login` prints a URL (`https://oxmiq.ai/oxcapsule/auth`); open it in any browser, complete auth, and paste the returned token back into the CLI. In CI, set `CAPSULE_AUTH_TOKEN` instead.

**Gotcha 3: `capsule status` shows "unauthorized" after successful login**

- **Symptom:** `capsule status` shows "Token expired" or "Unauthorized" immediately after `capsule auth login` succeeded.
- **Cause:** System clock is skewed by more than 5 minutes from UTC. The token is technically valid locally but fails server-side validation.
- **Diagnosis:** `date -u` — compare to actual UTC time.
- **Fix:** Sync NTP: `sudo sntp -sS time.apple.com` (macOS) or `sudo ntpdate -s time.nist.gov` (Linux).

**Gotcha 4: connection hangs after `capsule term`**

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

1. Run `capsule auth login` in a shell with no browser available (e.g. over SSH). Observe that it falls back to printing a URL (`https://oxmiq.ai/oxcapsule/auth`) instead of opening a browser.
2. Open the URL in a browser, complete auth, then paste the returned token back into the CLI. Confirm auth completes.
3. This is exactly what you'll do in any headless environment (or set `CAPSULE_AUTH_TOKEN`).

**Reproduce Gotcha 3:**

1. Set your system clock 10 minutes ahead (macOS System Preferences → Date & Time → uncheck "Set automatically" → advance by 10 minutes).
2. Run `capsule status`. Observe the unauthorized error.
3. Fix: re-enable automatic time sync. Run `sudo sntp -sS time.apple.com`.
4. Confirm `capsule status` works again.
5. **Important:** Re-enable automatic time sync — don't leave it off.

**Reproduce Gotcha 4 (8 min — simulate):**

1. Set a bad proxy: `export HTTPS_PROXY=http://127.0.0.1:9999`
2. Attempt to connect: `capsule term <your-dev-node-config-tag>`. Observe the hang or error.
3. Fix: `unset HTTPS_PROXY && capsule session endall && capsule term <config-tag>`.
4. Confirm connection succeeds.

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 34 · Capsule Install &amp; Auth">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "You're authenticating Capsule on a headless server with no browser. What does `capsule auth login` do?",
    "options": [
      "It fails — Capsule can only authenticate from a machine with a browser",
      "It falls back to a manual token flow: it prints a URL you open on any browser, then you paste the returned token back into the CLI (or you set `CAPSULE_AUTH_TOKEN`)",
      "It generates a device-specific license key that never expires",
      "It silently logs you in as an anonymous user"
    ],
    "answer": 1,
    "explain": "When no browser is available, `capsule auth login` automatically switches to the manual token fallback: it prints a URL (`https://oxmiq.ai/oxcapsule/auth`), you complete auth there and paste the token back into the CLI. For CI/automation you can instead export `CAPSULE_AUTH_TOKEN` and skip the interactive flow entirely."
  },
  {
    "stem": "An SshRTC connection (`capsule term`) keeps failing. What is the correct fallback?",
    "options": [
      "Delete all files from the remote machine and reconnect",
      "Add `--direct` to use a direct SSH connection instead of the SshRTC data channel",
      "Re-install the Capsule CLI from scratch",
      "Switch to a different GPU vendor"
    ],
    "answer": 1,
    "explain": "The SshRTC (WebRTC) data channel is the default because it works without public-facing ports, but it can fail behind restrictive networks/proxies. The documented fallback is `--direct`, which forces a traditional SSH connection (requires an open port). First reset connection state with `capsule session endall`, then retry; if it still fails, use `--direct`."
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
      "Run `capsule session endall` to reset SshRTC connection state, then retry",
      "Re-install the Capsule CLI",
      "Contact support immediately"
    ],
    "answer": 1,
    "explain": "Most hangs come from stuck SshRTC tunnels. `capsule session endall` tears down all active data-channel tunnels so you can retry cleanly; `capsule session list`/`end` do the same at finer grain. After resetting, retry the failing command; if it still fails, fall back to `--direct`."
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
  },
  {
    "stem": "Which four GitHub token (GH_TOKEN) scopes does the Capsule install require, and why?",
    "options": [
      "`repo` only — nothing else is needed",
      "`repo`, `read:org`, `workflow`, `admin:repo_hook`",
      "`repo` (read the private tap + release downloads), `read:org` (verify org membership), `workflow` (workflow-triggered releases), and `user` (read the profile for identity)",
      "No token is needed; the tap is public"
    ],
    "answer": 2,
    "explain": "Part 2 ('Requires GH_TOKEN during tap'): the software-packages repo is private, so `brew tap` authenticates with a PAT carrying `repo`, `read:org`, `workflow`, and `user`. The token is used only at install/update time, not at runtime — runtime auth is Azure B2C via `capsule auth login`."
  },
  {
    "stem": "What is the exact post-install command sequence to verify a working Capsule install?",
    "options": [
      "`capsule --version` -> `capsule auth login` -> `capsule status` (then `capsule auth storage` and `capsule list | head`)",
      "`capsule init` -> `capsule verify --all`",
      "`capsule check` -> `capsule login` -> `capsule ping`",
      "`capsule doctor` -> `capsule test`"
    ],
    "answer": 0,
    "explain": "Part 2 and Part 4: run `capsule --version` to confirm the binary is on PATH, `capsule auth login` to complete the Azure B2C browser flow, then `capsule status` to print your identity and token expiry. Part 4 adds `capsule auth storage` (OneDrive consent) and `capsule list | head` to confirm fleet visibility. There is no `capsule init`, `verify`, `check`, or `doctor` command."
  },
  {
    "stem": "Why does the Capsule install include `rclone`?",
    "options": [
      "It is the GPU driver Capsule needs to run benchmarks",
      "It is a Python package manager for model dependencies",
      "It is a terminal multiplexer that keeps sessions alive",
      "Capsule uses it under the hood for cloud storage mounts (OneDrive); you never call it directly, but it must be on PATH"
    ],
    "answer": 3,
    "explain": "Part 2 ('Installs rclone alongside') and Part 1: rclone is a file-transfer tool Capsule uses under the hood for OneDrive cloud-storage mounts. `capsule auth storage` and the automatic OneDrive mount drive it — you never invoke it directly — but it must be on PATH. The brew formula installs it automatically on macOS."
  },
  {
    "stem": "`capsule status` reports 'unauthorized' immediately after a successful `capsule auth login`. What is the most likely cause?",
    "options": [
      "The GH_TOKEN scopes are wrong",
      "The system clock is skewed more than 5 minutes from UTC, so a locally valid token fails server-side validation (diagnose with `date -u`, fix by syncing NTP)",
      "rclone is missing from PATH",
      "You must reinstall the CLI from scratch"
    ],
    "answer": 1,
    "explain": "Part 3 and Gotcha 3 in Part 5: clock skew causes silent auth failures — if the system clock is more than ~5 minutes ahead of UTC the access token is rejected server-side even though it looks valid locally. Diagnose with `date -u` against real UTC; fix by syncing NTP (`sudo sntp -sS time.apple.com` on macOS, `w32tm /resync` on Windows)."
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
