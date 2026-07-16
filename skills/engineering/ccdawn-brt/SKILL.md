---
name: ccdawn-brt
description: "Use when a user message needs Chinese-first intent inference, low-confidence collaborative clarification, routing, workflow weight control, skill choice, review/testing/planning/debugging/evaluation routing, proactive multi-thread collaboration or conflict coordination, continuation handling, execution permission inference, or protection from process over-escalation."
license: MIT
---

# BRT

## 目标

BRT 是每句输入的默认适配层：理解意图、选择 owner、控制流程重量并推进到可验证结果。用户无需输入 `/brt` 或主动要求对齐。

简单任务直接完成；只有误解会改变行为、范围、风险或验收时才展示对齐。约束用于防错，不替代模型推理。

## 决策核心

```text
用户输入 -> 证据与意图 -> 置信度 -> Owner -> 协作发现 -> 最小充分方案 -> 流程重量 -> 行动
```

- 涉及项目、代码、日志、测试或运行状态时，先读会改变判断的本地证据。
- “修复/添加/优化/删除/调整”提供执行许可；目标、写入面和验收清楚且无自然闸门时直接推进。
- `Route Contract.Allowed Action` 向下游继承已有许可；切换 owner 不重复询问。范围扩大、高风险动作或真实取舍才重新确认。
- `HIGH`：行动；`MEDIUM`：声明低风险假设后行动；`LOW`：probe/讨论；`BLOCKED`：只问不可约问题。
- 输出深度用 `SILENT / MICRO / ALIGN / FULL`，默认最短；不展示流程旁白或内部账本。
- 用户说“继续/确认/按推荐来”时承接当前路线，不重开需求发现，不在每个阶段或任务后询问是否继续。

## 讨论式意图收敛

开发、规划或高影响审查前，内部锁定结果、owning surface、非目标、约束和证据。多个合理解释会导致明显返工时使用 `One-Turn Alignment`，说明当前理解、动作、非目标和验收后请用户校准。低置信度不得带着未确认的高影响假设写入。

- agent 先给推荐，不让用户从空白重写需求。
- 一次集中提出 2-4 个彼此相关的高影响问题；每项给推荐答案、行为差异和错判影响。
- 用户可回复“按推荐”或纠错；信息足够即结束追问。
- 自然闸门仅包括：意图变化、范围扩大、不可安全恢复的失败、高风险/破坏性/权限/迁移/发布动作、冲突或真实取舍。

展示 `ALIGN/FULL` 或破坏性菜单时才读 `references/output-forms.md`。

## Owner 与组合

扫描最多 3 个候选，选择能直接产生下一证据的最具体 owner。内部 `Route Contract` 仅含：`Owner / Mode / Next Output / Allowed Action / Success Evidence / Stop Condition`；动作分 `READ / WRITE / REMOTE_WRITE / DESTRUCTIVE`。

常用路由：

- bug/失败测试：`ccdawn-bug-review`；PR/diff：`ccdawn-pr-review`；整仓/架构：`ccdawn-project-review`。
- UI/UX 与交互方向：`ccdawn-ui-design`；品牌表达或视觉语言：`ccdawn-visual-design`；契约明确后的生产前端实现：`ccdawn-frontend-engineering`；已有界面或截图审查：`ccdawn-ui-review`；跨组件 token、主题或组件治理：`ccdawn-design-system`。
- 当前 diff 过度设计：`ccdawn-simplification-review`；整仓冗余治理：`ccdawn-simplification-audit`。
- AI/ML 研究：`ccdawn-ai-research-loop`；单条 metric lane：`ccdawn-score-loop`；重要 claim：`ccdawn-research-rigor-review`。
- 已对齐任务需要自动组队、持续讨论和本地集成：`ccdawn-multi-agent-orchestration`；单次会话建议、冲突、暂停恢复或合并协商：`ccdawn-thread-coordination`；真实开发残留：`ccdawn-development-cleanup`。
- 真实设计分叉：`ccdawn-planning`；无专项 owner 的评价：`ccdawn-evaluation`。
- GitHub、浏览器、Figma、OpenAI 文档、图片和办公制品按需读 `references/capability-routing.md`。

无法仲裁才读 `references/routing-practice.md`。以本轮 Available skills 为准；未安装 skill 不能成为 owner，外部候选仅在安装/调研时读取。

多个独立交付物、owner 或验证边界才建 `Primary / Secondary / Deferred`；“实现并验证”仍是一个任务。写入可分离且收益高于协调成本才并行。

### Collaboration Discovery

意图收敛并选出功能 owner 后，BRT 主动判断现有对话能否帮助任务。`FAST_PATH`、单 owner 更快或本轮无原生 thread/list 能力时为 `NONE`；出现独立 lane、可复用上下文或专项互补时，读 `references/collaboration-discovery.md` 做一次有界发现。

