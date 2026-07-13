---
name: ccdawn-project-review
description: Use when CCDawn workflow needs a Chinese-first review of an entire repository, codebase, architecture, technical debt, test coverage, risk modules, maintainability, onboarding state, or project health before planning, refactoring, takeover, or prioritization.
license: MIT
---

# CCDawn Project Review

## 目标

对整个项目或一个明确子系统做只读、证据化审查，找出最影响后续完成率和误改率的结构性问题。

本 skill 不是 PR review，也不是直接修 bug。它回答：

- 这个项目当前健康吗；
- 哪些模块最值得先看、先测、先修；
- 哪些风险会影响后续开发、迁移、发布或接手；
- 下一步应该路由到哪个更具体的 CCDawn skill。

## BRT interface

- Context Boundary: 本次审查范围、实际读取的目录/入口/测试/配置/日志/git 信号/memory，以及明确排除范围。
- Output Contract: 项目健康结论、证据化 findings、行动队列、可选 Ordered Fix Queue、下一步路由。
- Allowed Action: 默认只读审查；不编辑文件、不移动分支、不改 index；用户要求边审边改时先回 `ccdawn-brt` 建立 Execution Contract。
- Success Evidence: findings 均有位置/命令/文件证据，行动队列能路由到具体 skill 或阶段。
- Stop Condition: 审查范围不明、需要写代码、发现 PR/diff 对象、发现具体 bug 需转调试、或用户目标变成实施。
- Route Out: `ccdawn-planning`、`ccdawn-bug-review`、`ccdawn-pr-review`、`ccdawn-completion-summary`、`ccdawn-evaluation`、`ccdawn-brt` 或 BLOCKED。

## 统一输出标准

- 用户可见输出默认中文；只有代码、命令、路径、错误原文、API/协议名、skill 名、状态枚举和外部专名保留英文。
- 报告、方案、审查、阶段文档和交接摘要使用中文标题与中文字段；内部字段对外翻译为：上下文边界、输出契约、允许动作、成功证据、停止条件、路由出口、下一步建议。
- 若必须保留英文状态或枚举，先用中文解释其含义。
- 用户可见正文末尾保留 `下一步建议: ...`，除非被更高优先级系统附录隔开。

## Owner 接入规则

进入本 skill 前先做轻量 owner 自检：

- 如果用户主目标不属于本 skill 的 owner 范围，不继续执行；回 `ccdawn-brt` 做 Owner 仲裁，或转交更具体 owner。
- 如果本 skill 只覆盖复合任务的一部分，只处理当前路由契约覆盖的 Primary/Secondary，不吞掉其他 owner。
- 如果发现 planning/development 正在替代更具体 owner，先输出路由修正，再进入正确 owner。

## 进入条件

使用前确认：

- 用户目标是审项目、审代码库、审架构、看技术债、看测试缺口、接手摸底、重构前盘点或判断项目健康；
- 当前工作区是可读取的项目目录；
- 审查范围已知：整个 repo、某个 package、某个模块、某条业务链路，未知时先用 `ccdawn-brt` 对齐；
- 默认只读，不编辑代码、不移动分支、不改 index。

如果用户要审的是 PR/diff/分支，使用 `ccdawn-pr-review`。如果用户报告具体 bug、失败测试或异常行为，使用 `ccdawn-bug-review`。

## 审查深度

先按项目大小和用户目标选择深度：

- QUICK：轻量摸底，适合“这个项目大概怎么样”“先看一眼”；只读目录、README、配置、测试入口、近期 git 信号。
- STANDARD：默认审项目；结合目录、关键文件、git 历史、测试/CI、依赖和核心链路。
- DEEP：重构、接手、发布前或高风险项目；增加热点文件、bug 磁铁、模块边界、测试有效性、数据/权限/迁移风险。

不要为了全面而扫描全仓。先找高信号入口，再钻关键模块。

## 证据采集

按需要选择，保持只读：

