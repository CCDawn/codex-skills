# Gherkin Reference

Use this only when writing `.feature` files or formal BDD scenarios.

## Core Keywords

- `Feature`: names the capability.
- `Rule`: groups scenarios under a business rule.
- `Background`: shared setup. Use sparingly.
- `Scenario`: one concrete example.
- `Scenario Outline`: a template with an `Examples` table.
- `Given`: preconditions.
- `When`: the action or event under test.
- `Then`: expected observable outcome.
- `And` / `But`: continuation of the previous step type.

## Scenario Outline

```gherkin
Scenario Outline: Invalid limits are rejected
  Given the supervised evolution workbench is open
  When the user enters case limit "<limit>"
  Then the workbench shows "<message>"

  Examples:
    | limit | message              |
    | -1    | limit must be >= 1   |
    | abc   | limit must be number |
```

Use outlines only when the same behavior repeats across several values. If the examples carry different meaning, split them into separate scenarios.

## Step Quality Checklist

- Keep one action in `When`.
- Put assertions in `Then`.
- Prefer domain language over implementation names.
- Keep scenarios independent.
- Do not create reusable step definitions too early; let the vocabulary settle first.
