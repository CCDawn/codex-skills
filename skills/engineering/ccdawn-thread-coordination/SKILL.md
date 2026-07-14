---
name: ccdawn-thread-coordination
description: "Use when multiple Codex App threads or agents work in the same project and need shared progress awareness, ownership arbitration, conflict pause/resume, bounded discussion, merge coordination, status exchange, or handoff through native thread tools without heavyweight orchestration."
license: MIT
---

# CCDawn Thread Coordination

## 目标

协调同一项目里的多个 Codex 会话：让 Agent 知道彼此任务、scope、阶段和 blocker，并通过紧凑消息讨论、暂停、恢复或快速合并。

代码/Git 是实现事实源，live registry 是协作事实源，`.docs/project-memory` 只存持久决策；thread 消息负责传输。普通单会话任务不触发，也不自动创建 worktree、子任务或轮询。

## BRT interface

- Context Boundary: 项目、Agent/thread、branch/worktree、任务、scope、checkpoint、claim、coordination、允许动作和目标分支。
- Output Contract: 当前 Agent 状态、owner/冲突判定、讨论决策或 merge order、消息送达状态、验证与剩余风险。
- Allowed Action: 使用 `list_threads`、`read_thread`、`send_message_to_thread` 和 `agent_coordination.py` 读取、注册、通知与更新协作状态；创建/fork/handoff/归档会话及远程 Git 动作仍需对应授权。
- Success Evidence: registry revision 更新，目标 thread 已核对；暂停有 `PAUSED`，讨论有统一 `DECISION`，合并有 Git/测试证据，恢复消息由 `read_thread` 确认送达。
- Stop Condition: 目标 thread 不明、工具不可用、owner 有争议、暂停未确认、registry/Git 状态漂移、破坏性或远程动作未授权。
- Route Out: 原任务 owner、`ccdawn-pr-review`、`ccdawn-development-cleanup`、`ccdawn-dawn-agent-html-memory`、`ccdawn-brt` 或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface 范围；不匹配时回 `ccdawn-brt` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## LIVE 接入

当第二个同项目 Agent 出现，或 coordination registry 已存在时：

1. 用 `list_threads`/`read_thread` 核对会话与任务，运行 `agent_coordination.py <project-root> status`，再用 `join` 注册 Agent、branch、scope 和任务。
2. 取得最小 claim 后执行；只在 checkpoint、blocker、暂停/恢复、merge-ready 和完成时 `update`。
3. 恢复、扩大 scope 或合并前重读状态；不广播完整对话、日志或思考过程。

工具未暴露时先按准确工具名发现能力；仍不可用则报告 BLOCKED，不伪造通信。raw thread id 只存于不入 Git 的本地 registry，不写 tracked 文件或 dashboard。

## 所有权与冲突

唯一临时 owner 顺序：用户明确指定 > 有效 claim/registry > 已拥有该模块且更早写入的 Agent。仍无法判定时，冲突面保持只读并回 BRT 裁决。

冲突握手：

1. 用 registry `open --kind conflict` 建立 `Coordination ID`、重叠范围、owner 和恢复条件。
2. 发送 `CONFLICT_PAUSE_REQUEST`，要求对方完成当前原子操作后停止新重叠写入。
3. `PAUSE_REQUEST` 不等于 `PAUSED`；用 `read_thread` 获得明确 checkpoint 回执后，再用 registry `pause` 让出 claim。此前 owner 不写冲突面。
4. owner 只处理声明范围并验证，然后 `resolve`，主动发送 `CONFLICT_RESOLVED`。
5. 对方重读 registry、Git、claim 和相关文件；`resume` 会重新检查重叠，通过后回复 `RESUMED`，否则 `BLOCKED`。

`send_message_to_thread` 不能强制中断正在运行的系统命令；无法获得安全 checkpoint 时保持只读。

### Owner 连续性与恢复债务

一次成功 `pause` 会产生恢复债务。`resolve` 只表示冲突决策完成，不表示协调闭环；registry 的 `resumePendingAgentIds` 清零后才可完成 owner 任务。

- `open` 默认给 owner 30 分钟租约；跨越 checkpoint 时执行 `heartbeat`，不高频轮询。
- owner 不得在 coordination 仍为 open 或存在恢复债务时调用 `complete`、给出完成结论或结束任务。
- `status` 发现 owner 过期、stale 或 completed 时标为 `owner-stale`；已注册 Agent 用 `takeover` 接管。健康 owner 仅在用户明确改派时允许 `--force`。
- 接管者继承原 owner 的范围、验证和恢复义务，不重新暂停一次，也不把协调问题扩成新开发任务。
- 修复后 `resolve` 并向 pending Agent 发送 `CONFLICT_RESOLVED`；对方 `resume`、回复 `RESUMED` 后清除债务。
- 被暂停任务只有经用户明确取消或已归档时才能用 `cancel-resume` 清除债务，并记录原因；不能把“对方没回复”当作取消。

## 讨论收敛

需要评估方案、接口或合并顺序时，协调者用 `open --kind discussion` 和 `DISCUSSION_REQUEST` 发同一问题与证据要求；参与者各回复一次 `DISCUSSION_POSITION`，协调者 `respond` 收集、`resolve` 一个 `DECISION` 并广播。默认 fan-out/fan-in；仅最终决策进入 memory，新证据改变结论才追加一轮。

## 快速合并

协调者建立 `open --kind merge`，参与者返回 `MERGE_READY`：`branch / base / head / dirty state / scopes / changed files / dependency / tests / risks`。

- 用 Git 重验 target、merge-base、diff 和工作区；无重叠依赖可成组集成，共享 contract、迁移或文件按依赖串行。
- 发布 `MERGE_ORDER`：owner、顺序、逐步验证、失败恢复和最终 gate；target 变化则重算。
- 风险分支逐个窄验证，全部集成后运行完整 gate；失败发 `REWORK_REQUEST`，成功发 `MERGE_ACCEPTED`。
- 不自动 push、发布、删除 branch/worktree 或绕过 `ccdawn-pr-review` 的高风险合并门槛。

## 记忆同步

并行 worker 只写 live registry。协调者在讨论/冲突/merge 解决后，用 `sync_project_memory.py --coordination-id <id>` 写一次 durable decision；长期 blocker 可按 Agent 写 checkpoint。dashboard 只读脱敏投影。

## 完成门槛

- 只发暂停请求但没有 `PAUSED`：BLOCKED。
- 已完成冲突修改但未主动发送恢复通知：PARTIAL。
- 恢复通知送达、尚无回执：`DELIVERED_AWAITING_RESUME`。
- 收到 `RESUMED`，或目标任务被明确取消/归档：协调闭环完成。
- owner 中途停止且未接管：`BLOCKED_OWNER_STALE`，不能把双方任务标记完成。
- merge 只有目标分支包含预期提交、验证通过且所有参与者收到结果后才完成。
