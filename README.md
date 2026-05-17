# Dawn Codex Skills Library

Custom skills for Codex, with a focus on competition-driven research workflows, behavior-gated implementation, and persistent project memory.

[中文说明](README.zh-CN.md)

## Included skills

### `brt`

The Behavior / Review / Test workflow skill. It acts as a pre-implementation gate for turning vague behavior changes into explicit examples, review lenses, acceptance criteria, and test intentions before code changes begin.

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
It now ships with a reference guide, a tighter response contract, and copy-ready phase templates.

### `literature-evidence-synthesis`

A supporting research skill for turning papers, web research, experiment notes, and citations into structured evidence artifacts such as literature matrices, method comparisons, claim maps, and experiment hypotheses.

### `paper-claim-traceability`

A paper-readiness skill for checking whether every important claim in a draft can be traced to evidence such as experiments, tables, figures, citations, or qualitative examples.

### `agent-html-memory`

A persistent project-memory skill for creating and maintaining `.docs/project-memory/` inside real software projects. It now supports shared multi-session work lanes under `.docs/project-memory/lanes/`, a generated HTML overview that aggregates those lanes, and a root `PROJECT_MEMORY.html` shortcut for humans.

Ask Codex to initialize project memory in natural language, or explicitly invoke the skill in chat. After initialization, the skill handles ongoing maintenance during later development sessions.

## Structure

```text
agent-html-memory/
  SKILL.md
  agents/
  bin/
  references/
  scripts/
brt/
  SKILL.md
  agents/
  references/
competition-research-lifecycle/
  SKILL.md
  REFERENCE.md
  EXAMPLES.md
  TEMPLATES.md
literature-evidence-synthesis/
  SKILL.md
  EXAMPLES.md
paper-claim-traceability/
  SKILL.md
  EXAMPLES.md
scripts/
  install_codex_library.py
```

## Install in Codex

Install the whole library with one command:

```bash
python scripts/install_codex_library.py
```

That command:

- copies every skill in this repository into `~/.codex/skills/`
- removes any legacy plugins that this repository used to ship

Install only selected skills:

```bash
python scripts/install_codex_library.py --skill brt --skill agent-html-memory
```

If you prefer manual installation, copy the skill folders into your Codex skills directory:

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
- `Initialize project memory for this repo`
- `Use agent-html-memory to initialize project memory for this repo as a frontend project`
