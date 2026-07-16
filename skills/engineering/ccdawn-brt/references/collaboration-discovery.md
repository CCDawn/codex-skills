# Collaboration Discovery

只在需求已收敛、功能 owner 已选定、本轮原生 thread/list 能力可用，且任务出现协作收益信号时读取。能力不可用时返回 `NONE`，不得伪造候选。发现目的是选择是否组队，不是启动协调。

## 有界发现

1. 使用本轮原生 thread/list 能力查找同一项目的活跃对话；registry 已存在时读取 Agent、scope、branch/worktree 和 checkpoint，不为发现初始化 memory 或 registry。
2. 只读最多 3 个最相关候选，确认真实任务、进度、有效 thread id、互补价值和重叠风险；路径或名称相似不等于同项目。
3. 比较可复用证据、关键路径缩短、独立验证价值与上下文/协调/合并成本。候选忙碌、过期、共享同一小文件或没有独特贡献时排除。

## 决策

- `NONE`：无正收益候选，原 owner 静默继续。
- `PEER_CONTEXT_REVIEW`：同行上下文能改善当前判断，交 thread coordination 做一次只读建议。
- `DISPATCH_READ_ONLY`：独立只读证据能降低风险，可交 thread coordination 有界派发。
- `COORDINATE_OVERLAP`：只有重叠、讨论或恢复需求，交 thread coordination。
- `DISPATCH_DISJOINT_WRITE -> TEAM_READY`：至少两个交付物有明确依赖和互不重叠写入面，且团队收益高于回收成本，交 multi-agent orchestration。
- `ASK_CREATE`：无现有候选但新增会话有明确收益；向用户询问一次，未授权则当前 owner 继续。

发现时不得发送消息、claim、创建会话或暂停其他 Agent。路由完成后由下游 owner 执行这些动作。