- 项目入口：README、package/pyproject/Cargo/go.mod、workspace 配置、启动脚本、CI、测试命令。
- 结构：目录分层、核心模块、跨层依赖、重复实现、废弃路径。
- git 信号：近期高频修改文件、多人改动热点、反复修 bug 的文件、长期无人维护的关键文件。
- 测试：测试入口、覆盖关键路径的测试、失败/跳过/脆弱测试、缺少回归锚点的高风险模块。
- 运行与配置：环境变量、迁移、feature flag、部署脚本、数据路径、权限边界。
- 文档与记忆：项目 memory、架构文档、决策记录、TODO/FIXME、已知风险。

常用只读命令示例：

```text
git status --short
git log --oneline --decorate -20
git log --name-only --pretty=format: --since="90 days ago"
rg -n "TODO|FIXME|HACK|deprecated|legacy|skip|only|flaky"
rg --files
```

PowerShell 下不要依赖 Bash-only 语法；路径用 `-LiteralPath` 或明确数组。

## 审查维度

默认选 4-6 个最相关维度，不全量铺开：

- 项目地图：主要模块、入口、数据流、外部依赖是否清楚。
- 热点与风险模块：修改频繁、反复出 bug、多人交叉维护或高耦合文件。
- 架构边界：分层是否清晰，是否存在循环依赖、跨层调用、重复抽象、单一事实源混乱。
- 测试质量：关键路径是否有测试，测试是否验证真实行为，是否存在脆弱/跳过/只测 mock 的问题。
- 可维护性：复杂度、命名、错误处理、配置分散、文档缺口是否阻碍后续 agent 接续。
- 安全与数据：权限、密钥、日志泄漏、删除/迁移、隐私、外部输入风险。
- 发布与运维：CI、部署、回滚、监控、迁移脚本、环境兼容风险。
- 用户价值：哪些问题最可能影响用户可见行为或任务完成率。

发现明确专项问题时路由：

- 具体 bug 或失败测试 -> `ccdawn-bug-review`
- PR/diff 合并前 -> `ccdawn-pr-review`
- 复杂新增功能、模块替换、开源库/项目复用价值评估 -> `ccdawn-feature-reuse-research`
- 需要方案 -> `ccdawn-planning`
- 需要任务拆分 -> `ccdawn-task-splitting`
- 完成状态/证据 -> `ccdawn-completion-summary`
- 安全专项 -> 已安装 `security-and-hardening` 时使用；否则用 `Defense-in-Depth Validation` 或保留在本 skill 做证据化风险审查
- 发布、CI 或合并前专项 -> 已安装 `gh-fix-ci` 时处理 CI；否则按对象路由到 `ccdawn-bug-review`、`ccdawn-pr-review` 或 `ccdawn-completion-summary`
- 性能专项 -> 已安装 `performance-optimization` / `react-component-performance` 时使用；否则保留在本 skill 并要求运行时或浏览器测量证据

## Findings 规则

每条 finding 必须有证据，不输出空泛建议。

严重度：

- P0：会导致无法运行、数据丢失、安全事故、错误发布或核心链路不可用。
- P1：高风险技术债、关键测试缺口、架构边界混乱、反复出 bug 的关键模块。
- P2：可维护性、局部测试缺口、配置/文档/错误处理问题，会增加后续误改率。
- P3：不阻塞但值得排期的清理、命名、文档或结构优化。

每条 finding 包含：

- 位置：文件、目录、命令输出或 git 信号；
- 问题：具体观察；
- 影响：为什么影响完成率、误改率、质量或风险；
- 建议：下一步最小有效动作；
- 路由：该回哪个 skill 或阶段。

## 行动队列

当 findings 指向多个后续动作时，先转成行动队列，再给下一步：

- Immediate Guardrail：低风险保护动作，例如关闭 stale claim、阻止误合、补发布/权限/删除防线。
- Primary Fix：证据最充分、最影响当前目标或用户可见链路的修复。
- Telemetry Gap：现有证据不足以定性为 bug，需要补日志、指标、probe 或复测。
- Deferred Refactor：维护性或结构性治理，当前目标不依赖时延后。

