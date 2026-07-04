---
name: ccdawn-planning
description: Use when aligned requirements need an implementation plan before coding; applies when ccdawn-brt or a prior stage routes to planning, or when work needs architecture choices, scope boundaries, file impact, risk decisions, validation strategy, or an implementation handoff plan.
---

# CCDawn Planning

## 目标

把已经对齐的需求转成可实施方案。此阶段只制定方案，不拆成执行任务，不写代码。

方案必须回答：

- 要达成什么行为结果；
- 本轮做什么、不做什么；
- 采用哪条实现路径，为什么；
- 会影响哪些文件、模块、状态或接口；
- 哪些相邻文件、行为、测试、配置或清理不属于本轮；
- 如何验证成功；
- 哪些风险需要在执行前知道。

## BRT interface

- Context Boundary: 已确认意图、需求账本、相关代码/文档/测试/配置/日志、复用决策、明确排除范围和保护边界。
- Output Contract: 实施方案，包括目标、范围、推荐路径、备选取舍、影响面、保护边界、验证策略、风险决策和 Route Out。
- Allowed Action: 只读分析和制定方案；不写业务代码、不改测试、不安装依赖、不执行迁移/删除/发布；复杂新增功能缺复用依据时先路由到 `ccdawn-feature-reuse-research`。
- Success Evidence: 下游可以据此判定拆分/不拆分；方案能点名用户可观察结果、owned surface、非目标、影响文件/模块、验证方式和剩余风险。
- Stop Condition: 需求不稳、复用研究缺失、影响面无法枚举、保护边界不清、高风险动作未确认、或用户目标变成直接写代码。
- Route Out: `ccdawn-task-splitting`、`FAST_PATH` 直接执行、`ccdawn-feature-reuse-research`、`ccdawn-brt` 或 BLOCKED。

## 进入条件

使用前确认已有：

- 来自 `ccdawn-brt` 的已确认意图或行为契约；
- BRT、上一阶段或用户已允许进入方案阶段；用户原始目标已包含执行许可时，可按自然闸门连续进入；
- 已知范围边界、关键约束、验证锚点；
- 必要的本地上下文：代码、文档、测试、配置、日志或历史决策。
- 若目标是复杂新增功能且外部/内部复用可能改变方案，已有 `ccdawn-feature-reuse-research` 的复用决策，或已明确跳过复用研究并记录原因。

如果缺少会改变方案的需求信息，先回到 `ccdawn-brt` 继续需求对齐，不要硬写方案。
如果缺少会改变方案的复用研究，先进入 `ccdawn-feature-reuse-research`，不要默认自研。

## 工作方式

1. 读取上下文：检查相关文件、测试、文档、配置和已有模式。
2. 检查复用决策：复杂新增功能必须说明 `REUSE / ADAPT / REFERENCE_ONLY / BUILD_IN_HOUSE / skipped`。
3. 识别方案分叉：只有当选择会影响风险、成本、行为或可维护性时，才给 2-3 个方案选项。
4. 推荐路径：给出推荐方案，并说明为什么优于其他路径。
5. 写方案：用具体文件、接口、数据流、状态流和验证方式描述实现路径。
6. 自审：从范围、可实施性、风险、验证四个角度检查方案。
7. 更新 Workflow Ledger，并按 BRT 自然闸门规则路由到 `ccdawn-task-splitting` 做“拆分/不拆分”判定，或在明确低风险时直接执行。

## 输出契约

默认输出：

