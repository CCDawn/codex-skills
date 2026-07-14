---
name: ccdawn-pr-review
description: Use when the user explicitly requests review of a PR, diff, branch, commit range, merge readiness, or review feedback, or when a high-risk change has reached an explicit pre-integration review gate; do not trigger merely because ordinary development finished.
license: MIT
---

# CCDawn PR Review

## 目标

只读审阅 PR、diff、branch 或 commit range，判断需求覆盖、回归风险和 merge readiness。先给 findings，不用长矩阵掩盖结论；审阅阶段不顺手改代码。

## BRT interface

- Context Boundary: PR/diff/base-head、需求来源、验证证据、禁止编辑边界、集成目标和排除范围。
- Output Contract: risk-ranked findings、简洁结论、证据缺口、修复顺序或 merge route。
- Allowed Action: 读取 diff/上下文并运行安全检查；不编辑、移动 HEAD/index、合并、推送或发布。
- Success Evidence: diff 与需求已对照，关键证据已检查，每条 finding 绑定位置、影响和验证条件。
- Stop Condition: 缺可审对象、审查目标/需求无法推断、关键证据不可得、对象漂移或远程/高风险动作未授权。
- Route Out: 对应开发 owner、`ccdawn-bug-review`、`ccdawn-planning`、`ccdawn-brt`、提交/PR/合并准备或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface 范围；不匹配时回 `ccdawn-brt` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文；保留技术字面量；只报结论、证据、风险和产出；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## 审阅流程

1. 定位 PR、base/head、merge-base 和实际 diff；检查工作区/分支是否漂移。
2. 从用户要求、PR body、issue/spec、现有行为和项目规则中取得需求来源。只有高影响目标无法推断时才回 BRT 集中对齐，不能只做 owner 路由。
3. 阅读变更及必要上下文，核对状态/API/数据/配置/迁移/用户流程和保护边界。
4. 检查最新测试、构建、lint、类型、运行时或手工验收证据；证据不足不能包装成通过。
5. 按 diff 风险选择相关视角，不固定遍历完整清单；只输出由本次变更引入、暴露或会阻塞集成的问题。
6. findings 优先；随后给 merge 结论和下一 route。

## Findings

- `P0 BLOCKER`：数据丢失、安全事故、核心不可用或不可逆发布风险。
- `P1 MUST_FIX`：重要需求缺失、明确 bug、关键契约/测试/迁移风险。
- `P2 SHOULD_FIX`：边界、错误处理、维护性或局部回归风险。
- `P3 NICE_TO_HAVE`：默认省略；只有能明显降低近期误改或审阅成本时才保留。

每条包含紧凑文件/行号或 diff 位置、问题、影响、建议方向和验证条件。纯风格偏好、无行为影响的命名建议、未被 diff 影响的既有问题不作为 finding；必要时用一句非阻塞备注。没有问题时明确“未发现阻塞性问题”，并说明尚未覆盖的证据边界。

多个问题按依赖和修复成本给执行顺序；用户已要求修复 review findings 时，回最具体 owner 连续处理所有 `SAFE_DIRECT` 项，不每项询问。设计分叉、高风险动作或 BLOCKED 才暂停。

## 结论

- `READY`：无 P0/P1，需求与证据足够。
- `READY_WITH_FIXES`：仅有非阻塞 P2/P3。
- `NEEDS_CHANGES`：存在 P0/P1、需求偏离或关键证据缺失。
- `BLOCKED`：没有可审 diff，或审查目标/证据无法取得。

## 输出

```text
Findings:
- P0/P1/P2/P3 [文件:行] 问题；影响；建议；验证条件

结论: READY / READY_WITH_FIXES / NEEDS_CHANGES / BLOCKED
审阅范围与需求来源: ...
验证证据/缺口: ...
执行顺序（仅多个修复项时）: ...
剩余风险: ...
下一步建议: <一个具体动作>
```

实际提交、推送、合并和发布仍需对应权限；审阅结论不等于自动执行远程动作。
