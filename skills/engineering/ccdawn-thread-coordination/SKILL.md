---
name: ccdawn-thread-coordination
description: "Use when multiple Codex App threads or agents are working in the same project and need conflict detection, ownership arbitration, cooperative pause, reliable resume, status exchange, or handoff through native thread tools without adding heavyweight orchestration."
license: MIT
---

# CCDawn Thread Coordination

## 目标

协调同一项目里的多个 Codex 会话。发现文件、模块、分支、运行环境或任务范围冲突时，先让非 owner 会话安全暂停；冲突解除后，由处理冲突的会话主动通知恢复。

这是轻量协调协议，不是通用多 agent 调度器。普通单会话任务不触发；不因协调自动创建 worktree、子任务、轮询或项目记忆。

## BRT interface

- Context Boundary: 当前项目、相关会话、冲突面、已有 owner/claim、各会话状态、允许动作和恢复条件。
- Output Contract: owner 判定、暂停请求及回执、冲突处理证据、恢复通知及送达状态、未解决风险。
- Allowed Action: 使用 `list_threads`、`read_thread` 和 `send_message_to_thread` 查找、读取和通知现有会话；只有用户明确要求时才创建、fork、handoff、归档会话或修改协调文件。
- Success Evidence: 目标会话身份已确认，暂停请求有 `PAUSED` 回执，冲突变更已验证，`CONFLICT_RESOLVED` 已发送并由 `read_thread` 确认送达；需要完整恢复时还应有 `RESUMED` 回执。
- Stop Condition: 目标会话无法确认、原生 thread 工具不可用、owner 仍有争议、暂停未确认、冲突需要破坏性动作，或恢复后的代码状态无法安全继续。
- Route Out: 原任务 owner、`ccdawn-brt`、`ccdawn-dawn-agent-html-memory`（仅现有项目记忆或用户明确要求持久协调时）或 BLOCKED。

用户可见输出默认中文；协议状态、代码、命令、路径和 thread 工具名保留英文。正文末尾给一个具体的 `下一步建议`。

## 所有权判定

按顺序选择唯一临时 owner：用户明确指定 > 有效 claim/项目 registry > 已经拥有该模块且更早开始写入的会话。仍无法判定时，不抢占；保持冲突面只读并回到 BRT 请求一次裁决。

工具未暴露时先按准确工具名发现能力；仍不可用则报告 BLOCKED，不伪造通信。用 `list_threads` 和 `read_thread` 核对目标会话、项目、分支/worktree、任务和最新状态。不要凭标题猜 thread，不把 raw thread id 写入受版本控制文件。

## 冲突握手

1. 生成简短 `Coordination ID`，说明冲突证据、重叠范围、临时 owner 和恢复条件。
2. 向需要暂停的会话发送 `CONFLICT_PAUSE_REQUEST`，要求它完成当前原子操作后停止新的重叠写入，并返回安全 checkpoint。
3. 用 `read_thread` 检查回执。`PAUSE_REQUEST` 不等于 `PAUSED`；收到明确回执前，owner 不得开始会覆盖对方工作的冲突写入。
4. 被暂停会话回复 `PAUSED`，包含当前状态、已改文件、未提交 diff/commit、已运行验证和恢复前必须知道的风险。
5. owner 只处理已声明的冲突面，完成后运行新鲜验证。
6. owner 主动发送 `CONFLICT_RESOLVED`，包含变更摘要、文件/commit、最新事实源、恢复前动作和剩余风险，再用 `read_thread` 确认消息成为对方的新 turn。
7. 被暂停会话重新读取 git/claim/相关文件，避免基于旧上下文继续；可安全继续时回复 `RESUMED`，否则回复 `BLOCKED` 和最小缺口。

暂停是协作式的：`send_message_to_thread` 不能保证中断正在执行的系统命令。紧急冲突也必须等待安全 checkpoint；无法获得回执时保持冲突面只读并报告 BLOCKED。

## 消息契约

```text
CONFLICT_PAUSE_REQUEST
- Coordination ID:
- Project / Surface:
- Conflict Evidence:
- Temporary Owner:
- Requested Checkpoint:
- Resume Condition:
- Reply With: PAUSED + state/diff/commit/tests/risks

CONFLICT_RESOLVED
- Coordination ID:
- Result / Verification:
- Changed Files / Commit:
- Current Source of Truth:
- Resume Actions:
- Residual Risks:
- Reply With: RESUMED or BLOCKED + reason
```

只发送增量上下文，不复制完整对话。默认不持续轮询；一次发送和一次定向回读足够，只有用户明确需要后台监督时才建立自动检查。

## 完成门槛

只完成冲突修改、没有主动发送恢复通知，协调任务仍是 `PARTIAL`。恢复通知已确认送达但对方尚未执行时，明确报告 `DELIVERED_AWAITING_RESUME`；只有收到 `RESUMED`，或目标任务已被用户明确取消/归档，才能报告协调闭环完成。
