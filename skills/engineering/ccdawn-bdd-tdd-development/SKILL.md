---
name: ccdawn-bdd-tdd-development
description: Use when a CCDawn task has been selected and the user confirms entering development; applies before implementing behavior changes, features, bug fixes, refactors, or tests that need BDD behavior anchors, TDD red-green-refactor discipline, task-scoped execution, and evidence before moving on.
---

# CCDawn BDD/TDD Development

## 目标

按已选择的任务进行开发。此阶段一次只执行一个任务，先锁定行为，再用 TDD 实现。即使用户授权连续执行全部 Critical Path，也必须逐任务推进。

核心顺序：

1. BDD：把任务翻译成 Given / When / Then 行为契约。
2. RED：先写失败测试，并确认失败原因正确。
3. GREEN：写最小实现让测试通过。
4. REFACTOR：只在测试保持通过时清理代码。
5. VERIFY：用新鲜证据证明任务完成。

## 进入条件

使用前确认已有：

- 用户确认进入开发；
- 一个明确的 `ccdawn-task-splitting` 任务；
- 任务的 Goal、Files、BDD Anchor、TDD Anchor、Verification；
- 当前工作区状态已检查，不覆盖无关用户改动。

如果没有明确任务，不要开始开发，先回到 `ccdawn-task-splitting`。如果用户授权连续执行全部 Critical Path，必须同时有有序 Task Graph、每个 critical task 的 BDD/TDD/Verification，以及当前下一个任务。

## BDD 契约

实现前先输出或内部确认：

```text
Behavior Contract:
- Given: 初始条件、权限、数据、状态
- When: 用户动作、系统事件或调用
- Then: 可观察结果
- And: 失败路径、边界或副作用约束
```

如果 BDD 契约会改变用户预期，先问用户；如果只是把已确认任务转成测试语言，可以继续。

## TDD 铁律

```
没有先失败的测试，就不要写生产代码。
```

必须做到：

- 先写一个最小失败测试；
- 运行测试并确认失败原因是目标行为缺失，不是拼写、导入或环境错误；
- 只写让该测试通过的最小实现；
- 重新运行测试并确认通过；
- 再进入下一个行为或重构。

如果任务确实无法自动化测试，必须在写实现前说明：

- 为什么无法自动化；
- 用什么结构性检查、人工验收或可逆 probe 代替；
- 这个替代证据的风险。

写正式 BDD 场景或 `.feature` 文件时，读取 `references/gherkin.md`。写测试、mock 或测试工具时，如出现 mock 断言、test-only production API、过度 mock，读取 `testing-anti-patterns.md`。

## 执行边界

- 只执行当前任务；除非用户明确授权连续 Critical Path，否则不顺手做下一个任务。
- 连续 Critical Path 授权只允许自动选择下一个 critical task；不得合并任务、跳过测试、跳过验证或扩大范围。停止条件以 `ccdawn-brt/references/runtime.md` 为准。
- 不扩大范围，不重构无关区域。
- 不覆盖用户或其他 agent 的无关改动。
- 不把失败测试改成适配实现；修实现或修测试意图，不能抹掉行为要求。
- 不用“手动看起来可以”替代要求中的测试命令。

## Execution Loop

执行循环归入本阶段。每个任务按这个顺序执行：

1. BEFORE：确认当前任务、BDD/TDD Anchor、文件范围、工作区状态和无阻塞歧义。
2. DURING：只执行当前任务，不扩大范围，不顺手执行下一个任务。
3. AFTER：验证输出契约，对比 expected vs actual，检查副作用，更新 Workflow Ledger。

连续 Critical Path 模式下，AFTER 通过后自动选择下一个未完成 critical task 继续；如果没有未完成 critical task，进入 `ccdawn-completion-summary`。连续模式不是跳过阶段交接，而是用户预先授权后续交接。

如果验证失败：

- 标记当前任务为 `PARTIAL` 或 `BLOCKED`；
- 写清失败命令、失败原因和影响范围；
- 给出可选修复；
- 只问一个真正阻塞的问题，其他问题放入风险或可选修复。

连续 Critical Path 模式遇到 runtime 定义的停止条件时，必须停止连续推进并报告当前任务状态。

## 输出契约

开发阶段输出保持短，只报告关键证据：

```text
Task N 开发结果:
- BDD: Given... When... Then...
- RED: 命令...；失败原因...
- GREEN: 命令...；通过结果...
- 变更: 文件/模块...
- 自审: 行为契约 PASS/NEEDS_CHANGE；副作用 PASS/ACCEPT_RISK；测试 PASS/NEEDS_CHANGE
- 剩余风险: ...

Ledger Update:
- Current Stage: DEVELOPING
- Current Task: Task N
- Completed Tasks: Task X..., Task N DONE/PARTIAL/BLOCKED
- Verification Evidence: RED..., GREEN...
- Unresolved Risks: ...
- Recommended Next Stage: 下一个任务 / ccdawn-completion-summary

下一步:
Task N 已完成。是否继续？
A. 执行下一个任务（如果还有任务，推荐）...
B. 连续执行剩余 Critical Path（需要明确授权；逐任务 BDD/TDD/验证，遇阻立刻停）...
C. 进入 ccdawn-completion-summary 做阶段总结（所有关键任务完成时推荐）...
D. 回到 ccdawn-task-splitting 调整任务...
E. 暂停...
```

## 完成门槛

任务完成前必须有：

- BDD 契约；
- 至少一个 RED 证据；
- GREEN 后的验证证据；
- 与任务 Goal 对齐的变更摘要；
- 对副作用和范围偏离的自审结论。

缺任一项，都不能声称任务完成。

## Workflow Ledger

每完成或阻塞一个任务，都必须更新账本：

- `Current Task` 是刚执行的任务。
- `Completed Tasks` 记录 `DONE / PARTIAL / BLOCKED`，不能只写“已处理”。
- `Verification Evidence` 写入 RED 和 GREEN 的命令与结果，或替代证据及风险。
- `Unresolved Risks` 写剩余风险和后续验证方式。
- 如果还有未完成 critical task，`Recommended Next Stage` 是下一个任务；如果已授权连续 Critical Path，写成 `继续下一个 critical task`；否则是 `ccdawn-completion-summary`。
- 完整字段和压缩规则以 `ccdawn-brt/references/runtime.md` 为准；本阶段默认只输出 `Ledger Update`。

## 阶段交接

没有连续授权时，每次完成一个任务后必须停下并询问是否继续。

如果还有未完成关键任务，默认建议执行下一个任务，并提供“连续执行剩余 Critical Path”的授权选项。如果所有关键任务完成，默认建议进入 `ccdawn-completion-summary`。

如果用户已经授权连续执行全部 Critical Path，在每个任务完成后输出短 checkpoint，并按 runtime 规则继续或停止。
