# CCDawn Workflow Runtime

Read this file only when the work is long-running, multi-step, blocked, resumed, or needs cross-stage handoff.

This runtime is not an implementation engine inside `ccdawn-brt`. It is the shared control layer for:

```text
ccdawn-brt -> [existing skill reuse | ccdawn-feature-reuse-research | ccdawn-score-loop | ccdawn-project-review | ccdawn-evaluation | ccdawn-bug-review | ccdawn-planning | ccdawn-pr-review]
ccdawn-planning -> ccdawn-task-splitting -> ccdawn-bdd-tdd-development -> ccdawn-completion-summary -> ccdawn-pr-review
```

`ccdawn-pr-review` applies when the next action is submit, push, PR, merge, release, or handoff review. A task can stop after `ccdawn-completion-summary` when no PR/diff review is needed.
`ccdawn-feature-reuse-research` applies before planning a complex new feature when external projects, libraries, examples, or current-project modules may change the implementation path.
`ccdawn-score-loop` applies when the current need is benchmark, leaderboard, validation-score, online/offline feedback, baseline promotion, worker-lane, or submission-package iteration.
`ccdawn-project-review` applies when the current need is whole-project, repository, architecture, technical debt, test gap, maintainability, onboarding, or risk-module review.
`systematic-debugging` is the primary bug/failure route; `root-cause-tracing` is added when the source is hidden deep in a call chain. `ccdawn-bug-review` is only a CCDawn adapter around those existing skills.
`ccdawn-evaluation` applies when the current need is judgment, comparison, audit, or process quality assessment and no more specific existing skill owns the task.

## Workflow State

State is a routing signal, not decoration.

- INTENT_DISCOVERY: `ccdawn-brt` is identifying the user text, likely intent, and risks.
- INTENT_CONVERGENCE: `ccdawn-brt` is comparing candidate intents and asking high-signal questions.
- BUNDLE_ROUTING: `ccdawn-brt` is grouping multiple user intents into Primary, Secondary, and Deferred actions before choosing stage routes.
- FEATURE_REUSE_RESEARCHING: `ccdawn-feature-reuse-research` is searching and evaluating reusable projects, libraries, examples, or modules before implementation planning.
- SCORE_LOOPING: `ccdawn-score-loop` is running score/benchmark lanes, promotion gates, online/offline calibration, or package feedback.
- PLANNING_READY: requirements are stable enough to ask whether to enter `ccdawn-planning`.
- PROJECT_REVIEWING: `ccdawn-project-review` is reviewing a repository, subsystem, architecture, technical debt, test gaps, or project health.
- EVALUATING: `ccdawn-evaluation` is judging a plan, workflow, skill, implementation, result, or current state.
- BUG_REVIEWING: `ccdawn-bug-review` is inspecting a bug, regression, failing test, or abnormal behavior before choosing a fix path.
- PLANNING: `ccdawn-planning` is producing an implementation plan.
- TASK_SPLITTING: `ccdawn-task-splitting` is deciding `NO_SPLIT` or producing a task graph with per-task development modes.
- DEVELOPING: `ccdawn-bdd-tdd-development` is executing one selected task.
- SUMMARIZING: `ccdawn-completion-summary` is checking evidence and reporting status.
- PR_REVIEWING: `ccdawn-pr-review` is checking a PR, branch, commit range, or local diff against requirements and evidence.
- MERGE_READY: `ccdawn-pr-review` found no blocking issues and the next action is submit, push, merge, release, or stop.
- BLOCKED: required information, prerequisites, or evidence are missing.
- COMPLETED: critical tasks are done, evidence passed, and no blocker remains.

Transition rules:

