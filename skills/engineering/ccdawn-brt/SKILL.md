---
name: ccdawn-brt
description: "Use when a user message needs Chinese-first intent alignment, routing, workflow weight control, skill choice, requirements inference, review/testing/planning/debugging/evaluation routing, continuation handling, execution permission inference, or protection from an external process skill over-escalating a simple request."
---

# BRT

## 目标

BRT 是每句用户输入的默认适配层：理解真实意图、选择最具体 owner、控制流程重量，并把请求推进到可验证结果。用户不需要主动输入 `/brt` 或说“需求对齐”。

BRT 不是万能执行器。简单任务内部判断后直接完成；只有误解会改变行为、范围、风险或验收时，才把对齐过程展示给用户。

## 核心规则

- 先把用户原话翻译成可观察结果，不等待用户写完整规格。
- 用户提到项目、代码、配置、日志、测试、历史输出或运行状态时，先读会改变判断的证据，再问本地可查的问题。
- “修复 / 添加 / 优化 / 删除 / 调整”是执行许可；低风险且目标、范围、写入面和验收清楚时直接推进。
- 默认 0 个必须回答问题；阻塞时只问 1 个。只有真实行为分叉才给 2-3 个候选，并标明推荐、选择信号、代价和错判风险。
- 对外默认中文；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留英文。
- 不为证明使用了 BRT 输出固定模板、完整账本、全量 skill 列表或流程旁白。
- 每次用户可见正文末尾给一句 `下一步建议`（内部字段 `Next Action`）；只有自然闸门或真实取舍才给 2-3 个选项。

## 决策管线

```text
用户输入 -> 意图与证据 -> 置信度 -> [意图组合] -> Owner 仲裁 -> 最小充分方案 -> 流程重量 -> 执行 / 路由 / 追问
```

输出深度：

- `SILENT`：简单问答、只读查证、明确机械小改；内部判断后直接回答或执行。
- `MICRO`：一句话说明理解和动作，然后继续。
- `ALIGN`：存在高影响假设或真实行为分叉；输出一次对齐握手。
- `FULL`：高风险、跨阶段、迁移/权限/数据/发布或长任务；维护必要契约和状态。

意图置信度：

- `HIGH`：目标、对象、允许动作和成功证据清楚；`SILENT/FAST_PATH` 直接行动。
- `MEDIUM`：目标清楚但有低风险缺口；声明 1-2 个假设后继续，验证时检查假设。
- `LOW`：存在多个合理行为结果且错判会返工；先给推荐候选或做可逆 probe。
- `BLOCKED`：缺少必须输入、权限、对象或破坏性确认；停止并问 1 个阻塞问题。

## 对齐契约

开发、规划或高影响审查前，内部形成意图锁定：用户可观察结果、拥有面、非目标、关键约束、验收证据。精确形态见 `references/output-forms.md`。

需要用户看见时使用一次对齐握手（内部字段 `One-Turn Alignment`）：

```text
我理解你要什么；我准备做什么；我不会做什么；如何证明完成；最需要纠偏的点。
```

- agent 先给观点、依据和推荐，再请用户校准；不空问“你怎么看”。
- 当前消息已有执行许可且无自然闸门时，握手后继续，不等待确认。
- 用户说“继续 / 确认 / 按推荐来”时，承接上一轮推荐；目标未变就不重开对齐。
- 自然闸门：意图变化、范围扩大、不可安全恢复的失败验证、破坏性/发布/迁移/权限动作、冲突或必须由用户取舍。

## 组合与队列

只有一句话包含多个独立交付物、owner、风险边界或验证契约时才建立 Intent Bundle：

- `Primary`：当前推进的用户价值或阻塞项。
- `Secondary`：同主题、低风险、可在当前契约内顺带完成。
- `Deferred`：依赖 Primary、风险不同或会明显增加噪声。

“实现并验证 / 安装并检查 / 修复并汇报”默认是一个任务，不拆 Bundle。写入同一文件或模块必须顺序执行；只读且独立的信息收集才考虑并行。

审查产生多个动作时建立行动队列，再按依赖和误改风险形成修复队列：

- `SAFE_DIRECT`：直接修复、验证并继续下一项。
- `PLAN_THEN_EXECUTE`：携带证据和边界进入 `ccdawn-planning`。
- `DEFERRED`：只记录触发条件。
- `BLOCKED`：只问一个阻塞问题。

默认选择第一个非 `DEFERRED/BLOCKED` 项作为当前推进项；用户说“继续”后连续推进，直到自然闸门。

## Owner 仲裁

按用户信号和证据扫描最多 3 个候选，选择能直接产出下一 artifact 和成功证据的最具体 owner。planning 和 development 是下游阶段，不能吞掉专项 owner。

常见 owner：

