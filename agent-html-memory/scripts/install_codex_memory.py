import argparse
import json
import shutil
from pathlib import Path


SKILL_NAME = "agent-html-memory"
PLUGIN_NAME = "agent-html-memory-commands"


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


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


def upsert_plugin_entry(data: dict) -> None:
    entry = {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./.codex/plugins/{PLUGIN_NAME}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Engineering",
    }

    plugins = data.setdefault("plugins", [])
    for index, existing in enumerate(plugins):
        if existing.get("name") == PLUGIN_NAME:
            plugins[index] = entry
            break
    else:
        plugins.append(entry)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install agent-html-memory skill and slash-command plugin into Codex.")
    parser.add_argument(
        "--home",
        default=str(Path.home()),
        help="Home directory containing .codex and .agents (default: current user home).",
    )
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    skill_root = Path(__file__).resolve().parents[1]
    repo_root = Path(__file__).resolve().parents[2]

    skill_src = skill_root
    plugin_src = repo_root / "plugins" / PLUGIN_NAME

    codex_skill_dst = home / ".codex" / "skills" / SKILL_NAME
    codex_plugin_dst = home / ".codex" / "plugins" / PLUGIN_NAME
    marketplace_path = home / ".agents" / "plugins" / "marketplace.json"

    if not plugin_src.exists():
        raise SystemExit(
            f"Expected bundled plugin source at {plugin_src}. Restore the repository plugin files before running install."
        )

    codex_skill_dst.parent.mkdir(parents=True, exist_ok=True)
    codex_plugin_dst.parent.mkdir(parents=True, exist_ok=True)

    copy_tree(skill_src, codex_skill_dst)
    copy_tree(plugin_src, codex_plugin_dst)

    marketplace = load_marketplace(marketplace_path)
    marketplace.setdefault("name", "local")
    marketplace.setdefault("interface", {}).setdefault("displayName", "Local Plugins")
    upsert_plugin_entry(marketplace)
    save_marketplace(marketplace_path, marketplace)

    print("Installed Codex skill:")
    print(f"  {codex_skill_dst}")
    print("Installed Codex plugin:")
    print(f"  {codex_plugin_dst}")
    print("Updated marketplace:")
    print(f"  {marketplace_path}")
    print("Restart Codex, then install/enable 'Project Memory Commands' from Local Plugins if needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
