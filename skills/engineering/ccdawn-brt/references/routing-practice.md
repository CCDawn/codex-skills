# BRT Routing Practice

Read this file only when route choice is unclear, a user asks whether routing is practical, or a new scenario needs calibration.

## Practical Route Gate

A route is actionable only when it can fill this contract:

```text
Route Contract:
- Owner:
- Mode:
- Next Output:
- Allowed Action:
- Success Evidence:
- Stop Condition:
```

If `Next Output` or `Success Evidence` is vague, the route is not ready. Probe first; if confidence remains `LOW`, run one batched collaborative discussion with 2-4 related high-impact questions before acting. Reserve a single question for a truly `BLOCKED` input.

## Owner Arbitration Gate

Before choosing planning, task splitting, development, or summary, run this compact owner check:

```text
Owner Arbitration:
- Candidate Owners: [1-3 signal-matched owners only]
- Selected Owner:
- Excluded Owners:
- Reason:
- Next Artifact:
- Success Evidence:
```

Rules:

- Pick the most specific owner that can produce the next artifact and success evidence.
- `ccdawn-planning` is only the implementation-plan owner; it must not absorb PR review, bug diagnosis, UI/design, score loop, project review, reuse research, completion summary, or evaluation.
- Development is an execution mode, not an intent owner. Enter it only after the selected owner has provided intent, boundaries, allowed actions, and success evidence.
- For composite requests, route Primary first and carry Secondary only when it shares the same contract; otherwise defer or split by owner/risk.
- If a downstream skill discovers a more specific owner, it must route back to BRT or hand off instead of continuing under the wrong owner.

## Scenario Matrix

