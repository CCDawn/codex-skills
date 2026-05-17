# Dawn Codex Skills Library

Custom skills for Codex, with a focus on competition-driven research workflows, behavior-gated implementation, and persistent project memory.

The `dawn-*` slash-command namespace is reserved for commands shipped by this repository.

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

### `literature-evidence-synthesis`

A supporting research skill for turning papers, web research, experiment notes, and citations into structured evidence artifacts such as literature matrices, method comparisons, claim maps, and experiment hypotheses.

### `paper-claim-traceability`

A paper-readiness skill for checking whether every important claim in a draft can be traced to evidence such as experiments, tables, figures, citations, or qualitative examples.

### `agent-html-memory`

A persistent project-memory skill for creating and maintaining `.docs/project-memory/` inside real software projects. It keeps a structured memory store, a generated HTML overview, and an index page synchronized as development moves forward.

This skill ships with an optional Codex local plugin command:

- `/dawn-memory-init`

That slash command initializes project memory once, then hands ongoing maintenance back to the skill during later development sessions.

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
literature-evidence-synthesis/
  SKILL.md
  EXAMPLES.md
paper-claim-traceability/
  SKILL.md
  EXAMPLES.md
plugins/
  dawn-commands/
    .codex-plugin/
    commands/
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
- installs bundled local plugins into `~/.codex/plugins/`
- updates `~/.agents/plugins/marketplace.json` when plugins are present

Install only selected skills:

```bash
python scripts/install_codex_library.py --skill brt --skill agent-html-memory
```

Skip plugin installation:

```bash
python scripts/install_codex_library.py --skip-plugins
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

If you installed bundled plugins, restart Codex and then install or enable `Dawn Commands` from `Local Plugins` in the app if needed.

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
- `/dawn-memory-init frontend`
