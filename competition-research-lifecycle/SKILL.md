---
name: competition-research-lifecycle
description: Orchestrates the full lifecycle of competition-driven research projects from task framing through data preparation, literature review, baseline setup, training, analysis, paper writing, and submission packaging. Use when the user is working on a research competition, Kaggle-style challenge, academic contest, benchmark track, or any end-to-end workflow that combines data work, experiments, and a paper or report deliverable.
---

# Competition Research Lifecycle

Use this skill to run a competition project as a staged research program.

`brt` is the governance layer for this workflow. It does not replace any phase. Use it to define behavior, review risks, and set acceptance checks before advancing a phase.

## Quick start

1. Identify the current phase.
2. Lock the phase goal, inputs, outputs, and exit criteria with BRT language.
3. Route to the right supporting skill for the work.
4. Produce the required artifact before moving on.

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
See [EXAMPLES.md](EXAMPLES.md) for example invocations across common competition types.

## Routing rules

- Use `aminer-data-search` for papers, authors, venues, citations, institutions, and patent-adjacent technical prior art.
- Use `autoglm-deepresearch` for competition context, public leaderboards, open-source baselines, blogs, policy, and non-paper sources.
- Use `research-paper-writer` only after evidence, experiments, and claims are already organized.
- Use engineering skills for dataset scripts, training pipelines, debugging, and reproducibility.
- Use project-management skills to turn the lifecycle into milestones, issues, and checklists.

## Required outputs

Before leaving a phase, ensure there is:

- a goal statement
- a BRT-style review summary
- a concrete artifact
- an exit decision

## Result format

Respond with:

```text
Current phase:
Goal:
Inputs:
Planned work:
Supporting skills:
Artifacts:
Exit criteria:
Next phase:
```