| User signal | Primary route | Mode | Next output | Success evidence | Stop condition |
|---|---|---|---|---|---|
| "修 bug / 为什么异常 / 测试失败" with target behavior | `ccdawn-bug-review`; add `root-cause-tracing` only when source is hidden | `COMPACT_FLOW` or `FAST_PATH` | root cause plus minimal fix | failing evidence reproduced or traced, fix diff, relevant test/log passes | cannot reproduce, ownership unclear, fix crosses scope |
| "审 PR / 看 diff / 能不能合并" | `ccdawn-pr-review` | `COMPACT_FLOW` | findings ordered by risk and merge readiness | diff inspected, requirement/evidence checked, blockers named or cleared | missing diff, stale branch, merge/release decision |
| "审项目 / 架构体检 / 技术债 / 接手摸底" | `ccdawn-project-review` | `COMPACT_FLOW` | risk-ranked project review and action queue | source files inspected, evidence-linked findings, recommended next owner | requested write action or scope becomes implementation |
| "审测试代码 / 无效约束测试 / 阻碍开发的测试" | `Testing Anti-Patterns` for targeted tests; `ccdawn-project-review` for broad test system | `COMPACT_FLOW` | categorized test constraint review | each item names test file/assertion, stale assumption, dev impact, recommendation, evidence | no test scope, no refactor signal, requested write action |
| "评价方案 / 这个流程繁琐吗 / skill 是否有效" | most specific owner first; otherwise `ccdawn-evaluation` | `MICRO` or `COMPACT_FLOW` | verdict, tradeoffs, actionable improvement queue | evaluated object named, criteria stated, concrete examples or evidence | object unclear or user wants implementation |
| "我有个想法 / 不知道要什么 / 帮我挖需求 / grill me" | installed `interview-me` or `idea-refine`; fallback `ccdawn-brt` alignment | `ALIGN` | intent candidates, high-signal questions, or refined proposal | user-visible outcome, non-goals, constraints, acceptance evidence, recommended next route | answer would be generic, user wants direct execution, no stable target |
| "开发 / 添加功能 / 实现 X" before scope is classified | Minimal Sufficient Solution Gate in `ccdawn-brt` | `FAST_PATH` or `COMPACT_FLOW` | no-build / local-native reuse / minimal implementation / research decision | current project and native options checked, external research used only when it can change plan | trust-boundary risk remains, feature scope unclear, external subsystem choice is material |
| "原生能力能满足 / 已有 helper / 标准库可用 / 同一机械替换" | BRT Minimal Sufficient Solution Gate, then current implementation owner | `FAST_PATH` | minimal diff or no-build verification | existing/native/stdlib path confirmed, behavior preserved, targeted check passes | trust boundary, state/API/data/migration/release risk remains |
| "新增复杂功能 / 模块 / 编辑器 / 搜索 / 可视化 / 导入导出" with a material external subsystem choice | `ccdawn-feature-reuse-research` before planning; otherwise use project/native reuse and current owner | `COMPACT_FLOW` or `FULL_FLOW` | reuse decision or implementation implication | local/native options checked; external candidates compared only when they can change the plan | feature is local, external choice is immaterial, network blocked, user forbids research |
| "多文件实现 / 小步推进 / 自动继续 / 不要太繁琐" | first collapse same-mechanism edits with the Minimal Sufficient Solution Gate; use installed `incremental-implementation` only when distinct units remain | `FAST_PATH` or `COMPACT_FLOW` | direct minimal implementation or ordered thin slices | repeated edits treated as one unit; distinct slices have owning files and verification | slice crosses API/data/security/release risk or requires BDD/TDD |
| Restored Superpowers skill says "always / every project / any feature" | BRT process-cost gate; it remains an optional method | current BRT mode | direct execution or only the risk-relevant method | selected method changes correctness/误改 risk; skipped methods have no material value | user explicitly requests that method and current risk justifies it |
| "模型能力高 / 不要流程压住能力 / 直接高效完成" | BRT capability-aware stage collapse | current BRT mode | direct result with only necessary artifacts | outcome, protected boundary and fresh evidence are clear; skipped process has no named failure-prevention value | irreversible/high-risk action, missing evidence, real user decision or handoff artifact required |
| "用 TDD / 测试优先 / 这个软件行为回归要稳" | `ccdawn-bdd-tdd-development` compact profile for the selected deterministic engineering subtask | `COMPACT_FLOW` | minimal RED -> GREEN evidence chain | expected behavior is known, existing failure reused or one focused test fails correctly, narrow test passes | expected metric outcome is unknown, RED is environmental, task is an experiment lane |
| "派 agent / 并行做 / 多 agent 审查" | BRT subagent cost gate; parent execution remains default | `COMPACT_FLOW` or `FULL_FLOW` | zero-agent direct work or one compact contract per independent lane | disjoint ownership, independent verification, dispatch/merge cost repaid; parent verifies diff and evidence | shared files, sequential dependency, child needs full history, review chain costs more than task |
| "其他 Agent 在做什么 / 同步进度 / 文件冲突 / 讨论方案 / 快速合并 / 暂停后恢复" | `ccdawn-thread-coordination` | `COMPACT_FLOW` | live status, converged decision, pause/resume handshake, or merge order | registry/Git/thread verified; ownership, checkpoints, decision or merge evidence current | target unknown, ownership disputed, no acknowledgement, registry/thread tools unavailable |
| "初始化/同步项目记忆 / 更新 dashboard / 跨会话恢复 / 正式交接留痕" | `ccdawn-dawn-agent-html-memory`，仅在用户或项目规则明确要求，或现有 `.docs/project-memory` 是恢复所需事实源时 | `FAST_PATH` or `COMPACT_FLOW` | memory read/init/sync result or durable handoff record | source state checked, write scope bounded, rendered/registry result verified | ordinary development needs no memory write, source facts stale, tracked-memory ownership conflicts |
| "持续迭代直到目标达成 / 固定成功指标反复推进 / 需要长期 stop condition" | `ccdawn-goal-loop`，仅在用户明确需要持久迭代契约且没有更具体 owner 时 | `COMPACT_FLOW` or `FULL_FLOW` | bounded goal contract or next evidence-producing iteration | goal, constraints, success evidence, allowed actions and stop condition are explicit | finite one-turn task, specific research/score owner exists, success metric remains undefined |
| "清理开发残留 / 删除旧分支 / 移除已合并 worktree / 功能完成后收尾" | `ccdawn-development-cleanup` | `FAST_PATH` or `COMPACT_FLOW` | `CLEAN / NOOP / DEFERRED_INTEGRATION / BLOCKED` | exact candidates classified; merged/clean/unoccupied/no-claim evidence current; post-clean status verified | dirty or unmerged ownership unknown, protected/remote branch, force/path risk, active claim |
| "这个改动风险高 / 自审一下 / 我怕改错 / 生产安全" | installed `doubt-driven-development`; fallback BRT Review Matrix + `ccdawn-pr-review` | `COMPACT_FLOW` or `FULL_FLOW` | doubt list, reconciled decision, or stop condition | claims checked against code/evidence, risky assumptions surfaced, route updated | evidence unavailable, irreversible action, user must choose tradeoff |
| "这个 diff 是否过度设计 / 能删什么 / 能否更简单" | `ccdawn-simplification-review`; correctness/merge readiness stays with `ccdawn-pr-review` | `COMPACT_FLOW` | evidence-backed cuts and keep decisions | diff and requirements inspected, behavior-preservation evidence named, unrelated correctness risks routed separately | no reviewable diff, behavior boundary unclear, proposed cut changes required behavior |
| "代码太复杂 / 精简项目 / 清理冗余依赖或抽象" | `ccdawn-simplification-audit`; architecture/project health stays with `ccdawn-project-review` | `COMPACT_FLOW` | ranked simplification queue | repository evidence, exclusions, benefit/risk and verification condition named for each candidate | scope too broad, evidence missing, simplification requires architecture tradeoff |
| "前端页面 / 组件 / UI 改版 / 响应式 / 视觉不像产品" | `ccdawn-ui-design` only when visual direction, interaction states, responsive behavior, accessibility polish, or design review is a material outcome; native controls and existing-pattern mechanical UI changes stay with BRT FAST_PATH | `FAST_PATH`, `COMPACT_FLOW`, or `FULL_FLOW` | minimal UI diff, UI intent lock, design contract, or design review | user-visible outcome, design-system boundary, relevant states, accessibility/visual evidence named | no runnable UI, design target unclear, user asks for pure backend |
| "审 UI / 设计系统合规 / accessibility / responsive check" | `ccdawn-ui-design`; fallback `ccdawn-pr-review` or `ccdawn-project-review` only when UI skill is unavailable or review is primarily diff/project risk | `COMPACT_FLOW` | design-quality findings and ordered fix queue | screenshot/DOM/responsive/accessibility evidence tied to each finding | no UI target, no visual/runtime access, review turns into implementation |
| "浏览器控制 / 打开网页 / 点击填写 / 截图 / 抓页面数据" | installed `agent-browser` or `browser-testing-with-devtools`; fallback available browser skill or Playwright | `COMPACT_FLOW` | browser action result or runtime evidence | page opened, requested interaction completed, screenshot/text/DOM/network evidence captured | login/profile risk, untrusted site action, destructive form submit |
| "开发规范 / AGENTS.md / DEVELOPMENT_STANDARD / spec / 官方文档一致性" | installed `spec-driven-development`, `source-driven-development`, or `context-engineering`; fallback BRT Intent Lock + standards scan + planning | `COMPACT_FLOW` or `FULL_FLOW` | spec/rule/context decision or standards-backed plan | local rules read, framework versions/docs checked when needed, contract and verification named | standards conflict, version unknown, user wants quick local-only edit |
| "复现 AI 论文 / 研究一个模型方向 / 多轮消融 / 实验后决定继续还是转向" | `ccdawn-ai-research-loop` | `COMPACT_FLOW` or `FULL_FLOW` | baseline diagnosis, hypothesis lane, findings synthesis, or continue/branch/pivot/stop decision | baseline and evaluation protocol identified; experiment evidence remains traceable; next experiment reduces a named uncertainty | baseline untrusted, protocol/data drift, budget missing, no distinguishable hypothesis |
| "冲榜 / score 回退 / benchmark 优化 / 迭代实验 / online feedback / baseline promotion" | `ccdawn-score-loop`; Huawei NSLB uses `ccdawn-huawei-nslb-score-loop` adapter | `COMPACT_FLOW` or `FULL_FLOW` | lane, evaluation, gate decision, online calibration, package record, or recovery artifact | baseline identified, metric/commands parsed, lane has one causal mechanism, promotion/rejection evidence recorded without TDD RED/GREEN | missing metric/profile, stale baseline, source drift, ambiguous online result |
| "这个研究结论可靠吗 / 能否晋升 baseline / claim 是否过度 / 结果很反直觉" | `ccdawn-research-rigor-review` | `COMPACT_FLOW` | findings-first rigor verdict and minimal strengthening action | claim, protocol, baseline and artifacts inspected; limitations and allowed wording named | artifact missing, leakage/protocol drift unresolved, result not reproducible |
| "Kaggle / 竞赛 / leaderboard / empirical research pipeline" | `ccdawn-competition-research-lifecycle`; research stage delegates to `ccdawn-ai-research-loop`, metric lane to `ccdawn-score-loop` | `FULL_FLOW` | lifecycle stage contract, data/metric/baseline/research route | competition brief, metric, data path, baseline, submission/experiment evidence identified | missing competition source, rules/private data risk, score metric unknown |
| "创意方向 / 命名 / 新概念 / 研究 idea / 产品点子" | installed creative method router; fallback `ccdawn-creative-toolbox` | `MICRO` or `COMPACT_FLOW` | selected method and ranked concept cards | creative target, selection criteria, tradeoffs, next convergence route named | target/context too thin, user needs implementation not ideation |
| "CI 挂了 / GitHub Actions 红了 / PR checks failing" | installed `gh-fix-ci`; fallback `ccdawn-bug-review` with CI logs | `COMPACT_FLOW` | failing check summary plus fix route or diff | CI log inspected, failing command identified, local repro/fix/verification evidence | no CI access, logs missing, fix crosses release boundary |
| "处理 PR 评论 / address comments / reviewer 要求" | installed `gh-address-comments`; fallback `ccdawn-pr-review` feedback route | `COMPACT_FLOW` | comment-by-comment disposition and safe changes | each comment mapped to accept/reject/clarify with evidence and tests | PR/comment source missing, review asks for unsafe scope |
| "issue/backlog/Linear/Notion spec/把需求转任务" | installed `issue-triage`, `linear`, `github-issue-creator`, or `notion-spec-to-implementation`; fallback BRT bundle + planning | `COMPACT_FLOW` | prioritized work items, implementation contract, or issue draft | source note/log/spec inspected, scope and acceptance criteria named, next owner selected | external workspace inaccessible, item lacks product goal, write/post action needs permission |
| "做 MCP server / 接工具 / agent tool integration" | installed `mcp-builder`; fallback `ccdawn-feature-reuse-research` then `ccdawn-planning` | `FULL_FLOW` | tool protocol plan, auth/boundary decisions, evaluation path | protocol/docs checked, tool schema and failure modes named, local test strategy defined | credentials/secrets risk, protocol unknown, external service unavailable |
| "跑 webapp 测试 / 端到端验证 / 页面功能测试" | installed `webapp-testing`; fallback project test scripts + browser/Playwright | `COMPACT_FLOW` | targeted test run and evidence summary | command/browser run captured, pass/fail mapped to feature risk, next fix route named | app cannot run, auth profile risk, test target unclear |
| "Sentry 报错 / 线上错误 / production stack trace" | installed `sentry-triage`; fallback `ccdawn-bug-review` + `root-cause-tracing` | `COMPACT_FLOW` | stack-to-source diagnosis and guard/fix | issue/event inspected or pasted, stack frames mapped, repro or proof step found | no stack/event data, secrets/PII risk, cannot access source |
| "Datadog 日志 / LangSmith trace / agent eval / LLM 调用异常" | installed `datadog-logs` or `langsmith-fetch`; fallback `ccdawn-bug-review` + observability route | `COMPACT_FLOW` | log/trace digest and root-cause route | queried or pasted evidence bounded by time/source, sensitive fields avoided, failing pattern linked to code/prompt | no access, privacy risk, time range/project unknown |
| "浏览器页面验证 / console/network/DOM/screenshot/performance trace" | installed `browser-testing-with-devtools`; fallback available browser/Playwright verification | `COMPACT_FLOW` | runtime evidence plus fix/verification | page opened, console/network/DOM/screenshot/performance signal captured | no runnable app, auth/profile risk, browser content untrusted |
| "安全审查 / auth / PII / webhook / upload / payment / untrusted input" | installed `security-and-hardening`; fallback `Defense-in-Depth Validation` | `FULL_FLOW` | threat model, hardening diff or risk report | trust boundaries/assets named, validation/authorization/data handling checked | missing security context, destructive credential/permission action |
| "性能卡顿 / Core Web Vitals / 渲染慢 / 大列表 / 响应慢" | installed `performance-optimization` or `react-component-performance`; fallback project/browser review | `COMPACT_FLOW` | measurement-backed bottleneck and fix route | baseline measured, bottleneck identified, after measurement or guard exists | no measurement path, optimization would be speculative |
| "API 设计 / 公共接口 / schema / 模块边界 / props contract" | installed `api-and-interface-design`; fallback `ccdawn-planning` with interface contract | `FULL_FLOW` | contract decision and compatibility risks | public behaviors, consumers, migration/deprecation risks identified | consumers unknown, backwards compatibility unclear |
| "迁移 / 废弃旧系统 / 删除旧 API / 大规模替换" | installed `deprecation-and-migration` or `codebase-migrate`; fallback `ccdawn-planning`, then split only when phases have independent dependencies, risks, owners, or verification gates | `FULL_FLOW` | migration plan, phases, rollback, user impact | old/new systems, consumers, rollout, validation, rollback evidence | destructive action, unknown consumers, no rollback |
| "提交 / 分支 / push / 发布 / 上线 / 回滚 / 部署流水线" | installed `git-workflow-and-versioning`, `ci-cd-and-automation`, `shipping-and-launch`, or `deploy-pipeline`; fallback git tools + completion/pr review | `FULL_FLOW` | release/commit/rollback plan or gated action | worktree clean/dirty state known, tests/checks named, rollback/permission gate explicit | destructive/remote action unconfirmed, checks missing, release owner unknown |
| "日志/指标/trace/告警 / 可观测性缺口" | installed `observability-and-instrumentation`; fallback planning or current development telemetry contract | `COMPACT_FLOW` | telemetry contract or instrumentation diff | symptom, metric/log/trace field, alert/verification path defined | no observable symptom, sensitive data logging risk |
| "OpenAI/Codex/API 文档 / PDF/Word/PPT/Excel / 生成图片" | corresponding system skill when present in this turn's Available skills (`openai-docs`, `pdf`, `documents`, `presentations`, `spreadsheets`, `imagegen`); otherwise BRT fallback with capability gap | `FAST_PATH` or `COMPACT_FLOW` | artifact, official-doc answer, or file operation result | official/current source or rendered/validated artifact evidence | system skill unavailable, file missing, high-stakes decision needs more context |
| "git 历史热点 / bug magnet / bus factor / 高风险文件" | installed `codebase-recon`; fallback `ccdawn-project-review` with git history probe | `COMPACT_FLOW` | hotspot/risk map and review focus | git history analyzed, hotspots linked to current request | no git history, shallow clone, review scope too broad |
| "目标明确但要先定方案" | `ccdawn-planning` | `COMPACT_FLOW` or `FULL_FLOW` | implementation plan with scope, files, risks, validation | plan covers confirmed intent and success evidence | requirement unstable or direct FAST_PATH is enough |
| "继续 / 按推荐来 / 确认" after a prior stage | route to the recommended next owner in ledger | current flow | next stage artifact, not repeated alignment | ledger fields match current request and no new blocker | user changed goal or previous route lacks success evidence |
| "多个动作一起做" | Intent Bundle in `ccdawn-brt`; route Primary first | `COMPACT_FLOW` | ordered Primary/Secondary/Deferred or internal sequence | owner/risk/verification boundaries resolved | actions conflict or need user tradeoff |
| Review output has Guardrail, Fix, telemetry, refactor | Action Queue plus Ordered Fix Queue in `ccdawn-brt`; execute in queue order after user confirms | `COMPACT_FLOW` | next queue item executed or planned with updated queue | each item has evidence/impact/route/success evidence, and completed items have verification | stale evidence, high-risk merge/release/delete |
| Clear one-file small edit with verification | `FAST_PATH` | `SILENT` or `MICRO` | minimal diff plus verification | targeted check passes or structural evidence exists | touches state/API/data/migration/release or ownership uncertain |

