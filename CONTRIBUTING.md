# Contributing

Thanks for contributing.

## What belongs here

This repository is for Codex skills related to research competitions, benchmark projects, evidence synthesis, and paper-readiness workflows.

Good additions include:

- new skills with clear trigger descriptions
- reference files that deepen an existing skill
- examples showing realistic usage
- improvements to installation or usage docs

## Repository growth rules

- One skill lives under `skills/<bucket>/<ccdawn-skill-name>/` with its own `SKILL.md`.
- The folder name must match the `name` field in `SKILL.md`. Treat mismatches as a bug, not a style issue.
- If you modify an existing skill, update the nearest examples or references in the same change when behavior or positioning changes.
- This repository ships a lightweight `.claude-plugin/plugin.json` manifest that indexes the promoted skills.
- Keep reusable behavior in the skill, its scripts, and its references. The plugin layer should stay thin and declarative.
- The formal local install targets for published skills are:
  - `~/.codex/skills/<ccdawn-skill-name>` as a real directory for runtime loading
  - `~/.agents/skills/<ccdawn-skill-name>` only when you explicitly need an extra local catalog copy
  Installing the same skill into both locations can produce duplicate slash-command entries in Codex. Do not rely on symlinks or junctions as the default install shape.

## Skill guidelines

- Keep `SKILL.md` concise and easy to route from description text.
- Move detailed procedures into `REFERENCE.md` or `EXAMPLES.md` when needed.
- Prefer stable instructions over time-sensitive guidance.
- Make artifacts and expected outputs explicit.
- Separate search, synthesis, and validation responsibilities when possible.

## Adding a new skill

1. Create a new folder under the appropriate bucket in `skills/`.
2. Add `SKILL.md` with a precise trigger description and a narrow job statement.
3. Add `REFERENCE.md`, `EXAMPLES.md`, `references/`, or `agents/` only when they materially help the skill.
4. Update [README.md](README.md), [README.zh-CN.md](README.zh-CN.md), bucket-level listings, and `.claude-plugin/plugin.json` when the catalog changes.
5. Run `python scripts/install_codex_library.py --dry-run` to preview the install plan, then `python scripts/install_codex_library.py` to install the local Codex copy. Use `--agent codex-agents` only when you explicitly need both copies.
6. Validate the installed live Codex skill with `python scripts/install_codex_library.py --verify-only` when the local Codex validator is available, then restart Codex and confirm the slash-command entry reloads.

## Suggested workflow

1. Create or update the skill folder.
2. Keep the description specific about when the skill should trigger.
3. Add at least one realistic example.
4. Test the live installed skill locally in Codex, not just the repo copy. `--verify-only --skill <name>` is the fastest post-install check when you only changed one skill.
5. If a slash-command entry is missing or duplicated, check the live `.codex` copy, then look for an extra `.agents` copy, then inspect the repo-local `.claude-plugin/plugin.json` if this repo is the active trusted workspace.
6. Restart Codex before declaring a metadata change broken.
7. Open a pull request with a short explanation of the use case.
