---
name: ccdawn-thread-coordination
description: "Use when multiple Codex App threads or agents work in the same project and need shared progress awareness, ownership arbitration, conflict pause/resume, bounded discussion, merge coordination, status exchange, or handoff through native thread tools without heavyweight orchestration."
license: MIT
---

# CCDawn Thread Coordination

## 目标

用 live registry 和原生 thread 消息协调同项目 Agent 的 scope、checkpoint、冲突、讨论和合并。代码/Git 是实现事实源，registry 是协作事实源；普通单会话不触发，也不自动创建 worktree、子任务或轮询。

## BRT interface

- Context Boundary: 项目、Agent/thread、branch/worktree、任务、scope、claim、coordination 和目标分支。
- Output Contract: ownership、冲突/讨论/合并决定、消息状态、验证和恢复债务。
- Allowed Action: 使用 `list_threads`、`read_thread`、`send_message_to_thread` 与 `agent_coordination.py`；创建/归档 thread 和远程 Git 仍需授权。
- Success Evidence: registry revision、目标 thread 回执、Git/测试证据，以及 pause/resume 或 merge 闭环。
- Stop Condition: thread 不明、owner 有争议、暂停未确认、状态漂移、工具不可用或高风险动作未授权。
- Route Out: 原 owner、`ccdawn-pr-review`、`ccdawn-development-cleanup`、`ccdawn-dawn-agent-html-memory`、`ccdawn-brt` 或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface 范围；不匹配时回 `ccdawn-brt` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文；保留技术字面量；只报产出、证据与风险；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## 接入与所有权

先用 `list_threads`/`read_thread` 核对真实 thread，再运行 registry `status` 和 `join`。只 claim 最小稳定 scope；仅在 checkpoint、blocker、pause/resume、merge-ready 和完成时 `update`，不广播完整对话或日志。

owner 顺序：用户明确指定 > 有效 claim/registry > 更早拥有该模块的 Agent。仍有争议时冲突面只读并回 BRT。

## 冲突恢复

1. owner 用 `open --kind conflict` 建立 coordination、重叠面和恢复条件。
2. 发送 `CONFLICT_PAUSE_REQUEST`；`PAUSE_REQUEST` 不等于 `PAUSED`。对方到安全 checkpoint 后回复，registry `pause` 才让出 claim。
3. owner 只处理声明范围并验证，随后 `resolve`，主动发送 `CONFLICT_RESOLVED`。
4. 对方重读 registry/Git/claim，执行 `resume` 重新检查重叠，成功回复 `RESUMED`。

`send_message_to_thread` 不能强制中断系统命令；未收到 `PAUSED` 前 owner 不写冲突面。

pause 会产生 `resumePendingAgentIds` 恢复债务。`resolve` 不是闭环，债务清零后 owner 才能 `complete`：

- `open` 默认 30 分钟 owner 租约；跨 checkpoint 用 `heartbeat`，不高频轮询。
- `status` 将过期/stale/completed owner 标为 `owner-stale`；注册 Agent 用 `takeover` 接管并继承修复与恢复义务。健康 owner 仅在用户明确改派时允许 force。
- 任务明确取消/归档才可 `cancel-resume`；无回复不等于取消。

## 讨论与合并

讨论采用 coordinator fan-out/fan-in：`DISCUSSION_REQUEST` 发同一问题，参与者各给一次 position，coordinator `resolve` 一个决定并广播；只持久化最终决定。

合并时参与者返回 `MERGE_READY`（branch/base/head/dirty/scopes/dependency/tests/risks）。coordinator 用 Git 重验后发布顺序：无重叠依赖可成组，共享 contract/文件按依赖串行；逐分支窄验证，集成后完整 gate。失败回 owner，成功广播结果。不自动 push、发布或删除 branch/worktree。

已解决且会影响未来行动的决定，协调者才执行 `sync_project_memory.py --coordination-id <id>`；并行 worker 不写 tracked memory。

## 完成门槛

- 未收到 `PAUSED`：BLOCKED；已修复但未发恢复消息：PARTIAL。
- 消息送达未收到恢复：`DELIVERED_AWAITING_RESUME`。
- `RESUMED` 或明确取消/归档后闭环；owner stale 且未接管保持 BLOCKED。
- merge 需目标分支包含预期提交、验证通过且参与者已收到结果。
