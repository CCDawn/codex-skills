---
name: ccdawn-visual-design
description: Use when a UI task primarily needs a distinctive but context-appropriate visual direction, brand expression, typography, color system, composition, imagery, iconography, or motion language before implementation; do not use for information architecture, routine product UI, design-system governance, implementation of an accepted direction, or review-only findings.
license: MIT
---

# CCDawn Visual Design

## 目标

把产品目的、受众和内容转成有辨识度且可实施的视觉语言。主动推断合适方向并给出推荐，不让用户先掌握设计术语；视觉强度服务任务，不以“独特”为理由牺牲可读性、性能或产品效率。

## BRT interface

- Context Boundary: 产品/品牌、受众、使用场景、内容与资产、目标 surface、现有视觉基线、技术和无障碍约束。
- Output Contract: 一个推荐视觉方向及其字体、色彩、构图、图像、图标、动效和关键组件表达，必要时附少量有实质差异的备选。
- Allowed Action: 分析现有产品和资产、形成视觉契约、制作必要原型或在授权范围内调整视觉实现；不改变无关信息架构、业务行为或全局设计系统。
- Success Evidence: 视觉决策与用户任务的对应关系、关键 surface 的真实渲染、目标视口和内容压力检查，以及无障碍/性能边界。
- Stop Condition: 品牌资产或产品定位存在高影响冲突、视觉方向会改变核心布局但未对齐、所需素材不可获得，或实施越过授权范围。
- Route Out: 信息架构或交互模型转 `ccdawn-ui-design`；生产实现转 `ccdawn-frontend-engineering`；系统 token/主题治理转 `ccdawn-design-system`；现有结果审查转 `ccdawn-ui-review`；验证后的真实残留转 `ccdawn-development-cleanup`；阻塞回 `ccdawn-brt`。

## 统一调用契约

- 只处理 BRT interface 范围；默认输出一个有依据的推荐方向，而不是风格名称堆砌。低影响细节由 agent 自行决策。
- 用户可见内容默认中文，只说明会改变实现的视觉决策、证据和取舍；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 BRT interface 为准，末行写 `下一步建议: <一个具体动作>`。

## 语境判断

- SaaS、CRM、后台、编辑器和运营工具：优先扫描、比较、密度、稳定层级和重复操作效率，辨识度来自精确而非装饰。
- 品牌、产品、作品集、活动和展示页面：品牌或对象必须成为首屏信号，可用图像、字体、构图和节奏建立记忆点。
- 游戏和创意体验：可以更具表现力，但交互反馈、可读性和性能仍是硬边界。
- 已有产品：先读取品牌资产、相邻页面、token 和组件；除非用户明确要求重塑，不引入不兼容的平行视觉语言。

用户只说“更好看、现代一点、有高级感”时，先结合产品类型和现有证据形成推荐。只有两个方向会显著改变布局、素材、品牌感知或实施成本时，集中给出 2-3 个具体方向，并说明推荐、行为差异和错判影响。

## 视觉契约

- 概念：用一句可执行原则说明视觉如何支持产品，而不是只给风格标签。
- 字体：定义 display/body/mono 的角色、层级、字重、行高和长文本行为；字体选择兼顾语言覆盖、加载和许可。
- 色彩：定义背景、surface、文本、边框、accent 和状态语义；保证对比度且不只靠颜色传达状态。
- 构图：根据内容优先级选择网格、密度、留白、对齐和节奏；避免默认 hero、均匀卡片阵列和无内容依据的装饰。
- 图像与图标：优先展示真实产品、对象、地点、人物或状态；图标来自项目已有库，核心图片必须可检查而非纯氛围填充。
- 动效：只设计能解释层级、状态变化、空间关系或品牌时刻的运动；明确 reduced-motion 和低性能降级。
- 细节：圆角、阴影、边框、纹理和背景效果形成有限体系，不同时堆叠多个视觉手法。

避免把任何字体、颜色、渐变或布局永久列为禁用项。问题是脱离语境的惯性选择，而不是某个视觉元素本身。

## 实施与验证

1. 读取真实内容和最长/最短样本，先验证层级与构图，再精修装饰。
2. 复用项目 token 和组件；新视觉语言跨多个消费者时转 `ccdawn-design-system` 建立系统契约。
3. 核心图像缺失且视觉结果依赖它时，使用本轮 Available skills 中的图像能力生成或寻找合适资产，不用临时渐变替代真实主体。
4. 可运行时在浏览器检查主要视口、长文本、关键状态、资源加载、console、溢出和动效降级；截图必须能看清实际产品或内容。
5. 比较结果是否实现概念原则、支持主任务并保持现有行为；没有运行证据时不声称视觉完成。

正文末行保留：`下一步建议: <一个具体动作>`。
