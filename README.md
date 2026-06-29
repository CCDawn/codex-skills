# Dawn Codex Skills

A local skill library focused on competition-driven research workflows, behavior-gated implementation, and persistent project memory.

The default operating model for this repo installs to one local live surface:

- `~/.codex/skills/<ccdawn-skill-name>` for the live skill directory Codex can load at runtime

An optional secondary surface is still available when you explicitly need it:

- `~/.agents/skills/<ccdawn-skill-name>` for the local skill catalog surface used by some app setups

Keep the folder name identical to the `name` field, using the `ccdawn-` namespace in `SKILL.md`, and validate the installed live Codex skill after updates.

[中文说明](README.zh-CN.md)

## Included skills

### Engineering

- **`ccdawn-brt`**  
  The Behavior / Review / Test workflow entry skill. It proactively infers what the user likely means, offers candidate intents and high-signal questions with recommendations, and turns aligned intent into behavior contracts, review lenses, test anchors, and next-stage routing.

- **`ccdawn-planning`**
  The planning-stage skill for turning aligned requirements into an implementation plan before code changes.

- **`ccdawn-task-splitting`**
  The task-splitting-stage skill for breaking an accepted plan into reviewable, independently verifiable work units.

- **`ccdawn-bdd-tdd-development`**
  The development-stage skill for behavior-anchored implementation with TDD discipline.

- **`ccdawn-completion-summary`**
  The completion-stage skill for fresh verification evidence, requirement comparison, and concise handoff summaries.

- **`ccdawn-pr-review`**
  The PR-review-stage skill for checking a PR, branch, commit range, or local diff against aligned requirements, task evidence, regression risk, and merge readiness.

- **`ccdawn-bug-review`**
  A CCDawn bug-review adapter that reuses `systematic-debugging` and `root-cause-tracing`, then summarizes evidence, root-cause state, impact, and the next fix route.

- **`ccdawn-evaluation`**
  A CCDawn evaluation adapter used only when no more specific review, debugging, planning, verification, feedback, or goal skill already owns the judgment.

- **`ccdawn-dawn-agent-html-memory`**  
  A persistent project-memory skill for creating and maintaining `.docs/project-memory/` inside real software projects. It supports shared multi-session work lanes under `.docs/project-memory/lanes/`, a generated HTML overview that aggregates those lanes, and a root `PROJECT_MEMORY.html` shortcut for humans.

- **`ccdawn-goal-loop`**  
  A goal-execution skill for turning an objective into a verified contract with evidence, constraints, allowed scope, next-step rules, and stop-on-blocker reporting.

### Research

- **`ccdawn-competition-research-lifecycle`**  
  An end-to-end workflow skill for research competitions and benchmark-style projects. It covers task framing, data preparation, literature and solution research, baseline setup, training and experimentation, analysis and ablation, paper writing, and submission packaging.

  This skill treats `ccdawn-brt` as a governance layer for defining phase goals, review points, and acceptance checks. It ships with a reference guide, a tighter response contract, and copy-ready phase templates.

### Competition

- **`ccdawn-huawei-nslb-score-loop`**  
  A project-specific score loop skill for the Huawei Algorithm Challenge 37 NSLB workspace. It coordinates isolated worker lanes, local proxy evidence, baseline promotion, package registration, and online score feedback calibration.

### Creative

- **`ccdawn-creative-toolbox`**  
  A context-aware creative ideation skill for concept collision, divergent thinking, naming, paradigm exploration, unusual alternatives, product ideas, research concepts, and surprising but useful options.

## Management format

Published skills use one consistent shape:

```text
skills/<bucket>/<ccdawn-skill-name>/
  SKILL.md
  agents/openai.yaml        # optional but recommended for Codex slash-command metadata
  references/               # optional supporting references, templates, ledgers, or schemas
  scripts/                  # optional helper tools used by the skill
```

Rules:

- `skill-name` must match the `name` field in `SKILL.md`.
- Every catalog change should update this README, `README.zh-CN.md`, the bucket README, and `.claude-plugin/plugin.json`.
- Install into `~/.codex/skills/<ccdawn-skill-name>` as real copied directories by running `python scripts/install_codex_library.py`.
- Avoid installing the same skill into both `~/.codex/skills` and `~/.agents/skills` unless duplicate slash-command entries are intentional.