## Failure Smells

- Route says only "建议进入某 skill" but cannot name the next artifact.
- Route chooses planning or development without first checking signal-matched candidate owners.
- Route recommends an intent, skill, plan, or execution order but cannot name the user signal, inference, recommendation reason, and risk if wrong.
- Route starts planning or coding before locking user-visible outcome, owning surface, non-goals, constraints, and acceptance evidence.
- Route asks library/framework/file-structure questions before behavior, scope, default, failure path, or acceptance questions.
- Route splits defaultable alignment into repeated user inputs instead of one alignment handshake with a default next action.
- Route recommends planning even though a low-risk edit can be finished and verified now.
- Route invokes task splitting only to produce `NO_SPLIT`; BRT or planning should keep that decision internal and route directly to implementation.
- Route sends every completed implementation through `ccdawn-completion-summary` even though the current owner can close with fresh evidence.
- Route starts implementing a complex/common feature without first checking local reuse, official examples, package ecosystem, GitHub, or similar projects.
- Route creates worktrees or subagents for one-theme sequential work.
- Route treats a sent pause request as proof that the other thread has paused, or starts conflicting writes before a `PAUSED` acknowledgement.
- Route resolves a cross-thread conflict but finishes without actively sending and verifying the resume notification.
- Route starts multi-agent work without reading an existing live registry, or writes full transcripts and command logs as progress.
- Route lets every Agent message every other Agent instead of one coordinator collecting positions and broadcasting the decision.
- Route merges from stale branch messages without re-reading Git target/base/head/diff and current test evidence.
- Route marks development complete without a silent cleanup check, or loads a verbose cleanup stage when there are no candidates.
- Route uses blanket `git clean`, force-deletes a branch/worktree, or treats dirty/unmerged/user-owned content as noise.
- Route lets a broad Superpowers trigger upgrade `FAST_PATH` into brainstorming, planning, worktree, strict TDD, per-task subagents, or branch finishing.
- Route treats invoking one Superpowers skill as permission to invoke its entire downstream chain.
- Route invokes a stage or generates an artifact but cannot name the concrete failure it prevents or who will reuse the output.
- Route exposes internal planning/self-review as long process narration even though no user decision or finding exists.
- Route dual-loads `ccdawn-bdd-tdd-development` and Superpowers `test-driven-development` for the same subtask.
- Route treats score regression, rejected hypothesis, candidate loss, or online neutral result as a TDD RED.
- Route sends an experiment mutation to general task splitting instead of keeping score-loop owner, unless a deterministic engineering defect was explicitly separated.
- Route sends full conversation or plan history to a child, or creates implementer/spec-reviewer/quality-reviewer chains for a bounded task.
- Route splits "实现、验证、汇报" into separate tasks without distinct owners or risks.
- Route sends review evidence gaps and confirmed defects into the same severity bucket.
- Route lists multiple fixable findings but offers only one isolated next step instead of an ordered queue.
- Route keeps asking for confirmation after the user already said "继续", "确认", or "按推荐来".
- Route treats the user as an oracle: it blindly obeys or asks "你要什么" without stating the agent's own judgment, recommendation, excluded options, and calibration question.
- Route treats leaderboard/benchmark work as ordinary planning and loses baseline, metric, lane, promotion, or online-feedback evidence.
- Route names an uninstalled GitHub skill as the only owner and provides no local fallback.
- Route handles CI, production errors, security, performance, API, migration, or observability as generic planning without the evidence those domains need.
- Route treats frontend work as "改样式" only and skips user-visible intent, design-system boundary, responsive states, browser/runtime evidence, or accessibility.
- Route handles browser control as free-form web browsing without a success artifact, profile/auth boundary, screenshot/DOM/text evidence, or stop condition for destructive actions.
- Route turns development standards into a lecture instead of reading the local rules and producing a concrete spec/context/quality gate decision.
- Route ignores a vague idea and jumps to implementation instead of extracting user-visible outcome, non-goals, constraints, and acceptance evidence.
- Route treats high-risk or production work as ordinary confidence output and skips a doubt/self-review gate.
- Route treats issue/spec/backlog text as implementation permission without converting it into a scoped contract.
- Route takes git push, release, deployment, form submit, or external workspace write actions without an explicit permission gate.