```text
实施方案:
- 目标: ...
- 范围: 本轮做...；不做...
- Context Boundary: 本阶段读取/依赖的代码、文档、测试、日志或外部研究边界...
- 推荐路径: ...
- 备选路径: A ... / B ...
- 复用决策: REUSE / ADAPT / REFERENCE_ONLY / BUILD_IN_HOUSE / skipped；证据...
- 影响面:
  - 文件/模块: ...
  - 接口/状态/数据: ...
- 保护边界: 不碰哪些相邻区域、用户改动或清理项
- 风险决策: ...
- 验证策略: ...
- Success Evidence: 方案完成后下游可用什么证明目标、范围和验证路径已经明确...
- Stop Condition: 需求不稳 / 复用研究缺失 / 影响面无法枚举 / 高风险动作未确认...
- 需要保留的假设: ...

Ledger Update:
- Current Stage: PLANNING
- Accepted Plan: ...
- Verification Evidence: ...
- Decisions: ...
- Assumptions: ...
- Unresolved Risks: ...
- Recommended Next Stage: ccdawn-task-splitting（判定拆分/不拆分） / FAST_PATH 直接执行 / ccdawn-feature-reuse-research / ccdawn-brt / BLOCKED
- Route Out: ccdawn-task-splitting / FAST_PATH 直接执行 / ccdawn-feature-reuse-research / ccdawn-brt / BLOCKED

方案自审:
- 范围: PASS/NEEDS_CHANGE，证据...
- 可实施性: PASS/NEEDS_CHANGE，证据...
- 风险: PASS/ACCEPT_RISK/NEEDS_CLARIFICATION，证据...
- 验证: PASS/NEEDS_CHANGE，证据...

下一步:
默认路由：<ccdawn-task-splitting / FAST_PATH 直接执行 / ccdawn-feature-reuse-research / ccdawn-brt / BLOCKED>，原因...
执行规则：用户原始目标已包含执行许可且无自然闸门时，直接进入默认路由；只有方案有真实分叉、高风险动作、需求变化或用户要求选择时，才列出可选下一步。
```

## 质量门槛

- 不写占位词：`TBD`、`TODO`、`后续补充`、`适当处理` 都不合格。
- 不只写方向：每个关键点都要落到文件、模块、接口、状态、测试或可观察行为。
- 不过早拆任务：是否拆分和子任务模式留给 `ccdawn-task-splitting`；本阶段只提供可执行方案。
- 不实现：本阶段不编辑业务代码，除非用户明确改变阶段目标。
- 不扩大范围：不能把用户没确认的增强项塞进推荐路径。
- 不写“相关文件都可能调整”这类无限边界；无法枚举影响面时，必须说明需要先 probe 或进入任务拆分降低误改风险。
- 复杂新增功能不能默认自研；必须引用复用研究结论，或说明为什么本次跳过 `ccdawn-feature-reuse-research`。

## Workflow Ledger

方案完成时必须给后续阶段留下可续接账本：

- `Confirmed Intent` 来自 `ccdawn-brt`，不能重新发明。
- `Accepted Plan` 写成一句可执行方案摘要。
- `Reuse Decision` 若存在，必须写入 `Decisions` 或 `Assumptions`，供拆分和开发阶段继承。
- `Task Graph` 在本阶段标为未判定，留给 `ccdawn-task-splitting` 决定拆分或不拆分。
- `Decisions` 只记录会影响实现、测试、风险或范围的决定。
- `Unresolved Risks` 必须包含仍不清楚的影响面或保护边界。
- `Recommended Next Stage` 默认是 `ccdawn-task-splitting` 做拆分判定；只有明确低风险直接执行时才写直接执行。
- 完整字段和压缩规则以 `ccdawn-brt/references/runtime.md` 为准；本阶段默认只输出 `Ledger Update`。

## 高风险方案审查

当方案涉及权限、安全、数据删除、迁移、发布、回滚、公共 API 或多模块重构时，可以读取 `plan-document-reviewer-prompt.md`，用它组织一次计划审查。审查只阻塞真实缺口，不阻塞措辞偏好。

## 阶段交接

完成方案后遵守 `ccdawn-brt/references/runtime.md` 的自然闸门规则：用户目标已包含执行许可时，按推荐路由继续；只有阻塞、高风险动作、验证失败、范围变化、目标变化、发布/合并/迁移/删除/权限动作前，才停下等用户选择。

如果需要下一阶段，默认进入 `ccdawn-task-splitting` 判定拆分/不拆分。只有用户给出明确执行许可，且方案是单步、低风险、可验证、可回滚时，才跳过任务拆分。若用户要求继续对齐需求，回到 `ccdawn-brt`。

如果用户要求直接实现，必须先套用 BRT 直接路径条件：用户给出明确执行动词或选择直接实现、影响范围可枚举、无迁移/删除/权限/发布风险、可快速验证、失败可回滚。不满足时进入 `ccdawn-task-splitting`，由拆分阶段决定不拆、拆成简单子任务，或拆出需要 BDD/TDD 的复杂子任务。
