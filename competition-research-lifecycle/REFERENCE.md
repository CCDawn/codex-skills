# Competition Research Lifecycle Reference

This reference defines the phase model, per-phase BRT gates, artifacts, and routing guidance for competition-oriented research work.

## Operating model

Treat the competition as a sequence of gated phases. Each phase must answer four questions before work begins:

1. What behavior should exist after this phase?
2. What can be reviewed before expensive work continues?
3. What evidence or artifact proves the phase is complete?
4. What is explicitly out of scope for this pass?

Use BRT as the language for those questions, not as a separate business step.

## Phase 1: Task framing

Purpose:
- Understand the competition objective, scoring metric, constraints, timeline, and deliverables.

Typical inputs:
- Competition brief
- Evaluation rules
- Submission format
- Timeline and compute budget

BRT gate:
- Behavior: the team can state the exact target metric, allowed data, and final deliverables.
- Review: check for misunderstood rules, hidden constraints, leakage risks, and deadline risk.
- Test: run or inspect a minimal valid submission path if possible.

Artifacts:
- `competition-brief.md`
- `metric-definition.md`
- `submission-checklist.md`

Exit criteria:
- Metric and ranking logic are explicit.
- Submission contract is understood.
- Constraints and open risks are recorded.

## Phase 2: Data preparation

Purpose:
- Convert raw competition data into reproducible training, validation, and inference inputs.

Typical inputs:
- Raw datasets
- Metadata
- Labels
- Schema notes

BRT gate:
- Behavior: data can be loaded, versioned, split, and audited reproducibly.
- Review: check leakage, duplicates, imbalance, missing values, schema drift, and label noise.
- Test: produce a deterministic manifest or repeatable preprocessing output.

Artifacts:
- `data-manifest.json`
- `preprocessing-report.md`
- `split-strategy.md`

Exit criteria:
- Dataset versions are identifiable.
- Train/validation/test handling is reproducible.
- Known data risks are documented.

## Phase 3: Literature and solution research

Purpose:
- Identify methods, priors, baselines, and transferable ideas relevant to the competition.

Routing:
- `aminer-data-search` for academic papers and citation trails.
- `autoglm-deepresearch` for leaderboards, repos, public solutions, domain context, and non-paper sources.

BRT gate:
- Behavior: candidate approaches are converted into concrete experiment hypotheses.
- Review: check novelty, feasibility, compute fit, and evidence quality.
- Test: every candidate method maps to a testable experiment or is explicitly dropped.

Artifacts:
- `literature-matrix.md`
- `method-candidates.md`
- `experiment-hypotheses.md`

Exit criteria:
- There is a ranked method shortlist.
- Each shortlisted method has rationale and expected signal.
- Research sprawl is controlled.

## Phase 4: Baseline system

Purpose:
- Create a minimal working end-to-end system that trains, validates, infers, and submits.

Typical inputs:
- Prepared data
- Reference model choice
- Default training recipe

BRT gate:
- Behavior: one reproducible baseline can complete the full competition loop.
- Review: check interface mismatches, reproducibility, logging gaps, and invalid comparisons.
- Test: verify at least one repeatable run and one valid submission artifact.

Artifacts:
- `baseline-run.md`
- `reproducibility-log.md`
- baseline config files

Exit criteria:
- Training and inference loop works.
- Metric calculation is trusted.
- Baseline score is recorded with config and seed.

## Phase 5: Training and experimentation

Purpose:
- Improve performance through disciplined experiment design and execution.

Typical inputs:
- Baseline system
- Hypothesis list
- Compute budget

BRT gate:
- Behavior: each experiment tests a clear hypothesis with controlled variable changes.
- Review: check confounds, missing logs, uncontrolled randomness, and compute waste.
- Test: record config, seed, model version, metric output, and notes for each run.

Artifacts:
- `experiments/`
- `runs/`
- `model-registry.md`
- `training-decisions.md`

Exit criteria:
- Experiments are attributable and comparable.
- Promising directions are distinguished from noise.
- Dead ends are logged to avoid repetition.

## Phase 6: Analysis and ablation

Purpose:
- Explain why performance moved and determine which components truly matter.

BRT gate:
- Behavior: the team can justify selected methods with evidence, not only leaderboard movement.
- Review: check overfitting to public feedback, unstable wins, and unsupported causal claims.
- Test: produce at least one ablation or comparative analysis that isolates key choices.

Artifacts:
- `ablation-table.md`
- `error-analysis.md`
- `final-model-selection.md`

Exit criteria:
- Main claims are evidence-backed.
- Failure modes are understood well enough to describe.
- Final approach is justified.

## Phase 7: Paper writing

Purpose:
- Convert the validated research record into a coherent paper or report.

Routing:
- `research-paper-writer` after claims, tables, figures, and references are organized.

BRT gate:
- Behavior: each claim in the paper traces to an experiment, table, qualitative case, or citation.
- Review: check overclaiming, missing limitations, weak related work framing, and citation gaps.
- Test: verify the abstract, contributions, method, results, and limitations align with evidence.

Artifacts:
- `paper-outline.md`
- `figures/`
- `tables/`
- manuscript draft

Exit criteria:
- Draft is structurally complete.
- Claims are traceable.
- References and figures are consistent.

## Phase 8: Submission packaging

Purpose:
- Assemble the final code, model, report, appendix, and submission files required by the competition.

BRT gate:
- Behavior: the final package can be submitted or handed off without hidden dependencies.
- Review: check missing files, environment assumptions, naming mismatches, and compliance issues.
- Test: run a final packaging checklist and, where possible, a clean reproduction pass.

Artifacts:
- final submission bundle
- `submission-notes.md`
- `environment-lock.md`

Exit criteria:
- Required deliverables are present.
- Reproduction instructions are usable.
- Final risks are documented.

## Default response pattern

When this skill is triggered, respond in this shape:

```text
Current phase:
Goal:
Recommended approach:
Supporting skills:
Artifacts to produce:
BRT gate:
- Behavior:
- Review:
- Test:
Scope guard:
Next action:
```

## Scope guard

This workflow covers the competition research lifecycle. It does not replace domain expertise, invent results, or treat paper drafting as a substitute for evidence collection.
