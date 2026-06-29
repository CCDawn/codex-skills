# BRT Templates

Read this file only when exact output templates, examples, or anti-patterns are needed.

## First Response

```text
需求对齐:
- 用户原话:
- 我猜你真正想要的是:
- 候选意图:
  - A: [具体行为]；适合 [选择信号]；代价 [牺牲/风险]
  - B: [具体行为]（推荐）；适合 [选择信号]；代价 [牺牲/风险]
  - C: [具体行为]；适合 [选择信号]；代价 [牺牲/风险]
- 关键信号:

请选关键项，或直接说“按推荐来”:
1. [问题]: A [适合/代价] / B（推荐）[适合/代价] / C [适合/代价]
2. [问题]: A（推荐）[适合/代价] / B [适合/代价]
3. [问题]: A [适合/代价] / B [适合/代价] / C（推荐）[适合/代价]
```

## Intent Options

```text
候选意图:
- A 保守理解:
  - Goal:
  - Expected Output:
  - Required Capability:
  - Choose When:
  - Tradeoff:
- B 标准理解（推荐）:
  - Goal:
  - Expected Output:
  - Required Capability:
  - Choose When:
  - Tradeoff:
- C 扩展理解:
  - Goal:
  - Expected Output:
  - Required Capability:
  - Choose When:
  - Tradeoff:
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

多角度自审:
- [视角]: Challenge / Evidence / Verdict
- [视角]: Challenge / Evidence / Verdict

测试锚点:
- 主路径:
- 关键边界:
```

## Planning Gate

```text
BRT 检查点:
- 已确认意图:
- 范围边界:
- 允许动作:
- 关键风险:
- 自审结论:
- 测试锚点:
- Workflow Ledger:
  - Confirmed Intent:
  - Current Stage: PLANNING_READY
  - Assumptions:
  - Unresolved Risks:
  - Recommended Next Stage: ccdawn-planning

是否进入 ccdawn-planning 制定实施方案？
A. 进入方案制定（推荐）...
B. 继续需求对齐...
C. 低风险直接实现（仅当用户明确选择）...
D. 暂停...
```

## Anti-Patterns

Bad:

```text
多角度自审:
- 核心用户: Challenge=用户可能不满意；Evidence=我会尽量对齐；Verdict=PASS
- 维护者: Challenge=以后可能难维护；Evidence=风险较低；Verdict=PASS
```

Why bad: Evidence 是态度或判断，不是证据；无法证明可以进入下一阶段。

Better:

```text
多角度自审:
- 核心用户: Challenge=是否真的解决“备选没参考价值”；Evidence=候选规则要求 Choose When 和 Tradeoff，且模板反例覆盖空泛备选；Verdict=PASS
- 维护者: Challenge=规则是否变臃肿；Evidence=主文件只新增质量门槛，详细例子留在 templates.md；Verdict=PASS
- 测试/QA: Challenge=如何检查 agent 是否执行；Evidence=输出必须包含 Review Matrix，且 Evidence 只能来自用户确认、本地事实、验证命令、probe 或显式假设；Verdict=PASS
```

Bad:

```text
评审:
- 核心用户
- 维护者
- QA
```

Why bad: 只列视角，没有质疑、证据和结论，不能阻止错误实现。

Better:

```text
多角度自审:
- 核心用户: Challenge=是否真的减少重复解释；Evidence=下轮可复用项目上下文；Verdict=PASS
- 维护者: Challenge=记忆噪声会不会膨胀；Evidence=只写项目级摘要并保留确认门槛；Verdict=ACCEPT_RISK，剩余风险是需要定期清理
- 测试/QA: Challenge=如何证明不是只改了话术；Evidence=用一次模糊需求对齐样例检查候选项是否都有适用信号和代价；Verdict=PASS
```

Bad:

```text
候选意图:
- A: 最小改动
- B: 标准方案（推荐）
- C: 完整方案
```

Why bad: 非推荐项只是抽象层级，用户不知道什么时候该选，也不知道会牺牲什么。

Better:

```text
候选意图:
- A: 只改当前回复格式；适合先验证语气是否对；代价是不会约束后续多轮行为。
- B: 改候选意图和问题选项规则（推荐）；适合解决“备选没参考价值”的核心问题；代价是输出会多一点点判断信号。
- C: 加完整案例库和评测 prompt；适合要系统压测 skill；代价是范围更大、维护成本更高。
```

Bad:

```text
你具体想要什么？
```

Why bad: 把需求工程推给用户，没有候选意图，也没有推荐。

Better:

```text
我猜你真正想解决的是“避免每次重新解释上下文”，而不是单纯“保存更多内容”。

候选意图:
- A: 只保存最近一次选择；适合只想少重复一次；代价是跨任务无法复用。
- B: 保存当前项目可复用上下文（推荐）；适合持续开发和多轮恢复；代价是需要维护项目级记忆。
- C: 做完整全局记忆管理；适合跨项目长期画像；代价是隐私、噪声和权限边界都更重。

请选关键项，或直接说“按推荐来”:
1. 保存范围: 最近一次（轻量但短效） / 当前项目（推荐，复用价值最高） / 全局（跨项目但风险高）
2. 是否允许自动写入: 否（最安全但麻烦） / 仅确认后（推荐，风险可控） / 是（省事但容易积累噪声）
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