## Structure

```text
.claude-plugin/
  plugin.json
AGENTS.md
CLAUDE.md
skills/
  competition/
    README.md
    ccdawn-huawei-nslb-score-loop/
  creative/
    README.md
    ccdawn-creative-toolbox/
  engineering/
    README.md
    ccdawn-dawn-agent-html-memory/
    ccdawn-brt/
    ccdawn-planning/
    ccdawn-task-splitting/
    ccdawn-bdd-tdd-development/
    ccdawn-completion-summary/
    ccdawn-pr-review/
    ccdawn-bug-review/
    ccdawn-evaluation/
    ccdawn-goal-loop/
  research/
    README.md
    ccdawn-competition-research-lifecycle/
scripts/
  install_codex_library.py
```

## Quickstart

Install the skills into the default local Codex surface as real folders:

```bash
python scripts/install_codex_library.py
```

That is the default, recommended workflow for this repo. It copies every published skill into:

```text
~/.codex/skills/<ccdawn-skill-name>
```

The install script also enforces that:

- the skill folder name matches the `name` field in `SKILL.md`
- installed Codex skills are copied as real directories, not symlinks or junctions
- installed live skills are validated when the local Codex `quick_validate.py` helper is available

Installing the same skill into both `.codex/skills` and `.agents/skills` can create duplicate slash-command entries in Codex. Only use the `.agents` target when you explicitly need that extra catalog copy.

Install only selected skills:

```bash
python scripts/install_codex_library.py --skill ccdawn-brt --skill ccdawn-dawn-agent-html-memory
```

Install only to the live Codex directory:

```bash
python scripts/install_codex_library.py --agent codex
```

Install only to the local slash-command catalog directory:

```bash
python scripts/install_codex_library.py --agent agents
```

Install to Claude's global skill folder only when you explicitly need it:

```bash
python scripts/install_codex_library.py --agent claude
```

Install to Codex, `.agents`, and Claude:

```bash
python scripts/install_codex_library.py --agent all
```

Install to both Codex and `.agents` only when you explicitly want both copies:

```bash
python scripts/install_codex_library.py --agent codex-agents
```

## Slash-command troubleshooting

If a slash-command entry is missing or duplicated, use this checklist before changing prompts or folder names:

1. Inspect the installed live copy in `~/.codex/skills/<ccdawn-skill-name>`, not just the repo copy.
2. Check whether an extra `~/.agents/skills/<ccdawn-skill-name>` copy exists. Keeping both copies can create duplicate slash-command entries.
3. Check `agents/openai.yaml` in the live installed copy and keep it aligned with the minimal `interface:` pattern already used by working skills in this repo.
4. If this repository is the active trusted workspace, also check `.claude-plugin/plugin.json`, because the repo-local manifest can affect visible entries.
5. Restart Codex and verify from a fresh thread before concluding that a metadata change did not load.

## Optional dev shortcut

For temporary local development only, you can still link the skills into `~/.claude/skills`:

On macOS/Linux:

```bash
bash scripts/link-skills.sh
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\link-skills.ps1
```

Do not treat the link flow as the formal publish/install path for this repository.

The repo metadata index lives at:

```text
.claude-plugin/plugin.json
```

The skills themselves live under:

```text
skills/
```

After installing or updating a live skill, restart the client so it reloads local skills.

## Development

- [Contributing guide](CONTRIBUTING.md)
- [MIT License](LICENSE)

## Usage

Invoke the skills in chat with prompts such as:

- `Use ccdawn-competition-research-lifecycle to plan this benchmark project`
- `Help me run this competition through a full research lifecycle`
- `Use ccdawn-goal-loop to turn this objective into a verified execution contract`
- `Use ccdawn-pr-review to review this PR before merge`
- `Use ccdawn-bug-review to wrap systematic-debugging for this regression`
- `Use ccdawn-evaluation to evaluate this workflow after checking for a more specific skill`
- `Use ccdawn-huawei-nslb-score-loop to prepare an NSLB epoch and gate child results`
- `Use ccdawn-creative-toolbox to generate new concept cards from this context`
- `Initialize project memory for this repo`
- `Use ccdawn-dawn-agent-html-memory to initialize project memory for this repo as a frontend project`

This repository is intentionally shaped like a local skill repo, not a marketplace-installed plugin.
