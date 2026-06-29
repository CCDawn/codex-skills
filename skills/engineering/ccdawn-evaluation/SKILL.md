---
name: ccdawn-evaluation
description: Use when CCDawn workflow needs a Chinese-first evaluation adapter and no more specific existing skill already owns the review, debugging, PR, planning, feedback, verification, or goal task.
---

# CCDawn Evaluation

## 目标

这是 CCDawn 的通用评价适配器，只处理“没有更具体 skill 承接”的评价问题。

先复用现有 skill：

- PR、diff、分支、提交范围：`ccdawn-pr-review`。
- 独立代码审阅：`requesting-code-review`。
- 外部 review 反馈是否采纳：`receiving-code-review`。
- bug、失败测试、异常行为：`systematic-debugging`，必要时叠加 `root-cause-tracing`。
- 完成状态和证据：`ccdawn-completion-summary` 或 `verification-before-completion`。
- 需求/真实目标/执行深度/流程重量：由 `ccdawn-brt` 判定；如果这些不清楚，先回 BRT。
- 方案制定前后的可实施性：`ccdawn-planning`。
- 目标是否可执行：`ccdawn-goal-loop`。

只有当用户要评价的是方案、流程、skill、当前状态、输出质量、合理性、灵活性、噪声、取舍或下一步价值，且用户目标已经清楚、没有更具体 skill 时，才在本 skill 内做轻量多维评价。

Owner 边界：

- `ccdawn-brt` 负责判断用户到底想评价什么、要不要评价、评价深度是否过重。
- `ccdawn-evaluation` 负责在评价对象和目标已知后给出证据化判断。
- 进入本 skill 后，只在评价目标或对象不明时回到 BRT；不要因为“流程重量”这类主题本身就回 BRT。

## 评价方式

1. 先写一句 `复用检查`：是否已有更具体 skill；有则路由，不继续评价。
2. 确认评价目标和对象已知；未知时只问 1 个问题或回 BRT。
3. 没有更具体 skill 时，选 2-4 个真正会改变行动的维度。
4. Evidence 必须来自文件、代码、测试、日志、用户要求、运行结果或明确假设。
5. 给出总评、必须调整、可选优化和下一步路由。

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
- 推荐判断: ...
- 关键证据: ...

多维评价:
- 维度: PASS / WEAK / FAIL / ACCEPT_RISK；证据...；影响...

必须调整:
- ...

下一步:
A. 按推荐调整（推荐）...
B. 路由到更具体 skill...
C. 回到 ccdawn-brt / ccdawn-planning / ccdawn-task-splitting...
D. 暂停...
```

## 质量门槛

- 有更具体 skill 时，必须路由，不在本 skill 里重写对方流程。
- 不给空泛建议；每条建议必须说明影响和触发条件。
- 不把“更完整/更严谨/更简洁”当结论，必须落到行为、成本、风险或证据。
- 不为了展示全面而输出低相关维度。
