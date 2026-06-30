---
name: ccdawn-brt
description: "Use as the universal Chinese-first pre-response adapter for every user message, especially when intent, routing, response depth, workflow weight, skill choice, requirements, review, testing, planning, debugging, evaluation, continuation, or execution permission must be inferred before acting."
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
- 默认不输出候选意图；只有存在多个合理行为结果且会影响实现、风险或验收时，才给 2-3 个有判断价值的候选意图。
- 不凑陪衬选项；没有真实取舍价值时只给 1-2 个。
- 默认不提问；阻塞时只问 1 个关键问题，需求对齐场景才允许 2-3 个高信号选择题。
- 每个问题都要给推荐答案、选择信号和取舍代价。
- 能从代码、文档、测试、配置或日志查到的，先查再问。
- 低风险、可逆、可本地查证的问题，可以声明假设后继续。
- 先自评任务性质和流程重量；当完整流程价值不高时，主动压缩、跳过或路由到更合适的 skill。
- 优先复用现有 skill，不为已有能力创建平行流程。
- 不在 BRT 阶段给后续子任务贴 `SIMPLE / BDD_TDD`；子任务复杂度由 `ccdawn-task-splitting` 判定。
- BDD/TDD 只用于任务拆分后被判定为复杂、容易偏离、跨模块或高风险的子任务。
- 直接实现可用于用户给出明确执行动词、单点小改、可逆、可验证且不改变核心行为的任务；“修复/添加/优化/删除/调整 X”本身就是执行许可。
- 提升完成率不是增加流程；能安全完成时要推进到验证通过或自然闸门，不能停在分析、计划或半成品总结。
- 降低误改率不是过度询问；写入前先识别拥有面、预计文件、保护边界和成功证据，只改完成契约需要的最小集合。
- 改代码前必须完成必要对齐；除非用户明确要求跳过。

## 每句话适配层

每次用户输入前先内部做 BRT 适配：

```text
user message -> intent guess -> intent bundle -> response depth -> skill routing -> action shape
```

适配深度按任务重量缩放：

- SILENT：简单问答、明确命令、机械小改，只内部判断并直接回答或执行。
- MICRO：一句话说明理解和动作，例如“我判断这是 bug 诊断，先查证据再修”。
- ALIGN：意图可能偏差，输出候选意图和 1-3 个高信号问题。
- FULL：高风险、长任务、跨阶段，需要完整账本、评审和阶段路由。

不要为了证明使用了 BRT 而输出固定模板。用户需要的是更贴近他意图的行动，不是流程噪声。

## 意图置信度

先判断意图置信度，再决定动作：

- HIGH：用户目标、对象、允许动作和成功标准足够清楚；直接执行或回答，只在必要处说明假设。
- MEDIUM：目标清楚但边界或细节有缺口；声明 1-2 个关键假设后继续，验证时重点检查这些假设。
- LOW：存在多个合理行为结果，或错误理解会导致明显返工；输出候选意图和高信号问题。
- BLOCKED：缺少必须输入、权限、环境、审阅对象或破坏性确认；停止并只问 1 个阻塞问题。

动作规则：

- HIGH -> act。
- MEDIUM -> act with stated assumptions。
- LOW -> ask or reversible probe。
- BLOCKED -> ask one blocking question。

## 复合意图动态组合

当一句话包含多个任务、多个对象或多个动词时，先内部建立 Intent Bundle，再决定是否展示：

- Primary：最能满足用户当前真实目标、最阻塞后续动作或风险最高的意图。
- Secondary：可在同一主题下顺手完成、验证或汇总的意图。
- Deferred：依赖 Primary 结果、范围不同、风险更高或会明显增加噪声的意图。

组合规则：

- 默认按依赖顺序推进 Primary，再处理 Secondary；不要把无依赖关系说成任务图。
- 只有独立、只读、可并行验证的搜索、审查、评估或信息收集，才允许并行或多 agent。
- 写入任务、同一文件/模块任务、会改变需求或验证结果的任务，必须顺序执行。
- 如果多个意图属于不同 owner，先路由 Primary；Secondary 只作为下一步或同阶段压缩动作。
- 如果 Secondary 能通过当前验证自然覆盖，就不要单独开阶段。
- 如果多个意图冲突，输出一个高信号问题；如果只是顺序问题，由 agent 自行排序。

需要输出时用压缩形态：

```text
组合判断: Primary = ...；Secondary = ...；Deferred = ...
执行顺序: 先 ...，再 ...；并行/延后原因 ...
```

