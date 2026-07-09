---
name: ccdawn-creative-toolbox
description: "Use when the user wants context-aware concept collision, unknown concept generation, divergent thinking, creative ideation, concept invention, paradigm exploration, unusual alternatives, product ideas, research concepts, strategy concepts, story concepts, or surprising but useful options."
---

# Creative Toolbox

## Goal

Use current context to generate genuinely new, nameable concepts instead of ordinary suggestion lists.

This skill should reduce creative noise: extract the useful tension, run a small set of high-yield operators, then return concept cards that can be judged, tested, or routed into planning.

## Default behavior

- Do not turn every creative request into a long ritual.
- Do not ask whether to enable role collision by default.
- Default `Collision Forum` is `skipped`.
- Enable `Collision Forum` only when the user explicitly asks for it, the creative quality clearly depends on multi-role debate, or BRT routes the request as deep co-creation.
- Use 3-5 operators, not the whole toolbox.
- Every final new concept must have a name, a mechanism, a source collision, and a next experiment.

## Minimal flow

1. Identify the creative target: product idea, research direction, naming, story/world concept, strategy, interface, or problem reframing.
2. Extract context materials: concept atoms, hidden tensions, evidence gaps, abnormal signals, unnamed needs, and hard boundaries.
3. Choose 3-5 operators:
   - required: `Context Collision`
   - required for new concepts/names: `Naming Forge`
   - at least one distant analogy or cross-domain mechanism
   - at least one assumption breaker, reversal, extreme constraint, or contradiction solver
4. Generate unnamed concept embryos before naming or judging.
5. Name and refine the strongest embryos.
6. Evaluate with 2-4 relevant perspectives; use top-talent role cards only when the task needs strong adversarial judgment.
7. Return 3-7 concept cards plus one recommended next step.

Load `references/full-toolbox.md` only when the user asks for a full creative run, needs detailed operator rules, wants Collision Forum, or the short flow is not enough.

Load `references/role-deck.md` only when running `Perspective Jury` with top-talent role cards.

## Operator menu

| Operator | Use when | Output |
|---|---|---|
| Context Collision | Always | Source materials plus new mechanism |
| Naming Forge | Naming or new concepts | Main name, alternatives, rejected names |
| Assumption Breaker | Brief is conventional | Reversed assumptions and opportunities |
| Cross-Domain Analogy | Need fresh structure | Borrowed mechanism, not surface style |
| Extreme Constraint | Need sharper ideas | Designs that survive a hard limit |
| Concept Fusion | Two ideas can combine | Third concept with a new mechanism |
| Mutation | Existing idea is close | Variants with changed user, scale, medium, or interaction |
| Contradiction Solver | Goals conflict | Layered or staged resolution |
| Novelty Filter | Output feels generic | Removed obvious ideas and survivors |
| Perspective Jury | Need self-review | Challenge, evidence, verdict |
| Collision Forum | User wants debate | Short multi-role exchange and second-generation ideas |

## Concept quality gate

A concept is eligible only when it:

- comes from at least two current context materials;
- changes a mechanism or relationship, not just wording;
- names something the user could not previously discuss clearly;
- can generate a follow-up function, experiment, story beat, metric, or decision;
- survives a usefulness check and at least one skeptical challenge.

Downgrade it to a normal idea if it is only an existing feature with a prettier name.

## Compact output

```text
创意调用:
- Target: ...
- Operators: ...
- Collision Forum: skipped / enabled, because ...
- Context Materials: ...

概念胚胎:
| Embryo | Source Collision | New Mechanism | Why It Is Not Generic |

新概念卡:
| Name | Definition | Source Collision | Mechanism | Newness | Next Experiment |

筛选:
- Safe:
- Sharp:
- Strange:
- Recommended:

Review:
- Challenge:
- Evidence:
- Verdict:

Route Out:
- ccdawn-planning / ccdawn-feature-reuse-research / ccdawn-evaluation / pause
```

Use the full output contract in `references/full-toolbox.md` only for deep creative sessions.

## BRT interface

- Context Boundary: user brief, current conversation context, extracted concept materials, and any explicit domain constraints.
- Output Contract: named concept cards, quality gate result, recommendation, and next route.
- Allowed Action: generate and evaluate concepts only; implementation, external research, asset creation, or code changes require routing to the proper owner.
- Success Evidence: each concept has source collision, mechanism, name, novelty reason, and testable next experiment.
- Stop Condition: creative target unclear, insufficient context materials, user asks to converge into implementation, or safety/ownership constraints block the concept.
- Route Out: `ccdawn-planning`, `ccdawn-feature-reuse-research`, `ccdawn-evaluation`, or back to `ccdawn-brt` for alignment.

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

## Common mistakes

- Asking for permission to run a long debate when a compact creative answer would help more.
- Producing a list of reasonable suggestions without new mechanisms.
- Naming too early and letting the name hide a weak concept.
- Using generic roles such as "user" and "engineer" when the task needs sharp expert evaluation.
- Keeping all weird ideas or deleting all weird ideas; filter by mechanism and testability.
