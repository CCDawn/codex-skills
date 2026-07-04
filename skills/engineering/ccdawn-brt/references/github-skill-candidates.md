# GitHub Skill Candidates

Read this file only when BRT sees a specialized domain where a GitHub/community skill may outperform the current local fallback, or when the user asks to install/compare external skills.

## Routing rule

External candidates are install-gated:

- If the skill is installed in the current session, route to it.
- If it is not installed, use the local fallback and record the candidate as optional.
- Ask to install only when the fallback cannot produce the required output or the user explicitly wants the external skill.
- Do not route to a missing skill as the only owner.

## High ROI candidates found on GitHub

| Signal | GitHub candidate | Source | Why it matters | Local fallback |
|---|---|---|---|---|
| Frontend UI implementation | `frontend-ui-engineering` | addyosmani/agent-skills | Production UI work needs component architecture, accessibility, responsive behavior, interaction states, and visual polish instead of generic generated UI. | `ccdawn-feature-reuse-research` + current project UI patterns + browser verification |
| Distinctive visual design | `frontend-design` | anthropics/skills | Strong when the task is aesthetic direction, typography, palette, layout identity, or avoiding templated frontend output. | BRT intent lock + local design system scan + browser screenshot review |
| Frontend design review | `frontend-design-review` | microsoft/skills | Useful for PR/UI review, design-system compliance, accessibility, component consistency, and responsive design checks. | `ccdawn-project-review` or `ccdawn-pr-review` + browser verification |
| React/Next.js performance patterns | `vercel-react-best-practices` | vercel-labs/agent-skills | Vercel-maintained React/Next guidance is more specific for data fetching, bundle, rendering, image, and component performance issues. | `ccdawn-project-review` + runtime measurement |
| CI/GitHub Actions failures | `gh-fix-ci` | ComposioHQ/awesome-codex-skills | CI logs need check-level evidence, not generic debugging. | `systematic-debugging` with CI logs |
| PR review comments | `gh-address-comments` | ComposioHQ/awesome-codex-skills | Maps reviewer comments to safe accept/reject/clarify actions. | `receiving-code-review` |
| Sentry/production stack traces | `sentry-triage` | ComposioHQ/awesome-codex-skills | Production issues need stack-to-source mapping and privacy boundaries. | `systematic-debugging` + `root-cause-tracing` |
| Git-history risk scan | `codebase-recon` | ComposioHQ/awesome-codex-skills | Hotspots, bug magnets, and bus factor improve project-review focus. | `ccdawn-project-review` with git history probe |
| Browser runtime verification | `browser-testing-with-devtools` | addyosmani/agent-skills | DOM, console, network, screenshot, and performance evidence reduce UI guesswork. | available browser skill or Playwright |
| Browser control with compact snapshots | `agent-browser` | vercel-labs/agent-browser | Ref-based snapshots, clicks, fills, screenshots, and batch actions are useful when MCP output is too noisy or token-heavy. | available browser skill, Chrome DevTools MCP, or Playwright |
| Chrome DevTools MCP server | `chrome-devtools-mcp` | ChromeDevTools/chrome-devtools-mcp | Official DevTools MCP gives live Chrome DOM, console, network, performance, and user-flow evidence for browser tasks. | available browser skill or Playwright |
| Security hardening | `security-and-hardening` | addyosmani/agent-skills | User input, auth, PII, webhooks, uploads, payment, and third-party APIs need threat-model evidence. | `Defense-in-Depth Validation` |
| Performance profiling | `performance-optimization`; `react-component-performance` | addyosmani/agent-skills; Dimillian/Skills | Performance work should measure before optimizing and avoid speculative complexity. | `ccdawn-project-review` + runtime measurement |
| API/interface design | `api-and-interface-design` | addyosmani/agent-skills | Public contracts, module boundaries, schemas, and props create compatibility risk. | `ccdawn-planning` with interface contract |
| Migration/deprecation | `deprecation-and-migration`; `codebase-migrate` | addyosmani/agent-skills; ComposioHQ/awesome-codex-skills | Removing/replacing systems requires consumer, rollout, and rollback evidence. | `ccdawn-planning` + `ccdawn-task-splitting` |
| Observability | `observability-and-instrumentation` | addyosmani/agent-skills | Logs, metrics, traces, and alerts should be designed with symptom and privacy boundaries. | telemetry contract inside current owner |
| Requirements/spec before coding | `spec-driven-development` | addyosmani/agent-skills | Strong for unclear feature work, significant changes, architectural decisions, or cases where a spec should become the shared source of truth. | `ccdawn-brt` Intent Lock + `ccdawn-planning` |
| Official-doc-grounded implementation | `source-driven-development` | addyosmani/agent-skills | Framework/library APIs drift; source-backed implementation reduces stale-memory bugs and gives citable decisions. | official docs/web research inside current owner |
| Project context and agent rules | `context-engineering` | addyosmani/agent-skills | Useful when agents ignore conventions, hallucinate patterns, or a project needs rules/context setup before work. | local `AGENTS.md` / standards scan + `ccdawn-project-review` |
| Code quality review framework | `code-review-and-quality` | addyosmani/agent-skills | Adds a structured correctness/readability/architecture/security/performance gate for nontrivial diffs. | `ccdawn-pr-review` |
| Architecture decisions and ADRs | `documentation-and-adrs` | addyosmani/agent-skills | Public APIs, architecture decisions, and shipped features need durable context for future agents and engineers. | `ccdawn-planning` + `ccdawn-completion-summary` |
| Kaggle competition workflow | `nvidia-kaggle-skill`; `kaggle-skill` | NVIDIA/nvidia-kaggle; shepsci/kaggle-skill | Kaggle tasks need competition context, public writeups/notebooks, datasets, local reproduction, and submission workflows. | `ccdawn-competition-research-lifecycle` + `ccdawn-score-loop` |
| Kaggle score stabilization | `agentic-kaggle-skill` | FrankS-IntelLab/agentic-kaggle-skill | Score stabilization, submission troubleshooting, and kernel workflows are more specific than a generic research lifecycle. | `ccdawn-score-loop` |
| Kaggle technique library | `ds-skills` | wenmin-wu/ds-skills | Distilled notebook methods can provide reusable EDA, baseline, feature, validation, and ensembling patterns. | `ccdawn-feature-reuse-research` + `ccdawn-score-loop` |
| Empirical research skill router | `auto-empirical-research-skills` | brycewang-stanford/Auto-Empirical-Research-Skills | Large empirical pipelines benefit from a router that loads only the relevant child skill instead of a huge lifecycle prompt. | `ccdawn-competition-research-lifecycle` |
| Creative method routing | `creative-ideation` | NousResearch/hermes-agent | Best when the agent should pick one fitting ideation method instead of running every creative operator. | `ccdawn-creative-toolbox` |
| Deep ideation team | `ideation_team_skill` | bladnman/ideation_team_skill | Useful only for high-value creative sessions that need multi-role debate and synthesis. | `ccdawn-creative-toolbox` deep mode |
| Research creative thinking | `creative-thinking-for-research` | Orchestra-Research/AI-Research-SKILLs | Research ideation benefits from cognitive-science-backed frameworks rather than generic brainstorming. | `ccdawn-creative-toolbox` |

## Installation note

When the user asks to install one of these, prefer `skill-installer` or the source repo's install command. After installation, restart Codex or open a new thread before expecting auto-trigger metadata to appear.