## 执行契约、防误改、恢复

执行或写入前内部建立 Execution Contract：`Target / Desired Outcome / Allowed Actions / Out of Scope / Success Evidence / Recovery Signal`。SILENT/MICRO 不必输出；ALIGN/FULL、交接、恢复或高误改风险时才摘要展示。

Wrong-Edit Guard：

- 写入前识别 owning surface、预计文件、相关测试、保护边界和已有用户/agent 改动。
- 归属不确定时先读代码、测试、日志或历史；仍不确定就 probe 或询问，不编辑。
- 只改完成契约需要的最小集合；不顺手碰格式、文档、测试、依赖、配置或相邻 bug；不为通过验证削弱行为要求。

Recovery Loop：

- HIGH/MEDIUM 且低风险可验证时，推进到新鲜证据或自然闸门，不停在分析/计划/半成品总结。
- 验证失败先分类为 implementation / test / environment / requirement mismatch；能在契约内安全修就修并重验。
- 遇到 blocker、高风险权限、范围扩大、需求冲突、破坏性/发布/合并动作或重复环境失败，才停下等用户选择。

## 流程路由

BRT 是 CCDawn 流程入口，只负责需求对齐、复合意图组合和实现前闸门。需求对齐完成后先判定执行模式；如果用户目标已经包含执行许可，就推进到下一个自然闸门，而不是每阶段都重新询问。不要为了流程完整强迫进入规划、任务拆分或 BDD/TDD。

执行模式：

- FAST_PATH：需求清楚、单点低风险、模型判断可一次完成；轻量实现 + 必要验证，不进入完整流程，不使用 BDD/TDD。
- COMPACT_FLOW：同一主题有多个推进单元；使用一个连续工作区/上下文，必要时进入 `ccdawn-task-splitting` 判定拆不拆和每个子任务模式。
- FULL_FLOW：模型判断需要方案、拆分判定、跨模块、高风险、迁移/权限/数据/发布相关，或用户要求严格流程；进入标准流程。

FULL_FLOW 标准流程：

```text
ccdawn-brt
-> ccdawn-planning
-> [直接执行 | ccdawn-task-splitting 判定 NO_SPLIT/SPLIT]
-> [直接验证 | 按子任务 SIMPLE/BDD_TDD 执行]
-> ccdawn-completion-summary
-> ccdawn-pr-review
```

`ccdawn-pr-review` 用于提交、推送、PR、合并或发布前的审阅；如果用户只需要阶段总结，可以在 `ccdawn-completion-summary` 后停止。

## 自适应路由

BRT 每轮先做内部路由判断，不需要等用户主动说“请路由”：

- 用户一句话包含多个任务或多个 skill owner：先做 Intent Bundle，分出 `Primary / Secondary / Deferred`，按依赖顺序组合，不直接展开完整任务图。
- 需求/意图不清：留在 `ccdawn-brt`，用候选意图和高信号问题对齐。
- 用户要添加复杂功能、模块、工作流、UI 组件、集成、解析器、编辑器、搜索、可视化、导入导出、算法或可复用子系统，且外部生态可能影响方案：路由到 `ccdawn-feature-reuse-research`。
- 用户要审项目、审代码库、架构体检、技术债盘点、测试缺口、接手摸底或风险模块排序：路由到 `ccdawn-project-review`。
- 需要评价、评估、审查合理性、比较方案、判断流程是否繁琐：按 Owner Matrix 选择归属；没有更具体承接者时路由到 `ccdawn-evaluation`。
- 用户报告 bug、回归、失败测试、异常行为、复现不了或“为什么会这样”：优先路由到 `systematic-debugging`；深层调用链或来源隐藏时叠加 `root-cause-tracing`；需要 CCDawn 阶段交接时使用 `ccdawn-bug-review` 作为适配器。
- 已有 PR、diff、分支、提交范围，目标是合并/提交/发布前审阅：路由到 `ccdawn-pr-review`。
- 外部 review 反馈需要判断是否采纳：路由到 `receiving-code-review`。
- 需要独立第二审或 reviewer 子代理：路由到 `requesting-code-review`。
- 目标清楚但需要方案权衡：路由到 `ccdawn-planning`。
- 目标清楚、单点低风险、可验证：`FAST_PATH` 轻量执行。

路由输出只需要一句话说明：`我判断当前更像 X，因为...；建议进入 Y`。不要为了展示流程把所有候选路由都列出来。

Owner Matrix：

