---
name: ccdawn-competition-research-lifecycle
description: Use when coordinating a research competition lifecycle, Kaggle-style challenge, academic contest, benchmark track, public leaderboard workflow, multi-agent experiment lanes, evidence ledger, paper claim traceability, or reproducible submission package.
---

# 竞赛科研全流程（Competition Research Lifecycle）

这个 skill 用来把一个竞赛科研项目当成可审查、可回退、可复现的研究闭环来运行。

`ccdawn-brt` 是治理层。它不替代任何阶段，而是用来定义行为目标、审查风险，并在阶段推进前设定验收检查。

`ccdawn-ai-research-loop` 是 baseline 复现、假设实验和多轮证据综合的研究工程层。

`ccdawn-research-rigor-review` 是重要 baseline、论文结论和提交证据的严谨性审查层。

## BRT interface

- Context Boundary: 竞赛规则、数据/metric、active baseline/evidence、实验账本、论文/提交工件和当前阶段。
- Output Contract: 阶段诊断、阶段行动、并行 lane、恢复计划、提交/论文证据审计或下一阶段路由。
- Allowed Action: 只在当前阶段 artifact 和已确认 lane 范围内行动；晋升 baseline/evidence、提交打包、论文 claim 固化或多 lane 合并前必须有 gate 证据。
- Success Evidence: 阶段 artifact、run log、metric 表、claim map、submission checklist、leaderboard/外部反馈记录或复现实验证据。
- Stop Condition: 数据/metric 漂移、active baseline 不一致、证据链缺失、提交格式不确定、claim 无来源、leaderboard 与 validation 严重冲突且未解释。
- Route Out: 当前阶段继续、`ccdawn-ai-research-loop`、`ccdawn-score-loop`、`ccdawn-research-rigor-review`、工程类 owner skill、`ccdawn-completion-summary`，或 BLOCKED。

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

## 核心原则

- 不从聊天记忆推进项目。优先读取当前项目里的规则、数据说明、实验日志、run records、论文草稿和提交要求。
- 每个实验、数据版本、baseline、表格和论文 claim 都要有来源链。
- 一次实验只验证一个主要假设。不要把多个策略捆成一个不可归因的胜利。
- 高成本训练前先跑小样本 smoke / proxy ranking。它用于发现 bug、估计算法优劣和淘汰明显差的候选，但不能替代正式 full validation、三 seed 或论文主结果。
- 公开榜单或外部评测是强信号，但不能替代干净 validation、复现日志和 claim 追溯。
- 如果发现数据泄漏、metric 错误、split 错误、日志缺失或提交包不一致，立即进入 `phase-recovery`，并标记受影响证据为 stale。

## 运行模式

- `phase-diagnosis`：根据当前工件、阻塞点和证据缺口判断阶段。
- `phase-execution`：完成当前阶段，并产出该阶段的可审查工件。
- `phase-recovery`：上游证据失效时回退修复，并隔离 stale 结果。
- `parallel-lanes`：把独立研究、数据、实验、写作审计任务拆成并行 lane，但只允许一个经过验证的候选结果晋升为 active baseline 或 active evidence。

## 快速开始

1. 读取当前项目中最可信的 source of truth：规则、数据 manifest、实验账本、run logs、论文证据映射、提交清单。
2. 判断当前阶段和模式：`phase-diagnosis`、`phase-execution`、`phase-recovery` 或 `parallel-lanes`。
3. 用 BRT 语言锁定目标、输入、输出、风险审查和测试证据。
4. 明确 active baseline、active data version、active evidence，或指出缺口。
5. 路由到最合适的支撑 skill，并先补齐本阶段工件。
6. 每一轮都给出明确决策：`advance`、`iterate`、`recover` 或 `stop`。

## 阶段列表

1. 任务定义
2. 数据准备
3. 文献与方案研究
4. Baseline 系统
5. 训练与实验
6. 分析与消融
7. 论文写作
8. 提交打包

查看 [REFERENCE.md](REFERENCE.md) 获取逐阶段规则、artifact 要求和路由说明。
查看 [TEMPLATES.md](TEMPLATES.md) 获取可直接复用的模板和响应骨架。
查看 [EXAMPLES.md](EXAMPLES.md) 获取常见竞赛类型的示例调用。

