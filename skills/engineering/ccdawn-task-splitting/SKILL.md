---
name: ccdawn-task-splitting
description: Use after a CCDawn implementation plan is accepted and the user confirms entering task splitting, before development starts; applies when work must be decomposed into ordered, reviewable, independently verifiable tasks with dependencies, development mode decisions, verification anchors, and handoff decisions.
---

# CCDawn Task Splitting

## 目标

把已确认方案拆成可执行任务图。此阶段只拆任务，不写代码。

好的任务拆分应该让后续 agent 清楚知道：

- 先做哪一项，为什么；
- 每个任务的输入、输出和依赖；
- 每个任务适合轻量实现还是需要 BDD/TDD；
- 哪些任务是关键路径，哪些是可选优化；
- 完成一个任务后怎样判断可以进入下一个任务。

## 进入条件

使用前确认已有：

- 已接受的 `ccdawn-planning` 方案；
- 用户确认进入任务拆分；
- 方案中的目标、范围、文件影响、风险和验证策略；
- 必要的代码或文档上下文。

如果方案本身还没被用户接受，不要拆任务，先回到 `ccdawn-planning`。

## 拆分原则

- 一个任务只交付一个可审阅结果。
- 每个任务必须能独立验证。
- 任务之间依赖要显式写出，不能让后续 agent 猜。
- 测试、脚手架、配置和文档不要单独漂浮；并入产出依赖它们的任务。
- 不把多个无关模块塞进同一个任务。
- 不把一次微小改动拆成无意义的小碎片。
- 简单任务标记为 `SIMPLE`，只要求明确产出和必要验证。
- 只有模型判断无法一次稳定完成、容易偏离、跨模块或高风险的任务，才标记为 `BDD_TDD`。

## Task Graph

Task Graph 规则归入本阶段。每个任务必须说明：

- input：本任务需要的需求、文件、数据、前置产物；
- output：本任务完成后可观察或可复用的产物；
- dependency：依赖的任务、确认、工具或环境状态；
- verification condition：证明任务完成且对齐的证据。

任务图还要标出：

- critical path：完成目标必须执行的任务；
- optional path：有价值但非必需的优化；
- high risk task：数据丢失、安全、回归、API 破坏或难回滚风险；
- ambiguous task：仍依赖假设或实现分叉的任务。

没有 verification condition 的 critical task 不允许进入开发。

## 任务卡格式

每个任务必须包含：

```text
Task N: 名称
- Goal: 本任务要达成的可观察结果
- Inputs: 来自需求、方案或前置任务的输入
- Outputs: 后续任务依赖的产物
- Files: 预计创建/修改/测试的路径
- Dependencies: 无 / Task X
- Criticality: critical / optional
- Development Mode: SIMPLE / BDD_TDD
- BDD/TDD Anchor: SIMPLE 写“无需，原因...”；BDD_TDD 写 Given / When / Then 和先失败测试
- Verification: 要运行的命令或结构性检查
- Review Gate: 任务完成后审什么
- Risk: 本任务最可能出偏差的点
```

简单任务可用压缩卡片：

```text
Task N: 名称
- Output:
- Files:
- Development Mode: SIMPLE
- Verification:
- Risk:
```

## 输出契约

默认输出：

```text
任务拆分:
- Critical Path: Task 1 -> Task 2 -> ...
- Optional Path: ...
- 并行性: 哪些不能并行，哪些可以独立处理

Task 1: ...
Task 2: ...
Task 3: ...

Ledger Update:
- Current Stage: TASK_SPLITTING
- Task Graph: Critical Path..., Optional Path...
- Current Task: 推荐 Task 1
- Verification Evidence: 拆分自审...
- Decisions: ...
- Unresolved Risks: ...
- Recommended Next Stage: 轻量执行 Task 1 / ccdawn-bdd-tdd-development（仅 BDD_TDD 任务）/ 授权后连续 Critical Path

拆分自审:
- 覆盖方案: PASS/NEEDS_CHANGE，证据...
- 依赖清晰: PASS/NEEDS_CHANGE，证据...
- 粒度合适: PASS/NEEDS_CHANGE，证据...
- 验证可行: PASS/NEEDS_CHANGE，证据...

下一步:
任务拆分已完成。建议先执行 Task 1；如果用户希望 agent 连续推进，也可以授权按 Critical Path 一次性执行到完成总结。
A. 轻量执行 Task 1（SIMPLE 任务推荐）...
B. 使用 ccdawn-bdd-tdd-development 执行 Task 1（仅 BDD_TDD 任务推荐）...
C. 连续执行全部 Critical Path（需要明确授权；逐任务按 SIMPLE 或 BDD_TDD 执行，遇阻立刻停）...
D. 调整任务拆分...
E. 先指定另一个任务...
F. 暂停...
```

## 质量门槛

- `BDD_TDD` 任务没有 BDD/TDD Anchor 不合格。
- `SIMPLE` 任务不要补形式化 BDD/TDD；只要说明为什么轻量验证足够。
- 任务不能只写“实现功能”“添加测试”“更新文档”。
- 不能在拆分阶段改代码。
- 如果拆分发现方案不可执行，回到 `ccdawn-planning`，不要硬拆。

## Workflow Ledger

任务拆分完成时必须更新账本增量：

- `Accepted Plan` 必须来自 `ccdawn-planning`。
- `Task Graph` 必须包含 critical path、optional path 和任务依赖。
- `Current Task` 默认推荐第一个未完成 critical task，除非用户指定其他任务。
- `Recommended Next Stage` 默认是第一个未完成 critical task，并标明 `SIMPLE` 或 `BDD_TDD`；同时提供“连续执行全部 Critical Path”的明确授权选项。
- 完整字段和压缩规则以 `ccdawn-brt/references/runtime.md` 为准；本阶段默认只输出 `Ledger Update`。

## 阶段交接

每次完成任务拆分后必须停下并询问是否进入下一阶段。

如果用户确认进入开发，按任务的 `Development Mode` 执行：`SIMPLE` 任务轻量实现和验证；`BDD_TDD` 任务使用 `ccdawn-bdd-tdd-development`。不要默认连续执行全部任务，除非用户明确选择“连续执行全部 Critical Path”。

如果用户选择连续执行全部 Critical Path：

- 把该选择写入 `Decisions`：`Continuous Critical Path authorized`。
- 后续执行细节、开发模式和停止条件以 `ccdawn-brt/references/runtime.md` 为准。
- 全部 critical tasks 完成后，默认路由到 `ccdawn-completion-summary`，不要停在中间等待用户重复确认。
