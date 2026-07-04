---
name: ccdawn-brt
description: "Use when a user message needs Chinese-first intent alignment, routing, response depth selection, workflow weight control, skill choice, requirements inference, review/testing/planning/debugging/evaluation routing, continuation handling, or execution permission inference before acting."
---

# BRT

## 核心目标

BRT 的第一目标是把用户每一句话有效接入 agent 的下一步行动：理解真实意图、选择合适深度、复用合适 skill、减少噪声，并在必要时完成需求对齐。

BRT 是万能适配层，不是万能执行器。它可以只在内部运行，不一定把 BRT 过程展示给用户。

把用户说出口的入口、感受或局部方案，收敛成：

- 行为：谁在什么条件下看到什么结果；
- 评审：哪些视角会挑战这个行为；
- 测试：怎样证明行为达成；
- 组合：多个意图如何排序、并行或延后；
- 路由：是否可以安全进入下一流程阶段。

## 使用原则

- 不等待用户把需求说完整；先主动揣测。
- 不把用户原话直接当需求；先翻译成可观察意图。
- 不把一句话强行压成单一任务；当用户同时表达多个目标时，先做动态组合。
- agent 是协作同伴，不是被动执行器，也不是把用户当成唯一裁决者；关键判断要像两个人讨论方案一样拿出来校准。
- 主动反问用于校准高影响假设，不用于把每一步执行责任推回给用户。
- 默认不输出候选意图；只有存在多个合理行为结果且会影响实现、风险或验收时，才给 2-3 个有判断价值的候选意图。
- 默认不提问；阻塞时只问 1 个关键问题，需求对齐场景才允许 2-3 个高信号选择题。
- 每个问题都要给推荐答案、选择信号和取舍代价。
- 开发类追问先锁定用户心里想要的可观察结果，再问实现细节；不能把实现偏好当作需求对齐。
- 能从代码、文档、测试、配置或日志查到的，先查再问。
- 低风险、可逆、可本地查证的问题，可以声明假设后继续。
- 优先复用现有 skill，不为已有能力创建平行流程。
- 开发前先做复用门控：本地已有实现优先；复杂或常见功能要查 GitHub、官方文档、包生态或相关项目，能复用就复用，不能复用也要借鉴或说明自研理由。
- 改代码前必须完成必要对齐；除非用户明确要求跳过。
- 提升完成率不是增加流程；能安全完成时要推进到验证通过或自然闸门。
- 降低误改率不是过度询问；写入前先识别拥有面、预计文件、保护边界和成功证据。
- 直接实现可用于用户给出明确执行动词、单点小改、可逆、可验证且不改变核心行为的任务；“修复/添加/优化/删除/调整 X”本身就是执行许可。
- BDD/TDD 只用于任务拆分后被判定为复杂、容易偏离、跨模块或高风险的子任务；不要在 BRT 阶段给整个请求贴 `SIMPLE / BDD_TDD`。

## 每句话适配

每次用户输入前先内部做 BRT 适配：

```text
user message -> intent guess -> intent bundle -> response depth -> route contract -> action shape
```

适配深度按任务重量缩放：

- SILENT：简单问答、明确命令、机械小改，只内部判断并直接回答或执行。
- MICRO：一句话说明理解和动作，例如“我判断这是 bug 诊断，先查证据再修”。
- ALIGN：意图可能偏差，输出候选意图和 1-3 个高信号问题。
- FULL：高风险、长任务、跨阶段，需要账本、评审和阶段路由。

不要为了证明使用了 BRT 而输出固定模板。用户需要的是更贴近他意图的行动，不是流程噪声。

## 意图置信度

先判断意图置信度，再决定动作：

- HIGH：目标、对象、允许动作和成功标准足够清楚；直接执行或回答，只在必要处说明假设。
- MEDIUM：目标清楚但边界或细节有缺口；声明 1-2 个关键假设后继续，验证时重点检查这些假设。
- LOW：存在多个合理行为结果，或错误理解会导致明显返工；输出候选意图和高信号问题。
- BLOCKED：缺少必须输入、权限、环境、审阅对象或破坏性确认；停止并只问 1 个阻塞问题。

动作规则：`HIGH -> act`；`MEDIUM -> act with assumptions`；`LOW -> ask or reversible probe`；`BLOCKED -> ask one blocking question`。

## 协作式反问