## Output Shapes

Use one line for routine routing:

```text
路由判断: Owner = ccdawn-project-review；Mode = COMPACT_FLOW；Next Output = action queue；Success Evidence = evidence-linked findings with selected next route.
意图理由: 信号=用户要求“审项目”；推断=当前价值是风险排序而不是实现；推荐=ccdawn-project-review；错判代价=直接开发会绕过架构/测试风险。
对齐握手: 我理解你要项目级风险判断；我准备只读审查并输出行动队列；我不会改代码；我会用文件证据和风险排序证明结论；如果这里不对，最该纠偏的是审查范围。
默认推进: 无自然闸门时，我将直接开始只读审查。
```

Use a reuse gate line before development:

```text
复用门控: Decision = QUICK_RESEARCH；Reason = 功能常见且外部实现可能影响方案；Scope = 当前项目已有模块 + 官方文档 + GitHub/包生态；Next Output = 复用决策。
```

Use one line for review starts that may otherwise become noisy:

```text
审查契约: Owner = Testing Anti-Patterns；Mode = COMPACT_FLOW；Next Output = categorized test constraint review；Success Evidence = test file/assertion/stale assumption/dev impact/recommendation；Context Boundary = targeted tests + direct standards + relevant diff/failure evidence.
```

Use a short queue when the user needs to choose:

