---
name: ccdawn-dawn-agent-html-memory
description: Use when the user or project rules explicitly request project-local memory/dashboard initialization or updates, or when an existing `.docs/project-memory/` is needed for cross-session recovery, durable decisions, blockers, parallel-agent coordination, or formal handoff; do not auto-initialize or sync it for ordinary development.
license: MIT
---

# Agent HTML Memory

## 目标

按需维护仓库内 `.docs/project-memory/` 和 HTML 总览，并为同项目 Agent 提供不入 Git 的实时 coordination registry。实时状态用于协作，持久记忆只保存会改变未来行动的决策与 checkpoint。

## BRT interface

- Context Boundary: 目标仓库、live coordination registry、现有 `.docs/project-memory/`、项目规则、Agent/claim/coordination 状态和需要持久化的事实。
- Output Contract: 紧凑 Agent 状态，或已初始化/更新的结构化 memory、索引和含协作视图的 HTML dashboard。
- Allowed Action: 默认只读；写入时限于 `.docs/project-memory/`、根目录 `PROJECT_MEMORY.html`，初始化时可按明确授权更新 `AGENTS.md` memory block。
- Success Evidence: 目标事实出现在对应 lane/JSON，并由 renderer 同步到 `INDEX.md`、`overview.html` 和适用的 `PROJECT_MEMORY.html`。
- Stop Condition: 未满足激活闸门、项目根目录不明、memory 格式损坏、真实重叠 claim、renderer 失败，或写入会覆盖未理解的用户内容。
- Route Out: 完成后返回当前 owner；正式跨阶段交接可转 `ccdawn-completion-summary`；阻塞则回 `ccdawn-brt`。

## 激活闸门

只有以下情况之一成立才加载或执行本 skill：

- 用户明确要求初始化、查看、更新、同步、渲染或修复项目 memory/dashboard。
- 项目规则明确要求在当前任务读取或同步 `.docs/project-memory/`。
- 仓库已存在该目录，且其中的跨会话状态、关键决策、blocker 或 lane ownership 会改变当前判断。
- 当前任务需要把重要结果持久化给未来会话、并行 agent 或正式交接，且聊天上下文和普通文档不足以承载。
- 同项目存在多个 Agent，或 live coordination registry 已存在且会改变 ownership、冲突、讨论或合并判断。

普通实现、机械小改、一次性审查、简单问答和单会话可闭环任务默认不触发。目录不存在时，不因为“这是软件项目”而主动初始化；先有用户授权或项目规则。

## 工作模式

- `READ`：只读取 `INDEX.md`、`profile.json` 和会改变判断的 lane；不要无差别加载全部 JSON/历史。
- `INIT`：仅在明确授权后初始化目录、profile、索引与 dashboard。是否注入 `AGENTS.md` 必须遵循用户选择或项目规则。
- `SYNC`：只写本轮的 durable delta，例如决策、blocker、lane 状态、可复用技术事实或正式下一步；不记录完整对话和过程旁白。
- `GUARD`：仅在确有并行 agent/session、活跃 claim 或项目强制规则时检查/认领；单 agent 普通工作不创建 claim。
- `LIVE`：第二个同项目 Agent 出现后注册任务、scope、branch 和 checkpoint；只在状态变化时更新，不持续同步对话或命令。

能用 `READ` 回答就不 `SYNC`，能更新一个 lane 就不重写全局历史。不要把 memory sync 当成所有任务的 definition of done。

## 管理范围

```text
.docs/project-memory/
  memory.json
  profile.json
  overview.html
  INDEX.md
  inbox.json
  lanes/
  archive/
  agent-claims.json  # 可选，仅并行协调
PROJECT_MEMORY.html
```

Live registry 位于 `<git-common-dir>/ccdawn/coordination/registry.json`；非 Git 项目回退到 `~/.codex/project-coordination/<project-id>/registry.json`。它跨 worktree 共享但不进入 Git，保存 thread 映射、Agent 状态、claim 和当前 coordination；dashboard 只渲染脱敏投影。

