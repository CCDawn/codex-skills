---
name: agent-html-memory
description: Create and maintain a per-project HTML memory dashboard backed by structured data. Use when Codex needs a durable project overview that tracks progress, modules, decisions, issues, todos, technical notes, and recent updates, and when Codex should keep that overview synchronized after development work. Trigger for requests about project memory, project overview HTML, status dashboard, persistent progress tracking, technical detail tracking, "update the project memory page", or any meaningful development session inside a repository that already contains `.docs/project-memory/`.
---

# Agent HTML Memory

Create a project-local memory system under `.docs/project-memory/` and keep it current after meaningful work.

## Enforcement model

Treat project memory maintenance as part of the definition of done.

- Before meaningful development, read `INDEX.md`, `memory.json`, `profile.json`, and any lane files relevant to the current responsibility.
- During development, place raw findings in `inbox.json` when needed.
- After meaningful development, update only the current lane file plus the global recent-updates feed, then run the sync command.
- Do not end a task with stale project memory unless the user explicitly says to skip it.

If the repository contains `.docs/project-memory/`, assume this skill is active even when the user did not mention it by name.

## Proactive initialization trigger

When working inside a repository that does not yet contain `.docs/project-memory/`, proactively check whether this looks like a real software project that would benefit from persistent project memory.

Strong signals include:

- the repository contains `AGENTS.md`
- the repository contains source folders such as `src/`, `app/`, `server/`, `backend/`, or `frontend/`
- the repository contains build or package files such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or similar
- the user asks for ongoing implementation, debugging, refactoring, or project tracking

When those signals are present:

- briefly suggest initializing project memory if it is missing
- if the user is asking you to do real development work and has not objected to project memory, prefer initializing it early in the session
- after initialization, treat this skill as active for the rest of the project work

Do not interrupt tiny one-off questions or trivial read-only tasks just to bootstrap memory.

## Explicit initialization prompts

When the user wants a one-time setup, accept direct prompts such as:

- `Initialize project memory for this repo`
- `Use agent-html-memory to initialize project memory for this backend project`
- `Bootstrap persistent memory for this codebase`

Treat those prompts as explicit permission to run the setup workflow immediately.

## Continuous improvement

Treat real usage as feedback for the skill itself.

- When this skill causes repeated friction, update the skill instead of only working around the friction in one project.
- Improve the smallest reusable layer that would help the next session: `SKILL.md`, Python scripts, templates, or references.
- Record meaningful improvements in `IMPROVEMENT.md`.
- Prefer changes that reduce repeated manual steps, tighten agent behavior, or make project memory more reliable.

Do this only when the improvement is local, safe, and clearly useful. Do not derail urgent user work for speculative cleanup.

## What this skill manages

Maintain these files inside the target project:

```text
.docs/project-memory/
  memory.json
  profile.json
  overview.html
  INDEX.md
  inbox.json
  lanes/
  archive/
```

- `memory.json` is the shared shell for project-level metadata, lane index data, and global `recentUpdates`.
- `profile.json` is the project adaptation layer.
- `overview.html` is a generated static dashboard for humans.
- `INDEX.md` is the quick navigation entry for both humans and agents.
- `inbox.json` is a staging area for quick capture during ongoing work.
- `lanes/*.json` are the per-responsibility memory files that individual sessions should maintain.
- `archive/` stores historical items moved out of the active dashboard.
- `PROJECT_MEMORY.html` lives at the project root as the stable human-facing shortcut into the dashboard.

Do not treat `overview.html` as the primary editable artifact unless the user explicitly asks for a one-off manual page.

## Setup

When the project does not already have a memory system:

1. Run `python <this-skill>/scripts/init_project_memory.py <project-root>`.
2. Pick the closest project type:
   - `frontend`
   - `backend`
   - `automation`
   - `research`
   - `general`
3. Let initialization inject the `Project Memory Rules` block into `AGENTS.md` unless the user explicitly opts out.
4. Confirm the generated files exist under `.docs/project-memory/`.

## Update workflow

After a meaningful task, update the memory system in this order:

