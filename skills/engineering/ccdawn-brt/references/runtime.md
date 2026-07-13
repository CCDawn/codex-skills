# CCDawn Workflow Runtime

Read this file only when the work is long-running, multi-step, blocked, resumed, or needs cross-stage handoff.

This runtime is not an implementation engine inside `ccdawn-brt`. It is the shared control layer for:

```text
ccdawn-brt -> most specific owner
owner -> [direct execution | persistent planning when reusable] -> [optional splitting | compact TDD when risky] -> proportional verification -> [optional summary/review when another boundary needs it]
```

`ccdawn-pr-review` applies when the next action is submit, push, PR, merge, release, or handoff review. A task can stop after `ccdawn-completion-summary` when no PR/diff review is needed.
`ccdawn-feature-reuse-research` applies before planning a complex new feature when external projects, libraries, examples, or current-project modules may change the implementation path.
`ccdawn-ai-research-loop` owns AI/ML research questions, baseline reproduction, hypothesis portfolios, ablations, multi-round evidence synthesis, and continue/branch/pivot/stop direction decisions.
`ccdawn-score-loop` exclusively owns benchmark, leaderboard, validation-score, online/offline feedback, baseline promotion, worker-lane, experiment mutation, and submission-package iteration while the main unknown is metric impact. Experiment lanes bypass general SIMPLE/BDD_TDD classification.
`ccdawn-research-rigor-review` gates important research claims, surprising results, active-baseline promotion, and high-cost direction changes; it is not a mandatory review after every experiment lane.
`ccdawn-project-review` applies when the current need is whole-project, repository, architecture, technical debt, test gap, maintainability, onboarding, or risk-module review.
`ccdawn-simplification-review` applies when the primary question is what unnecessary complexity can be removed from a current diff without changing required behavior.
`ccdawn-simplification-audit` applies when the primary question is what dependency, abstraction, wrapper, legacy path, or duplicate structure can be removed from a repository or subsystem.
External GitHub skill candidates are install-gated. Route to them only when they are installed or the user asks to install/use them; otherwise use the local fallback owner and preserve the candidate as an optional Route Out.
Frontend design, UI engineering, browser control, development-standard/spec/source-doc, Kaggle/empirical-research, and creative-method candidates follow the same install gate. If they are missing, fill the Route Contract with the local CCDawn owner, current project patterns, browser/Playwright verification, or official-doc research instead of blocking.
Intent interview/refinement, incremental implementation, doubt/self-review, code simplification, git/versioning, CI/CD, shipping, issue/backlog/spec intake, MCP/tool integration, webapp testing, logs, and LLM traces also follow the install gate. External workspace writes, remote git actions, releases, deployments, and destructive browser actions require an explicit permission gate.
Superpowers process skills are scoped methods, not the workflow owner. BRT mode and the current Route Contract decide whether brainstorming, planning, worktree isolation, strict TDD, subagents, review loops, or branch finishing are justified; broad `always/every/any` trigger language does not upgrade the flow by itself. Verification evidence remains mandatory but proportional to the claim and risk.
Assume a high-capability reasoning model can keep a bounded plan, dependency order, and self-review internal. Require a visible artifact or separate stage only when another person/session needs it, the user wants to review it, or a named high-risk failure needs the checkpoint.
When a subtask needs TDD, use the compact `ccdawn-bdd-tdd-development` owner instead of dual-loading Superpowers `test-driven-development`. Reuse a real failing test or stable reproduction as RED, run the narrow test to GREEN, and defer broad suites to integration risk or closeout.
Score regression, metric underperformance, rejected hypotheses, and neutral/worse online feedback are experiment evidence, not TDD RED. Route only a separated deterministic harness/parser/schema/metric/seed/shape/packaging bug to compact TDD, then return to the original score lane without treating GREEN as promotion evidence.
Default to no subagent. If independent write lanes justify dispatch, use one implementer per lane with a compact contract, let the parent verify diff and command evidence, and add at most one final independent reviewer only for a high-risk boundary or explicit user request. Do not create implementer-plus-two-reviewer chains per task or allow child agents to dispatch grandchildren.
`systematic-debugging` is the primary bug/failure route; `root-cause-tracing` is added when the source is hidden deep in a call chain. `ccdawn-bug-review` is only a CCDawn adapter around those existing skills.
`ccdawn-evaluation` applies when the current need is judgment, comparison, audit, or process quality assessment and no more specific existing skill owns the task.

