---
name: literature-evidence-synthesis
description: Synthesizes papers, web research, experiment notes, and citations into structured research artifacts such as literature matrices, method comparisons, evidence maps, related-work outlines, and experiment hypotheses. Use when the user has gathered sources but needs them normalized, compared, clustered, or converted into evidence for a competition project, benchmark study, survey, or paper draft.
---

# Literature Evidence Synthesis

Use this skill after search and before final writing.

It turns raw sources into reusable evidence artifacts.

## Quick start

1. Identify the source set.
2. Normalize each source into comparable fields.
3. Group the sources by method, claim, dataset, metric, or theme.
4. Produce the artifact that best supports the current phase.

## Supported artifacts

- literature matrix
- method comparison table
- evidence map
- claim-to-source map
- experiment hypothesis list
- related-work outline

## Inputs

Typical inputs include:

- paper lists from `aminer-data-search`
- web findings from `autoglm-deepresearch`
- notes from code or experiment runs
- citations already collected by the user

## Output format

Respond with:

```text
Goal:
Source set:
Normalization fields:
Grouping strategy:
Artifacts to produce:
Gaps or weak evidence:
Recommended next action:
```

## Notes

- Prefer structured comparison over prose summaries.
- Keep source provenance visible.
- Separate facts, interpretations, and open questions.
- Do not jump to paper drafting until the evidence artifacts are stable.

See [EXAMPLES.md](EXAMPLES.md) for example use.
