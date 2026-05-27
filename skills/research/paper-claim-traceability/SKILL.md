---
name: paper-claim-traceability
description: 审核论文、报告或 competition writeup 中的 claims，判断它们是否由实验、表格、图、引用或定性证据支撑。适用于用户已经有 draft，想检查 traceability、降低 overclaiming、补强 limitations，或在投稿前建立一条可审计的证据链。
---

# 论文 Claim 可追溯性审查（Paper Claim Traceability）

这个 skill 适合在工作流后期使用，也就是实验和写作素材已经存在之后。

## 快速开始

1. 先明确本次要审查的是某个 draft section，还是整篇 manuscript。
2. 抽取主要 claims、contribution statements 和 comparative statements。
3. 把每个 claim 映射到支撑证据，或者标记为支撑不足。
4. 给出修订、删除、降调表述，或补证据的建议。

## 审查目标

- title 和 abstract 中的 claims
- contribution bullets
- related-work positioning
- methodology claims
- results interpretation
- conclusion 和 future-work statements

## 证据类型

- experiment logs
- tables
- figures
- citations
- qualitative examples
- error analyses
- ablation studies

## 输出格式

响应时使用：

```text
审查范围:
已审查的 claims:
证据充分的 claims:
证据偏弱的 claims:
缺乏支撑的 claims:
缺失证据:
建议修订:
投稿风险:
```

## 说明

- 优先保证 traceability，而不是修辞上的漂亮。
- 尽早标记 overclaiming。
- 区分“缺证据”和“缺写法”。
- 当证据狭窄或不稳定时，必须要求写出 limitations。

查看 [EXAMPLES.md](EXAMPLES.md) 获取示例用法。
