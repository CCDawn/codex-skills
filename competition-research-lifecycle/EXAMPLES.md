# Competition Research Lifecycle Examples

## Example 1: AI competition

User request:

```text
We are doing an image classification competition. Help me run the full research workflow from dataset cleanup to final paper.
```

Recommended response shape:

```text
Current phase: Data preparation
Phase mode: phase-execution
Goal: Build a reproducible dataset pipeline and validation split for the image classification task.
Inputs: raw images, labels, competition rules, compute budget
Recommended approach:
- audit labels and duplicates
- define split strategy
- produce a dataset manifest and preprocessing report
Supporting skills:
- engineering skill for preprocessing scripts
- brt for gate definition
Artifacts to produce:
- data-manifest.json
- preprocessing-report.md
- split-strategy.md
- use the data readiness template for the phase artifact
BRT gate:
- Behavior: the dataset can be loaded, split, and regenerated reproducibly.
- Review: check leakage, duplicates, and schema drift before training begins.
- Test: rerun preprocessing and verify the same manifest and split outputs.
Scope guard: model selection is out of scope until the data artifact is stable.
Exit criteria:
- splits are reproducible
- leakage risks are reviewed
- preprocessing output is repeatable
Decision: advance
Next action: route to literature and solution research with the cleaned data assumptions
```

## Example 2: Mathematical modeling contest

User request:

```text
We need a full workflow for a mathematical modeling contest, including assumptions, experiments, and final report writing.
```

Recommended response shape:

```text
Current phase: Task framing
Phase mode: phase-execution
Goal: Turn the problem statement into measurable subproblems, constraints, and report requirements.
Inputs: contest prompt, deliverable rules, time limit
Recommended approach:
- extract assumptions and objective functions
- define evaluation criteria and deliverable contract
- identify modeling branches worth testing
Supporting skills:
- brt for phase gate
- autoglm-deepresearch for domain context if needed
Artifacts to produce:
- competition-brief.md
- metric-definition.md
- assumption-register.md
- use the task framing template for the phase artifact
BRT gate:
- Behavior: the team can restate the contest problem, assumptions, and scoring logic clearly.
- Review: check hidden constraints, unrealistic assumptions, and time risk.
- Test: verify one minimal path from problem statement to report deliverable.
Scope guard: do not start experiments until assumptions and deliverables are explicit.
Exit criteria:
- the problem is decomposed
- assumptions are explicit
- candidate modeling directions are ranked
Decision: advance
Next action: build a literature and prior-solution shortlist for the highest-value branches
```

## Example 3: Benchmark paper plus code submission

User request:

```text
Help me manage an NLP benchmark submission with experiments, ablations, and a workshop paper.
```

Recommended response shape:

```text
Current phase: Literature and solution research
Phase mode: phase-execution
Goal: Build a shortlist of methods and turn them into concrete experiment hypotheses for the benchmark.
Inputs: benchmark description, baseline repo, related work area
Recommended approach:
- use AMiner to collect core papers and citation paths
- use DeepResearch to inspect public baselines and benchmark context
- use literature-evidence-synthesis to normalize the source set
- rank methods by feasibility and expected signal
Supporting skills:
- aminer-data-search
- autoglm-deepresearch
- literature-evidence-synthesis
- brt
Artifacts to produce:
- literature-matrix.md
- method-candidates.md
- experiment-hypotheses.md
BRT gate:
- Behavior: each shortlisted method maps to a concrete experiment.
- Review: check novelty, feasibility, and evidence quality before implementation.
- Test: every method is either promoted into a hypothesis card or explicitly dropped.
Scope guard: do not branch into paper drafting while the shortlist is still unstable.
Exit criteria:
- shortlisted methods are evidence-backed
- each method maps to an experiment
- research sprawl is controlled
Decision: advance
Next action: build the minimal end-to-end baseline for the top-ranked method
```

## Example 4: Late-stage paper drafting

User request:

```text
We already have results and tables. Use the competition workflow to get us to a clean final paper draft.
```

Recommended response shape:

```text
Current phase: Paper writing
Phase mode: phase-execution
Goal: Turn validated results, tables, and related work into a coherent competition paper draft.
Inputs: experiment logs, figures, tables, references, final model choice
Recommended approach:
- organize claims by evidence
- run paper-claim-traceability on the abstract, contributions, and results sections
- route to the paper-writing skill once evidence organization is stable
Supporting skills:
- literature-evidence-synthesis
- paper-claim-traceability
- research-paper-writer
- brt
Artifacts to produce:
- paper-outline.md
- figures/
- tables/
- manuscript draft
BRT gate:
- Behavior: every important claim traces to a table, figure, experiment, or citation.
- Review: check overclaiming, missing limitations, and weak related-work positioning.
- Test: inspect whether the abstract and contributions can be justified from the current evidence pack.
Scope guard: no final submission packaging until claim traceability is clean.
Exit criteria:
- each claim is traceable
- limitations are explicit
- the draft is structurally complete
Decision: advance
Next action: package the submission bundle and run the final compliance checklist
```

## Example 5: Late discovery of data leakage

User request:

```text
We are in ablation and just found that our validation split leaked entity identities. How should the competition workflow recover?
```

Recommended response shape:

```text
Current phase: Data preparation
Phase mode: phase-recovery
Goal: rebuild a valid split strategy and restabilize downstream evidence.
Inputs: current split logic, leakage finding, affected experiments, competition rules
Recommended approach:
- isolate which runs are invalidated
- repair the split strategy and regenerate data artifacts
- mark downstream experiments and claims as stale until rerun
Supporting skills:
- brt
- engineering skill for preprocessing and reruns
Artifacts to produce:
- updated split-strategy.md
- leakage-incident.md
- rerun-priority-list.md
BRT gate:
- Behavior: downstream experiments depend on a valid, documented split.
- Review: check whether leakage touches ranking logic, features, or only validation partitions.
- Test: rerun preprocessing and verify the repaired split deterministically.
Scope guard: do not continue paper-writing with invalidated results.
Exit criteria:
- the leakage mechanism is understood
- affected runs are marked or retired
- the repaired split is reproducible
Decision: recover
Next action: rerun baseline and promoted experiments against the repaired split
```