- Do not leave `INTENT_CONVERGENCE` until at least one intent is stable or a reversible probe has reduced uncertainty.
- Build an Intent Bundle only when one user message contains multiple deliverables, multiple skill owners, different risk boundaries, or different verification contracts. Routine verification, install checks, summaries, and handoff notes stay inside the Primary completion evidence.
- Select Primary by priority: blocking evidence or safety/destructive risk first, then the user's explicit deliverable, then validation/reporting that can be naturally covered by the same contract.
- Route by Primary first. Carry Secondary only when it is same-theme, low-risk, and does not change the Primary contract. Defer or ask when bundled intents conflict.
- Show the bundle only when it changes execution order, skill owner, risk boundary, visible scope, or requires user tradeoff. Otherwise keep it internal.
- A route is actionable only when it has a Route Contract: Owner, Mode, Next Output, Allowed Action, Success Evidence, and Stop Condition. If the next artifact or success evidence cannot be named, stay in BRT for a probe or one clarifying question.
- Parallelize only independent read-only research, review, audit, search, or evaluation work, and only when the speedup is worth the coordination cost. Any write action, shared file/module, shared verification, migration, release, or permission-sensitive work stays sequential in one current contract.
- When a review or audit produces multiple follow-up actions, create an Action Queue before choosing the next stage: Immediate Guardrail, Primary Fix, Telemetry Gap, Deferred Refactor. Do not mix confirmed defects, evidence gaps, governance risks, and maintenance refactors in one severity bucket.
- Prefer existing specialized skills before CCDawn wrapper skills. Route complex feature reuse research to `ccdawn-feature-reuse-research`, score/benchmark/leaderboard iteration to `ccdawn-score-loop`, whole-project/codebase/architecture/technical-debt review to `ccdawn-project-review`, bug/failure work to `systematic-debugging`, deep source tracing to `root-cause-tracing`, PR/diff work to `ccdawn-pr-review`, external review feedback to `receiving-code-review`, and independent reviewer requests to `requesting-code-review`.
- `ccdawn-brt` routes to `ccdawn-planning`, not directly to development, unless the user message already gives clear execution permission and the path is single-scope, reversible, locally verifiable, and has no migration/deletion/permission/release risk. Explicit execution verbs such as fix/add/update/remove/adjust count as permission when the target is clear.
- Each stage gives a next action after its output contract. Stop for user choice only at natural gates: blocker, failed verification that cannot be safely recovered inside the current contract, changed intent, scope expansion, destructive/high-risk action, release/merge action, or worktree conflict.
- If the user changes the goal, return to `ccdawn-brt`.
- If a later stage discovers the plan is wrong, return to `ccdawn-planning`.
- If a selected task is unclear, return to `ccdawn-task-splitting`.
- A user may authorize continuous Critical Path execution after task splitting. This authorizes repeated task handoff only; each task still runs through its selected development mode, verification, ledger update, and stop-on-blocker checks.
- Continuous Critical Path execution must stop on blocker, failed verification that cannot be safely recovered inside the current Execution Contract, changed intent, scope expansion, high-risk unconfirmed action, or worktree conflict.
- A failed verification is first a recovery signal, not automatically a handoff stop. If the cause is inside the current Execution Contract and safe to fix, route back to the owning development/debug stage, fix, and re-verify. Stop only when it becomes a natural gate.
- Do not enter `COMPLETED` before `ccdawn-completion-summary` verifies evidence.
- Do not enter `MERGE_READY` before `ccdawn-pr-review` verifies the diff or PR. `COMPLETED` means implementation evidence passed; `MERGE_READY` means integration review passed.

## Flow and Task Mode Gates

BRT and planning only decide the flow route:

- `FAST_PATH`: clear, low-risk, reversible, locally verifiable, and can finish in one implementation pass. Use light implementation and necessary verification.
- `COMPACT_FLOW`: multiple related work units under one theme. Use one continuous workspace/context. Enter task splitting only when split/no-split or per-subtask mode is unclear.
- `FULL_FLOW`: needs a plan and likely split/no-split decision because it crosses modules, has unclear sequencing, or touches state/API/security/data/migration/release.

Do not assign `SIMPLE` or `BDD_TDD` to the whole user request.

Self-assess process weight before routing:

- Use intent confidence before asking: `HIGH` acts, `MEDIUM` acts with stated assumptions, `LOW` asks or probes, `BLOCKED` asks one blocking question.
- If there are multiple intents, choose `COMPACT_FLOW` when they share a theme and can be ordered in one context; choose separate routing only when owner, risk, deliverable, or verification truly differs.
- If the main value is adding a complex feature where external or internal reuse may change the plan, route to `ccdawn-feature-reuse-research` before `ccdawn-planning`.
- If the main value is measurable score optimization, benchmark/leaderboard feedback, online/offline calibration, baseline promotion, worker lanes, or submission packages, route to `ccdawn-score-loop`.
- If the main value is judgment, comparison, or audit, route to the most specific existing review skill; use `ccdawn-evaluation` only when none fits.
- If the main value is project health, architecture, technical debt, test gaps, onboarding, or risk-module triage, route to `ccdawn-project-review`.
- If the main value is diagnosing a failing behavior, route to `systematic-debugging`; use `ccdawn-bug-review` only when CCDawn handoff/ledger is needed.
- If the main value is reviewing a PR/diff/branch before integration, route to `ccdawn-pr-review`.
- If a step does not change outcome, reduce it: skip planning, choose `NO_SPLIT`, compress ledger, or keep `FAST_PATH`.
- Reuse the current worktree for one theme. Create a new worktree only for parallel work, conflict isolation, high-risk isolation, or explicit user request.

## Execution Contract and Edit Guard

Any stage that may write files must carry a compact Execution Contract. Keep it internal for small safe tasks; output it when handing off, resuming, or touching risky areas.

```text
Execution Contract:
- Target:
- Desired Outcome:
- Allowed Actions:
- Out of Scope:
- Success Evidence:
- Recovery Signal:
```

Before writing, run the edit guard:

- identify the owning surface and expected files;
- inspect worktree state and protect unrelated user or agent changes;
- list the protected boundary: adjacent files, behavior, tests, config, docs, dependencies, or cleanup not required by the contract;
- if the needed edit crosses the protected boundary, return to `ccdawn-brt` or `ccdawn-planning` before writing;
- if ownership is uncertain after reading local context, probe or ask instead of editing.

Verification recovery:

- classify failures as implementation, test intent, environment, or requirement mismatch;
- fix implementation/test alignment only when the fix stays inside the contract;
- do not weaken behavior requirements just to pass tests;
- route environment or requirement mismatches to the owning stage with one concrete next action.

Owner boundaries:

- `ccdawn-brt` owns intent alignment, response depth, execution permission, and process weight.
- `ccdawn-evaluation` owns quality judgment of a plan, workflow, skill, result, or current state after the user goal is known.
- Once routed to `ccdawn-evaluation`, return to BRT only when the user's goal or evaluation object is unclear.

`ccdawn-task-splitting` owns the split decision:

- `NO_SPLIT`: one low-risk execution unit, clear verification, no staged dependencies, no BDD/TDD need.
- `SPLIT`: create subtasks and classify each subtask as `SIMPLE` or `BDD_TDD`.

Inside `SPLIT`, upgrade a subtask to `BDD_TDD` only when at least one signal is present:

- behavior is new or ambiguous enough that a one-pass implementation is likely to drift;
- failure path, state transition, persistence, permission, migration, API, or integration contract matters;
- change spans multiple modules or depends on staged refactoring;
- existing bug is not localized or has already regressed;
- verification requires a new behavior test to be trustworthy;
- user explicitly asks for strict BDD/TDD.

Keep a subtask `SIMPLE` when it is localized, has clear expected output, has no risky state/API/data change, and a direct verification command or structural check is enough.

## Workflow Ledger

Maintain a compact ledger whenever work spans more than one reply, one file, or one stage. The ledger can live in the reply unless the project has persistent memory.

Minimum fields:

```text
Workflow Ledger:
- Confirmed Intent:
- Intent Bundle:
- Route Contract:
- Action Queue:
- Current Stage:
- Accepted Plan:
- Task Graph:
- Current Task:
- Completed Tasks:
- Verification Evidence:
- Decisions:
- Assumptions:
- Unresolved Risks:
- Recommended Next Stage:
```