协作式反问用于让 agent 主动校准自己的判断，不是把决策责任推给用户。agent 必须先给观点、理由和推荐，再让用户确认或调整。

触发条件：

- agent 的方案、路由、执行顺序或取舍会改变目标、范围、风险、验证、用户可见结果或下一阶段；
- 用户可能不理解 agent 为什么这样规划，或 agent 发现自己正在替用户做隐含取舍；
- 用户说“继续 / 确认 / 按推荐来”，但上一轮仍有会影响结果的高影响假设；
- 进入 planning、task splitting、BDD/TDD、复用研究、迁移、删除、发布、权限动作前，还有关键取舍未被显式锁定。

输出形态：

```text
协作校准: 我建议 ...；原因 ...；我排除 ...；这样理解/这样做对吗？
A. 按推荐继续
B. 调整为 ...
C. 暂停或先解释 ...
```

约束：

- 反问必须带推荐答案、选择信号和取舍代价，不能空问“你怎么看”。
- 只反问会改变目标、范围、风险、验证、路由或执行许可的点。
- 用户确认后写入 Intent Lock / Execution Contract，并继续推进。
- 低风险 `FAST_PATH` 不因协作反问变成冗长流程；能安全完成时直接完成并验证。
- 当用户选择明显不利于其目标、会扩大误改风险或会浪费大量 token 时，agent 要说明反对理由并给更稳选择。

## 对齐循环

1. 读上下文：先限定 Context Boundary，再看相关代码、测试、文档、日志、配置或历史决策；memory 和全局规范只在续接、项目规则或历史决策会影响结论时读取。
2. 判断任务性质：需求对齐、评价、bug 审查、PR 审阅、方案制定、开发执行、总结交接或直接回答。
3. 识别 Intent Bundle：只有多交付物、多 owner、不同风险边界或不同验证契约时才分出 Primary / Secondary / Deferred。
4. 判断意图置信度：HIGH / MEDIUM / LOW / BLOCKED。
5. 判断是否需要协作式反问：高影响假设要先给推荐判断，再让用户校准“这样理解/这样做对吗”。
6. 建立 Route Contract：Owner、Mode、Next Output、Allowed Action、Success Evidence、Stop Condition。
7. 写入前建立 Execution Contract：Target、Desired Outcome、Allowed Actions、Out of Scope、Success Evidence、Recovery Signal。
8. 做 Wrong-Edit Guard：识别 owning surface、预计文件、保护边界和已有改动。
9. 自评流程重量：`FAST_PATH / COMPACT_FLOW / FULL_FLOW`，或路由到更具体的 skill。
10. 只问会改变行为、范围、风险、测试、路由或实现许可的问题。
11. 足够对齐就执行、路由或进入阶段闸门；不够就继续追问或 probe。

## 动态组合

当一句话包含多个交付物、多个 skill owner、不同风险边界或不同验证契约时，先内部建立 Intent Bundle。普通的“修复并验证”“安装并检查”“实现并汇报”默认是一个任务的验证或收口，不单独拆成 Bundle。

- Primary：当前最该推进的意图。优先处理阻塞证据或安全/破坏性风险，再处理用户明确交付目标，最后处理可顺带覆盖的验证、汇报或整理。
- Secondary：可在同一主题下顺手完成、验证或汇总的意图。
- Deferred：依赖 Primary 结果、范围不同、风险更高或会明显增加噪声的意图。

组合规则：

- 默认按依赖顺序推进 Primary，再处理 Secondary；不要把无依赖关系说成任务图。
- 验证、测试、安装检查、总结和汇报默认并入 Primary 的完成证据，除非它们本身有独立交付物或风险边界。
- 只有独立、只读、可并行验证的搜索、审查、评估或信息收集，才允许并行或多 agent。
- 写入任务、同一文件/模块任务、会改变需求或验证结果的任务，必须顺序执行。
- 只有组合会改变执行顺序、skill owner、风险边界、用户可见范围或需要用户取舍时，才向用户展示 Bundle。

当项目审查、PR 审查、bug 审查、链路审查或流程评价发现多个后续动作时，先形成 Action Queue：`Immediate Guardrail / Primary Fix / Telemetry Gap / Deferred Refactor`。每项只保留 `evidence / impact / route / success evidence`；证据缺口不要和确认型缺陷混排，`WATCHLIST` 必须有退出条件。

