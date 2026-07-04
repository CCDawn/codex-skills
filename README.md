# Dawn Codex Skills

A local skill library focused on competition-driven research workflows, behavior-gated implementation, and persistent project memory.

[中文说明](README.zh-CN.md)

## Install

Fastest path: copy a ready prompt into Codex and let Codex install the package for you:

- [Codex one-click install prompts](INSTALL_PROMPTS.md)

Manual install:

```bash
git clone https://github.com/CCDawn/codex-skills.git
cd codex-skills
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

On macOS/Linux:

```bash
sh ./install.sh
```

The default install target is:

- `~/.codex/skills/<ccdawn-skill-name>` for the live skill directory Codex can load at runtime

The installer avoids `~/.agents/skills` by default to prevent duplicate slash-command entries. Use [Install Details](#install-details) for dry runs, verification, selected-skill installs, and advanced targets.


## Included skills

### Engineering

- **`ccdawn-brt`**  
  The Behavior / Review / Test workflow entry skill. It proactively infers what the user likely means, offers candidate intents and high-signal questions with recommendations, and turns aligned intent into behavior contracts, review lenses, test anchors, and next-stage routing.

- **`ccdawn-feature-reuse-research`**
  The reuse-research skill for complex feature additions where existing projects, libraries, examples, or in-project modules may change the plan.

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

- **`ccdawn-project-review`**
  The project-review skill for repository, architecture, technical debt, test gap, maintainability, onboarding, and project health reviews.

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

- **`ccdawn-score-loop`**
  A generic score-loop template for benchmark, leaderboard, validation, baseline promotion, worker-lane, online/offline feedback, and submission-package iteration.

- **`ccdawn-huawei-nslb-score-loop`**  
  A Huawei Algorithm Challenge 37 NSLB adapter over the generic score-loop template. It keeps project commands, ledgers, mutation space, online feedback, and package rules in a project-specific profile.

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
INSTALL_PROMPTS.md
install.ps1
install.sh
skills/
  competition/
    README.md
    ccdawn-score-loop/
    ccdawn-huawei-nslb-score-loop/
  creative/
    README.md
    ccdawn-creative-toolbox/
  engineering/
    README.md
    ccdawn-dawn-agent-html-memory/
    ccdawn-brt/
    ccdawn-feature-reuse-research/
    ccdawn-planning/
    ccdawn-task-splitting/
    ccdawn-bdd-tdd-development/
    ccdawn-completion-summary/
    ccdawn-pr-review/
    ccdawn-project-review/
    ccdawn-bug-review/
    ccdawn-evaluation/
    ccdawn-goal-loop/
  research/
    README.md
    ccdawn-competition-research-lifecycle/
scripts/
  install_codex_library.py
```

## Install Details

You can call the Python installer directly:

```bash
python scripts/install_codex_library.py
```

The installer copies published skills as real directories, checks that folder names match the `name` field in `SKILL.md`, and validates installed Codex skills when the local Codex `quick_validate.py` helper is available.

Preview without changing files:

```bash
python scripts/install_codex_library.py --dry-run
```

List available skills:

```bash
python scripts/install_codex_library.py --list
```

Verify the already installed live Codex copy without reinstalling:

```bash
python scripts/install_codex_library.py --verify-only
```

Install only selected skills:

```bash
python scripts/install_codex_library.py --skill ccdawn-brt --skill ccdawn-dawn-agent-html-memory
```

Install target options:

```bash
python scripts/install_codex_library.py --agent codex         # default live Codex target
python scripts/install_codex_library.py --agent agents        # optional local catalog copy
python scripts/install_codex_library.py --agent claude        # optional Claude global copy
python scripts/install_codex_library.py --agent codex-agents  # Codex plus .agents
python scripts/install_codex_library.py --agent all           # all supported targets
```

Only install the same skill into both `.codex/skills` and `.agents/skills` when duplicate slash-command surfaces are intentional.

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
- `Use ccdawn-project-review to review this repository before refactoring`
- `Use ccdawn-feature-reuse-research before adding a complex editor module`
- `Use ccdawn-bug-review to wrap systematic-debugging for this regression`
- `Use ccdawn-evaluation to evaluate this workflow after checking for a more specific skill`
- `Use ccdawn-score-loop to run this benchmark optimization loop`
- `Use ccdawn-huawei-nslb-score-loop to prepare an NSLB epoch and gate child results`
- `Use ccdawn-creative-toolbox to generate new concept cards from this context`
- `Initialize project memory for this repo`
- `Use ccdawn-dawn-agent-html-memory to initialize project memory for this repo as a frontend project`

This repository is maintained as a local skill library.