`WATCHLIST` 必须有退出条件：哪些指标、日志、测试、运行证据或时间窗口能证明关闭、降级或升级。Telemetry Gap 不要和确认型 P1 混在同一严重度里。

当行动队列里存在多个可连续修复项，再生成 Ordered Fix Queue：

- `Execution Order` 按依赖、改动范围、验证难度、误改风险和用户价值排序，不等同于 `Severity Rank`。
- 每项标记 `SAFE_DIRECT / PLAN_THEN_EXECUTE / DEFERRED / BLOCKED`。
- `SAFE_DIRECT` 可在用户说“继续/开始修复/按顺序修”后直接执行并验证。
- `PLAN_THEN_EXECUTE` 先进入 `ccdawn-planning` 或对应 owner；不要和低风险清理混做。
- `DEFERRED` 只记录触发条件；不在当前队列里顺手修。

## 输出契约

```text
项目审查:
- 范围: 整仓 / 子系统 / 模块...
- 深度: QUICK / STANDARD / DEEP
- 结论: HEALTHY / WATCHLIST / NEEDS_ATTENTION / HIGH_RISK / BLOCKED
- Context Boundary: 本次实际读取的目录、入口、测试、配置、日志、git 信号或 memory...
- Allowed Action: 只读审查；需要写代码时回 BRT 建立 Execution Contract
- 关键证据: ...

项目地图:
- 入口:
- 核心模块:
- 测试/CI:
- 数据/配置/外部依赖:

Findings:
- P0/P1/P2/P3: [位置] 问题；影响；建议；路由

风险热区:
- 模块/文件: 证据...；为什么优先...

测试与验证:
- 已有证据:
- 缺口:
- 建议补强:
- Success Evidence: findings 均有位置/命令/文件证据，行动队列能路由到具体 skill 或阶段
- Stop Condition: 审查范围不明 / 需要写代码 / 发现 PR/diff 对象 / 发现具体 bug 需转调试

行动队列:
- Immediate Guardrail: 证据...；动作...；路由...
- Primary Fix: 证据...；动作...；路由...
- Telemetry Gap: 证据缺口...；补证方式...；退出 WATCHLIST 条件...
- Deferred Refactor: 延后原因...；触发条件...

修复队列（仅多个可连续修复项时）:
- 1. ... [SAFE_DIRECT / PLAN_THEN_EXECUTE / DEFERRED / BLOCKED]；为什么排在这里...；Success Evidence...

下一步:
默认路由：<Ordered Fix Queue / ccdawn-planning / ccdawn-bug-review / ccdawn-pr-review / ccdawn-completion-summary / ccdawn-evaluation / ccdawn-brt / BLOCKED>，原因...
执行规则：若有多个可连续修复项，输出 Ordered Fix Queue 并在用户说“继续/开始修复/按顺序修”后从第 1 项推进；若只有一个明确后续 owner，直接路由；只有审查范围、修复顺序或高风险动作需要用户取舍时，才列出选项。

Route Out: Ordered Fix Queue / ccdawn-planning / ccdawn-bug-review / ccdawn-pr-review / ccdawn-completion-summary / ccdawn-evaluation / ccdawn-brt / BLOCKED
```

## 质量门槛

- 不编辑文件；如果用户要求边审边改，先用 `ccdawn-brt` 重新对齐并建立 Execution Contract。
- 不把“项目很复杂”“测试不足”“架构混乱”当 finding，必须落到证据和影响。
- 不用单一指标下结论；热点文件必须结合职责、测试、历史、风险一起解释。
- 不把所有 TODO 都当技术债；只报告影响任务完成、误改风险、用户行为或发布风险的项。
- 不建议大重构，除非已说明触发条件、收益、替代路径和验证方式。
- 不和 `ccdawn-pr-review` 抢职责；有具体 diff 时交给 PR review。
