# Project Memory Rules

Add this block to the target repository `AGENTS.md` so every agent session treats project memory as part of normal development.

```md
## Project Memory Rules

- If `.docs/project-memory/` does not exist and this repository is under active development, initialize project memory before or during the first meaningful implementation task.

- Before starting any meaningful development task, read:
  - `.docs/project-memory/INDEX.md`
  - `.docs/project-memory/memory.json`
  - `.docs/project-memory/profile.json`

- During development, store raw findings, partial observations, and unresolved breadcrumbs in:
  - `.docs/project-memory/inbox.json`

- After completing any meaningful development task, update:
  - `.docs/project-memory/memory.json`
  - `.docs/project-memory/INDEX.md`
  - `.docs/project-memory/overview.html`

- Rebuild project memory with:
  - `python <skill-root>/scripts/sync_project_memory.py <project-root> --focus "<current focus>" --update "<what changed>"`

- When active memory becomes noisy, move old resolved items into:
  - `.docs/project-memory/archive/`

- Treat project memory sync as part of the definition of done.
- Do not finish a task with stale project memory unless the user explicitly says to skip it.
```