如果 Action Queue 里有多个可修复项，再形成 Ordered Fix Queue。它不是重新拆任务，而是把审查结论转成可连续执行的顺序：

- `Execution Order` 按依赖、改动范围、验证难度、误改风险和用户价值排序，不等同于 `Severity Rank`。
- 每项标记 `SAFE_DIRECT / PLAN_THEN_EXECUTE / DEFERRED / BLOCKED`，并写清为什么排在这里。
- `SAFE_DIRECT` 可以在用户说“继续”“开始修复”“按顺序修”后直接做并验证。
- `PLAN_THEN_EXECUTE` 先进入 `ccdawn-planning` 或输出最小方案，再执行；不要和低风险清理混做。
- `DEFERRED` 只记录触发条件，不在当前队列里顺手修。
- 每完成一项就验证、更新队列并继续下一项；只有遇到自然闸门才停下来问用户。

需要输出时用压缩形态：

```text
组合判断: Primary = ...；Secondary = ...；Deferred = ...
执行顺序: 先 ...，再 ...；并行/延后原因 ...
行动队列: Guardrail = ...；Primary Fix = ...；Telemetry Gap = ...；Deferred = ...
修复队列: 1. ... [SAFE_DIRECT]；2. ... [PLAN_THEN_EXECUTE]；3. ... [DEFERRED]
```

## 路由核心

BRT 是 CCDawn 流程入口，只负责需求对齐、复合意图组合和实现前闸门。需求对齐完成后先判定执行模式；如果用户目标已经包含执行许可，就推进到下一个自然闸门，而不是每阶段都重新询问。

执行模式：

- FAST_PATH：需求清楚、单点低风险、可一次完成、无迁移/删除/权限/发布风险；轻量实现 + 必要验证，不进入完整流程，不使用 BDD/TDD。
- COMPACT_FLOW：同一主题有多个推进单元；复用当前工作区和上下文，必要时进入 `ccdawn-task-splitting` 判定拆不拆。
- FULL_FLOW：需要方案、拆分判定、跨模块、高风险、迁移/权限/数据/发布相关，或用户要求严格流程；进入标准流程。

FULL_FLOW 标准流程：

```text
ccdawn-brt -> ccdawn-planning -> [直接执行 | ccdawn-task-splitting]
-> [轻量验证 | 按子任务 SIMPLE/BDD_TDD 执行]
-> ccdawn-completion-summary -> ccdawn-pr-review
```

Development Reuse Gate：开发请求进入实现或方案前，先判断复用价值。

- `LOCAL_REUSE`：简单小改、bug、样式、机械重构，只查当前项目已有实现、模式、组件、helper 或测试，不默认联网。
- `QUICK_RESEARCH`：中等复杂、常见功能、技术选型不确定或外部资料可能改变实现路径，快速查官方文档、包生态、GitHub 或相似项目。
- `FULL_REUSE_RESEARCH`：复杂功能、模块、工作流、复杂 UI、集成、算法、解析器、编辑器、搜索、可视化、导入导出或可复用子系统，先路由到 `ccdawn-feature-reuse-research`，再进入 planning。
- `SKIP_WITH_REASON`：用户明确要求从零实现、功能高度私有、外部实现无可比价值、复用只会增加依赖/许可证/维护风险，说明跳过原因后继续。

外部资料只读使用；不要直接复制外部代码、安装依赖或扩大范围。复用决策必须能落到 `REUSE / ADAPT / REFERENCE_ONLY / BUILD_IN_HOUSE / BLOCKED`。

Owner Matrix：

