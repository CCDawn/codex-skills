# Integration Ownership

仅在出现 `MERGE_READY` 或 integration queue 时读取。

## 原子认领

所有相关 Agent 只检查一次 `lane=integration/<target-key>`：

- 用户指定 > 有效 integration claim > 首个成功原子认领者。
- 无有效 claim 时，具备目标分支权限且能开始维护队列的 Agent 应 claim，并发送一次 `INTEGRATION_CLAIMED`，包含 `Agent / Thread / Target / Queue / Lease / Next Checkpoint`。
- 已有有效 claim 时，其余 Agent只提交 branch/commit/tests/risks；不得自行等待稳定 `main`、重复 rebase/full gate 或合并。

负责人 ACK `MERGE_READY`、维护队列、串行应用交付，在最终 HEAD 运行一次完整 gate。claim 有效期间不启动新的无关实现任务。

认领的是推进义务，不要求当下即可写入 `main`。dirty checkout、等待 peer 释放或已证明无关的 baseline failure 都是队列状态，不是放弃 owner 的理由。交付已提交后，将实现 claim 转为 ready/released，由 integration claim 承担后续责任。

若失败能在 clean base 复现且交付没有新增失败，标记 `MERGE_READY_CONDITIONAL`；默认不接管或要求用户授权修复无关基线。强制 gate 仍阻止合入时，owner 保留队列责任，只向现有基线 owner 发一次协调并等待可行动事件；只有产品、安全、迁移或真实范围取舍才询问用户。

无法及时推进时发送 `INTEGRATION_HANDOFF` 并释放 claim，不得静默占位。只有明确释放、租约失活或 Git 已证明义务完成时，其他 Agent 才可 `takeover`。完成后广播一次 `INTEGRATED`，释放 claim 并关闭关联 merge coordination。
