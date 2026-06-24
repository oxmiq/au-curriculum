# Day 34 · Installation

> **Concept of the day:** **install once, use every day.** A clean Capsule install takes under 15 minutes; a botched one loses you a day. Today you install the CLI, complete the auth flow, run `capsule status`, and memorise the four most-asked support questions.<br> **Pre-reading:** Capsule Power User Lab Guide **Module 2** (~20 min).

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
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-07/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: What the Install Actually Does | 20 min |
| Part 3 | Core Concepts: Authentication Flow | 20 min |
| Part 4 | Hands-On: Install on Your Laptop | 45 min |
| Part 5 | Core Concepts: Four Common Gotchas | 20 min |
| Part 6 | Hands-On: Gotcha Reproduction Lab | 30 min |
| Part 7 | Wrap-up & Connection | 10 min |
| **Total** | | **~160 min + pre-reading** |

---

## Part 1 — Pre-Reading Review · 15min

### Reading —

Before continuing, you should have read **Lab Guide Module 2** (Installation). It covers:

- Prerequisites: GH_TOKEN scopes, brew tap command, rclone dependency
- The install steps for macOS and Windows
- The `capsule --version` → `capsule auth login` → `capsule status` verification sequence
- Common install gotchas

If you haven't read it yet, stop and read it now (~20 min).

### Exercise:

Answer from memory:

1. What GitHub token scopes are required for the install? List all four.
2. What directory does Capsule store config and tokens in after install?
3. What is `rclone` and why does Capsule install it?
4. What is the exact command sequence to verify a successful install?
5. Name one of the four common install gotchas.

---

## Part 2 — Core Concepts: What the Install Actually Does · 20min

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

## Part 3 — Core Concepts: Authentication Flow · 20min

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

## Part 4 — Hands-On: Install on Your Laptop · 45min

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

## Part 5 — Core Concepts: Four Common Gotchas · 20min

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

## Part 6 — Hands-On: Gotcha Reproduction Lab · 30min

### Exercise:

Reproduce three of the four gotchas deliberately and fix them. You will remember what you reproduce much better than what you only read.

**Reproduce Gotcha 1 (8 min):**

1. Temporarily remove the capsule binary directory from PATH: `export PATH=$(echo $PATH | tr ':' '\n' | grep -v capsule | tr '\n' ':')`
2. Run `capsule --version`. Observe the "command not found" error.
3. Fix: add the directory back, or run `source ~/.zshrc`.
4. Confirm `capsule --version` works again.

**Reproduce Gotcha 2 (7 min):**

1. Run `capsule auth login --device-code`. Observe that it prints a URL + code instead of opening a browser.
2. Copy the URL. Open it in a browser. Enter the code. Confirm auth completes.
3. This is exactly what you'll do in any headless environment.

**Reproduce Gotcha 3 (7 min):**

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

## Part 7 — Wrap-up & Connection · 10min

### Self-check

Before closing, tick each item:

- [ ] I have Capsule installed and `capsule status` shows a valid token.
- [ ] I have `capsule list` returning my fleet.
- [ ] I can recite the four gotchas and their fixes without notes.
- [ ] I understand the difference between the access token and refresh token TTLs.
- [ ] I know the `--device-code` flag for headless auth.
- [ ] I know `capsule cleanup` as the first step when something is stuck.

### Connect Forward

You've installed the tool. The next two days build the daily workflow: environments and fleet discovery (Day 35), and then the Week 7 Friday wrap (Day 36) to cement everything before Week 8's operational deep-dives.

### Pre-read for tomorrow (Day 35 · Environments & Fleet Discovery)

- **Resource:** Capsule Power User Lab Guide **Module 3** (~15 min).
- **Reflection questions:**
  1. How do you list available machines? What command shows machine details?
  2. What fields distinguish an `available` machine from a `leased` one?
  3. What does `capsule config customer set` do and when do you need it?

---

## Stuck?

Ask **oxtutor** to walk through the install steps, explain the auth flow, or quiz you on the four gotchas and their fixes.
