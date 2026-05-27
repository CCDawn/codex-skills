---
name: huawei-nslb-score-loop
description: Use when optimizing, benchmarking, packaging, comparing baselines, handling online score feedback, or coordinating parallel agents for the Huawei Algorithm Challenge 37 NSLB project in C:\Users\17533\Documents\New project 5.
---

# Huawei NSLB Score Loop

Use this skill only for the Huawei Algorithm Challenge 37 NSLB workspace:

`C:\Users\17533\Documents\New project 5`

It narrows general autoresearch behavior to this contest: one C++17 submission file, local proxy benchmarks, a baseline ledger, daily online submission limits, and online score feedback that overrides local proxy optimism.

The operating model is Harnessed Grandmaster Exploration: bold search, strict execution. Search, imagination, and risk-taking should stay broad; execution must stay isolated, recoverable, and evidence-producing. The skill should prevent wrong execution, not timid thinking. Many radical hypotheses may be explored in parallel, but only one fully verified candidate can update the active baseline.

Rationality rule: harden the harness, not the imagination. Fix contradictions in execution rules instead of adding creativity gates. If a worker has a bounded experiment, assigned workspace, stop condition, and result contract, it should be allowed to run even when the idea is unusual or under-theorized. If its own lane needs a concrete witness/target artifact and the artifact does not exist, the correct outcome is `needs-more-evidence` or `blocked-by-missing-witness` with current evidence, not an invalid epoch. Treat format variants such as `basedOn` as an object and suite names with underscores/spaces as equivalent when the meaning matches.

## Primary Objective

Primary objective:

```text
Harnessed Grandmaster Exploration:
Explore like a top leaderboard competitor; execute like a safety harness.
Constrain execution errors, evidence gaps, state corruption, and promotion.
Do not constrain imagination, mechanism search, role shape, or risk appetite.
```

The skill is successful when agents naturally follow this loop:

```text
bold hypothesis -> isolated first-kill test -> current evidence -> lesson or candidate -> memory update -> next hypothesis
```

It is unsuccessful when agents spend the round satisfying templates, role quotas, or paperwork while avoiding executable experiments.

## Rule Layers

Hard constraints protect execution integrity only:

- main-workspace source safety and source drift classification
- worker isolation and absolute workspace patch boundaries
- serial writes to pool, ledger, weights, dataset ledger, mutation space, and submission map
- every manifest lane recovered as completed, completed-invalid, retired, or cancelled with a blocker
- no promotion/package from missing current evidence, stale evidence, unverified combined patches, or online-regressed branches
- real online feedback must be recorded and must not move online-best unless it truly improves
- upload zip names stay short; long metadata is persisted in `docs/submission-map.json`

Soft constraints guide search but must not block execution by themselves:

- validation thesis quality
- negative controls
- same-case counterfactual witnesses
- dataset-evolution lanes
- expert role coverage
- Phase A/B portfolio shape
- freeform/template ratios
- minimum idea score
- presence of a risk gatekeeper

Risk escape keeps search alive under stagnation:

- a controlled-risk, architecture, or 044-style exploit lane may run with imperfect validation if it is isolated, compile-checked where applicable, first-kill scored, and records a reusable lesson
- a risky lane can fail locally and still be useful if it narrows the search space
- missing validation evidence should downgrade promotion confidence, not cancel unrelated bold lanes

Promotion remains strict. Exploration is permissive; baseline updates are not.

## Search Freedom And Harness Boundaries

Do not over-constrain idea generation. Workers may propose unusual architectures, high-variance mechanisms, new proxy objectives, and aggressive local probes. The coordinator's job is not to make every idea safe before it is imagined; it is to make every execution reversible and every failure informative.

Idea generation must not start from a fixed menu of lanes. Use the menu only as fallback or harness scaffolding. The default order is:

1. Diverge: create a pool of non-template hypotheses by combining online-positive mechanisms, online-neutral controls, current source structure, PDF legality, scorer components, and recent failed lessons.
2. Challenge: score each idea for online explanation, novelty, duplicate risk, smallest decisive test, runtime/source safety, and whether it can produce current evidence.
3. Converge: select one attack thesis, then choose a dispatch portfolio that contributes to that thesis. Prefer varied causal mechanisms over role coverage. A portfolio with five different templates but one repeated causal idea is bad; a portfolio with five different causal ideas and no generic gatekeeper is acceptable if each lane has its own stop condition.
4. Dispatch: only after convergence, convert selected lanes into isolated workers with baseline hash, workspace, kill condition, and `child_result.json` contract.

Templates are useful names for recurring responsibilities, not a substitute for thought. If an idea board mostly contains old stock lanes, the coordinator must either regenerate with freeform divergence or manually narrow it before dispatch.

Hard boundaries are execution harness rules:

- Do not let a worker edit the main project `src/Solution.cpp`; worker edits stay inside isolated workspaces.
- Do not launch a worker without a lane id, assigned workspace, baseline hash, stop condition, and expected `child_result.json`.
- Do not leave ready/active workers unrecovered. Every manifest lane ends as completed, completed-invalid, retired, or cancelled with a blocker.
- Do not write `pool_state.json`, ledger, weights, mutation space, submission map, or dataset ledger in parallel.
- Do not promote or package from stale evidence, missing child results, source drift, or an unverified combined patch.
- Do not repeat a failed direction silently. Repetition is allowed only when the new hypothesis names what causal variable changed.

Everything else is negotiable. A risky idea may run if it is isolated, bounded by a first-kill test, and records a reusable lesson.

Do not convert soft constraints into hidden hard gates. Missing dataset lanes, weak validation theses, uneven role coverage, low portfolio beauty, or unusual architecture shape may lower confidence or add warnings, but they must not suppress a bounded worker when source/workspace safety is clean.

## Attack Thesis Loop

When recent epochs produce no promotion path, do not let the loop end at "missing witness" prose. Turn the missing evidence into the next executable attack thesis, or pivot the thesis when the same missing-evidence track has already been spent.

Attack thesis is dynamic. It should be inferred from the selected portfolio, not forced into the baseline-044 residual envelope. Valid thesis families include:

- counterfactual evidence portfolio: same-case scorer movement or bounded empty-search proof.
- architecture breakout portfolio: new solver subsystem, search-policy, local repair pipeline, scorer surrogate, or moonshot basin probe.
- online-confirmed exact-neighbor exploit portfolio: one proven online-positive mechanism, one exact neighboring shape, forensic-before-patch.
- validation repair portfolio: dataset/proxy/negative-control calibration after online/local disagreement.
- hidden-objective reframe portfolio: objective model, upload-budget decision, or dataset-candidate decision after second-order stagnation.
- mechanism divergence portfolio: several independent causal mechanisms under the same execution harness.

If the current thesis is counterfactual evidence, the witness lane may output one of:

- `counterfactualWitnesses`: records with `caseId`, `flowId`, `baselinePort`, `alternativePort`, component deltas for `phase_inner`, `phase_between`, `job_between`, `max_single`, `max_global`, `scoreDelta`, and legality/runtime notes.
- `witnessSearchSummary`: bounded empty-search proof with searched case, flow count, alternative count, and the component reason every alternative failed.

The risk sidecar may be an R2/R3 architecture, scorer-moving mutation, or any bounded free edit lane. It does not have to wait for the witness lane if it is isolated, reversible, compile-checked, first-kill scored, and records a reusable lesson.

Do not run another epoch whose only new result is "we still need exact comparator evidence." Either produce the witness artifact, prove the searched space is empty, or demote witness to support and pivot toward architecture, objective-reframe, search-policy, or validation-repair lanes.

## Grandmaster Validation Doctrine

Borrow the Kaggle grandmaster rule: trust validation only after making validation trustworthy. Local benchmark score is not truth, and online leaderboard score is not an oracle. Treat the online score as an expensive, sparse, noisy extra validation fold that calibrates the local suite.

Validation hierarchy:

1. Mechanism-level validation: prove the candidate moves the intended scorer component or solver decision on the same case.
2. Offline fold validation: test the smallest relevant proxy suite that historically predicts online movement for this family/mechanism/shape.
3. Negative-control validation: compare against online-neutral/down shapes so the candidate is not merely improving a known proxy trap.
4. Online fold validation: use the real leaderboard result to update weights, dataset candidates, and future trust.

Rules:

- Do not ask "did local score go up?" before asking "is this validation fold representative of the hidden objective?"
- Public/online feedback should update the validation model, not replace it. One online score can confirm, contradict, or reduce trust; it should not blindly define the next local objective.
- Every serious candidate must name its validation thesis: which local evidence should predict online movement, which online feedback records support that belief, and what result would falsify it.
- When local and online disagree, first repair the validation fold or dataset candidate, then continue mutation. Do not keep stacking code on a proxy that just lied.
- When validation is weak but exploration is valuable, run the lane as isolated diagnostic/controlled-risk work and record it as evidence, not as promotion proof.
- Public/online score can be used like a held-out fold for model selection, but repeated adaptive probing can overfit it. Spend upload budget on one named hypothesis at a time.

Kaggle-style experiment system:

- Maintain out-of-fold thinking: every local suite/case family is a fold with a trust weight learned from online feedback.
- Maintain negative controls: a candidate should ideally beat or preserve online-positive shapes while rejecting known online-neutral decoys.
- Maintain an idea library: read winning approaches, previous attempts, and similar mechanisms as inspiration, then translate them into this solver's legal moves.
- Maintain ensemble/composition discipline: two neutral components may combine, but only test the combination as a new hypothesis with same-case component evidence. Never bundle because both looked locally harmless.
- Maintain hill-climb discipline: small verified improvements are useful, but stagnation should trigger broader architecture/search-policy ideas, not endless threshold grinding.

## Skill Call Router

When the user invokes `$huawei-nslb-score-loop`, a slash-style command that names this skill, or a short request such as "status", "prepare epoch", "close epoch", "gate child", "rank children", "online update", or "check idea", route it through this skill directly. Do not create a separate plugin or command package for these operations.

Default project:

```powershell
$project = "C:\Users\17533\Documents\New project 5"
$tool = "C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py"
```

Supported skill intents:

