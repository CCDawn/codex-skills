---
name: ccdawn-task-splitting
description: Use after a CCDawn implementation plan is accepted and the user confirms entering task splitting or split/no-split routing, before development starts; applies when work may need decomposition, when it may be valid to choose NO_SPLIT, or when subtasks need SIMPLE vs BDD_TDD development mode decisions, verification anchors, dependencies, and handoff decisions.
---

# CCDawn Task Splitting

## 目标

把已确认方案拆成可执行任务图，或明确判定无需拆分。此阶段只做拆分决策，不写代码。

好的任务拆分应该让后续 agent 清楚知道：

- 这个方案是否真的需要拆分；
- 先做哪一项，为什么；
- 每个任务的输入、输出和依赖；
- 每个任务拥有哪个修改面，以及哪些相邻区域不能误碰；
- 每个任务适合轻量实现还是需要 BDD/TDD；
- 哪些任务是关键路径，哪些是可选优化；
- 完成一个任务后怎样判断可以进入下一个任务。

## 进入条件

使用前确认已有：

- 已接受的 `ccdawn-planning` 方案；
- 用户确认进入任务拆分，或 planning 阶段建议进入本阶段做拆分/不拆分判定；
- 方案中的目标、范围、文件影响、风险和验证策略；
- 复杂新增功能的复用决策：REUSE / ADAPT / REFERENCE_ONLY / BUILD_IN_HOUSE / skipped；
- 必要的代码或文档上下文。

如果方案本身还没被用户接受，不要拆任务，先回到 `ccdawn-planning`。

## 拆分原则

- 一个任务只交付一个可审阅结果。
- 每个任务必须能独立验证。
- 任务之间依赖要显式写出，不能让后续 agent 猜。
- 测试、脚手架、配置和文档不要单独漂浮；并入产出依赖它们的任务。
- 不把多个无关模块塞进同一个任务。
- 不把一次微小改动拆成无意义的小碎片。
- 如果决定拆分，每个子任务必须标记 `SIMPLE` 或 `BDD_TDD`。
- `SIMPLE` 子任务只要求明确产出和必要验证。
- 只有 agent 判断子任务无法一次稳定完成、容易偏离、跨模块或高风险时，才标记为 `BDD_TDD`。
- 如果方案本身就是一个可一次执行的单元，输出 `NO_SPLIT`，不要硬拆成任务。

## 拆分判定

选择 `NO_SPLIT`，当方案同时满足：

- 一个实现单元即可完成；
- 文件范围和验证方式清楚；
- 不需要先后依赖或分阶段交付；
- 不涉及迁移、删除、权限、安全、持久化、公共 API 或发布风险；
- 失败可快速回滚；
- 不需要 BDD/TDD 才能稳定实现。

选择 `SPLIT`，当任一条件成立：

- 需要多个先后依赖的产物；
- 跨模块或跨页面，容易在一次实现中混乱；
- 有高风险步骤需要单独验收；
- 至少有一个子任务可能需要 BDD/TDD 才能稳定实现；
- 需要并行 agent 或分 PR；
- 用户明确要求拆分。

## 子任务模式判定

只在 `SPLIT` 后对子任务判定模式。

标记 `SIMPLE`，当子任务：

- 范围局部，输出明确；
- 不涉及状态迁移、权限、安全、持久化、公共 API 或发布风险；
- 不需要新行为契约才能理解；
- 直接验证或结构检查足够。

标记 `BDD_TDD`，当子任务任一条件成立：

- 行为、失败路径、状态流转或数据契约不清；
- 跨模块协作，容易一次实现偏离；
- 之前类似问题回归过；
- 需要新增行为测试才可信；
- 涉及权限、安全、迁移、持久化、公共 API、发布或回滚；
- 用户要求谨慎 BDD/TDD。

## Task Graph

Task Graph 规则归入本阶段。每个任务必须说明：

