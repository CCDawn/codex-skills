---
name: ccdawn-task-splitting
description: "Use when BRT or an accepted implementation plan has already found multiple independent deliverables, owners, dependency artifacts, risk gates, verification contracts, parallel lanes, or cross-session boundaries that genuinely require an executable task graph before development."
license: MIT
---

# CCDawn 任务拆分

## 目标

只为已经确认需要拆分的工作建立最小任务图。`NO_SPLIT` 默认由 BRT 或 Planning 内部判定，不把本 skill 当成每个方案都必须经过的审批阶段。

## BRT interface

- Context Boundary: 已接受方案、拆分触发原因、影响面、依赖、owner、风险与验证边界。
- Output Contract: 最小 critical path、必要 task cards、开发模式和连续执行路由；误路由时返回紧凑 `NO_SPLIT`。
- Allowed Action: 只做任务边界与依赖设计；不修改代码，不重新规划需求，不制造可合并的小任务。
- Success Evidence: 每个任务都有独立产出、拥有面、依赖和验证，拆分能降低协调或误改风险。
- Stop Condition: 方案未接受、拆分触发原因不成立、边界或验证不清、高风险动作未确认或任务图不能执行。
- Route Out: 当前 owner 连续实施、`ccdawn-bdd-tdd-development`、`ccdawn-score-loop`、`ccdawn-planning`、`ccdawn-brt` 或 BLOCKED。

用户可见输出默认中文，并遵守 BRT 的自然闸门和下一步规范。

## 拆分闸门

至少满足一项才建立任务图：

- 多个独立交付物或 owner；
- 后续任务必须消费前一任务产生的 artifact；
- 高风险步骤需要独立验收、权限、回滚或发布闸门；
- 需要并行、分 PR、跨会话交接或不同验证契约；
- 用户明确要求拆分。

多个文件、同机制批量修改、描述较长、普通跨模块实现或“可能需要测试”不构成拆分理由。如果误路由且一个上下文可以完成，输出：

```text
拆分判定: NO_SPLIT
理由: <为什么一个执行单元更可靠>
直接路由: 当前 owner 实施并验证
下一步建议: 直接实施
```

然后继续，不建立 Task Graph、ledger 或 summary 阶段。

## 任务设计

- 一个任务交付一个后续步骤或独立验收真正需要的结果。
- 测试、文档、配置和脚手架并入依赖它们的功能任务，不单独漂浮。
- 共享文件、顺序依赖或共享验证的任务保持串行；只有写入面和证据独立才并行。
- Critical Path 只包含完成用户目标必需的任务；可选优化放入 Deferred，不生成当前任务卡。
- 默认连续执行 Critical Path。用户已有执行许可时，不在每个任务之间询问是否继续。

实验 lane 不进入 `SIMPLE/BDD_TDD` 判定：当主要未知量是候选对 metric/score 的影响时，整条 lane 归 `ccdawn-score-loop`。只有从实验中分离出的确定性工程 bug 才建立工程任务。

开发模式按任务判定：

- `SIMPLE`：行为和边界明确，直接实现加风险相称的验证即可。
- `BDD_TDD`：确定性行为存在重大回归、状态/数据/权限/迁移/公共契约风险，需要失败测试锚定预期；使用 `ccdawn-bdd-tdd-development`。

不要因为文件多、跨模块、实现失败或用户要求“谨慎”就自动选择 BDD/TDD；先说明哪项确定性行为风险需要测试先行。

## 紧凑任务卡

```text
Task N: <可观察产出>
- Files/Boundary:
- Dependencies:
- Mode: SIMPLE / BDD_TDD
- Verification:
- Risk/Stop:
```

只有下游确实需要时才补 Inputs、Reuse、回滚或详细 Test Anchor。禁止把每个函数、测试文件或机械编辑拆成任务。

## 输出

```text
任务图:
- 拆分理由:
- Critical Path: Task 1 -> Task 2 -> ...
- 并行/串行边界:

Task 1: ...
Task 2: ...

执行路由:
- 当前任务:
- 连续执行: 是（默认）/ 否（说明自然闸门）
- 成功证据:
- 停止条件:
下一步建议: 执行当前任务
```

任务完成后由当前 owner 用新鲜证据直接收口。只有跨阶段综合、恢复、正式交接或 PR 前需要持久证据时才使用 `ccdawn-completion-summary`，不能把它设为每条 Critical Path 的默认尾声。