- `memory.json`：项目元数据、lane 索引和精简的 `recentUpdates`。
- `profile.json`：项目类型、dashboard preset、视觉模式和展示密度。
- `lanes/*.json`：按稳定职责或子系统保存状态、决策、问题和下一步。
- `inbox.json`：尚未归类但确有后续价值的临时事实；保持很小。
- `archive/`：从 active state 移出的历史，不用于堆积本轮过程。
- `overview.html`、`INDEX.md`、`PROJECT_MEMORY.html`：由脚本生成或刷新，不作为随意手改的事实源。

不得存储 secrets、token、个人关系信息、通用知识或完整聊天记录。仓库已有其他 memory surface 时，遵循现有 authority，不擅自迁移或建立双轨。

## 初始化

首次初始化时读取 `references/setup.md`，再运行：

```powershell
py -3 <skill-root>\scripts\init_project_memory.py <project-root> --project-type <type> --dashboard-preset <preset> --skip-agents-rules
```

选择最接近的 `frontend`、`backend`、`automation`、`research` 或 `general`，避免为分类反复追问。初始化后确认 JSON、lane/archive 目录、索引和 HTML 文件存在；只有用户或项目规则明确需要持续规则时，才去掉 `--skip-agents-rules` 并注入 `references/AGENTS-snippet.md`。

## 读取与同步

同步前只读取当前 lane、`profile.json` 和必要的 shared metadata。记录内容必须是未来会话会据此改变行动的事实：

- 已验证的模块状态或 milestone
- 行为/架构决策及其影响
- 未解决 blocker、证据和下一步
- 跨会话继续所需的技术事实
- 正式 handoff 的 owner、范围和验证状态

优先保留旧历史，只追加或更新本轮拥有的条目。同步命令：

```powershell
py -3 <skill-root>\scripts\sync_project_memory.py <project-root> --lane <lane> --focus "<current focus>" --update "<durable delta>"
py -3 <skill-root>\scripts\capture_note.py <project-root> --lane <lane> --title "<title>" --details "<fact>"
py -3 <skill-root>\scripts\render_overview.py <project-root>
```

`capture_note.py` 只用于尚需调查的高价值线索，不把每个观察都写入 inbox。

## 并行协作

只有存在真实并行或 registry 已存在时使用 `scripts/agent_coordination.py`：

```powershell
py -3 <skill-root>\scripts\agent_coordination.py <project-root> status
py -3 <skill-root>\scripts\agent_coordination.py <project-root> join --agent <label> --agent-id <id> --task "<task>" --scope <scope>
py -3 <skill-root>\scripts\agent_coordination.py <project-root> update --agent-id <id> --stage <stage> --last-checkpoint "<evidence>"
py -3 <skill-root>\scripts\agent_coordination.py <project-root> claim --lane <lane> --scope <scope> --agent-id <id> --task "<task>"
```

`agent_work_guard.py` 保留为兼容入口。只认领最小稳定 scope；暂停会让出 claim，恢复必须重新检查。每次工具调用使用文件锁、revision 和原子替换，旧 `.docs/project-memory/agent-claims.json` 只迁移读取，不删除。

已解决的讨论、冲突或 merge 决策由协调者同步一次：

```powershell
py -3 <skill-root>\scripts\sync_project_memory.py <project-root> --lane <lane> --coordination-id <id>
py -3 <skill-root>\scripts\sync_project_memory.py <project-root> --lane <lane> --agent-id <id>
```

并行 worker 不直接同步 tracked memory；它只发布 live checkpoint，由协调者归并 durable delta。

## 验证

写入后运行 renderer，并检查：

1. durable delta 出现在正确 lane 和 `recentUpdates`（需要全局记录时）。
2. `INDEX.md` 的计数和链接一致。
3. `overview.html` 与根目录入口可打开，最新状态归属正确。
4. 没有覆盖无关 lane、旧历史或用户并行改动。

渲染或结构异常时读取 `references/troubleshooting.md`；只在用户要求调整 dashboard 视觉时读取 `references/html-design.md`。

用户可见输出默认中文，正文末尾保留：`下一步建议: <一个具体动作>`。
