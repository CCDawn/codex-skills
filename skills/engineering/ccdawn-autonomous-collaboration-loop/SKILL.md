---
name: ccdawn-autonomous-collaboration-loop
description: "Use when the user explicitly enables an automated same-project multi-thread development loop that keeps peer Codex tasks progressing, recovers conflicts or stale coordination, integrates verified work into local main, and closes cleanup without repeated gates; do not use before opt-in, for one-off coordination, remote publication without permission, or subagent creation."
license: MIT
---

# CCDawn 自动协作开发闭环

## 目标

用户确认一次后，驱动同项目平级会话完成各自任务、恢复冲突、验证并合入本地 `main`。不创建主从团队或接管其他任务。

## BRT interface

- Context Boundary: 已对齐的共同目标、用户一次性授权、现有同项目 thread、各自任务/branch/worktree/scope、共享契约、目标 `main` 和验证门。
- Output Contract: collaboration agreement、可接管状态、各任务交付证据、integration queue、本地 `main` 验证、恢复与清理闭环。
- Allowed Action: 在授权范围内读取/发送 thread 消息、维护 registry、执行本地写入/提交/合入 `main`、验证和安全清理；新建会话、远程 push/PR merge/发布、破坏性或高风险动作仍需单独授权。
- Success Evidence: 每个原任务达到验收，目标 `main` 包含预期交付，集成门通过，open coordination、恢复债务和已知开发残留清零。
- Stop Condition: 未获开启确认、共同目标或 target 不明、产品/安全/数据迁移取舍未决、需要远程授权、破坏性动作，或自动恢复连续失败。
- Route Out: 各 Agent 原 owner、`ccdawn-multi-agent-orchestration`、`ccdawn-thread-coordination`、`ccdawn-pr-review`、`ccdawn-development-cleanup`、`ccdawn-dawn-agent-html-memory`、`ccdawn-brt` 或 BLOCKED。

## 统一调用契约

- 用户可见内容默认中文；只报行动决定、blocker 和最终证据。Route Out 仅以 BRT interface 为准；末行写 `下一步建议: <一个具体动作>`。
- 各 Agent 保留自己的任务、scope、branch 和完成责任；Loop Owner 只维护闭环，不成为其他任务的 owner。
- 开启后不在每个阶段、task、普通冲突或恢复动作后询问是否继续。

## 开启与授权

BRT 仅在非简单目标确有两个以上会话协作价值时询问一次：“是否开启自动化协作开发闭环？”用户确认后，本次共同目标获得持续授权，直到完成、取消或触发自然闸门。

持续授权包括联系现有会话、协商边界、安全开发、本地提交、按序合入本地 `main`、验证和安全清理。拒绝时回原 owner。

没有合适现有会话时，说明收益和任务边界后只询问一次是否创建新会话。远程 push、创建或合并 PR、发布、force/破坏性操作不继承本授权。

## 角色与持久状态

- `Loop Owner`：维护状态、租约、待发送 outbox、恢复债务和完成门；不替 peer 写任务结论。
- `Peer Owner`：完成自己的原任务，提供 scope、依赖和 `MERGE_READY` 证据。
- `Integration Owner`：按依赖顺序重验并合入本地 `main`，失败回送责任 owner。
- `Recovery Dispatcher`：任何活跃参与者在 Loop Owner 租约过期时可 `takeover`，继承 outbox、恢复和集成义务，但不能继承或伪造 peer 的完成声明。

状态只保留会改变后续动作的最小事实：

```text
DISCOVER -> AGREEMENT -> RUNNING -> NEGOTIATING
         -> MERGE_READY -> INTEGRATING -> INTEGRATED -> CLOSED
```

每个 peer 记录 `Task / Scope / Branch or Worktree / Dependency / Checkpoint / Tests / Blocker / Resume Debt`。有现成 registry 时使用它；跨会话恢复确有需要时由 `ccdawn-dawn-agent-html-memory` 提供状态载体，但 memory 不是执行 owner。

## 自动循环

### 1. 发现与约定

