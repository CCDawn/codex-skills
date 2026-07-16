# Team Protocol

只在形成真实团队后读取。所有消息使用同一个 `Orchestration ID` 和稳定 `Reply To`，先读已有消息再发送。

## 候选判断

按以下顺序筛选：同一项目与事实源、近期仍活跃、任务互补或持有可复用证据、scope 可分离、具备有效 thread id。只读最多 3 个最相关候选；路径相似但项目不明不算同项目。

## TEAM_INVITE

```text
Type: TEAM_INVITE
Orchestration ID:
From Agent / From Task:
To Agent / Current Task:
Why This Agent:
Deliverable:
Scope:
Dependency In:
Evidence Out:
Return Condition:
Do Not Touch:
Reply To:
```

邀请前必须持有一次原子创建的 dispatch claim；消息携带其 id。接收方只回复 `ACCEPTED / ADAPT / DECLINED`，并说明实际 branch/worktree、可接受 scope 和依赖缺口。未收到 `ACCEPTED` 不视为入队；claim 已释放或过期时，迟到 ACK/结果不能恢复原派发。

## CHECKPOINT

只发送以下状态：

- `CONTRACT_CHANGE`：任务契约或 scope 必须改变；
- `DEPENDENCY_READY`：另一成员可以开始；
- `ACTIONABLE_FINDING`：新证据会改变其他成员行动；
- `BLOCKED`：需要其他成员独有证据或决定；
- `MERGE_READY`：交付物已完成并可回收；
- `CORRECTION`：此前结论错误且会导致误改。

相同证据只保留最新状态；关联 findings 在自然 checkpoint 聚合。无变化进度、过程旁白和非阻塞催促不发送。

## MERGE_READY

```text
Type: MERGE_READY
Orchestration ID:
Agent / Deliverable:
Base / Head:
Branch / Worktree:
Changed Scope:
Dependency State:
Tests:
Known Risks:
Suggested Integration Order:
```

该消息只是候选证据，coordinator 必须用 Git 和测试重验。集成完成后只广播一次 `INTEGRATED`；失败只通知负责返修的成员和受影响依赖方。
