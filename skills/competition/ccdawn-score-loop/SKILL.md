---
name: ccdawn-score-loop
description: "Use when repeated work is governed by an explicit metric, active baseline, candidate comparison, promotion gate, leaderboard feedback, or submission iteration; do not use for a one-off research check that its current owner can execute directly."
license: MIT
---

# CCDawn Score Loop

## 目标

围绕一个明确 metric 连续比较 baseline 与 candidate，并用可复现证据决定 `PROMOTE / REJECT / HOLD`。这是单条量化 lane owner，不负责整个研究方向或竞赛生命周期。

## BRT interface

- Context Boundary: metric、active baseline、candidate/lane、评价命令、允许写入面、晋升条件和预算。
- Output Contract: candidate 结果、delta、gate 决策、必要记录和下一 lane/回传。
- Allowed Action: 在已确认范围内一次改变一个主要机制并评估；不静默改变 metric、数据、baseline 或提交目标。
- Success Evidence: baseline/candidate 身份、命令、解析后的指标、diff/config、关键副指标和 artifact。
- Stop Condition: baseline/协议漂移、metric 不明、结果不可解析、写入冲突、预算耗尽或继续无信息价值。
- Route Out: 继续当前 loop、返回 `ccdawn-ai-research-loop`、返回 `ccdawn-competition-research-lifecycle`、`ccdawn-bug-review`、`ccdawn-brt` 或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface 范围；不匹配时回 `ccdawn-brt` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## 实验 owner 独占

只有主要未知量是“候选能否持续改善明确 metric，并需要晋升/淘汰循环”时进入。AI Research 中可在同一上下文完成的一次低成本实验由研究 owner 直接执行，不为一次比较加载本 skill。

分数下降、candidate reject 和 online neutral/worse 是实验结果，不是 TDD RED。确定性的 metric/parser/schema/seed/shape/NaN/打包 bug 临时路由 `ccdawn-bug-review`，修复后返回原 lane。

## 自适应重量

- `QUICK`：已有 baseline、命令和 gate，直接比较一个 candidate；不创建 profile、ledger、worker 或独立 artifact。
- `STANDARD`：反复候选、跨会话或需要晋升历史；维护最小记录。
- `FULL`：leaderboard/online feedback、提交包、昂贵运行或并行 lane；使用项目 profile 和持久 artifact。

缺少正式 profile 不阻塞 QUICK；只要 metric、baseline、命令、范围和 gate 足以解释结果即可。STANDARD/FULL 才持久化这些字段，优先读取项目已有事实源，不创建平行 ledger。

## 最小循环

1. 确认当前 baseline、source/config、metric、数据/seed 和评价协议没有漂移。
2. 定义一个主要机制、预期信号、`smallestDecisiveEvaluation` 和 kill condition。
3. 先运行最小决定性检查；有希望时再扩到代表性检查或完整 gate。
4. 解析 baseline/candidate/delta 与副作用，得到 `PROMOTE / REJECT / HOLD / BLOCKED`。
5. 只有晋升、跨会话恢复、online feedback 或可复用失败教训才写记录；普通 QUICK 直接汇报。
6. 有执行许可且下一 lane 明确时连续推进，不逐候选询问。

一个 lane 只改变一个可归因机制。Smoke/proxy 用于淘汰和排序，不替代目标评估；online score 是稀疏外部证据，不覆盖干净本地协议。没有新的因果变量、诊断信号或校准价值时停止重复尝试。

## 并行与回传

默认不创建 worker、worktree 或 lane matrix。只有候选写入面独立、资源允许且并行收益明显时才隔离；worker 只返回 diff、命令、指标和 artifact，不能自行晋升共享 baseline。

由 AI Research 发起时只回传：`Candidate / Hypothesis outcome / Metric evidence / Mechanism evidence / Caveat / Reusable lesson / Pivot signal`，研究方向仍由研究 owner 决定。由 Competition Lifecycle 发起时回传 gate 与提交/榜单影响。

## 输出

```text
Gate: PROMOTE / REJECT / HOLD / BLOCKED
- Baseline / Candidate:
- Metric delta 与关键副作用:
- 机制判断与证据:
- 记录/Artifact: <仅需要时>
下一步建议: <一个具体动作>
```
