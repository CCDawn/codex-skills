# BRT Runtime Details

Read this file only when the task is long-running, multi-step, blocked, resumed, or about agent execution behavior.

## Task State

State is an execution control signal, not a decoration.

- INTENT_DISCOVERY: identifying the user text, possible intent, and keyword risk.
- INTENT_CONVERGENCE: comparing hypotheses and converging a recommendation.
- PLANNING: intent is stable enough to build a Task Graph and verification strategy.
- EXECUTING: the user has allowed implementation and steps are being executed.
- VERIFYING: checking output against expectations.
- BLOCKED: required information, prerequisites, or evidence are missing.
- COMPLETED: critical steps are done, verification passed, and no blocker remains.

State transition rules:

- Stay in INTENT_DISCOVERY until the user's real goal is at least roughly understood.
- Move to INTENT_CONVERGENCE when multiple plausible meanings would change behavior.
- Move to PLANNING only when at least one hypothesis is stable and remaining risk can be recorded.
- If all hypotheses are unstable, run a reversible probe or ask a small set of high-signal choice questions.
- Do not enter EXECUTING until the implementation gate is shown and the user allows it.
- Do not enter COMPLETED before verification.

## Task Graph

Use a Task Graph for long tasks, cross-file changes, multi-step workflows, or anything requiring more than one execution step.

Each step must include:

- input: context, files, data, or previous outputs needed by the step.
- output: observable result required after the step.
- dependency: prior steps, confirmations, tools, or environment state.
- verification condition: evidence that the step is complete and aligned.

Also mark:

- critical path: required for completion.
- optional path: useful but not required.
- high risk step: data loss, security, regression, API breakage, or hard rollback risk.
- ambiguous step: still depends on assumptions or implementation branches.

Do not execute a critical path step without a verification condition.

## Task Memory

Maintain Task Memory for continuous development, debugging, optimization, long tasks, and skill design. It can live in the current reply unless the project already has persistent memory.

Include:

- intent: converged intent.
- assumptions: explicit assumptions and risks.
- decisions: choices affecting behavior, scope, tests, or implementation permission.
- step progress: Task Graph step state.
- unresolved risks: remaining risks and next action.

Update Task Memory after every execution step. If code reality conflicts with the plan, update Task Memory and the requirement ledger before continuing.

## Execution Loop

After entering EXECUTING:

1. BEFORE execution: verify prerequisites, confirm no ambiguity, and declare step scope.
2. DURING execution: execute only the current step; do not expand scope.
3. AFTER execution: verify the output contract, compare expected vs actual, check side effects, and update Task Memory and task state.

If verification fails:

- Set state to VERIFYING or BLOCKED.
- Explain blockage reason.
- Mark impacted step.
- Provide possible fixes.
- Ask only the required high-signal choice questions unless a reversible probe can resolve it.

## Probe

Use a low-risk probe when intent, environment, or implementation path is unstable.

Probe requirements:

- no write action unless explicitly allowed and reversible.
- no destructive action.
- reversible.
- clear observation signals.
- clear interpretation mapping from signal to likely intent/path.

A probe is not implementation. After it, update the requirement ledger, Task Memory, convergence judgment, and next action.

## Completion Gate

Enter COMPLETED only when:

- all critical steps executed.
- verification passed.
- no unresolved blockers remain.
- intent is satisfied or explicitly updated.
- expected vs actual is aligned.
- side-effect check found no undisclosed risk.
- closure lists open questions and residual risks.
