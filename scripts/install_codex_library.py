import argparse
import json
import shutil
from pathlib import Path

DEPRECATED_PLUGIN_NAMES = {
    "agent-html-memory-commands",
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


def discover_plugins(repo_root: Path) -> list[Path]:
    plugins_root = repo_root / "plugins"
    if not plugins_root.exists():
        return []
    plugins = []
    for child in plugins_root.iterdir():
        if child.is_dir() and (child / ".codex-plugin" / "plugin.json").exists():
            plugins.append(child)
    return sorted(plugins, key=lambda path: path.name)


def load_marketplace(path: Path) -> dict:
    if not path.exists():
        return {
            "name": "local",
            "interface": {"displayName": "Local Plugins"},
            "plugins": [],
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_marketplace(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def upsert_plugin_entry(data: dict, plugin_name: str) -> None:
    entry = {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": f"./.codex/plugins/{plugin_name}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Engineering",
    }

    plugins = data.setdefault("plugins", [])
    for index, existing in enumerate(plugins):
        if existing.get("name") == plugin_name:
            plugins[index] = entry
            break
    else:
        plugins.append(entry)


def remove_plugin_entry(data: dict, plugin_name: str) -> None:
    plugins = data.get("plugins", [])
    data["plugins"] = [plugin for plugin in plugins if plugin.get("name") != plugin_name]


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
    parser.add_argument(
        "--skip-plugins",
        action="store_true",
        help="Skip installing bundled Codex plugins and marketplace entries.",
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

    installed_plugins = []
    marketplace_path = home / ".agents" / "plugins" / "marketplace.json"
    if not args.skip_plugins:
        plugin_dest_root = home / ".codex" / "plugins"
        plugin_dest_root.mkdir(parents=True, exist_ok=True)
        marketplace = load_marketplace(marketplace_path)
        marketplace.setdefault("name", "local")
        marketplace.setdefault("interface", {}).setdefault("displayName", "Local Plugins")

        for deprecated_name in sorted(DEPRECATED_PLUGIN_NAMES):
            deprecated_path = plugin_dest_root / deprecated_name
            if deprecated_path.exists():
                shutil.rmtree(deprecated_path)
            remove_plugin_entry(marketplace, deprecated_name)

        for plugin_path in discover_plugins(repo_root):
            destination = plugin_dest_root / plugin_path.name
            copy_tree(plugin_path, destination)
            installed_plugins.append(destination)
            upsert_plugin_entry(marketplace, plugin_path.name)

        save_marketplace(marketplace_path, marketplace)

    print("Installed Codex skills:")
    for path in installed_skills:
        print(f"  {path}")

    if installed_plugins:
        print("Installed Codex plugins:")
        for path in installed_plugins:
            print(f"  {path}")
        print("Updated marketplace:")
        print(f"  {marketplace_path}")

    if args.skip_plugins:
        print("Skipped bundled plugin installation.")

    print("Restart Codex so it reloads the updated skill and plugin library.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