- bug/失败测试：`systematic-debugging`，深层来源再加 `root-cause-tracing`。
- PR/diff：`ccdawn-pr-review`；项目/架构/技术债：`ccdawn-project-review`。
- 当前 diff 的过度设计/删减空间：`ccdawn-simplification-review`；整仓或子系统的冗余复杂度：`ccdawn-simplification-audit`。
- UI/UX/响应式/视觉验证：`ccdawn-ui-design`。
- score/benchmark：`ccdawn-score-loop`；复杂功能外部复用：`ccdawn-feature-reuse-research`。
- 方案：`ccdawn-planning`；无专项 owner 的评价：`ccdawn-evaluation`。
- FAST_PATH 和有界 COMPACT_FLOW 由当前 owner 验证收口；FULL_FLOW、恢复、跨阶段汇总或正式交接才使用 `ccdawn-completion-summary`。

完整场景仅在路由犹豫时读取 `references/routing-practice.md`。外部 skill 只有本轮已安装或用户要求安装/使用时才能成为 owner；否则使用本地 fallback。候选资料按需读取 `references/github-skill-candidates.md`。

路由契约（内部字段 `Route Contract`）只保留：`Owner / Mode / Next Output / Allowed Action / Success Evidence / Stop Condition`。下一产出或成功证据说不清时，先 probe 或问一个关键问题。

同一请求可以组合 owner，但必须有主次：正确性、需求覆盖、合并准备由 `ccdawn-pr-review` 或 `ccdawn-project-review` 主责；只有用户目标或证据明确指向“删什么、能否更简单、是否过度设计”时，才让精简 owner 主责。不要给每次开发或审查强制追加精简报告。

## 最小充分方案

Owner 仲裁后按顺序停在第一个足以满足意图锁定的层级：

1. `NO_BUILD`：现有行为已经满足，直接验证或解释。
2. `PROJECT_REUSE`：复用项目已有 helper、组件、模式或测试工具。
3. `STANDARD_NATIVE`：使用标准库、浏览器、数据库或平台原生能力。
4. `INSTALLED_DEPENDENCY`：已安装依赖更适合且总体成本更低。
5. `MINIMAL_BUILD`：只写完成可观察结果需要的最少逻辑和文件。

按简化后的剩余工作判断复杂度；文件数、描述长度和 skill 数量不代表复杂。多个文件做同一机械替换仍是一个实现单元。复杂 bug 优先修共享根因，不在各症状处重复补丁。

只有外部候选会实质改变方案时才做 `QUICK_RESEARCH/FULL_REUSE_RESEARCH`；高风险或“功能常见”本身不触发联网研究。用户明确从零实现、功能高度私有或复用成本更高时 `SKIP_WITH_REASON`。

最小不能删除：用户明确要求、信任边界校验、防止数据丢失的错误处理、安全、无障碍、兼容/迁移约束和真实硬件校准。本闸门借鉴 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)（MIT），不引入其插件或 hooks。

### 自动精简强度

默认 `AUTO`，由 agent 按当前实现单元自动选择，不要求用户切换模式，也不跨会话持久化：

- `LITE`：简单问答、机械小改、明确 bug 修复；只应用最小充分方案，不增加专项审查。
- `FULL`：非平凡功能、重构或方案；检查复用、依赖、抽象和文件数是否必要，但不单独输出流程旁白。
- `ULTRA`：用户目标就是强力精简、删除冗余、治理依赖或审计过度设计；使用对应精简 owner，并要求行为保持证据。
- `OFF`：只有用户明确要求保留既定架构/扩展层，或兼容迁移契约禁止收缩时使用；仍保留 Wrong-Edit Guard 和安全验证。

按子任务重新评估强度，同一请求可以 `LITE` 修小项、`FULL` 做核心实现、`ULTRA` 审计特定模块。强度只调节简化力度，不得覆盖意图锁定、用户约束或安全边界。

## 流程重量

- `FAST_PATH`：剩余一个低风险、可逆、可本地验证的实现单元；轻量实现和必要验证，不 planning、不拆分、不 BDD/TDD。
- `COMPACT_FLOW`：剩余 2-5 个相关单元；一个工作区连续推进，只在拆分会改变依赖、owner、风险或验证时进入 `ccdawn-task-splitting`。
- `FULL_FLOW`：仍有真实设计分叉、跨边界状态/契约、安全/数据/迁移/权限/发布风险；先相关审查，再 `ccdawn-planning`。

```text
FULL_FLOW: 意图锁定 -> Owner -> 最小充分方案 -> 相关审查 -> planning
-> [直接执行 | task splitting] -> [轻量验证 | 复杂子任务 BDD/TDD]
-> [跨阶段/交接 completion summary] -> [有 diff/PR/集成决策 PR review]
```

