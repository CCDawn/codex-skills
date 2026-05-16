# Codex Skills

这是一个面向 Codex 的自定义 skills 仓库，重点服务于竞赛型科研工作流。

## 当前包含的 skill

### `brt`

这是 Behavior / Review / Test 工作流 skill。它的作用是在真正开始实现之前，把模糊的功能想法收束成清晰的行为定义、评审视角、验收标准和测试意图。

### `competition-research-lifecycle`

这是一个覆盖竞赛科研全周期的主流程 skill，包含：

- 任务理解
- 数据整理
- 文献与方案调研
- baseline 搭建
- 训练与实验
- 分析与消融
- 论文写作
- 提交打包

它把 `brt` 视为流程治理层，用来定义每个阶段的目标、评审点和验收标准。

### `literature-evidence-synthesis`

这是一个科研证据整理 skill，用来把论文、网页调研、实验记录和引用材料整理成可复用的结构化产物，例如：

- 文献矩阵
- 方法对照表
- claim map
- 实验假设清单
- related work 提纲

### `paper-claim-traceability`

这是一个论文验收 skill，用来检查论文中的核心结论是否能追溯到实验、表格、图、引用或案例，避免“写出来了，但证据没跟上”。

## 仓库结构

```text
brt/
  SKILL.md
  agents/
  references/
competition-research-lifecycle/
  SKILL.md
  REFERENCE.md
  EXAMPLES.md
literature-evidence-synthesis/
  SKILL.md
  EXAMPLES.md
paper-claim-traceability/
  SKILL.md
  EXAMPLES.md
```

## 如何安装到 Codex

把对应 skill 文件夹复制到你的 Codex 全局 skills 目录：

```text
~/.codex/skills/
```

Windows 通常是：

```text
C:\Users\<你自己的用户名>\.codex\skills\
```

复制完成后，重启 Codex 桌面端，让它重新加载全局 skills。

## 使用方式

在 Codex 聊天里可以直接这样触发：

- `使用 competition-research-lifecycle 帮我规划这个竞赛项目`
- `用 literature-evidence-synthesis 把这些论文整理成文献矩阵`
- `用 paper-claim-traceability 检查这篇论文初稿的证据链`
