---
name: ccdawn-thread-coordination
description: "Use when multiple Codex App threads or agents work in the same project and need proactive collaboration discovery or bounded dispatch, shared progress awareness, ownership arbitration, conflict pause/resume, discussion, merge coordination, status exchange, or handoff through native thread tools without heavyweight orchestration."
license: MIT
---

# CCDawn Thread Coordination

## 目标

用 registry 和 thread 消息协调派发、scope、冲突和合并。代码/Git 是实现事实源；无高收益不触发。

## BRT interface

- Context Boundary: 项目、Agent/thread、branch/worktree、scope、claim、coordination 和目标分支。
- Output Contract: ownership、协调决定、验证和恢复债务。
- Allowed Action: 使用 `read_thread`、`send_message_to_thread` 与 `agent_coordination.py`；创建/归档或远程 Git 需授权。
- Success Evidence: registry revision、thread 回执、Git/测试及协调闭环。
- Stop Condition: thread 不明、owner 争议、暂停未确认、状态漂移或动作未授权。
- Route Out: 原 owner、`ccdawn-pr-review`、`ccdawn-development-cleanup`、`ccdawn-dawn-agent-html-memory`、`ccdawn-brt` 或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface；不匹配时回 `ccdawn-brt` 或具体 owner。
- 用户可见内容默认中文；只报产出、证据和风险；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## 接入与所有权

BRT 首次写入前调用 `preflight`；`CLEAR/PEERS_NO_OVERLAP` 返回原 owner。`OVERLAP` 先静默分诊；只 claim 最小 scope，仅在状态转换时 `update`。

owner 顺序：用户指定 > 有效 claim/registry > 更早 owner。非 owner 停止自身冲突写入，不要求既有 owner 暂停；争议面只读。

## 主动协作

发现已有会话，只向相关空闲 Agent 派发独立 lane。发送前一次 claim `thread/<agent-id>` 与 `dispatch/<task-key>`；写入再含实际 scope。消息给出 `Task / Why / Scope / Allowed Action / Expected Output / Verification / Dependency / Return Condition`，禁止递归派发。

owner 保留关键路径与集成。结果、拒绝或超时后释放 claim；超时标 stale，迟到结果先复核。可选协作不 BLOCKED。简单任务、同文件或忙碌 Agent 不派发。

无合适会话且新会话有明确收益时，说明边界和收益，向用户询问是否创建；未授权不创建，也不得因此停止当前可推进工作。

## 冲突恢复

Silent Conflict Triage 核验 claim 新鲜度、真实写入、owner、关键路径和替代工作。优先 `SELF_NARROWED / CONTINUE_NON_CONFLICTING / WAIT_SILENTLY`，不建 coordination、不发消息。

有效 owner 的真实写冲突阻塞关键路径、无法绕开且需其暂停/交接/决定时才为 `MESSAGE_REQUIRED`。同一 participants + surface 的 open coordination 存在则复用，不重复发送；否则 `open --kind conflict` 并发送一次 `CONFLICT_PAUSE_REQUEST`。`PAUSE_REQUEST` 不等于 `PAUSED`，确认前不写冲突面。

修复后 `resolve` 并主动发送 `CONFLICT_RESOLVED`；对方重读状态，执行 `resume` 后回复 `RESUMED`。`resume` 关闭已清债 coordination；不要随后调用 registry `respond --status RESUMED`。

`send_message_to_thread` 不能中断系统命令；消息不是抢占机制。

pause 产生 `resumePendingAgentIds`；债务清零才能 `complete`：

- `open` 默认 30 分钟租约；跨 checkpoint 用 `heartbeat`，不高频轮询。
- `status` 标记 `owner-stale`；注册 Agent 用 `takeover` 并继承恢复义务。健康 owner 仅由用户改派。
- 任务明确取消/归档才可 `cancel-resume --confirmed-by-user`；无回复不等于取消，不得自行设置确认标记。

## 讨论与合并

讨论用 fan-out/fan-in：`DISCUSSION_REQUEST` 发同一问题，各给一次 position，coordinator `resolve` 并广播。

合并返回 `MERGE_READY`（branch/base/head/dirty/scopes/dependency/tests/risks）。coordinator 用 Git 重验；无重叠可成组，共享面串行。逐分支窄验证，集成后完整 gate；失败退回，成功广播。不自动 push、发布或清理。

### 条件合入快线

hook/gate 失败先分为 `CHANGE_FAILURE / BASELINE_FAILURE / ENVIRONMENT_FAILURE / POLICY_FAILURE / UNKNOWN`。窄验证通过、diff 可审、失败已在干净 base 复现或证实与 diff 无关，且不涉及安全、secret、权限、迁移、发布合规或强制 gate，才标记 `MERGE_READY_CONDITIONAL`。

- 环境修复只做一次 2-5 分钟 probe；无新证据即停止。
- 优先跳过单个已证明无关的 hook（如 `SKIP=<hook-id>`）；`--no-verify` 仅在项目策略或用户明确允许时使用，并记录 hook、失败、base 证据和补验责任。
- 条件提交不等于通过；integration owner 补跑 gate/CI 后才广播。
- 无法提交但 diff 已保留时，交给 integration owner 应用；不得无人接管。

影响未来行动的决定才执行 `sync_project_memory.py --coordination-id <id>`；并行 worker 不写 tracked memory。

## 完成

未收到 `PAUSED` 为 BLOCKED；已修复未恢复为 PARTIAL；送达未恢复为 `DELIVERED_AWAITING_RESUME`。`RESUMED` 或取消后闭环；merge 需目标分支含预期提交且验证通过。
