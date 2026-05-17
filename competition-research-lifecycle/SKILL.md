---
name: competition-research-lifecycle
description: Orchestrates the full lifecycle of competition-driven research projects from task framing through data preparation, literature review, baseline setup, training, analysis, paper writing, and submission packaging. Use when the user is working on a research competition, Kaggle-style challenge, academic contest, benchmark track, or any end-to-end workflow that combines data work, experiments, and a paper or report deliverable.
---

# Competition Research Lifecycle

Use this skill to run a competition project as a staged research program.

`brt` is the governance layer for this workflow. It does not replace any phase. Use it to define behavior, review risks, and set acceptance checks before advancing a phase.

`literature-evidence-synthesis` is the default evidence-normalization layer for research-heavy phases.

`paper-claim-traceability` is the default evidence-audit layer for late-stage writing and packaging.

## Operating modes

- `phase-diagnosis`: infer the current phase from the user's artifacts, blockers, and missing evidence.
- `phase-execution`: define the work needed to complete the current phase and produce its artifact.
- `phase-recovery`: detect when a later phase is blocked by a weaker upstream artifact and route back deliberately.

## Quick start

1. Diagnose the current phase from the user's artifacts and current blocker.
2. Lock the phase goal, inputs, outputs, and exit criteria with BRT language.
3. Route to the right supporting skill for the work.
4. Produce or request the phase artifact before moving on.
5. End the pass with an explicit decision: `advance`, `iterate`, or `recover`.

## Phases

1. Task framing
2. Data preparation
3. Literature and solution research
4. Baseline system
5. Training and experimentation
6. Analysis and ablation
7. Paper writing
8. Submission packaging

See [REFERENCE.md](REFERENCE.md) for phase-by-phase rules, artifacts, and routing.
See [TEMPLATES.md](TEMPLATES.md) for reusable artifact templates and response skeletons.
See [EXAMPLES.md](EXAMPLES.md) for example invocations across common competition types.

## Routing rules

- Use `brt` when entering a new phase, changing scope, or promoting a result into the next phase.
- Use `literature-evidence-synthesis` during Phase 3 to convert papers, repos, notes, and public findings into a literature matrix, comparison table, claim map, or experiment hypothesis pack.
- Use `literature-evidence-synthesis` again during Phase 7 when related work, method positioning, or evidence organization is still loose.
- Use `paper-claim-traceability` in late Phase 7 and again before Phase 8 when abstracts, contribution bullets, tables, and final claims need evidence checks.
- Use `aminer-data-search` for papers, authors, venues, citations, institutions, and patent-adjacent technical prior art.
- Use `autoglm-deepresearch` for competition context, public leaderboards, open-source baselines, blogs, policy, and non-paper sources.
- Use `research-paper-writer` only after evidence, experiments, and claims are already organized.
- Use engineering skills for dataset scripts, training pipelines, debugging, and reproducibility.
- Use project-management skills to turn the lifecycle into milestones, issues, and checklists.

## Required outputs

Before leaving a phase, ensure there is:

- a goal statement
- a BRT gate
- a concrete artifact or a named artifact gap
- an exit decision
- a next action owned by a person, agent, or workstream

## Result format

Respond with:

```text
Current phase:
Phase mode:
Goal:
Inputs:
Recommended approach:
Supporting skills:
Artifacts to produce:
BRT gate:
- Behavior:
- Review:
- Test:
Scope guard:
Exit criteria:
Decision:
Next action:
```