- input：本任务需要的需求、文件、数据、前置产物；
- output：本任务完成后可观察或可复用的产物；
- dependency：依赖的任务、确认、工具或环境状态；
- verification condition：证明任务完成且对齐的证据。
- owned surface / protected boundary：本任务负责的文件、模块、行为，以及不应顺手修改的相邻区域。

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
- Boundary: 本任务拥有的修改面；明确不碰的相邻文件、行为或清理项
- Reuse: 本任务继承的复用决策、候选模块/库、禁止误用边界；无则写“无”
- Dependencies: 无 / Task X
- Criticality: critical / optional
- Development Mode: SIMPLE / BDD_TDD
- BDD/TDD Anchor: SIMPLE 写“无需，原因...”；BDD_TDD 写 Given / When / Then 和先失败测试
- Verification: 要运行的命令或结构性检查
- Review Gate: 任务完成后审什么
- Risk: 本任务最可能出偏差的点
```

`SIMPLE` 子任务可用压缩卡片：

```text
Task N: 名称
- Output:
- Files/Boundary:
- Reuse:
- Development Mode: SIMPLE
- Verification:
- Risk:
```

## 输出契约

`NO_SPLIT` 输出：

```text
任务拆分判定:
- Decision: NO_SPLIT
- 理由: ...
- 直接执行单元:
  - Output:
  - Files:
  - Verification:
  - Risk:

Ledger Update:
- Current Stage: TASK_SPLITTING
- Task Graph: 不需要
- Current Task: 直接执行单元
- Decisions: NO_SPLIT
- Unresolved Risks: ...
- Recommended Next Stage: 轻量执行 / ccdawn-completion-summary

下一步:
A. 不拆分，直接执行（推荐）...
B. 强制拆分任务...
C. 回到 ccdawn-planning 调整方案...
D. 暂停...
```

`SPLIT` 输出：

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
- 有误改风险的任务缺少 Boundary 不合格。
- 复杂新增功能缺少 Reuse 字段不合格；如果选择自研，必须说明已研究或已跳过复用研究的原因。
- 不能在拆分阶段改代码。
- 如果拆分发现方案不可执行，回到 `ccdawn-planning`，不要硬拆。

## Workflow Ledger

任务拆分完成时必须更新账本增量：

- `Accepted Plan` 必须来自 `ccdawn-planning`。
- `Split Decision` 必须是 `NO_SPLIT` 或 `SPLIT`。
- `NO_SPLIT` 时，`Task Graph` 写“不需要”，`Current Task` 写“直接执行单元”，`Recommended Next Stage` 写轻量执行或完成总结。
- `SPLIT` 时，`Task Graph` 必须包含 critical path、optional path 和任务依赖。
- `SPLIT` 时，`Current Task` 默认推荐第一个未完成 critical task，除非用户指定其他任务。
- `SPLIT` 时，`Recommended Next Stage` 默认是第一个未完成 critical task，并标明 `SIMPLE` 或 `BDD_TDD`；同时提供“连续执行全部 Critical Path”的明确授权选项。
- 完整字段和压缩规则以 `ccdawn-brt/references/runtime.md` 为准；本阶段默认只输出 `Ledger Update`。

## 阶段交接

完成拆分判定后遵守 `ccdawn-brt/references/runtime.md` 的自然闸门规则：用户目标已包含执行许可时，按推荐任务继续；只有阻塞、高风险动作、验证失败、范围变化、目标变化、发布/合并/迁移/删除/权限动作前，才停下等用户选择。

进入开发时，按任务的 `Development Mode` 执行：`SIMPLE` 任务轻量实现和验证；`BDD_TDD` 任务使用 `ccdawn-bdd-tdd-development`。只有用户明确选择“连续执行全部 Critical Path”或原始目标已经是完成整个 critical path 时，才连续执行全部任务；否则执行推荐的下一个任务。

如果用户选择连续执行全部 Critical Path：

- 把该选择写入 `Decisions`：`Continuous Critical Path authorized`。
- 后续执行细节、开发模式和停止条件以 `ccdawn-brt/references/runtime.md` 为准。
- 全部 critical tasks 完成后，默认路由到 `ccdawn-completion-summary`，不要停在中间等待用户重复确认。
