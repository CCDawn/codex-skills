# Dawn Codex Skills

这是一个本地 skill 仓库，重点覆盖竞赛型研究流程、行为闸门式实现，以及持久化项目记忆。

## 安装

最快方式：把现成提示词复制给 Codex，让 Codex 自动安装：

- [复制给 Codex 的一键安装提示词](INSTALL_PROMPTS.md)

手动安装：

```bash
git clone https://github.com/CCDawn/codex-skills.git
cd codex-skills
```

Windows PowerShell 推荐用：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

macOS/Linux 推荐用：

```bash
sh ./install.sh
```

默认安装目标是：

- `~/.codex/skills/<ccdawn-skill-name>`：给 Codex 运行时直接加载的 live skill 目录

安装器默认不写入 `~/.agents/skills`，避免重复 slash-command。演练、验证、只安装部分 skill 和高级目标见 [安装细节](#安装细节)。

## 当前包含的 skill

### Engineering

- **`ccdawn-brt`**  
  Behavior / Review / Test 流程入口 skill。它会主动揣测用户心里真正想要的结果，给出候选意图、推荐方案和高信号选择题，让用户选择或确认后，再把模糊功能想法收束成行为契约、评审视角、测试锚点和下一阶段路由。

- **`ccdawn-feature-reuse-research`**
  复杂功能新增前的复用调研 skill，用来比较现有项目、库、示例和项目内模块，判断复用价值和实现边界。

- **`ccdawn-planning`**
  方案制定阶段 skill，用来在需求对齐后、动代码前形成实施方案。

- **`ccdawn-task-splitting`**
  任务拆分阶段 skill，用来把已确认方案拆成可审阅、可独立验证的任务单元。

- **`ccdawn-bdd-tdd-development`**
  开发阶段 skill，用来围绕行为预期执行 BDD/TDD 风格开发。

- **`ccdawn-completion-summary`**
  完成总结阶段 skill，用来做新鲜验证、需求对照和简洁交接总结。

- **`ccdawn-pr-review`**
  PR 审阅阶段 skill，用来把 PR、分支、提交范围或本地 diff 对照已确认需求、任务证据、回归风险和合并准备度进行审查。

- **`ccdawn-project-review`**
  项目审查 skill，用来审查整个仓库、架构、技术债、测试缺口、可维护性、接手状态和项目健康。

- **`ccdawn-bug-review`**
  CCDawn bug 审查适配器，优先复用 `systematic-debugging` 和 `root-cause-tracing`，再总结证据、根因状态、影响范围和修复路由。

- **`ccdawn-evaluation`**
  CCDawn 评估适配器，只在没有更具体的 review、debug、planning、verification、feedback 或 goal skill 承接时使用。

- **`ccdawn-dawn-agent-html-memory`**  
  这是一个项目记忆 skill，用来在真实软件项目里创建并持续维护 `.docs/project-memory/`。它支持按职责拆分的多会话共享 lane，生成会聚合这些 lane 的 HTML 总览页，并在项目根目录生成一个 `PROJECT_MEMORY.html` 快捷入口。

- **`ccdawn-goal-loop`**  
  这是一个目标执行 skill，用来把一个目标整理成带有证据、限制条件、允许范围、下一步判断规则和阻塞停止报告的可执行合同。

### Research

- **`ccdawn-competition-research-lifecycle`**  
  这是一个面向研究竞赛和 benchmark 项目的端到端工作流 skill，覆盖任务定义、数据准备、文献和方案调研、baseline 搭建、训练与实验、分析与消融、论文写作和提交打包。

  它把 `ccdawn-brt` 视为流程治理层，用来定义每个阶段的目标、评审点和验收标准，同时附带参考指南、更紧的响应契约，以及可直接复用的阶段模板。

### Competition

- **`ccdawn-score-loop`**
  通用 score loop 模板，用来处理 benchmark、榜单、validation、baseline promotion、worker lane、online/offline feedback 和提交包迭代。

- **`ccdawn-huawei-nslb-score-loop`**  
  Huawei Algorithm Challenge 37 NSLB 项目的 score loop 适配层，基于通用模板保留项目命令、ledger、mutation space、online feedback 和打包规则。

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
INSTALL_PROMPTS.md
install.ps1
install.sh
skills/
  competition/
    README.md
    ccdawn-score-loop/
    ccdawn-huawei-nslb-score-loop/
  creative/
    README.md
    ccdawn-creative-toolbox/
  engineering/
    README.md
    ccdawn-dawn-agent-html-memory/
    ccdawn-brt/
    ccdawn-feature-reuse-research/
    ccdawn-planning/
    ccdawn-task-splitting/
    ccdawn-bdd-tdd-development/
    ccdawn-completion-summary/
    ccdawn-pr-review/
    ccdawn-project-review/
    ccdawn-bug-review/
    ccdawn-evaluation/
    ccdawn-goal-loop/
  research/
    README.md
    ccdawn-competition-research-lifecycle/
scripts/
  install_codex_library.py
```

## 安装细节

也可以直接调用 Python 安装器：

```bash
python scripts/install_codex_library.py
```

安装器会把已发布 skill 复制成真实目录，检查目录名是否和 `SKILL.md` 的 `name` 字段一致，并在本机存在 Codex `quick_validate.py` 时校验 live skill。

只演练安装计划，不改文件：

```bash
python scripts/install_codex_library.py --dry-run
```

列出当前仓库可安装的 skills：

```bash
python scripts/install_codex_library.py --list
```

只验证已经安装到 Codex live 目录的副本，不重新安装：

```bash
python scripts/install_codex_library.py --verify-only
```

只安装部分 skill：

```bash
python scripts/install_codex_library.py --skill ccdawn-brt --skill ccdawn-dawn-agent-html-memory
```

安装目标选项：

```bash
python scripts/install_codex_library.py --agent codex         # 默认 live Codex 目标
python scripts/install_codex_library.py --agent agents        # 可选本地 catalog 副本
python scripts/install_codex_library.py --agent claude        # 可选 Claude 全局副本
python scripts/install_codex_library.py --agent codex-agents  # Codex 加 .agents
python scripts/install_codex_library.py --agent all           # 所有支持目标
```

只有在明确需要重复入口时，才把同一个 skill 同时安装到 `.codex/skills` 和 `.agents/skills`。

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
- `用 ccdawn-pr-review 在合并前审阅这个 PR`
- `用 ccdawn-project-review 在重构前审查这个仓库`
- `添加复杂编辑器模块前先用 ccdawn-feature-reuse-research 做复用调研`
- `用 ccdawn-bug-review 包装 systematic-debugging 来审查这个回归`
- `用 ccdawn-evaluation 在检查更具体 skill 后评估这个流程`
- `用 ccdawn-score-loop 跑这个 benchmark 优化循环`
- `用 ccdawn-huawei-nslb-score-loop 准备 NSLB epoch 并 gate child results`
- `用 ccdawn-creative-toolbox 基于当前上下文生成新概念卡`
- `帮我给这个仓库初始化项目记忆`
- `使用 ccdawn-dawn-agent-html-memory 把这个仓库按 frontend 项目初始化项目记忆`

这个仓库按本地 skill library 维护。
