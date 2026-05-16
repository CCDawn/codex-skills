# Competition Research Lifecycle Examples

## Example 1: AI competition

User request:

```text
We are doing an image classification competition. Help me run the full research workflow from dataset cleanup to final paper.
```

Recommended response shape:

```text
Current phase: Data preparation
Goal: Build a reproducible dataset pipeline and validation split for the image classification task.
Inputs: raw images, labels, competition rules, compute budget
Planned work:
- audit labels and duplicates
- define split strategy
- produce a dataset manifest
Supporting skills:
- engineering skill for preprocessing scripts
- brt for gate definition
Artifacts:
- data-manifest.json
- preprocessing-report.md
- split-strategy.md
Exit criteria:
- splits are reproducible
- leakage risks are reviewed
- preprocessing output is repeatable
Next phase: Literature and solution research
```

## Example 2: Mathematical modeling contest

User request:

```text
We need a full workflow for a mathematical modeling contest, including assumptions, experiments, and final report writing.
```

Recommended response shape:

```text
Current phase: Task framing
Goal: Turn the problem statement into measurable subproblems, constraints, and report requirements.
Inputs: contest prompt, deliverable rules, time limit
Planned work:
- extract assumptions and objective functions
- define evaluation criteria
- identify modeling branches worth testing
Supporting skills:
- brt for phase gate
- autoglm-deepresearch for domain context if needed
Artifacts:
- competition-brief.md
- metric-definition.md
- assumption-register.md
Exit criteria:
- the problem is decomposed
- assumptions are explicit
- candidate modeling directions are ranked
Next phase: Literature and solution research
```

## Example 3: Benchmark paper plus code submission

User request:

```text
Help me manage an NLP benchmark submission with experiments, ablations, and a workshop paper.
```

Recommended response shape:

```text
Current phase: Literature and solution research
Goal: Build a shortlist of methods and turn them into concrete experiment hypotheses for the benchmark.
Inputs: benchmark description, baseline repo, related work area
Planned work:
- use AMiner to collect core papers and citation paths
- use DeepResearch to inspect public baselines and benchmark context
- rank methods by feasibility and expected signal
Supporting skills:
- aminer-data-search
- autoglm-deepresearch
- brt
Artifacts:
- literature-matrix.md
- method-candidates.md
- experiment-hypotheses.md
Exit criteria:
- shortlisted methods are evidence-backed
- each method maps to an experiment
- research sprawl is controlled
Next phase: Baseline system
```

## Example 4: Late-stage paper drafting

User request:

```text
We already have results and tables. Use the competition workflow to get us to a clean final paper draft.
```

Recommended response shape:

```text
Current phase: Paper writing
Goal: Turn validated results, tables, and related work into a coherent competition paper draft.
Inputs: experiment logs, figures, tables, references, final model choice
Planned work:
- organize claims by evidence
- outline the manuscript
- route to the paper-writing skill once inputs are complete
Supporting skills:
- research-paper-writer
- brt
Artifacts:
- paper-outline.md
- figures/
- tables/
- manuscript draft
Exit criteria:
- each claim is traceable
- limitations are explicit
- the draft is structurally complete
Next phase: Submission packaging
```
