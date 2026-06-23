# BRT Templates And Examples

Read this file only when exact output templates, examples, or anti-patterns are needed.

## First Response

```text
意图发现:
- 用户原话:
- 推荐理解:
- 备选误解风险:
- 关键信号:
- 状态判定: CONVERGED / NEED_ASSUMPTION / NEED_PROBE
- 下一步动作: ENTER_PLANNING / ASK_SINGLE_CLARIFYING_QUESTION / RUN_PROBE

需求对齐:
- 我理解你真正想要的是:
- 最可能误解的是:

追问:
- 是否按 [推荐答案] 推进？
- 推荐答案:
- 原因: [为什么这是最高信号问题]
```

## Intent Discovery

```text
意图发现:
- 用户原话: [用户实际说法]
- 推荐理解: [用户可能真正想解决的问题]
- 心智画像: [用户可能在担心什么、想避免什么、希望最终看到什么]
- 备选误解风险: [最容易走偏的相邻意图]
- 关键信号: [来自措辞、上下文、代码或任务形态的证据]
- 关键词风险: [过宽/过窄/可能用错的词]
- 状态判定: [CONVERGED / NEED_ASSUMPTION / NEED_PROBE]
- 下一步动作: [ENTER_PLANNING / ASK_SINGLE_CLARIFYING_QUESTION / RUN_PROBE]

追问:
- 问题: [只问当前最高信号的一个问题]
- 推荐答案: [agent 建议]
- 原因: [为什么答案会改变行为/范围/风险/测试/许可]
```

## Multi-Hypothesis Discovery

Use only when the recommendation is unstable or the user benefits from choosing between paths.

```text
候选意图:
- 保守路径:
  - Goal:
  - Expected Output:
  - Required Capability:
- 标准路径:
  - Goal:
  - Expected Output:
  - Required Capability:
- 扩展路径（可选）:
  - Goal:
  - Expected Output:
  - Required Capability:

推荐理解:
- 选择:
- 原因:
- 最大误解风险:
```

## Failed Intent Calibration

```text
意图校准失败:
- 被否定的推断: [刚才 agent 的推断]
- 用户反馈: [不对 / 不是这个意思 / 我也说不清]
- 可能偏差: [重点错 / 范围错 / 对象错 / 结果错 / 操作方式错]
- 候选意图:
  - A:
  - B:
  - C:
- 推荐探针:
  - 做什么:
  - 不做什么:
  - 如何观察是否接近真实意图:

追问:
- 问题: 哪个更接近？如果都不对，我会换一组候选。
- 推荐答案:
- 原因:
```

## Quick BRT

```text
需求对齐:
- 推荐理解:
- 备选误解风险:
- 关键信号:
- 推荐答案:

行为摘要:
- 参与者:
- 触发条件:
- 结果:
- 不在范围内:

推荐评审视角:
- 核心用户:
- 维护者:
- 测试/QA:

测试映射:
- [场景] -> [测试层]
```

## Full BRT Design

```text
需求账本:
- 用户原话:
- agent 推断意图:
- 已确认意图:
- 用户目标:
- 使用者/触发者:
- 可观察结果:
- 数据/状态边界:
- 操作边界:
- 失败路径:
- 验证证据:

范围边界:
- 本轮覆盖:
- 本轮不覆盖:

推荐方案:
- 方案:
- 理由:

备选方案:
- A:
- B:

示例:
- Given:
- When:
- Then:

推荐评审视角:
- 核心用户:
- 维护者:
- 测试/QA:
```

## Review Result

```text
评审:
- 核心用户 [阻塞|重要|可选]:
  - 关注点:
  - 发现:
  - 为什么重要:
  - 推导结果:
- 维护者 [阻塞|重要|可选]:
  - 关注点:
  - 发现:
  - 为什么重要:
  - 推导结果:
- 测试/QA [阻塞|重要|可选]:
  - 关注点:
  - 发现:
  - 为什么重要:
  - 推导结果:

评审后的设计调整:
- 
```

## Decision Record

```text
决策记录:
- 决定:
  原因:
  未采用方案:
  未采用原因:
```

## BRT Checkpoint

