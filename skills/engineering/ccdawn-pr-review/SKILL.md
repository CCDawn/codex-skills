---
name: ccdawn-pr-review
description: Use when CCDawn development has completed or a PR/diff is ready for review before merge, push, release, or handoff; applies when code changes must be checked against aligned requirements, task graph, verification evidence, regressions, security/data risks, and merge readiness.
---

# CCDawn PR Review

## 目标

对已经完成的 CCDawn 任务、分支、PR 或本地 diff 做证据化审阅，判断是否可以进入提交、推送、PR、合并或发布。

此阶段只审阅，不修代码。发现问题后，把用户路由回合适阶段。

核心原则：

```text
没有读 diff、需求和证据，就不要说 ready。
```

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
- 不用审阅阶段顺手修复问题。需要修复时，路由到 `ccdawn-bdd-tdd-development`。
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

Review Matrix:
- 需求覆盖: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...
- 行为正确性: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...
- 测试证据: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...
- 风险/发布: PASS/NEEDS_CHANGE/ACCEPT_RISK，证据...

Ledger Update:
- Current Stage: PR_REVIEWING / MERGE_READY / BLOCKED
- Verification Evidence: ...
- Unresolved Risks: ...
- Recommended Next Stage: ccdawn-bdd-tdd-development / ccdawn-completion-summary / 提交/推送/合并 / 暂停

下一步:
A. 回到 ccdawn-bdd-tdd-development 修复 P0/P1（有阻塞问题时推荐）...
B. 回到 ccdawn-completion-summary 补证据或重做完成判断...
C. 提交/推送/合并/发布（READY 时推荐）...
D. 回到 ccdawn-brt 或 ccdawn-planning 调整方向...
```

## 结论规则

- `READY`：无 P0/P1，需求覆盖和验证证据足够，剩余风险已说明且可接受。
- `READY_WITH_FIXES`：无 P0/P1，只有 P2/P3，修复后可进入 summary 或再次审阅。
- `NEEDS_CHANGES`：存在 P0/P1，或需求偏离、测试证据不足、发布风险未处理。
- `BLOCKED`：没有可审阅 diff、无法确定需求来源、验证命令无法运行且没有替代证据。

## 路由规则

- 代码问题：回到 `ccdawn-bdd-tdd-development`，按任务和 TDD 修。
- 任务拆分错误：回到 `ccdawn-task-splitting`。
- 方案错误：回到 `ccdawn-planning`。
- 需求方向错误：回到 `ccdawn-brt`。
- 证据不足但实现可能正确：回到 `ccdawn-completion-summary` 补验证总结。
- 外部 review 反馈需要处理时，使用 `receiving-code-review` 的“先验证再执行”原则。
- 用户明确要独立第二审时，可使用 `requesting-code-review` 派发只读 reviewer。

## 常见失败

- 只看测试结果，不看 diff。
- 只看 diff，不对照需求。
- 发现问题后直接修代码，导致审阅和实现混在一起。
- 把 P3 风格意见当阻塞问题。
- 没有 findings 时只说“LGTM”，没有说明证据边界。