## Workflow State

State is a routing signal, not decoration.

- INTENT_DISCOVERY: `ccdawn-brt` is identifying the user text, likely intent, and risks.
- INTENT_CONVERGENCE: `ccdawn-brt` is comparing candidate intents and asking high-signal questions.
- BUNDLE_ROUTING: `ccdawn-brt` is grouping multiple user intents into Primary, Secondary, and Deferred actions before choosing stage routes.
- FEATURE_REUSE_RESEARCHING: `ccdawn-feature-reuse-research` is searching and evaluating reusable projects, libraries, examples, or modules before implementation planning.
- AI_RESEARCHING: `ccdawn-ai-research-loop` is reproducing a baseline, selecting hypotheses, synthesizing experiment evidence, or deciding whether to continue, branch, pivot, consolidate, or stop.
- SCORE_LOOPING: `ccdawn-score-loop` is running score/benchmark lanes, promotion gates, online/offline calibration, or package feedback.
- RESEARCH_RIGOR_REVIEWING: `ccdawn-research-rigor-review` is checking whether important evidence supports a baseline promotion, research claim, or high-cost next direction.
- EXTERNAL_SKILL_CANDIDATE: BRT found a better GitHub/community skill candidate but must verify installation or use a local fallback.
- PLANNING_READY: requirements are stable and planning has enough value to enter `ccdawn-planning`; do not pause only to ask whether to proceed when permission already exists.
- PROJECT_REVIEWING: `ccdawn-project-review` is reviewing a repository, subsystem, architecture, technical debt, test gaps, or project health.
- SIMPLIFICATION_REVIEWING: `ccdawn-simplification-review` is reviewing a current diff for evidence-backed cuts while leaving correctness and merge readiness to PR review.
- SIMPLIFICATION_AUDITING: `ccdawn-simplification-audit` is ranking removable repository complexity while leaving architecture and project health to project review.
- EVALUATING: `ccdawn-evaluation` is judging a plan, workflow, skill, implementation, result, or current state.
- BUG_REVIEWING: `ccdawn-bug-review` is inspecting a bug, regression, failing test, or abnormal behavior before choosing a fix path.
- PLANNING: `ccdawn-planning` is producing an implementation plan.
- TASK_SPLITTING: `ccdawn-task-splitting` is producing a task graph after BRT or planning has already found real dependency, owner, risk, parallel, verification, or handoff boundaries. `NO_SPLIT` stays an internal BRT/planning decision.
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
- Run Owner Arbitration before planning, task splitting, development, or summary. List only signal-matched candidate owners, choose the most specific owner that can produce the next artifact and success evidence, and treat planning/development as downstream flow stages rather than default owners.
- Parallelize only independent read-only research, review, audit, search, or evaluation work, and only when the speedup is worth the coordination cost. Any write action, shared file/module, shared verification, migration, release, or permission-sensitive work stays sequential in one current contract.
- Do not inherit a complete Superpowers chain from one selected method. Re-evaluate each downstream method against the current BRT mode, remaining risk, and coordination cost.
- Treat prompt preparation, repeated repository reading, review dispatch, worktree setup, and result merging as real subagent cost. Keep work in the parent when that cost is not clearly repaid.
- When a review or audit produces multiple follow-up actions, create an Action Queue before choosing the next stage: Immediate Guardrail, Primary Fix, Telemetry Gap, Deferred Refactor. Do not mix confirmed defects, evidence gaps, governance risks, and maintenance refactors in one severity bucket.
- Prefer existing specialized skills before CCDawn wrapper skills. Route AI/ML research direction and multi-round evidence synthesis to `ccdawn-ai-research-loop`, concrete score/benchmark lanes to `ccdawn-score-loop`, important research claims to `ccdawn-research-rigor-review`, complex feature reuse research to `ccdawn-feature-reuse-research`, whole-project/codebase/architecture/technical-debt review to `ccdawn-project-review`, bug/failure work to `systematic-debugging`, deep source tracing to `root-cause-tracing`, PR/diff work to `ccdawn-pr-review`, external review feedback to `receiving-code-review`, and independent reviewer requests to `requesting-code-review`. If a later stage detects that a more specific owner should have handled the request, it must route back to BRT for Owner Arbitration or hand off to that owner.
- If a GitHub-discovered skill is more specific but not installed, do not stop. Use the local fallback owner and record the external skill as `Optional Route Candidate`. Ask about installation only when fallback cannot satisfy the requested output or the user explicitly wants the external skill.
- Direct execution is the default after internal alignment when the owner can name the intended outcome, protected boundary, success evidence, and recovery signal. Enter `ccdawn-planning` only when its artifact will be reviewed/reused, coordinates distinct owners or phases, preserves a long-task decision, or gates irreversible/high-risk sequencing. Explicit verbs such as fix/add/update/remove/adjust count as permission when the target is clear.
- Each stage gives a next action after its output contract. Stop for user choice only at natural gates: blocker, failed verification that cannot be safely recovered inside the current contract, changed intent, scope expansion, destructive/high-risk action, release/merge action, or worktree conflict.
- If the user changes the goal, return to `ccdawn-brt`.
- If a later stage discovers the plan is wrong, return to `ccdawn-planning`.
- If an existing task boundary is unclear, return to `ccdawn-planning`; enter `ccdawn-task-splitting` only when a real split trigger remains.
- A user may authorize continuous Critical Path execution after task splitting. Related tasks may remain one internal sequence; update a ledger only when handoff, resumption, blocker, deferred work, or high-risk evidence would otherwise be lost.
- Continuous Critical Path execution must stop on blocker, failed verification that cannot be safely recovered inside the current Execution Contract, changed intent, scope expansion, high-risk unconfirmed action, or worktree conflict.
- A failed verification is first a recovery signal, not automatically a handoff stop. If the cause is inside the current Execution Contract and safe to fix, route back to the owning development/debug stage, fix, and re-verify. Stop only when it becomes a natural gate.
- Any flow may complete from fresh verification in the current owner when no handoff, deferred item, or unresolved risk remains. Use `ccdawn-completion-summary` only for cross-stage synthesis, resumed work, formal handoff, or evidence that must persist.
- Do not enter `MERGE_READY` before `ccdawn-pr-review` verifies the diff or PR. `COMPLETED` means the current route's success evidence passed; `MERGE_READY` means integration review passed.

