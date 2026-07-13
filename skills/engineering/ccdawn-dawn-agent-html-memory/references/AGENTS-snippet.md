# Project Memory Rules

仅在用户或仓库维护者明确选择项目 memory 后，才把下面的 block 加入目标仓库 `AGENTS.md`。它让 agent 在确有跨会话价值时使用 memory，不要求每个任务读写或创建 claim。

```md
## Project Memory Rules

- `.docs/project-memory/` 是跨会话项目状态的辅助事实面；只在其内容会改变当前判断，或需要持久化决策、blocker、handoff 时读取或更新。
- 读取时先看 `.docs/project-memory/INDEX.md` 和当前职责相关 lane；不要默认加载全部历史。
- 普通单会话实现、机械小改、简单问答和一次性审查不要求 memory sync。
- 只有存在真实并行 agent/session 或 active claim 风险时，才用 `agent_work_guard.py status/check/claim/release`；claim 保持最小 scope，并在工作结束后释放。
- 更新只记录 durable delta：已验证状态、关键决策、blocker、跨会话技术事实和正式下一步；不要写完整对话或过程旁白。
- 写入后运行 `sync_project_memory.py` 或 `render_overview.py`，并验证 lane、`INDEX.md`、`overview.html` 和 `PROJECT_MEMORY.html` 一致。
- 不存在 `.docs/project-memory/` 时不要自动初始化，除非用户明确授权或项目规则要求。
```
