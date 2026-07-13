---
name: ccdawn-huawei-nslb-score-loop
description: Use when optimizing, benchmarking, packaging, comparing baselines, handling online score feedback, or coordinating parallel agents for a Huawei Algorithm Challenge 37 NSLB workspace identified by its solver and score-loop artifacts.
license: MIT
---

# Huawei NSLB Score Loop

This is the Huawei NSLB project adapter for `ccdawn-score-loop`.

Use `ccdawn-score-loop` as the generic operating model, then apply the project-specific profile in `references/huawei-nslb-profile.md` when the request involves status, epoch work, workers, gate decisions, packaging, online feedback, failed-diff recovery, or project memory sync.

## Profile

```text
Project root: resolve from explicit `--project`, `CCDawn_HUAWEI_NSLB_ROOT`, or the current repository markers
Primary source: src/Solution.cpp
Tool: <codex-home>\skills\ccdawn-huawei-nslb-score-loop\scripts\score_loop_tools.py
Mutation space: references/mutation_space.json
Main ledger: docs/optimization-ledger.json
Online/offline weights: docs/online-offline-weights.json
Search graph: docs/search-graph.json
Attempt cards: docs/attempt-cards/
Failed diffs: docs/failed-diffs-index.json and docs/failed_diffs/
```

Known online-best anchor unless the project ledger says otherwise:

```text
baseline: baseline-044-large-sparse-phase6-residual-target
online score: 344736301
source SHA256: 28b33d6d67d547fbc4415ec363a1c80db7a1f8e2fe1f308fd96a8a528a0441cb
```

## BRT interface

- Context Boundary: Huawei NSLB project root, current baseline hash, score-loop ledger/search graph, selected command/lane, and isolated worker workspace when applicable.
- Output Contract: status, epoch, worker, gate, package, online feedback, or recovery artifact with machine-readable evidence.
- Allowed Action: only profile-approved commands and lane workspaces; workers never mutate the main baseline, ledger, package map, or promotion state unless the parent gate explicitly does it.
- Success Evidence: command output, `child_result.json`, attempt card, ledger/search-graph update, compiled diff, gate decision, or registered short submission package.
- Stop Condition: source drift, stale baseline hash, overlapping ledger/pool write, missing child result, invalid package, ambiguous online feedback, or user pause.
- Route Out: `ccdawn-score-loop`, project-specific command, launch/recover workers, parent promotion gate, online feedback wait, project memory sync, or BLOCKED with one required input.

## 统一调用契约

- 只处理 BRT interface 范围；不匹配时回 `ccdawn-brt` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## Required context commands

Before meaningful optimization, run or inspect the equivalent current outputs:

```powershell
$project = if ($env:CCDawn_HUAWEI_NSLB_ROOT) {
  (Resolve-Path -LiteralPath $env:CCDawn_HUAWEI_NSLB_ROOT).Path
} else {
  (git rev-parse --show-toplevel 2>$null)
}
if (-not $project -or -not (Test-Path -LiteralPath (Join-Path $project "src\Solution.cpp"))) {
  throw "请通过 --project、CCDawn_HUAWEI_NSLB_ROOT 或当前仓库提供 Huawei NSLB 项目根目录。"
}
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$tool = Join-Path $codexHome "skills\ccdawn-huawei-nslb-score-loop\scripts\score_loop_tools.py"

python $tool status --project $project
python $tool doctor --project $project --min-score 0
python $tool drift --project $project
```

Do not rely on chat memory as the source of truth for score, source hash, active workers, or package mapping.

## Command routing

Route these requests through the profile reference:

- status, doctor, drift, restore online best;
- prepare/run/dispatch/collect/close epoch;
- lane pool update, worker recovery, child result validation;
- failed-diff furnace, risk resurrection, search graph, attempt cards;
- online feedback/update, submission registration, package gate;
- dataset/proxy lane status and validation.

Use short upload names such as `sub053.zip`; store long metadata in `docs/submission-map.json`.

## Worker rule

Workers must follow the generic `ccdawn-score-loop` contract plus these Huawei constraints:

- main project is read-only for workers;
- each lane edits only the assigned isolated workspace;
- solver edits normally touch only `src/Solution.cpp`;
- each edit lane must compile or return a concrete blocker;
- each lane must run the smallest decisive first-kill before broad suites;
- every worker must write `child_result.json` before completion.

For the detailed worker prompt, command router, mutation families, risk-resurrection rules, online calibration rules, and memory sync commands, load `references/huawei-nslb-profile.md`.

## Completion

After meaningful Huawei score-loop work, update project memory with the lane `competition-huawei-nslb` unless the user explicitly says to skip it.
