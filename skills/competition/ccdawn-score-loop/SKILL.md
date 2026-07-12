---
name: ccdawn-score-loop
description: "Use when optimizing any measurable score, benchmark, leaderboard, validation metric, online/offline feedback loop, experiment lane, baseline promotion, or submission package where iterative evidence should guide code, model, or search changes."
---

# Score Loop

## Goal

Run score-driven work as an evidence loop:

```text
baseline -> one causal change -> smallest decisive check -> promotion/rejection -> ledger update -> next change
```

This is a generic template. A project-specific profile must define the metric, commands, files, promotion gate, and ledger surfaces. If no profile exists, first build a compact profile instead of inventing commands.

## BRT interface

- Context Boundary: project root, score metric, active baseline, allowed write surface, experiment ledger, validation commands, and selected lane.
- Output Contract: status, experiment lane, worker contract, gate decision, package record, online feedback update, or recovery artifact.
- Allowed Action: only the profile-approved write surface, one causal mechanism per lane, no baseline promotion/package/submission without a parsed gate decision.
- Success Evidence: command output, score delta, diff, result JSON/report, ledger/search update, promotion decision, or registered package.
- Stop Condition: source drift, stale baseline, missing metric definition, invalid validation command, overlapping writes, unsafe promotion, ambiguous online feedback, or user pause.
- Route Out: continue score loop, launch/recover worker lane, promote/reject candidate, package/submit, update project memory, or BLOCKED with one required input.

## 实验 owner 独占

只要当前工作的主要未知量是“候选是否改善 metric/score”，该修改就属于 score-loop experiment lane，即使它改代码、跨模块或结果变差，也不进入通用 `SIMPLE/BDD_TDD` 分类。

- score regression、候选分数下降、假设被拒、online neutral/worse 都是实验 gate 结果，不是 TDD RED，也不代表代码 bug。
- 实验使用 `BASELINE / CANDIDATE / DELTA / PROMOTE / REJECT / HOLD`，不要用 RED/GREEN 描述方向。
- 只有发现预期行为明确的工程缺陷，例如 metric 计算、解析、数据 schema、seed、shape、NaN、打包或评测脚本错误，才临时路由到 `ccdawn-bdd-tdd-development`。
- 临时工程修复必须写清确定性行为，修复并验证后返回原 baseline/lane；TDD GREEN 只能证明工具行为正确，不能证明实验候选应晋升。
- 文件数量、跨模块、运行失败或分数回退本身都不能把整个实验升级成 BDD/TDD。

## 统一输出标准

- 用户可见输出默认中文；只有代码、命令、路径、错误原文、API/协议名、skill 名、状态枚举和外部专名保留英文。
- 报告、方案、审查、阶段文档和交接摘要使用中文标题与中文字段；内部字段对外翻译为：上下文边界、输出契约、允许动作、成功证据、停止条件、路由出口、下一步建议。
- 若必须保留英文状态或枚举，先用中文解释其含义。
- 用户可见正文末尾保留 `下一步建议: ...`，除非被更高优先级系统附录隔开。

## Owner 接入规则

进入本 skill 前先做轻量 owner 自检：

- 如果用户主目标不属于本 skill 的 owner 范围，不继续执行；回 `ccdawn-brt` 做 Owner 仲裁，或转交更具体 owner。
- 如果本 skill 只覆盖复合任务的一部分，只处理当前路由契约覆盖的 Primary/Secondary，不吞掉其他 owner。
- 如果发现 planning/development 正在替代更具体 owner，先输出路由修正，再进入正确 owner。

## Required profile

Before meaningful optimization, identify or create:

```text
Project:
- Root:
- Metric:
- Higher is better / lower is better:
- Active baseline:
- Online/best-known anchor:
- Allowed write files:
- Protected files:
- Status command:
- Fast validation:
- Full validation:
- Packaging command:
- Ledger paths:
- Result artifact schema:
- Promotion gate:
- Stop conditions:
```

Project adapters may keep this in their own `references/*profile.md` or repository docs.

## When to use

Use this skill for:

- benchmark or leaderboard optimization;
- repeated local validation with promotion gates;
- online/offline score disagreement;
- multiple candidate implementations or model variants;
- worker lanes that need isolated evidence;
- package/submission registration;
- recovery of partial or failed experiment diffs.

Do not use it for ordinary feature implementation, one-off bugfixes, or scoreless refactors. Route those to BRT, planning, debugging, or development skills.

## Operating rules

- One lane tests one causal mechanism.
- Prefer a small decisive check before broad validation.
- Do not promote on stale source, unclear metric, missing artifact, or unparsed output.
- Failed attempts still become searchable lessons.
- Online feedback updates calibration; it does not replace clean local validation.
- Hard harness failures block execution; soft confidence issues change lane choice or first-kill tests.
- Coordinator applies promotions; workers do not mutate the main baseline or ledger directly unless the profile explicitly allows it.

## Lane matrix

Every executable lane must fit this shape:

