---
name: ccdawn-evaluation
description: Use when CCDawn workflow needs a Chinese-first evaluation adapter and no more specific existing skill already owns the review, debugging, PR, planning, feedback, verification, or goal task.
license: MIT
---

# CCDawn Evaluation

## 目标

评价方案、流程、skill、输出质量、合理性、灵活性或下一步价值。只在没有更具体 owner 时使用；不重复 PR、项目、bug、复用研究或 planning 流程。

## BRT interface

- Context Boundary: 被评价对象、用户标准、证据来源、允许动作和已排除的专项 owner。
- Output Contract: 简洁总评、会改变行动的 findings、按 ROI 排序的建议和 Route Out。
- Allowed Action: 默认只读；用户已要求优化且改动低风险、范围清楚、可验证时可路由直接执行。
- Success Evidence: 判断绑定具体对象、证据、影响和可验证下一步。
- Stop Condition: 对象/目标不明、存在更具体 owner、关键证据缺失、实施越界或高风险取舍未确认。
- Route Out: 更具体 owner、`ccdawn-brt`、`ccdawn-planning`、FAST_PATH、`ccdawn-completion-summary` 或 BLOCKED。

## 统一调用契约

- 只处理 BRT interface 范围；不匹配时回 `ccdawn-brt` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文；保留技术字面量；只报结论、证据、风险和产出；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## 评价方法

1. 先内部确认没有更具体 owner；无需向用户输出“复用检查”。
2. 从需求覆盖、流程成本、完成率、误改风险、证据质量、维护性和用户价值中选 2-4 个会改变行动的维度。
3. 每个 finding 给证据、影响和最小有效改进，不用“更完善/更灵活”等空话。
4. 多个改进按依赖、ROI 和误改风险排序；严重度不等于执行顺序。
5. 用户已要求“继续/优化/修复”时，选择并连续执行当前契约内的 `SAFE_DIRECT` 项；只有 planning、高风险取舍或 BLOCKED 才停下。

内部可以多视角自审，但没有 finding 不展示矩阵，不输出固定角色或完整行动分类。

## 输出

```text
评估结论: GOOD / ACCEPTABLE_WITH_RISK / NEEDS_CHANGE / BLOCKED
关键依据: ...
Findings:
- <问题>；证据...；影响...；建议...
执行顺序（仅多个动作时）:
1. <动作> [SAFE_DIRECT/PLAN_THEN_EXECUTE/DEFERRED/BLOCKED]；完成条件...
剩余风险: ...
下一步建议: <一个具体动作>
```

评价对象不清时回 BRT 对齐；评价变成项目/PR/bug/复用专项时立即 Route Out，不在本 skill 扩写对应流程。
