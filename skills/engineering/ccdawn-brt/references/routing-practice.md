# BRT Routing Practice

Read this file only when route choice is unclear, a user asks whether routing is practical, or a new scenario needs calibration.

## Practical Route Gate

A route is actionable only when it can fill this contract:

```text
Route Contract:
- Owner:
- Mode:
- Next Output:
- Allowed Action:
- Success Evidence:
- Stop Condition:
```

If `Next Output` or `Success Evidence` is vague, the route is not ready. Probe or ask one high-signal question before acting.

## Scenario Matrix

| User signal | Primary route | Mode | Next output | Success evidence | Stop condition |
|---|---|---|---|---|---|
| "修 bug / 为什么异常 / 测试失败" with target behavior | `systematic-debugging`; add `root-cause-tracing` when source is hidden | `COMPACT_FLOW` or `FAST_PATH` | root cause plus minimal fix | failing evidence reproduced or traced, fix diff, relevant test/log passes | cannot reproduce, ownership unclear, fix crosses scope |
| "审 PR / 看 diff / 能不能合并" | `ccdawn-pr-review` | `COMPACT_FLOW` | findings ordered by risk and merge readiness | diff inspected, requirement/evidence checked, blockers named or cleared | missing diff, stale branch, merge/release decision |
| "审项目 / 架构体检 / 技术债 / 接手摸底" | `ccdawn-project-review` | `COMPACT_FLOW` | risk-ranked project review and action queue | source files inspected, evidence-linked findings, recommended next owner | requested write action or scope becomes implementation |
| "评价方案 / 这个流程繁琐吗 / skill 是否有效" | most specific owner first; otherwise `ccdawn-evaluation` | `MICRO` or `COMPACT_FLOW` | verdict, tradeoffs, actionable improvement queue | evaluated object named, criteria stated, concrete examples or evidence | object unclear or user wants implementation |
| "新增复杂功能 / 模块 / 编辑器 / 搜索 / 可视化 / 导入导出" | `ccdawn-feature-reuse-research` before planning | `FULL_FLOW` | reuse candidates and implementation implication | searched current/web ecosystem when needed, candidates compared, reuse value decided | feature is actually small/local, network blocked, user forbids research |
| "目标明确但要先定方案" | `ccdawn-planning` | `COMPACT_FLOW` or `FULL_FLOW` | implementation plan with scope, files, risks, validation | plan covers confirmed intent and success evidence | requirement unstable or direct FAST_PATH is enough |
| "继续 / 按推荐来 / 确认" after a prior stage | route to the recommended next owner in ledger | current flow | next stage artifact, not repeated alignment | ledger fields match current request and no new blocker | user changed goal or previous route lacks success evidence |
| "多个动作一起做" | Intent Bundle in `ccdawn-brt`; route Primary first | `COMPACT_FLOW` | ordered Primary/Secondary/Deferred or internal sequence | owner/risk/verification boundaries resolved | actions conflict or need user tradeoff |
| Review output has Guardrail, Fix, telemetry, refactor | Action Queue in `ccdawn-brt`; execute Guardrail only if it prevents harm, otherwise Primary Fix | `COMPACT_FLOW` | selected queue item plan or execution | each queue item has evidence/impact/route/success evidence | stale evidence, high-risk merge/release/delete |
| Clear one-file small edit with verification | `FAST_PATH` | `SILENT` or `MICRO` | minimal diff plus verification | targeted check passes or structural evidence exists | touches state/API/data/migration/release or ownership uncertain |

## Failure Smells

- Route says only "建议进入某 skill" but cannot name the next artifact.
- Route recommends planning even though a low-risk edit can be finished and verified now.
- Route creates worktrees or subagents for one-theme sequential work.
- Route splits "实现、验证、汇报" into separate tasks without distinct owners or risks.
- Route sends review evidence gaps and confirmed defects into the same severity bucket.
- Route keeps asking for confirmation after the user already said "继续", "确认", or "按推荐来".

## Output Shapes

Use one line for routine routing:

```text
路由判断: Owner = ccdawn-project-review；Mode = COMPACT_FLOW；Next Output = action queue；Success Evidence = evidence-linked findings with selected next route.
```

Use a short queue when the user needs to choose:

```text
行动队列: Guardrail = ...；Primary Fix = ...；Telemetry Gap = ...；Deferred = ...
推荐下一步: A 执行 Primary Fix（推荐）/ B 先补 telemetry / C 暂停
```

Use a blocking question only when the contract cannot be filled:

```text
BLOCKED: 路由缺少审阅对象。请选择 A 当前 diff（推荐）/ B 指定 PR URL / C 指定文件范围。
```
