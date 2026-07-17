---
name: ccdawn-bug-review
description: "Use when a bug, correctness regression, failing test, build failure, abnormal behavior, or suspected root cause needs Chinese-first diagnosis, bounded repair, and evidence-based verification; measurable performance work uses ccdawn-performance-engineering."
license: MIT
---

# CCDawn Bug Review

## 目标

直接承接 bug 诊断与契约内修复：先用证据定位根因，再做最小修复和风险相称的验证。不要求展示固定阶段、长检查表或完整思维过程。

## BRT interface

- Context Boundary: 预期行为、实际症状、失败命令/日志、相关代码与测试、允许修改面和非目标。
- Output Contract: 根因状态、证据链、最小修复或下一 probe、影响范围、验证结果和剩余风险。
- Allowed Action: 用户要求修复且边界清楚时可直接读取、复现、修改和验证；只要求审查时保持只读。
- Success Evidence: 失败可复现或有等价证据，根因与修复存在因果联系，目标验证通过且未越界。
- Stop Condition: 缺少必要对象/权限、根因仍不稳定且写入会扩大误改、需要破坏性动作、需求冲突或风险越过当前授权。
- Route Out: 契约内修复、`root-cause-tracing`、`ccdawn-performance-engineering`、`ccdawn-planning`、`ccdawn-development-cleanup`、`ccdawn-pr-review`、`ccdawn-brt` 或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface 范围；不匹配时回 `ccdawn-brt` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## 调试契约

1. 写清 `Expected / Actual / Scope`，先读本地可得的代码、日志、失败测试和近期 diff。
2. 优先复用现有失败测试或稳定复现；无法直接运行时，用调用链、状态变化或日志建立最窄证据链。
3. 定位 owning surface，沿数据流或控制流追到最早错误来源。来源藏在深层链路时才加载 `root-cause-tracing`。
4. 主问题是可测延迟、吞吐或资源时路由 `ccdawn-performance-engineering`；需先排除正确性、环境或失败重试时继续诊断。
5. 标记根因：`CONFIRMED / HYPOTHESIS / ENVIRONMENT / TEST_ISSUE / REQUIREMENT_MISMATCH`。只有 `CONFIRMED` 才进入行为修复；其他状态继续低风险 probe 或路由正确 owner。
6. 用户已授权修复且根因、边界、回滚和验证清楚时，直接做最小修复；不为流程形式停下确认。
7. 运行能证明因果关系的窄验证，再按影响面决定是否扩展。区分实现失败、测试意图过期、环境失败和需求不一致。

## Bug 测试锚点

Bug 修复不转交 TDD owner。已有失败测试或稳定复现直接作为 RED；若回归风险显著且没有自动化证据，在当前 owner 内补一个最小行为测试，确认它因目标缺陷失败后修复并得到 GREEN。局部、可逆且现有验证足够时直接修复，不为形式制造 RED。

测试只证明已确认的预期行为，不替代根因诊断。测试意图过期时标记 `TEST_ISSUE`，需求不一致时标记 `REQUIREMENT_MISMATCH`，不得为了 GREEN 固化旧约束。

## 流程重量

- 简单、局部、可逆问题：当前 owner 直接修复并验证，不 planning、不拆分、不创建 worktree。
- 确定性行为存在明显回归、状态/数据/权限/迁移或公共契约风险：由当前 Bug owner 使用紧凑测试锚点，不发生 owner 切换。
- 真实设计分叉、跨系统迁移或修复边界无法在当前上下文稳定表达：进入 `ccdawn-planning`。
- 多文件或复杂调用链本身不触发额外流程；能由一个根因修复统一解决就保持一个实现单元。

## 输出

普通修复只需汇报：`根因 / 修改 / 验证 / 剩余风险 / 下一步建议`。只读审查或阻塞时再补：

```text
Bug 判断:
- 根因状态:
- 关键证据:
- 影响范围:
- 建议动作:
- 停止条件:
下一步建议: <一个具体动作>
```

不得为了让测试通过而削弱正确行为，也不得在根因仍是猜测时堆叠补丁。
