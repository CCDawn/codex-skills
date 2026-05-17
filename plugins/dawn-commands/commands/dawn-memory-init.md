---
description: Initialize project memory in the current project, write Project Memory Rules into AGENTS.md, and enable automatic ongoing memory maintenance through the installed agent-html-memory skill.
argument-hint: [project-type]
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit]
---

# Dawn Memory Init

Initialize persistent project memory for the current repository and make it part of normal development flow.

## Arguments

The user invoked this command with: $ARGUMENTS

Interpret `$ARGUMENTS` as an optional project type hint such as `frontend`, `backend`, `fullstack`, `library`, or `cli`.

## Instructions

When this command is invoked:

1. Detect the current project root by looking for the nearest repository root or workspace root.
2. If `.docs/project-memory/` already exists in that project:
   - do not reinitialize it
   - summarize that project memory is already active
   - remind the user that future development work will keep it synchronized automatically
3. If project memory is missing:
   - run:

```bash
node <user-home>/.codex/skills/agent-html-memory/bin/agent-html-memory-init.js <project-root> --project-type <type>
```

   - resolve `<user-home>` from the current machine before running the command
   - on Windows this is typically `C:/Users/<username>`
   - on Unix-like systems this is typically `$HOME`

4. Use the provided argument as `--project-type` when it is present and plausible. If no argument is provided, infer the type from the repository shape and choose a conservative default.
5. After initialization, confirm these outcomes:
   - `.docs/project-memory/` exists
   - `AGENTS.md` contains `Project Memory Rules`
6. Tell the user that after this one-time manual initialization, the installed `agent-html-memory` skill should handle ongoing memory reads, capture, and sync during meaningful development work in this project.

## Output requirements

- State the resolved project root.
- State whether memory was newly initialized or already active.
- If initialized, mention that `AGENTS.md` was updated.
- If the repository shape makes project type ambiguous, state the assumption you used.

## Example usage

```text
/dawn-memory-init
/dawn-memory-init frontend
/dawn-memory-init backend
```
