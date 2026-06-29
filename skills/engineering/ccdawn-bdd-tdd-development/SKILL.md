---
name: ccdawn-bdd-tdd-development
description: Use when a CCDawn task has been selected and the user confirms entering development; applies before implementing behavior changes, features, bug fixes, refactors, or tests that need BDD behavior anchors, TDD red-green-refactor discipline, task-scoped execution, and evidence before moving on.
---

# CCDawn BDD/TDD Development

## 目标

按已选择的任务进行开发。此阶段一次只执行一个任务，先锁定行为，再用 TDD 实现。

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

如果没有明确任务，不要开始开发，先回到 `ccdawn-task-splitting`。

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

写测试、mock 或测试工具时，如出现 mock 断言、test-only production API、过度 mock，读取 `testing-anti-patterns.md`。

## 执行边界

- 只执行当前任务，不顺手做下一个任务。
- 不扩大范围，不重构无关区域。
- 不覆盖用户或其他 agent 的无关改动。
- 不把失败测试改成适配实现；修实现或修测试意图，不能抹掉行为要求。
- 不用“手动看起来可以”替代要求中的测试命令。

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

下一步:
Task N 已完成。是否继续？
A. 执行下一个任务（如果还有任务，推荐）...
B. 进入 ccdawn-completion-summary 做阶段总结（所有关键任务完成时推荐）...
C. 回到 ccdawn-task-splitting 调整任务...
D. 暂停...
```

## 完成门槛

任务完成前必须有：

- BDD 契约；
- 至少一个 RED 证据；
- GREEN 后的验证证据；
- 与任务 Goal 对齐的变更摘要；
- 对副作用和范围偏离的自审结论。

缺任一项，都不能声称任务完成。

## 阶段交接

每次完成一个任务后必须停下并询问是否继续。

如果还有未完成关键任务，默认建议执行下一个任务。如果所有关键任务完成，默认建议进入 `ccdawn-completion-summary`。
