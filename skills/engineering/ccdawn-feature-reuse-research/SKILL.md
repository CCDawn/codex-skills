---
name: ccdawn-feature-reuse-research
description: Use when CCDawn workflow is about adding a complex feature, capability, module, workflow, UI component, integration, parser, editor, search, visualization, algorithm, import/export, or reusable subsystem where existing projects, libraries, examples, or modules may change the implementation plan.
---

# CCDawn Feature Reuse Research

## 目标

在复杂功能进入方案制定前，先做只读复用研究：搜索相关项目、库、模块、官方示例和成熟实现，评估是否值得复用、改造、只参考，或自研。

本 skill 不写代码、不安装依赖、不把外部代码直接复制进项目。它输出一个可交给 `ccdawn-planning` 的复用决策。

## 进入条件

使用前确认：

- 用户目标是新增功能、模块、能力、工作流、复杂 UI、集成、解析器、编辑器、搜索、可视化、导入导出、算法或可复用子系统；
- 功能复杂度足以影响方案选择，且外部生态可能已有成熟实现；
- 搜索结果会改变实现路径、依赖选择、风险、成本或验证方式；
- 允许联网搜索。若当前不能联网，说明限制，并用本地已有依赖、文档和代码做降级研究。

不使用本 skill：

- 单点小改、样式调整、普通 bug 修复、机械重构；
- 用户明确要求从零实现；
- 功能高度私有，外部实现没有可比价值；
- 复用只会增加依赖、许可证、维护或集成负担。

## 研究范围

按功能类型选择 2-4 类来源，不要盲目铺开：

- 官方文档和官方示例：框架、SDK、协议、浏览器/API、平台能力。
- 包管理器生态：npm、PyPI、Cargo、Go modules、Maven、NuGet 等。
- GitHub 项目：相似产品、组件库、插件、参考实现、算法实现。
- 当前项目内复用：已有模块、工具函数、设计系统、服务接口、测试 helper。
- 标准/论文/规范：协议、格式、算法、互操作行为。

优先级：

1. 当前项目已有可复用模块；
2. 官方推荐库或官方示例；
3. 活跃、许可证清晰、测试充分的成熟库；
4. 可参考的开源项目设计；
5. 自研。

## 候选筛选

每个候选必须有明确价值，不凑数。最多保留 3-5 个候选。

候选字段：

- Name / Link：名称和来源链接；
- Capability Fit：覆盖目标功能的哪些部分；
- License：许可证是否允许当前项目使用；
- Activity：维护活跃度、近期提交、issue 状态、发布频率；
- Integration Cost：接入成本、依赖体积、框架/语言/运行时兼容；
- Adaptation Cost：需要改造的程度；
- Testability：是否容易写测试和验证；
- Project Fit：是否符合当前架构、代码风格、依赖边界和长期维护能力；
- Risk：供应链、弃维护、过度依赖、API 不稳定、性能或可扩展性风险。

如果找不到有价值候选，也要输出 `BUILD_IN_HOUSE`，并说明搜索证据和自研边界。

## 决策规则

输出一个主决策：

- `REUSE`：直接引入库或模块，适合成熟、低集成成本、许可证清晰、测试充分。
- `ADAPT`：借用模块或局部实现思路，需要包装、裁剪或适配当前架构。
- `REFERENCE_ONLY`：只参考设计、API、数据结构、交互或测试思路，不引入依赖。
- `BUILD_IN_HOUSE`：自研，原因可能是需求特殊、候选不活跃、许可证不合适、集成成本高或依赖风险大。
- `BLOCKED`：无法搜索、许可证不明、需求不清或必须用户选择。

评估权重：

- 用户目标贴合度 > 当前项目适配度 > 维护活跃度 > 可测试性 > 集成成本 > 依赖体积。
- 不因为“有现成库”就默认复用；复用必须降低总体成本或风险。
- 不因为“能自研”就跳过研究；复杂常见功能必须解释为什么不复用。

## 输出契约

```text
复用研究:
- 目标功能:
- 搜索范围:
- Context Boundary: 用户目标、当前项目可复用点、网络/本地搜索范围、排除范围...
- 当前项目已有复用点:
- 结论: REUSE / ADAPT / REFERENCE_ONLY / BUILD_IN_HOUSE / BLOCKED
- 推荐原因:

候选评估:
- 候选: 名称 / 链接
  - Fit:
  - License:
  - Activity:
  - Integration Cost:
  - Adaptation Cost:
  - Testability:
  - Project Fit:
  - Risk:
  - Verdict: keep / reject；原因...

复用决策:
- Decision:
- Dependency Impact:
- Implementation Boundary:
- Verification Strategy:
- Rejected Alternatives:
- Success Evidence: 当前项目复用点已查、候选有链接/本地证据、许可证/集成风险已判断
- Stop Condition: 无法搜索 / 许可证不明 / 需求不清 / 复用会改变用户未确认范围

下一步:
A. 进入 ccdawn-planning，按复用决策制定方案（推荐）...
B. 继续搜索指定方向...
C. 放弃复用，直接规划自研...
D. 回到 ccdawn-brt 重新对齐需求...

Route Out: ccdawn-planning / 继续复用研究 / ccdawn-brt / 暂停
```

## 质量门槛

- 必须给链接或本地证据；不能写“可能有库”“应该可以参考”。
- 必须说明被拒绝候选为什么不适合。
- 许可证不清时不能推荐 `REUSE`。
- 未检查当前项目已有模块时，不能推荐外部依赖。
- 不安装、不运行、不复制外部代码；需要试用库时，先进入 `ccdawn-planning` 建立执行契约。
- 如果搜索会花费大量时间，先做 QUICK 研究，再建议是否继续 DEEP 研究。
- 进入 `ccdawn-planning` 前，必须把 `复用决策` 作为方案输入。