```text
行动队列: Guardrail = ...；Primary Fix = ...；Telemetry Gap = ...；Deferred = ...
推荐下一步: A 执行 Primary Fix（推荐）/ B 先补 telemetry / C 暂停
```

Use an ordered queue when findings should be fixed sequentially:

```text
严重度排序: P1 ...；P2 ...；P2 ...
修复队列:
1. ... [SAFE_DIRECT]；原因 = 范围小/验证清楚/先移除误导
2. ... [PLAN_THEN_EXECUTE]；原因 = P1 但涉及 API/迁移/兼容，先方案再做
3. ... [DEFERRED]；原因 = 另一个结构面，触发条件 = ...
执行规则: 用户说“继续/开始修复/按顺序修”后从 1 开始，完成一项验证一项；遇到自然闸门才停。
```

Use a blocking question only when the contract cannot be filled:

```text
BLOCKED: 路由缺少审阅对象。请选择 A 当前 diff（推荐）/ B 指定 PR URL / C 指定文件范围。
```

Use collaborative calibration when the agent's own route or plan may be hard for the user to understand:

```text
协作校准: 我建议先做结构审查而不是直接修；原因是你现在问的是“这样做为什么合理”，不是要马上改代码；我排除直接进入实现，因为那会跳过共同理解。这样判断对吗？
A. 按推荐先拆解原因（推荐）
B. 直接进入修复
C. 暂停
```
