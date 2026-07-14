import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SUPERPOWERS_ENTRYPOINTS = (
    "using-superpowers",
    "using-skills-community",
    "brainstorming",
    "test-driven-development",
    "using-git-worktrees",
    "writing-plans",
    "subagent-driven-development",
    "dispatching-parallel-agents",
    "executing-plans",
    "finishing-a-development-branch",
    "receiving-code-review",
    "requesting-code-review",
    "systematic-debugging",
    "verification-before-completion",
    "writing-skills",
)
DISABLED_SKILL_FILENAME = "SKILL.md.ccdawn-disabled"


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))


def read_skill_name(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{skill_md} is missing YAML frontmatter.")

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if stripped.startswith("name:"):
            return stripped.split(":", 1)[1].strip().strip("'\"")

    raise SystemExit(f"{skill_md} is missing a frontmatter name field.")


def discover_skills(repo_root: Path) -> list[Path]:
    skills = []
    skill_root = repo_root / "skills"
    for path in skill_root.rglob("SKILL.md"):
        skill_dir = path.parent
        skill_name = read_skill_name(skill_dir)
        if skill_name != skill_dir.name:
            raise SystemExit(
                f"Skill folder name '{skill_dir.name}' must match frontmatter name '{skill_name}' in {path}."
            )
        skills.append(skill_dir)
    return sorted(skills, key=lambda path: path.name)


def destination_roots(home: Path, agent: str) -> list[Path]:
    roots = []
    if agent in {"claude", "all"}:
        roots.append(home / ".claude" / "skills")
    if agent in {"codex", "codex-agents", "all"}:
        roots.append(home / ".codex" / "skills")
    if agent in {"agents", "codex-agents", "all"}:
        roots.append(home / ".agents" / "skills")
    return roots


def codex_skills_root(home: Path) -> Path:
    return home / ".codex" / "skills"


def targets_codex(home: Path, roots: list[Path]) -> bool:
    return codex_skills_root(home) in roots


def process_skill_conflict_state(home: Path) -> list[tuple[str, str]]:
    root = codex_skills_root(home)
    states = []
    for name in SUPERPOWERS_ENTRYPOINTS:
        skill_dir = root / name
        active = (skill_dir / "SKILL.md").exists()
        disabled = (skill_dir / DISABLED_SKILL_FILENAME).exists()
        if active and disabled:
            state = "conflict"
        elif active:
            state = "active"
        elif disabled:
            state = "disabled"
        else:
            state = "absent"
        states.append((name, state))
    return states


def manage_process_skill_conflicts(home: Path, action: str, dry_run: bool = False) -> None:
    if action == "ignore":
        return

    root = codex_skills_root(home)
    changed = []
    blocked = []
    for name, state in process_skill_conflict_state(home):
        skill_dir = root / name
        active_path = skill_dir / "SKILL.md"
        disabled_path = skill_dir / DISABLED_SKILL_FILENAME

        if action == "warn":
            if state == "active":
                changed.append((name, "active"))
            elif state == "conflict":
                blocked.append((name, "both active and disabled entrypoints exist"))
            continue

        if state == "conflict":
            blocked.append((name, "both active and disabled entrypoints exist"))
            continue

        if action == "disable" and state == "active":
            changed.append((name, "would disable" if dry_run else "disabled"))
            if not dry_run:
                active_path.rename(disabled_path)
        elif action == "restore" and state == "disabled":
            changed.append((name, "would restore" if dry_run else "restored"))
            if not dry_run:
                disabled_path.rename(active_path)

    if action == "warn" and changed:
        print("Warning: Superpowers entrypoints can bypass CCDawn BRT routing and add unnecessary workflow context:")
        for name, _ in changed:
            print(f"  {root / name / 'SKILL.md'}")
        print("To disable only their auto-discovery entrypoints, rerun with --process-skill-conflicts disable.")
    elif changed:
        verb = "Planned process skill conflict changes" if dry_run else "Process skill conflict changes"
        print(f"{verb}:")
        for name, state in changed:
            print(f"  {name}: {state}")

    if blocked:
        print("Process skill conflict entries requiring manual inspection:")
        for name, reason in blocked:
            print(f"  {root / name}: {reason}")


def codex_validator_path(home: Path) -> Path:
    return codex_skills_root(home) / ".system" / "skill-creator" / "scripts" / "quick_validate.py"


def validate_installed_codex_skills(home: Path, installed_skills: list[Path]) -> list[Path]:
    validator = codex_validator_path(home)
    if not validator.exists():
        return []

    validated = []
    for skill_path in installed_skills:
        subprocess.run([sys.executable, str(validator), str(skill_path)], check=True)
        validated.append(skill_path)
    return validated


def validate_ccdawn_package(repo_root: Path) -> None:
    validator = repo_root / "scripts" / "validate_ccdawn_skills.py"
    if validator.exists():
        subprocess.run([sys.executable, str(validator), "--repo-root", str(repo_root)], check=True)


def print_available_skills(available_skills: list[Path]) -> None:
    print("Available skills:")
    for skill_path in available_skills:
        print(f"  {skill_path.name}")


def print_install_plan(home: Path, roots: list[Path], skill_names: list[str]) -> None:
    print("Install plan:")
    print(f"  Home: {home}")
    print("  Targets:")
    for root in roots:
        print(f"    {root}")
    print("  Skills:")
    for name in skill_names:
        print(f"    {name}")
    validator = codex_validator_path(home)
    print(f"  Codex validator: {validator if validator.exists() else 'not found'}")


def warn_duplicate_agents_copy(home: Path, selected_skill_names: set[str], roots: list[Path]) -> None:
    codex_root = codex_skills_root(home)
    agents_root = home / ".agents" / "skills"
    if codex_root not in roots or agents_root in roots or not agents_root.exists():
        return

    duplicates = sorted(name for name in selected_skill_names if (agents_root / name).exists())
    if duplicates:
        print("Warning: matching .agents skill copies already exist and may create duplicate slash-command entries:")
        for name in duplicates:
            print(f"  {agents_root / name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install this local skill library into local Codex, optional .agents, and Claude skill directories.")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available skills and exit without installing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the install plan without copying files.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Validate currently installed Codex skills without copying files.",
    )
    parser.add_argument(
        "--skip-package-validate",
        action="store_true",
        help="Skip CCDawn package convention validation before install or dry run.",
    )
    parser.add_argument(
        "--home",
        default=str(Path.home()),
        help="Home directory containing .claude, .codex, and optional .agents (default: current user home).",
    )
    parser.add_argument(
        "--agent",
        choices=["claude", "codex", "agents", "codex-agents", "all"],
        default="codex",
        help="Which local skill directories to populate (default: codex). Use codex-agents only when you explicitly need both copies.",
    )
    parser.add_argument(
        "--skill",
        dest="skills",
        action="append",
        help="Install only the named skill. Repeat for multiple skills. Defaults to all skills in the repository.",
    )
    parser.add_argument(
        "--process-skill-conflicts",
        choices=["warn", "disable", "restore", "ignore"],
        default="warn",
        help=(
            "Manage local Superpowers entrypoints that can bypass BRT routing. "
            "disable/restore renames only SKILL.md, preserving the original directory and content (default: warn)."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    home = Path(args.home).expanduser().resolve()

    available_skills = discover_skills(repo_root)
    if args.list:
        print_available_skills(available_skills)
        return 0

    available_skill_names = {path.name for path in available_skills}
    selected_skill_names = set(args.skills or sorted(available_skill_names))
    unknown = sorted(selected_skill_names - available_skill_names)
    if unknown:
        known = ", ".join(sorted(available_skill_names))
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}\nKnown skills: {known}")

    selected_skill_names_list = sorted(selected_skill_names)

    if not args.skip_package_validate:
        validate_ccdawn_package(repo_root)

    roots = destination_roots(home, args.agent)
    if args.dry_run:
        print_install_plan(home, roots, selected_skill_names_list)
        if targets_codex(home, roots):
            manage_process_skill_conflicts(home, args.process_skill_conflicts, dry_run=True)
        print("Dry run only; no files changed.")
        return 0

    if args.verify_only:
        installed_codex_skills = [codex_skills_root(home) / name for name in selected_skill_names_list]
        missing = [path for path in installed_codex_skills if not path.exists()]
        if missing:
            print("Missing installed Codex skill(s):")
            for path in missing:
                print(f"  {path}")
            return 1
        validator = codex_validator_path(home)
        if not validator.exists():
            print(f"Codex validator not found: {validator}")
            return 1
        validated_codex_skills = validate_installed_codex_skills(home, installed_codex_skills)
        print("Validated live Codex skills:")
        for path in validated_codex_skills:
            print(f"  {path}")
        manage_process_skill_conflicts(home, "warn")
        return 0

    installed_skills = []
    installed_codex_skills = []
    for root in roots:
        root.mkdir(parents=True, exist_ok=True)
        for skill_path in available_skills:
            if skill_path.name not in selected_skill_names:
                continue
            destination = root / skill_path.name
            copy_tree(skill_path, destination)
            installed_skills.append(destination)
            if root == home / ".codex" / "skills":
                installed_codex_skills.append(destination)

    validated_codex_skills = validate_installed_codex_skills(home, installed_codex_skills)
    if targets_codex(home, roots):
        manage_process_skill_conflicts(home, args.process_skill_conflicts)

    print(f"Repository: {repo_root}")
    print(f"Home: {home}")
    print("Installed skills:")
    for path in installed_skills:
        print(f"  {path}")
    if validated_codex_skills:
        print("Validated live Codex skills:")
        for path in validated_codex_skills:
            print(f"  {path}")
    elif installed_codex_skills:
        print("Codex validator not found; skipped live validation.")
    warn_duplicate_agents_copy(home, selected_skill_names, roots)
    print("Restart the client so it reloads the updated local skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
