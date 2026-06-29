# Dawn Codex Skills

这是一个本地 skill 仓库，重点覆盖竞赛型研究流程、行为闸门式实现，以及持久化项目记忆。

这个仓库默认只安装到一层 live 本地目录：

- `~/.codex/skills/<ccdawn-skill-name>`：给 Codex 运行时直接加载的 live skill 目录

如果你明确需要，也还保留可选的第二层目录：

- `~/.agents/skills/<ccdawn-skill-name>`：给某些应用环境下的本地 skill 目录使用

目录名必须和 `SKILL.md` 里的 `name` 一致，更新后要校验 live Codex skill。

## 当前包含的 skill

### Engineering

- **`ccdawn-brt`**  
  Behavior / Review / Test 工作流 skill。它会主动揣测用户心里真正想要的结果，给出候选意图、推荐方案和高信号选择题，让用户选择或确认后，再把模糊功能想法收束成清晰的行为定义、评审视角、Task Graph、执行闸门、验收标准和测试意图。

- **`ccdawn-planning`**
  复制出来的方案制定阶段 skill 包，用来在需求对齐后、动代码前形成实施方案。

- **`ccdawn-task-splitting`**
  复制出来的任务拆分阶段 skill 包，用来把已确认方案拆成可审阅、可独立验证的任务单元。

- **`ccdawn-bdd-tdd-development`**
  复制出来的开发阶段 skill 包，用来围绕行为预期执行 BDD/TDD 风格开发。

- **`ccdawn-completion-summary`**
  复制出来的完成总结阶段 skill 包，用来做新鲜验证、需求对照和简洁交接总结。

- **`ccdawn-dawn-agent-html-memory`**  
  这是一个项目记忆 skill，用来在真实软件项目里创建并持续维护 `.docs/project-memory/`。它支持按职责拆分的多会话共享 lane，生成会聚合这些 lane 的 HTML 总览页，并在项目根目录生成一个 `PROJECT_MEMORY.html` 快捷入口。

- **`ccdawn-goal-loop`**  
  这是一个目标执行 skill，用来把一个目标整理成带有证据、限制条件、允许范围、下一步判断规则和阻塞停止报告的可执行合同。

### Research

- **`ccdawn-competition-research-lifecycle`**  
  这是一个面向研究竞赛和 benchmark 项目的端到端工作流 skill，覆盖任务定义、数据准备、文献和方案调研、baseline 搭建、训练与实验、分析与消融、论文写作和提交打包。

  它把 `ccdawn-brt` 视为流程治理层，用来定义每个阶段的目标、评审点和验收标准，同时附带参考指南、更紧的响应契约，以及可直接复用的阶段模板。

### Competition

- **`ccdawn-huawei-nslb-score-loop`**  
  这是一个面向 Huawei Algorithm Challenge 37 NSLB 项目的专用 score loop skill，用来协调隔离 worker lane、本地 proxy evidence、baseline promotion、打包登记，以及 online score feedback 校准。

### Creative

- **`ccdawn-creative-toolbox`**  
  这是一个上下文创意生成 skill，用来做 concept collision、divergent thinking、Naming Forge、新概念生成、范式探索、产品想法、研究概念和非常规但有用的方向生成。

## 统一管理格式

已发布 skill 统一使用这个目录形状：

```text
skills/<bucket>/<ccdawn-skill-name>/
  SKILL.md
  agents/openai.yaml        # 可选，但推荐用于 Codex 斜杠指令 metadata
  references/               # 可选，用于参考资料、模板、ledger 或 schema
  scripts/                  # 可选，用于 skill 自带辅助工具
```

规则：

- `skill-name` 必须和 `SKILL.md` 里的 `name` 字段一致。
- 每次 catalog 变化，都同步更新 `README.md`、`README.zh-CN.md`、对应 bucket 的 `README.md`，以及 `.claude-plugin/plugin.json`。
- 正式安装到 `~/.codex/skills/<ccdawn-skill-name>` 时，运行 `python scripts/install_codex_library.py`，使用真实目录复制。
- 除非你明确想要重复斜杠条目，否则不要把同一个 skill 同时安装到 `~/.codex/skills` 和 `~/.agents/skills`。

## 仓库结构

