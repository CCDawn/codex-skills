# CCDawn Codex Skills

[![Release](https://img.shields.io/github/v/release/CCDawn/codex-skills?display_name=tag)](https://github.com/CCDawn/codex-skills/releases)
[![Validate](https://github.com/CCDawn/codex-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/CCDawn/codex-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/CCDawn/codex-skills)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-21-2f81f7)](#完整-skill-目录)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f883d)](https://agentskills.io/)

**让 Codex 先理解你，再决定怎么做。**

21 个中文优先 Agent Skills，覆盖意图对齐、动态路由、轻量开发、代码审查、UI 设计和 AI 研究工作流。

- 用户正常说需求即可，不需要主动输入 `/brt` 或记忆流程命令。
- [`ccdawn-brt`](skills/engineering/ccdawn-brt/SKILL.md) 会在意图明确时直接推进，在高影响歧义出现时集中讨论并给出推荐。
- 简单任务直接实现和验证；只有真实风险存在时才升级到规划、拆分或紧凑 TDD。

[English](README.en.md) | **简体中文**

## 20 秒看懂 BRT

![BRT 从意图对齐到自动路由、实施与验证的演示](assets/brt-demo.gif)

这是一个流程示例：用户只需正常表达需求；BRT 会先查证可用上下文，只讨论会改变结果的问题，然后把已对齐的任务交给最具体的 Skill。

## 快速体验

先预览最重要的入口 Skill：

```powershell
gh skill preview CCDawn/codex-skills ccdawn-brt
```

使用 Agent Skills CLI 查看或安装：

```powershell
npx skills add CCDawn/codex-skills --list
npx skills add CCDawn/codex-skills --skill '*' -g -a codex -y
```

需要 CCDawn 完整安装策略，包括安装演练、live copy 验证和可逆处理冲突入口时，使用仓库安装器：

```powershell
git clone https://github.com/CCDawn/codex-skills.git
Set-Location codex-skills
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

macOS/Linux：

```bash
git clone https://github.com/CCDawn/codex-skills.git
cd codex-skills
sh ./install.sh
```

默认只安装到 `~/.codex/skills/<ccdawn-skill-name>`，不会同时写入 `~/.agents/skills` 造成重复入口。高级选项见[安装细节](#安装细节)。

## 为什么使用 CCDawn

| 常见问题 | CCDawn 的处理方式 |
| --- | --- |
| 用户没有写完整规格 | 先读取可查证上下文，再讨论真正会改变结果的问题 |
| Skill 很多但不会自动选 | BRT 选择最具体 owner，并可动态组合多个意图 |
| 简单修改被流程拖慢 | 按子任务风险控制重量，默认优先直接实现和验证 |
| 审查只给结论、不继续推进 | 形成按依赖排序的行动队列，在边界内连续处理 |
| AI 研究和普通开发混用流程 | 分离研究实验、评分循环、严谨性审查和软件 TDD |

## 精选 Skill

- [`ccdawn-brt`](skills/engineering/ccdawn-brt/SKILL.md)：默认适配层，负责意图理解、讨论式对齐、路由和流程重量控制。
- [`ccdawn-bug-review`](skills/engineering/ccdawn-bug-review/SKILL.md)：从症状和失败证据定位根因，完成有界修复与验证。
- [`ccdawn-pr-review`](skills/engineering/ccdawn-pr-review/SKILL.md)：按风险排序审查 PR、diff、分支和合并准备度。
- [`ccdawn-ui-design`](skills/engineering/ccdawn-ui-design/SKILL.md)：处理 UI/UX、响应式、无障碍和浏览器视觉验证。
- [`ccdawn-ai-research-loop`](skills/research/ccdawn-ai-research-loop/SKILL.md)：复现 baseline，推进假设、实验、消融与研究方向收敛。
- [`ccdawn-feature-reuse-research`](skills/engineering/ccdawn-feature-reuse-research/SKILL.md)：为复杂功能评估项目内外可复用方案。

## 懒人安装

不想手动 clone、找目录或运行命令时，把下面的提示词直接发给 Codex。

<details>
<summary>展开一键安装提示词</summary>

```text
请帮我一键安装 CCDawn 的 Codex skills 技能包。

仓库地址：https://github.com/CCDawn/codex-skills.git

要求：
1. 如果本机已有这个仓库，就进入仓库并更新到最新 main；如果没有，就 clone 到一个合适的本地目录。
2. 只安装到当前用户的 Codex live skills 目录：~/.codex/skills。
3. 不要安装到 ~/.agents/skills，避免重复 slash-command。
4. 先运行安装演练，再执行正式安装。
5. 安装后验证 live skills 是否可用。
6. 使用安装脚本默认可逆停用安装器识别的完整 Superpowers 自动发现入口集，保留原目录和内容，不要删除。
7. 最后用中文汇报：仓库位置、安装目录、安装了哪些 skills、冲突入口处理、验证是否通过、是否需要重启 Codex。
8. 重点提醒我：最重要入口是 ccdawn-brt；用户正常说需求即可。意图明确时直接推进；意图不清且误解会返工时，BRT 要先说明当前理解和依据，一次集中讨论 2-4 个高影响问题并给出推荐，用户可回复“按推荐”完成对齐，然后自动路由。

如果遇到 Git、Python、网络、权限问题，只问我一个最关键的阻塞问题。
```

</details>

需要更严格限制写入范围时，用[强约束版安装提示词](INSTALL_PROMPTS.md#强约束版)。

## 完整 Skill 目录

### 工程流程

- **`ccdawn-brt`**  
  CCDawn 最重要入口 skill。高置信度任务直接推进；低置信度且误解会返工时，先查证，再用一轮讨论式追问确认结果、范围、非目标和验收。每个问题提供具体推荐、理由和错判影响，用户可以只纠正不对的项。

- **`ccdawn-ui-design`**
  UI/UX 专项 owner，负责信息层级、交互状态、响应式、无障碍和浏览器视觉验证；机械前端小改不会自动升级成设计流程。

- **`ccdawn-feature-reuse-research`**
  只在复用候选会实质改变复杂功能的架构、依赖或实现范围时调研现有项目、库、标准、示例和项目内模块。

- **`ccdawn-planning`**
  只在真实设计分叉、高风险顺序或跨边界交接需要可复用方案时触发；默认方案完成后由当前 owner 直接实施。

- **`ccdawn-task-splitting`**
  只在已确认存在独立依赖、owner、风险或验证边界时建立最小任务图；普通 `NO_SPLIT` 不进入此阶段。

- **`ccdawn-bdd-tdd-development`**
  仅对复杂、高回归风险子任务使用紧凑 TDD；复用已有 RED、运行窄验证，默认不派发逐任务子代理和 reviewer 链。

- **`ccdawn-completion-summary`**
  只为跨阶段综合、恢复、正式交接、PR/发布前证据生成持久总结；普通实现由当前 owner 直接收口。

- **`ccdawn-pr-review`**
  PR 审阅阶段 skill，用来把 PR、分支、提交范围或本地 diff 对照已确认需求、任务证据、回归风险和合并准备度进行审查。

- **`ccdawn-project-review`**
  项目审查 skill，用来审查整个仓库、架构、技术债、测试缺口、可维护性、接手状态和项目健康。

- **`ccdawn-simplification-review`**
  当前 diff 的精简审查 skill，用来寻找可删除代码、原生/标准库替代、无效抽象和不必要依赖；不替代正确性审查。

- **`ccdawn-simplification-audit`**
  整仓或子系统精简审计 skill，用来形成证据化复杂度 findings 和按风险排序的精简队列。

- **`ccdawn-bug-review`**
  紧凑 bug owner，直接完成证据收集、根因定位、契约内最小修复和验证；只有深层来源才加载 `root-cause-tracing`。

- **`ccdawn-evaluation`**
  CCDawn 评估适配器，只在没有更具体的 review、debug、planning、verification、feedback 或 goal skill 承接时使用。

- **`ccdawn-dawn-agent-html-memory`**  
  按需维护 `.docs/project-memory/` 的跨会话状态、关键决策、blocker、lane 和 HTML 总览；普通开发不会自动初始化、同步或创建 claim。

- **`ccdawn-goal-loop`**  
  这是一个目标执行 skill，用来把一个目标整理成带有证据、限制条件、允许范围、下一步判断规则和阻塞停止报告的可执行合同。

### 研究流程

- **`ccdawn-ai-research-loop`**
  AI 研究工程主流程，负责 baseline 复现、可证伪假设、最小实验、多轮 findings 综合，以及继续、分支、转向或停止决策。

- **`ccdawn-research-rigor-review`**
  重要 baseline、反直觉结果和论文级结论晋升前的轻量严谨性审查；普通实验 lane 不强制触发。

- **`ccdawn-competition-research-lifecycle`**  
  这是一个面向研究竞赛和 benchmark 项目的端到端工作流 skill，覆盖任务定义、数据准备、文献和方案调研、baseline 搭建、训练与实验、分析与消融、论文写作和提交打包。

  它把 `ccdawn-brt` 视为流程治理层，用来定义每个阶段的目标、评审点和验收标准，同时附带参考指南、更紧的响应契约，以及可直接复用的阶段模板。

### 竞赛与评分

- **`ccdawn-score-loop`**
  通用 score loop 模板。实验使用 `BASELINE/CANDIDATE/DELTA/GATE`，分数回退或假设失败不进入 TDD；只有分离出的确定性工程 bug 才临时使用 RED/GREEN。

- **`ccdawn-huawei-nslb-score-loop`**  
  Huawei Algorithm Challenge 37 NSLB 项目的 score loop 适配层，基于通用模板保留项目命令、ledger、mutation space、online feedback 和打包规则。

### 创意工具

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
- 正式安装到 `~/.codex/skills/<ccdawn-skill-name>` 时，优先运行 `install.ps1` / `install.sh`，或直接调用 Python 安装器，使用真实目录复制。
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
    ccdawn-ui-design/
    ccdawn-feature-reuse-research/
    ccdawn-planning/
    ccdawn-task-splitting/
    ccdawn-bdd-tdd-development/
    ccdawn-completion-summary/
    ccdawn-pr-review/
    ccdawn-project-review/
    ccdawn-simplification-review/
    ccdawn-simplification-audit/
    ccdawn-bug-review/
    ccdawn-evaluation/
    ccdawn-goal-loop/
  research/
    README.md
    ccdawn-ai-research-loop/
    ccdawn-research-rigor-review/
    ccdawn-competition-research-lifecycle/
scripts/
  install_codex_library.py
```

## 安装细节

也可以直接调用 Python 安装器。Windows PowerShell 推荐用 `py -3`；macOS/Linux 推荐用 `python3`。

```powershell
py -3 scripts\install_codex_library.py
```

安装器会先运行 CCDawn package validator，再把已发布 skill 复制成真实目录，检查目录名是否和 `SKILL.md` 的 `name` 字段一致，并在本机存在 Codex `quick_validate.py` 时校验 live skill。`install.ps1` 和 `install.sh` 默认使用 `--process-skill-conflicts disable`：只把已识别 Superpowers skill 的 `SKILL.md` 改名为 `SKILL.md.ccdawn-disabled`，不删除目录或内容。

恢复这些入口：

```powershell
py -3 scripts\install_codex_library.py --agent codex --process-skill-conflicts restore
```

直接调用 Python 安装器时，默认只警告；要使用 BRT 的低噪声路由，显式加 `--process-skill-conflicts disable`。需要单独使用某个 Superpowers skill 时，可先恢复全部入口，再手动保留所需入口；恢复不会改变 CCDawn skills。

只演练安装计划，不改文件：

```powershell
py -3 scripts\install_codex_library.py --dry-run
```

列出当前仓库可安装的 skills：

```powershell
py -3 scripts\install_codex_library.py --list
```

只验证已经安装到 Codex live 目录的副本，不重新安装：

```powershell
py -3 scripts\install_codex_library.py --verify-only
```

只安装部分 skill：

```powershell
py -3 scripts\install_codex_library.py --skill ccdawn-brt --skill ccdawn-dawn-agent-html-memory
```

安装目标选项：

```powershell
py -3 scripts\install_codex_library.py --agent codex         # 默认 live Codex 目标
py -3 scripts\install_codex_library.py --agent agents        # 可选本地 catalog 副本
py -3 scripts\install_codex_library.py --agent claude        # 可选 Claude 全局副本
py -3 scripts\install_codex_library.py --agent codex-agents  # Codex 加 .agents
py -3 scripts\install_codex_library.py --agent all           # 所有支持目标
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

macOS/Linux：

```bash
bash scripts/link-skills.sh
```

Windows PowerShell：

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

## 开发

- [贡献指南](CONTRIBUTING.md)
- [MIT 许可证](LICENSE)

## 使用方式

安装后建议把 `ccdawn-brt` 作为主入口。用户不需要记固定口令或主动声明流程，正常说需求即可，例如：

- `修一下这个登录 bug`
- `帮我审这个 PR`
- `先审查一下这个项目结构`
- `我要加一个复杂编辑器功能`
- `这个 benchmark 分数退化了，帮我分析并继续优化`
- `帮我把这个目标拆成可验证的执行计划`
- `帮我给这个仓库初始化项目记忆`

BRT 会根据意图置信度控制交流成本：

- 需求明确：直接执行或路由，不为了展示流程而追问。
- 需求存在多种合理解释：先读取可查证的上下文，再用一条消息集中讨论 2-4 个会改变结果的问题。
- 讨论时 agent 会先说明当前理解、依据和推荐；用户可以回复 `按推荐`，也可以只指出需要修改的编号。
- 信息足够后立即继续，不重复确认已经对齐的内容；只有缺少不可替代输入时才单独询问阻塞问题。

例如输入 `优化一下这个页面，但我还不确定应该优先改视觉还是操作流程`，BRT 应先结合现有页面形成判断，再与用户讨论目标结果、改动范围和验收方式，而不是直接改代码或只路由到 UI skill。

这个仓库按本地 skill library 维护。
