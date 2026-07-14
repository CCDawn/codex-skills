import argparse
import json
import re
import sys
from pathlib import Path


BRT_INTERFACE_FIELDS = [
    "Context Boundary",
    "Output Contract",
    "Allowed Action",
    "Success Evidence",
    "Stop Condition",
    "Route Out",
]

BRT_CORE_MARKERS = [
    "One-Turn Alignment",
    "Route Contract",
    "Next Action",
    "FAST_PATH",
    "COMPACT_FLOW",
    "FULL_FLOW",
    "ccdawn-simplification-review",
    "ccdawn-simplification-audit",
    "ccdawn-ai-research-loop",
    "ccdawn-research-rigor-review",
    "ccdawn-thread-coordination",
    "ccdawn-development-cleanup",
    "默认 `AUTO`",
    "能力感知与阶段折叠",
    "`FAST_PATH` 直接执行并最小验证",
    "Skill Budget",
    "约束用于防错",
    "Superpowers 默认不参与自动路由",
    "## 讨论式意图收敛",
    "低置信度不得带着未确认的高影响假设写入",
    "一次集中提出 2-4 个",
]

UNIFIED_CONTRACT_MARKERS = [
    "## 统一调用契约",
    "用户可见内容默认中文",
    "下一步建议: <一个具体动作>",
    "Route Out 仅以 BRT interface 为准",
]

DIRECT_WRITE_OWNERS = {
    "ccdawn-bdd-tdd-development",
    "ccdawn-bug-review",
    "ccdawn-design-system",
    "ccdawn-frontend-engineering",
    "ccdawn-thread-coordination",
    "ccdawn-ui-design",
}

TOKEN_BUDGETS = {
    "ccdawn-ai-research-loop": 2200,
    "ccdawn-bdd-tdd-development": 1350,
    "ccdawn-brt": 2500,
    "ccdawn-bug-review": 1200,
    "ccdawn-competition-research-lifecycle": 2500,
    "ccdawn-completion-summary": 2400,
    "ccdawn-creative-toolbox": 1400,
    "ccdawn-dawn-agent-html-memory": 1400,
    "ccdawn-development-cleanup": 1900,
    "ccdawn-design-system": 1500,
    "ccdawn-evaluation": 1000,
    "ccdawn-feature-reuse-research": 2100,
    "ccdawn-frontend-engineering": 1500,
    "ccdawn-goal-loop": 1100,
    "ccdawn-huawei-nslb-score-loop": 1200,
    "ccdawn-planning": 1600,
    "ccdawn-pr-review": 1500,
    "ccdawn-project-review": 1500,
    "ccdawn-research-rigor-review": 1600,
    "ccdawn-score-loop": 2200,
    "ccdawn-simplification-audit": 1000,
    "ccdawn-simplification-review": 1000,
    "ccdawn-task-splitting": 1350,
    "ccdawn-thread-coordination": 1300,
    "ccdawn-ui-design": 1650,
    "ccdawn-ui-review": 1350,
    "ccdawn-visual-design": 1500,
}

BRT_REFERENCE_BUDGETS = {
    "routing-practice.md": 2200,
    "runtime.md": 1800,
    "output-forms.md": 900,
}

BRT_REFERENCE_REQUIRED_MARKERS = {
    "routing-practice.md": [
        "未出现的 skill 不能成为 owner",
        "不完成一个就停下来询问",
        "多个 `SAFE_DIRECT` 项只推荐一个",
    ],
    "runtime.md": [
        "完成一个 task 不构成用户闸门",
        "当前项通过后自动进入下一个已授权项",
    ],
    "output-forms.md": [
        "已有执行许可时连续推进 `SAFE_DIRECT`",
        "只有自然闸门才提供 2-3 个具体选项",
    ],
}

BRT_PROFILE_BUDGETS = {
    "alignment": (["SKILL.md", "references/output-forms.md"], 3400),
    "routing": (["SKILL.md", "references/routing-practice.md"], 4700),
    "long-task": (["SKILL.md", "references/runtime.md"], 4300),
    "maximum": (
        [
            "SKILL.md",
            "references/output-forms.md",
            "references/routing-practice.md",
            "references/runtime.md",
        ],
        7000,
    ),
}

