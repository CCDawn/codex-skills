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
- 2026-05-17: Made `summary`, `lanes`, and `progress` section titles respect `profile.json` labels so localized dashboards can render coherent non-English section headings without patching generated HTML by hand.
- 2026-05-18: Added dedicated setup and troubleshooting references, and clarified that this skill is for project-local repository memory rather than user-global or personal memory.
- 2026-05-18: Added HTML renderer design guidance inspired by the frontend-design skill, then upgraded the overview layout away from generic dark cards toward a denser operational dashboard.
- 2026-05-18: Added `profile.json.visualMode` with named modes (`briefing`, `console`, `studio`, `lab`) so dashboard presentation can be tuned without rewriting the renderer.
- 2026-05-18: Added `profile.json.density` with named levels (`comfortable`, `balanced`, `compact`) so information spacing can be tuned independently from visual style.
- 2026-05-18: Added `profile.json.sectionLayouts` so section width and dashboard rhythm can be tuned per repository without patching the renderer.
- 2026-05-18: Added preset-driven profile resolution with `dashboardPreset` so section order, emphasis, visual mode, and density can move together while lower-level fields remain optional overrides.
- 2026-06-24: Added `agent_work_guard.py` and `agent-html-memory-guard` so multi-agent sessions can check, claim, and release project-memory lanes without manually editing registry files.
