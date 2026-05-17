# Competition Research Lifecycle Reference

This reference defines the phase model, per-phase BRT gates, checklists, templates, and routing guidance for competition-oriented research work.

## Operating model

Treat the competition as a sequence of gated phases. Each phase must answer four questions before work begins:

1. What behavior should exist after this phase?
2. What can be reviewed before expensive work continues?
3. What evidence or artifact proves the phase is complete?
4. What is explicitly out of scope for this pass?

Use BRT as the language for those questions, not as a separate business step.

Every pass should end with one of these decisions:

- `advance`: exit criteria are met and the next phase can start.
- `iterate`: stay in the same phase because the artifact is incomplete or the signal is weak.
- `recover`: move back to an upstream phase because a dependency is invalid.
- `stop`: pause because time, compute, access, or evidence is insufficient.

Use [TEMPLATES.md](TEMPLATES.md) to avoid inventing artifact formats from scratch.

## Shared artifact expectations

Unless the user asks for another format, phase artifacts should capture:

- the goal of the phase
- the exact inputs or evidence sources used
- the main decision made in the phase
- the open risks that remain
- the next action needed to advance

For experiments and papers, keep provenance visible. Record dataset versions, configs, sources, citations, and table or figure lineage.

## Phase 1: Task framing

Purpose:
- Understand the competition objective, scoring metric, constraints, timeline, and deliverables.

Enter when:
- the task or rules are still ambiguous
- the team cannot state the metric, contract, or deliverables clearly
- submission format, budget, or compliance assumptions are still fuzzy

Typical inputs:
- competition brief
- evaluation rules
- submission format
- timeline and compute budget

Checklist:
- metric and ranking logic are written down in plain language
- allowed and disallowed data or tools are explicit
- deliverables, deadlines, and team constraints are explicit
- likely leakage or compliance risks are named early

Routing:
- `brt` to lock scope and phase exit criteria
- `autoglm-deepresearch` if domain context, historical baselines, or policy context are unclear

BRT gate:
- Behavior: the team can state the exact target metric, allowed data, and final deliverables.
- Review: check for misunderstood rules, hidden constraints, leakage risks, and deadline risk.
- Test: run or inspect a minimal valid submission path if possible.

Artifacts:
- `competition-brief.md`
- `metric-definition.md`
- `submission-checklist.md`
- use the task framing template in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- metric and ranking logic are explicit
- submission contract is understood
- constraints and open risks are recorded

Recovery signals:
- the metric was misunderstood
- rules imply a different validation or submission contract
- required deliverables were discovered too late

## Phase 2: Data preparation

Purpose:
- Convert raw competition data into reproducible training, validation, and inference inputs.

Enter when:
- task rules are sufficiently clear
- raw data exists but is not yet reproducible, auditable, or split correctly

Typical inputs:
- raw datasets
- metadata
- labels
- schema notes

Checklist:
- dataset sources and versions are identifiable
- split logic is written and reproducible
- known risks such as leakage, duplicates, or noise are logged
- preprocessing outputs can be regenerated

BRT gate:
- Behavior: data can be loaded, versioned, split, and audited reproducibly.
- Review: check leakage, duplicates, imbalance, missing values, schema drift, and label noise.
- Test: produce a deterministic manifest or repeatable preprocessing output.

Artifacts:
- `data-manifest.json`
- `preprocessing-report.md`
- `split-strategy.md`
- use the data readiness template in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- dataset versions are identifiable
- train, validation, and test handling is reproducible
- known data risks are documented

Recovery signals:
- experiment results depend on an unstable or undocumented split
- preprocessing cannot be rerun
- leakage or schema drift is found later

## Phase 3: Literature and solution research

Purpose:
- Identify methods, priors, baselines, and transferable ideas relevant to the competition.

Enter when:
- baseline direction is still open
- the team has raw sources but no ranked method shortlist
- related work and public baselines are scattered

Routing:
- `aminer-data-search` for academic papers and citation trails
- `autoglm-deepresearch` for leaderboards, repos, public solutions, domain context, and non-paper sources
- `literature-evidence-synthesis` to normalize sources into comparable artifacts

Checklist:
- sources are grouped by method, dataset, metric, or claim
- each candidate method has feasibility and expected signal notes
- the shortlist is ranked instead of left as an open pile
- every shortlisted method maps to a testable experiment

BRT gate:
- Behavior: candidate approaches are converted into concrete experiment hypotheses.
- Review: check novelty, feasibility, compute fit, and evidence quality.
- Test: every candidate method maps to a testable experiment or is explicitly dropped.

Artifacts:
- `literature-matrix.md`
- `method-candidates.md`
- `experiment-hypotheses.md`
- use the research evidence and hypothesis templates in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- there is a ranked method shortlist
- each shortlisted method has rationale and expected signal
- research sprawl is controlled

Recovery signals:
- the shortlist is based on vague taste rather than evidence
- no candidate maps cleanly to an experiment
- late-stage claims reveal missing related work coverage

## Phase 4: Baseline system

Purpose:
- Create a minimal working end-to-end system that trains, validates, infers, and submits.

Enter when:
- the team has a chosen starting method or reference baseline
- data and metric handling are stable enough for implementation

Typical inputs:
- prepared data
- reference model choice
- default training recipe

