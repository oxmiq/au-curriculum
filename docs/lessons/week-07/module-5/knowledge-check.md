<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 7 — Bridge: Theory Meets Tooling</a>
    <span class="sep">/</span>
    <a href="../">Day 35 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-07/module-5}
  </div>
</div>

# Week 7 Knowledge Check

**Week 7 · Bridge: Theory Meets Tooling.** 30-question bank · **16 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m5-canonical" data-kind="wrap-up" data-draw="16" data-lesson="Week 7 · Bridge: Theory Meets Tooling" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Klarna's customer-service agent used which orchestration pattern?",
    "options": [
      "Single-agent loop",
      "Planner-worker",
      "Supervisor-worker",
      "Swarm / parallel sampling"
    ],
    "answer": 1,
    "explain": "Klarna used planner-worker: a natural-language frontend classified intent and routed each inquiry to specialized sub-agents that called Klarna's order-management, returns, and read-only payment APIs."
  },
  {
    "stem": "The key governance control in Klarna's agent deployment was:",
    "options": [
      "Unrestricted tool access",
      "Human review of every single response before sending",
      "Read-only payment access plus hard human-escalation thresholds (refunds above a limit, disputes, complaint threads)",
      "No governance — fully autonomous"
    ],
    "answer": 2,
    "explain": "Klarna's agent has read access to payment data but no direct payment-mutation access. Hard escalation rules route refunds above a threshold, disputed transactions, and complaint threads to a human — 'human-in-the-loop on the critical path' — rather than reviewing every response."
  },
  {
    "stem": "Claude Code / Cursor represent what orchestration pattern?",
    "options": [
      "Planner-worker",
      "Supervisor-worker",
      "Single-agent with tools",
      "Hierarchical with sub-planners"
    ],
    "answer": 2,
    "explain": "Claude Code and Cursor are single-agent harnesses: one model with a defined toolset (read_file, write_file, run_command, git_*) runs the loop. Orchestration is minimal — the work is in the prompt and tool design."
  },
  {
    "stem": "For coding agents like Claude Code / Cursor, what makes their environment different from customer-service agents?",
    "options": [
      "They don't use tools",
      "They work in highly structured, stateful environments (files, tests, git) where tool results are deterministic and every write is reversible via git",
      "They require human approval for every action",
      "They cannot access the internet"
    ],
    "answer": 1,
    "explain": "Coding agents work in highly structured, stateful codebases: file contents and test pass/fail are deterministic feedback, and git makes every write reversible. That reversibility is why interactive dev can let the agent write directly."
  },
  {
    "stem": "How did SemiAnalysis's due-diligence agent improve research throughput?",
    "options": [
      "It cut per-company screening from 45 minutes to 8 minutes, letting the firm screen 200+ more companies per month",
      "It replaced all human analysts with a single model and no oversight",
      "It screened exactly 10,000 companies per day with zero errors",
      "It eliminated the need to read SEC filings entirely"
    ],
    "answer": 0,
    "explain": "Per Day 32, the planner-worker-composer due-diligence agent cut initial screening from 45 minutes to 8 minutes per company, letting the firm screen 200+ more companies per month. Human review remained mandatory before client-facing output."
  },
  {
    "stem": "Why is the Action layer, not the Intelligence layer, usually the bottleneck for research agents?",
    "options": [
      "Research agents deliberately use weaker models",
      "Messy inputs (HTML tables with merged cells) cause misreads and parsing failures, so better data-extraction tooling beats a better model",
      "The Intelligence layer never fails in practice",
      "Research agents run so few steps that model quality is irrelevant"
    ],
    "answer": 1,
    "explain": "Day 32 concludes that for research agents tool quality is the bottleneck. Failures like misread financial tables, fabricated metrics, and HTML parsing errors are fixed with better tooling (convert tables to JSON, require citations, run specialized parsers before the LLM) — 'better tooling outperforms a better model on messy data.'"
  },
  {
    "stem": "The five agent layers, from bottom to top, are:",
    "options": [
      "Intelligence, Action, Governance, Orchestration, Economics",
      "Action, Intelligence, Orchestration, Governance, Economics",
      "Governance, Action, Intelligence, Economics, Orchestration",
      "Economics, Orchestration, Governance, Action, Intelligence"
    ],
    "answer": 0,
    "explain": "The five layers: Intelligence (the model doing reasoning), Action (tools and protocols), Governance (controls that bound behavior), Orchestration (the pattern sequencing intelligence + action), and Economics (the cost model vs a human baseline)."
  },
  {
    "stem": "Which layer answers 'which model runs, in what order, and when to retry or escalate'?",
    "options": [
      "Intelligence",
      "Action",
      "Governance",
      "Orchestration"
    ],
    "answer": 3,
    "explain": "Orchestration is the pattern that sequences intelligence + action — single-agent loops, planner-worker, supervisor-worker — deciding execution order, retries, and escalation. Governance instead bounds what the agent is allowed to do."
  },
  {
    "stem": "The Economics layer of the agent stack primarily deals with:",
    "options": [
      "Security and compliance",
      "Tool selection and execution",
      "The cost model — per-task cost vs a human baseline, and latency/throughput/cost tradeoffs",
      "Multi-agent communication protocols"
    ],
    "answer": 2,
    "explain": "Economics is the cost model: per-task cost vs human labor, which model to use (fast/cheap vs slow/powerful), and latency-vs-throughput tradeoffs. Klarna's ~20x per-ticket cost drop is an Economics-layer result."
  },
  {
    "stem": "Klarna's early agent apologized for problems that weren't Klarna's fault after several turns. Which layer did this failure originate in, and where was it fixed?",
    "options": [
      "It originated in Action and was fixed by adding a new API",
      "It originated in the Intelligence layer (model output/tone) but was fixed at the Governance layer — a human-review step for threads with more than three complaint signals",
      "It originated in Orchestration and was fixed by adding more sub-agents",
      "It originated in Economics and was fixed by switching to a cheaper model"
    ],
    "answer": 1,
    "explain": "This 'tone drift' is an Intelligence-layer defect (model output), but the fix was applied at the Governance layer: a human reviews and approves or edits any conversation with more than three complaint signals before it is sent."
  },
  {
    "stem": "What is Capsule?",
    "options": [
      "A managed cloud GPU rental marketplace",
      "A Python library for quantizing model weights",
      "A remote development and application streaming platform — you stay on your laptop while terminals, editors, and desktops run on remote hardware and stream back",
      "A Kubernetes distribution you install on your own cluster"
    ],
    "answer": 2,
    "explain": "Capsule is a remote development and application streaming platform for GPU fleets. The CPU, GPU, RAM, and disk live on remote machines; terminals, VS Code, Cursor, and full desktops run there and stream back to your laptop. Only the CLI runs locally."
  },
  {
    "stem": "Which statement about Capsule's default connection methods is correct?",
    "options": [
      "capsule term defaults to the SshRTC data channel (SSH over WebRTC); capsule ssh defaults to direct TCP SSH",
      "Both capsule term and capsule ssh default to direct TCP SSH",
      "capsule term defaults to direct SSH; capsule ssh defaults to SshRTC",
      "Both default to SshRTC and neither can use direct SSH"
    ],
    "answer": 0,
    "explain": "Per USAGE.md, capsule term (and code/cursor) use the SshRTC data channel by default, so the remote needs no public port. capsule ssh uses a direct TCP SSH connection by default. Add --direct to any command to force direct SSH."
  },
  {
    "stem": "Capsule's default connection method, SshRTC, carries SSH traffic over what transport?",
    "options": [
      "A raw public TCP port on the remote",
      "A WebRTC data channel (no public port needed)",
      "An HTTPS REST API",
      "gRPC"
    ],
    "answer": 1,
    "explain": "SshRTC tunnels SSH through a WebRTC data channel, so the remote machine never needs a publicly reachable port and NAT traversal 'just works.' Use --direct to force a traditional TCP SSH connection instead."
  },
  {
    "stem": "A corporate proxy is mangling WebRTC so capsule term hangs. How do you force a plain TCP SSH connection?",
    "options": [
      "Run capsule connect --tcp",
      "Set the environment variable CAPSULE_TCP=1",
      "Add the --direct flag (e.g. capsule term <tag> --direct)",
      "There is no fallback; SshRTC is mandatory"
    ],
    "answer": 2,
    "explain": "Adding --direct bypasses the SshRTC (WebRTC) data channel for a direct TCP SSH connection — the documented fallback when WebRTC fails or for clean port-forwarding. First run capsule session endall to reset connection state, then retry."
  },
  {
    "stem": "Where does the Capsule CLI store its config, cached token, and SSH keys?",
    "options": [
      "In ~/.capsule/ on every OS",
      "In /etc/capsule/ shared across all users",
      "macOS: $HOME/Library/Application Support/Capsule/; Windows: %APPDATA%\\capsule (holding capsule.conf, capsule_rsa/.pub, rclone.conf)",
      "In the current working directory"
    ],
    "answer": 2,
    "explain": "There is no ~/.capsule/. Capsule uses the OS config directory — $HOME/Library/Application Support/Capsule/ on macOS, %APPDATA%\\capsule on Windows — holding capsule.conf, the auto-generated capsule_rsa/capsule_rsa.pub keypair, and rclone.conf. The Azure B2C token is cached alongside (in the macOS Keychain where available)."
  },
  {
    "stem": "How does capsule auth login authenticate you?",
    "options": [
      "It authenticates against GitHub using your GH_TOKEN",
      "It reads a static API key from capsule.conf",
      "It opens a browser to the Azure B2C login and caches a token, with a manual-token fallback (prints a URL) for headless sessions",
      "It exchanges SSH keys directly with each node"
    ],
    "answer": 2,
    "explain": "capsule auth login runs the Azure B2C browser flow and caches a token; when no browser is available it falls back to a manual token flow (prints https://oxmiq.ai/oxcapsule/auth), or you can set CAPSULE_AUTH_TOKEN. GH_TOKEN is only for install/updates and --repo access, never runtime auth."
  },
  {
    "stem": "What is the difference between an 'environment' and a 'customer' in Capsule?",
    "options": [
      "The environment is a backend deployment (prod/public/dev/demo — endpoint + B2C tenant); the customer is the fleet selector inside it that scopes which machines capsule list shows",
      "The environment is a cluster of GPU machines; the customer is the billing account",
      "They are two names for the same setting",
      "The environment picks a GPU vendor; the customer picks a region"
    ],
    "answer": 0,
    "explain": "An environment is a backend deployment set with capsule env set — it selects the API endpoint and Azure B2C tenant, NOT a cluster of machines. The customer selector (capsule config customer set; micc default, plus modelhosting/oneplay/cree8) scopes which fleet appears in capsule list."
  },
  {
    "stem": "Why does switching environments with capsule env set force a fresh capsule auth login?",
    "options": [
      "It resets the customer override back to the default",
      "The auth token is scoped per environment and different environments use different Azure B2C tenants",
      "Any active sessions expire the moment you change environments",
      "Switching environments re-installs the CLI binary"
    ],
    "answer": 1,
    "explain": "The token is scoped to an environment, and environments (e.g. public vs prod) use different B2C tenants — your prod account is not your public account. So capsule env set must be followed by a fresh capsule auth login."
  },
  {
    "stem": "capsule list is empty or shows the wrong machines. What should you check FIRST?",
    "options": [
      "The GPU driver version on each node",
      "Your ~/.ssh/known_hosts file",
      "capsule env show and capsule config customer show",
      "The benchmark results dashboard"
    ],
    "answer": 2,
    "explain": "Which machines you see is decided by two settings: the environment (backend/tenant) and the customer selector (the fleet inside it). A wrong or empty capsule list almost always traces to one of them, so capsule env show and capsule config customer show are the first commands to run."
  },
  {
    "stem": "In Capsule's vocabulary, what is the relationship between a config-tag, a unique ID, and a machine?",
    "options": [
      "A config-tag IS a single machine",
      "They are all the same thing",
      "A config-tag refers to hardware; a unique ID refers to software",
      "A config-tag names a machine pool/class (any available member); a unique ID targets one specific physical machine; a machine is the box the scheduler hands you"
    ],
    "answer": 3,
    "explain": "A config-tag is a pool/class name — the scheduler hands you any available member. A unique ID (e.g. boostergold461), used with -u/--unique, pins one specific physical machine. Run capsule list to see pools and capsule list --all to reveal unique IDs."
  },
  {
    "stem": "How do you list every NVIDIA machine with at least 24 GB of VRAM?",
    "options": [
      "capsule list --all",
      "capsule list --gpu nvidia --min-vram 24",
      "capsule list | grep nvidia",
      "capsule list --filter \"vendor=nvidia,vram>=24\""
    ],
    "answer": 3,
    "explain": "Filtering uses a comma-separated key=value / key>=value grammar with AND semantics: capsule list --filter \"vendor=nvidia,vram>=24\". There is no --gpu or --min-vram flag. On PowerShell, quote the whole filter and use capsule (not the cap shortener) so > isn't treated as redirection."
  },
  {
    "stem": "How do you target one specific physical machine instead of any available machine from a pool?",
    "options": [
      "A config tag always targets one specific machine",
      "Use its unique ID with -u/--unique (reveal unique IDs via capsule list --all)",
      "Pass --gpus with the exact GPU model to pin the box",
      "Add --refresh to lock the current machine"
    ],
    "answer": 1,
    "explain": "A config tag hands you any available machine from a pool. To pin one specific box, reveal unique IDs with capsule list --all and target it with -u/--unique (e.g. -u boostergold461). USAGE.md notes capsule ssh --unique boostergold461 as the pattern."
  },
  {
    "stem": "Before starting heavy work on a machine, why run capsule list --users?",
    "options": [
      "To renew your reservation on the machine",
      "To list which users are permitted to log in to each machine",
      "To see which machines already have active user sessions, so you don't disrupt someone else's work",
      "To display the billing owner of each machine"
    ],
    "answer": 2,
    "explain": "Capsule has no lease/reservation system — you just connect and use a machine. capsule list --users is the sniff test showing which machines have active users, so you can pick a free one instead of blowing away a colleague's session."
  },
  {
    "stem": "Capsule has no lease/reservation system. How do you manage and clean up your connections when done?",
    "options": [
      "capsule session list shows your active SshRTC tunnels; capsule session end closes one (by unique id, port, or session id) and capsule session endall closes them all",
      "capsule lease release returns the machine to the pool",
      "capsule disconnect --all ends every reservation",
      "Nothing to clean up — sessions expire on a timer"
    ],
    "answer": 0,
    "explain": "You don't reserve machines — you connect and the machine is yours while the session is open, so cleanup is your responsibility. capsule session list enumerates your SshRTC data-channel tunnels; session end closes a specific one and session endall closes them all without disturbing others."
  },
  {
    "stem": "What are the exact four GH_TOKEN scopes required to install Capsule?",
    "options": [
      "repo, read:org, workflow, user",
      "repo, read:org, gist",
      "repo, read:user, admin:org",
      "repo, read:org, workflow, write:discussion"
    ],
    "answer": 0,
    "explain": "The four scopes are repo (read the private tap and release downloads), read:org (verify org membership), workflow (workflow-triggered releases), and user (read the profile for identity). GH_TOKEN is used only at install/update time — runtime auth is Azure B2C."
  },
  {
    "stem": "Why does the Capsule install include rclone?",
    "options": [
      "It is the GPU driver Capsule needs to run benchmarks",
      "It is a Python package manager for model dependencies",
      "It is a terminal multiplexer that keeps sessions alive",
      "Capsule uses it under the hood for cloud storage mounts (OneDrive); you never call it directly but it must be on PATH"
    ],
    "answer": 3,
    "explain": "rclone is a file-transfer tool Capsule uses for OneDrive cloud-storage mounts. capsule auth storage and the automatic OneDrive mount drive it — you never invoke it directly — but it must be on PATH. The brew formula installs it automatically on macOS."
  },
  {
    "stem": "What is cap in the Capsule CLI?",
    "options": [
      "A separate, lighter client that supports only a subset of commands",
      "A shortcut for capsule, created during install as a symlink (Unix/macOS) or batch wrapper (Windows) — cap list == capsule list",
      "A command that only exists on Windows",
      "There is no shortcut; you must always type capsule"
    ],
    "answer": 1,
    "explain": "cap is a shortcut alias for capsule created automatically at install; the commands are equivalent. One caveat: on PowerShell, cap list --filter with a > breaks, so use capsule and quote the filter argument there."
  },
  {
    "stem": "The Capsule access token has a TTL of about 60 minutes. What happens automatically when it expires?",
    "options": [
      "All commands stop working immediately",
      "You must re-run capsule auth login every hour",
      "It is silently refreshed using the refresh token (~30-day TTL)",
      "The control plane automatically extends the same token forever"
    ],
    "answer": 2,
    "explain": "When the ~60-minute access token expires, Capsule uses the refresh token (~30 days) to mint a new one without a browser. Only when the refresh token itself expires must you re-run capsule auth login."
  },
  {
    "stem": "capsule status shows a valid token but every command returns 'unauthorized'. What is the most likely cause?",
    "options": [
      "The control plane is permanently down",
      "The system clock is skewed more than ~5 minutes from UTC, so a locally-valid token fails server-side validation",
      "The machine you want to reach is offline",
      "rclone is missing from PATH"
    ],
    "answer": 1,
    "explain": "This is clock skew: if the system clock is more than ~5 minutes ahead of UTC the access token is rejected server-side even though it looks valid locally. Diagnose with date -u against real UTC; fix by syncing NTP (sudo sntp -sS time.apple.com on macOS, w32tm /resync on Windows)."
  },
  {
    "stem": "What is the post-install command sequence to verify a working Capsule install?",
    "options": [
      "capsule init then capsule verify --all",
      "capsule --version, then capsule auth login, then capsule status",
      "capsule check, then capsule login, then capsule ping",
      "capsule doctor, then capsule test"
    ],
    "answer": 1,
    "explain": "Run capsule --version (confirm the binary is on PATH), capsule auth login (complete the Azure B2C browser flow), then capsule status (confirm identity + token expiry). Part 4 adds capsule auth storage and capsule list | head to confirm OneDrive and fleet visibility. There is no capsule init/verify/check/doctor."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 35 · Consolidation](index.md)

-   __Back to the week__

    [Week 7 — Bridge: Theory Meets Tooling overview](../index.md)

-   __Continue the curriculum__

    [Day 36 · Connecting](../../week-08/module-1/index.md)

</div>
