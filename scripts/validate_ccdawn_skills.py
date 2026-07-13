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
    "默认 `AUTO`",
    "能力感知与阶段折叠",
    "`FAST_PATH` 直接执行并最小验证",
    "Skill Budget",
    "约束用于防错",
    "Superpowers 默认不参与自动路由",
]


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

    if not (skill_dir / "agents" / "openai.yaml").exists():
        errors.append(f"{skill_dir.relative_to(repo_root)}: missing agents/openai.yaml")

    if name.startswith("ccdawn-") and name != "ccdawn-brt":
        if "## BRT interface" not in text:
            errors.append(f"{label}: missing '## BRT interface'")
        for field in BRT_INTERFACE_FIELDS:
            if field not in text:
                errors.append(f"{label}: missing BRT interface field '{field}'")

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
    }
    if name in route_regressions:
        contract = route_regressions[name]
        for marker in contract["required"]:
            if marker not in text:
                errors.append(f"{label}: low-noise route contract missing marker '{marker}'")
        for marker in contract["forbidden"]:
            if marker in text:
                errors.append(f"{label}: forced-stage regression marker found '{marker}'")

    token_budgets = {
        "ccdawn-brt": 4500,
        "ccdawn-planning": 1800,
        "ccdawn-task-splitting": 1600,
        "ccdawn-completion-summary": 3000,
        "ccdawn-bug-review": 1800,
    }
    estimated_tokens = estimated_instruction_tokens(text)
    budget = token_budgets.get(name)
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
