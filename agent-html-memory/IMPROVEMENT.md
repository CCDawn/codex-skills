# Skill Improvement Log

Use this file to record concrete friction discovered while using the skill and the change made in response.

## How to use it

- Add one short entry when repeated friction or a missing workflow is discovered.
- Prefer logging the change after updating the skill, not before.
- Keep entries factual: problem, change, expected benefit.

## Entries

- 2026-05-17: Added `INDEX.md`, `inbox.json`, `archive/`, and cross-reference support so the project memory dashboard scales beyond a single flat summary.
- 2026-05-17: Added `agent-html-memory-init` and `agent-html-memory-sync` commands so initialization and routine syncing are easier to enforce in real projects.
- 2026-05-17: Added agent-html-memory-capture so agents can record in-flight findings into inbox.json before the end-of-task sync step.
- 2026-05-17: Switched the memory model to shared multi-session lanes under `.docs/project-memory/lanes/`, with global recent-updates aggregation and a root `PROJECT_MEMORY.html` shortcut.
