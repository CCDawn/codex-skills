---
name: goal-loop
description: 将用户给出的目标、可验证证据、必须遵守的限制、允许使用的输入和工具边界、下一步判断规则，以及阻塞停止条件整理成一个可执行的 goal contract，并按迭代回合推进。Use when the user provides a goal 达成 request, wants explicit success evidence, strict constraints, bounded scope, next-step selection rules, or stop-on-blocker reporting.
---

# Goal Loop

这个 skill 用来把一个目标变成可执行、可验证、可停止的工作回路。

它不是泛泛的 brainstorming，也不是 BRT 的替代品。它关注的是：目标是否清楚、证据是否足够、约束是否被守住、下一步是否值得做、以及什么时候必须停下来报告。

## Goal contract

先把下面 6 个字段补齐：

- `Goal`：Codex 最终要完成什么
- `Evidence`：什么证据能确认结果有效
- `Constraints`：哪些限制条件不能被破坏
- `Allowed scope`：允许使用的输入、工具、文件范围或操作边界
- `Next-step rule`：每一轮迭代后如何判断下一步最优行动
- `Blocker protocol`：遇到阻塞或无路可走时如何停止并汇报

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
Current action:
Decision:
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