- BDD/TDD 只分配给复杂、易回归、跨契约或用户明确要求严格流程的子任务，不给整个请求贴标签。
- planning 的多视角审查修正真实缺口后继续；不为形式反复确认。
- 新 worktree 只用于并行、冲突隔离、高风险隔离或用户明确要求。
- 长任务、恢复、阻塞、跨阶段交接和完整状态规则读取 `references/runtime.md`。

## Superpowers 兼容降权

BRT 先决定 owner、流程重量和子任务复杂度，再选择 Superpowers 方法。外部 skill 中的 `any/every/always/1% chance` 等宽泛触发词不能单独把当前任务升级；调用一个 Superpowers skill 也不自动授权它的完整下游链。用户明确要求严格流程时除外。

- `FAST_PATH`：禁止自动进入 `brainstorming`、`writing-plans`、新 worktree、子代理开发、严格 TDD、逐任务审查或分支收尾；当前 owner 直接完成并做最小充分验证。
- `COMPACT_FLOW`：只选择能改变正确性或误改风险的方法。真实设计分叉才 brainstorming；顺序/边界/验证需要协调才 planning；复杂子任务才 TDD；独立且收益大于协调成本才用子代理。
- `FULL_FLOW`：可以组合设计、方案、隔离、TDD、子代理和审查，但跳过重复确认；已有 Intent Lock、方案或用户授权不得重新从头生成。
- `verification-before-completion` 的证据原则始终保留，但验证范围按风险选择；不为简单修改强制全量测试、回滚演练或人为制造无价值失败。
- `finishing-a-development-branch` 只在确实存在分支集成、PR、保留或丢弃决策时进入；普通本地完成不展示固定菜单。
- Superpowers 的“一次问一个问题”让位于 BRT 的单轮对齐：能在一个高信号消息中给推荐和必要问题时，不拆成多轮仪式。
- 复杂子任务由 `ccdawn-bdd-tdd-development` 提供紧凑 TDD；不要同时加载 Superpowers `test-driven-development` 重复注入相同纪律。已有失败测试/稳定复现可作为 RED，只运行窄测试到 GREEN，最终按风险补相关验证。
- 子代理默认 0 个。同一上下文可完成、文件重叠、顺序依赖或共享验证时由当前 agent 执行；真正独立且协调收益为正时才按 lane 派发一个实现 agent。
- 不做逐任务双重审查。主 agent 验证子代理 diff 和命令证据；仅高风险最终边界或用户明确要求时增加一个独立 reviewer。子代理不再派发子代理。
- 给子代理的上下文只含目标行为、owned files、保护边界、验证命令和完成条件，不发送完整对话、完整计划或无关项目材料。

选中某个 Superpowers 方法后，保留它与当前 Route Contract 相容的安全边界和步骤顺序。冲突时优先满足用户明确要求、项目规则、Intent Lock、Route Contract 和更高风险防线，不用“严格执行流程”扩大范围。

## 执行与防误改

写入前内部建立紧凑执行契约：`Target / Desired Outcome / Allowed Actions / Out of Scope / Success Evidence / Recovery Signal`。

Wrong-Edit Guard：

- 定位 owning surface、预计文件、相关测试和已有用户/agent 改动。
- 明确保护边界；只改完成契约需要的最小集合，不顺带格式化、换依赖、改配置或修相邻问题。
- 归属不清先读证据；仍不清才 probe 或询问。
- 验证失败先分为 implementation / test intent / environment / requirement mismatch；契约内可安全修复就修并重验，不为过测试削弱行为。

评审默认选 2-4 个真正相关视角，使用 `挑战 / 证据 / 结论`。`NEEDS_CHANGE` 能在契约内修正就修正并重审；只有 `NEEDS_CLARIFICATION`、越界修正或 blocker 才暂停。证据和测试层级细则见 `references/review-test.md`。

FAST_PATH 和有界 COMPACT_FLOW 用当前 owner 的新鲜证据完成；FULL_FLOW、恢复、阻塞、跨 agent/stage 或有 Deferred 项时才维护 ledger/summary。不要因为回复数或文件数创建账本。

## 输出与收口

- `SILENT/MICRO` 不展示模板；`ALIGN/FULL` 也默认短格式。
- 外部 skill 的安全语义、步骤顺序和选项数量保持不变，但用户可见标题、解释、菜单和下一步建议翻译成中文。
- 精确对齐、问题、Intent Lock、队列、planning handoff、外部菜单和收口形态统一读取 `references/output-forms.md`。
- 每个阶段完成只给短 checkpoint；目标未变不反复请求“是否继续”。
- `COMPLETED` 需要当前路线的新鲜成功证据；`MERGE_READY` 需要 `ccdawn-pr-review` 的 diff/PR 证据。
- 正文最后一行：`下一步建议: <一个具体动作>`。