```json
{
  "laneId": "short-id",
  "attemptId": "short-attempt-id",
  "targetComponent": "module/function/model/data fold",
  "mutationType": "edit | architecture | controlled-risk | diagnostic | dataset | fusion",
  "hypothesis": "one causal mechanism only",
  "intendedMetric": "primary or component metric",
  "nonScoreSignal": "secondary signal, legality, runtime, or diagnostic proof",
  "smallestDecisiveEvaluation": "single case, narrow suite, trace, or bounded run",
  "killCondition": "flat, regression, timeout, illegal output, or missing target",
  "expectedDiffSurface": ["path/to/file"],
  "negativeControls": ["known failed family or baseline comparison"],
  "recoveryArtifact": "result JSON, report, diff, or dataset path"
}
```

Proposal-only lanes are valid only for diagnostics, dataset/proxy construction, or when the lane explicitly cannot edit code. They still need a concrete artifact.

## Worker contract

Workers are diff-first executors:

1. Work only in the assigned isolated workspace.
2. Confirm baseline/source identity before editing.
3. Implement exactly one mechanism or produce one diagnostic artifact.
4. Run the smallest decisive evaluation before broad suites.
5. Preserve diff, report, logs, and parsed metrics.
6. Write a result artifact before finishing.

Minimum result fields:

```text
laneId, attemptId, baselineId, hypothesis, mutationType, changedFiles,
commandsRun, checksRun, smallestDecisiveEvaluationResult, metricsBeforeAfter,
promotionCandidate, result, summary, avoidNextTime, artifactPaths, diffSummary
```

Existing profiles may continue reading legacy `smallestDecisiveTest` / `smallestDecisiveTestResult` fields, but new instructions and artifacts use `evaluation` to avoid confusing experiment evidence with TDD.

## Evaluation and promotion

Use `smoke -> screen -> parent gate`:

- Smoke: cheap proof that the target signal moves or the idea is impossible.
- Screen: 2-3 representative checks for promising candidates.
- Parent gate: full validation, legality, runtime, package shape, ledger update, and rollback readiness.

Promote only when:

- candidate is based on the current baseline;
- diff scope matches the lane;
- validation output is parsed, not eyeballed;
- failure modes and secondary signals are acceptable;
- ledger/search graph records the decision;
- package or release artifacts match the project profile.

Reject or hold when the gain is unparsed, overfit to one fold, illegal, too slow, dependent on stale state, or missing a reproducible artifact.

## Online/offline feedback

Treat online score, hidden tests, external review, or public leaderboard as sparse validation folds:

1. Record the exact package/candidate and score.
2. Compare against local validation and expected direction.
3. Identify which local fold or proxy lied.
4. Update trust weights or diagnostic cases.
5. Continue only with a named causal explanation or new calibration lane.

Never move best-known online/baseline on neutral or worse feedback unless the user explicitly accepts a tradeoff.

## Recovery loop

When progress stalls:

- inspect failed diffs, partial workers, rejected attempts, and stale labels;
- revive only candidates with a new causal variable, new witness, or reusable artifact;
- rewrite broad old ideas into one-mechanism lanes;
- preserve rejected compiled diffs as search material;
- stop if no safe new causal variable can be named.

## 研究回传契约

当本 lane 由 `ccdawn-ai-research-loop` 发起时，gate 决策后把实验信息交回研究 owner，而不是自行决定整个研究方向：

```text
Candidate:
Hypothesis outcome: supported / rejected / unresolved
Metric evidence:
Mechanism evidence:
Confidence and caveat:
Reusable lesson:
Next-hypothesis signal:
Pivot signal:
Artifact paths:
```

- metric 没有提升但排除了关键机制时，仍可标记为高信息价值；不得伪装成 promotion。
- 单次分数提升但缺少机制证据时，只能晋升候选 baseline，不能直接扩写成研究 claim。
- 连续 lane 出现相同失败、结果冲突、强 seed/split 敏感或信息增益降低时，设置 `Pivot signal`，交回外层综合。
- QUICK 模式可把这些字段压缩进短汇报；只有跨会话、高成本或需要交接时才写独立 artifact。
- score-loop 不负责生成新的研究总规划；下一假设由研究 owner 结合多轮证据选择。

## Compact outputs

Status:

```text
Score Loop Status:
- Baseline:
- Best score:
- Active lanes:
- Drift/blockers:
- Recommended next lane:
- Success Evidence:
- Route Out:
```

Gate:

```text
Gate Decision:
- Candidate:
- Evidence:
- Verdict: promote / reject / hold / blocked
- Reason:
- Next action:
```

Research return:

```text
研究回传:
- 假设结果:
- 指标证据:
- 机制证据:
- 可复用教训:
- 下一假设/转向信号:
- Artifact:
```

Online feedback:

```text
Online Feedback:
- Package/candidate:
- Score:
- Local expectation:
- Calibration lesson:
- Best-known update: yes/no
- Next lane:
```
