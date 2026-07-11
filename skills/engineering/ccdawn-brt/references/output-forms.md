# BRT Output Forms

Read this file only when exact user-visible output forms, external skill menu normalization, queue/checkpoint forms, or detailed option quality rules are needed.

## Alignment Handshake

Use when the user should understand the next move, but repeated clarification would waste turns.

```text
对齐握手: 我理解你要 ...；我准备 ...；我不会 ...；我会用 ... 证明；如果这里不对，最该纠偏的是 ...
默认推进: 无自然闸门时，我将直接 ...
下一步建议: ...
```

Do not ask required questions by default. Put defaultable scope, order, verification, and route into `默认推进`. If the current user message already grants execution permission and no natural gate exists, continue after the handshake.

## Collaborative Calibration

Use when the agent's interpretation, route, plan, ordering, or tradeoff changes observable outcome, risk, validation, or next stage.

```text
协作校准: 我建议 ...；原因 ...；我排除 ...；这样理解/这样做对吗？
意图理由: 信号=...；推断=...；推荐理由=...；错判代价=...
默认推进: 无自然闸门时，我将 ...
A. 按推荐继续（推荐）...
B. 调整为 ...
C. 暂停或先解释 ...
```

The question must include the recommended answer, choosing signal, and tradeoff. Do not use this shape for low-risk `FAST_PATH` unless a high-impact assumption remains.

## External Skill Output Normalization

BRT is the final Chinese display layer. When routing to non-CCDawn external skills, preserve the external skill's safety semantics, step order, option count, and execution constraints, but translate user-visible titles, explanations, menus, and next actions into Chinese.

Rules:

- Do not expose external English templates verbatim.
- If an external skill says `exactly these options`, preserve option count, order, and meaning, not English wording.
- Keep English only for code, commands, paths, original errors, API/protocol names, skill names, enum values, symbols, and external proper names.
- Exact confirmation tokens such as `discard` may remain English; explain risk in Chinese.
- If both the external skill and BRT require `下一步建议`, merge them into one Chinese section.

`finishing-a-development-branch` menu mapping:

```text
下一步建议:
1. 本地合并回 <base-branch>
2. 推送并创建拉取请求
3. 保留当前分支，稍后处理
4. 丢弃本次工作
请选择 1-4。
```

For detached HEAD or externally managed workspaces:

```text
下一步建议:
1. 作为新分支推送并创建拉取请求
2. 保留当前状态，稍后处理
3. 丢弃本次工作
请选择 1-3。
```

Discard confirmation:

```text
这会永久删除当前分支、相关提交和可清理的 worktree。确认要丢弃时，请输入 `discard`。
```

## Candidate Intent Quality

Candidate intents help the user choose; they do not ask the user to rewrite the requirement.

Use only when ALIGN/FULL has multiple real behavior outcomes. Prefer:

- A: conservative, smallest reversible interpretation.
- B: standard recommended interpretation.
- C: expanded interpretation, only when useful.

Each option must name behavior difference, choosing signal, tradeoff, user signal, rationale, and risk if wrong. Delete any option that only says "simpler", "more complete", or "larger scope" without concrete behavior.

## Question Design

Ask only questions that change observable outcome, scope, risk, verification, route, or implementation permission.

- Start with behavior and acceptance, then technical choices.
- Default 0 required questions; blocked asks 1; alignment asks 2-3 high-signal choices when needed.
- Rank by impact: goal > scope > risk/permission > output shape > test evidence.
- Each option must include choosing signal or tradeoff and mark the recommended choice.
- If the user says "按推荐来", lock the recommended option and continue.

Do not ask local-context questions that tools can answer, equivalent naming/order questions, or implementation details that do not change user-visible results.

## Intent Lock

Use before planning or implementation when the behavior contract must be explicit.

```text
意图锁定: 用户可观察结果 = ...；拥有面 = ...；非目标 = ...；关键约束 = ...；验收证据 = ...；默认推进 = ...
```

Only add choices when a real behavior, scope, risk, or permission branch remains. If the user says "按推荐来", lock the recommended choice and continue.

## Planning Handoff

```text
方案交接: 已确认意图 = ...；范围 = ...；关键风险 = ...；验证锚点 = ...；未决项 = ...
默认推进: 用户已授权且没有自然闸门时，直接进入 `ccdawn-planning`。
下一步建议: 进入 `ccdawn-planning` 产出实施方案。
```

Do not ask whether to enter planning merely because alignment is complete. Ask only when requirements remain unstable, a high-impact tradeoff is unresolved, or the user requested a choice.

## Minimal Sufficient Solution

```text
最小充分方案: 层级 = NO_BUILD / PROJECT_REUSE / STANDARD_NATIVE / INSTALLED_DEPENDENCY / MINIMAL_BUILD；依据 = ...；剩余实现单元 = ...；外部研究 = NONE / QUICK_RESEARCH / FULL_REUSE_RESEARCH / SKIP_WITH_REASON；成功证据 = ...
```

External research is valid only when it can materially change the implementation plan. File count alone does not increase process weight.

## Bundle and Queue Forms

Use compressed forms unless the user asks for the full ledger.

```text
组合判断: Primary = ...；Secondary = ...；Deferred = ...
执行顺序: 先 ...，再 ...；并行/延后原因 ...
行动队列: Guardrail = ...；Primary Fix = ...；Telemetry Gap = ...；Deferred = ...
修复队列:
1. ... [SAFE_DIRECT]；原因 = ...
2. ... [PLAN_THEN_EXECUTE]；原因 = ...
3. ... [DEFERRED]；触发条件 = ...
当前推进项: ... [SAFE_DIRECT / PLAN_THEN_EXECUTE / DEFERRED / BLOCKED]
队列项路由: owner = ...；交接上下文 = 意图/证据/影响面/保护边界/成功证据/停止条件
下一步建议: ...
```

Queue semantics:

- `SAFE_DIRECT`: can execute and verify after "继续 / 开始修复 / 按顺序修".
- `PLAN_THEN_EXECUTE`: route to `ccdawn-planning` with the queue item handoff; BRT does not write the full plan.
- `DEFERRED`: record trigger condition only.
- `BLOCKED`: ask one blocking question.

## Next Action

`下一步建议` must be the last visible user-facing line unless platform/system appendices are required after it.

```text
下一步建议: ...
```

Default to one concrete action. Use 2-3 options only for blockers, high-risk remote writes, publish/merge/delete/migration/permission gates, or real tradeoffs; mark the recommendation.

## BRT Closing Summary

Use this only when a full ALIGN/FULL checkpoint is helpful:

```text
已对齐的真实意图:
已排除的误解:
推荐理由 / 意图理由:
对齐握手:
当前行为契约:
执行契约和保护边界:
自审结论:
验证锚点:
剩余风险:
下一步建议: ...
```