## Flow and Task Mode Gates

BRT and planning decide the flow route only after Owner Arbitration and the Minimal Sufficient Solution Gate. Complexity means the work still required after checking no-build, local reuse, standard/native capabilities, and installed dependencies; file count alone is not complexity.

- `FAST_PATH`: one remaining low-risk implementation unit, reversible, locally verifiable, and finishable in one pass. A few files with the same mechanical replacement still count as one unit. Use light implementation and necessary verification.
- `COMPACT_FLOW`: multiple related work units remain under one theme and fit one reasoning context. Enter task splitting only when it changes dependencies, ownership, risk, or verification.
- `FULL_FLOW`: real design choices, cross-boundary contracts, unclear sequencing, or state/API/security/data/migration/release risk remain after simplification. FULL controls risk; it does not require every workflow stage.

Do not assign `SIMPLE` or `BDD_TDD` to the whole user request.
Do not assign either mode to an experiment lane whose expected metric result is unknown.

Planning is not the default owner or a mandatory bridge to implementation. Enter it only when a persistent/reviewable plan has value beyond the model's internal execution outline.

Self-assess process weight before routing:

- Use intent confidence before asking: `HIGH` acts, `MEDIUM` acts with stated assumptions, `LOW` asks or probes, `BLOCKED` asks one blocking question.
- If there are multiple intents, choose `COMPACT_FLOW` when they share a theme and can be ordered in one context; choose separate routing only when owner, risk, deliverable, or verification truly differs.
- If the main value is adding a complex feature where external or internal reuse may change the plan, route to `ccdawn-feature-reuse-research` before `ccdawn-planning`.
- If the main value is an AI/ML research question, paper/repository baseline reproduction, hypothesis-driven ablation, multi-round findings synthesis, or direction selection, route to `ccdawn-ai-research-loop`.
- If the main value is one already-defined measurable candidate, benchmark/leaderboard feedback, online/offline calibration, worker lane, or submission package, route to `ccdawn-score-loop`; return its research signal to `ccdawn-ai-research-loop` when that owner initiated the lane.
- If an important result is about to become an active baseline, paper/report claim, surprising conclusion, or high-cost direction change, route to `ccdawn-research-rigor-review` before accepting it.
- Do not send an experiment lane through `ccdawn-task-splitting` merely because its code spans modules, its run failed, or its score regressed. Split only a detached deterministic engineering defect; keep candidate evaluation with score-loop.
- If the main value is extracting unclear intent or refining a rough idea, keep `ccdawn-brt` as the owner unless an installed interview/refine skill can produce a better intent contract.
- If the main value is a bounded implementation, first collapse repeated mechanical edits into one FAST_PATH unit. Use incremental slices or `ccdawn-task-splitting` SIMPLE tasks only when independent work units remain before escalating a complex subtask to BDD/TDD.
- If the main value is high-risk confidence checking, code simplification, git/release/deploy, issue/spec intake, MCP/tool integration, webapp testing, logs, or LLM traces, route to the matching installed specialized skill; otherwise use the fallback in `github-skill-candidates.md`.
- If the main value is frontend UI/design, browser control/runtime verification, development standards/spec/source-doc alignment, CI failure repair, GitHub PR comment handling, Sentry/production triage, security hardening, performance profiling, API contract design, migration/deprecation, or observability, route to the matching installed specialized skill; otherwise use the fallback in `github-skill-candidates.md`.
- If the main value is Kaggle-specific competition workflow, route through `ccdawn-competition-research-lifecycle`; let it delegate research direction to `ccdawn-ai-research-loop` and concrete metric lanes to `ccdawn-score-loop`.
- If the main value is creative ideation, pick an installed creative method router only when present; otherwise route to `ccdawn-creative-toolbox`.
- If the main value is judgment, comparison, or audit, route to the most specific existing review skill; use `ccdawn-evaluation` only when none fits.
- If the main value is project health, architecture, technical debt, test gaps, onboarding, or risk-module triage, route to `ccdawn-project-review`.
- If the main value is diagnosing a failing behavior, route to `systematic-debugging`; use `ccdawn-bug-review` only when CCDawn handoff/ledger is needed.
- If the main value is reviewing a PR/diff/branch before integration, route to `ccdawn-pr-review`.
- If a step does not change outcome, reduce it: skip planning, keep `NO_SPLIT` internal, compress ledger, or remain in `FAST_PATH`.
- Prefer outcome gates over method gates: require scope, safety, evidence, and recovery; let the current model choose the shortest sound method.
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

