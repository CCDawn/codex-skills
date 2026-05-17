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

- One skill lives in one top-level folder with its own `SKILL.md`.
- If you modify an existing skill, update the nearest examples or references in the same change when behavior or positioning changes.
- If a skill needs a manual slash-command entrypoint, define it under `plugins/dawn-commands/commands/`.
- Slash commands from this repository must use the `dawn-` prefix. Do not add unprefixed commands.
- Treat `dawn-*` as the reserved command namespace for this repository.
- Keep plugin-facing command names stable and move implementation details behind the skill or scripts, not inside the command contract.

## Skill guidelines

- Keep `SKILL.md` concise and easy to route from description text.
- Move detailed procedures into `REFERENCE.md` or `EXAMPLES.md` when needed.
- Prefer stable instructions over time-sensitive guidance.
- Make artifacts and expected outputs explicit.
- Separate search, synthesis, and validation responsibilities when possible.

## Adding a new skill

1. Create a new top-level folder named after the skill.
2. Add `SKILL.md` with a precise trigger description and a narrow job statement.
3. Add `REFERENCE.md`, `EXAMPLES.md`, `references/`, or `agents/` only when they materially help the skill.
4. Update [README.md](README.md) and [README.zh-CN.md](README.zh-CN.md) so the library index stays complete.
5. Run `python scripts/install_codex_library.py --skip-plugins` to verify the library still installs cleanly.

## Adding or changing a Dawn command

1. Add or update a Markdown command file under `plugins/dawn-commands/commands/`.
2. Name the file after the actual command, for example `dawn-memory-init.md`.
3. Keep the command focused on explicit entry behavior; ongoing automation should live in the skill, not the command wrapper.
4. If the command changes the public contract, update both READMEs in the same change.
5. Re-run `python scripts/install_codex_library.py` and confirm the command appears under `Dawn Commands`.

## Suggested workflow

1. Create or update the skill folder.
2. Keep the description specific about when the skill should trigger.
3. Add at least one realistic example.
4. Test the skill locally in Codex.
5. Open a pull request with a short explanation of the use case.
