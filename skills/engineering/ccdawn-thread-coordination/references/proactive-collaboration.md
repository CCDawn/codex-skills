# 主动协作

## 派发

只向相关空闲 Agent 派发独立 lane。发送前 claim `thread/<agent-id>` 与 `dispatch/<task-key>`；写入再含实际 scope。消息给出 `From Agent / From Task / To Agent / To Task / Reply To / Scope / Expected Output / Return Condition`，禁止递归派发。

owner 保留关键路径与集成。结果、拒绝或超时后释放 claim；超时标 stale，迟到结果先复核。可选协作不 BLOCKED；简单任务、同文件或忙碌 Agent 不派发。

## 同行建议

相关 Agent 处理同一 surface、接口或依赖时可做一次 `PEER_CONTEXT_REVIEW`：只读其 task、checkpoint 和 diff。有证据支持的具体改进才发送 `ADVICE_AVAILABLE`，写明双方身份与职责、证据、影响和建议。无 finding 不发消息；不夺 owner、不暂停、不强制采纳，不轮询或重复提醒。

接收方回复 `ACCEPT / ADAPT / DECLINE` 及理由后继续。建议涉及新 scope 或共享契约时再进入 discussion；普通建议不建 coordination。
