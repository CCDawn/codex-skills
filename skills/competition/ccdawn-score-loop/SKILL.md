---
name: ccdawn-score-loop
description: "Use when optimizing any measurable score, benchmark, leaderboard, validation metric, online/offline feedback loop, experiment lane, baseline promotion, or submission package where iterative evidence should guide code, model, or search changes."
---

# Score Loop

## Goal

Run score-driven work as an evidence loop:

```text
baseline -> one causal change -> smallest decisive check -> promotion/rejection -> ledger update -> next change
```

This is a generic template. A project-specific profile must define the metric, commands, files, promotion gate, and ledger surfaces. If no profile exists, first build a compact profile instead of inventing commands.

## BRT interface

- Context Boundary: project root, score metric, active baseline, allowed write surface, experiment ledger, validation commands, and selected lane.
- Output Contract: status, experiment lane, worker contract, gate decision, package record, online feedback update, or recovery artifact.
- Allowed Action: only the profile-approved write surface, one causal mechanism per lane, no baseline promotion/package/submission without a parsed gate decision.
- Success Evidence: command output, score delta, diff, result JSON/report, ledger/search update, promotion decision, or registered package.
- Stop Condition: source drift, stale baseline, missing metric definition, invalid validation command, overlapping writes, unsafe promotion, ambiguous online feedback, or user pause.
- Route Out: continue score loop, launch/recover worker lane, promote/reject candidate, package/submit, update project memory, or BLOCKED with one required input.

## Required profile

Before meaningful optimization, identify or create:

```text
Project:
- Root:
- Metric:
- Higher is better / lower is better:
- Active baseline:
- Online/best-known anchor:
- Allowed write files:
- Protected files:
- Status command:
- Fast validation:
- Full validation:
- Packaging command:
- Ledger paths:
- Result artifact schema:
- Promotion gate:
- Stop conditions:
```

Project adapters may keep this in their own `references/*profile.md` or repository docs.

## When to use

Use this skill for:

- benchmark or leaderboard optimization;
- repeated local validation with promotion gates;
- online/offline score disagreement;
- multiple candidate implementations or model variants;
- worker lanes that need isolated evidence;
- package/submission registration;
- recovery of partial or failed experiment diffs.

Do not use it for ordinary feature implementation, one-off bugfixes, or scoreless refactors. Route those to BRT, planning, debugging, or development skills.

## Operating rules

- One lane tests one causal mechanism.
- Prefer a small decisive check before broad validation.
- Do not promote on stale source, unclear metric, missing artifact, or unparsed output.
- Failed attempts still become searchable lessons.
- Online feedback updates calibration; it does not replace clean local validation.
- Hard harness failures block execution; soft confidence issues change lane choice or first-kill tests.
- Coordinator applies promotions; workers do not mutate the main baseline or ledger directly unless the profile explicitly allows it.

## Lane matrix

Every executable lane must fit this shape:

```json
{
  "laneId": "short-id",
  "attemptId": "short-attempt-id",
  "targetComponent": "module/function/model/data fold",
  "mutationType": "edit | architecture | controlled-risk | diagnostic | dataset | fusion",
  "hypothesis": "one causal mechanism only",
  "intendedMetric": "primary or component metric",
  "nonScoreSignal": "secondary signal, legality, runtime, or diagnostic proof",
  "smallestDecisiveTest": "single case, narrow suite, trace, or bounded run",
  "killCondition": "flat, regression, timeout, illegal output, or missing target",
  "expectedDiffSurface": ["path/to/file"],
  "negativeControls": ["known failed family or baseline comparison"],
  "recoveryArtifact": "result JSON, report, diff, or dataset path"
}
```

Proposal-only lanes are valid only for diagnostics, dataset/proxy construction, or when the lane explicitly cannot edit code. They still need a concrete artifact.

## Worker contract

Workers are diff-first executors:

1. Work only in the assigned isolated workspace.
2. Confirm baseline/source identity before editing.
3. Implement exactly one mechanism or produce one diagnostic artifact.
4. Run the smallest decisive test before broad suites.
5. Preserve diff, report, logs, and parsed metrics.
6. Write a result artifact before finishing.

Minimum result fields:

```text
laneId, attemptId, baselineId, hypothesis, mutationType, changedFiles,
commandsRun, checksRun, smallestDecisiveTestResult, metricsBeforeAfter,
promotionCandidate, result, summary, avoidNextTime, artifactPaths, diffSummary
```

## Validation and promotion

Use `smoke -> screen -> parent gate`:

- Smoke: cheap proof that the target signal moves or the idea is impossible.
- Screen: 2-3 representative checks for promising candidates.
- Parent gate: full validation, legality, runtime, package shape, ledger update, and rollback readiness.

Promote only when:

- candidate is based on the current baseline;
- diff scope matches the lane;
- validation output is parsed, not eyeballed;
- failure modes and secondary signals are acceptable;
- ledger/search graph records the decision;
- package or release artifacts match the project profile.

Reject or hold when the gain is unparsed, overfit to one fold, illegal, too slow, dependent on stale state, or missing a reproducible artifact.

## Online/offline feedback

Treat online score, hidden tests, external review, or public leaderboard as sparse validation folds:

1. Record the exact package/candidate and score.
2. Compare against local validation and expected direction.
3. Identify which local fold or proxy lied.
4. Update trust weights or diagnostic cases.
5. Continue only with a named causal explanation or new calibration lane.

Never move best-known online/baseline on neutral or worse feedback unless the user explicitly accepts a tradeoff.

## Recovery loop

When progress stalls:

- inspect failed diffs, partial workers, rejected attempts, and stale labels;
- revive only candidates with a new causal variable, new witness, or reusable artifact;
- rewrite broad old ideas into one-mechanism lanes;
- preserve rejected compiled diffs as search material;
- stop if no safe new causal variable can be named.

## Compact outputs

Status:

```text
Score Loop Status:
- Baseline:
- Best score:
- Active lanes:
- Drift/blockers:
- Recommended next lane:
- Success Evidence:
- Route Out:
```

Gate:

```text
Gate Decision:
- Candidate:
- Evidence:
- Verdict: promote / reject / hold / blocked
- Reason:
- Next action:
```

Online feedback:

```text
Online Feedback:
- Package/candidate:
- Score:
- Local expectation:
- Calibration lesson:
- Best-known update: yes/no
- Next lane:
```