只读最多 3 个最相关的同项目现有 thread。确认双向收益、写入边界、共享契约、依赖和 Integration Owner；用 `ccdawn-multi-agent-orchestration` 建立 peer agreement。无正收益候选则结束自动编排，当前 owner 继续。

### 2. 并行推进

各 peer 继续自己的非冲突任务。只在共享契约变化、依赖就绪、可行动证据、纠错、blocker 或 `MERGE_READY` 时通信；不轮询式催促，不发送无变化进度。

消息默认只发差量：`From/Task / Changed Fact / Action Impact / Evidence Pointer / Reply Needed`。不重复背景、完整方案、测试清单或未变化字段；优先使用文件、commit、测试和消息指针。仅首次共享契约或安全关键语义展开。

### 3. 冲突协商

普通重叠先缩 scope、调整顺序、交换接口建议或继续安全面，由 `ccdawn-thread-coordination` 复用一个 discussion。双方保持开发，不向用户升级。

只有继续写会立即覆盖或回归且无法拆分时，暂停冲突 surface，不暂停整个任务。记录 `resumePendingAgentIds`；解决后主动发送 `CONFLICT_RESOLVED`，由当前 Loop Owner 或接管者确认对方恢复。发起者完成或退出不取消恢复义务。

### 4. 故障与接管

`send_message_to_thread` 不是硬中断，消息可能延迟到对方下个 checkpoint。Loop Owner 必须维护租约和幂等 outbox；租约失活时，任一活跃参与者执行 `takeover` 后继续，不依赖原发起会话重新出现。

自动恢复先分类为任务失败、依赖失败、集成失败或环境失败；把可行动证据发给责任 owner，其他 peer 继续安全工作。只有产品取舍、权限/安全/迁移风险，或同一 blocker 经两轮不同恢复策略仍失败，才询问用户。

接管者只继承推进义务，不能继承证据所有权。失活 peer 没有正式 `MERGE_READY` 时：

- Git commit/artifact、scope 和新鲜验证足以独立重验：接管者可标记 `MERGE_READY_RECOVERED`，必须注明原 owner 未确认及重验证据。
- 只有聊天中的采纳、计划、进度或草稿：标记 `RECOVERY_PENDING_EVIDENCE`；接管者自行完成缺口或恢复原 owner，不能代其宣告完成。
- 无法安全完成且两轮恢复失败：保持明确 owner/blocker 后再询问用户，不把缺证据项目合入。

### 5. 集成队列

每个 peer 用 `MERGE_READY` 提交 `Base / Head or Artifact / Changed Scope / Tests / Dependencies / Risks`。`MERGE_READY_RECOVERED` 也必须满足相同证据门。Integration Owner 以 Git 和新鲜测试为事实源：

1. 无依赖且不重叠的交付可成组；共享契约或依赖项串行。
2. 每项合入前重验窄测试和 scope；机械冲突可自动解决，语义冲突回相关 peer 讨论。
3. 合入本地 `main` 后运行一次集成 gate；失败只重开责任任务和受影响依赖。
4. 不用远程 CI 替代本地证据，也不在未授权时 push 或操作远程 PR。

可重建的 ignored/untracked 测试缓存不阻塞 `MERGE_READY`，统一留给 final cleanup；删除受阻且不影响 tracked 交付时保留，不更换多种命令追查。

### 6. 收尾

全部原任务验收、本地 `main` 含目标交付、集成 gate 通过、open coordination 与恢复债务清零后，调用 `ccdawn-development-cleanup` 清理本轮可证明安全的 claim、已吸收本地 branch/worktree 和临时噪音。最后只做一次整体汇报。

## 完成门

以下条件必须同时成立：

- 每个 peer 的原任务已完成或由用户明确取消；“消息已发送”“已采纳”“接近完成”和恢复生成的总结都不能代替交付证据；
- 本地 `main` 包含所有预期交付且集成验证通过；
- 没有未处理 outbox、open coordination、stale owner 或 `resumePendingAgentIds`；
- 清理没有删除未合并工作，远程动作仍保持未执行；
- 失败和 Deferred 项有明确 owner、证据和触发条件。

未满足时由当前 Loop Owner 或接管者继续闭环，不把普通协调债务抛回用户。
