import argparse
import shutil
from pathlib import Path

LEGACY_PLUGIN_NAMES = {
    "agent-html-memory-commands",
    "dawn-commands",
}


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def discover_skills(repo_root: Path) -> list[Path]:
    skills = []
    for child in repo_root.iterdir():
        if child.is_dir() and (child / "SKILL.md").exists():
            skills.append(child)
    return sorted(skills, key=lambda path: path.name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install this Codex multi-skill library into the current user's Codex directories.")
    parser.add_argument(
        "--home",
        default=str(Path.home()),
        help="Home directory containing .codex and .agents (default: current user home).",
    )
    parser.add_argument(
        "--skill",
        dest="skills",
        action="append",
        help="Install only the named skill. Repeat for multiple skills. Defaults to all skills in the repository.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    home = Path(args.home).expanduser().resolve()

    available_skills = discover_skills(repo_root)
    available_skill_names = {path.name for path in available_skills}
    selected_skill_names = set(args.skills or sorted(available_skill_names))
    unknown = sorted(selected_skill_names - available_skill_names)
    if unknown:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}")

    selected_skills = [path for path in available_skills if path.name in selected_skill_names]
    skill_dest_root = home / ".codex" / "skills"
    skill_dest_root.mkdir(parents=True, exist_ok=True)

    installed_skills = []
    for skill_path in selected_skills:
        destination = skill_dest_root / skill_path.name
        copy_tree(skill_path, destination)
        installed_skills.append(destination)

    plugin_dest_root = home / ".codex" / "plugins"
    marketplace_path = home / ".agents" / "plugins" / "marketplace.json"
    for legacy_name in sorted(LEGACY_PLUGIN_NAMES):
        legacy_path = plugin_dest_root / legacy_name
        if legacy_path.exists():
            shutil.rmtree(legacy_path)

    if marketplace_path.exists():
        import json

        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        plugins = marketplace.get("plugins", [])
        marketplace["plugins"] = [plugin for plugin in plugins if plugin.get("name") not in LEGACY_PLUGIN_NAMES]
        marketplace_path.write_text(json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Installed Codex skills:")
    for path in installed_skills:
        print(f"  {path}")
    print("Removed legacy plugin installs from this repository when present.")

    print("Restart Codex so it reloads the updated skill and plugin library.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
