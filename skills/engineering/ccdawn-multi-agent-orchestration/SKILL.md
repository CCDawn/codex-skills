---
name: ccdawn-multi-agent-orchestration
description: "Use when aligned project work has multiple valuable same-project Codex threads/agents or genuinely independent lanes and needs automatic team formation, bounded dispatch, evidence-driven discussion, progress recovery, dependency-aware local integration, and end-to-end verification; do not use for simple work, one-off peer advice, or a single overlap/conflict that ccdawn-thread-coordination can resolve."
license: MIT
---

# CCDawn Multi-Agent Orchestration

## 目标

把已对齐需求交给最小有效 Agent 团队，持续回收关键证据并完成本地集成。当前 Agent 是 coordinator 和集成 owner；专项 Agent 负责边界清晰的交付物。

## BRT interface

- Context Boundary: 已对齐意图、同项目候选 thread、任务边界、依赖、branch/worktree、验证和本地集成目标。
- Output Contract: team roster、成员契约、讨论决定、集成结果、验证证据和未决风险。
- Allowed Action: 读取/发送 thread 消息、使用现有 registry、派发已授权工作并在允许范围内本地集成；新建用户会话、远程 Git、发布和破坏性动作需单独授权。
- Success Evidence: 成员回执、可追踪提交或 artifact、目标分支包含已选结果、集成验证通过且协调债务清零。
- Stop Condition: 意图未对齐、没有正收益团队、owner/scope 不清、集成目标不明、高风险取舍、恢复债务或权限不足。
- Route Out: 专项任务 owner、`ccdawn-thread-coordination`、`ccdawn-pr-review`、`ccdawn-development-cleanup`、`ccdawn-brt` 或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface；用户可见内容默认中文，只报团队决定、关键 checkpoint、集成证据和风险。
- Route Out 仅以 BRT interface 为准；末行写 `下一步建议: <一个具体动作>`。
- 编排不能扩大用户意图、写入面或权限，也不能把普通任务强行拆给多个 Agent。

## 进入闸门

BRT 已完成意图对齐和有界会话发现，以 `TEAM_READY` 交接，且本轮具有可用的原生 thread read/send 能力，并满足至少一项：

- 现有 Agent 持有可直接复用的相关上下文、实现或证据；
- 有两个以上可独立交付、写入面可分离且并行能缩短关键路径的 lane；
- 不同专项视角会实质降低误改、回归或集成风险。

若单 owner 更快、任务共享同一小文件、候选忙碌/过期、拆分后合并成本不低于收益，则返回原 owner。单次建议、状态交换或冲突处理路由 `ccdawn-thread-coordination`。

## 编排循环

### 1. 建立任务真相

锁定 `Intent / Deliverables / Non-goals / Allowed Actions / Base / Integration Target / Success Evidence`。需要设计方案时先用 `ccdawn-planning` 形成一个可执行方案；不为组队额外制造 TASK_GRAPH。

### 2. 组成最小团队

优先复用同项目现有 thread。读取候选的当前任务、checkpoint、scope、branch/worktree 和 blocker，选择 2-4 个有独特贡献且可联系的成员。无合适 thread 时，只在新增会话收益明确时向用户询问一次；未授权不创建，也不停止当前可推进工作。

coordinator 保留关键路径、共享契约、集成和最终验证。每个成员只有一个明确 owner contract：`Deliverable / Scope / Dependency In / Evidence Out / Return Condition / Do Not Touch`。写入 lane 必须互不重叠；只读审查不得顺带改代码；禁止成员递归派发。

邀请前用一次 registry claim 原子占用 `lane=dispatch/<task-key>`，并同时写入 `thread/<agent-id>` 与 `task/<orchestration-id>/<deliverable>` scopes。claim 失败则不发送；拒绝或超时后释放。迟到结果必须匹配仍有效的 dispatch id，否则只作为待复核候选，不能进入 integration queue。

发送 `TEAM_INVITE` 后只把 `ACCEPTED` 的成员加入 roster；拒绝、忙碌或超时的可选成员不阻塞主线。需要具体消息结构时读取 `references/team-protocol.md`。

### 3. 事件驱动协作

成员只在契约变化、依赖就绪、发现会改变他人行动的证据、出现 blocker 或达到 `MERGE_READY` 时发送 checkpoint。coordinator 不固定频率轮询，不转发逐步思考，也不要求无变化状态。

共享接口、方案或证据产生分歧时，使用 `ccdawn-thread-coordination` 建立一个可复用 discussion；成员回复立场与证据，coordinator 收齐必要意见后形成单一决定并广播。普通重叠先缩 scope 或协商；只有无法拆分且继续写会立即覆盖/回归时才暂停。

### 4. 回收与恢复

每个结果必须包含 `Base / Head or Artifact / Changed Scope / Tests / Assumptions / Risks`。迟到结果按最新 base 重验；不能直接覆盖已集成内容。

成员失活但 lane 可替代时，先保存已有证据，再转派给空闲成员或 coordinator；不要重做已验证工作。coordination owner 失活时使用 `takeover`，并继承全部 `resumePendingAgentIds`。可选成员失败不阻断无依赖主线；关键 lane 失败才进入 BLOCKED 或返修。

### 5. 自动本地集成

按依赖顺序建立 integration queue。不要为每个小 lane 新建 worktree；复用现有 branch/worktree，只有独立写入确实需要隔离时才创建。多个写入分支存在时，优先使用一个明确的本地 integration target。

在已有 WRITE 授权内，本地集成属于任务本身，不在每个成员完成后询问是否继续。每项合入前由 coordinator 重验提交、diff、base、dirty state、scope 和聚焦测试：

- 无依赖且无共享面可以成组；有依赖或共享契约必须串行。
- 冲突先退回相关 owner 协商；coordinator 只处理边界明确的机械冲突。
- 集成操作失败使用对应的 `merge/cherry-pick/rebase --abort` 恢复，不覆盖既有未提交改动。
- 每项完成后跑窄验证；全部进入目标后跑一次集成 gate。
- 验证失败按责任 lane 返修，不让所有成员重复诊断同一问题。

不得在未授权时 push、创建/合并远程 PR、发布，或直接改受保护 `main`。本地 integration branch 验证通过后，才把远程动作交给相应 GitHub owner 或用户闸门。

## 完成门

只有以下全部成立才结束：关键 deliverable 已集成；目标分支包含选定提交；集成验证通过或有明确允许的条件证据；open coordination 和恢复债务清零；没有无人接管的失败 lane。

只在已知产生临时 branch/worktree/claim 时路由 `ccdawn-development-cleanup`。普通结束不生成额外总结 skill；跨会话正式交接才使用 `ccdawn-completion-summary`。
