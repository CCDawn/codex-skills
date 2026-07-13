---
name: ccdawn-completion-summary
description: Use when completed work needs formal cross-stage or cross-session synthesis, resumed-task closure, durable handoff evidence, deferred-risk accounting, or PR/release readiness evidence that cannot be represented by the current owner's normal verification and concise final response.
license: MIT
---

# CCDawn Completion Summary

## 目标

用新鲜证据完成正式交接或跨阶段收口。普通 FAST_PATH 和有界 COMPACT_FLOW 由当前 owner 验证后直接汇报，不单独加载本 skill。

核心原则：

```
没有新鲜验证证据，就不要声称完成。
```

总结阶段不直接补写功能；但发现可恢复缺口时，必须把用户带回最具体的开发、debug 或验证阶段，而不是把半成品包装成最终汇报。

## BRT interface

- Context Boundary: 已确认需求、任务图、完成项、diff、验证命令/日志/截图、保护边界、剩余风险和交付目标。
- Output Contract: `COMPLETE / PARTIAL / BLOCKED` 结论、需求覆盖、验证证据、保护边界检查、恢复动作、交付状态和 Route Out。
- Allowed Action: 只验证、读取证据和总结；不补写新功能、不削弱测试、不提交/推送/发布；可恢复缺口必须路由到最具体开发/debug/验证阶段。
- Success Evidence: 每个完成 claim 都有新鲜命令、检查、日志、截图或结构性证据支撑，并对照 critical tasks 和已确认意图。
- Stop Condition: 关键任务未完成、新鲜证据缺失、NEEDS_CHANGE 未解决、保护边界越界、需要用户决策或高风险交付动作。
- Route Out: `ccdawn-pr-review`、提交/PR 准备、对应开发模式、`ccdawn-bug-review`、`ccdawn-planning`、`ccdawn-brt` 或 BLOCKED。

## 统一输出标准

- 用户可见输出默认中文；只有代码、命令、路径、错误原文、API/协议名、skill 名、状态枚举和外部专名保留英文。
- 报告、方案、审查、阶段文档和交接摘要使用中文标题与中文字段；内部字段对外翻译为：上下文边界、输出契约、允许动作、成功证据、停止条件、路由出口、下一步建议。
- 若必须保留英文状态或枚举，先用中文解释其含义。
- 用户可见正文末尾保留 `下一步建议: ...`，除非被更高优先级系统附录隔开。

## Owner 接入规则

进入本 skill 前先做轻量 owner 自检：

- 如果用户主目标不属于本 skill 的 owner 范围，不继续执行；回 `ccdawn-brt` 做 Owner 仲裁，或转交更具体 owner。
- 如果本 skill 只覆盖复合任务的一部分，只处理当前路由契约覆盖的 Primary/Secondary，不吞掉其他 owner。
- 如果发现 planning/development 正在替代更具体 owner，先输出路由修正，再进入正确 owner。

## 进入条件

只在至少存在一项额外价值时进入：跨会话恢复、跨 owner/stage 综合、正式交接、Deferred/未决风险需要持久化、或 PR/发布前需要独立证据包。进入前确认已有：

- 已对齐需求或任务图；
- 已完成的实现、验证或阶段产物；
- 可以运行或检查的验证证据；
- 涉及写入时，有当前 Execution Contract、保护边界和 Success Evidence；缺失时先从需求、任务图和 diff 快速补齐；
- 需要汇报给用户的下一步决策。

如果只是当前 owner 完成了普通实现和验证，直接给简短完成说明，不进入本 skill。如果发现关键任务没做完，回到最具体的开发/debug owner；任务边界本身错误时回 `ccdawn-planning` 或 `ccdawn-brt`，不要为补形式进入任务拆分。

## 验证门槛

汇报前必须：

1. 识别要证明的 claim：完成、修复、测试通过、可提交、可进入下一步。
2. 运行或读取能证明 claim 的新鲜证据。
3. 检查输出、退出码、失败数、覆盖项。
4. 对照需求和任务图逐项判断。
5. 检查变更是否越过保护边界。
6. 只陈述证据能支持的结论。

不能用这些话代替证据：

- “应该可以”
- “看起来没问题”
- “理论上”
- “我已经改了所以完成”
- “测试之前通过过”

## Completion Gate

完成闸门归入本阶段。只有同时满足这些条件，才能输出 `COMPLETE`：

