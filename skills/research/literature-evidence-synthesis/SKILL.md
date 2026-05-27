---
name: literature-evidence-synthesis
description: 把论文、网页调研、实验笔记和引用整理为结构化研究产物，例如 literature matrix、method comparison、evidence map、related-work outline 和 experiment hypotheses。适用于用户已经收集了一批来源，但还需要把它们标准化、比较、聚类，或转成 competition project、benchmark study、survey 或 paper draft 可直接使用的证据。
---

# 文献证据整合（Literature Evidence Synthesis）

这个 skill 适合在 search 之后、正式写作之前使用。

它的作用是把原始来源整理成可复用的 evidence artifacts。

## 快速开始

1. 先识别当前要处理的来源集合。
2. 把每个来源标准化为一组可比较字段。
3. 按方法、claim、数据集、metric 或主题分组。
4. 产出最能支撑当前阶段的 artifact。

## 支持的 artifact 类型

- literature matrix
- method comparison table
- evidence map
- claim-to-source map
- experiment hypothesis list
- related-work outline

## 输入来源

常见输入包括：

- 来自 `aminer-data-search` 的论文列表
- 来自 `autoglm-deepresearch` 的网页调研结果
- 来自代码或实验运行的笔记
- 用户已经收集好的 citations

## 输出格式

响应时使用：

```text
目标:
来源集合:
标准化字段:
分组策略:
要产出的 artifact:
证据缺口或薄弱点:
建议的下一步:
```

## 说明

- 优先使用结构化对比，而不是纯 prose summary。
- 保持 source provenance 可见。
- 明确区分事实、解释和开放问题。
- 在 evidence artifacts 没稳定前，不要直接跳到论文写作。

查看 [EXAMPLES.md](EXAMPLES.md) 获取示例用法。
