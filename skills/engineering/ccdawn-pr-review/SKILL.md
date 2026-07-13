---
name: ccdawn-pr-review
description: Use when the user explicitly requests review of a PR, diff, branch, commit range, merge readiness, or review feedback, or when a high-risk change has reached an explicit pre-integration review gate; do not trigger merely because ordinary development finished.
license: MIT
---

# CCDawn PR Review

## 目标

对已经完成的 CCDawn 任务、分支、PR 或本地 diff 做证据化审阅，判断是否可以进入提交、推送、PR、合并或发布。

此阶段只审阅，不修代码。发现问题后，把用户路由回合适阶段。

核心原则：

```text
没有读 diff、需求和证据，就不要说 ready。
```

## BRT interface

- Context Boundary: PR/diff/base-head、需求/方案/任务图/完成总结、验证证据、禁止编辑边界、发布/合并目标和明确排除范围。
- Output Contract: risk-ranked findings、需求覆盖、验证证据、Review Matrix、merge readiness、修复/补证据/发布前路由和 Route Out。
- Allowed Action: 默认只读审阅；不编辑文件、不移动 HEAD、不改 index、不合并/推送/发布；需要修复时路由回对应开发阶段。
- Success Evidence: diff 已审、需求已对照、关键验证证据已检查，每条 finding 都绑定文件/行号/命令证据和回流阶段。
- Stop Condition: 缺可审阅 diff、缺需求来源、验证证据不可得、审阅对象与用户目标不一致、或提交/推送/合并/发布需要明确权限。
- Route Out: 对应开发模式、`ccdawn-task-splitting`、`ccdawn-completion-summary`、提交/推送/合并准备、`ccdawn-planning`、`ccdawn-brt` 或 BLOCKED。

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

使用前确认至少有：

- 已对齐需求、方案、任务图或完成总结；
- 可审阅对象：PR URL、base/head、分支名，或本地未提交/已提交 diff；
- 已有验证证据，或可以安全读取/运行的验证命令；
- 用户希望判断是否可提交、推送、开 PR、合并、发布或继续修复。

如果缺少可审阅 diff，先输出 `BLOCKED`。如果缺少需求来源，先回到 `ccdawn-brt` 或 `ccdawn-planning`，不要只按代码喜好审。

## 审阅边界

- 默认只读：不要编辑文件、不要移动 HEAD、不要改 index、不要改分支状态。
- 可以运行只读检查、测试、构建或 lint；如果命令会写缓存或产物，说明影响并避免把产物当代码改动提交。
- 不用审阅阶段顺手修复问题。需要修复时，按原任务的 Development Mode 路由；复杂子任务才回到 `ccdawn-bdd-tdd-development`。
- 不扩大评审范围到用户未要求的重构、风格统一或架构重写。
- 不把缺少证据包装成通过。

## 审阅流程

1. 定位审阅范围：识别 PR、base/head、merge-base、本地 diff 或提交范围。
2. 读取需求来源：BRT 需求账本、Workflow Ledger、方案、任务图、完成总结或用户原始要求。
3. 读取变更：看 diff、关键文件、测试、配置、迁移、脚本和文档影响。
4. 读取证据：看最新测试、构建、lint、类型检查、手工验收、probe 或发布验证结果。
5. 多角度审查：从需求覆盖、正确性、测试证据、风险、可维护性和集成影响判断。
6. 输出 findings：先列问题，再给结论；没有问题也要说明剩余测试缺口或风险。
7. 路由下一步：修复、补测、回到方案、进入提交/PR/合并，或暂停。

## 审阅视角

默认检查这些视角，只保留与当前 diff 有关的高信号项：

- 需求覆盖：是否满足已确认意图、任务图和明确不做范围。
- 范围边界：是否只改了 Execution Contract 需要的 owned surface，是否误碰相邻文件、配置、测试或用户改动。
- 行为正确性：主路径、边界、失败路径、状态迁移是否正确。
- 回归风险：是否破坏现有 API、数据、配置、兼容性或用户工作流。
- 测试证据：测试是否验证真实行为，是否有缺口，失败是否被解释。
- 安全与数据：权限、隐私、密钥、删除、迁移、回滚、日志泄漏。
- 可维护性：复杂度、耦合、命名、重复、错误处理是否给后续开发制造风险。
- 集成与发布：部署、迁移、文档、环境变量、feature flag、版本兼容。

## Findings 规则

Findings 必须按严重度输出：

