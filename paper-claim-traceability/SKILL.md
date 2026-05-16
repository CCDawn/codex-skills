---
name: paper-claim-traceability
description: Audits whether claims in a paper, report, or competition writeup are supported by experiments, tables, figures, citations, or qualitative evidence. Use when the user has a draft and wants to verify traceability, reduce overclaiming, strengthen limitations, or prepare a submission-ready evidence chain.
---

# Paper Claim Traceability

Use this skill late in the workflow, after experiments and drafting already exist.

## Quick start

1. Identify the draft section or full manuscript under review.
2. Extract major claims, contribution statements, and comparative statements.
3. Map each claim to supporting evidence or mark it unsupported.
4. Recommend revision, deletion, qualification, or stronger evidence collection.

## Review targets

- title and abstract claims
- contribution bullets
- related-work positioning
- methodology claims
- result interpretation
- conclusion and future-work statements

## Evidence types

- experiment logs
- tables
- figures
- citations
- qualitative examples
- error analyses
- ablation studies

## Output format

Respond with:

```text
Scope:
Claims reviewed:
Supported claims:
Weakly supported claims:
Unsupported claims:
Missing evidence:
Recommended revisions:
Submission risk:
```

## Notes

- Prefer explicit traceability over rhetorical polish.
- Flag overclaiming early.
- Distinguish missing evidence from missing writing.
- Require limitations when evidence is narrow or unstable.

See [EXAMPLES.md](EXAMPLES.md) for example use.
