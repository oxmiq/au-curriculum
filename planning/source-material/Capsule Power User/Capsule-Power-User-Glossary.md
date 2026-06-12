# Capsule Power-User — Glossary

*Vocabulary reference for Weeks 8–9. Each term has a one-line "field definition," a paragraph of explanation, and a cross-reference to the Lab Guide module or Cheatsheet section where it is introduced. Use this to look things up during the labs.*

---

### `--direct`
**Field:** A connection flag that bypasses Capsule's SshRTC overlay and connects via direct TCP.

Lower latency than SshRTC, but only works when both endpoints have routable connectivity (no symmetric NAT, no restrictive firewall). Use for low-latency interactive work when you control the network; default (SshRTC) for laptops on hotel/coffee-shop networks. *Introduced: Day 38.*

### `--filter`
**Field:** A query expression on `capsule list` that selects machines by attribute: `vendor`, `gpu`, `os`, `vram`, `memory`, `cores`, `ci`.

Operators include `=`, `>=`, `<=`. Vendor values: `nvidia`, `tenstorrent`, `amd`, `intel`. Example: `--filter "vendor=nvidia,vram>=80"` returns H100-class boxes. PowerShell users must quote the expression — `>` is redirection in PS. *Introduced: Day 37.*

### Azure B2C
**Field:** Microsoft's external-identity service that Capsule uses for authentication, with per-environment tenants.

`prod` uses `mihirainfra.b2c`; `public` uses `oxcapsule.b2c`; `dev` and `demo` use their own. Switching environments means switching tenants, which means switching user registries — hence the forced re-auth on `capsule env set`. *Introduced: Day 36.*

### `capsule auth`
**Field:** Sub-command family for authentication: `login`, `logout`, `status`, `storage`, `token`.

`login` opens a browser flow (with a manual-token fallback at `oxmiq.ai/oxcapsule/auth` for headless boxes). `status` shows identity + token expiry. `storage` authorizes the OneDrive mount. For CI/headless: `export CAPSULE_AUTH_TOKEN=…`. *Introduced: Day 36.*

### `capsule benchmark`
**Field:** Runs a structured load test against a model on a Capsule machine, reporting TTFT, ITL, TPS, and throughput.

Key flags: `--model`, `--concurrency`, `--tp`, `--quantization`, `--backend` (vLLM / SGLang / TRT-LLM). The output uses the exact Phase-1 vocabulary (TTFT, ITL, TPS) from Week 4. *Introduced: Day 41.*

### `capsule chat`
**Field:** An interactive REPL connected to a model running on a Capsule machine; used for *qualitative* evaluation after benchmarking.

Where `benchmark` answers "how fast?", `chat` answers "did quantization break anything?" Use a structured prompt set (factual recall, math, code, refusal) to spot regressions. *Introduced: Day 43.*

### `capsule cleanup`
**Field:** The "fix Capsule's local state" command. Clears stale connection tracking, cached fleet data, and orphaned tunnels.

Always the *first* thing to try when `capsule list` shows wrong machines or `capsule term` hangs. Cheap, safe, idempotent. *Introduced: Day 40.*

### `capsule code`, `capsule cursor`, `capsule claude`
**Field:** Connect commands that open VS Code Remote-SSH / Cursor Remote-SSH / Claude Code Desktop against a Capsule machine, respectively.

Each one wires the Remote-SSH config to the SshRTC overlay (or direct, with `--direct`) so the editor treats the remote box as a normal SSH host. *Introduced: Day 38.*

### `capsule config customer`
**Field:** Selects the customer-context fleet: `micc` (default), `modelhosting`, `oneplay`, `cree8`, etc.

The customer context is *the* most common cause of "I see the wrong machines." Always check it before debugging anything else. `capsule config customer unset` returns to the environment's default. *Introduced: Day 37.*

### `capsule docker`
**Field:** Launches a container on a Capsule machine with the GPU exposed and `nvidia-container-toolkit` (or vendor equivalent) pre-wired.