`ccdawn-brt` or `ccdawn-planning` first decides whether splitting has value. `NO_SPLIT` routes directly to implementation without loading another skill. `ccdawn-task-splitting` owns only the `SPLIT` artifact when multiple dependent deliverables, distinct owners, independent risk gates, parallel lanes, cross-session handoff, different verification contracts, or user-requested decomposition remain.

- `SPLIT`: create only the minimum subtasks needed by those boundaries and classify each as `SIMPLE` or `BDD_TDD`.
- Experiment lane: bypass this engineering classification and stay with `ccdawn-score-loop`; only a separated deterministic defect may return as a SIMPLE/BDD_TDD subtask.

Inside `SPLIT`, upgrade a subtask to `BDD_TDD` only when at least one signal is present:

- behavior is new or ambiguous enough that a one-pass implementation is likely to drift;
- failure path, state transition, persistence, permission, migration, API, or integration contract matters;
- deterministic engineering change spans multiple modules or depends on staged refactoring;
- existing deterministic software bug is not localized or has already regressed;
- verification requires a new behavior test to be trustworthy;
- user explicitly asks for strict BDD/TDD.

Keep a subtask `SIMPLE` when it is localized, has clear expected output, has no risky state/API/data change, and a direct verification command or structural check is enough.

## Workflow Ledger

