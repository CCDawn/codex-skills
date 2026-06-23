# BRT Templates

Read this file only when exact output templates, examples, or anti-patterns are needed.

## First Response

```text
需求对齐:
- 用户原话:
- 我猜你真正想要的是:
- 候选意图:
  - A:
  - B: （推荐）
  - C:
- 关键信号:

请选关键项，或直接说“按推荐来”:
1. [问题]: A / B（推荐） / C
2. [问题]: A（推荐） / B / C
3. [问题]: A / B / C（推荐）
```

## Intent Options

```text
候选意图:
- A 保守理解:
  - Goal:
  - Expected Output:
  - Required Capability:
- B 标准理解（推荐）:
  - Goal:
  - Expected Output:
  - Required Capability:
- C 扩展理解:
  - Goal:
  - Expected Output:
  - Required Capability:
```

## Quick BRT

```text
需求账本:
- 已确认意图:
- 范围边界:
- 操作边界:
- 失败路径:
- 验证证据:
- 剩余风险:

行为摘要:
- 触发:
- 结果:
- 不做:

测试锚点:
- 主路径:
- 关键边界:
```

## Implementation Gate

```text
BRT 检查点:
- 已确认意图:
- 范围边界:
- 允许动作:
- 关键风险:
- 测试锚点:
- 完成汇报:

是否进入实现？
```

## Anti-Patterns

Bad:

```text
你具体想要什么？
```

Why bad: 把需求工程推给用户，没有候选意图，也没有推荐。

Better:

```text
我猜你真正想解决的是“避免每次重新解释上下文”，而不是单纯“保存更多内容”。

候选意图:
- A: 只保存最近一次选择
- B: 保存可复用的工作上下文（推荐）
- C: 做完整记忆管理

请选关键项，或直接说“按推荐来”:
1. 保存范围: 最近一次 / 当前项目（推荐） / 全局
2. 是否允许自动写入: 否 / 仅确认后（推荐） / 是
```

Bad:

```text
我会实现一个完整记忆系统。
```

Why bad: 把宽泛词照字面扩展成大范围实现。

Better:

```text
我建议先按“当前项目可复用上下文 + 确认后写入”推进，这样行为可观察、风险可控。
```