HOT_ROUTE_EXTERNAL_CANDIDATES = {
    "agent-browser",
    "api-and-interface-design",
    "browser-testing-with-devtools",
    "codebase-recon",
    "context-engineering",
    "doubt-driven-development",
    "incremental-implementation",
    "performance-optimization",
    "security-and-hardening",
    "spec-driven-development",
    "webapp-testing",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = read_text(skill_md)
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    values: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def parse_openai_interface(openai_yaml: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in read_text(openai_yaml).splitlines():
        match = re.match(r'^\s{2}(display_name|short_description|default_prompt):\s*["\'](.*)["\']\s*$', line)
        if match:
            values[match.group(1)] = match.group(2)
    return values


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", text))


def estimated_instruction_tokens(text: str) -> int:
    """Cheap language-aware size proxy; whitespace counts badly undercount Chinese."""
    cjk_chars = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", text))
    latin_words = len(re.findall(r"[A-Za-z0-9_]+", text))
    punctuation = len(re.findall(r"[^\w\s\u3400-\u9fff]", text))
    return cjk_chars + round(latin_words * 1.3) + punctuation // 3


def discover_skill_dirs(repo_root: Path) -> list[Path]:
    return sorted(
        [path.parent for path in (repo_root / "skills").rglob("SKILL.md")],
        key=lambda item: item.name,
    )


def rel_skill_path(repo_root: Path, skill_dir: Path) -> str:
    return "./" + skill_dir.relative_to(repo_root).as_posix()


def validate_ccdawn_route_references(
    repo_root: Path,
    skill_names: set[str],
    errors: list[str],
) -> None:
    references: dict[str, list[str]] = {}
    for markdown_path in sorted((repo_root / "skills").rglob("*.md")):
        text = read_text(markdown_path)
        for referenced_name in sorted(set(re.findall(r"\bccdawn-[a-z0-9-]+\b", text))):
            if referenced_name in skill_names:
                continue
            label = markdown_path.relative_to(repo_root).as_posix()
            references.setdefault(referenced_name, []).append(label)

    for missing_name, paths in sorted(references.items()):
        locations = ", ".join(paths[:3])
        if len(paths) > 3:
            locations += f", and {len(paths) - 3} more"
        errors.append(
            f"unresolved CCDawn route '{missing_name}' referenced by {locations}; "
            "package the skill or remove the route"
        )


def validate_skill(
    repo_root: Path,
    skill_dir: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    skill_md = skill_dir / "SKILL.md"
    text = read_text(skill_md)
    frontmatter = parse_frontmatter(skill_md)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    license_id = frontmatter.get("license", "")
    label = str(skill_md.relative_to(repo_root))

    if not name:
        errors.append(f"{label}: missing frontmatter name")
    elif name != skill_dir.name:
        errors.append(f"{label}: frontmatter name '{name}' does not match folder '{skill_dir.name}'")

    if not description:
        errors.append(f"{label}: missing frontmatter description")
    else:
        if not description.startswith("Use when"):
            errors.append(f"{label}: description must start with 'Use when'")
        if len(description) > 500:
            warnings.append(f"{label}: description is {len(description)} chars; consider shortening")

    if license_id != "MIT":
        errors.append(f"{label}: frontmatter license must be 'MIT'")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append(f"{skill_dir.relative_to(repo_root)}: missing agents/openai.yaml")
    else:
        interface = parse_openai_interface(openai_yaml)
        metadata_label = str(openai_yaml.relative_to(repo_root))
        for field in ["display_name", "short_description", "default_prompt"]:
            value = interface.get(field, "")
            if not value:
                errors.append(f"{metadata_label}: missing interface field '{field}'")
            elif name.startswith("ccdawn-") and not contains_cjk(value):
                errors.append(f"{metadata_label}: '{field}' must be Chinese-first")
        prompt = interface.get("default_prompt", "")
        if name and f"${name}" not in prompt:
            errors.append(f"{metadata_label}: default_prompt must invoke '${name}'")

    if name.startswith("ccdawn-") and name != "ccdawn-brt":
        if "## BRT interface" not in text:
            errors.append(f"{label}: missing '## BRT interface'")
        for field in BRT_INTERFACE_FIELDS:
            if field not in text:
                errors.append(f"{label}: missing BRT interface field '{field}'")

        for marker in UNIFIED_CONTRACT_MARKERS:
            if marker not in text:
                errors.append(f"{label}: unified call contract missing marker '{marker}'")

        route_out_count = len(re.findall(r"(?m)^- Route Out:", text))
        if route_out_count != 1:
            errors.append(
                f"{label}: expected exactly one canonical BRT interface Route Out, found {route_out_count}"
            )
        example_route_outs = re.findall(r"(?m)^Route Out:[^\r\n]*", text)
        if any(line.strip() not in {"Route Out:", "Route Out: <沿用 BRT interface>"} for line in example_route_outs):
            errors.append(f"{label}: output examples must not redefine the canonical Route Out")
        if re.search(r"(?m)^默认路由：<(?!从 BRT interface)[^>]+>", text):
            errors.append(f"{label}: default route examples must select from the BRT interface")

        if name in DIRECT_WRITE_OWNERS:
            route_out = re.search(r"(?m)^- Route Out:.*$", text)
            if route_out is None or "ccdawn-development-cleanup" not in route_out.group(0):
                errors.append(f"{label}: direct write owner must route verified residue to ccdawn-development-cleanup")

        if re.search(r"(?m)^Route Out: .*暂停", text):
            errors.append(f"{label}: Route Out should use BLOCKED or a concrete owner, not generic pause")
        if re.search(r"(?m)^A\. ", text):
            warnings.append(f"{label}: top-level A/B/C option menu found; ensure it is behind a natural gate")

    if name == "ccdawn-brt":
        for marker in BRT_CORE_MARKERS:
            if marker not in text:
                errors.append(f"{label}: BRT missing core marker '{marker}'")

    if name == "ccdawn-bdd-tdd-development":
        for marker in ["## 紧凑 TDD", "现有失败测试或稳定复现可直接作为 RED", "默认不派发子代理", "分数下降"]:
            if marker not in text:
                errors.append(f"{label}: compact TDD profile missing marker '{marker}'")

    if name == "ccdawn-bug-review":
        for marker in ["不要求展示固定阶段", "根因状态", "只有 `CONFIRMED`", "当前 owner 直接修复并验证"]:
            if marker not in text:
                errors.append(f"{label}: compact debugging owner missing marker '{marker}'")

    if name == "ccdawn-ui-design":
        for marker in ["## 界面契约", "响应式边界", "浏览器验证", "现有设计系统"]:
            if marker not in text:
                errors.append(f"{label}: UI owner missing marker '{marker}'")

    if name == "ccdawn-ui-review":
        for marker in ["findings 优先", "## 审查面", "真实用户任务", "浏览器能力", "ccdawn-frontend-engineering"]:
            if marker not in text:
                errors.append(f"{label}: UI review owner missing marker '{marker}'")

    if name == "ccdawn-frontend-engineering":
        for marker in ["## 生产实现", "关键状态", "响应式", "真实浏览器", "ccdawn-ui-design"]:
            if marker not in text:
                errors.append(f"{label}: frontend implementation owner missing marker '{marker}'")

    if name == "ccdawn-design-system":
        for marker in ["## 系统闸门", "## 事实源与契约", "## 渐进迁移", "多个消费者", "Figma/code"]:
            if marker not in text:
                errors.append(f"{label}: design-system owner missing marker '{marker}'")

    if name == "ccdawn-visual-design":
        for marker in ["## 语境判断", "## 视觉契约", "产品类型", "一个有依据的推荐方向", "reduced-motion"]:
            if marker not in text:
                errors.append(f"{label}: visual-design owner missing marker '{marker}'")

    if name == "ccdawn-score-loop":
        for marker in ["## 实验 owner 独占", "不是 TDD RED", "smallestDecisiveEvaluation", "## 研究回传契约"]:
            if marker not in text:
                errors.append(f"{label}: experiment/TDD boundary missing marker '{marker}'")

    if name == "ccdawn-ai-research-loop":
        for marker in ["## Baseline Gate", "## 内层实验循环", "## 外层综合与转向", "ccdawn-score-loop"]:
            if marker not in text:
                errors.append(f"{label}: AI research loop missing marker '{marker}'")

    if name == "ccdawn-research-rigor-review":
        for marker in ["## 触发闸门", "## 审查方法", "ACCEPT", "QUALIFY", "REJECT", "BLOCKED"]:
            if marker not in text:
                errors.append(f"{label}: research rigor gate missing marker '{marker}'")

    if name == "ccdawn-thread-coordination":
        for marker in [
            "CONFLICT_PAUSE_REQUEST",
            "`PAUSE_REQUEST` 不等于 `PAUSED`",
            "主动发送 `CONFLICT_RESOLVED`",
            "DISCUSSION_REQUEST",
            "MERGE_READY",
            "sync_project_memory.py --coordination-id",
            "send_message_to_thread",
            "read_thread",
            "resumePendingAgentIds",
            "`takeover`",
            "`heartbeat`",
        ]:
            if marker not in text:
                errors.append(f"{label}: thread coordination contract missing marker '{marker}'")

    compact_review_contracts = {
        "ccdawn-evaluation": [
            "无需向用户输出“复用检查”",
            "没有 finding 不展示矩阵",
            "连续执行当前契约内的 `SAFE_DIRECT` 项",
        ],
        "ccdawn-project-review": [
            "不逐项询问",
            "不默认生成项目地图、矩阵、ledger",
        ],
        "ccdawn-pr-review": [
            "findings 优先",
            "只输出有 finding 或真实证据缺口的视角",
        ],
    }
    for marker in compact_review_contracts.get(name, []):
        if marker not in text:
            errors.append(f"{label}: compact review contract missing marker '{marker}'")

    if name == "ccdawn-dawn-agent-html-memory":
        for marker in [
            "agent_coordination.py",
            "git-common-dir",
            "coordination registry",
            "--coordination-id",
            "并行 worker 不直接同步 tracked memory",
            "resumePendingAgentIds",
            "takeover",
            "cancel-resume",
        ]:
            if marker not in text:
                errors.append(f"{label}: live coordination/memory bridge missing marker '{marker}'")

    if name == "ccdawn-development-cleanup":
        for marker in [
            "静默清理检查",
            "DEFERRED_INTEGRATION",
            "git clean -fdx",
            "git branch -d",
            "git worktree remove",
            "远程分支删除必须单独授权",
        ]:
            if marker not in text:
                errors.append(f"{label}: development cleanup safety contract missing marker '{marker}'")

    if name == "ccdawn-task-splitting" and "实验 lane 不进入" not in text:
        errors.append(f"{label}: missing experiment-lane bypass for SIMPLE/BDD_TDD classification")

    route_regressions = {
        "ccdawn-planning": {
            "required": ["默认 `DIRECT_IMPLEMENTATION`", "`NO_SPLIT` 是 BRT/Planning 的内部结论"],
            "forbidden": ["默认进入 `ccdawn-task-splitting`"],
        },
        "ccdawn-task-splitting": {
            "required": ["只为已经确认需要拆分", "不能把它设为每条 Critical Path 的默认尾声"],
            "forbidden": ["默认路由到 `ccdawn-completion-summary`"],
        },
        "ccdawn-completion-summary": {
            "required": ["普通 FAST_PATH 和有界 COMPACT_FLOW", "不单独加载本 skill"],
            "forbidden": [],
        },
        "ccdawn-development-cleanup": {
            "required": ["完全干净时由当前 owner 记为 `NOOP`", "禁止 force 删除 dirty worktree"],
            "forbidden": ["git clean -fdx --force", "git branch -D"],
        },
    }
    if name in route_regressions:
        contract = route_regressions[name]
        for marker in contract["required"]:
            if marker not in text:
                errors.append(f"{label}: low-noise route contract missing marker '{marker}'")
        for marker in contract["forbidden"]:
            if marker in text:
                errors.append(f"{label}: forced-stage regression marker found '{marker}'")

    estimated_tokens = estimated_instruction_tokens(text)
    budget = TOKEN_BUDGETS.get(name)
    if budget is not None and estimated_tokens > budget:
        warnings.append(
            f"{label}: about {estimated_tokens} instruction tokens exceeds the {budget} hot-route budget"
        )


def validate_catalog(repo_root: Path, skill_dirs: list[Path], errors: list[str]) -> None:
    skill_names = sorted(path.name for path in skill_dirs)
    expected_plugin_paths = sorted(rel_skill_path(repo_root, path) for path in skill_dirs)

    plugin_path = repo_root / ".claude-plugin" / "plugin.json"
    if not plugin_path.exists():
        errors.append(".claude-plugin/plugin.json: missing")
    else:
        try:
            plugin_data = json.loads(read_text(plugin_path))
        except json.JSONDecodeError as exc:
            errors.append(f".claude-plugin/plugin.json: invalid JSON: {exc}")
        else:
            actual_paths = sorted(plugin_data.get("skills", []))
            if actual_paths != expected_plugin_paths:
                missing = sorted(set(expected_plugin_paths) - set(actual_paths))
                extra = sorted(set(actual_paths) - set(expected_plugin_paths))
                if missing:
                    errors.append(f".claude-plugin/plugin.json: missing skills {missing}")
                if extra:
                    errors.append(f".claude-plugin/plugin.json: extra skills {extra}")

    for readme_name in ["README.md", "README.zh-CN.md"]:
        readme_path = repo_root / readme_name
        if not readme_path.exists():
            errors.append(f"{readme_name}: missing")
            continue
        readme_text = read_text(readme_path)
        missing_names = [name for name in skill_names if name not in readme_text]
        if missing_names:
            errors.append(f"{readme_name}: missing skill names {missing_names}")

    brt_root = repo_root / "skills" / "engineering" / "ccdawn-brt"
    brt_text = "\n".join(read_text(path) for path in sorted(brt_root.rglob("*.md")))
    missing_routes = [name for name in skill_names if name != "ccdawn-brt" and name not in brt_text]
    if missing_routes:
        errors.append(f"ccdawn-brt: missing package owner routes {missing_routes}")

    for reference_name, budget in BRT_REFERENCE_BUDGETS.items():
        reference_path = brt_root / "references" / reference_name
        if not reference_path.exists():
            errors.append(f"ccdawn-brt/references/{reference_name}: missing")
            continue
        estimated = estimated_instruction_tokens(read_text(reference_path))
        if estimated > budget:
            errors.append(
                f"ccdawn-brt/references/{reference_name}: about {estimated} tokens exceeds {budget}"
            )
        for marker in BRT_REFERENCE_REQUIRED_MARKERS.get(reference_name, []):
            if marker not in read_text(reference_path):
                errors.append(
                    f"ccdawn-brt/references/{reference_name}: missing route regression marker '{marker}'"
                )

    for profile_name, (relative_paths, budget) in BRT_PROFILE_BUDGETS.items():
        estimated = 0
        missing_profile_files = []
        for relative_path in relative_paths:
            profile_path = brt_root / relative_path
            if not profile_path.exists():
                missing_profile_files.append(relative_path)
                continue
            estimated += estimated_instruction_tokens(read_text(profile_path))
        if missing_profile_files:
            errors.append(f"ccdawn-brt profile {profile_name}: missing {missing_profile_files}")
        elif estimated > budget:
            errors.append(f"ccdawn-brt profile {profile_name}: about {estimated} tokens exceeds {budget}")

    hot_route_text = read_text(brt_root / "references" / "routing-practice.md")
    leaked_candidates = sorted(
        candidate for candidate in HOT_ROUTE_EXTERNAL_CANDIDATES if f"`{candidate}`" in hot_route_text
    )
    if leaked_candidates:
        errors.append(
            "ccdawn-brt routing-practice: external install candidates belong in "
            f"github-skill-candidates.md, found {leaked_candidates}"
        )

    huawei_root = repo_root / "skills" / "competition" / "ccdawn-huawei-nslb-score-loop"
    for markdown_path in sorted(huawei_root.rglob("*.md")):
        if re.search(r"(?i)[A-Z]:\\Users\\", read_text(markdown_path)):
            errors.append(
                f"{markdown_path.relative_to(repo_root)}: project adapter must not hard-code a user profile path"
            )

    validate_ccdawn_route_references(repo_root, set(skill_names), errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CCDawn skill package routing and catalog conventions.")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root to validate.",
    )
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Return nonzero when warnings are found.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    skill_dirs = discover_skill_dirs(repo_root)
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dirs:
        errors.append("No skills found under skills/")

    for skill_dir in skill_dirs:
        validate_skill(repo_root, skill_dir, errors, warnings)
    validate_catalog(repo_root, skill_dirs, errors)

    if errors:
        print("CCDawn skill package validation failed:")
        for error in errors:
            print(f"  ERROR: {error}")
    if warnings:
        print("CCDawn skill package validation warnings:")
        for warning in warnings:
            print(f"  WARN: {warning}")

    if errors or (warnings and args.warnings_as_errors):
        return 1

    print(f"CCDawn skill package validation passed: {len(skill_dirs)} skills checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
