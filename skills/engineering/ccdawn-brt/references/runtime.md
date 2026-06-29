# CCDawn Workflow Runtime

Read this file only when the work is long-running, multi-step, blocked, resumed, or needs cross-stage handoff.

This runtime is not an implementation engine inside `ccdawn-brt`. It is the shared control layer for:

```text
ccdawn-brt -> ccdawn-planning -> ccdawn-task-splitting -> ccdawn-bdd-tdd-development -> ccdawn-completion-summary -> ccdawn-pr-review
```

`ccdawn-pr-review` applies when the next action is submit, push, PR, merge, release, or handoff review. A task can stop after `ccdawn-completion-summary` when no PR/diff review is needed.

## Workflow State

State is a routing signal, not decoration.

- INTENT_DISCOVERY: `ccdawn-brt` is identifying the user text, likely intent, and risks.
- INTENT_CONVERGENCE: `ccdawn-brt` is comparing candidate intents and asking high-signal questions.
- PLANNING_READY: requirements are stable enough to ask whether to enter `ccdawn-planning`.
- PLANNING: `ccdawn-planning` is producing an implementation plan.
- TASK_SPLITTING: `ccdawn-task-splitting` is producing a task graph.
- DEVELOPING: `ccdawn-bdd-tdd-development` is executing one selected task.
- SUMMARIZING: `ccdawn-completion-summary` is checking evidence and reporting status.
- PR_REVIEWING: `ccdawn-pr-review` is checking a PR, branch, commit range, or local diff against requirements and evidence.
- MERGE_READY: `ccdawn-pr-review` found no blocking issues and the next action is submit, push, merge, release, or stop.
- BLOCKED: required information, prerequisites, or evidence are missing.
- COMPLETED: critical tasks are done, evidence passed, and no blocker remains.

Transition rules:

- Do not leave `INTENT_CONVERGENCE` until at least one intent is stable or a reversible probe has reduced uncertainty.
- `ccdawn-brt` routes to `ccdawn-planning`, not directly to development, unless the user explicitly chooses a direct path that is single-scope, reversible, locally verifiable, and has no migration/deletion/permission/release risk.
- Each stage stops after its output contract and asks whether to enter the next stage.
- If the user changes the goal, return to `ccdawn-brt`.
- If a later stage discovers the plan is wrong, return to `ccdawn-planning`.
- If a selected task is unclear, return to `ccdawn-task-splitting`.
- A user may authorize continuous Critical Path execution after task splitting. This authorizes repeated task handoff only; each task still runs through BDD, RED, GREEN, VERIFY, ledger update, and stop-on-blocker checks.
- Continuous Critical Path execution must stop on blocker, failed verification, changed intent, scope expansion, high-risk unconfirmed action, or worktree conflict.
- Do not enter `COMPLETED` before `ccdawn-completion-summary` verifies evidence.
- Do not enter `MERGE_READY` before `ccdawn-pr-review` verifies the diff or PR. `COMPLETED` means implementation evidence passed; `MERGE_READY` means integration review passed.

## Workflow Ledger

Maintain a compact ledger whenever work spans more than one reply, one file, or one stage. The ledger can live in the reply unless the project has persistent memory.

Minimum fields:

```text
Workflow Ledger:
- Confirmed Intent:
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
- Update the ledger at every stage boundary.
- Treat the ledger as the handoff contract for "continue".
- Do not invent missing entries. If a field is unknown, mark it as unknown and route to the stage that can resolve it.
- If code reality conflicts with the ledger, update the ledger and explain the mismatch before continuing.
- Compress the ledger for small tasks: output one `Ledger Update` line when no stage handoff, blocker, or resumed work depends on the full ledger.

## Stage Delta Ledger

Stage skills should not repeat the full ledger when a compact update is enough. Output only the changed fields plus the next recommended stage.

- `ccdawn-planning`: `Current Stage`, `Accepted Plan`, `Decisions`, `Assumptions`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-task-splitting`: `Current Stage`, `Task Graph`, `Current Task`, `Decisions`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-bdd-tdd-development`: `Current Stage`, `Current Task`, `Completed Tasks`, `Verification Evidence`, `Unresolved Risks`, `Recommended Next Stage`.
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
