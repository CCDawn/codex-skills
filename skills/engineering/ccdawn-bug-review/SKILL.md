---
name: ccdawn-bug-review
description: Use when the user reports a bug, regression, failing test, broken behavior, inconsistent state, suspected root cause, or asks to inspect why something is wrong before deciding whether to fix it.
---

# CCDawn Bug Review

## 目标

对 bug、回归、失败测试或异常行为做证据化审查，先判断问题是否真实、影响什么、最可能的根因在哪里，再决定是否进入修复流程。

此阶段只审查和定位，不直接修代码；除非用户明确要求“边查边修”，否则发现修复动作后路由回 `ccdawn-planning`、`ccdawn-task-splitting` 或对应开发模式。

## 进入条件

使用前确认至少有一个信号：

- 用户描述了错误、异常、失败、回归、不一致、卡住或“为什么会这样”；
- 当前测试、构建、日志、UI、接口或数据状态显示异常；
- PR/diff review 发现疑似 bug，需要先定位根因；
- 实现阶段验证失败，需要判断是代码、测试、环境还是需求问题。

如果用户其实是在要求审阅 PR/diff，使用 `ccdawn-pr-review`。如果用户是在比较方案或评价质量，使用 `ccdawn-evaluation`。

## 审查方式

1. 复述可观察症状：只写用户或工具能看到的现象。
2. 收集证据：读取相关代码、测试、日志、配置、命令输出或最小复现路径。
3. 分层定位：区分需求误解、测试错误、环境问题、数据问题、实现 bug、集成回归。
4. 给出根因判断：按置信度排序，说明证据和反证。
5. 路由修复：判断是否需要轻量修复、重新规划、任务拆分或 BDD/TDD。

## 输出契约

```text
Bug 审查:
- 结论: CONFIRMED / NOT_REPRODUCED / ENVIRONMENT / TEST_ISSUE / NEEDS_MORE_EVIDENCE
- 症状: ...
- 证据: 命令/文件/日志/复现信号...
- 影响范围: ...
- 根因候选:
  - A ...；证据...；置信度...
  - B ...；证据...；置信度...
- 推荐处理: ...

下一步:
A. 进入轻量修复（局部、低风险、验证清楚时推荐）...
B. 进入 ccdawn-planning 制定修复方案（跨模块或根因影响设计时推荐）...
C. 进入 ccdawn-task-splitting 判定子任务模式（修复需要拆分时推荐）...
D. 补充复现证据...
E. 暂停...
```

## 路由规则

- 局部、根因明确、可快速验证：轻量修复。
- 涉及状态流转、持久化、权限、安全、公共 API、迁移、发布或多模块：`ccdawn-planning`。
- 修复路径有多个依赖步骤：`ccdawn-task-splitting`。
- 子任务复杂、容易回归或需要行为测试证明：`ccdawn-bdd-tdd-development`。
- 需要提交、PR 或合并前审查：`ccdawn-pr-review`。

## 质量门槛

- 不把猜测写成结论。
- 不用“可能是这里”替代证据。
- 不为了修复而跳过复现或最小证据。
- 不把环境失败误判成业务 bug。
- 不在没有用户授权时顺手修代码。

