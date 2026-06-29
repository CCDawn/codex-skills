# CCDawn Workflow Runtime

Read this file only when the work is long-running, multi-step, blocked, resumed, or needs cross-stage handoff.

This runtime is not an implementation engine inside `ccdawn-brt`. It is the shared control layer for:

```text
ccdawn-brt -> ccdawn-planning -> ccdawn-task-splitting -> ccdawn-bdd-tdd-development -> ccdawn-completion-summary
```

## Workflow State

State is a routing signal, not decoration.

- INTENT_DISCOVERY: `ccdawn-brt` is identifying the user text, likely intent, and risks.
- INTENT_CONVERGENCE: `ccdawn-brt` is comparing candidate intents and asking high-signal questions.
- PLANNING_READY: requirements are stable enough to ask whether to enter `ccdawn-planning`.
- PLANNING: `ccdawn-planning` is producing an implementation plan.
- TASK_SPLITTING: `ccdawn-task-splitting` is producing a task graph.
- DEVELOPING: `ccdawn-bdd-tdd-development` is executing one selected task.
- SUMMARIZING: `ccdawn-completion-summary` is checking evidence and reporting status.
- BLOCKED: required information, prerequisites, or evidence are missing.
- COMPLETED: critical tasks are done, evidence passed, and no blocker remains.

Transition rules:

- Do not leave `INTENT_CONVERGENCE` until at least one intent is stable or a reversible probe has reduced uncertainty.
- `ccdawn-brt` routes to `ccdawn-planning`, not directly to development, unless the user explicitly chooses a low-risk direct implementation path.
- Each stage stops after its output contract and asks whether to enter the next stage.
- If the user changes the goal, return to `ccdawn-brt`.
- If a later stage discovers the plan is wrong, return to `ccdawn-planning`.
- If a selected task is unclear, return to `ccdawn-task-splitting`.
- Do not enter `COMPLETED` before `ccdawn-completion-summary` verifies evidence.

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

- Update the ledger at every stage boundary.
- Treat the ledger as the handoff contract for "continue".
- Do not invent missing entries. If a field is unknown, mark it as unknown and route to the stage that can resolve it.
- If code reality conflicts with the ledger, update the ledger and explain the mismatch before continuing.

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

Only `ccdawn-completion-summary` can mark the workflow `COMPLETED`.

Completion requires:

- all critical tasks completed or explicitly removed from scope.
- verification evidence is fresh and passed.
- expected vs actual behavior is aligned.
- no unresolved blocker remains.
- Review Matrix or stage self-review has no unresolved `NEEDS_CLARIFICATION` or `NEEDS_CHANGE`.
- accepted residual risks are listed.
- next action is explicit: commit/PR, stop, or return to a prior stage.