Saves you the setup work of "container can see the GPU." Useful for portability — your benchmark recipe runs identically on any Capsule box. *Introduced: Day 39.*

### `capsule env`
**Field:** Selects the deployment environment: `prod`, `public`, `dev`, `demo`. `capsule env set <name>` switches; `capsule env show` displays current.

Switching environments forces re-authentication because each environment uses a different Azure B2C tenant with a separate user registry. *Introduced: Day 37.*

### `capsule exec`
**Field:** Runs a one-off command on a Capsule machine non-interactively and returns its exit code.

Pair with `capsule term` (interactive shell). Rule of thumb: `term` for exploration, `exec` for scripting and automation. *Introduced: Day 38.*

### `capsule list`
**Field:** Lists machines in the current customer/environment fleet. Flags: `--all` (include unique IDs), `--users` (who's connected), `--json`, `--filter`.

Output by default is grouped by config tag (e.g., `NV-3060-04-1`). Add `--all` to see unique IDs you'd need for `-u`-style routing. *Introduced: Day 37.*

### `capsule mcp`
**Field:** Exposes Capsule CLI operations as an MCP (Model Context Protocol) server consumable by AI assistants.

`capsule mcp --output` writes the manifest. Any MCP-aware client (Claude Desktop, Cursor, VS Code Copilot) can then call Capsule operations as tools. Connect: this is the same MCP protocol covered in Week 7 Day 32 — the Capsule CLI is now an *Action layer* for an agent. *Introduced: Day 44.*

### `capsule schedule`
**Field:** Submits a long-running job (benchmark, training, eval) to run server-side without holding an interactive terminal.

Use whenever a task is longer than ~30 min: SSH drops, laptop sleeps, and benchmark crashes all stop ruining your day. Sub-commands: `start`, `status`, `logs`, `cancel`. *Introduced: Day 44.*

### `capsule status`
**Field:** Reports the local Capsule client's identity, env, customer context, and connection health in one snapshot.

The first command in the daily-loop discipline (`status → env show → customer show → list → term`). *Introduced: Day 36.*

### `capsule stream`
**Field:** Opens a WebRTC desktop or single-app stream from a Capsule machine to your local display.

Used when you need a *graphical* workload on a remote GPU — game launchers, GUI debuggers, 3D viewers. WebRTC outperforms VNC/RDP for high-frame-rate GPU content because it negotiates codecs end-to-end. *Introduced: Day 39.*

### `capsule term`
**Field:** Opens an interactive remote shell to a Capsule machine, default via SshRTC overlay.

The workhorse connection command. Routing: `capsule term <config-tag>` (any matching machine) or `capsule term -u <unique-id>` (specific machine). *Introduced: Day 38.*

### Config tag (routing-by-tag)
**Field:** A human-readable group identifier (e.g., `NV-3060-04-1`) used to route to *any* machine matching the tag.

Tag-routing is the right choice when "any L4 machine" is fine. The wrong choice when you've set up state on a specific machine — use `-u` routing for that. *Introduced: Day 38.*

### Customer context
**Field:** The fleet partition selected by `capsule config customer`. Determines which machines `capsule list` returns.

Distinct from environment. You can be in `prod` env with `modelhosting` customer, or `prod` env with `micc` customer — and see entirely different fleets. *Introduced: Day 37.*

### Daily-loop discipline
**Field:** The canonical start-of-day sequence: `capsule status` → `capsule env show` → `capsule config customer show` → `capsule list --users` → `capsule term <tag>`.

Running this every morning catches 90% of "why don't I see the machines I expect?" before you waste time on it. End-of-day: `capsule cleanup`. *Introduced: Day 36 (Cheatsheet daily-loop panel).*

### Dotfile passthrough
**Field:** Mechanism that copies a curated set of local dotfiles (`.vimrc`, `.zshrc`, `.gitconfig`, etc.) to the remote machine on first connect.

Lets you carry your editor/shell config to a fresh GPU box without scping each file. Configured via Capsule's dotfile manifest. *Introduced: Day 39.*

### Environment (Capsule env)
**Field:** A top-level deployment target: `prod` (internal prod), `public` (external/partner), `dev`, `demo`.

Each env has its own B2C tenant, customer namespace, and fleet. Always confirm `capsule env show` before assuming you're looking at production data. *Introduced: Day 37.*

### Manifest (MCP manifest)
**Field:** A JSON document describing the tools an MCP server exposes — names, descriptions, parameter schemas, return types.

`capsule mcp --output` writes this manifest. The model reads the description fields to decide which tool to call. *Introduced: Day 44. Cross-reference: Week 7 Day 32.*

### OneDrive mount
**Field:** Persistent, cross-machine file storage backed by the user's OneDrive, exposed as a local path on every Capsule machine.

Right choice for files you want to persist across machine swaps. Wrong choice for one-off transfers (use `scp`) or for huge datasets (use customer-specific block storage). *Introduced: Day 39.*

### `scp` (over Capsule)
**Field:** Standard SCP from your local box to a Capsule machine, with the connection routed through the SshRTC overlay automatically.

The right choice for one-off file transfers. Wrong choice for files you'll need on the *next* machine too (use OneDrive mount for that). *Introduced: Day 39.*

### Session limits
**Field:** Per-user caps on the number of concurrent Capsule connections (term/code/cursor/claude), enforced server-side.

Hit your limit, you get a clean error and can `capsule status` to see what's open. The limits exist to keep one engineer from accidentally squatting on a fleet during testing. *Introduced: Day 38.*

### SshRTC
**Field:** Capsule's WebRTC-based SSH overlay; tunnels SSH inside a peer-to-peer WebRTC data channel.

Solves the "client behind NAT, server behind firewall" problem without VPN setup. Slight latency overhead vs. `--direct` TCP; near-zero setup cost. *Introduced: Day 38.*

### Tag vs unique-ID routing
**Field:** The two ways to address a machine: config-tag (`capsule term NV-3060-04-1`, any matching machine) or unique-ID (`capsule term -u <id>`, specific machine).

Tag for "any of these is fine." Unique-ID for "I've been working on *this* one." Misrouting by tag when you needed unique-ID is the single most common reproducibility bug in benchmark work. *Introduced: Day 38.*

### Tenant
**Field:** The Azure B2C identity scope. In Capsule context: `prod` ↔ `mihirainfra.b2c`, `public` ↔ `oxcapsule.b2c`, etc.

Different tenants = different user databases. A user account in `prod` does not exist in `public` unless explicitly provisioned there. *Introduced: Day 36.*

### Tool manifest (Capsule MCP)
**Field:** The MCP-format JSON that `capsule mcp --output` emits, describing every Capsule CLI command as a callable tool.

When an AI assistant connects to `capsule mcp`, it parses this manifest and gains the ability to call Capsule operations as tools — list machines, deploy a model, run a benchmark — under user-scoped permissions. *Introduced: Day 44.*

### WebRTC (in Capsule context)
**Field:** The peer-to-peer media + data protocol used both for SshRTC (shell tunneling) and `capsule stream` (desktop streaming).

Same underlying technology powers two different Capsule features, which is why both work through firewalls without VPN setup. *Introduced: Day 38 (SshRTC) and Day 39 (stream).*

---

## Concept-graph anchors

Glossary terms map onto `docs/kb/concepts.json` (v0.1). IDs you'll see referenced from facilitator material:

| Concept-graph ID | Glossary term |
|---|---|
| `capsule.auth.b2c` | Azure B2C |
| `capsule.fleet.env` | Environment |
| `capsule.fleet.customer` | Customer context |
| `capsule.connect.sshrtc` | SshRTC |
| `capsule.connect.direct` | `--direct` |
| `capsule.connect.tag_vs_uid` | Tag vs unique-ID routing |
| `capsule.bench.runner` | `capsule benchmark` |
| `capsule.eval.chat` | `capsule chat` |
| `capsule.ops.schedule` | `capsule schedule` |
| `capsule.ops.mcp` | `capsule mcp` |
| `capsule.diag.daily_loop` | Daily-loop discipline |