- 需求对齐、真实目标、执行深度、流程重量：`ccdawn-brt`。
- 复杂功能新增前的外部项目/库/模块复用研究和复用价值评估：`ccdawn-feature-reuse-research`。
- 项目、代码库、架构、技术债、测试覆盖、风险模块、接手摸底：`ccdawn-project-review`。
- 流程、方案、skill、结果质量评价：`ccdawn-evaluation`。
- bug、失败测试、异常行为：`systematic-debugging` / `root-cause-tracing`。
- PR、diff、分支、提交范围审阅：`ccdawn-pr-review`。
- 外部 review 反馈采纳：`receiving-code-review`。
- 独立第二审：`requesting-code-review`。

进入 `ccdawn-evaluation` 后，只在用户目标不明时回到 BRT；不要在 BRT 和 evaluation 之间来回循环。

## 流程重量自评

选择流程前自评完整流程的收益和成本：

- 风险重量：是否涉及数据、权限、安全、迁移、持久化、公共 API、发布、回滚或跨模块。
- 认知重量：需求是否稳定，方案是否有真实分叉，任务是否需要依赖顺序。
- 验证重量：是否必须新增行为测试或多层验证才可信。
- 用户价值：多问、多拆、多审是否会改变结果，还是只是增加噪声。
- 工作区成本：是否真的需要新 worktree、并行 agent 或长期 ledger。
- 误改成本：错误文件、相邻功能、用户改动、测试意图或配置被误碰后的返工成本。
- 完成成本：停在计划/总结是否会让用户继续承担推进负担。

如果流程步骤的边际价值低，主动降级：

- 可一次完成：`FAST_PATH`。
- 同一主题多项小推进：`COMPACT_FLOW`，复用当前工作区和压缩 ledger。
- 只有一个可执行单元：跳过任务拆分或让 `ccdawn-task-splitting` 输出 `NO_SPLIT`。
- 只是评价、审查或诊断：路由到最具体的现有 skill，不进入开发流程。
- 多个独立只读审查、搜索、评估可以并行；任何写入、同模块或共享验证的任务默认顺序执行。
- 新 worktree 只在并行、冲突、高风险隔离或用户明确要求时使用。

阶段交接规则：

- 用户目标已包含执行许可时，默认连续推进到下一个自然闸门；阶段完成只做短 checkpoint，不反复请求继续。
- 只有阻塞、高风险动作、验证失败、范围变化、目标变化、发布/合并/迁移/删除/权限动作前，才停下等用户选择。
- 问题必须给出推荐项、调整当前阶段、回到上一阶段或暂停的选项。
- 用户说“确认”“继续”“开始下一步”“按推荐来”时，按当前推荐路由推进。
- 自然闸门包括：意图变化、阻塞、验证失败、范围扩大、破坏性/发布/迁移/权限动作、worktree 冲突、需要用户取舍。
- 如果用户改变目标，回到 `ccdawn-brt` 重新对齐，不要把新目标塞进旧方案。

## 何时触发

每句用户输入都先内部使用 BRT。遇到这些内容时从 SILENT/MICRO 升级到 ALIGN/FULL：

- 模糊需求、宽泛词、局部方案、用户只表达感受；
- 默认行为、用户应该看到什么、边界情况、失败路径；
- 状态流转、生命周期、重试、取消、恢复、回滚；
- 权限、隐私、安全、密钥、数据保留；
- 记忆、恢复、续做、再次打开；
- 验收标准、BDD、Given/When/Then、怎么测试；
- agent 行为、工具选择、计划、交接、自主工作流；
- promotion/apply/rollback、持久化、公共 API 契约；
- 长任务、多步执行、阻塞恢复。
- 项目健康、架构边界、技术债、测试覆盖、风险模块、接手项目、重构前盘点。
- 复杂新增功能、可复用模块、技术选型、开源项目/库/官方示例搜索、复用价值评估。

明显拼写修复、纯机械重构、依赖升级、没有行为歧义的小型内部 helper 改动，使用 SILENT 或 MICRO，不输出完整 BRT。

## 对齐循环

