---
name: ccdawn-completion-summary
description: Use after CCDawn development, verification, or a workflow stage ends, before claiming completion, moving to another stage, committing, pushing, or creating a PR; applies when fresh evidence, requirement coverage, residual risk, and next-step choices must be summarized.
---

# CCDawn Completion Summary

## 目标

用新鲜证据确认当前阶段是否真的完成，并给用户一个低噪声总结。此阶段只验证和汇报，不补做新功能。

核心原则：

```
没有新鲜验证证据，就不要声称完成。
```

## 进入条件

使用前确认已有：

- 已对齐需求或任务图；
- 已完成的实现、验证或阶段产物；
- 可以运行或检查的验证证据；
- 需要汇报给用户的下一步决策。

如果发现关键任务没做完，回到 `ccdawn-bdd-tdd-development` 或 `ccdawn-task-splitting`，不要把未完成包装成总结。

## 验证门槛

汇报前必须：

1. 识别要证明的 claim：完成、修复、测试通过、可提交、可进入下一步。
2. 运行或读取能证明 claim 的新鲜证据。
3. 检查输出、退出码、失败数、覆盖项。
4. 对照需求和任务图逐项判断。
5. 只陈述证据能支持的结论。

不能用这些话代替证据：

- “应该可以”
- “看起来没问题”
- “理论上”
- “我已经改了所以完成”
- “测试之前通过过”

## 输出契约

默认输出：

```text
完成总结:
- 结论: COMPLETE / PARTIAL / BLOCKED
- 需求覆盖:
  - 已满足: ...
  - 未满足: ...
  - 明确不做: ...
- 验证证据:
  - 命令/检查: ...
  - 结果: ...
- 主要变更: ...
- 副作用和风险: ...
- 交付状态: 可提交/需补测/需返工/等待用户决策

下一步:
A. 提交/推送/准备 PR（证据充分时推荐）...
B. 回到 ccdawn-bdd-tdd-development 补任务...
C. 回到 ccdawn-planning 或 ccdawn-brt 调整方向...
D. 暂停...
```

## 结论规则

- `COMPLETE`：所有关键任务完成，验证通过，没有未解决阻塞，满足已确认意图。
- `PARTIAL`：有可用进展，但仍缺关键任务、验证或用户决策。
- `BLOCKED`：当前无法继续，必须说明阻塞原因、影响步骤、可选修复和一个最关键问题。

## 汇报风格

- 中文优先；
- 少解释流程，多给结论和证据；
- 不重复用户已经知道的背景；
- 不把日志整段贴给用户，只提取能证明结论的关键行；
- 如果验证失败，直接说失败，不粉饰。

## 阶段交接

每次总结后必须给下一步选择。

如果用户选择继续开发，使用 `ccdawn-bdd-tdd-development`。如果用户发现需求方向不对，回到 `ccdawn-brt`。如果用户要进入 PR 审阅而还没有 CCDawn 专用 PR skill，可临时使用现有 code review skill，并在后续新增 `ccdawn-pr-review`。
