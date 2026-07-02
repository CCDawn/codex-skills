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
| CI/GitHub Actions failures | `gh-fix-ci` | ComposioHQ/awesome-codex-skills | CI logs need check-level evidence, not generic debugging. | `systematic-debugging` with CI logs |
| PR review comments | `gh-address-comments` | ComposioHQ/awesome-codex-skills | Maps reviewer comments to safe accept/reject/clarify actions. | `receiving-code-review` |
| Sentry/production stack traces | `sentry-triage` | ComposioHQ/awesome-codex-skills | Production issues need stack-to-source mapping and privacy boundaries. | `systematic-debugging` + `root-cause-tracing` |
| Git-history risk scan | `codebase-recon` | ComposioHQ/awesome-codex-skills | Hotspots, bug magnets, and bus factor improve project-review focus. | `ccdawn-project-review` with git history probe |
| Browser runtime verification | `browser-testing-with-devtools` | addyosmani/agent-skills | DOM, console, network, screenshot, and performance evidence reduce UI guesswork. | available browser skill or Playwright |
| Security hardening | `security-and-hardening` | addyosmani/agent-skills | User input, auth, PII, webhooks, uploads, payment, and third-party APIs need threat-model evidence. | `Defense-in-Depth Validation` |
| Performance profiling | `performance-optimization`; `react-component-performance` | addyosmani/agent-skills; Dimillian/Skills | Performance work should measure before optimizing and avoid speculative complexity. | `ccdawn-project-review` + runtime measurement |
| API/interface design | `api-and-interface-design` | addyosmani/agent-skills | Public contracts, module boundaries, schemas, and props create compatibility risk. | `ccdawn-planning` with interface contract |
| Migration/deprecation | `deprecation-and-migration`; `codebase-migrate` | addyosmani/agent-skills; ComposioHQ/awesome-codex-skills | Removing/replacing systems requires consumer, rollout, and rollback evidence. | `ccdawn-planning` + `ccdawn-task-splitting` |
| Observability | `observability-and-instrumentation` | addyosmani/agent-skills | Logs, metrics, traces, and alerts should be designed with symptom and privacy boundaries. | telemetry contract inside current owner |

## Installation note

When the user asks to install one of these, prefer `skill-installer` or the source repo's install command. After installation, restart Codex or open a new thread before expecting auto-trigger metadata to appear.
