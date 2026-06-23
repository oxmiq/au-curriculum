# Oxmiq × Andhra University — Internship Curriculum

Your personal learning environment for the 10-week program. You'll **fork** this repo, run the lesson site locally, and use **oxtutor** as your on-demand tutor.

## Quickstart

```bash
# 1. Fork this repo on GitHub, then clone YOUR fork
git clone git@github.com:<your-username>/au-curriculum.git
cd au-curriculum

# 2. Run the site locally
pip install mkdocs mkdocs-material
mkdocs serve            # open http://localhost:8000

# 3. Stay current with new lessons (safe — you only ever write to your own folders)
git pull upstream main
```

Open the **Curriculum Map** to see every concept, what you've passed, and what unlocks next. Click a concept to read its lesson, then take the canonical knowledge check.

## Working with oxtutor

oxtutor is your tutor: it re-explains lessons, generates practice knowledge checks, and records your progress. It only ever writes to `practice/`, `progress/`, and `scratch/` — your lessons stay clean for `git pull`. See `agents.md` for how it navigates this repo.

### Installing oxtutor

oxtutor runs as a Capsule agent, so you reach it through the `capsule` CLI and the first run installs everything for you. There's no wheel to download and you don't need access to any Oxmiq source repos.

```bash
# 1. Sign in to Capsule (one time — Oxmiq sets up your login during onboarding)
capsule auth login

# 2. First run installs the oxtutor runtime automatically, then answers your prompt
capsule agent oxtutor -p "explain TTFT"
```

The first `capsule agent oxtutor` run downloads the oxtutor runtime from Oxmiq's binaries channel using your Capsule login — no GitHub token, no manual install — and keeps it up to date on later runs. If you're not signed in, it stops and asks you to run `capsule auth login` first.

To force an update to the latest runtime:

```bash
capsule agent oxtutor update
```

### Connecting to the model

oxtutor is a thin client: it needs a model **endpoint**, a **model name**, and a **key**, and it fails fast if any is missing. You provide all three explicitly — either as environment variables or as CLI flags (a flag overrides its environment variable). Oxmiq gives you these values during onboarding.

| What | Environment variable | CLI flag |
|------|----------------------|----------|
| Endpoint | `OXMIQ_AGENT_API_BASE` | `--api-base` |
| Model | `OXMIQ_AGENT_MODEL` | `--model` |
| Key | `OXMIQ_AGENT_API_KEY` | `--api-key` |

The simplest setup is to export the three variables once per shell session:

```bash
export OXMIQ_AGENT_API_BASE="<endpoint-from-onboarding>"
export OXMIQ_AGENT_MODEL="<model-from-onboarding>"
export OXMIQ_AGENT_API_KEY="<your-key-from-onboarding>"

capsule agent oxtutor -p "explain TTFT"
```

Or pass them inline on a single run (flags win over the environment):

```bash
capsule agent oxtutor \
  --api-base "<endpoint>" --model "<model>" --api-key "<your-key>" \
  -p "explain TTFT"
```

If any of the three is missing, oxtutor stops and tells you which one — it never guesses a default.

> **Coming soon — automatic setup.** Once student provisioning is live, `capsule auth login` will wire your endpoint, model, and personal key for you, and you won't set any of these by hand. Until then, use the explicit values from onboarding as shown above.

### Running it

From inside your fork, give oxtutor a prompt:

```bash
cd au-curriculum
capsule agent oxtutor -p "quiz me on this week's lesson"
```

It grounds its teaching in your actual lesson files and follows the project rules in `agents.md`.

## Layout

- `docs/lessons/` — the lessons + canonical knowledge checks (read-only; synced from upstream)
- `docs/kb/` — the curriculum map
- `docs/practice/`, `docs/progress/`, `scratch/` — yours; oxtutor writes here
- `agents.md`, `skills/` — how oxtutor is configured
