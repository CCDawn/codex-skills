# Project Memory Rules

Add this block to the target repository `AGENTS.md` so every agent session treats project memory as part of normal development.

```md
## Project Memory Rules

- If `.docs/project-memory/` does not exist and this repository is under active development, initialize project memory before or during the first meaningful implementation task.

- Before starting any meaningful development task, read:
  - `.docs/project-memory/INDEX.md`
  - `.docs/project-memory/memory.json`
  - `.docs/project-memory/profile.json`
  - any lane files in `.docs/project-memory/lanes/` that are relevant to the current responsibility

- When another agent may be active or the task touches a shared lane/scope, check and claim work with:
  - `python <skill-root>/scripts/agent_work_guard.py <project-root> status`
  - `python <skill-root>/scripts/agent_work_guard.py <project-root> claim --lane "<stable-responsibility-id>" --scope "<file-or-module-scope>" --agent "<session-label>" --task "<short task>"`
  - release the claim after syncing memory

- During development, store raw findings, partial observations, and unresolved breadcrumbs in:
  - `.docs/project-memory/inbox.json`

- After completing any meaningful development task, update:
  - the current lane file in `.docs/project-memory/lanes/`
  - `.docs/project-memory/memory.json` only for shared metadata and global recent updates
  - `.docs/project-memory/INDEX.md`
  - `.docs/project-memory/overview.html`
  - `PROJECT_MEMORY.html` at the project root

- Rebuild project memory with:
  - `python <skill-root>/scripts/sync_project_memory.py <project-root> --lane "<stable-responsibility-id>" --focus "<current focus>" --update "<what changed>"`

- When active memory becomes noisy, move old resolved items into:
  - `.docs/project-memory/archive/`

- Treat project memory sync as part of the definition of done.
- Do not finish a task with stale project memory unless the user explicitly says to skip it.
```
