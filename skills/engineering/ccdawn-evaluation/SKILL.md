---
name: ccdawn-evaluation
description: Use when the user asks to evaluate, assess, audit, compare, score, judge reasonableness, inspect quality, or decide whether a plan, design, workflow, skill, implementation, or result is good enough.
---

# CCDawn Evaluation

## 目标

对方案、设计、流程、skill、实现结果或当前状态做多维评估，给出有证据的判断、风险和下一步建议。

此阶段只评价和给建议，不直接修改；如果评估发现需要改动，再路由回 `ccdawn-brt`、`ccdawn-planning`、`ccdawn-task-splitting`、开发或 PR 审查。

## 进入条件

使用前确认用户或上下文在问：

- “评估一下”“评价”“审查是否合理”“有没有问题”“是否有效”；
- 比较多个方案、实现路径、流程设计或 skill 设计；
- 判断当前输出是否过度复杂、是否足够灵活、是否符合需求；
- 对完成结果做质量、风险、可维护性、成本或用户体验判断。

如果对象是 PR/diff/提交范围，使用 `ccdawn-pr-review`。如果对象是 bug 或失败行为，使用 `ccdawn-bug-review`。

## 评价方式

1. 定义评价对象和目标：评价什么，服务哪个用户目标。
2. 选 3-5 个高相关维度：只选会改变结论或行动的维度。
3. 收集证据：来自文件、代码、测试、日志、用户要求、运行结果或明确假设。
4. 给结论：不要平均主义；明确推荐、可接受风险和必须补的缺口。
5. 路由下一步：继续对齐、改方案、拆任务、修复、审 PR 或停止。

## 默认维度

按对象选择，不要全部输出：

- 需求对齐：是否满足用户真实目标。
- 效率和噪声：是否为了流程而增加低价值步骤。
- 灵活性：是否能根据任务重量、风险和证据改变流程。
- 正确性：是否能被本地事实或验证证明。
- 风险：是否涉及数据、安全、权限、迁移、发布或回滚。
- 可维护性：是否让后续 agent 更容易继续。
- 用户体验：是否让用户少做无价值选择。

## 输出契约

```text
评估结论:
- 总评: GOOD / ACCEPTABLE_WITH_RISK / NEEDS_CHANGE / BLOCKED
- 推荐判断: ...
- 关键证据: ...

多维评价:
- 维度: PASS / WEAK / FAIL / ACCEPT_RISK；证据...；影响...

必须调整:
- ...

可选优化:
- ...

下一步:
A. 按推荐调整（推荐）...
B. 回到 ccdawn-brt 重新对齐目标...
C. 回到 ccdawn-planning 改方案...
D. 进入 ccdawn-task-splitting 或开发...
E. 暂停...
```

## 质量门槛

- 不给空泛建议；每条建议必须说明影响和触发条件。
- 不用“更完整”“更谨慎”“更简洁”当结论，必须落到行为、成本、风险或证据。
- 不为了展示全面而输出低相关维度。
- 不把实现建议伪装成已验证事实。
- 如果缺少关键证据，结论必须是 `BLOCKED` 或 `ACCEPTABLE_WITH_RISK`。

