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

**Week 7 · Bridge: Theory Meets Tooling.** 16 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m5-canonical" data-kind="wrap-up" data-draw="16" data-lesson="Week 7 · Bridge: Theory Meets Tooling" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Klarna's agent system used which orchestration pattern?",
    "options": [
      "Single-agent loop",
      "Planner-worker",
      "Supervisor-worker",
      "Swarm / parallel sampling"
    ],
    "answer": 1,
    "explain": "Klarna used planner-worker: a central planner decomposed customer inquiries into subtasks (search, categorize, respond) that specialized workers executed."
  },
  {
    "stem": "The dominant governance control in Klarna's agent deployment was:",
    "options": [
      "Unrestricted tool access",
      "Human review in the loop for every response",
      "Output filtering + human escalation thresholds",
      "No governance — fully autonomous"
    ],
    "answer": 2,
    "explain": "Klarna's governance was output filtering (checking responses before showing to customers) combined with human escalation for high-risk or uncertain cases."
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
    "explain": "Claude Code and Cursor are single-agent harnesses: one model with a defined toolset runs the loop. Orchestration is minimal — it's all in the prompt and tool design."
  },
  {
    "stem": "For coding agents like Claude Code / Cursor, what makes their environment different from customer-service agents?",
    "options": [
      "They don't use tools",
      "They work in adversarial, stateful environments (codebases) where a wrong action can break things",
      "They require human approval for every action",
      "They cannot access the internet"
    ],
    "answer": 1,
    "explain": "Coding agents work in adversarial, stateful codebases — one wrong <code>rm -rf</code> or bad edit can cause real damage. This makes the Action layer especially critical."
  },
  {
    "stem": "The SemiAnalysis research agent improved throughput by screening how many companies per month?",
    "options": [
      "100",
      "500",
      "2,000",
      "10,000"
    ],
    "answer": 2,
    "explain": "SemiAnalysis's research agent screened ~2,000 companies per month — a massive throughput leap over manual research. The Action layer (web scraping, data processing) was often the bottleneck, not the Intelligence layer."
  },
  {
    "stem": "Capsule's 3-layer architecture is: CLI → Control Plane → Node Agents. What protocol connects CLI to Control Plane?",
    "options": [
      "Raw SSH",
      "WebRTC (SshRTC)",
      "HTTPS REST API",
      "gRPC"
    ],
    "answer": 2,
    "explain": "CLI connects to Control Plane via HTTPS REST API. The Control Plane coordinates, stores metadata, and routes. Node Agents connect back via WebRTC for interactive sessions."
  },
  {
    "stem": "In Capsule's architecture, where are authentication tokens stored after <code>capsule auth login</code> on macOS?",
    "options": [
      "In a config file in the project directory",
      "In the macOS Keychain",
      "In environment variables",
      "In ~/.capsule/config.json"
    ],
    "answer": 1,
    "explain": "Tokens are stored in the macOS Keychain for security. This keeps credentials out of config files that might be committed to version control."
  },
  {
    "stem": "In Capsule's vocabulary, what is the relationship between a config-tag, a node, and a machine?",
    "options": [
      "A config-tag IS a machine",
      "A node is a running instance; a machine is the physical/gce resource; a config-tag labels nodes",
      "They are all the same thing",
      "config-tag refers to hardware, node refers to software"
    ],
    "answer": 1,
    "explain": "A machine is the underlying resource (physical or cloud VM). A node is Capsule's running agent on that machine. A config-tag is the label you use to route commands to specific nodes."
  },
  {
    "stem": "undefined",
    "options": [
      "SSH is not secure enough",
      "WebRTC works through NAT/firewalls without port-forwarding and supports streaming",
      "WebRTC is faster than SSH",
      "SSH requires a separate key management system"
    ],
    "answer": 1,
    "explain": "WebRTC enables peer-to-peer connections that traverse NAT and firewalls — critical for connecting to machines in different network environments without complex port-forwarding."
  },
  {
    "stem": "What are the exact four GH_TOKEN scopes required for Capsule installation?",
    "options": [
      "repo, read:user, workflow",
      "repo, read:org, gist",
      "repo, read:user, admin:org",
      "repo, read:org, workflow, write:discussion"
    ],
    "answer": 0,
    "explain": "The four required scopes are: repo (full control of private repositories), read:user (read user profile data), workflow (update GitHub Actions workflows), and gist (create/manage gists)."
  },
  {
    "stem": "The Capsule access token has a TTL of approximately 60 minutes. What happens automatically when it expires?",
    "options": [
      "All commands stop working immediately",
      "The token is silently refreshed using the refresh token",
      "You must re-run capsule auth login",
      "The control plane automatically extends it"
    ],
    "answer": 1,
    "explain": "The access token is silently refreshed using the refresh token. However, if the refresh token itself expires, you must re-run <code>capsule auth login</code>."
  },
  {
    "stem": "If <code>capsule status</code> shows 'valid' but all commands return 'unauthorized', what is the most likely cause?",
    "options": [
      "The control plane is down",
      "The access token expired but refresh succeeded — need to re-authenticate",
      "The machine is offline",
      "There is a network connectivity issue"
    ],
    "answer": 1,
    "explain": "Status may report stale valid state from a cached token. The real issue is often an expired access token where the refresh also failed. Run <code>capsule auth login</code> to fix."
  },
  {
    "stem": "What command would you run to discover machines with NVIDIA GPUs having 24GB+ VRAM?",
    "options": [
      "capsule list --all",
      "capsule list --filter vendor=nvidia,vram>=24",
      "capsule list --gpu",
      "capsule list | grep nvidia"
    ],
    "answer": 1,
    "explain": "The filter flag uses key=value pairs: <code>capsule list --filter \"vendor=nvidia,vram>=24\"</code>. This returns only machines matching both criteria."
  },
  {
    "stem": "The five agent layers in order (from bottom to top) are:",
    "options": [
      "Intelligence, Action, Governance, Orchestration, Economics",
      "Action, Intelligence, Orchestration, Governance, Economics",
      "Governance, Action, Intelligence, Economics, Orchestration",
      "Economics, Orchestration, Governance, Action, Intelligence"
    ],
    "answer": 0,
    "explain": "The five layers: Intelligence (model + prompting), Action (tools), Governance (security + guardrails), Orchestration (multi-agent coordination), Economics (cost + latency tradeoffs)."
  },
  {
    "stem": "Which layer answers the question: 'which model runs, in what order, and when to retry or escalate?'",
    "options": [
      "Intelligence",
      "Action",
      "Governance",
      "Orchestration",
      "Economics"
    ],
    "answer": 3,
    "explain": "Orchestration is the control plane layer that coordinates multiple agents, decides execution order, handles retries, and manages escalation — the 'which model runs, when' question."
  },
  {
    "stem": "The Economics layer primarily deals with:",
    "options": [
      "Security and compliance",
      "Tool selection and execution",
      "Model selection, latency/throughput tradeoffs, cost optimization",
      "Multi-agent communication protocols"
    ],
    "answer": 2,
    "explain": "Economics layer covers: which model to use (fast/cheap vs slow/powerful), batching strategies, latency vs throughput tradeoffs, and cost optimization at the system level."
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