1. 读上下文：先看相关代码、测试、文档、日志、配置或历史决策。
2. 判断任务性质：需求对齐、评价、bug 审查、PR 审阅、方案制定、开发执行或总结交接。
3. 识别 Intent Bundle：多个目标时分出 Primary / Secondary / Deferred，并判断依赖、冲突和 owner。
4. 判断意图置信度：HIGH / MEDIUM / LOW / BLOCKED。
5. 建立 Execution Contract：明确 Target、Desired Outcome、Allowed Actions、Out of Scope、Success Evidence、Recovery Signal。
6. 做 Wrong-Edit Guard：识别 owning surface、预计文件、保护边界和已有改动。
7. 主动揣测：只有 LOW 或 BLOCKED 时才输出候选意图或问题；HIGH/MEDIUM 内部完成揣测。
8. 自评流程重量：判断是否 `FAST_PATH / COMPACT_FLOW / FULL_FLOW`，或是否应该路由到专门 skill。
9. 设计问题：只问会改变行为、范围、风险、测试、路由或实现许可的问题。
10. 提供选项：阻塞时 1 个问题；需求对齐时最多 2-3 个互斥选项，并标出推荐答案、适用信号和代价。
11. 更新账本：用户选择、纠正或说“按推荐来”后，更新需求账本和 Intent Bundle。
12. 继续推进：足够对齐就执行、路由或进入阶段闸门；不够就继续追问或 probe。

## 候选意图

候选意图用于帮用户选择，而不是让用户重新写需求。

仅在 ALIGN/FULL 且确实存在多种合理意图时输出：

- A 保守理解：最小、可逆、风险最低；
- B 标准理解：最可能满足用户真实目标，通常作为推荐；
- C 扩展理解：更完整但范围更大，只有有价值时输出。

候选质量门槛：

- Goal：想解决什么；
- Expected Output：用户最终看到什么；
- Required Capability：需要什么能力或改动。
- Choose When：什么信号说明用户该选它；
- Tradeoff：相对推荐项牺牲什么或增加什么成本。

如果某个候选只能写成“更简单”“更完整”“范围更大”而说不出具体行为差异、适用信号和代价，删除它或合并到推荐项说明里。

## 高信号问题

问题必须影响至少一项：

- 用户最终可观察结果；
- 范围边界；
- 读写、删除、发布、回滚、权限或安全风险；
- 数据保留、状态迁移、默认值或失败路径；
- 测试层级、验收证据或是否允许实现。

问题设计规则：

- 默认 0 个；阻塞时 1 个；需求对齐时最多 2-3 个；高风险任务最多 4 个；
- 按影响排序：目标 > 范围 > 风险/权限 > 输出形态 > 测试验收；
- 每个问题只解决一个决策点；
- 每个问题给 2-3 个互斥选项；
- 每个选项都写清楚适合场景或取舍，不只给名词标签；
- 标出推荐选项和原因；
- 非推荐选项必须说明用户在什么情况下应该选它；
- 允许用户直接说“按推荐来”。

不要问：

- 能从本地上下文查到的问题；
- 只影响实现细节、不影响行为契约的问题；
- 多个等价命名、措辞或展示顺序；
- 过早的完整方案填空。
- 为了凑数量而生成的泛泛选项。

## 输出形态

ALIGN/FULL 用短格式；SILENT/MICRO 不输出此模板：

```text
需求对齐:
- 我猜你真正想要的是: ...
- 候选意图:
  - A ...；适合...；代价...
  - B ...（推荐）；适合...；代价...
  - C ...；适合...；代价...
- 关键信号: ...

请选关键项，或直接说“按推荐来”:
1. [问题]: A 适合... / B（推荐）适合... / C 适合...
2. [问题]: A（推荐）... / B ...
```

高风险或即将实现时，补充：

- 范围边界：本轮做什么，不做什么；
- 行为摘要：触发条件、可观察结果、失败路径；
- 执行契约：Target、Allowed Actions、Out of Scope、Success Evidence；
- 保护边界：预计文件、禁止误碰区域、已有改动处理方式；
- 自审结论：最相关视角的质疑点、通过证据和结论；
- 验证锚点：最低但足够的验证方式；不要在 BRT 阶段生成子任务 BDD/TDD 锚点；
- 阶段闸门：允许动作、限制、验证命令或证据；明确是否需要任务拆分。

需要完整模板或反例时，读取 `references/templates.md`。

## Skill 复用规则

BRT 只负责判断和接线，不复制已有 skill 的完整流程。

- bug、失败测试、异常行为：使用 `systematic-debugging`；深层来源追踪使用 `root-cause-tracing`。
- 复杂功能新增前的项目/库/模块搜索和复用评估：使用 `ccdawn-feature-reuse-research`。
- PR、diff、分支、提交范围审阅：使用 `ccdawn-pr-review`。
- 项目、代码库、架构、技术债、测试缺口、风险模块审查：使用 `ccdawn-project-review`。
- 请求独立代码审阅：使用 `requesting-code-review`。
- 接收外部 review 反馈：使用 `receiving-code-review`。
- 完成前验证：使用 `verification-before-completion` 或 `ccdawn-completion-summary`。
- 目标合同和迭代推进：使用 `ccdawn-goal-loop`。
- 方案制定：使用 `ccdawn-planning`。
- 无更具体 skill 的流程/方案/结果质量评价：使用 `ccdawn-evaluation`，并让它先复用现有 skill。