```text
BRT 检查点:
- 锁定行为:
- 范围边界:
- 评审视角:
- 阻塞问题:
- 测试锚点:
- 实施目标:
- 任务契约:
  - 目标:
  - 上下文:
  - 限制:
  - 允许动作:
  - 验证方式:
  - 完成汇报:

是否继续实施？
```

## Implementation Loop

```text
实施目标:
被测试场景:
RED:
GREEN:
重构:
验证:
```

## Result Summary

```text
BRT 结果:
- 已交付行为:
- 评审阻塞项:
- 测试锚点:
- 开放问题:
- 剩余风险:
- 下一步:
```

## Example Mapping

```text
功能: Remember supervised evolution settings

规则: workbench 复用上一次成功配置

示例: 数据集来源
- Given: previous run used dataset "custom_prompt_jsonl" with limit 2
- When: the workbench opens again
- Then: dataset and limit prompts default to those values

示例: bundle 来源
- Given: previous run used bundle "saved_bundle" with keep_worktree true
- When: the workbench opens again
- Then: bundle and keep_worktree prompts default to those values
```

## Anti-Patterns

Bad:

```text
我来做。顺便问一下：你要放哪里？要不要编辑？要不要导出？
```

Why bad: asks multiple questions and gives no current understanding or recommendation.

Better:

```text
需求对齐:
- 当前理解: 你想新增一个只读入口，让用户集中查看 agent 记忆。
- 未决分歧: 这页是只读查看，还是包含编辑/删除这类管理动作。
- 为什么重要: 这会改变权限、安全、接口和测试范围。
- 会更新: 需求账本、范围边界、测试映射

追问:
- 问题: 本轮是否先做只读聚合页？
- 推荐答案: 是，先只读。
- 原因: 能先建立清晰数据边界，避免把查看页膨胀成管理系统。
```

Bad:

```text
BRT 结果: 已完成。下一步后续跟进。
```

Why bad: no verification, no connection to the main thread, no actionable next step.

Better:

```text
BRT 结果:
- 已交付行为: BRT 会在任一阶段发现关键不确定性时暂停追问。
- 测试锚点: quick_validate.py passed。
- 开放问题: 尚未做真实对话压测。
- 下一步: 用一个模糊功能请求压测 BRT 是否只问一个高价值问题并更新需求账本。
```

Bad:

```text
用户说“把所有记忆都做得更智能”，我将新增一个完整记忆管理系统。
```

Why bad: treats broad and possibly inaccurate wording as literal requirements.

Better:

```text
意图发现:
- 用户原话: “把所有记忆都做得更智能”
- agent 推断意图: 用户可能真正想解决的是记忆分散、难查找、无法判断哪些记忆对当前任务有用。
- 关键词风险: “所有”范围过宽，“智能”不可测试。
- 推荐解释: 本轮先把相关记忆聚合为只读视图，并按来源和更新时间排序，不做编辑/删除。
- 待确认点: 本轮是否先解决“查找和理解记忆”，而不是做“管理记忆”。

追问:
- 问题: 是否先按“只读聚合 + 来源/时间排序”理解你的目标？
- 推荐答案: 是。
- 原因: 这个行为可观察、可测试，也能避免把需求膨胀成完整记忆管理系统。
```

Bad:

```text
用户说“不对，我也说不清”。那请你重新描述一下真实需求。
```

Why bad: forces the user to perform requirements engineering and gives no recovery path.

Better:

```text
意图校准失败:
- 被否定的推断: 你想做“只读聚合 + 来源/时间排序”的记忆查看页。
- 用户反馈: 不对，但也说不清。
- 可能偏差: 重点可能错了；你说的“智能”也许不是“展示”，而是“判断哪些记忆有用”。
- 候选意图:
  - A: 更容易找到相关记忆
  - B: 自动总结和压缩记忆
  - C: 自动判断当前任务该用哪些记忆
- 推荐探针:
  - 做什么: 先做只读的“当前任务相关记忆推荐”预览。
  - 不做什么: 不编辑、不删除、不自动改写记忆。
  - 如何观察是否接近真实意图: 用一次真实任务检查推荐记忆是否帮上忙。

追问:
- 问题: 哪个更接近？如果都不对，我会换一组候选。
- 推荐答案: C。
- 原因: “智能”更像是判断相关性，而不是单纯展示或管理。
```
