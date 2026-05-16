---
name: brt
description: "BRT workflow: Behavior, Review, Test. A pre-implementation gate for turning vague feature ideas into validated behavior designs, review questions, acceptance criteria, and test plans. When this skill is used, do not edit code, run implementation commands, or commit until a BRT checkpoint has been shown and the user confirms, unless the user explicitly says to skip the checkpoint. Trigger proactively for requests involving expected behavior, defaults, memory/restore behavior, permissions, state transitions, user expectations, edge cases, completion criteria, broad loops, safety gates, promotion/apply/rollback workflows, persistence, or public API behavior."
---

# BRT

## Overview

Use BRT before implementation when an idea needs to become a clear, reviewed, testable behavior design. BRT means:

- Behavior: understand intent, compare approaches, and express the chosen behavior as examples and Given/When/Then scenarios.
- Review: recommend relevant review perspectives, get user confirmation, then challenge the behavior design through those lenses.
- Test: map the reviewed scenarios to the smallest useful tests and proceed with TDD when implementation is requested.

Treat BRT as a pre-implementation gate, not a post-implementation summary.

Hard rule: using BRT means stop before implementation. The first BRT response must be a Behavior/Review/Test checkpoint or a question needed to create one. Do not implement first and summarize later.

If the user says "start", "开始做", "继续做", "重新使用 BRT", or similar wording, interpret that as "start the BRT gate" unless they explicitly say "skip checkpoint and implement now."

Do not use this for obvious typos, mechanical refactors, dependency bumps, or tiny internal helper changes with no behavior ambiguity.

Use the slogan: define behavior, challenge behavior, protect behavior.

Default to compact output. Expand only when the user asks, the work is high risk, or producing a design/documentation artifact.

## Trigger Signals

Use BRT proactively when the request includes or implies:

- Expected behavior: "should", "when X happens", "what should happen", "default behavior".
- User expectation: "user expects", "first time", "again", "remember", "restore", "resume".
- State transitions: status changes, workflow steps, lifecycle, retry, cancellation, rollback.
- Permissions or trust: access, roles, privacy, secrets, data retention, safety.
- Edge cases: invalid input, empty state, failure path, partial completion, conflict.
- Acceptance criteria: "done means", "how to test", "BDD", "Given/When/Then", "验收".
- Agent behavior: tool choice, memory, planning, handoff, autonomous workflow, repeated task behavior.

If these signals are present and the user did not explicitly ask for BRT, briefly say you are using BRT because the behavior needs clarification before implementation.

## First Response

When BRT is invoked for implementation work, start by deciding whether this is Quick BRT or Full BRT.

For Full BRT, the first response should define behavior and confirm review perspectives, not ask for implementation yet:

```text
I am using BRT as a pre-implementation gate.

Behavior:
- Goal: [one sentence]
- Example: Given [context], When [action], Then [observable outcome]
- Scope guard: [what this pass will not cover]

Review:
- Recommended perspectives:
  - [perspective]: [why]
  - [perspective]: [why]
  - [perspective]: [why]

Confirm these review perspectives, or tell me what to replace.
```

For Quick BRT only, use a compact checkpoint:

```text
I am using BRT as a pre-implementation gate.

Behavior:
- Locked behavior: [draft one sentence]
- Scope guard: [what this pass will not cover]

Review:
- Recommended perspectives:
  - [perspective]: [why]
  - [perspective]: [why]
  - [perspective]: [why]
- Blocking question: [one question if needed, otherwise "none"]

Test:
- Test anchor: [main scenario/test that will protect the behavior]
- Implementation target: [one sentence]

Confirm these review perspectives and proceed to implementation?
```

If the behavior is not clear enough to draft this checkpoint, ask exactly one clarifying question instead.

## Workflow

Before the full workflow, consider whether the request can use a fast path. If the behavior is narrow, low risk, and already mostly clear, propose Quick BRT and ask for confirmation:

```text
This looks small enough for Quick BRT: behavior summary, recommended review perspectives, top questions, and test mapping. Use quick mode?
```

If the user confirms, use Quick BRT. If the user declines, use the full workflow. If the work touches security, data loss, permissions, payments, migrations, public API contracts, or broad architecture, do not suggest quick mode.

