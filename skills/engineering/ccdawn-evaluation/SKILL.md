---
name: ccdawn-evaluation
description: Use when CCDawn workflow needs a Chinese-first evaluation adapter and no more specific existing skill already owns the review, debugging, PR, planning, feedback, verification, or goal task.
---

# CCDawn Evaluation

## 目标

这是 CCDawn 的通用评价适配器，只处理“没有更具体 skill 承接”的评价问题。

先复用现有 skill：

- PR、diff、分支、提交范围：`ccdawn-pr-review`。
- 复杂功能新增前的项目/库/模块搜索、技术选型、复用价值评估：`ccdawn-feature-reuse-research`。
- 项目、代码库、架构、技术债、测试缺口、风险模块、接手摸底：`ccdawn-project-review`。
- 独立代码审阅：`requesting-code-review`。
- 外部 review 反馈是否采纳：`receiving-code-review`。
- bug、失败测试、异常行为：`systematic-debugging`，必要时叠加 `root-cause-tracing`。
- 完成状态和证据：`ccdawn-completion-summary` 或 `verification-before-completion`。
- 需求/真实目标/执行深度/流程重量：由 `ccdawn-brt` 判定；如果这些不清楚，先回 BRT。
- 方案制定前后的可实施性：`ccdawn-planning`。
- 目标是否可执行：`ccdawn-goal-loop`。

只有当用户要评价的是方案、流程、skill、当前状态、输出质量、合理性、灵活性、噪声、取舍或下一步价值，且用户目标已经清楚、没有更具体 skill 时，才在本 skill 内做轻量多维评价。项目级审查默认交给 `ccdawn-project-review`，复用价值评估默认交给 `ccdawn-feature-reuse-research`，不要在本 skill 里重写这些专项流程。

Owner 边界：

- `ccdawn-brt` 负责判断用户到底想评价什么、要不要评价、评价深度是否过重。
- `ccdawn-evaluation` 负责在评价对象和目标已知后给出证据化判断。
- 进入本 skill 后，只在评价目标或对象不明时回到 BRT；不要因为“流程重量”这类主题本身就回 BRT。

## BRT interface

- Context Boundary: 被评价对象、用户评价标准、证据来源、已排除的更具体 owner、允许读取范围。
- Output Contract: 总评、多维评价、必须调整、可选优化、行动队列和 Route Out。
- Allowed Action: 默认只读评价；只有用户目标明确要求“调整/优化”，且改动低风险、范围清楚、可验证时，才路由到 `FAST_PATH` 或下游开发阶段。
- Success Evidence: 结论绑定评价对象、证据和可执行下一步；没有空泛“更好/更完整”。
- Stop Condition: 评价对象不明、存在更具体 owner、缺关键证据、用户目标变成实施、或评价结论会改变高风险路线且未校准。
- Route Out: 更具体 skill、`ccdawn-brt`、`ccdawn-planning`、`ccdawn-task-splitting`、`FAST_PATH` 调整、`ccdawn-completion-summary` 或 BLOCKED。

## 进入条件

使用前确认评价对象和评价目的已知；未知时回到 `ccdawn-brt` 做需求对齐。若更具体 skill 已经能承接，不在本 skill 内重写对方流程。

## 评价方式

1. 先写一句 `复用检查`：是否已有更具体 skill；有则路由，不继续评价。
2. 确认评价目标和对象已知；未知时只问 1 个问题或回 BRT。
3. 没有更具体 skill 时，选 2-4 个真正会改变行动的维度。
4. Evidence 必须来自文件、代码、测试、日志、用户要求、运行结果或明确假设。
5. 给出总评、必须调整、可选优化和下一步路由。

如果评价对象是审查报告、流程结果或多发现输出，必须先把后续动作归入 `Immediate Guardrail / Primary Fix / Telemetry Gap / Deferred Refactor`，再推荐下一步。若存在多个可修复项，转成 Ordered Fix Queue，并标记 `SAFE_DIRECT / PLAN_THEN_EXECUTE / DEFERRED / BLOCKED`。不要把确认型问题、证据缺口、治理风险和维护性重构混成同一类建议。

## 默认维度

按对象选择，不要全量输出：

- 需求对齐：是否满足用户真实目标。
- 流程重量：步骤、问题、worktree、ledger 是否带来实际价值。
- 灵活性：是否能根据风险和证据自动变通。
- 证据质量：结论是否有本地事实或验证支撑。
- 完成率：是否把明确请求推进到可验证结果，而不是停在计划、分析或半成品总结。
- 误改风险：是否识别 owning surface、保护边界、无关改动和验证失败恢复路径。
- 风险：是否涉及数据、安全、权限、迁移、发布或回滚。
- 可维护性：是否便于后续 agent 接续。
- 用户价值：是否减少用户无效选择和认知负担。

## 输出契约

```text
评估:
- 复用检查: 已有更具体 skill / 无更具体 skill
- 总评: GOOD / ACCEPTABLE_WITH_RISK / NEEDS_CHANGE / BLOCKED
- Context Boundary: 被评价对象、用户标准、证据来源、已排除的专项 owner...
- Allowed Action: 只读评价 / FAST_PATH 调整 / 路由到下游阶段 / BLOCKED
- 推荐判断: ...
- 关键证据: ...

多维评价:
- 维度: PASS / WEAK / FAIL / ACCEPT_RISK；证据...；影响...

必须调整:
- ...
- Success Evidence: 结论绑定评价对象、证据和可执行下一步；无空泛“更好/更完整”
- Stop Condition: 评价对象不明 / 存在更具体 owner / 缺关键证据 / 用户目标变成实施

行动队列（仅多后续动作时）:
- Immediate Guardrail: ...
- Primary Fix: ...
- Telemetry Gap: ...
- Deferred Refactor: ...

修复队列（仅多个可修复项时）:
- 1. ... [SAFE_DIRECT / PLAN_THEN_EXECUTE / DEFERRED / BLOCKED]；原因...；Success Evidence...

下一步:
默认路由：<更具体 skill / FAST_PATH 调整 / ccdawn-planning / ccdawn-task-splitting / ccdawn-completion-summary / ccdawn-brt / BLOCKED>，原因...
执行规则：用户已要求“优化/调整/继续”且改动低风险、范围清楚、可验证时，直接进入默认路由；只有评价对象不明、存在高风险取舍、或用户要求选择时，才列出选项。

Route Out: 更具体 skill / FAST_PATH 调整 / ccdawn-planning / ccdawn-task-splitting / ccdawn-completion-summary / ccdawn-brt / BLOCKED
```

## 质量门槛

- 有更具体 skill 时，必须路由，不在本 skill 里重写对方流程。
- 不给空泛建议；每条建议必须说明影响和触发条件。
- 不把“更完整/更严谨/更简洁”当结论，必须落到行为、成本、风险或证据。
- 不为了展示全面而输出低相关维度。
