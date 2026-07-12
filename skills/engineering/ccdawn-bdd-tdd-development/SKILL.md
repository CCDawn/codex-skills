---
name: ccdawn-bdd-tdd-development
description: Use when a selected CCDawn subtask has meaningful behavior, regression, state, data, security, migration, public-contract, or cross-module risk that needs a failing test before implementation; simple or mechanical work should stay with its current owner and use targeted verification.
---

# CCDawn 紧凑 BDD/TDD

## 目标

只对已选中的复杂子任务使用最少测试闭环。保留 RED/GREEN 的可信度，不生成无助于实现的仪式性文档、逐步旁白或代理审查链。

## BRT interface

- Context Boundary: 当前子任务、目标行为、owned surface、保护边界、现有失败证据和验证命令。
- Output Contract: 最小实现、紧凑 RED/GREEN 证据、相关验证结果和剩余风险。
- Allowed Action: 只改当前行为所需的生产代码和测试；不扩大范围、不覆盖无关改动。
- Success Evidence: RED 确认目标缺失或回归，GREEN 确认最小实现通过，相关回归检查通过。
- Stop Condition: 行为预期不清、测试不能证明目标、边界冲突、修复需要扩大范围或高风险授权。
- Route Out: 当前 owner、`ccdawn-score-loop`、下一个已授权任务、`ccdawn-completion-summary`、`ccdawn-pr-review`、`ccdawn-brt` 或 BLOCKED。

## 模式闸门

进入本 skill 前按子任务判断，不给整个请求贴 `BDD_TDD` 标签。

直接降级为轻量实现，当任务是机械替换、样式/文案、配置、生成代码、小范围适配，或现有验证已经足够证明行为。

分数下降、metric 未提升、候选被 reject、假设失败、online neutral/worse 是实验结果，不是 TDD RED。此类任务返回 `ccdawn-score-loop`；只有预期输入输出明确的 metric/harness/parser/schema/seed/shape/NaN/打包 bug 留在本 skill。

使用紧凑 TDD，当存在任一强信号：

- 已知的确定性软件行为回归或失败测试；
- 状态、数据、权限、安全、迁移、公共 API 或持久化风险；
- 失败路径/边界容易遗漏；
- 跨模块行为只有自动化测试才能可信证明；
- 用户明确要求 TDD。

只有“文件多”“描述长”或 Superpowers 写着 `always`，不足以触发本 skill。

## 紧凑 TDD

1. 用一行锁定行为：`给定 ...，当 ...，则 ...`。只有行为仍有真实分叉时才展示给用户。
2. 现有失败测试或稳定复现可直接作为 RED；不要为了形式再复制一个测试。
3. 没有 RED 时，只写能证明当前行为边界的最小失败测试，并运行最窄命令确认失败原因正确。
4. 写通过该测试所需的最小实现，不顺带重构。
5. 重跑最窄测试得到 GREEN；随后只运行受影响的相关测试。全量测试留给集成风险或最终收口。
6. 只有实现已经产生重复或明显复杂度时才重构，并保持测试通过。

Token 约束：

- 不为每个函数、分支或实现细节各写一个测试；围绕可观察行为和高风险边界组织测试。
- 不创建 `.feature`、长 Given/When/Then 文档或测试矩阵，除非用户/项目明确需要。
- 已保存真实 RED 输出后，不回滚修复再次证明失败。
- 不逐轮汇报 RED、GREEN、REFACTOR；执行完成后压缩为一条证据链。
- 优先复用现有 fixture/helper；新增测试基础设施的成本高于当前风险时，改用最小集成测试、结构检查或可逆 probe，并说明缺口。
- 出现 mock 断言、test-only production API 或过度 mock 风险时，才读取 `testing-anti-patterns.md`；写正式 Gherkin 时才读取 `references/gherkin.md`。

## 子代理派遣

默认不派发子代理。当前 agent 能在同一上下文完成实现和窄验证时，直接执行。

只有同时满足以下条件才派发：任务彼此独立、修改面不重叠、交付物可单独验证，而且节省的工作明显大于准备上下文、审查和合并成本。

- 相关的连续步骤交给一个实现 agent，不按测试/文件/小任务分别派发。
- 子代理只接收紧凑包：目标行为、owned files、保护边界、RED/验证命令、完成条件；不发送完整对话、完整方案和无关历史。
- 默认不做“每任务 implementer + spec reviewer + quality reviewer”。主 agent 检查 diff 并重跑证据即可。
- 只有安全/数据/迁移/公共 API 等高风险最终边界，或用户明确要求独立审查时，才增加一个最终 reviewer。
- 子代理不得继续派发子代理；确有独立新 lane 时回主 agent 决策。
- 同文件、顺序依赖或共享验证的任务留在主 agent 串行执行，不创建额外 worktree。

## 失败处理

- RED 失败原因错误：先修测试或环境，不写生产实现。
- GREEN 未通过：在当前边界内修复并重跑，不新增代理或扩大测试面逃避根因。
- 测试意图与需求冲突：停止并回 BRT 对齐，不能削弱需求来过测试。
- 自动化不可行：记录替代证据、残余风险和后续触发条件，不伪造 TDD 完成。

## 输出

默认只输出：

```text
开发结果:
- 模式: LIGHTWEIGHT / COMPACT_TDD
- 变更: <文件和行为>
- 证据: RED <命令/关键信号>；GREEN <命令/结果>；回归 <必要检查>
- 风险: <无或一个真实缺口>
下一步建议: <继续下一个已授权任务或收口>
```

`LIGHTWEIGHT` 不输出虚构 RED/GREEN。只有 FULL_FLOW、跨阶段交接、阻塞或存在 Deferred 项时才更新完整 ledger；普通任务不重复输出 Context Boundary、Task Graph、自审矩阵和阶段菜单。

## 完成门槛

- 变更满足当前行为和文件边界；
- COMPACT_TDD 有真实 RED 与 GREEN，LIGHTWEIGHT 有最小充分验证；
- 主 agent 已检查实际 diff 和验证输出；
- 没有未说明的失败、范围扩张或高风险动作。