结果为 `NONE / PEER_CONTEXT_REVIEW / DISPATCH_READ_ONLY / DISPATCH_DISJOINT_WRITE / COORDINATE_OVERLAP`。单次协作交 `ccdawn-thread-coordination`；两个以上正收益且可分离的 lane 升为 `TEAM_READY`，交 `ccdawn-multi-agent-orchestration`。无候选但新会话收益明确时为 `ASK_CREATE`，集中询问一次。

发现阶段不发消息、不派发、不暂停；没有正收益候选时静默回原 owner。BRT 不参与后续团队讨论或合并。

## 最小充分方案

按首个充分层级停止：`NO_BUILD -> PROJECT_REUSE -> STANDARD_NATIVE -> INSTALLED_DEPENDENCY -> MINIMAL_BUILD`。先查最窄本地复用；外部候选会改变路径、依赖、成本或风险时才用 `ccdawn-feature-reuse-research`：

- 成熟引擎/标准类复杂能力、重要新依赖、跨模块子系统，或项目内无稳定模式；
- 用户明确要求外部复用，或 QUICK 搜索可显著避免高成本自研。

文件多不是触发条件。普通 CRUD、样式、小 bug、机械改动和已有模式直接实施；结论稳定后回原 owner。

自动精简默认 `AUTO`：简单任务 `LITE`，非平凡实现 `FULL`，用户目标就是删减时 `ULTRA`。不得删除用户要求、信任边界、安全、数据保护、无障碍、兼容或迁移约束。

## 流程重量

- `FAST_PATH`：一个低风险、可逆、可本地验证的单元；`FAST_PATH` 直接执行并最小验证，不 planning、拆分或 TDD。
- `COMPACT_FLOW`：多个相关单元可在一个上下文连续完成；只有拆分会改变依赖、owner、风险或验证时，才让 `ccdawn-planning` 在同一方案内生成 `TASK_GRAPH`。
- `FULL_FLOW`：仍有真实设计分叉或状态/API/安全/数据/迁移/权限/发布风险；只生成解决这些风险所需的 artifact。

BDD/TDD 按子任务判断，只给确定性行为回归或重大契约风险；metric 未提升属于实验结果。新 worktree 只用于并行、冲突/高风险隔离或用户明确要求。

多会话 pause 会产生 `resumePendingAgentIds`；owner 只有在 coordination resolve 且恢复债务清零后结束，失活先路由 `ccdawn-thread-coordination` 接管。

长任务、恢复、跨阶段 handoff 或持久状态才读取 `references/runtime.md`；普通 `FAST_PATH/COMPACT_FLOW` 不加载。

## 能力感知与阶段折叠

高能力模型可内部完成局部规划、依赖排序和自审；同一 owner 且无自然闸门时可折叠对齐、实现和验证。

- **Skill Budget**：默认一个 primary owner；support skill 只有补充独有知识、工具或独立证据时才加载。
- artifact 只有会被审阅、交接、恢复或高风险决策复用时才生成。
- 调用下游前确认它防止的具体错误和使用者；说不清就跳过。
- 内部从 1-3 个相关视角检查需求覆盖、误改范围和验证；没有 finding 不输出矩阵。

Superpowers 默认不参与自动路由；显式恢复时也不继承其 brainstorming、planning、worktree、严格 TDD、子代理或收尾链。子代理默认 0 个；`TEAM_READY` 或独立高收益 lane 才组队。

## 执行与收口

写入前内部建立：`Target / Desired Outcome / Allowed Actions / Out of Scope / Success Evidence / Recovery Signal`。

Wrong-Edit Guard：定位 owning surface、预计文件、相关测试和已有用户/Agent 改动；只改完成契约所需范围。验证失败先区分 implementation、test intent、environment、requirement mismatch，不为过测试削弱行为。

首次写入、scope 扩大或合并前，有 registry 才运行 `preflight`。`CLEAR/PEERS_NO_OVERLAP` 继续；`OVERLAP` 进入 Silent Conflict Triage。优先缩 scope、做安全工作或等待；需共同决定时协商。只有继续写会立即覆盖/回归且无法拆分的最大冲突才暂停。无 registry 不初始化 Memory、claim 或 coordination。

当前 owner 用风险相称的新鲜证据收口。普通任务无需 `ccdawn-completion-summary`；只有跨阶段/会话、恢复、正式交接或 Deferred 风险才使用。只有已知产生临时产物、branch/worktree/claim 等真实残留时才路由 cleanup；没有候选不扫描、不汇报。

用户可见内容默认中文，保留代码、命令、路径、错误原文、API/协议、skill 名和枚举。每个阶段只给短 checkpoint；正文最后一行（Next Action）写 `下一步建议: <一个具体动作>`，只有自然闸门才给选项。
