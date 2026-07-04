---
name: ccdawn-goal-loop
description: Use when the user gives a goal-oriented request that needs explicit success evidence, strict constraints, bounded scope, allowed inputs or tools, next-step selection rules, iterative progress, or stop-on-blocker reporting.
---

# Goal Loop

这个 skill 用来把一个目标变成可执行、可验证、可停止的工作回路。

它不是泛泛的 brainstorming，也不是 BRT 的替代品。它关注的是：目标是否清楚、证据是否足够、约束是否被守住、下一步是否值得做、以及什么时候必须停下来报告。

## BRT interface

- Context Boundary: 当前目标、可用输入/工具/文件范围、明确约束、已获得证据和本轮迭代对象。
- Output Contract: goal contract、当前行动、advance/iterate/stop 决策、证据和 Route Out。
- Allowed Action: 只执行 goal contract 允许的最小下一步；写入、联网、安装、删除、迁移、发布或权限动作必须在 contract 中显式允许。
- Success Evidence: 当前行动产出能满足或推进 `Evidence` 字段的可检查证据。
- Stop Condition: 约束会被突破、没有有效下一步、缺少必须信息/权限、连续失败无法产生新证据、或用户要求暂停。
- Route Out: 继续 goal loop、回到 `ccdawn-brt` 重新对齐目标、进入具体 owner skill、`ccdawn-completion-summary`，或 BLOCKED。

## Goal contract

先把下面 6 个字段补齐：

- `Goal`：Codex 最终要完成什么
- `Evidence`：什么证据能确认结果有效
- `Constraints`：哪些限制条件不能被破坏
- `Allowed scope`：允许使用的输入、工具、文件范围或操作边界
- `Next-step rule`：每一轮迭代后如何判断下一步最优行动
- `Blocker protocol`：遇到阻塞或无路可走时如何停止并汇报

映射到 BRT 时：

- `Goal` -> Desired Outcome；
- `Evidence` -> Success Evidence；
- `Constraints` + `Allowed scope` -> Allowed Actions / Out of Scope；
- `Next-step rule` -> Route Out 和下一轮选择规则；
- `Blocker protocol` -> Stop Condition 和 BLOCKED 输出。

## Operating rules

1. 如果字段缺失，并且会影响执行路径，先只问最关键的一个。
2. 在动手前，先复述一遍填好的 goal contract。
3. 每一轮只做能最大化新证据、同时不突破约束的最小下一步。
4. 每轮结束时，明确判断是 `advance`、`iterate` 还是 `stop`。
5. 如果已经阻塞，或者没有有效路径可以继续，必须停止，不要硬推进。

## Stop rule

一旦停止，必须报告：

- 已经尝试过的方法
- 已获得的证据
- 当前阻塞点
- 还需要什么信息、权限或资源才能继续

## Output format

响应时使用：

```text
Goal:
Evidence:
Constraints:
Allowed scope:
Next-step rule:
Blocker protocol:
Allowed action:
Current action:
Decision:
Route Out:
Success Evidence:
Stop Condition:
If blocked:
- Tried methods:
- Evidence obtained:
- Current blocker:
- Needed info or permission:
```

## When to use

- 用户给出一个明确目标，但需要先变成可执行合同
- 用户要求每轮迭代后根据证据和约束决定下一步
- 用户要求遇到阻塞时停止并报告
- 用户需要一个 bounded workflow，而不是开放式探索

See [EXAMPLES.md](EXAMPLES.md) for concrete prompt patterns and stop cases.