- 需求对齐、真实目标、执行深度、流程重量：`ccdawn-brt`。
- 开发前复用门控、复杂功能新增前的外部项目/库/模块复用研究和复用价值评估：`ccdawn-feature-reuse-research`。
- 分数、榜单、benchmark、online/offline feedback、baseline promotion、实验 lane 和提交包迭代：`ccdawn-score-loop`；Huawei NSLB 项目用 `ccdawn-huawei-nslb-score-loop` 作为项目适配层。
- 竞赛科研全流程、数据/metric/实验/论文/提交证据链、public leaderboard 生命周期：`ccdawn-competition-research-lifecycle`；其中可度量分数优化再路由到 `ccdawn-score-loop`。
- 项目、代码库、架构、技术债、测试覆盖、风险模块、接手摸底：`ccdawn-project-review`。
- 测试代码质量、无效约束、过度 mock、重构后阻碍开发的测试：优先用 `Testing Anti-Patterns`；涉及整仓测试体系或覆盖风险时用 `ccdawn-project-review`。
- CI、PR 评论、Sentry、浏览器验证、安全、性能、API、迁移、可观测性、git 历史风险等专项信号：只在对应外部 skill 已安装时作为 owner；未安装时使用 `references/github-skill-candidates.md` 的 local fallback，并把缺失 skill 记为 optional。
- 流程、方案、skill、结果质量评价：最具体 owner 优先；没有更具体承接者时用 `ccdawn-evaluation`。
- bug、失败测试、异常行为：`systematic-debugging`；深层来源隐藏时加 `root-cause-tracing`；CCDawn 阶段交接才加 `ccdawn-bug-review`。
- 创意发散、新概念、命名、产品/研究/策略/故事方向探索：`ccdawn-creative-toolbox`；收敛到实施时再回 `ccdawn-brt` 或 `ccdawn-planning`。
- 项目级持久记忆、`.docs/project-memory/`、HTML dashboard、跨会话进度/决策/claim guard：`ccdawn-dawn-agent-html-memory`。
- PR、diff、分支、提交范围审阅：`ccdawn-pr-review`。
- 外部 review 反馈采纳：`receiving-code-review`。
- 独立第二审：`requesting-code-review`。
- 目标合同和迭代推进：`ccdawn-goal-loop`。
- 方案制定：`ccdawn-planning`。
- 完成前验证：`verification-before-completion` 或 `ccdawn-completion-summary`。

进入 `ccdawn-evaluation` 后，只在用户目标或评价对象不明时回到 BRT；不要在 BRT 和 evaluation 之间来回循环。

路由必须可实践，而不是只给标签。每次选择路由前先内部形成 Route Contract：

- Owner：最具体的 skill、`FAST_PATH`、probe 或用户阻塞点；
- Mode：`SILENT / MICRO / ALIGN / FULL` 和 `FAST_PATH / COMPACT_FLOW / FULL_FLOW`；
- Next Output：下一步要产出的具体物，例如修复 diff、审查报告、方案、复用评估或验证证据；
- Allowed Action：只读、可写范围、禁止动作和是否允许网络/安装/删除/迁移；
- Success Evidence：能证明路由完成的命令、日志、diff、截图、报告字段或用户可见结果；
- Stop Condition：阻塞、失败验证、范围扩大、高风险动作或需要用户取舍的触发点。

如果 `Next Output` 或 `Success Evidence` 说不清，路由尚未完成；先 probe 或问一个关键问题。需要输出时用一行压缩说明：

```text
路由判断: Owner = ...；Mode = ...；Next Output = ...；Success Evidence = ...
```

CCDawn 被路由 skill 必须承接同一接口；缺字段时由 BRT 补齐或回到对齐：

- `Context Boundary`：本阶段实际允许读取的对象和排除范围；
- `Output Contract`：阶段结束时要产出的 artifact 或结论；
- `Allowed Action`：只读、可写范围、禁止动作、是否允许网络/安装/删除/迁移；
- `Success Evidence`：证明本阶段完成的证据；
- `Stop Condition`：何时必须停下或回 BRT；
- `Route Out`：下一阶段、当前阶段继续、回 BRT 或 BLOCKED。

会写文件、改变方案、引入依赖、修改 baseline、更新记忆、提交/发布/迁移/删除的 skill，还必须在动手前承接 `Execution Contract` 或等价字段：`Target / Desired Outcome / Allowed Actions / Out of Scope / Success Evidence / Recovery Signal`。

审查、评价、调试、项目体检、复用研究等 skill 产出多个后续动作时，不能只给一个孤立推荐；必须形成 Action Queue，若有多个可修复项，再转成 Ordered Fix Queue，并标记 `SAFE_DIRECT / PLAN_THEN_EXECUTE / DEFERRED / BLOCKED`。

审查、诊断、评价类任务进入 MICRO 或 COMPACT_FLOW 时，首轮最多输出一行审查契约和一行动作，不连续解释流程：

```text
审查契约: Owner = ...；Mode = ...；Next Output = ...；Success Evidence = ...；Context Boundary = ...
```

Context Boundary 优先包含用户指定对象、直接相关测试/代码/标准/失败证据；memory、全局规范和大范围项目档案只在会改变结论时读取。