- 所有 critical tasks 已完成，或已被用户明确移出范围。
- 新鲜验证证据通过。
- expected vs actual 对齐。
- 没有 unresolved blocker。
- 阶段自审或 Review Matrix 没有未解决的 `NEEDS_CLARIFICATION` 或 `NEEDS_CHANGE`。
- 副作用检查没有未披露风险。
- 变更没有越过保护边界，或越界点已被用户明确接受。
- residual risks 已列出并说明是否接受。

如果验证失败或证据不足：

- 若缺口可在当前 Execution Contract 内修复，结论写 `PARTIAL`，`Recommended Next Stage` 指向具体恢复动作：轻量开发、`ccdawn-bdd-tdd-development`、`ccdawn-bug-review` 或补验证。
- 若缺口需要新范围、权限、迁移、删除、发布或需求变更，结论写 `BLOCKED`，只问一个阻塞问题。
- 不把“已发现问题”当作完成；不让用户自己猜下一步该回哪里修。

## 输出契约

默认输出：

```text
完成总结:
- 结论: COMPLETE / PARTIAL / BLOCKED
- Context Boundary: 本次总结覆盖的需求、任务、diff、验证命令和保护边界...
- 需求覆盖:
  - 已满足: ...
  - 未满足: ...
  - 明确不做: ...
- 验证证据:
  - 命令/检查: ...
  - 结果: ...
- 主要变更: ...
- 副作用和风险: ...
- 保护边界: PASS/ACCEPT_RISK/NEEDS_CHANGE ...
- Success Evidence: 支撑结论的最新命令、检查、截图、日志或结构性证据...
- Stop Condition: 关键任务未完成 / 新鲜证据缺失 / NEEDS_CHANGE 未解决 / 需要用户决策...
- 恢复动作: 无 / 回到具体阶段...
- 交付状态: 可提交/需补测/需返工/等待用户决策

Ledger Update:
- Current Stage: SUMMARIZING / COMPLETED / BLOCKED
- Completed Tasks: ...
- Verification Evidence: ...
- Unresolved Risks: ...
- Recommended Next Stage: ccdawn-pr-review / 提交或 PR 准备 / 对应开发模式补任务 / ccdawn-bug-review / ccdawn-planning / ccdawn-brt / BLOCKED
- Route Out: ccdawn-pr-review / 提交或 PR 准备 / 对应开发模式 / ccdawn-bug-review / ccdawn-planning / ccdawn-brt / BLOCKED

下一步:
默认路由：<收口 / ccdawn-pr-review / 提交或 PR 准备 / 对应开发模式补任务 / ccdawn-bug-review / ccdawn-planning / ccdawn-brt / BLOCKED>，原因...
执行规则：COMPLETE 且没有提交、推送、PR、合并、发布或补任务需求时直接收口；PARTIAL 时路由到最具体恢复阶段；BLOCKED 时只问一个阻塞问题；远程写入、发布、合并、删除或迁移动作前必须停下等用户授权。
```

## 结论规则

- `COMPLETE`：所有关键任务完成，验证通过，没有未解决阻塞，满足已确认意图。
- `PARTIAL`：有可用进展，但仍缺关键任务、验证或用户决策。
- `BLOCKED`：当前无法继续，必须说明阻塞原因、影响步骤、可选修复和一个最关键问题。

## Workflow Ledger

总结时必须读取并更新账本：

- 用 `Task Graph` 判断是否所有 critical tasks 完成。
- 用 `Verification Evidence` 支撑结论，不够就输出 `PARTIAL` 或 `BLOCKED`。
- `Unresolved Risks` 不能为空泛，必须说明影响和建议下一步。
- `Recommended Next Stage` 必须是用户可选择的动作。
- 完整字段和压缩规则以 `ccdawn-brt/references/runtime.md` 为准；本阶段默认只输出 `Ledger Update`。

## 汇报风格

- 中文优先；
- 少解释流程，多给结论和证据；
- 不重复用户已经知道的背景；
- 不把日志整段贴给用户，只提取能证明结论的关键行；
- 如果验证失败，直接说失败，不粉饰。

## 阶段交接

总结后按自然闸门给下一步：如果工作已经完成且没有提交、推送、PR、合并、发布或补任务需求，可以直接收口；如果存在后续动作，给默认路由和原因。只有存在真实分叉、高风险动作或需要用户授权时，才给用户选项。

如果用户选择继续开发，按任务的 Development Mode 执行；`BDD_TDD` 子任务使用 `ccdawn-bdd-tdd-development`。如果用户发现需求方向不对，回到 `ccdawn-brt`。如果用户要进入 PR、提交、推送、合并或发布前审阅，使用 `ccdawn-pr-review`。