If the user does not answer the mode question but continues with the request, default to Quick BRT for small low-risk tasks and Full BRT for medium or high-risk tasks. State the default briefly and continue.

### Behavior

1. Inspect the project context first: nearby code, tests, docs, recent commits, `AGENTS.md`, `CONTEXT.md`, issues, plans, or existing feature files.
2. Identify the user goal, actor, trigger, observable outcome, constraints, and success criteria.
3. Ask one clarifying question at a time only when the answer changes the design. Prefer a multiple-choice question when useful.
4. Propose 2-3 approaches with trade-offs. Lead with the recommended option and explain why.
5. Convert the recommended option into concrete examples before writing general rules.
6. Write BDD scenarios using Given/When/Then for behavior that crosses UI, CLI, workflow, persistence, business rules, or agent state.
7. Write a scope guard that states what this BRT will not cover.

### Review

8. Recommend the review perspectives that best fit the feature, then ask the user to confirm or modify the set before running the review.
9. Review the design from the confirmed perspectives and produce challenge questions, risks, and suggested changes.
10. Revise the examples, scenarios, or approach when the review reveals a real gap. If review reveals the goal itself is wrong or incomplete, return to Behavior instead of patching scenarios.

### Test

11. Map each scenario to the lowest useful test layer: unit, integration, end-to-end, or manual acceptance.
12. Choose the artifact level or ask when ambiguous: chat-only, design document, or implementation artifacts.
13. Present a BRT checkpoint and confirm direction before implementation.
14. If the user confirms implementation, proceed with TDD: make one scenario fail, make it pass, refactor, verify.
15. If the user wants documentation, save the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md` unless the repo uses another convention.

## Stage Exit Criteria

Do not let BRT become endless discussion. Move forward when each stage has enough clarity.

Behavior is complete when:

- The actor, trigger, and observable outcome are explicit.
- At least two concrete examples exist, unless the behavior truly has only one path.
- The happy path and at least one edge or failure path are named.
- Important constraints, out-of-scope items, and a scope guard are stated.

Review is complete when:

- Review perspectives were recommended and the user confirmed or modified them.
- Each confirmed perspective produced either a question/risk/change with severity or a clear "no major concern."
- High-impact review findings became design changes, open questions, or explicit accepted risks.
- The review used no more perspectives than needed.
- If alternatives, Blocking findings, or design-changing review findings exist, the decision log records the chosen path and rejected alternative.

Test is complete when:

- Each core scenario maps to a test layer or an intentional manual acceptance check.
- Full BRT includes at least one concrete behavior example before the implementation checkpoint.
- The plan includes at least one happy path and one edge/failure path when applicable.
- The test mapping chooses a specific test strategy instead of leaving "or" alternatives for implementation time.
- The selected tests are the fewest tests that protect the agreed behavior.
- Blocking questions are resolved before implementation.
- At most one non-blocking open question remains before implementation.
- The BRT checkpoint has been shown before code changes.

## Implementation Gate

Before modifying code, present a compact BRT checkpoint and wait for user confirmation unless the user explicitly asked to design and implement in one pass.

A BRT checkpoint is not a substitute for BRT. For Full BRT, do not ask to implement until the response has included at least one concrete behavior example, review findings with severity, test mapping, and a decision log entry when a non-obvious decision exists.

Use this shape:

```text
BRT checkpoint:
- Behavior locked: [one sentence]
- Scope guard: [what is excluded]
- Review perspectives: [confirmed or proposed]
- Blocking issues: [none or list]
- Test anchor: [main test/scenario]
- Implementation target: [one sentence]

Proceed to implementation?
```

If the user asked for a broad loop, roadmap step, architecture change, safety gate, promotion/apply workflow, rollback, permissions, persistence, or public API behavior, use Full BRT and require this checkpoint before editing code.

Do not use "BRT result" only after implementation. If work has already been implemented without a BRT checkpoint, call that out honestly and use BRT to review the result before continuing.

## Quick BRT

Use Quick BRT only after asking and receiving confirmation. It reduces ceremony while preserving the BRT shape.

Quick BRT output:

```text
Behavior summary:
- Actor:
- Trigger:
- Outcome:
- Out of scope:

Recommended review perspectives:
- [perspective]: [why]
- [perspective]: [why]
- [perspective]: [why]

Top questions:
- [highest-value question/risk]
- [highest-value question/risk]
- [highest-value question/risk]