```text
doctor:
  Run `score_loop_tools.py doctor`. Treat a score below 9.5 as a harness warning, not an automatic creativity ban. Only source drift, missing ledger/baseline, unsafe main-workspace edits, or unrecoverable worker/pool state should stop edit lanes. Dataset backlog, duplicate risk, or weak idea-board quality should redirect lanes toward learning, not freeze search.

drift:
  Run `score_loop_tools.py drift`. Classify whether src/Solution.cpp is clean, matches a known baseline snapshot, or is unrecorded source drift.

restore-online-best:
  Run `score_loop_tools.py restore-online-best`. Preview restoring src/Solution.cpp from the best-known online baseline snapshot. Use `--write --update-ledger` only after reviewing the backup path and intentionally returning both source and currentBaseline to online-best.

init-weights:
  Run `score_loop_tools.py init-weights`. Seed docs/online-offline-weights.json from ledger onlineEvaluations; use --write only when the explicit weight file should be created.

run-epoch [run-id]:
  Run `score_loop_tools.py run-epoch`. It performs online-best/source-safety checks and prepares an epoch in one command. For broad autonomous work, first generate `idea-board --write`, then pass the written board with `run-epoch --idea-board <board.json>` or `prepare-epoch --idea-board <board.json>`. If active baseline is not best-known online, it emits diagnostic commands instead of opening edit lanes unless `--allow-online-unconfirmed` is explicit.

dispatch-epoch <run-dir>:
  Run `score_loop_tools.py dispatch-epoch --phase auto`. Convert an epoch manifest into a phase-gated ready/not-ready worker dispatch queue with prompt paths, compact worker_context.json paths, workspaces, baseline hash checks, spawnAgent contracts, and persistent pool_state.json when --write is used. Default auto dispatches Phase A diagnostic/review lanes first and blocks Phase B edit/exploit lanes until Phase A has schema-valid current evidence.

collect-epoch <run-dir>:
  Run `score_loop_tools.py collect-epoch`. Summarize worker completion, validate child_result files against lane manifests, rank completed lanes, and update pool_state.json when --write is used. Manifest lanes are canonical; stale workspace directories outside the manifest must not create missing-child noise.

pool-update <run-dir> <lane> <status>:
  Run `score_loop_tools.py pool-update` after spawning, blocking, completing, or retiring a worker. This keeps `pool_state.json` aligned with real subagent ids and prevents duplicate dispatch. Use `--clear-blocker` whenever a previously blocked lane is manually activated or completed.

phase-transition <run-dir>:
  Run `score_loop_tools.py phase-transition --to-phase B --reason "<Phase A current evidence>" --write` before launching any Phase B worker after Phase A. This records the coordinator decision, clears stale phase blockers, and marks eligible Phase B lanes ready. If Phase B is manually narrowed without this transition, close-epoch must report a protocol warning.

pool-retire <run-dir>:
  Run `score_loop_tools.py pool-retire --completed`. Retire completed worker lanes from `pool_state.json` after their results have been collected and learned.

learn-from-children <run-dir>:
  Run `score_loop_tools.py learn-from-children`. Extract fingerprints, positive/negative patterns, avoidNextTime lessons, and proposed mutation-space/index updates from child_result files. Dry-run first; use --write-index and --write-mutation-space only after coordinator review.

archive-attempt <child_result.json>:
  Run `score_loop_tools.py archive-attempt`. Convert one validated child_result into a ledger successful/failed experiment record. Dry-run first; use --write only after coordinator has accepted the bucket and lesson. If the child belongs to an epoch, manifest lane metadata is canonical for family/mechanism/shape. If epoch closeout rejected or marked the result needs-more-evidence, accepted archive requires `--manual-override --override-reason "<why parent gate overruled closeout>"`.

register-submission <short.zip>:
  Run `score_loop_tools.py register-submission` before handing a package to the user for upload. The uploaded zip filename must be short, normally `subNNN.zip`; store the full attempt id, family, mechanism, shape, basedOn, and predicted direction in `docs/submission-map.json` instead of the filename.

online-feedback <raw leaderboard text>:
  Run `score_loop_tools.py online-feedback` when the user pastes raw online feedback such as a zip name, timestamp, score, and `success`. Prefer this over asking the user for attempt/family/mechanism/shape. It parses the short zip name, looks up `docs/submission-map.json`, then delegates to `online-update`. After real feedback, also run `dataset-status`; if the result is neutral/down or contradicts local proxy evidence, create or update a dataset candidate with `dataset-suggest`.

dataset-status:
  Run `score_loop_tools.py dataset-status`. Summarize `docs/dataset-evolution-ledger.json`: pending candidates, validated/promoted proxy candidates, frozen traps, and the next dataset action.

dataset-suggest:
  Run `score_loop_tools.py dataset-suggest`. Convert online feedback or a worker `datasetCandidate` into a durable offline dataset candidate. Use this when local proxy gain is online-neutral/down, when a worker generates new cases, or before changing benchmark gates.

dataset-validate:
  Run `score_loop_tools.py dataset-validate`. Check a dataset candidate has source online feedback, positive records it preserves, neutral/down records it rejects, artifact/generated-case evidence, and promotion-gate impact. Use `--write` only after reviewing the validation result.

dataset-promote:
  Run `score_loop_tools.py dataset-promote` to mark a validated dataset candidate as usable proxy evidence, or `dataset-promote --freeze` to record it as a negative/trap pattern. This is metadata promotion; actual benchmark code changes still require coordinator review.

validate-child <child_result.json>:
  Run `score_loop_tools.py validate-child`. Reject malformed child results before ranking or gate-decision. Add `--run-dir <epoch-dir> --strict` when validating a real worker result so baseline hash, basedOn, allowed files, required lane suites, required artifacts, and counterfactual-witness evidence are checked against epoch_manifest.json. `--project` is accepted for command-shape compatibility but does not mutate project state.

audit-skill:
  Run `score_loop_tools.py audit-skill`. Check that CLI commands and the skill router are still aligned after edits.

reweight-mutations:
  Run `score_loop_tools.py reweight-mutations`. Use online/offline family weights to adjust mutation-space direction states; dry-run first, write only after review.

status:
  Run `score_loop_tools.py status`, then summarize baseline id, source hash match, online-best state, and warnings.

idea-board:
  Run `score_loop_tools.py idea-board`. Generate ideas in two stages: first a freeform non-template divergent pool, then an evidence-based convergence review that selects dispatchable lanes and writes a dynamic `attackThesis`. The board should include project memory, successful/failed ledger lessons, online/offline weights, dataset-evolution candidates, frozen patterns, recent online feedback, `divergentPool`, per-idea quality scores, evidence anchors, `convergenceReview`, `attackThesis`, `attackDoctrine`, `validationDoctrine`, stagnationMode, and a portfolio qualityGate. Do not treat stock lanes such as generic risk gatekeeper, generic controlled-risk mutation, generic dataset candidate, or generic architecture breakout as the idea step itself; they are harness or fallback lanes. Freeform share, role coverage, dataset coverage, and portfolio shape are soft goals. QualityGate is a harness check: hard failures are only missing lane ownership, workspace/hash safety, stop conditions, or recoverable child-result boundaries. Use `--write` when the board will guide a real epoch. Dataset-evolution lanes are recommended when feedback is neutral/down, but they are not allowed to block a strong exploit, architecture, controlled-risk, or bounded free edit lane by themselves. If recent epochs are safe but stagnant, selected lanes should preserve mutation pressure through at least one bounded risk/architecture/044-style/free-edit lane when safe. If counterfactual witness work has already saturated, witness lanes should become support or pivot evidence instead of the default main thesis. Use `--force-stagnation` for validation or an explicit strategic reset. Use `--prefer-044-mode` when the coordinator wants the baseline-044 playbook to be prioritized, not made exclusive. Use `--template-only` only for regression testing the old behavior.

prepare-epoch [run-id]:
  Run `status` first. If clean, run `prepare-epoch` with the optional run id. If an expert idea board exists, use `--idea-board <docs/idea-boards/*.json>`; otherwise the epoch falls back to mutation-space lanes. Report manifest path, lane count, qualityGate state, phase split, workspace paths, worker_context.json paths, harnessWarnings, and which prompts are eligible for dispatch. Expert epochs are invalid only for hard harness failures: missing lane ownership/workspace/hash, missing smallestDecisiveTest/killCondition, missing recoverable child_result contract, or stale baseline mismatch. Advisory warnings should be shown to the coordinator but must not suppress bold lanes by themselves.

close-epoch <run-dir|epoch-id>:
  Resolve epoch ids under `tmp/score-loop-epochs/`, run `close-epoch --write`, and summarize winners, rejects, missing child results, and next parent gate. A valid closeout can still be `reject`, `needs-more-evidence`, or `no-results`; those are completed learning epochs, not command failures. If it returns `invalid-epoch`, do not end the conversation; continue the controller loop until every manifest lane is completed, fixed, or explicitly cancelled with a reason.

rank-children <run-dir>:
  Run `rank-children` and report ranked candidates by evidence quality. Do not promote from ranking alone.

gate-child <child_result.json>:
  Run `gate-decision`; report decision, parent gate commands, strengths, and risks.

online-update <attempt> <score> <family> <mechanism> [shape]:
  First dry-run `online-update` and explain the family/mechanism/shape calibration effect. Use `--write` only when the user confirms the score is real. Add `--write-ledger` only for real online feedback that should append docs/optimization-ledger.json.onlineEvaluations. Add `--accept-best-update` only when the attempt is accepted as the new best-known online baseline.

check-idea <hypothesis>:
  Run `check`; if it is near-duplicate, require a new causal mechanism or guard before opening an edit lane.
```

If a user writes a command-like phrase without full arguments, infer the safe defaults where obvious; otherwise ask only for the missing value that changes filesystem writes or online calibration. Read-only status, index, check, suggest-lanes, idea-board, epoch-board, rank, and gate operations may run immediately.

The skill-level router is the canonical "slash command" surface. Any old local plugin named `nslb-score-loop-commands` is obsolete and should not be used as the source of truth.

Before any autonomous run, execute:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py doctor --project "C:\Users\17533\Documents\New project 5"
```

If the doctor score is below 9.5, classify the failed checks. Hard-stop only for source/baseline integrity, missing canonical ledger, unsafe worker isolation, or pool state that cannot be recovered. For softer issues such as dataset backlog, duplicate-risk backlog, or low idea-board quality, continue with a harnessed epoch that explicitly targets the issue or runs bounded exploration with a first-kill test.

If active baseline is not the best-known online baseline, treat it as a yellow gate even when source hash is clean. Default `run-epoch` should not open exploit/edit lanes from that branch. Choose one:

- restore online-best with `restore-online-best --write --update-ledger`
- run diagnostic/proposal-only work
- explicitly use `--allow-online-unconfirmed` for a small, bounded epoch

If source drift exists, run `drift` before any `prepare-epoch` or `run-epoch --allow-dirty`. Dirty runs must include a concrete `--drift-classification` and should stay diagnostic-only unless the drift has been recorded as an attempt.

When the drift is not intended to become a new attempt, restore the online-best snapshot in two phases:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py restore-online-best --project "C:\Users\17533\Documents\New project 5"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py restore-online-best --project "C:\Users\17533\Documents\New project 5" --write --update-ledger
```

The write path backs up the current drift source under `docs/drift-backups/` before copying the baseline snapshot to `src/Solution.cpp`. `--update-ledger` also moves `currentBaseline` to the restored baseline record so source and ledger do not diverge.

## Required Context

Before any optimization or packaging work, read:

- `AGENTS.md`
- `.docs/project-memory/INDEX.md`
- `.docs/project-memory/memory.json`
- `.docs/project-memory/profile.json`
- `.docs/project-memory/lanes/competition-huawei-nslb.json`
- `docs/competition-taskbook.md`
- `docs/optimization-workflow.md`
- `docs/optimization-ledger.json`
- `docs/dataset-evolution-ledger.json`
- `docs/official-pdf-rules.md`

Then inspect current code state:

- `git status --short`
- current baseline id, hash, scores, known weaknesses from `docs/optimization-ledger.json`
- SHA256 of `src/Solution.cpp`

Never reason from stale chat memory when these files exist.

## Memory Durability Contract

Treat durable project files as the memory system; chat history is only a convenience layer.

Canonical memory layers:

- `docs/optimization-ledger.json`: source of truth for current baseline, successful/failed attempts, duplicate fingerprints, `avoidNextTime` lessons, and real online evaluations.
- `docs/online-offline-weights.json`: online feedback calibration for family, mechanism, and shape weights. This file decides whether local proxy gains should be trusted less or more next time.
- `docs/dataset-evolution-ledger.json`: dataset-candidate memory for dynamic offline-suite evolution. It tracks which generated/proposed proxy cases came from online feedback, what positives they explain, what neutral/down branches they reject, and whether they are candidate/validated/promoted/frozen.
- `docs/submission-map.json`: short upload filename to full attempt metadata mapping. Use this so online zip names stay upload-safe while feedback can still be auto-calibrated.
- `docs/exploration-index.json`: child-agent learning index written by `learn-from-children --write-index`. It captures worker fingerprints, lessons, retry policies, and duplicate avoidance beyond the main ledger.
- `references/mutation_space.json`: skill-level search prior, including bounded families, knobs, disabled lanes, and `frozenPatterns` learned from repeated failures.
- `tmp/score-loop-epochs/<run-id>/epoch_manifest.json`, `pool_state.json`, and `epoch_closeout.json`: per-epoch trace for lane intent, worker ownership, validation, ranking, retirement, and final gate decisions.
- `.docs/project-memory/*.json` and `.docs/project-memory/*.html`: human-readable project memory and dashboard. Use it for situational awareness, but do not let it override the ledger, weights, source hash, or online feedback.

Required write points:

- Before giving the user an online upload package: keep the upload filename short, normally `subNNN.zip`, and run `register-submission --write` to persist the long attempt metadata in `docs/submission-map.json`.
- After a worker finishes: run `validate-child --run-dir <epoch-dir> --strict`, then `collect-epoch --write`.
- After collecting an epoch: run `learn-from-children`; use `--write-index` for accepted child-result lessons and `--write-mutation-space` for repeated rejected patterns that should be frozen.
- After accepting a child attempt into history: run `archive-attempt --write` so successful and failed experiments are both searchable by `index`, `check`, `suggest-lanes`, and `doctor`.
- After a real online score: if the user pasted raw leaderboard feedback, run `online-feedback --write --write-ledger --auto-accept-best`; it should infer metadata from `docs/submission-map.json`. Use manual `online-update --write --write-ledger` only when no package mapping exists. Then run `dataset-status`; if the feedback is neutral/down or local proxy evidence was misleading, create or refresh a `datasetCandidate` with `dataset-suggest --write`.
- After a worker produces new proxy cases or a dataset-evolution lane finishes: run `validate-child --strict`, then `dataset-suggest --source-child-result <child_result.json> --write`, then `dataset-validate --candidate-id <id> --strict --write`. Do not treat generated cases as promotion gates before validation.
- After restoring online-best: use `restore-online-best --write --update-ledger` so source and ledger converge.

Reliability rule: if `doctor` reports a missing canonical ledger/baseline/source layer, do not launch unattended exploit lanes. If optional memory layers or dataset ledgers are stale, launch lanes that either repair the layer or continue bounded exploration while recording the gap.

## Active Baseline Rule

`docs/optimization-ledger.json.currentBaseline` is the source of truth.

- New experiments must start from the active baseline snapshot.
- If `src/Solution.cpp` differs from `currentBaseline.sourceSha256`, stop and identify whether this is an unrecorded user/agent experiment.
- Do not overwrite or revert untracked user work without understanding it.
- Do not stack a new attempt on top of a rejected or online-regressed attempt.

As of this skill's creation, the known active line is `baseline-006-official-hot-source-allocator`, but always trust the ledger over this sentence.

## Experiment Loop

Each attempt must have one primary strategy. Write down before editing:

- attempt id
- based-on baseline
- hypothesis
- expected case/family improvement
- predicted risk
- files to touch, normally only `src/Solution.cpp`

Default scope is narrow. Avoid broad rewrites, multi-strategy bundles, and large unused templates because the official environment has tight compile/runtime constraints.

## Parallel Experiment Mode

Use this mode when the user asks for multi-agent work, parallel experiments, independent hypotheses, search branches, or faster score exploration.

Coordinator responsibilities:

1. Read the required context and active baseline first.
2. Start each epoch with 1-2 proposal-only lanes before edit lanes when the next weakness is unclear.
3. Create a short experiment board with 3-6 independent lanes.
4. Assign each lane a unique attempt id, one hypothesis, one expected affected case family, and a strict file scope.
5. Tell subagents they may inspect the whole project but must not promote, package, submit online, or edit shared ledger/memory directly.
6. Prefer isolated worktrees or copied workspaces for concurrent edits. If the environment cannot create isolated workspaces, run subagents as proposal-only reviewers and apply one patch at a time in the main workspace.
7. Merge candidates only after comparing their exact diffs and measurements against the active baseline.

Patch boundary contract:

- The main project root is read-only for workers. Only the coordinator may edit `C:\Users\17533\Documents\New project 5\src\Solution.cpp`.
- A worker may edit only files under its assigned isolated workspace path from `epoch_manifest.json`.
- `apply_patch` does not inherit a shell command `workdir`. Workers must not use relative patch headers such as `*** Update File: src/Solution.cpp`.
- If a worker uses `apply_patch`, every file header must be an absolute path under its assigned workspace, for example `*** Update File: C:\...\tmp\score-loop-epochs\<epoch>\workspaces\<lane>\src\Solution.cpp`.
- After any worker patch, verify both hashes: workspace `src/Solution.cpp` may change, but main project `src/Solution.cpp` must still equal the active baseline hash.
- If the main project hash changes while workers are active, stop the epoch, run `drift`, restore or record the drift, and do not close or promote from that epoch as normal evidence.

Efficient subagent use means increasing independent evidence, not increasing worker count. Before spawning a worker, the coordinator must be able to state what uncertainty that worker reduces. Do not spawn a worker for a task that can be answered by reading the ledger or by asking an existing active worker for a narrower follow-up.

Recommended epoch pattern:

1. `scout`: proposal-only lanes mine the ledger, benchmark deltas, official rules, and rejected attempts for one actionable weakness each.
2. `mutate`: edit lanes apply one tiny change each from the best scout hypotheses, preferably in isolated workspaces.
3. `audit`: one proposal-only lane compares candidate diffs for stale-baseline risk, scope creep, known bad patterns, and online-alignment strength.
4. `promote-or-reset`: the coordinator applies at most one candidate in the main workspace, verifies it, records the result, then starts a fresh epoch from the active baseline.

When generating a new autonomous epoch, prefer the bundled mutation-space board over ad hoc worker prompts:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py idea-board --project "C:\Users\17533\Documents\New project 5" --run-id "<idea-id>" --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py prepare-epoch --project "C:\Users\17533\Documents\New project 5" --idea-board "C:\Users\17533\Documents\New project 5\docs\idea-boards\<idea-id>.json"
```

The idea board reads durable project memory, the ledger, online/offline weights, exploration index, and `references/mutation_space.json`. `prepare-epoch --idea-board` converts `selectedLanes` into canonical manifest lanes and creates isolated workspaces, prompts, and an `epoch_manifest.json` under `tmp/score-loop-epochs/<run-id>`. Mutation-space `epoch-board` is now only a fallback when no expert board exists or the user names a specific bounded mutation.

Hard invalidation rule: if an epoch was intended to be expert-panel driven but `epoch_manifest.json` or any worker prompt contains generic `Test one ... mutation` hypotheses instead of the board's selected hypotheses, stop the epoch as invalid/proposal-only and regenerate with `prepare-epoch --idea-board`.

Use direct implementation without subagents when the task is small, deterministic, and already has a single obvious edit. Use subagents when there are multiple plausible hypotheses, stale-evidence risk, or enough independent case families to justify parallel search.

Subagent lane types that usually help this contest:

- `micro-local`: one tiny C++ change around an already identified weak case.
- `risk-reduction`: remove or guard a known regressive pattern while preserving baseline behavior.
- `case-forensics`: no code edits; inspect benchmark failures and propose one targeted hypothesis.
- `evolution-mutation`: mutate one parameter, threshold, ordering tie-break, allocator choice, or guard condition.
- `benchmark-alignment`: check whether local proxy gains match official/PDF rules and online history.
- `rollback-auditor`: compare a candidate with the ledger and identify hidden stacking or stale-baseline risk.
- `diff-auditor`: review one candidate patch for broad rewrites, bundled strategies, randomness, runtime risk, and known rejected patterns.

Parallel search rules:

- Every lane starts from `docs/optimization-ledger.json.currentBaseline`.
- Never let two lanes write to the same main workspace file concurrently.
- Never let a worker patch the main workspace. Worker patches must target absolute paths inside that worker's assigned workspace.
- Never combine two unverified improvements just because both looked good locally.
- Treat a candidate as a patch plus evidence, not as a new baseline.
- If two candidates improve different families, test each alone first, then test a combined patch as a new independent attempt.
- Keep top candidates by evidence quality: official sample legality, full-suite delta, catastrophic-regression absence, runtime risk, and consistency with online feedback.
- Failed lanes must produce a concrete lesson or guardrail, not just "did not improve".
- A lane must stop early if it discovers the workspace hash is not the supplied baseline, the hypothesis is already rejected in the ledger, or the change requires multiple coupled strategies.
- A worker response is incomplete until it includes baseline hash observed, changed files, commands run, parsed deltas, risks, and a promotion recommendation.

## Speed-First Experiment Protocol

Default autonomous work should optimize for evidence per minute, not maximum local certainty per worker.

Keep speed optimization skill-side by default unless the user explicitly asks for tooling changes. The current project benchmark runner supports safe engineering optimizations that do not change scoring semantics: content-hash compile caching, `--exe` reuse, `--discard-case-files`, and `--plan-suites` overlap analysis. Use these to remove repeated work, but never use them to weaken final promotion evidence.

## Expert Panel Idea Board

Before a new autonomous epoch opens worker lanes, run an expert-panel divergent idea board unless the user supplied a specific narrow hypothesis. This is the default antidote to local-optimum search and repeated guard/threshold tweaking.

The board uses multiple expert roles, all with the same durable context:

- `Online Forensics Expert`: read recent online feedback and infer which hidden shapes are likely present or absent.
- `Algorithm Mechanism Expert`: propose a new single-cause mechanism beyond existing guard/threshold widening.
- `Benchmark/Data Generator Expert`: design proxy cases that explain online feedback and expose local/online mismatch.
- `Dataset Evolution Expert`: turn online feedback into a `datasetCandidate` that can be validated, promoted, or frozen before benchmark gates change.
- `Counterfactual Debugger`: audit solver decision points by replaying second-best or rejected choices.
- `Risk/Runtime Gatekeeper`: veto duplicate, runtime-risky, or under-specified ideas before dispatch.
- `Exploit Strategist`: propose at most one minimal extension of an online-confirmed signal.

Every role must start from:

- `.docs/project-memory/INDEX.md`
- `.docs/project-memory/memory.json`
- `.docs/project-memory/lanes/competition-huawei-nslb.json`
- `docs/optimization-ledger.json`
- `docs/online-offline-weights.json`
- `docs/dataset-evolution-ledger.json`
- `docs/exploration-index.json`
- `references/mutation_space.json`

Every idea must cite the successful lesson it builds on, the failed or frozen lesson it avoids, the online feedback it tries to explain, the smallest decisive test, and the kill condition. If it cannot cite those, keep it proposal-only.

Command:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py idea-board --project "C:\Users\17533\Documents\New project 5" --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py prepare-epoch --project "C:\Users\17533\Documents\New project 5" --idea-board "C:\Users\17533\Documents\New project 5\docs\idea-boards\<written-board>.json" --max-lanes 6
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py dispatch-epoch --run-dir "C:\Users\17533\Documents\New project 5\tmp\score-loop-epochs\<epoch-id>" --phase auto --write
```

Do not drop the written board path. `idea-board --write` is not enough by itself; the next epoch must consume that exact file with `--idea-board`, or the expert hypotheses, context contracts, and kill conditions will not reach child agents.

Generated expert worker prompts must contain:

- `Expert role`
- `Worker type`
- `Why now`
- `Smallest decisive test`
- `Kill condition`
- `Idea quality score`
- `Evidence anchors`
- compact worker context plus durable references to read only if compact context is insufficient
- evidence expectations for successful lesson, failed/frozen lesson, and online feedback when available

If any of these are missing, do not launch workers. Regenerate the epoch from the idea board.

Idea-board quality gate:

- Every idea gets a deterministic `qualityScore` based on required fields, novelty, duplicate risk, online/offline weights, recent online feedback, artifact clarity, and whether it is cheap diagnostic evidence or a bounded patch candidate.
- `selectedLanes` is a portfolio, not the first N ideas. It should preserve useful tension across online evidence, proxy/data thinking, score-moving mechanisms, and execution risk. It does not need every category in every epoch if that would suppress a strong exploit or architecture lane.
- `prepare-epoch --idea-board` should reject only boards that lack harness integrity: missing stop conditions, missing smallest decisive tests, no recoverable worker ownership, or no evidence boundary. Do not reject a board merely because it lacks a dataset lane, has more than one exploit lane, or contains risky architecture.
- Idea quality is a ranking hint, not an execution gate. Only missing hypothesis, smallest decisive test, kill condition, owner/workspace/hash, or child-result boundary should block dispatch.
- The board should write `evidenceAnchors.successfulLesson`, `evidenceAnchors.failedOrFrozenLesson`, and `evidenceAnchors.onlineFeedbackRecord` from compact context when available. Missing anchors reduce confidence but do not block bounded exploration.
- Treat qualityGate as advisory except for hard harness failures. Low portfolio quality should add `harnessWarnings`, reduce rank confidence, or cause the coordinator to add a balancing lane; it should not freeze search when the user asks for risk or when a 044-style exploit/architecture lane is ready.

### Stagnation Mode

The loop is considered stagnant after two recent closed epochs repeatedly end without an eligible parent gate or promotion path, especially when they keep selecting the same template lanes (`online_discriminator-positive_vs_neutral`, `hidden_proxy_generator-online_neutral_decoys`, `risk_gatekeeper-duplicate_and_runtime_filter`, `exploit_strategist-minimal_confirmed_signal_extension`) and only produce `proposal-only`, `reject`, `flat`, `not-dispatched`, or `needs-more-evidence` results.

When `idea-board` sets `stagnationMode.active=true`:

- Treat the old safe board as saturated. Do not spend another round merely restating the baseline-044 phase4-6/job<=24/flow4096 residual envelope.
- `selectedLanes` should favor novelty, but novelty is measured by causal mechanism, not by paperwork. A lane may be novel because it changes architecture, search policy, scorer surrogate, target shape, or exploit path.
- Add expert roles for `Adversarial Proxy Builder`, `Small Exhaustive Enumerator`, `Mechanism Breakout Expert`, and `Promotion Candidate Revalidator`.
- A proxy-generator lane should create a new PDF-legal generator/report or adversarial case set when useful. If it only audits existing benchmark definitions or reuses phase7/job32/jobs22 neutral decoys as positive evidence, mark it diagnostic/rejected, but do not let that invalidate unrelated exploit or architecture lanes.
- A risk gatekeeper may bound exploration and kill duplicates, but it may not veto all mutation. It should allow at least one bounded high-variance artifact/enumeration/mechanism-breakout lane unless source/workspace/runtime safety is genuinely broken.
- Revalidation is allowed for prior tiny positive candidates, but each revalidation must name one missing evidence item and end as promote-through-parent-gate, freeze, or reject.
- A worker that claims a new artifact must prove it exists. `child_result.json` should include `artifactPaths`, `generatedArtifacts`, `newArtifacts`, or `currentEvidence` entries with `artifact` / `report` paths under the workspace. Prose-only claims are a lesson, not artifact evidence.
- A dataset-evolution worker that claims dataset progress must include `datasetCandidate` with `candidateId`, `sourceOnlineFeedback`, `caseFamily`, `caseShape`, `hypothesis`, `explainsPositive`, `rejectsNeutralOrNegative`, artifact/generated-case evidence, and `promotionGateImpact`. If it cannot, close as diagnostic without blocking other lanes.
- If two consecutive stagnation-mode epochs still produce no auditable new artifact and no candidate worth parent review, `stagnationMode.escapeLevel` should become `2`; the next board should include an objective-reframe or online-submission revalidation escape lane instead of widening patch size.
- If two consecutive stagnation-mode epochs produce artifacts but no parent-gate path and `dataset-status` shows validated backlog, this is also second-order stagnation. Prefer a dataset decision lane to promote, freeze, reject, or merge validated clusters, but do not let backlog block an unrelated strong exploit or architecture lane.
- If two consecutive stagnant epochs have already spent counterfactual/witness lanes without a parent-gate path, set `witnessSaturated=true`: demote witness lanes to support unless they name a changed target, and raise architecture, search-policy, objective-reframe, online-confirmed exploit, or bounded free edit pressure.

### Controlled Risk Mode

When `stagnationMode.active=true`, the default posture changes from safety-first to controlled-risk-first.

- Each broad stagnation epoch should preserve mutation pressure through at least one bounded edit lane unless source/workspace/runtime safety is genuinely broken. This may be `controlledRiskLane`, architecture, 044-style exploit, or another freeform edit lane with a workspace, baseline hash, smallest decisive test, kill condition, and child-result contract.
- Bounded edit lanes may co-dispatch with Phase A diagnostics. They do not need Phase A to prove a target first; the purpose is to create mutation pressure when diagnosis is stale.
- Risk/Runtime Gatekeeper may narrow the risk lane's blast radius, but it may not block every mutation lane unless active baseline hash/source safety is broken.
- If Phase A artifacts are flat across known baselines, the gatekeeper may cancel duplicate/stale edit lanes, but it must leave either one output-moving discriminator-search lane or one bounded edit/architecture lane alive. Cancelling all edit pressure is allowed only with a recorded source-safety, runtime-safety, or explicit online-budget blocker.
- A negative controlled-risk result is acceptable if it contains `mutationAttempted=true`, `attemptedDiffSummary`, `checksRun`, parsed first-kill score/delta, and an `avoidNextTime` lesson.
- If the first-kill suite is flat/worse, the worker should revert the workspace patch and still record the attempted mutation. Reverted negative attempts are useful evidence; silent non-attempts are invalid.
- The number of concurrent risky lanes is a coordinator budget choice, not a fixed cap. Multiple independent bounded risky lanes may run in isolated workspaces if worker slots, runtime, and duplicate control are clean. The coordinator still applies at most one candidate to the main workspace after collection.

The intent is to trade cheap local failures for search gradient. Do not let process compliance replace scorer movement.

### 044-Style Online-Confirmed Exploit Mode

Use this mode whenever there is an online-confirmed positive mechanism with plausible untested neighboring shapes. Baseline-044 succeeded this way: it extended the online-confirmed large-sparse residual repair family from phase4/phase5 to one exact phase6/flow4096 shape, after a temporary forensic probe proved the target moved.

Command:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py idea-board --project "C:\Users\17533\Documents\New project 5" --write --prefer-044-mode
```

Use this when the loop has become too generic, too dataset-heavy, or too afraid to patch. It is not a conservative guard-tuning mode and it is not exclusive. It simply keeps the proven baseline-044 playbook near the top of the portfolio while architecture and controlled-risk lanes can still run beside it. The worker is free to choose a surprising adjacent target as long as it names one exact shape and proves with a forensic/probe that the output or score can move before applying the patch.

Rules:

- Start from an online-confirmed positive family/mechanism, not from generic local score optimism.
- Pick exactly one neighboring hidden shape or decision surface per worker.
- Before patching, build a temporary forensic comparator, probe, trace, or generated 3-5 case slice that shows baseline vs candidate movement.
- If the forensic is flat, write `child_result.json` as rejected/inconclusive and do not patch.
- If the forensic moves, apply only the minimal single-cause patch needed for that exact shape.
- Do not combine broadening dimensions inside one worker. Boundary expansions such as phase count, job count, flow count, leaf band, or capacity-shadow changes are allowed, but each expansion gets its own lane unless the worker explicitly marks the result as architecture/moonshot rather than 044 exploit.
- The coordinator may dispatch this lane alongside Phase A diagnostics because the forensic-before-patch rule is its own harness.

Required child evidence:

- `currentEvidence` or `evidenceNotes.smallestDecisiveTestResult` describing the forensic/probe.
- Exact target shape and why it is adjacent to the online-confirmed signal.
- `deltasVsBaseline` for the forensic if `promotionCandidate=true`.
- `avoidNextTime` naming which boundary should not be broadened without new online or forensic evidence.

This mode should be preferred over another proxy-only epoch when a strong online-positive mechanism still has unexplored exact neighbors.

### Architecture Innovation Mode

When the user asks to take more risk, or when `stagnationMode.active=true`, the loop should stop acting like a narrow guard tuner and open architecture search.

- `idea-board` should include architectureBreakoutLane lanes in stagnation mode, but the number is a budget choice, not a law. Good lanes change a solver subsystem, search frontier, candidate ranking, rollback policy, or scorer surrogate; bad lanes only rename another threshold/guard.
- Use a risk ladder instead of one rigid budget:
  - `R1`: micro mutation, exactly one first-kill scorer.
  - `R2`: architecture prototype, one solver subsystem, one first-kill scorer and an optional second suite only if the first moves positively.
  - `R3`: moonshot architecture variant, isolated workspace only, prototype quality is acceptable if it is easy to revert.
- Architecture lanes may be rough. They must be isolated, compile-checked, first-kill scored, and recorded with `architectureAttempted=true` plus `architectureSummary`.
- Stagnation mode may select up to four edit lanes and dispatch up to five workers when hypotheses are genuinely different.
- Risk/Runtime Gatekeeper may bound runtime, file scope, and first-kill choice, but it must not collapse architecture lanes back into only diagnostics or only known residual-envelope tweaks.
- Parent promotion remains strict: even if an R2/R3 lane finds a local win, the coordinator applies at most one candidate to the main project and runs the full parent gate before packaging.

Useful commands:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py idea-board --project "C:\Users\17533\Documents\New project 5" --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py idea-board --project "C:\Users\17533\Documents\New project 5" --write --force-stagnation
```

Phase-gated execution is a harness, not an imagination filter:

- Phase A contains diagnostic, review, online-discriminator, hidden-proxy-generator, forensics, and risk-gatekeeper lanes.
- Phase B contains edit, exploit, and code-mutation lanes.
- `prepare-epoch --idea-board` must write lane `phase`, `phasePrerequisites`, `commandBudget`, `timeBudgetMinutes`, `allowedCommands`, and `contextPath`.
- `dispatch-epoch --phase auto --write` is the default. It dispatches only Phase A until Phase A child results contain `currentEvidence` or `evidenceNotes.smallestDecisiveTestResult`.
- Exception: in controlled-risk, architecture-innovation, or 044-style online-confirmed exploit mode, controlled-risk, architecture-breakout, and forensic-before-patch exploit lanes may be ready during Phase A dispatch. This is intentional and should not be treated as a protocol violation; the forensic/first-kill test is the harness.
- Do not manually launch Phase B prompts just because they exist under `prompts/`. Existing prompts are not permission to run.
- After Phase A completes and before launching any Phase B worker, run `phase-transition --to-phase B --reason "<specific currentEvidence summary>" --write`, or rerun `dispatch-epoch --phase B --write`. This is the official handoff record from diagnosis to mutation.
- If the coordinator narrows a Phase B prompt manually, the narrowing must be named in the `phase-transition --reason`, and the corresponding lane blocker must be cleared with `pool-update --clear-blocker` or by `phase-transition`.
- `collect-epoch` and `close-epoch` should surface protocol warnings when a Phase B worker is active/completed/retired without a recorded Phase B transition, or when a completed/retired worker still has blocker text.
- Use `dispatch-epoch --phase all` only as an explicit coordinator override, and record why Phase A was bypassed in the epoch closeout.
- If Phase A evidence changes the target shape, regenerate or narrow Phase B instead of using stale prewritten edit prompts.
- If Phase A was skipped or left `ready`, the epoch is still valid only when the coordinator records why the bypass was intentional, or explicitly cancels unused lanes with a blocker before parent gating or final reporting.

Worker context compression is mandatory:

- Every worker prompt must point to a compact `worker_context.json`.
- The worker reads that JSON first and should not open full `SKILL.md`, full ledger, full project memory, or broad `Solution.cpp` ranges unless the compact context is insufficient.
- The compact context is allowed to carry only the active baseline, online-best metadata, 3-8 relevant successful lessons, 3-8 failed/frozen lessons, recent online feedback, lane hypothesis, kill condition, command budget, command whitelist, and stale-evidence rule.
- If a worker needs more context, it should open one specific file/range and explain why in `currentEvidence`.

Evidence boundary:

- `currentEvidence` means evidence produced in this exact epoch for the lane's smallest decisive test.
- `priorEvidence` means old epoch child results, old chat summaries, or previous benchmark artifacts. It can explain why the lane exists, but it cannot justify promotion by itself.
- A child result with empty `currentEvidence` and non-empty `priorEvidence` must be `proposal-only`, `rejected`, or `inconclusive`, never `promotionCandidate=true`.
- `diagnostic-only` is a lane mode, not a benchmark suite. Any `checksRun` containing `python tools\benchmark.py --suite diagnostic-only` is invalid.
- For any lane with `requiresNewArtifact=true`, strict validation should reject claims of artifact progress when the result lacks auditable artifact evidence. A missing artifact can still be a valid negative lesson if `promotionCandidate=false`.
- For any lane with `requiresCounterfactualWitness=true`, strict validation should require exact same-case witness evidence or a bounded empty-search proof before treating the lane as successful. A bounded empty-search proof must name the searched case, flow count, alternative count, and why every alternative failed.
- For any lane with `requiresDatasetCandidate=true`, strict validation should require a schema-valid `datasetCandidate` only when the worker claims dataset progress. Missing candidate means diagnostic/no-progress, not a reason to invalidate unrelated lanes.
- For any lane with `requiresMutationAttempt=true`, strict validation should require `mutationAttempted=true` or `changedFiles` including `src/Solution.cpp`, plus mutation evidence in `attemptedDiffSummary`, `mutationSummary`, or `currentEvidence`. A failed compile or reverted mutation is valid negative evidence when recorded honestly.
- For any lane with `requiresArchitectureAttempt=true`, strict validation should require `architectureAttempted=true` or `changedFiles` including `src/Solution.cpp`, plus architecture evidence in `architectureSummary`, `attemptedDiffSummary`, or `currentEvidence`, unless the lane explicitly closes as `blocked-by-missing-witness` / `needs-more-evidence`.
- Negative/proposal learning results are valid completions when they are honest, non-promotional, and include currentEvidence or evidenceNotes. They should not be marked `completed-invalid` merely because they failed to find the hoped-for witness, dataset candidate, artifact, or patch. Invalid is for broken harness, malformed result, unsafe file writes, missing baseline/source checks, or unsupported promotion claims.

Selection rules:

- Favor variety, but do not enforce a fixed non-exploit ratio when exploit evidence is strong.
- Multiple exploit lanes may run in one epoch if they target distinct mechanisms or exact shapes and each has its own first-kill/forensic test.
- Each epoch should include at least one online discriminator or hidden proxy generator lane when recent online feedback was neutral.
- Dataset-evolution lanes are useful after neutral/down feedback, but optional in exploit or architecture-heavy epochs. If no valid `datasetCandidate` is created, the epoch may still improve search by producing code, traces, or negative lessons.
- Each autonomous broad epoch should include one risk-gatekeeper/review lane unless the task is a single narrow user-specified hypothesis.
- The selected portfolio should preserve useful tension: one lane asks "what hidden shape are we fitting?", one lane asks "what proxy would expose mismatch?", one lane asks "what mechanism can move score?", and one lane asks "why should we not run this?"
- Risk/Runtime Gatekeeper may block dispatch only for harness failures: missing workspace isolation, missing baseline hash, no stop condition, unbounded runtime, duplicate no-new-cause lane, or unsafe main-workspace write. It should not block imagination because the idea is unusual.
- In stagnation mode, allow up to five active workers and up to four edit/architecture lanes when hypotheses are genuinely different. This loosens exploration, not promotion.

Use a three-stage gate:

1. `smoke`: hash check, compile once, and run the smallest relevant target/diagnostic suite.
2. `screen`: run only the online-aligned guard suite that can disprove the idea, usually `online_fit_core`, `hidden_shape`, or a named forensic suite.
3. `confirm`: only the coordinator runs full/official/pdfstress/runtime on the top schema-valid candidate after collection.

Worker speed rules:

- Default budgets are small on purpose: diagnostic/review/proposal lanes get about 8 shell commands and 20 minutes; edit/exploit lanes get about 12 shell commands and 35 minutes. When the budget is exhausted, the worker writes `child_result.json` instead of continuing to search.
- Diagnostic lanes use the generated `allowedCommands` whitelist. They may read targeted files, use `rg`, inspect small JSON excerpts, run score-loop read-only tools, or run a named benchmark suite if explicitly listed; they must not compile or benchmark broadly unless the prompt names that suite.
- Search output must be bounded. Workers must not run recursive `rg` over `tmp/score-loop-epochs`, `workspaces`, `build`, `dist`, or the whole project root. Use a specific file or narrow directory plus `--glob '!tmp/**' --glob '!build/**' --glob '!dist/**' --max-count 20`. If historical evidence is needed, read `docs/exploration-index.json`, `docs/optimization-ledger.json`, or one named epoch file instead of searching every copied workspace.
- Compile once per candidate and reuse the executable with `python tools\benchmark.py --suite <suite> --exe build\score_loop_candidate.exe --discard-case-files`.
- If the coordinator runs `python tools\benchmark.py --suite <suite>` without `--exe`, the benchmark tool may reuse a content-hash cached executable. This is equivalent to recompiling the same source and is allowed for speed; use `--no-compile-cache` only when diagnosing compiler/cache issues.
- Generated worker prompts must include the concrete compile command `g++ -std=c++17 -O2 -pipe src\Solution.cpp -o build\score_loop_candidate.exe`; if a prompt lacks it, stop and regenerate dispatch instead of letting workers run broad interpreted rebuild loops.
- Do not run `full`, `official`, `pdfstress`, or `runtime` before target evidence moves, unless the lane is explicitly a runtime lane.
- Do not run `--compare-baselines` inside worker lanes. If a baseline comparison is needed, use the smallest decisive suite and put the broad comparison in coordinator confirmation.
- After parsing benchmark `report.json`, delete large per-case `.in`/`.out` files inside the worker workspace unless needed for diagnosis. Prefer `--discard-case-files`; keep `report.json`, diffs, and `child_result.json`.
- Before a broad coordinator gate containing multiple suites, run `python tools\benchmark.py --plan-suites <suite...>` to see overlap. This is analysis only: it can reveal duplicated case work, but promotion still requires the named gate suites or an equivalent coordinator-recorded aggregation.
- Stop after the first decisive negative result. A rejected lane with a concrete lesson is better than a slow lane that proves the same no-op three ways.
- Worker `checksRun` must distinguish `smoke`, `screen`, and any `confirm` suites actually run. If a worker skipped confirmation because the target was flat, say so explicitly.
- Confirmation suites listed in `mutation_space.json` are coordinator-only by default. Workers may mention them as remaining verification, but should not run them unless the prompt explicitly says this lane is already a top candidate.
- Worker `child_result.json` should include `laneId`, `attemptId`, `affectedFamily`, `changedMechanism`, `hiddenShape`, `currentEvidence`, `priorEvidence`, `budgetUsed`, and `budgetExceeded`; however, coordinator tools still treat `epoch_manifest.json` as the source of truth if those labels conflict or are missing.

This protocol is allowed to reject many ideas with less evidence. It is not allowed to promote from less evidence. Promotion still requires the full parent gate.

Suggested lane board format:

```text
epoch:
attempt:
lane:
based_on:
hypothesis:
uncertainty_reduced:
expected_gain:
known_risk:
allowed_files:
commands:
owner:
status: planned | active | blocked | completed | completed-invalid | cancelled | retired
result:
decision: promote-candidate | reject | needs-more-evidence | proposal-only
lesson:
```

## Worker Pool Management

The UI may keep historical subagents visible after they are no longer useful. Do not treat every listed name as an active worker.

Pool rules:

- Only the coordinator writes `pool_state.json`, ledger, weights, submission map, exploration index, or mutation space. Subagents report facts; they do not run shared-state write commands.
- Treat every `pool-update`, `pool-retire`, `collect-epoch --write`, and `dispatch-epoch --write` as a serialized coordinator action. Do not launch these write commands in parallel.
- `pool-update` and `pool-retire` use a local lock, but the coordinator should still batch or sequence pool writes so the visible worker board remains understandable.
- A manifest lane may end only as `completed`, `completed-invalid`, or `cancelled`. Use `pool-update --status cancelled --blocker "<why this lane will not run>" --write` only when the coordinator intentionally drops a lane; never leave an unlaunched lane as quiet `ready` and then close the epoch.
- Keep a small active pool, usually 2-4 workers total for routine epochs; in architecture-innovation mode use up to 5 active workers when lanes are genuinely independent.
- Reuse an existing idle worker before spawning a new one for the same lane type or hypothesis family.
- Do not create a fresh worker for a trivial follow-up that can be answered by an already active worker.
- When a worker finishes its lane, mark it `retired` and stop assigning it new work in the current epoch.
- Retired workers stay in history only; they are not part of the active working set.
- If the environment supports close/delete/terminate, use it after results are captured. If it does not, simulate cleanup by removing the worker from the active board and starting a new epoch.
- Collapse duplicate names or duplicate roles into one logical lane unless they are proving genuinely different hypotheses.
- If the pool becomes cluttered, perform a cleanup checkpoint before launching more workers:
  1. record each worker as active, blocked, completed, or retired
  2. keep only active workers with unfinished lanes
  3. archive completed or duplicate workers
  4. spawn new workers only for still-open independent lanes

Recommended lifecycle tags:

- `active`: currently assigned to an open lane
- `blocked`: waiting on another lane or missing evidence
- `completed`: returned a result
- `retired`: closed for this epoch, never assign new work
- `duplicate`: same role as another worker, keep only one active

Practical guardrail:

- If more than one worker has the same role and no independent hypothesis, keep one and retire the rest.
- If a worker has not received a new assignment for a full round, treat it as retire-eligible.
- Prefer depth over breadth once the active pool is full: continue stronger lanes rather than spawning more names.
- Keep one coordinator only. Subagents do not assign other subagents, update ledgers, or decide promotion.
- Do not keep a worker alive across epochs unless it owns a still-open lane with a specific pending question.

Worker efficiency checklist before spawning:

```text
needed_worker:
  lane:
  hypothesis:
  uncertainty_reduced:
  why_existing_workers_cannot_answer:
  expected_artifact: patch | proposal | audit | benchmark-comparison
  stop_condition:
```

Stop spawning and consolidate when:

- there are already 2 edit lanes touching `src/Solution.cpp`
- the next lane would test the same affected family with a different wording
- there is no current active-baseline hash in the prompt
- the coordinator has not reviewed completed diffs from the current epoch
- online feedback is pending for a candidate that would invalidate the search direction

## Autonomous Improvement Mode

Use this mode when the user asks the AI to keep improving without human decisions. Autonomy does not mean every attempt improves. It means the active baseline never regresses without explicit evidence, every failed attempt adds a reusable lesson, and online submission budget is spent only on candidates that pass gates.

Autonomous contract:

- The coordinator may choose hypotheses, spawn subagents, edit code, run local verification, reject candidates, restore the active baseline, and record lessons without asking the user.
- The coordinator may promote a local baseline only through the Promotion Gate.
- The coordinator must not submit online unless the user has explicitly provided an online submission budget and the project has a known safe submission path.
- If online submission is not available, produce `dist/submission.zip` and a ranked candidate report, then stop before consuming external quota.
- For upload, do not use descriptive long zip names. Use short names such as `sub047.zip` or `s047.zip`; long attempt metadata belongs in `docs/submission-map.json` via `register-submission --write`.
- If online score feedback arrives and contradicts local evidence, restore the online-best baseline before the next epoch.

What can be guaranteed:

- `currentBaseline` does not move backward locally: only a fully gated candidate can replace it.
- The main workspace is restored to the active baseline after rejected attempts.
- Each epoch produces either a promoted candidate, a ranked candidate ready for online validation, or a concrete negative lesson.
- Repeated failed patterns are not silently repeated. They may still be explored when the new hypothesis names the causal variable that changed, the first-kill test is different, or the lane is a deliberate adversarial/architecture probe.

What cannot be guaranteed:

- Every experiment improves score.
- Local proxy gains transfer to hidden tests.
- Online score improves without spending submission quota.

Autonomous epoch loop:

```text
0. doctor
   Run the skill doctor. If score < 9.5, classify failures. Hard-stop only source/baseline/ledger/workspace integrity issues; for duplicate backlog, dataset backlog, or weak portfolio shape, continue with harness warnings and bounded high-variance lanes.

0.5. drift
   If source hash differs from the ledger baseline, classify it. Never launch edit lanes from unrecorded drift.

1. lock-baseline
   Read required context, check git status, verify Solution.cpp SHA against currentBaseline.

2. mine
   Select one weakness family from ledger evidence: known weakness, online-aligned gain, critical regression, or unexplored small mutation.

3. plan
   Build an epoch board with 1-2 scout/audit lanes and up to 2 edit lanes.
   Each lane must state uncertainty_reduced and stop_condition.

4. implement
   Apply only one narrow patch at a time in the main workspace, or use isolated workspaces for parallel edits.

5. verify
   Run regression, quick benchmark, then full benchmark when quick is legal and promising.

6. decide
   Promote, reject, guard-and-retest as a new attempt, or keep as candidate needing online validation.

7. record
   Update the ledger and project memory with score deltas, affected family, onlineAlignment, retryPolicy, and avoidNextTime.

8. next-epoch
   Start from the active baseline only. Never stack on a rejected or unverified candidate.
```

Autonomous scoring policy:

- Prefer online-aligned affected families over raw local gain.
- Prefer small, explainable diffs over broad rewrites with larger proxy gains.
- Reject any candidate with catastrophic case regression unless a guard fully removes the regression and is retested as a new attempt.
- If two consecutive epochs produce proxy-only gains that do not pass alignment review, switch to `case-forensics` and `benchmark-alignment` lanes before more edits.
- If two online submissions in the same family regress, freeze that family until a new scout lane identifies a different causal mechanism.

## Direction Governance

Use this section to keep autonomous search moving toward the real hidden objective instead of chasing local proxy noise. The goal is not to prove that every step is correct. The goal is to make wrong directions self-limiting and make promising directions receive more budget.

Core validation stance:

- "Trust your validation" means build a validation fold that deserves trust, then follow it with discipline.
- The online leaderboard is a held-out fold with low sample count and high cost. Use it to calibrate family/mechanism/shape trust, not as an unrestricted oracle.
- A candidate should carry both a score thesis and a validation thesis: why these local cases are expected to predict the online hidden fold.
- If the validation thesis is missing, the lane can still be a diagnostic or risk-sidecar experiment, but it cannot become promotion evidence by score alone.

Direction signal hierarchy:

1. Online score on official hidden tests.
2. Offline evidence that historically matched online movement.
3. Official/PDF-aligned legality and case-family reasoning.
4. Full benchmark consistency.
5. Quick benchmark gain.
6. Intuition or code aesthetics.

Every epoch must classify its direction:

```text
direction_state: exploit | explore | diagnose | freeze
direction_basis:
  strongest_signal:
  affected_family:
  online_alignment: aligned | contradicted | unknown | proxy-only
  validation_thesis:
  local_fold_trust: high | medium | low | unknown
  online_fold_role: confirm | contradict | calibrate | pending
  why_this_is_closer_to_hidden_objective:
  disconfirming_evidence:
  next_budget: high | medium | low | stop
```

Direction policy:

- `exploit`: use when a family has online-aligned gains or repeated full-suite gains without critical regression. Spend more mutations here, but keep each mutation narrow.
- `explore`: use when there is no strong online-aligned direction. Try diverse small hypotheses across families instead of many variants of one proxy gain.
- `diagnose`: use after proxy-only gains, unexplained regressions, stale-baseline risk, or conflicting benchmark signals. Prefer proposal-only agents and audits before edits.
- `freeze`: use when a family has repeated online regression, catastrophic local regression, or matches a known rejected pattern. No new edits in that family until a scout lane names a new causal mechanism.

Do not let this policy become timidity. A `freeze` is a memory warning, not a ban on architecture imagination. The coordinator may thaw a frozen family for one isolated lane when it states the new causal variable, different first-kill evidence, and rollback boundary.

Budget allocation rule:

- Allocate about 60% of edit attempts to `exploit` directions with online-aligned evidence.
- Allocate about 30% to `explore` directions that are small, legal, and causally distinct.
- Allocate about 10% to `diagnose` and benchmark-alignment work.
- Allocate 0% to `freeze` directions.
- If there is no `exploit` direction, shift budget to `explore` plus `diagnose`, not to bigger rewrites.

Trend checks:

- After every 2 epochs, summarize whether evidence is converging, conflicting, or stagnant.
- If evidence is converging, narrow the search around the winning affected family.
- If evidence is conflicting, stop edits and run `benchmark-alignment` or `rollback-auditor`.
- If evidence is stagnant, increase diversity of hypotheses rather than increasing patch size.
- If all current directions are frozen or stagnant, return to official rules, taskbook, and failure ledger before more code edits.

Long-run improvement assumption:

- With enough time, the loop can approach better answers only if it maintains a reliable feedback gradient.
- The coordinator must therefore optimize for feedback quality first, local score second.
- A lower-scoring experiment can still be valuable if it improves the map of which families transfer online.
- A higher-scoring experiment is harmful if it teaches the loop to chase a proxy-only direction.

## 9.5 Quality Bar

This skill is considered 9.5-ready only when the loop is both strategic and mechanically self-limiting. Use the bundled doctor as the machine-readable gate:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py doctor --project "C:\Users\17533\Documents\New project 5"
```

Required properties:

- active baseline source hash matches the ledger before edits
- best-known online baseline and score are recorded
- mutation space is bounded, with frozen patterns for repeated failures
- failed attempts have concrete `avoidNextTime` lessons
- online/offline calibration is visible either in explicit family weights or in ledger `onlineEvaluations`
- duplicate fingerprints are controlled on the current baseline before new lanes are opened; historical duplicates should remain searchable but are not a hard blocker when they are already frozen or lessoned
- router commands cover status, idea check, epoch preparation, child ranking, gate decision, closeout, online update, and doctor
- child_result files validate against the required schema before ranking
- mutation-space direction states can be reweighted from online/offline family weights after online feedback
- epoch manifests can be converted into dispatch queues and collected without hand-inspecting every workspace

If a quality check fails:

- do not start unattended edit lanes only when the failure is a hard harness failure
- run proposal-only `case-forensics`, `benchmark-alignment`, or ledger-cleanup work
- repair the missing evidence or guardrail, or convert the warning into an explicit bounded-risk lane
- rerun doctor before returning to autonomous mutation

Use the score as a governance signal, not as a leaderboard metric. A 9.5 loop can still find bad ideas, but it should reject them cheaply, remember why, and keep the active baseline clean.

Doctor scoring nuance:

- `onlineEvaluations` in the ledger count as online calibration evidence.
- `docs/online-offline-weights.json` is still preferred after new online submissions because it makes family weights machine-readable.
- `docs/dataset-evolution-ledger.json` is required for unattended hidden-set fitting. If it is missing, initialize it from the next online feedback or an existing worker `datasetCandidate`.
- Duplicate fingerprints only fail the hard gate when they repeat on the current baseline. Historical duplicates are acceptable if they have `avoidNextTime` lessons or appear in frozen patterns.

## Dataset Evolution Gate

Online feedback must improve the offline dataset model, not only adjust weights.

Lifecycle:

```text
online feedback -> dataset hypothesis -> generated case/report artifact -> datasetCandidate -> validate against historical online positives/neutrals/negatives -> promote or freeze -> optional benchmark integration
```

Rules:

- A local suite or generated case becomes promotion evidence only after it explains at least one online-positive record and rejects at least one neutral/down or contradicted record.
- Neutral online feedback is not "nothing happened". It should usually create a negative dataset candidate or freeze a misleading local proxy shape.
- `dataset-promote` is metadata promotion. It does not by itself edit `tools/benchmark.py`; code integration still needs a coordinator-reviewed patch and normal tests.
- Do not keep adding cases that only make the current local candidate look better. The candidate must state what online outcome it predicts differently next time.
- If a generated case cannot be validated, keep it as `candidate` or `frozen`; do not put it into parent promotion gates.
- When multiple workers generate proxy cases, merge the lesson, not the files. Promote at most one dataset candidate per causal shape.
- Validated candidates are not progress until they change future decisions. If `dataset-status` reports many `validatedBacklog` items and `promoted=0/frozen=0`, open a dataset decision lane before another dataset/proxy generation lane. Each validated cluster must be promoted, frozen, rejected, or merged within the next epoch.

Required `datasetCandidate` shape:

```text
datasetCandidate:
  candidateId:
  sourceOnlineFeedback:
  caseFamily:
  caseShape:
  hypothesis:
  explainsPositive: []
  rejectsNeutralOrNegative: []
  artifactPaths: []        # or generatedCaseFacts/caseCount
  generatedCaseFacts: []
  promotionGateImpact:
```

Commands:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py dataset-status --project "C:\Users\17533\Documents\New project 5"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py dataset-suggest --project "C:\Users\17533\Documents\New project 5" --source-child-result "<child_result.json>" --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py dataset-validate --project "C:\Users\17533\Documents\New project 5" --candidate-id "<candidate-id>" --strict --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py dataset-promote --project "C:\Users\17533\Documents\New project 5" --candidate-id "<candidate-id>" --target-suite "<suite-or-proxy-name>" --reason "<why it predicts online better>" --write
```

Use `dataset-promote --freeze` when the candidate explains a proxy trap or online-neutral decoy that future workers should avoid.

## Online-Offline Calibration

Use official online score feedback as a sparse sensor for the hidden dataset, within the contest rules and submission limits. The goal is not to reverse-engineer hidden cases directly. The goal is to learn which offline case families, benchmarks, and code-change patterns predict online movement.

Leaderboard-as-fold rule:

- Treat the public/online score like one additional validation fold, not the objective function itself.
- A single online tie or drop should not erase a mechanism if the validation thesis remains plausible, but it must reduce trust in the exact family/mechanism/shape that was tested.
- A single online improvement should not license broad variants. It raises trust for the specific mechanism and shape that were actually tested.
- If repeated online feedback contradicts the same local suite, downgrade that suite and open a dataset/alignment lane before more edits.

After every online score, update a calibration record:

```text
online_calibration:
  submitted_attempt:
  based_on:
  online_score:
  online_delta_vs_best:
  local_quick_delta:
  local_full_delta:
  affected_family:
  changed_mechanism:
  predicted_direction: up | down | neutral | unknown
  actual_direction: up | down | neutral
  calibration_result: confirmed | contradicted | inconclusive
  offline_weight_update:
  validation_thesis:
  local_fold_trust_before:
  local_fold_trust_after:
  online_fold_interpretation:
  hidden_dataset_hypothesis:
  next_action: exploit | explore | diagnose | freeze | restore-online-best
```

Calibration policy:

- Treat each online submission as an expensive experiment that tests one primary hidden-dataset hypothesis.
- Prefer `online-feedback` on raw leaderboard text. It must map both short upload names (`sub050.zip`) and long internal package names (`submission_baseline-050-...zip`) through `docs/submission-map.json`; do not accept `family=unknown`, `mechanism=unknown`, or blank `hidden_dataset_hypothesis` when a mapping exists.
- Before submission, state what online movement the candidate is expected to reveal and which offline signal it is testing.
- After submission, compare predicted vs actual direction, not just raw score.
- Increase trust in offline suites or affected families that repeatedly predict online direction.
- Split trust by family, mechanism, and case shape when possible. A family can be online-positive while one mechanism or shape inside it is still frozen.
- Decrease trust in proxy cases that improve locally but regress online.
- If online feedback contradicts the current active direction, restore the online-best baseline before new edits.
- If two candidates with different mechanisms produce the same online direction, look for the shared affected family.
- If local and online disagree repeatedly, spend the next epoch on `benchmark-alignment` and case-family diagnosis, not code mutation.

Maintain an offline benchmark weight map:

```text
benchmark_weight:
  case_family:
  changed_mechanism:
  hidden_shape:
  current_weight:
  evidence_count:
  online_confirmed:
  online_contradicted:
  last_update:
  reason:
```

Use the weight map when ranking candidates:

- Local gains in high-weight, online-confirmed family/mechanism/shape combinations count more.
- Local gains in contradicted or proxy-only families count less.
- A small gain in an online-confirmed mechanism can outrank a larger gain in a contradicted mechanism.
- A candidate that improves many low-weight proxy cases but hurts one high-weight family or shape is risky.

Hidden dataset hypothesis discipline:

- Hypotheses must be about distributions and mechanisms, such as hotspot prevalence, permutation sensitivity, duplicate-flow density, capacity pressure, or routing tie-break behavior.
- Do not infer or attempt to reconstruct individual hidden cases.
- Do not use online submissions for broad uncontrolled probing. Each submission should test one named hypothesis.
- Record uncertainty. Hidden-dataset hypotheses are working beliefs, not facts, until repeatedly confirmed.

After user-reported online feedback, use the helper to update the offline family weight map:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py online-update --project "C:\Users\17533\Documents\New project 5" --attempt "<attempt-id>" --online-score "<score>" --family "<affected-family>" --mechanism "<changed-mechanism>" --shape "<case-shape-if-known>" --predicted-direction up --hidden-hypothesis "<one mechanism-level belief>" --write
```

This writes `docs/online-offline-weights.json`. Use `--write` only after the online score is real. Without `--write`, the command is a dry run for reviewing how the calibration would change.

Then update the dataset evolution layer. If the online result was neutral/down or contradicted the local proxy, create a dataset candidate immediately:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py dataset-suggest --project "C:\Users\17533\Documents\New project 5" --source-online-feedback "<attempt-or-baseline>" --family "<affected-family>" --mechanism "<mechanism>" --case-shape "<hidden/proxy shape>" --hypothesis "<why local proxy mispredicted online>" --explains-positive "<online-positive baseline>" --rejects-neutral-negative "<neutral/down attempt>" --promotion-gate-impact "<how future offline gate should change>" --write
```

## Exploration Deduplication

Large exploration is allowed, but it must expand coverage instead of repeating the same idea. The coordinator must keep an exploration index and check it before creating lanes, editing code, or submitting online.

Use the bundled read-only helper before opening edit lanes:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py status --project "C:\Users\17533\Documents\New project 5"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py index --project "C:\Users\17533\Documents\New project 5"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py check --project "C:\Users\17533\Documents\New project 5" --hypothesis "<one narrow idea>"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py suggest-lanes --project "C:\Users\17533\Documents\New project 5"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py epoch-board --project "C:\Users\17533\Documents\New project 5"
```

If `status` reports source hash drift, stop and classify/backup/restore before assigning workers. A real prior run hit repeated main-source drift while child agents were active; treating drift as a hard stop prevents stacking untracked worker code into the active baseline.

If `check` returns `near-duplicate-review-ledger-lessons`, the coordinator may still run the attempt, but must name the new causal mechanism or guard that makes it different from the prior failures. If it cannot, change the lane to `proposal-only` or choose a `suggest-lanes` alternative.

Exploration fingerprint:

```text
exploration_fingerprint:
  based_on:
  affected_family:
  changed_mechanism:
  parameter_or_rule:
  direction: increase | decrease | enable | disable | reorder | guard | replace
  expected_effect:
  known_risk:
```

Deduplication policy:

- Do not run a new attempt if its fingerprint matches a rejected attempt unless the new attempt changes the causal mechanism or adds a specific guard for the recorded failure.
- Do not create multiple lanes that differ only by wording, small threshold values, or code location when they test the same mechanism.
- Batch adjacent parameter values into a planned sweep only when the benchmark cost is low and the sweep has a clear stop rule.
- Prefer orthogonal hypotheses across affected families before running many variants inside one proxy-only family.
- After a failed attempt, record the fingerprint plus `avoidNextTime` so future workers can reject duplicates quickly.
- If a worker proposes an idea already covered in the ledger, convert the lane to `proposal-only` and ask for a new mechanism or a sharper guard.

Exploration budget rules:

- Many small experiments are better than one broad rewrite, but every experiment must have a unique fingerprint.
- In an `explore` epoch, choose diverse families first: at most one edit lane per affected family unless that family is online-aligned.
- In an `exploit` epoch, variants may share the same family, but each must change only one parameter, guard, tie-break, or allocator behavior.
- Stop a sweep early when two adjacent variants move in the wrong direction or when the best variant still fails legality, runtime, or critical-regression checks.
- Never online-submit multiple variants from the same local sweep unless the first online result confirms the family direction.

Exploration index format:

```text
exploration_index_entry:
  attempt:
  fingerprint:
  result: promoted | rejected | candidate | online-confirmed | online-contradicted
  score_delta:
  lesson:
  retry_policy: never | only-with-guard | only-from-clean-baseline | allowed
```

## Candidate Ranking Tools

After child agents finish, collect and rank their `child_result.json` files before reviewing diffs:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py rank-children --run-dir "C:\Users\17533\Documents\New project 5\tmp\score-loop-epochs\<epoch-id>"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py close-epoch --run-dir "C:\Users\17533\Documents\New project 5\tmp\score-loop-epochs\<epoch-id>" --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py gate-decision --child-result "<path-to-child_result.json>"
```

Ranking is only a triage aid, not a promotion decision. It prioritizes candidates with positive online-aligned deltas and penalizes runtime risk, regressions, flat/no-op evidence, and worker-declared rejection.

For score-loop epochs, pass the epoch root containing `epoch_manifest.json` to `rank-children` and `close-epoch`, not the raw `workspaces/` directory. Manifest-aware ranking ignores stale workspace folders and applies the lane metadata labels.

`close-epoch` summarizes the whole run and writes `epoch_closeout.json`. `gate-decision` classifies a single child result as `eligible-for-parent-gate`, `needs-more-evidence`, `reject-or-needs-more-evidence`, or `reject`, and lists parent gate commands. Neither command applies patches or promotes; they prevent weak candidates from reaching the main workspace.

Closeout is a promotion boundary. If `epoch_closeout.json.topDecision` is not `eligible-for-parent-gate`, do not archive that child as accepted or promote a local baseline unless a human/coordinator records a manual override with a concrete reason. The override must explain which parent gate evidence invalidated the closeout decision and must be stored in the ledger record.

When ranking or archiving children from an epoch, use `epoch_manifest.json` lane metadata as canonical. Do not let `basedOn` names or free-text summaries relabel a leaf-band/capacity-shadow lane as `large_sparse/residual_target`.

Coordinator decision order:

1. Reject missing `child_result.json` unless the worker returned a clear patch and measurements elsewhere.
2. Reject or freeze candidates with `online_fit_core`, `hidden_shape`, or other high-weight family regressions unless the attempt explicitly targeted a different online-confirmed tradeoff.
3. Treat local proxy-only gains as `needs-more-evidence`, especially leaf-band-only, random-only, phase-between-only, or benchmark-forensics-only gains.
4. Review exact diffs only for the top-ranked non-rejected candidates.
5. Apply at most one candidate to the main workspace, then run the normal Promotion Gate.

Lessons from prior autonomous runs:

- Child agents can all complete yet produce no promotable candidate; this is useful if their results shrink the search space.
- `large-sparse` remains online-important, but coarse widening can become no-op or runtime risky; require a named residual target before widening.
- `leaf-band` proxy gains are fragile; do not sacrifice `online_fit_core`, negative guard seeds, or runtime for a single positive seed.
- Main workspace drift can happen while parallel workers are running; verify the active source hash before and after collecting workers.

## Mutation Space

The default bounded search space lives at `references/mutation_space.json`.

Use it when:

- creating autonomous epoch boards
- deciding whether a family is `exploit`, `explore`, `diagnose`, or `freeze`
- choosing required benchmark suites for a mutation
- checking whether a worker proposal exceeds allowed mechanisms

Do not treat the mutation space as exhaustive. It is a safe default for autonomous work, not a ceiling. If a new idea is outside it, run it in an isolated workspace as an architecture/controlled-risk/044-style lane when it has a stop condition and first-kill test; use `proposal-only` only when the execution harness is unclear. Add it to the mutation space after a coordinator review names the family, mechanism, required suites, and reject conditions.

## Autonomous Epoch Runner

Default 9+ workflow for unattended search preparation:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py idea-board --project "C:\Users\17533\Documents\New project 5" --run-id "<idea-id>" --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py run-epoch --project "C:\Users\17533\Documents\New project 5" --run-id "<epoch-id>" --idea-board "C:\Users\17533\Documents\New project 5\docs\idea-boards\<idea-id>.json"
```

Using bare `run-epoch` is allowed only for a specific bounded mutation-space sweep or emergency fallback. For autonomous search, bare `run-epoch` is considered lower quality because it can skip the expert-panel divergence step.

Then:

1. Review `tmp/score-loop-epochs/<epoch-id>/epoch_manifest.json`.
2. Run `dispatch-epoch --run-dir <epoch-dir> --write` to create `dispatch_queue.json` and `pool_state.json`.
3. Launch workers using the dispatch queue, one per isolated workspace. Prefer each task's `spawnAgent` block as the direct `multi_agent_v1.spawn_agent` contract: worker role, message prompt, workspace, expected artifact, patch boundary, and stop condition. If the worker launcher cannot guarantee workspace isolation, launch the lane as proposal-only.
4. After each worker is spawned, record its real agent id:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py pool-update --run-dir "C:\Users\17533\Documents\New project 5\tmp\score-loop-epochs\<epoch-id>" --lane "<lane-id>" --status active --worker-id "<agent-id>" --write
```

5. Run `collect-epoch --run-dir <epoch-dir> --project "C:\Users\17533\Documents\New project 5" --write` after workers finish. This updates `pool_state.json`; completed lanes become retire candidates, active missing lanes stay active instead of being requeued. It ranks only schema-valid completed children. Completed-invalid children must be fixed or rejected before closeout. Missing `ready` lanes must be dispatched, and lanes intentionally dropped must be marked `cancelled` with a blocker before closeout. It also reports `mainWorkspaceGuard`; if the guard says the main source hash drifted, stop and run `drift`/`restore-online-best` before learning, closing, or promoting.
6. Learn from child outputs before choosing the next direction:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py learn-from-children --run-dir "C:\Users\17533\Documents\New project 5\tmp\score-loop-epochs\<epoch-id>" --project "C:\Users\17533\Documents\New project 5"
```

If the learned lessons are valid, rerun with `--write-index`; use `--write-mutation-space` only for stable rejected patterns that should become frozen guardrails.

7. Retire completed lanes after their results are captured:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py pool-retire --run-dir "C:\Users\17533\Documents\New project 5\tmp\score-loop-epochs\<epoch-id>" --completed --write
```

8. Close and gate:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py close-epoch --run-dir "C:\Users\17533\Documents\New project 5\tmp\score-loop-epochs\<epoch-id>" --write
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py gate-decision --child-result "<top-child-result>"
```

9. Apply at most one `eligible-for-parent-gate` candidate to the main workspace.
10. Run every parent gate command from `gate-decision`, then the normal Promotion Gate.
11. Archive the accepted or rejected attempt after the coordinator decision:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py archive-attempt --project "C:\Users\17533\Documents\New project 5" --child-result "<child_result.json>"
```

Use `--accepted --write` only after the parent gate actually accepts the candidate.

If `epoch_closeout.json` did not mark the candidate `eligible-for-parent-gate`, the accepted archive command must be explicit:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py archive-attempt --project "C:\Users\17533\Documents\New project 5" --child-result "<child_result.json>" --accepted --manual-override --override-reason "<parent gate evidence that overruled closeout>" --write
```

Never auto-apply worker code from `prepare-epoch`. The coordinator must inspect the diff and gate-decision output first.

Never send a final user-facing answer while an epoch has `collect-epoch.complete=false`, active workers, ready lanes, missing child results, or `close-epoch.topDecision=invalid-epoch`. Stay in the same controller conversation: dispatch remaining ready lanes, wait for active workers, fix invalid child results, or explicitly cancel unused lanes with `pool-update --status cancelled --blocker "<reason>" --write`; then rerun `collect-epoch --write` and `close-epoch --write`.

Continuous autonomous mode: when the user asks for automatic iteration, continuous score search, or "keep going until finished", one closed epoch is not the finish line. After every valid closeout:

- If `topDecision=eligible-for-parent-gate`, inspect/apply at most one diff, run `gate-decision`, parent gates, archive, memory sync, and package/register a short `subNNN.zip` only if accepted.
- If `topDecision` is `reject`, `reject-or-needs-more-evidence`, `needs-more-evidence`, or `no-results`, write the lessons first (`learn-from-children`, `archive-attempt` for accepted rejected lessons, mutation-space/index updates when warranted), then immediately open the next expert `idea-board`/`run-epoch` unless a stop condition below is active. The next board must state what changed: new causal variable, new target evidence, new risk sidecar, new objective frame, or a frozen direction. Do not repeat the same paperwork-shaped epoch.
- A final answer is allowed only when there is a concrete handoff boundary: an upload package is ready and external online feedback is required, the daily/contest submission budget blocks the next decision, source/tooling is genuinely blocked, or the user explicitly asks to pause/stop/status-only.

Never close an epoch as successful while `collect-epoch` reports `mainWorkspaceGuard.sourceHashMatches=false`. Treat that as an invalid epoch until the drift is classified and the active source is restored or deliberately recorded as a new attempt.

Promotion thresholds should be explicit in the attempt record:

```text
promotion_threshold:
  min_quick_delta:
  min_full_delta:
  max_allowed_critical_regression:
  runtime_limit:
  online_alignment_required: yes | no
  submit_online: yes | no
```

Autonomous stop conditions:

- active baseline hash cannot be verified
- required context or ledger is missing or invalid
- workspace contains unexplained user changes
- benchmark or regression tooling is broken
- no safe online submission budget/path exists and the next decision requires online score
- repeated epochs produce no new evidence, only variants of known rejected patterns

## Verification Commands

Use these commands from the project root:

```powershell
python tools\run_regression.py
python tools\benchmark.py --suite quick
python tools\benchmark.py --suite full
```

Run additional official/PDF-aligned benchmark commands only if the project already provides them or the ledger references the exact command. Do not invent a new gate and promote from it without recording why it is more relevant than the existing gate.

The regression command must rebuild `dist/submission.zip` before any promoted submission package is trusted.

## Promotion Gate

Promote only when all are true:

- official sample regression passes
- outputs are legal
- quick/full benchmark results are parsed and compared to current baseline
- no critical case has catastrophic regression
- stress/runtime risk is not materially worse
- `dist/submission.zip` contains exactly root-level `Solution.cpp`
- result is recorded in `docs/optimization-ledger.json`
- project memory is updated and rendered

Prefer online-aligned evidence over raw local proxy gain. Small local gains on hidden-distribution-sensitive routing are not enough by themselves, especially after `baseline-007` regressed online.

## Candidate Merge Protocol

Before accepting any subagent patch:

1. Confirm the candidate was based on the current baseline hash, not another lane's rejected state.
2. Review the diff for scope creep, broad rewrites, unused templates, unsafe randomness, environment assumptions, and compile/runtime risk.
3. Apply the patch in the main workspace only after the diff is understood.
4. Run the verification commands appropriate to the claimed risk.
5. Record the candidate in `docs/optimization-ledger.json` even when rejected if it taught a reusable lesson.

Use the following decision policy:

- Strong local gain + no critical regression + online-aligned family: eligible for promotion.
- Small local gain + hidden-distribution risk: keep as candidate, do not submit online without a second reason.
- Any catastrophic case regression: reject or add a guard, then retest as a new attempt.
- Candidate based on stale hash: reject as evidence; optionally rebase manually as a new attempt.
- Candidate with multiple strategy changes: split or reject unless the diff is already tiny and causally clear.

## Online Score Rule

Online score feedback beats local proxy benchmark.

If the user reports an online score:

1. Compare it with the best known online score in the ledger.
2. If worse, mark that baseline `rejected-after-online-submission` or demote it.
3. Restore `currentBaseline` to the best known online baseline unless the user explicitly accepts the tradeoff.
4. Rebuild `dist/submission.zip` from the restored baseline.
5. Record score, delta, timestamp, and lesson in the ledger and project memory.

Do not continue optimizing from a locally-promoted baseline after online regression.

Use the helper in two phases:

```powershell
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py online-update --project "C:\Users\17533\Documents\New project 5" --attempt "<attempt-id>" --online-score "<score>" --family "<family>" --mechanism "<mechanism>" --shape "<shape-if-known>" --predicted-direction up --hidden-hypothesis "<hypothesis tested>"
python C:\Users\17533\.codex\skills\huawei-nslb-score-loop\scripts\score_loop_tools.py online-update --project "C:\Users\17533\Documents\New project 5" --attempt "<attempt-id>" --online-score "<score>" --family "<family>" --mechanism "<mechanism>" --shape "<shape-if-known>" --predicted-direction up --hidden-hypothesis "<hypothesis tested>" --write --write-ledger
```

Add `--accept-best-update` only when the score is a real improvement and the coordinator accepts that attempt as the new best-known online baseline. A worse or neutral online result should append an `onlineEvaluations` record and update calibration, but it must not move `currentBaseline` automatically.

## Rejection Rule

If an attempt fails any gate:

- restore `src/Solution.cpp` from active baseline snapshot
- record `failureReason`
- record `avoidNextTime` as a concrete technical rule
- keep useful measurements, but do not let the rejected code remain active
- update project memory

Do not repeat failed patterns already listed in the ledger unless the new attempt changes the causal issue.

## Subagent Prompt Template

When delegating a lane, copy this prompt and fill the bracketed fields:

```text
You are a subagent for the Huawei Algorithm Challenge 37 NSLB optimization project.

Main project root, read-only reference: C:\Users\17533\Documents\New project 5
Assigned isolated workspace, use this as your working directory: [workspace path from epoch_manifest.json]
Workspace Solution.cpp absolute path: [workspace]\src\Solution.cpp
Main Solution.cpp must remain unchanged: C:\Users\17533\Documents\New project 5\src\Solution.cpp
Skill to follow: huawei-nslb-score-loop
Lane id: [lane-id]
Attempt id: [attempt-id]
Based on baseline: [currentBaseline id + sourceSha256]
Hypothesis: [one primary strategy only]
Expected improvement family: [case/family]
Known risk: [risk]
Allowed files to edit: [usually src/Solution.cpp only, or "none; proposal-only"]

Rules:
- Read AGENTS.md, docs/optimization-ledger.json, docs/optimization-workflow.md, docs/competition-taskbook.md, and the active baseline context before acting.
- Start from the active baseline only. If the workspace hash differs from the supplied baseline hash, stop and report it.
- Shell commands must use the assigned isolated workspace as `workdir`.
- Do not edit or run implementation commands in the main project root.
- `apply_patch` does not inherit shell `workdir`. If you use `apply_patch`, every file header must be an absolute path under the assigned workspace.
- Never use relative `apply_patch` headers such as `*** Update File: src/Solution.cpp`; that can modify the main project and invalidates the lane.
- After any patch, verify the main Solution.cpp hash still equals the supplied baseline hash. If it changed, stop and report main-workspace drift.
- Do not edit docs/optimization-ledger.json, project memory, package files, or submission artifacts.
- Do not submit online and do not promote a baseline.
- Keep the change narrow: one idea, minimal diff, no broad rewrite.
- Run only the needed local checks for the hypothesis. Prefer:
  python tools\run_regression.py
  python tools\benchmark.py --suite quick
  python tools\benchmark.py --suite full
- If checks are expensive, run regression + quick first and clearly state what remains unverified.

Return exactly:
1. Baseline hash observed
2. Files changed
3. Hypothesis and implemented change
4. Commands run and parsed score deltas
5. Critical regressions or runtime risks
6. Unified diff or patch summary
7. Decision recommendation: promote-candidate / reject / needs-more-evidence
8. Lesson for the ledger, including avoidNextTime if rejected
9. For dataset-evolution lanes, a `datasetCandidate` object with the required fields above
```

## Pool Control Template

Before spawning new workers, write the current pool state:

```text
pool_state:
  active: [name/lane]
  blocked: [name/lane]
  completed: [name/lane]
  retired: [name/lane]
  duplicates_to_close: [name/lane]
  new_workers_allowed: [0-3]
```

Use this rule:

- If `new_workers_allowed` is 0, reuse existing active workers only.
- If `duplicates_to_close` is non-empty, retire them before creating any new worker.
- If a lane has a clear owner, do not assign the same lane to a second worker.
- If the same hypothesis appears twice, consolidate it into one lane and retire the duplicate.

## Known High-Risk Patterns

Check the ledger for the latest list. Historically risky patterns include:

- broad cross-phase unique-flow reordering
- unbounded duplicate-flow group repair
- treating repeat-heavy proxy cases as official-hidden evidence
- extending official hot-source logic to over-capacity source hotspots
- source-native port mapping for official permutation/destination hotspot traffic
- stacking local-only hot-destination/permutation gains after online regression

## Packaging

After any promoted baseline or restored online-best baseline:

```powershell
python tools\run_regression.py
```

Then verify:

- `dist/submission.zip` exists
- zip contains exactly `Solution.cpp`
- source file size is under contest limits
- SHA256 of `src/Solution.cpp` matches the ledger baseline source hash

Final user-facing answer should include the active baseline id, score deltas, package path, and whether tests/benchmarks ran.

## Memory Update

After meaningful work, update project memory. Use the existing project memory script referenced in `AGENTS.md` when available, then render the HTML overview:

```powershell
python C:\Users\17533\.codex\skills\dawn-agent-html-memory\scripts\render_overview.py "C:\Users\17533\Documents\New project 5"
```

Project memory sync is part of the done definition unless the user explicitly says to skip it.