Checklist:
- one reproducible run path exists end to end
- metric computation matches the competition contract
- configs, seeds, and environment assumptions are recorded
- one valid submission artifact can be produced

BRT gate:
- Behavior: one reproducible baseline can complete the full competition loop.
- Review: check interface mismatches, reproducibility, logging gaps, and invalid comparisons.
- Test: verify at least one repeatable run and one valid submission artifact.

Artifacts:
- `baseline-run.md`
- `reproducibility-log.md`
- baseline config files
- use the baseline run template in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- training and inference loop works
- metric calculation is trusted
- baseline score is recorded with config and seed

Recovery signals:
- metric code disagrees with competition scoring
- the run cannot be reproduced
- no valid end-to-end submission can be generated

## Phase 5: Training and experimentation

Purpose:
- Improve performance through disciplined experiment design and execution.

Enter when:
- the baseline loop is working
- there is a hypothesis list worth testing
- compute budget and logging discipline are defined

Typical inputs:
- baseline system
- hypothesis list
- compute budget

Checklist:
- each run changes a controlled set of variables
- every run records config, seed, and metric output
- dead ends are logged as explicitly as wins
- promotion to the next run is based on evidence, not memory

BRT gate:
- Behavior: each experiment tests a clear hypothesis with controlled variable changes.
- Review: check confounds, missing logs, uncontrolled randomness, and compute waste.
- Test: record config, seed, model version, metric output, and notes for each run.

Artifacts:
- `experiments/`
- `runs/`
- `model-registry.md`
- `training-decisions.md`
- use the experiment card template in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- experiments are attributable and comparable
- promising directions are distinguished from noise
- dead ends are logged to avoid repetition

Recovery signals:
- runs are not comparable because configs drifted invisibly
- the team cannot explain why a score changed
- public leaderboard feedback replaced local validation discipline

## Phase 6: Analysis and ablation

Purpose:
- Explain why performance moved and determine which components truly matter.

Enter when:
- there are multiple meaningful runs to compare
- method selection is becoming final
- the team needs evidence for claims, not only scores

Checklist:
- at least one comparative or ablation view isolates important changes
- error patterns or failure modes are written down
- final model choice is explained with evidence
- claim language stays within what the evidence supports

BRT gate:
- Behavior: the team can justify selected methods with evidence, not only leaderboard movement.
- Review: check overfitting to public feedback, unstable wins, and unsupported causal claims.
- Test: produce at least one ablation or comparative analysis that isolates key choices.

Artifacts:
- `ablation-table.md`
- `error-analysis.md`
- `final-model-selection.md`
- use the ablation and final-selection templates in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- main claims are evidence-backed
- failure modes are understood well enough to describe
- final approach is justified

Recovery signals:
- the chosen method only wins on noisy or unstable evidence
- there is no explanation for why the final method was promoted
- paper drafting starts before evidence is organized

## Phase 7: Paper writing

Purpose:
- Convert the validated research record into a coherent paper or report.

Enter when:
- the final model story is stable enough to describe
- tables, figures, or core experiment evidence already exist
- the team can name the contribution without guessing

Routing:
- `research-paper-writer` after claims, tables, figures, and references are organized
- `literature-evidence-synthesis` if related work or method positioning is still scattered
- `paper-claim-traceability` once a draft or structured outline exists

BRT gate:
- Behavior: each claim in the paper traces to an experiment, table, qualitative case, or citation.
- Review: check overclaiming, missing limitations, weak related work framing, and citation gaps.
- Test: verify the abstract, contributions, method, results, and limitations align with evidence.

Checklist:
- the paper outline follows the available evidence
- each contribution statement has supporting material
- limitations and uncertainty are explicit
- references, tables, and figures are internally consistent

Artifacts:
- `paper-outline.md`
- `figures/`
- `tables/`
- manuscript draft
- use the paper evidence map template in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- draft is structurally complete
- claims are traceable
- references and figures are consistent

Recovery signals:
- abstract claims outrun the evidence
- results sections use tables with unclear lineage
- related work is too thin to justify positioning

## Phase 8: Submission packaging

Purpose:
- Assemble the final code, model, report, appendix, and submission files required by the competition.

Enter when:
- the final draft or final model is already chosen
- deliverables are known and mostly complete
- handoff or submission risk matters more than exploration

BRT gate:
- Behavior: the final package can be submitted or handed off without hidden dependencies.
- Review: check missing files, environment assumptions, naming mismatches, and compliance issues.
- Test: run a final packaging checklist and, where possible, a clean reproduction pass.

Checklist:
- required files are present and named correctly
- environment and reproduction instructions are usable
- final claims match the submitted artifact versions
- known residual risks are documented for handoff

Artifacts:
- final submission bundle
- `submission-notes.md`
- `environment-lock.md`
- use the submission checklist template in [TEMPLATES.md](TEMPLATES.md)

Exit criteria:
- required deliverables are present
- reproduction instructions are usable
- final risks are documented

Recovery signals:
- a final file depends on undocumented local state
- the submission bundle and paper refer to different results
- last-minute packaging reveals a missing upstream artifact

## Default response pattern

When this skill is triggered, respond in this shape:

```text
Current phase:
Phase mode:
Goal:
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

## Scope guard

This workflow covers the competition research lifecycle. It does not replace domain expertise, invent results, or treat paper drafting as a substitute for evidence collection.