Test mapping:
- [scenario] -> [test layer]
```

After the user answers the top questions or confirms assumptions, present a BRT checkpoint before implementation or documentation.

## Question Discipline

Ask about behavior, not implementation trivia:

- Who or what performs the action?
- What state exists before the action?
- What action or event triggers the behavior?
- What outcome can the user, CLI, test, log, file, or agent observe?
- What edge case would make this behavior surprising?
- What should explicitly remain out of scope?

Keep momentum. If ambiguity is low risk, state the assumption and continue.

## Scope Guard

Write a scope guard during Behavior to prevent the design from expanding during review:

```text
Scope guard:
This BRT covers [specific behavior], not [larger adjacent feature].
```

Example:

```text
Scope guard:
This BRT covers restoring the last supervised evolution dataset defaults, not building a full preset manager.
```

If Review discovers a larger feature is actually necessary, call that out as a separate follow-up instead of silently expanding the current BRT.

## Approach Comparison

Use this compact shape:

```text
Recommended: [approach]
Why: [reason]

Alternative A: [trade-off]
Alternative B: [trade-off]
```

Prefer the smallest design that satisfies the behavior and leaves a clear extension path.

## Review Pass

After drafting the examples and scenarios, recommend 3-5 review perspectives that fit the feature. Ask the user to confirm the list or replace any perspective before doing the review.

Avoid over-review. Prefer 3 perspectives for normal work. Use 4-5 only when the work is high risk, cross-functional, security-sensitive, user-facing in a surprising way, or creates a durable public contract.

Always include these baseline perspectives unless clearly irrelevant:

- Primary user
- Maintainer
- Test/QA

Add optional perspectives from these common lenses, or invent more specific ones when the feature calls for it:

- Primary user: Is the behavior understandable, useful, forgiving, and visible at the right moment?
- New user: Is the first-run experience clear and hard to misuse?
- Power user: Does the workflow stay efficient and configurable without clutter?
- Product owner: Does it solve the actual user goal, avoid scope creep, and define success clearly?
- Domain expert: Does the language match the domain, and are important rules or exceptions missing?
- Maintainer: Is the design simple, compatible with existing architecture, and easy to evolve?
- Test/QA: Are edge cases, failure states, regressions, and observability covered?
- Security/privacy: Could the behavior leak data, persist sensitive state, grant excess access, or enable misuse?
- Operations/support: Will failures be diagnosable, recoverable, and explainable?
- Future integrator/plugin author: Does the behavior expose stable contracts and extension points?

Recommend perspectives in this shape and pause for confirmation:

```text
Recommended review perspectives:
- Primary user: [why this lens matters]
- Maintainer: [why this lens matters]
- Test/QA: [why this lens matters]

Confirm these, or tell me which perspectives to replace.
```

After the user confirms or modifies the set, output one concise concern or question for each confirmed lens. Do not invent busywork; if a confirmed lens turns out not to apply, say why and ask whether to replace it.

Classify review findings:

- Blocking: must resolve before implementation.
- Important: should resolve before implementation unless the user accepts the risk.
- Optional: can defer without weakening the core behavior.

Use this shape:

```text
Review:
- User [Blocking|Important|Optional]: [question/risk/change]
- Engineering [Blocking|Important|Optional]: [question/risk/change]
- Test/QA [Blocking|Important|Optional]: [question/risk/change]

Design changes from review:
- [scenario, rule, or approach change]
```

If a review point changes behavior, update the examples and scenarios before moving to test mapping.

## Decision Log

Record the important decisions made during BRT. Keep it short and useful for future maintainers.

Use this shape:

```text
Decision log:
- Decision: [what will be true]
  Why: [reason]
  Rejected: [alternative not chosen]
  Reason rejected: [short reason]
```

Only log decisions that affect behavior, test scope, architecture direction, or future extension.

Do not log obvious decisions.

Decision log is mandatory for Full BRT when any of these are present:

- Alternatives were compared.
- A Blocking review finding was raised.
- Review changed the design.
- A scope guard excludes a tempting adjacent feature.
- A non-obvious architecture, data, security, persistence, or public API choice was made.

## Example Mapping

Write examples before scenarios:

```text
Feature: Remember supervised evolution settings

Rule: The workbench reuses the last successful configuration