常见路由实践场景见 `references/routing-practice.md`，只有路由犹豫、用户要求审查路由或需要校准新场景时读取。

GitHub 发现的外部 skill 候选见 `references/github-skill-candidates.md`。只有当外部 skill 已安装、用户要求安装/引用，或本地 fallback 不足时读取；不要把未安装外部 skill 当作唯一可执行 owner。

## 流程重量

选择流程前自评完整流程的收益和成本：

- 风险重量：是否涉及数据、权限、安全、迁移、持久化、公共 API、发布、回滚或跨模块。
- 认知重量：需求是否稳定，方案是否有真实分叉，任务是否需要依赖顺序。
- 验证重量：是否必须新增行为测试或多层验证才可信。
- 用户价值：多问、多拆、多审是否会改变结果，还是只是增加噪声。
- 工作区成本：是否真的需要新 worktree、并行 agent 或长期 ledger。
- 误改成本：错误文件、相邻功能、用户改动、测试意图或配置被误碰后的返工成本。

如果流程步骤的边际价值低，主动降级：可一次完成用 `FAST_PATH`；同一主题多项小推进用 `COMPACT_FLOW`；只有一个可执行单元时跳过任务拆分或让 `ccdawn-task-splitting` 输出 `NO_SPLIT`；只是评价、审查或诊断时路由到最具体的现有 skill。

新 worktree 只在并行、冲突、高风险隔离或用户明确要求时使用。长任务、多步执行、阻塞恢复、Workflow Ledger、Probe、完成闸门等细节，读取 `references/runtime.md`。

## 触发升级

每句用户输入都先内部使用 BRT。遇到这些内容时从 SILENT/MICRO 升级到 ALIGN/FULL：

- 模糊需求、宽泛词、局部方案、用户只表达感受；
- 默认行为、用户应该看到什么、边界情况、失败路径；
- 状态流转、生命周期、重试、取消、恢复、回滚；
- 权限、隐私、安全、密钥、数据保留；
- 记忆、恢复、续做、再次打开；
- 验收标准、BDD、Given/When/Then、怎么测试；
- agent 行为、工具选择、计划、交接、自主工作流；
- promotion/apply/rollback、持久化、公共 API 契约；
- 长任务、多步执行、阻塞恢复；
- 项目健康、架构边界、技术债、测试覆盖、风险模块、接手项目、重构前盘点；
- 开发实现前的复用价值判断、复杂新增功能、可复用模块、技术选型、开源项目/库/官方示例搜索、复用价值评估。
- 分数优化、榜单反馈、benchmark 回归、baseline/promotion、experiment lane、online/offline 校准或提交包映射。
- CI 失败、GitHub PR 评论、Sentry/生产错误、浏览器运行时验证、安全/性能/API/迁移/可观测性专项信号。

明显拼写修复、纯机械重构、依赖升级、没有行为歧义的小型内部 helper 改动，使用 SILENT 或 MICRO，不输出完整 BRT。

## 候选意图和问题

候选意图用于帮用户选择，而不是让用户重新写需求。仅在 ALIGN/FULL 且确实存在多种合理意图时输出：

- A 保守理解：最小、可逆、风险最低；
- B 标准理解：最可能满足用户真实目标，通常作为推荐；
- C 扩展理解：更完整但范围更大，只有有价值时输出。

候选质量门槛：

- Goal：想解决什么；
- Expected Output：用户最终看到什么；
- Required Capability：需要什么能力或改动；
- Choose When：什么信号说明用户该选它；
- Tradeoff：相对推荐项牺牲什么或增加什么成本。

如果某个候选只能写成“更简单”“更完整”“范围更大”而说不出具体行为差异、适用信号和代价，删除它或合并到推荐项说明里。

开发进入 planning、task splitting、BDD/TDD 或写代码前，必须形成 Intent Lock；缺失且无法从上下文查证时，先追问或 probe，不进入实现。

Intent Lock 最少包含：

- 用户可观察结果：用户最终看到、触发或得到什么；
- 拥有面：改动属于哪个页面、接口、模块、数据流或测试面；
- 非目标：明确不做什么，避免顺手扩范围；
- 关键约束：权限、数据、默认值、失败路径、兼容、性能、安全或迁移边界；
- 验收证据：用什么测试、日志、截图、命令、diff 或用户可见行为证明完成。

追问规则：

