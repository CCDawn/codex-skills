---
name: ccdawn-planning
description: Use when requirements or intent have been aligned by ccdawn-brt and the user confirms entering planning, before implementation starts; applies when work needs architecture choices, scope boundaries, file impact, risk decisions, validation strategy, or an implementation handoff plan.
---

# CCDawn Planning

## 目标

把已经对齐的需求转成可实施方案。此阶段只制定方案，不拆成执行任务，不写代码。

方案必须回答：

- 要达成什么行为结果；
- 本轮做什么、不做什么；
- 采用哪条实现路径，为什么；
- 会影响哪些文件、模块、状态或接口；
- 如何验证成功；
- 哪些风险需要在执行前知道。

## 进入条件

使用前确认已有：

- 来自 `ccdawn-brt` 的已确认意图或行为契约；
- 用户允许进入方案阶段；
- 已知范围边界、关键约束、验证锚点；
- 必要的本地上下文：代码、文档、测试、配置、日志或历史决策。

如果缺少会改变方案的需求信息，先回到 `ccdawn-brt` 继续需求对齐，不要硬写方案。

## 工作方式

1. 读取上下文：检查相关文件、测试、文档、配置和已有模式。
2. 识别方案分叉：只有当选择会影响风险、成本、行为或可维护性时，才给 2-3 个方案选项。
3. 推荐路径：给出推荐方案，并说明为什么优于其他路径。
4. 写方案：用具体文件、接口、数据流、状态流和验证方式描述实现路径。
5. 自审：从范围、可实施性、风险、验证四个角度检查方案。
6. 更新 Workflow Ledger，询问用户是否进入 `ccdawn-task-splitting`。

## 输出契约

默认输出：

```text
实施方案:
- 目标: ...
- 范围: 本轮做...；不做...
- 推荐路径: ...
- 备选路径: A ... / B ...
- 影响面:
  - 文件/模块: ...
  - 接口/状态/数据: ...
- 风险决策: ...
- 验证策略: ...
- 需要保留的假设: ...

Workflow Ledger:
- Confirmed Intent: ...
- Current Stage: PLANNING
- Accepted Plan: ...
- Task Graph: 未生成
- Current Task: 无
- Completed Tasks: 无
- Verification Evidence: ...
- Decisions: ...
- Assumptions: ...
- Unresolved Risks: ...
- Recommended Next Stage: ccdawn-task-splitting

方案自审:
- 范围: PASS/NEEDS_CHANGE，证据...
- 可实施性: PASS/NEEDS_CHANGE，证据...
- 风险: PASS/ACCEPT_RISK/NEEDS_CLARIFICATION，证据...
- 验证: PASS/NEEDS_CHANGE，证据...

下一步:
方案已完成。是否进入 ccdawn-task-splitting 拆分任务？
A. 进入任务拆分（推荐）...
B. 调整方案...
C. 暂停在方案阶段...
```

## 质量门槛

- 不写占位词：`TBD`、`TODO`、`后续补充`、`适当处理` 都不合格。
- 不只写方向：每个关键点都要落到文件、模块、接口、状态、测试或可观察行为。
- 不过早拆任务：任务粒度留给 `ccdawn-task-splitting`。
- 不实现：本阶段不编辑业务代码，除非用户明确改变阶段目标。
- 不扩大范围：不能把用户没确认的增强项塞进推荐路径。

## Workflow Ledger

方案完成时必须给后续阶段留下可续接账本：

- `Confirmed Intent` 来自 `ccdawn-brt`，不能重新发明。
- `Accepted Plan` 写成一句可执行方案摘要。
- `Task Graph` 在本阶段标为未生成，留给 `ccdawn-task-splitting`。
- `Decisions` 只记录会影响实现、测试、风险或范围的决定。
- `Recommended Next Stage` 默认是 `ccdawn-task-splitting`。

## 高风险方案审查

当方案涉及权限、安全、数据删除、迁移、发布、回滚、公共 API 或多模块重构时，可以读取 `plan-document-reviewer-prompt.md`，用它组织一次计划审查。审查只阻塞真实缺口，不阻塞措辞偏好。

## 阶段交接

每次完成方案后必须停下并询问是否进入下一阶段。

如果用户确认进入下一步，使用 `ccdawn-task-splitting`。如果用户要求继续对齐需求，回到 `ccdawn-brt`。如果用户要求直接实现，先提醒缺少任务拆分会增加执行偏差，再按用户最新指令执行。