```text
.claude-plugin/
  plugin.json
AGENTS.md
CLAUDE.md
skills/
  competition/
    README.md
    ccdawn-huawei-nslb-score-loop/
  creative/
    README.md
    ccdawn-creative-toolbox/
  engineering/
    README.md
    ccdawn-dawn-agent-html-memory/
    ccdawn-brt/
    ccdawn-planning/
    ccdawn-task-splitting/
    ccdawn-bdd-tdd-development/
    ccdawn-completion-summary/
    ccdawn-goal-loop/
  research/
    README.md
    ccdawn-competition-research-lifecycle/
scripts/
  install_codex_library.py
```

## 快速开始

推荐默认把 skills 安装到 live Codex 目录：

```bash
python scripts/install_codex_library.py
```

这是这个仓库以后固定使用的正式安装方式。它会把每个已发布 skill 复制到：

```text
~/.codex/skills/<ccdawn-skill-name>
```

安装脚本还会强制保证：

- skill 目录名和 `SKILL.md` 里的 `name` 一致
- 安装到 Codex 的 skill 是真实目录，不是 symlink 或 junction
- 如果本机存在 Codex 自带的 `quick_validate.py`，会顺手校验 live skill

如果同一个 skill 同时安装到 `.codex/skills` 和 `.agents/skills`，Codex 里可能会出现重复的斜杠条目。只有在你明确需要额外目录副本时，才使用 `.agents` 目标。

只安装部分 skill：

```bash
python scripts/install_codex_library.py --skill ccdawn-brt --skill ccdawn-dawn-agent-html-memory
```

只安装到 live Codex 目录：

```bash
python scripts/install_codex_library.py --agent codex
```

只安装到本地斜杠目录：

```bash
python scripts/install_codex_library.py --agent agents
```

只有在你明确需要时，才安装到 Claude：

```bash
python scripts/install_codex_library.py --agent claude
```

同时安装到 Codex、`.agents` 和 Claude：

```bash
python scripts/install_codex_library.py --agent all
```

如果你明确需要同时保留 Codex 和 `.agents` 两份副本：

```bash
python scripts/install_codex_library.py --agent codex-agents
```

## 斜杠指令排查

如果斜杠条目缺失或重复，先按这个顺序排查，不要先改提示词或随手改目录名：

1. 先看 `~/.codex/skills/<ccdawn-skill-name>` 里的 live 安装副本，不要只看仓库副本。
2. 检查是否还存在额外的 `~/.agents/skills/<ccdawn-skill-name>` 副本；同一个 skill 两边都装时，Codex 里可能出现重复条目。
3. 检查 live 安装副本里的 `agents/openai.yaml`，并保持它和本仓库里已经验证可用的最小 `interface:` 结构一致。
4. 如果当前激活且受信任的工作区就是这个仓库，也要检查 `.claude-plugin/plugin.json`，因为仓库本地 manifest 也可能影响可见条目。
5. 修改 metadata 后先重启 Codex，再在新线程里验证，不要在旧线程里直接下结论。

## 可选的开发捷径

如果只是临时开发调试，仍然可以把 skills 链接到 `~/.claude/skills`。

macOS/Linux:

```bash
bash scripts/link-skills.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\link-skills.ps1
```

不要把这条链接流程当成这个仓库的正式发布/安装方式。

仓库里的元数据索引在这里：

```text
.claude-plugin/plugin.json
```

真正的 skills 内容在这里：

```text
skills/
```

安装或更新 live skill 后，重启客户端，让它重新加载本地 skills。

## 使用方式

在 Codex 聊天里可以直接这样触发：

- `使用 ccdawn-competition-research-lifecycle 帮我规划这个竞赛项目`
- `用 ccdawn-goal-loop 把这个目标整理成可验证的执行合同`
- `用 ccdawn-huawei-nslb-score-loop 准备 NSLB epoch 并 gate child results`
- `用 ccdawn-creative-toolbox 基于当前上下文生成新概念卡`
- `帮我给这个仓库初始化项目记忆`
- `使用 ccdawn-dawn-agent-html-memory 把这个仓库按 frontend 项目初始化项目记忆`

这个仓库现在刻意对齐“本地 skill 仓库”模式，而不是 marketplace plugin 模式。
