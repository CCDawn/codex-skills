# Codex Skills

Custom skills for Codex, focused on competition-driven research workflows.

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

## Structure

```text
competition-research-lifecycle/
  SKILL.md
  REFERENCE.md
  EXAMPLES.md
```

## Usage

Install or copy the skill into your Codex skills directory, then invoke it in chat with prompts such as:

- `Use competition-research-lifecycle to plan this benchmark project`
- `Help me run this competition through a full research lifecycle`
- `We need a competition workflow covering data, experiments, and paper writing`