Maintain a compact ledger only when work is long-running, resumed, blocked, handed across agents/stages, or has deferred items that would otherwise be lost. File count and reply count alone do not trigger a ledger.

Minimum fields:

```text
Workflow Ledger:
- Confirmed Intent:
- Intent Rationale:
- One-Turn Alignment:
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
- When a recommendation, route, plan, or execution order changes, update `Intent Rationale` with user signal, inference, recommendation reason, and risk if wrong.
- When a user turn can be resolved with a default recommendation, preserve `One-Turn Alignment`: intent mirror, agent action preview, non-goals, success evidence, correction point, and default next action.
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

- `ccdawn-brt`: `Current Stage`, `Intent Rationale`, `One-Turn Alignment`, `Intent Bundle`, `Route Contract`, `Action Queue`, `Decisions`, `Assumptions`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-planning`: `Current Stage`, `Intent Bundle`, `Accepted Plan`, `Decisions`, `Assumptions`, `Unresolved Risks`, `Recommended Next Stage`.
- `ccdawn-feature-reuse-research`: `Current Stage`, `Reuse Decision`, `Candidate Evidence`, `Rejected Alternatives`, `Verification Strategy`, `Recommended Next Stage`.
- `ccdawn-score-loop`: `Current Stage`, `Baseline`, `Metric`, `Lane`, `Score Evidence`, `Gate Decision`, `Calibration Lesson`, `Recommended Next Stage`.
- `ccdawn-ai-research-loop`: `Research Question`, `Active Baseline`, `Current Evidence`, `Direction Decision`, `Next Experiment`, `Stop Condition`.
- `ccdawn-research-rigor-review`: `Verdict`, `Findings`, `Allowed Claim`, `Missing Evidence`, `Minimal Strengthening Action`, `Route Out`.
- external candidate route: `Current Stage`, `Candidate Skill`, `Installed?`, `Fallback Owner`, `Evidence Needed`, `Recommended Next Stage`.
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

The current owner may mark a FAST_PATH or bounded COMPACT_FLOW implementation `COMPLETED` when fresh success evidence passes. `ccdawn-completion-summary` owns FULL_FLOW, resumed, cross-stage, or formal handoff completion synthesis. Only `ccdawn-pr-review` can mark a PR or diff `MERGE_READY`.

Runtime owns the state transition; the stage skills own the detailed criteria.

- Do not mark `COMPLETED` without fresh evidence from the current route; require `ccdawn-completion-summary` only for FULL_FLOW, resumed, cross-stage, or formal handoff work.
- Do not mark `MERGE_READY` without `ccdawn-pr-review` evidence.
- If evidence is missing, stale, or contradicted by the diff, route to the owning stage instead of claiming readiness.
- If the gap is fixable inside the current Execution Contract, recommend the recovery route; if it requires new scope, permission, or intent change, stop at the natural gate.