Example: Dataset source
- Given: previous run used dataset "custom_prompt_jsonl" with limit 2
- When: the workbench opens again
- Then: dataset and limit prompts default to those values

Example: Bundle source
- Given: previous run used bundle "saved_bundle" with keep_worktree true
- When: the workbench opens again
- Then: bundle and keep_worktree prompts default to those values
```

Use this map to find missing cases and decide what deserves tests.

## Scenario Style

Use Given/When/Then for stakeholder-readable behavior:

```gherkin
Feature: Remember supervised evolution settings

  Scenario: Reopening the workbench reuses the previous dataset settings
    Given the user previously ran supervised evolution with dataset "custom_prompt_jsonl"
    And the case limit was 2
    When the user opens the supervised evolution workbench again
    Then "custom_prompt_jsonl" is offered as the default dataset
    And "2" is offered as the default case limit
```

Rules:

- Use `Given` for context that already exists.
- Use `When` for the single behavior under test.
- Use `Then` for observable outcomes.
- Use product language before implementation language.
- Avoid UI click details unless the exact interaction matters.
- Avoid `.feature` files unless the repo already uses a BDD framework or non-developers will read/write them.

For detailed Gherkin syntax, read `references/gherkin.md`.

## Test Mapping

Choose the lowest layer that proves the behavior:

- Unit test: isolated business rule, parser, formatter, policy, state decision.
- Integration test: persistence, CLI prompt flow, filesystem, multiple modules, agent workflow.
- End-to-end test: real browser/terminal flow or behavior only visible through the full product.
- Manual acceptance: visual or exploratory behavior that should be checked but not automated yet.

Prefer the fewest tests that protect the agreed behavior. Do not create one brittle test for every line of a scenario when a smaller set of tests covers the same risk.

## Artifact Level

Choose the lightest artifact level that matches the user's intent. Ask only when ambiguous.

- Chat-only: Use for quick clarification, small behavior decisions, or when the user asks to think through an idea.
- Design document: Use when the user asks for docs, plans, handoff, team review, or a durable decision record. Save to `docs/plans/YYYY-MM-DD-<topic>-design.md` unless the repo uses another convention.
- Implementation artifacts: Use when the user asks to build it. Produce or update tests, code, and any necessary plan/checklist.

If using Quick BRT, default to chat-only unless the user asks for a file or implementation.

## Result Summary

End every BRT pass with a short result summary. For Full BRT, this is mandatory both before implementation handoff and after implementation completes.

```text
BRT result:
- Behavior locked: [one sentence]
- Review blockers: [none or list]
- Test anchor: [main test/scenario that protects the behavior]
- Open question: [none or one non-blocking question]
- Next action: [implement, document, ask user, defer]
```

Do not proceed to implementation with unresolved Blocking review findings. Before implementation, reduce open questions to zero or one non-blocking question.

After implementation, include the same result shape with verification filled in:

```text
BRT result:
- Behavior shipped: [one sentence]
- Review blockers: [resolved / none]
- Test anchor: [tests actually run]
- Open question: [none or one non-blocking question]
- Next action: [merge, review diff, follow-up]
```

Python projects can encode BDD scenarios directly in pytest:

```python
def test_reopening_workbench_uses_saved_dataset_defaults(...):
    # Given
    save_last_run(dataset_name="custom_prompt_jsonl", dataset_limit=2)

    # When
    defaults = open_supervised_evolution_workbench()

    # Then
    assert defaults.dataset_name == "custom_prompt_jsonl"
    assert defaults.dataset_limit == 2
```

## Output Formats

For clarification/design:

```text
Goal:
Assumptions:
Scope guard:
Recommended approach:
Alternatives:
Rules:
Examples:
Scenarios:
Review:
Decision log:
Test mapping:
Open questions:
```

For implementation:

```text
Implementation target:
Scenario under test:
RED:
GREEN:
Refactor:
Verification:
```

## Finishing

Before closing the loop, verify the design answers:

- What behavior will exist after the change?
- How will the user or system observe it?
- What did the scope guard exclude?
- Which examples prove it?
- Which perspectives challenged it, and what changed?
- Which decisions were recorded, and why?
- Which tests will protect it?
- What is intentionally out of scope?

Before implementing, state a one-sentence implementation target that freezes the behavior to build.