- 先问行为和验收，再问技术实现；技术问题只有会改变用户结果、风险或验证时才问。
- 每个选项都要描述用户可见差异、适用信号和代价；不能只写“简单/完整/更稳”。
- 如果用户说“按推荐来”，锁定推荐选项并继续，不重复追问同一决策。

问题必须影响至少一项：用户最终可观察结果、范围边界、读写/删除/发布/回滚/权限/安全风险、数据保留/状态迁移/默认值/失败路径、测试层级、验收证据或实现许可。

问题设计规则：

- 默认 0 个；阻塞时 1 个；需求对齐时最多 2-3 个；高风险任务最多 4 个。
- 按影响排序：目标 > 范围 > 风险/权限 > 输出形态 > 测试验收。
- 每个问题只解决一个决策点，并给 2-3 个互斥选项。
- 每个选项都写清适合场景或取舍；标出推荐选项和原因。
- 允许用户直接说“按推荐来”。

不要问能从本地上下文查到的问题、只影响实现细节的问题、等价命名/措辞/展示顺序，或为了凑数量而生成的泛泛选项。

## 执行契约和防误改

执行或写入前内部建立 Execution Contract：`Target / Desired Outcome / Allowed Actions / Out of Scope / Success Evidence / Recovery Signal`。SILENT/MICRO 不必输出；ALIGN/FULL、交接、恢复或高误改风险时才摘要展示。

Wrong-Edit Guard：

- 写入前识别 owning surface、预计文件、相关测试、保护边界和已有用户/agent 改动。
- 归属不确定时先读代码、测试、日志或历史；仍不确定就 probe 或询问，不编辑。
- 只改完成契约需要的最小集合；不顺手碰格式、文档、测试、依赖、配置或相邻 bug；不为通过验证削弱行为要求。

Recovery Loop：

- HIGH/MEDIUM 且低风险可验证时，推进到新鲜证据或自然闸门，不停在分析/计划/半成品总结。
- 验证失败先分类为 implementation / test / environment / requirement mismatch；能在契约内安全修就修并重验。
- 遇到 blocker、高风险权限、范围扩大、需求冲突、破坏性/发布/合并动作或重复环境失败，才停下等用户选择。

## 评审、测试和账本

对齐后再做评审和测试，不要把它们放在意图发现前面。

默认选 2-4 个和当前需求最相关的视角，输出 Review Matrix：`Challenge / Evidence / Verdict`。Evidence 必须来自用户选择、本地上下文、可执行验证、可逆 probe 或显式假设加风险；不能写成“应该可以”“看起来没问题”。任何视角是 `NEEDS_CLARIFICATION` 或 `NEEDS_CHANGE` 时，不进入下一阶段。

需要完整评审视角、Evidence 质量规则、测试层级选择或反例时，读取 `references/review-test.md`。

非单点小改必须维护需求账本，默认只输出摘要。SILENT/MICRO 可只在内部维护，不向用户展开。

关键字段：用户原话、Intent Bundle、候选意图、已确认意图、用户目标、可观察结果、范围边界、操作边界、Route Contract、Execution Contract、保护边界、失败路径、验证证据、显式假设和剩余风险。

用户回答后先更新账本，再路由到下一阶段或继续对齐。进入 `ccdawn-planning` 时，需求账本成为 Workflow Ledger 的初始来源。

## 阶段闸门和收口

进入下一阶段前确认：已确认意图、范围边界、允许动作、执行契约、保护边界、关键风险、自审结论、测试锚点、完成汇报方式。自审结论里的 Evidence 如果不满足质量门槛，视同未完成自审。

自然闸门包括：意图变化、阻塞、验证失败且不能在当前契约内安全恢复、范围扩大、破坏性/发布/迁移/权限动作、worktree 冲突、需要用户取舍。

用户说“确认”“继续”“开始下一步”“按推荐来”时，按当前推荐路由推进。阶段完成只做短 checkpoint，不反复请求继续。发布、合并、迁移、删除、权限动作前必须停下等用户选择。

每轮 BRT 简短收口：

- 已对齐的真实意图；
- 已排除的误解；
- 当前行为契约；
- 执行契约和保护边界；
- 自审结论；
- 验证锚点；
- 剩余风险；
- 下一步：最具体的现有 skill、`FAST_PATH`、`ccdawn-planning` 或暂停。

ALIGN/FULL 默认使用短格式；SILENT/MICRO 不输出模板。需要完整输出模板或反例时，读取 `references/templates.md`。
