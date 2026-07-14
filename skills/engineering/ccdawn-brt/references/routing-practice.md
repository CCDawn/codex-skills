# BRT Routing Practice

只在 BRT 无法从主文件稳定选择 owner 时读取。先检查本轮 Available skills；未出现的 skill 不能成为 owner，也不为普通任务临时安装。

## 仲裁顺序

1. 锁定可观察结果、对象、允许动作和成功证据。
2. 选择能直接产生下一结果的最具体 owner，而不是流程阶段名。
3. 只在 primary owner 缺少专属工具、知识或独立证据时增加一个 support skill。
4. `Next Output` 或 `Success Evidence` 仍含糊时，先查证；`LOW` 用一次集中讨论，`BLOCKED` 只问一个必要问题。

## 核心路由表

| 用户信号 | Primary owner | 默认重量 | 下一产出 |
|---|---|---|---|
| 修 bug、异常、失败测试、性能症状有明确对象 | `ccdawn-bug-review` | FAST/COMPACT | 根因状态、最小修复、验证 |
| 审 PR、diff、branch、commit、merge readiness | `ccdawn-pr-review` | COMPACT | findings-first 审阅结论 |
| 审整仓、架构、技术债、测试体系、接手摸底 | `ccdawn-project-review` | COMPACT | 风险排序 findings 与执行队列 |
| 评价流程、方案、skill、输出质量，且无更具体 owner | `ccdawn-evaluation` | MICRO/COMPACT | 证据化判断与高 ROI 建议 |
| 新建或重定 UI/UX、信息层级、交互模型、响应式或无障碍决策 | `ccdawn-ui-design` | FAST/COMPACT | 可实施 UI 契约 |
| 已有 UI 契约或项目模式，需要组件、状态、响应式和无障碍生产实现 | `ccdawn-frontend-engineering` | FAST/COMPACT | 前端代码与浏览器运行证据 |
| 审查已有页面、截图、UI 流程、视觉回归、响应式或无障碍 | `ccdawn-ui-review` | COMPACT | findings 与浏览器证据 |
| 复杂功能存在实质性的外部复用决策 | `ccdawn-feature-reuse-research` | COMPACT | 复用/借鉴/自建判断 |
| 目标已对齐但有真实设计分叉、迁移或跨边界契约 | `ccdawn-planning` | COMPACT/FULL | 最小实施方案 |
| 已确认存在独立交付、owner、依赖或验证边界 | `ccdawn-task-splitting` | COMPACT | 可执行任务图 |
| 确定性行为回归或高风险工程契约需要 RED | `ccdawn-bdd-tdd-development` | COMPACT | 紧凑 RED/GREEN 实现 |
| AI/ML baseline、假设、消融、方向选择 | `ccdawn-ai-research-loop` | COMPACT/FULL | 研究闭环或下一实验 |
| 单条 benchmark/score/baseline promotion lane | `ccdawn-score-loop` | COMPACT/FULL | candidate 评估与晋升结论 |
| Huawei Algorithm Challenge 37 NSLB 项目 score lane | `ccdawn-huawei-nslb-score-loop` | COMPACT/FULL | 项目命令与 ledger 适配后的 score loop |
| 重要研究 claim、反直觉结果、baseline 晋升审查 | `ccdawn-research-rigor-review` | COMPACT | ACCEPT/QUALIFY/REJECT |
| 竞赛/benchmark 全生命周期 | `ccdawn-competition-research-lifecycle` | FULL | 阶段契约与下游 owner |
| 用户明确需要持久目标、反复迭代和 stop condition，且无专项 owner | `ccdawn-goal-loop` | COMPACT/FULL | 有界 goal contract 与下一轮证据 |
| 多会话进度、冲突、暂停恢复、讨论或合并 | `ccdawn-thread-coordination` | COMPACT | registry 状态或协调闭环 |
| 用户/项目明确要求 memory、dashboard、跨会话恢复 | `ccdawn-dawn-agent-html-memory` | FAST/COMPACT | 持久 delta 或恢复上下文 |
| 已验证工作存在临时产物、旧 branch/worktree/claim | `ccdawn-development-cleanup` | FAST/COMPACT | CLEAN/NOOP/DEFERRED/BLOCKED |
| 当前 diff/PR 是否过度设计 | `ccdawn-simplification-review` | COMPACT | 可删与保留判断 |
| 整仓/子系统冗余复杂度与依赖膨胀 | `ccdawn-simplification-audit` | COMPACT | 排序后的精简队列 |

系统或插件 skill 仅在本轮 Available skills 中真实存在且比 CCDawn fallback 更具体时使用，例如官方文档、浏览器、GitHub、PDF、表格或图像工具。候选安装资料属于 `github-skill-candidates.md`，不属于运行时路由表。

## 相邻边界

- PR/diff 正确性由 PR review 主责；只有目标明确指向删减时才叠加 simplification review。
- UI PR 仍由 PR review 主责；只有需要真实界面证据时才把 UI review 作为 support，不重复审查同一代码风险。
- 具体 bug 交给 bug owner；整仓测试健康度和架构风险交给 project review。
- planning 解决设计分叉；task splitting 只表达真实独立边界，不能用来输出 `NO_SPLIT`。
- 实验 metric 未提升不是 TDD RED；确定性 harness/parser/schema bug 才进入工程 TDD。
- UI 文件的机械修改可留在 FAST_PATH；产品、交互或视觉结果未定时由 UI design 主责，结果已定且主要工作是生产实现时由 frontend engineering 主责。
- 普通完成由当前 owner 收口；正式跨阶段证据包才进入 completion summary。

## 多动作推进

同一请求产生多个后续动作时：

- 按依赖、用户价值、误改风险和验证成本排序，不按严重度机械排序。
- `SAFE_DIRECT` 在已有执行许可下依次修复并验证，不完成一个就停下来询问。
- `PLAN_THEN_EXECUTE` 先形成必要方案，再自动回到执行。
- `DEFERRED` 只记录触发条件；`BLOCKED` 才停止并问一个问题。
- 只有用户必须选择顺序、范围或高风险动作时才展示选项。

## 路由失败信号

- 明确小改被升级为 planning、task graph、TDD、worktree、子代理或 completion summary。
- 只输出“建议进入某 skill”，却说不出下一产出和成功证据。
- 推荐候选宽泛，无法说明具体行为差异和错判成本。
- 需求 `LOW` 时只路由不对齐，或把本地可查问题抛给用户。
- 多个 `SAFE_DIRECT` 项只推荐一个，却没有依赖、权限或风险阻塞。
- 把发送 pause 当作已暂停，或 owner 在 `resumePendingAgentIds` 清零前结束。
- 把未安装 skill 当作唯一 owner，或为普通任务搜索/安装新 skill。
- 为同一子任务同时加载功能重叠的 review、TDD、debug 或 summary skill。
- 完成后无真实残留仍加载 cleanup，或有残留却只输出泛化提醒。

出现这些信号时回到 BRT 主文件，重新选择最具体 owner 和最低充分流程重量。