1. Read `.docs/project-memory/memory.json` and `.docs/project-memory/profile.json`.
2. Read `inbox.json` when the task involved quick captures or unresolved notes.
3. Resolve the current responsibility lane, such as `backend-auth` or `frontend-dashboard`.
4. Update only that lane file unless the user explicitly asks for broader edits.
5. Append a short entry to global `recentUpdates`.
6. When there is a real behavior or architecture decision, append a `decisions` item inside the current lane.
7. When there is a new blocker or investigation thread, append or update an `issues` item inside the current lane.
8. Add or preserve cross-references such as related modules, issues, decisions, or files.
9. Re-render `overview.html`, refresh `INDEX.md`, and refresh the root `PROJECT_MEMORY.html` shortcut with `python <this-skill>/scripts/render_overview.py <project-root>`.

Prefer preserving existing history. Do not rewrite old entries just to make them prettier.

## What to record

Keep the memory high signal. Favor compact factual notes over narration.

- `summary`: shared shell metadata, not a free-form scratchpad for every session
- `progress`: completion summary and milestones
- `modules`: feature or subsystem status with notes inside the current lane
- `decisions`: context, decision, impact inside the current lane
- `issues`: status, severity, impact, next step inside the current lane
- `todos`: next actions with owner and status when known inside the current lane
- `techNotes`: key implementation details worth reloading later inside the current lane
- `recentUpdates`: chronological short log of meaningful work at the global level, with lane references

Use lightweight cross-references when entries are related:

- `relatedModules`
- `relatedIssues`
- `relatedDecisions`
- `relatedFiles`

## Adaptation rules

Use `profile.json` to adapt the dashboard by project type.

- `projectType`: broad mode such as `frontend` or `automation`
- `sections`: ordered list of sections to emphasize in HTML
- `labels`: display labels for project-specific wording

Keep adaptation light. Avoid building a large configuration DSL unless the project truly needs it.

## Inbox and capture

Use `inbox.json` for quick capture during a task when information is too raw to place immediately in the main memory.

- Capture half-formed findings, observations, temporary blockers, and breadcrumbs.
- Fold useful items into `memory.json` before the task closes.
- Leave unresolved but important fragments in `inbox.json` only when they still need follow-up.
- Keep `inbox.json` small. It is a staging area, not the main history.

## Index

Maintain `INDEX.md` as a compact navigation page.

- Show the current project type, last updated time, and active files.
- Link to `overview.html`, `memory.json`, `profile.json`, `inbox.json`, `lanes/`, `archive/`, and `PROJECT_MEMORY.html`.
- Summarize counts for modules, open issues, decisions, todos, and recent updates.

This file helps both humans and agents re-enter the project quickly.

## Archive

Archive old history instead of deleting it.

- Move stale or resolved updates, issues, or decisions into `archive/` when active memory becomes noisy.
- Keep active memory focused on current state plus near history.
- Prefer archive files grouped by topic or time window, such as `issues-resolved.json` or `updates-2026-q2.json`.

Archive by moving old entries out of active arrays and leaving a brief trace in active memory when necessary.

## Update discipline

Update the memory system when:

- a task completes
- a module status changes
- a blocker appears or is resolved
- a technical decision is made
- the planned next step changes

Skip updates only for trivial cosmetic work or when the user explicitly says not to maintain the memory page.

## Verification

After updating memory:

1. Run the renderer.
2. Open the generated `overview.html` in a browser when practical, or at minimum inspect the file contents.
3. Check that the latest task appears in `recentUpdates`.
4. Check that the active lane shows the latest owner, focus, and update time.
5. Check that any changed modules, todos, or issues are reflected in the HTML under the correct lane.
6. Check that `INDEX.md` reflects the latest counts and file links.
7. Check that the project-root `PROJECT_MEMORY.html` opens the overview.

## Commands

Replace `<skill-root>` with this skill folder path.

```bash
python <skill-root>/scripts/init_project_memory.py <project-root> --project-type frontend
python <skill-root>/scripts/render_overview.py <project-root>
python <skill-root>/scripts/sync_project_memory.py <project-root> --lane backend-auth --focus "What changed" --update "Short summary of this task"
python <skill-root>/scripts/capture_note.py <project-root> --lane backend-auth --title "Observation" --details "What you noticed"
agent-html-memory-init <project-root> --project-type frontend
agent-html-memory-sync <project-root> --lane backend-auth --focus "What changed" --update "Short summary of this task"
agent-html-memory-capture <project-root> --lane backend-auth --title "Observation" --details "What you noticed"
```
