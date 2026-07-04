---
name: ccdawn-bug-review
description: Use when CCDawn workflow needs a Chinese-first handoff around an existing debugging skill for a bug, regression, failing test, abnormal behavior, or suspected root cause.
---

# CCDawn Bug Review

## 目标

这是 CCDawn 的 bug 审查适配器，不是新的调试流程。

优先复用现有 skill：

- `systematic-debugging`：默认 bug、失败测试、异常行为、构建失败、性能异常、集成问题。
- `root-cause-tracing`：错误出现在深层调用链、坏值来源不清、需要倒追触发源。
- `verification-before-completion`：修复后声明完成前验证。
- `ccdawn-pr-review`：对象是 PR、diff、分支或提交范围。

只有当需要中文优先的 CCDawn 阶段交接、Workflow Ledger、修复路由或用户想先“审查 bug 再决定是否修”时，才使用本 skill 包装上述流程。

## BRT interface

- Context Boundary: 症状、失败命令、日志、相关代码/测试、用户指定范围、已排除的 PR/diff 或环境范围。
- Output Contract: 复用 skill 选择、根因状态、影响范围、下一步路由和是否允许修复。
- Allowed Action: 默认只读审查；根因 CONFIRMED 且局部低风险时可路由到 `FAST_PATH` 轻量修复；跨模块、高风险或需求不清时必须进入 planning/拆分。
- Success Evidence: 根因状态有证据支撑，下一步能路由到调试、轻量修复、规划或 PR 审阅。
- Stop Condition: 无法复现、缺失败证据、根因未确认且修复会写代码、范围扩大、高风险动作或用户要求暂停。
- Route Out: `systematic-debugging`、`root-cause-tracing`、`FAST_PATH` 轻量修复、`ccdawn-planning`、`ccdawn-task-splitting`、`ccdawn-pr-review`、`ccdawn-brt` 或 BLOCKED。

## 进入条件

使用前确认 bug 对象不是 PR/diff 审阅、不是泛项目体检，也不是纯测试约束审查。若用户实际想要“先审查 bug 再决定是否修”，本 skill 输出根因状态和修复路由；若用户已经要求直接修复，只有在根因明确、范围局部且可验证时走 `FAST_PATH`。

## 使用方式

1. 判定问题类型：bug、回归、失败测试、环境问题、测试问题、需求误解或 PR 审阅。
2. 加载并遵守最具体的现有 skill；不要复制或弱化它的硬规则。
3. 用 CCDawn 格式输出证据、根因状态、影响范围和下一步路由。
4. 需要修复时，按风险路由到轻量修复、`ccdawn-planning`、`ccdawn-task-splitting` 或 `ccdawn-bdd-tdd-development`。

## 输出契约

```text
Bug 审查路由:
- 复用 skill: systematic-debugging / root-cause-tracing / ccdawn-pr-review / ...
- 理由: ...
- Context Boundary: 症状、失败命令、日志、相关代码/测试、用户指定范围...
- Allowed Action: 只读审查 / FAST_PATH 轻量修复 / 进入方案或拆分 / 暂停
- 症状: ...
- 当前证据: ...
- 根因状态: UNKNOWN / HYPOTHESIS / CONFIRMED / ENVIRONMENT / TEST_ISSUE
- 影响范围: ...
- Success Evidence: 根因状态有证据支撑，下一步能路由到调试、轻量修复、规划或 PR 审阅
- Stop Condition: 无法复现 / 缺失败证据 / 根因未确认且修复会写代码 / 范围扩大或高风险
- 下一步:
  默认路由：<systematic-debugging / root-cause-tracing / FAST_PATH 轻量修复 / ccdawn-planning / ccdawn-task-splitting / ccdawn-pr-review / ccdawn-brt / BLOCKED>，原因...
  执行规则：根因 CONFIRMED 且局部低风险时可直接进入 FAST_PATH；根因未确认则继续证据收集；跨模块、高风险或方案分叉进入 planning/拆分；只有缺失败证据、范围不明或修复会越界时才问一个阻塞问题。
- Route Out: systematic-debugging / root-cause-tracing / FAST_PATH 轻量修复 / ccdawn-planning / ccdawn-task-splitting / ccdawn-pr-review / ccdawn-brt / BLOCKED
```

## 质量门槛

- 根因未确认时，不得提出修复方案。
- 不把 `ccdawn-bug-review` 当作 `systematic-debugging` 的替代品。
- 不为已有调试规则再写一套弱化版流程。
- 如果只是简单失败诊断，直接使用 `systematic-debugging` 并给短摘要。