- `P0 BLOCKER`：会导致数据丢失、安全事故、无法运行、核心功能错误或不可逆发布风险。
- `P1 MUST_FIX`：重要需求缺失、明显 bug、关键测试缺口、迁移/兼容风险。
- `P2 SHOULD_FIX`：可维护性、边界行为、错误处理、局部回归风险。
- `P3 NICE_TO_HAVE`：不阻塞合并的清理、命名、文档或轻量优化。

每条 finding 必须包含：

- 文件和行号，或明确的 diff/命令位置；
- 具体问题；
- 为什么影响需求、风险或可维护性；
- 建议修复方向；
- 需要回到哪个 CCDawn 阶段。

不要输出泛泛问题：

- “注意错误处理”
- “可以优化代码”
- “测试还不够”
- “看起来有风险”

如果没有发现问题，明确说“未发现阻塞性问题”，并列出仍未覆盖的证据边界。

## 输出契约

默认输出：

```text
PR 审阅:
- 结论: READY / READY_WITH_FIXES / NEEDS_CHANGES / BLOCKED
- 审阅范围:
  - Base/Head 或 PR:
  - 需求来源:
  - 证据来源:
- Context Boundary: diff 范围、需求/任务来源、验证证据和禁止编辑边界...

Findings:
- P0/P1/P2/P3: [文件:行] 问题；影响；建议；回到阶段

需求覆盖:
- 已覆盖:
- 未覆盖:
- 明确不做:

验证证据:
- 已有证据:
- 新增检查:
- 缺口:
- Success Evidence: diff 已审、需求已对照、关键证据已检查、阻塞项已明确或排除
- Stop Condition: 缺 diff / 缺需求来源 / 验证证据不可得 / 发布合并动作需要用户确认

Review Matrix:
- 需求覆盖: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...
- 行为正确性: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...
- 范围边界: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...
- 测试证据: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...
- 风险/发布: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...

Ledger Update:
- Current Stage: PR_REVIEWING / MERGE_READY / BLOCKED
- Verification Evidence: ...
- Unresolved Risks: ...
- Recommended Next Stage: 对应开发模式 / ccdawn-task-splitting / ccdawn-completion-summary / 提交或推送或合并准备 / ccdawn-planning / ccdawn-brt / BLOCKED
- Route Out: 对应开发模式 / ccdawn-task-splitting / ccdawn-completion-summary / 提交或推送或合并准备 / ccdawn-planning / ccdawn-brt / BLOCKED

下一步:
默认路由：<对应开发模式 / ccdawn-task-splitting / ccdawn-completion-summary / 提交或推送或合并准备 / ccdawn-planning / ccdawn-brt / BLOCKED>，原因...
执行规则：NEEDS_CHANGES 直接回最具体修复阶段；READY_WITH_FIXES 直接给修复队列或补证据路由；READY 只进入提交、推送、合并或发布准备，实际远程写入和发布动作必须等用户明确授权；只有修复顺序、需求方向或发布风险需要取舍时，才列出选项。
```

## 结论规则

- `READY`：无 P0/P1，需求覆盖和验证证据足够，剩余风险已说明且可接受。
- `READY_WITH_FIXES`：无 P0/P1，只有 P2/P3，修复后可进入 summary 或再次审阅。
- `NEEDS_CHANGES`：存在 P0/P1，或需求偏离、测试证据不足、发布风险未处理。
- `BLOCKED`：没有可审阅 diff、无法确定需求来源、验证命令无法运行且没有替代证据。

## 路由规则

- 代码问题：回到对应 owner 直接修复；只有已经确认存在独立依赖、风险或验证边界时才进入 `ccdawn-task-splitting`。
- 任务边界错误：普通情况由当前 owner 收敛；真实拆分错误才回到 `ccdawn-task-splitting`。
- 方案错误：回到 `ccdawn-planning`。
- 需求方向错误：回到 `ccdawn-brt`。
- 证据不足但实现可能正确：当前 owner 补最窄有效验证；只有正式交接才进入 `ccdawn-completion-summary`。
- 外部 review 反馈先与代码和需求核对，再决定接受、拒绝或澄清，不因 reviewer 身份盲改。
- 用户明确要独立第二审且风险足以抵消上下文成本时，可派一个只读 reviewer；主 agent 仍负责最终证据判断。

## 常见失败

- 只看测试结果，不看 diff。
- 只看 diff，不对照需求。
- 发现问题后直接修代码，导致审阅和实现混在一起。
- 把 P3 风格意见当阻塞问题。
- 没有 findings 时只说“LGTM”，没有说明证据边界。
