---
name: ccdawn-dawn-agent-html-memory
description: Use when Codex needs project-local persistent memory under `.docs/project-memory/`, a generated HTML repository dashboard, durable progress/modules/decisions/issues/todos tracking, project memory initialization, project memory sync after meaningful development, or "update the project memory page" requests.
---

# Agent HTML Memory

Create a project-local memory system under `.docs/project-memory/` and keep it current after meaningful work.

## BRT interface

- Context Boundary: target repository root, `.docs/project-memory/`, relevant lane files, project rules, and the current task result.
- Output Contract: initialized or updated project memory files plus rendered dashboard/index evidence.
- Allowed Action: edit only `.docs/project-memory/`, `PROJECT_MEMORY.html`, and the AGENTS memory block during initialization unless the user explicitly authorizes broader changes.
- Success Evidence: changed lane/recent update is present in JSON, `overview.html`, `INDEX.md`, and root `PROJECT_MEMORY.html` when applicable.
- Stop Condition: missing project root, malformed memory files, overlapping active claim, renderer failure, or user explicitly skips memory.
- Route Out: return to the current CCDawn stage, `ccdawn-completion-summary`, or BLOCKED with one required fix/input.

## 统一输出标准

- 用户可见输出默认中文；只有代码、命令、路径、错误原文、API/协议名、skill 名、状态枚举和外部专名保留英文。
- 报告、方案、审查、阶段文档和交接摘要使用中文标题与中文字段；内部字段对外翻译为：上下文边界、输出契约、允许动作、成功证据、停止条件、路由出口、下一步建议。
- 若必须保留英文状态或枚举，先用中文解释其含义。
- 用户可见正文末尾保留 `下一步建议: ...`，除非被更高优先级系统附录隔开。

## Owner 接入规则

进入本 skill 前先做轻量 owner 自检：

- 如果用户主目标不属于本 skill 的 owner 范围，不继续执行；回 `ccdawn-brt` 做 Owner 仲裁，或转交更具体 owner。
- 如果本 skill 只覆盖复合任务的一部分，只处理当前路由契约覆盖的 Primary/Secondary，不吞掉其他 owner。
- 如果发现 planning/development 正在替代更具体 owner，先输出路由修正，再进入正确 owner。

## Load extra references when needed

- Read `references/setup.md` on first initialization, or when the right project type, lane shape, or adoption approach is unclear.
- Read `references/troubleshooting.md` when the memory system feels stale, noisy, misplaced, or inconsistent.
- Read `references/html-design.md` when improving `overview.html` rendering or when the user wants a more polished dashboard presentation.

## Enforcement model

Treat project memory maintenance as part of the definition of done.

- Before meaningful development or continuation work where memory can change the answer, read `INDEX.md`, `memory.json`, `profile.json`, and only the lane files relevant to the current responsibility.
- When another agent may be working in the same project, run the work guard status/check before editing and claim the active lane when overlap risk exists.
- During development, place raw findings in `inbox.json` when needed.
- After meaningful development, update only the current lane file plus the global recent-updates feed, then run the sync command.
- Do not end a task with stale project memory unless the user explicitly says to skip it.

If the repository contains `.docs/project-memory/`, treat this skill as available for meaningful repository work, continuation, cross-session decisions, or memory updates. Do not automatically read or update it for trivial read-only questions, tiny one-off edits, or reviews where project memory cannot change the conclusion.

## Relationship to built-in memory and other context

This skill complements chat context, `AGENTS.md`, and any built-in or workspace memory system. It does not replace them.

Use `.docs/project-memory/` for durable repository state such as:

- subsystem progress
- engineering decisions
- blockers and follow-up threads
- project-specific technical notes
- cross-session next steps

Do not use this skill for:

- user-global personal memory
- contact or relationship tracking
- generic knowledge unrelated to the repository
- secrets, credentials, or tokens
- full chat transcript dumps

If the repository already has another memory surface such as `MEMORY.md` or `memory/`, do not rewrite it just because this skill exists. Keep this system focused on project-local state and carry over only the facts that help future repository work.

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
- `Use ccdawn-dawn-agent-html-memory to initialize project memory for this backend project`
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
- `overview.html` should follow the renderer design guidance in `references/html-design.md`: polished, operational, and easy to scan, not generic template UI.
- `INDEX.md` is the quick navigation entry for both humans and agents.
- `inbox.json` is a staging area for quick capture during ongoing work.
- `lanes/*.json` are the per-responsibility memory files that individual sessions should maintain.
- `archive/` stores historical items moved out of the active dashboard.
- `PROJECT_MEMORY.html` lives at the project root as the stable human-facing shortcut into the dashboard.
- `agent-claims.json` is an optional coordination registry for active/ready agent work claims.

Do not treat `overview.html` as the primary editable artifact unless the user explicitly asks for a one-off manual page.

## Work guard

Use `scripts/agent_work_guard.py` when work may overlap across sessions or agents.

- `status` is read-only and shows active/ready claims.
- `check` is read-only and returns nonzero when the requested lane or scope overlaps an active/ready claim.
- `claim` writes an expiring claim to `agent-claims.json` only when no overlap exists, unless `--force` is used after manual review.
- `release` closes the claim as `released`, `completed`, or `blocked`.
- Claims expire automatically by TTL and are stored outside the main memory model, so they do not pollute the dashboard.

Claim the smallest stable lane/scope that protects the work. Release the claim after the memory sync step finishes.

## Setup

For first-time setup details, load `references/setup.md`.

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
- `dashboardPreset`: high-level composition family such as `default`, `ops-heavy`, `review-heavy`, or `research-log`
- `visualMode`: named presentation style such as `briefing`, `console`, `studio`, or `lab`
- `density`: information density such as `comfortable`, `balanced`, or `compact`
- `sectionLayouts`: per-section layout spans such as `standard`, `narrow`, `wide`, or `full`
- `sections`: ordered list of sections to emphasize in HTML
- `labels`: display labels for project-specific wording

Treat `dashboardPreset` as the base layer. Use the other fields only when you need explicit overrides on top of that preset.

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

If verification fails or the dashboard looks wrong, load `references/troubleshooting.md`.

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
python <skill-root>/scripts/init_project_memory.py <project-root> --project-type frontend --dashboard-preset review-heavy --visual-mode studio --density comfortable
python <skill-root>/scripts/render_overview.py <project-root>
python <skill-root>/scripts/sync_project_memory.py <project-root> --lane backend-auth --focus "What changed" --update "Short summary of this task"
python <skill-root>/scripts/capture_note.py <project-root> --lane backend-auth --title "Observation" --details "What you noticed"
python <skill-root>/scripts/agent_work_guard.py <project-root> status
python <skill-root>/scripts/agent_work_guard.py <project-root> check --lane backend-auth --scope src/auth
python <skill-root>/scripts/agent_work_guard.py <project-root> claim --lane backend-auth --scope src/auth --agent codex-session --task "Auth changes"
python <skill-root>/scripts/agent_work_guard.py <project-root> release --claim-id claim-id --status completed
agent-html-memory-init <project-root> --project-type frontend --dashboard-preset review-heavy --visual-mode studio --density comfortable
agent-html-memory-sync <project-root> --lane backend-auth --focus "What changed" --update "Short summary of this task"
agent-html-memory-capture <project-root> --lane backend-auth --title "Observation" --details "What you noticed"
agent-html-memory-guard <project-root> status
```