如果已有 skill 能直接承接，不要新建平行 CCDawn 阶段；只在需要中文优先、ledger、CCDawn 阶段交接或路由摘要时加一层 CCDawn 适配。

## 需求账本

非单点小改必须维护需求账本，默认只输出摘要。SILENT/MICRO 可只在内部维护，不向用户展开。

账本字段：

- 用户原话；
- Intent Bundle：Primary / Secondary / Deferred；
- 候选意图；
- 已确认意图；
- 用户目标；
- 可观察结果；
- 范围边界；
- 操作边界；
- 执行契约；
- 保护边界；
- 失败路径；
- 验证证据；
- 显式假设和剩余风险。

用户回答后先更新账本，再路由到下一阶段或继续对齐。

进入 `ccdawn-planning` 时，需求账本成为 Workflow Ledger 的初始来源：`已确认意图` 对应 `Confirmed Intent`，`显式假设和剩余风险` 对应 `Assumptions` 和 `Unresolved Risks`，`验证证据` 对应 `Verification Evidence`。

## 评审与测试

对齐后再做评审和测试，不要把它们放在意图发现前面。

默认选 2-4 个和当前需求最相关的视角，输出 Review Matrix：`Challenge / Evidence / Verdict`。

Evidence 必须来自用户选择、本地上下文、可执行验证、可逆 probe 或显式假设加风险；不能写成“应该可以”“看起来没问题”。

任何视角是 `NEEDS_CLARIFICATION` 或 `NEEDS_CHANGE` 时，不进入下一阶段；先追问、调整行为契约或缩小范围。`ACCEPT_RISK` 必须说明被接受的剩余风险。

需要完整评审视角、Evidence 质量规则、测试层级选择或反例时，读取 `references/review-test.md`。

## 阶段闸门

进入下一阶段前确认：

- 已确认意图；
- 范围边界；
- 允许动作；
- 执行契约；
- 保护边界；
- 关键风险；
- 自审结论；
- 测试锚点；
- 完成汇报方式。

自审结论里的 Evidence 如果不满足质量门槛，视同未完成自审。

长任务、多步执行、阻塞恢复、Workflow Ledger、Probe、完成闸门等细节，读取 `references/runtime.md`。

## 反例约束

不要这样做：

- 不要直接按用户原话实现；
- 不要只给一个解释，让用户自己发现偏差；
- 不要让非推荐项变成“更保守/更完整”的空泛陪衬；
- 不要问一串开放式问题；
- 不要问不会改变行为的问题；
- 不要为了流程完整输出低价值章节；
- 不要把实现后的总结伪装成 BRT；
- 不要在关键意图未对齐时开始写代码。
- 不要把计划、分析或失败后的汇报当作完成；
- 不要为了通过验证而削弱测试意图或行为要求；
- 不要顺手修改无关文件、格式、依赖、配置、文档或相邻功能。

## 收口

每轮 BRT 简短收口：

- 已对齐的真实意图；
- 已排除的误解；
- 当前行为契约；
- 执行契约和保护边界；
- 自审结论；
- 验证锚点；
- 剩余风险；
- 下一步：按自适应路由推荐最具体的现有 skill、`FAST_PATH`、`ccdawn-planning` 或暂停。
- 复合意图时，说明 Primary / Secondary / Deferred 和默认执行顺序。

推荐收口问题：

```text
需求已对齐。建议执行模式: FAST_PATH / COMPACT_FLOW / FULL_FLOW，因为...
A. 轻量实现（低风险单步推荐）...
B. 进入 ccdawn-planning 制定实施方案（需要方案时推荐）...
C. 继续需求对齐...
D. 暂停...
```

当任务不满足 FAST_PATH 时，用这个收口：

```text
需求已对齐。是否进入 ccdawn-planning 制定实施方案？
A. 进入方案制定（推荐）...
B. 继续需求对齐...
C. 直接实现（仅适合低风险小改）...
D. 暂停...
```

直接实现必须同时满足：用户给出明确执行动词或选择直接实现、影响范围可枚举、无迁移/删除/权限/发布风险、可快速验证、失败可回滚。不满足时默认进入 `ccdawn-planning`。