## Source of Truth 规则

如果项目里已有下列工件，先读取它们，再下判断：

- 竞赛规则、评分说明、提交格式、官方 FAQ
- `data-manifest`、`split-strategy`、预处理日志
- baseline 记录、实验账本、run logs、model registry
- 消融表、错误分析、最终模型选择记录
- 论文 outline、claim map、表格和图片来源记录
- submission checklist、environment lock、复现说明

如果没有这些工件，先创建或要求补齐最小版本，不要假装已有证据。

## Baseline 与证据晋升规则

- 新实验必须说明基于哪个 active baseline、数据版本和 metric 版本。
- 若当前代码、数据、配置或论文表格与 active 记录不一致，先停下并报告漂移。
- 只有通过阶段 gate 的候选结果才能晋升为 active baseline 或 active evidence。
- 失败实验也要记录 lesson、failure reason 和 avoid next time。
- 论文 claim 只能引用 active 或明确标记为 accepted 的证据。

## 小样本 Smoke Gate

当正式训练很慢、算力昂贵或候选算法很多时，先建立 smoke gate：

1. 固定一个小样本子集、seed、训练步数、评估命令和记录格式。
2. 让 active baseline 和每个候选算法都跑同一个 smoke。
3. 记录能否启动、是否 OOM、单步耗时、显存峰值、proxy metric、相对 baseline delta。
4. 只把 smoke 作为 `promote-to-full-run`、`reject` 或 `needs-more-evidence` 的依据。
5. 不把 smoke 分数写成论文主结果，不用它替代正式验证。

如果 smoke 排名和历史正式结果经常冲突，先修正 smoke 设计，而不是继续依赖它筛选算法。

## 并行 lane 规则

当用户要求多 agent、并行推进、快速探索或拆分任务时：

1. 建立 3-6 个互相独立的 lane。
2. 每个 lane 只能有一个主假设、一个交付物和清晰边界。
3. 不让多个 lane 同时修改同一个主工作区文件。
4. lane 产物只是候选证据，不能直接晋升。
5. 合并前必须比较 diff、日志、指标、风险和证据来源。

常用 lane：`data-audit`、`literature-forensics`、`baseline-build`、`training-ablation`、`leaderboard-alignment`、`claim-audit`、`submission-check`。

## 路由规则

- 进入新阶段、修改范围、或准备把结果推进到下一阶段时，使用 `ccdawn-brt`。
- 在第 3、5、6 阶段使用 `ccdawn-ai-research-loop` 统筹 baseline 复现、假设组合、实验 lane 和 findings 综合；具体 metric lane 下沉到 `ccdawn-score-loop`。
- 在第 7 阶段，如果 related work、方法定位或证据组织仍然松散，先由研究循环收敛证据与适用范围。
- 在第 7 阶段后段和第 8 阶段之前，使用 `ccdawn-research-rigor-review` 审查 abstract、contribution bullets、tables 和最终 claims 的证据支撑。
- 论文、项目、榜单和非论文资料检索使用当前已安装的浏览/研究工具；不把未安装的外部 skill 名写成强制 owner。
- 只有证据、实验和 claims 已整理清楚后，才路由到当前可用的论文写作 owner。
- 数据脚本、训练管线、调试和复现性问题，交给工程类 skills。
- 需要拆里程碑、issues 或 checklist 时，交给项目管理类 skills。

## 阶段退出前必须具备的内容

离开任一阶段前，至少确保有：

- 一个清晰的目标陈述
- 一个 BRT gate
- 一个具体 artifact，或者一个被明确命名的 artifact 缺口
- active baseline / active evidence 状态，或为什么当前阶段还没有
- 一个退出决策
- 一个归属明确的人、agent 或 workstream 的下一步行动

## 响应格式

触发这个 skill 时，使用以下格式响应：

```text
当前阶段:
阶段模式:
目标:
输入:
Context Boundary:
Source of truth:
Active baseline / evidence:
建议做法:
支持技能:
要产出的 artifact:
BRT gate:
- Behavior:
- Review:
- Test:
范围约束:
Success Evidence:
Stop Condition:
退出标准:
阶段决策:
下一步行动:
Route Out:
```

