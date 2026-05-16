# Codex Skills

Custom skills for Codex, focused on competition-driven research workflows.

[中文说明](README.zh-CN.md)

## Included skills

### `competition-research-lifecycle`

An end-to-end workflow skill for research competitions and benchmark-style projects. It covers:

- task framing
- data preparation
- literature and solution research
- baseline setup
- training and experimentation
- analysis and ablation
- paper writing
- submission packaging

This skill treats `brt` as a governance layer for defining phase goals, review points, and acceptance checks.

### `literature-evidence-synthesis`

A supporting research skill for turning papers, web research, experiment notes, and citations into structured evidence artifacts such as literature matrices, method comparisons, claim maps, and experiment hypotheses.

### `paper-claim-traceability`

A paper-readiness skill for checking whether every important claim in a draft can be traced to evidence such as experiments, tables, figures, citations, or qualitative examples.

## Structure

```text
competition-research-lifecycle/
  SKILL.md
  REFERENCE.md
  EXAMPLES.md
literature-evidence-synthesis/
  SKILL.md
  EXAMPLES.md
paper-claim-traceability/
  SKILL.md
  EXAMPLES.md
```

## Install in Codex

Copy the skill folders into your Codex skills directory:

```text
~/.codex/skills/
```

On Windows, that is typically:

```text
C:\Users\<you>\.codex\skills\
```

After copying, restart Codex so it reloads global skills.

## Development

- [Contributing guide](CONTRIBUTING.md)
- [MIT License](LICENSE)

## Usage

Invoke the skills in chat with prompts such as:

- `Use competition-research-lifecycle to plan this benchmark project`
- `Help me run this competition through a full research lifecycle`
- `We need a competition workflow covering data, experiments, and paper writing`
- `Use literature-evidence-synthesis to turn these papers into a literature matrix`
- `Use paper-claim-traceability to review this draft before submission`