Ledger rules:

- When `ccdawn-brt` enters planning, seed `Workflow Ledger` from the requirement ledger: confirmed intent, assumptions, unresolved risks, and verification anchors.
- When an Intent Bundle exists, carry it as `Primary / Secondary / Deferred`; stage skills may execute only the part covered by their current contract and must preserve deferred items as next-stage context.
- When a Route Contract exists, preserve the selected Owner, Mode, Next Output, Allowed Action, Success Evidence, and Stop Condition until the next stage replaces or completes it.
- When an Action Queue exists, preserve `Immediate Guardrail / Primary Fix / Telemetry Gap / Deferred Refactor`; the next stage should execute or plan only the selected queue item and keep the rest as deferred context.
- Update the ledger at every stage boundary.
- Treat the ledger as the handoff contract for "continue".
- Do not invent missing entries. If a field is unknown, mark it as unknown and route to the stage that can resolve it.
- If code reality conflicts with the ledger, update the ledger and explain the mismatch before continuing.
- Compress the ledger for small tasks: output one `Ledger Update` line when no stage handoff, blocker, or resumed work depends on the full ledger.
- Add `Execution Contract` and `Protected Boundary` only when they affect handoff, resumption, high-risk editing, or failed-verification recovery.

## Stage Delta Ledger

Stage skills should not repeat the full ledger when a compact update is enough. Output only the changed fields plus the next recommended stage.

- `ccdawn-brt`: `Current Stage`, `Intent Bundle`, `Route Contract`, `Action Queue`, `Decisions`, `Assumptions`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-planning`: `Current Stage`, `Intent Bundle`, `Accepted Plan`, `Decisions`, `Assumptions`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-feature-reuse-research`: `Current Stage`, `Reuse Decision`, `Candidate Evidence`, `Rejected Alternatives`, `Verification Strategy`, `Recommended Next Stage`.
- `ccdawn-score-loop`: `Current Stage`, `Baseline`, `Metric`, `Lane`, `Score Evidence`, `Gate Decision`, `Calibration Lesson`, `Recommended Next Stage`.
- `ccdawn-task-splitting`: `Current Stage`, `Split Decision`, `Task Graph`, `Current Task`, `Decisions`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-bdd-tdd-development`: `Current Stage`, `Current Task`, `Development Mode`, `Completed Tasks`, `Verification Evidence`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-completion-summary`: `Current Stage`, `Completed Tasks`, `Verification Evidence`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-pr-review`: `Current Stage`, `Verification Evidence`, `Unresolved Risks`, `Recommended Next Stage`.

Use the full ledger when resuming, blocked, handing off to another agent, or when a missing field would change the route.

## Probe

Use a low-risk probe when intent, environment, or implementation path is unstable.

Probe requirements:

- no destructive action.
- no write action unless explicitly allowed and reversible.
- clear observation signals.
- clear interpretation mapping from signal to likely intent, plan, or task.

A probe is not implementation. After a probe, update the requirement ledger, Workflow Ledger, convergence judgment, and next-stage recommendation.

## Blocked Handling

When blocked, output:

```text
BLOCKED:
- Reason:
- Impacted Stage:
- Impacted Ledger Field:
- Possible Fixes:
- Required User Input: [one high-signal question, with options]
```

Ask one blocking question only. If several questions are useful but not required, put them in possible fixes instead.

## Completion Gate

Only `ccdawn-completion-summary` can mark implementation `COMPLETED`. Only `ccdawn-pr-review` can mark a PR or diff `MERGE_READY`.

Runtime owns the state transition; the stage skills own the detailed criteria.

- Do not mark `COMPLETED` without `ccdawn-completion-summary` evidence.
- Do not mark `MERGE_READY` without `ccdawn-pr-review` evidence.
- If evidence is missing, stale, or contradicted by the diff, route to the owning stage instead of claiming readiness.
- If the gap is fixable inside the current Execution Contract, recommend the recovery route; if it requires new scope, permission, or intent change, stop at the natural gate.
