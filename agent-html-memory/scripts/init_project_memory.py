from __future__ import annotations

import argparse
from pathlib import Path

from memory_model import ensure_directories, utc_now, write_json
from render_overview import refresh_outputs


SECTION_PRESETS = {
    "general": [
        "summary",
        "lanes",
        "progress",
        "modules",
        "decisions",
        "issues",
        "todos",
        "techNotes",
        "recentUpdates",
    ],
    "frontend": [
        "summary",
        "lanes",
        "progress",
        "modules",
        "issues",
        "todos",
        "decisions",
        "techNotes",
        "recentUpdates",
    ],
    "backend": [
        "summary",
        "lanes",
        "progress",
        "modules",
        "decisions",
        "issues",
        "todos",
        "techNotes",
        "recentUpdates",
    ],
    "automation": [
        "summary",
        "lanes",
        "progress",
        "issues",
        "todos",
        "modules",
        "techNotes",
        "recentUpdates",
        "decisions",
    ],
    "research": [
        "summary",
        "lanes",
        "progress",
        "techNotes",
        "issues",
        "todos",
        "decisions",
        "recentUpdates",
        "modules",
    ],
}


LABEL_PRESETS = {
    "general": {},
    "frontend": {
        "modules": "Features and Surfaces",
        "techNotes": "Implementation Notes",
    },
    "backend": {
        "modules": "Services and Modules",
        "techNotes": "Operational Notes",
    },
    "automation": {
        "modules": "Flows and Steps",
        "progress": "Automation Status",
    },
    "research": {
        "modules": "Workstreams",
        "decisions": "Research Decisions",
        "techNotes": "Evidence and Notes",
    },
}


def build_memory(project_name: str, project_type: str) -> dict:
    now = utc_now()
    return {
        "project": {
            "name": project_name,
            "type": project_type,
            "root": ".",
            "memoryVersion": 2,
        },
        "summary": {
            "currentPhase": "Shared memory active",
            "health": "green",
            "focus": "See active lanes",
            "lastUpdated": now,
        },
        "progress": {
            "percent": 0,
            "status": "Memory ready",
            "milestones": [
                {
                    "title": "Shared HTML memory initialized",
                    "status": "done",
                    "note": "Created global memory shell, lanes directory, overview, and root shortcut.",
                }
            ],
        },
        "recentUpdates": [
            {
                "timestamp": now,
                "title": "Initialized shared project memory",
                "details": "Created memory.json, profile.json, overview.html, INDEX.md, inbox.json, lanes/, archive/, and PROJECT_MEMORY.html.",
            }
        ],
        "lanes": [],
    }


def build_profile(project_type: str) -> dict:
    if project_type not in SECTION_PRESETS:
        raise ValueError(f"Unsupported project type: {project_type}")
    return {
        "projectType": project_type,
        "sections": SECTION_PRESETS[project_type],
        "labels": LABEL_PRESETS[project_type],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a project memory dashboard.")
    parser.add_argument("project_root", help="Path to the target project root.")
    parser.add_argument(
        "--project-type",
        default="general",
        choices=sorted(SECTION_PRESETS.keys()),
        help="Project profile preset to use.",
    )
    parser.add_argument(
        "--project-name",
        default=None,
        help="Optional display name. Defaults to the project root folder name.",
    )
    parser.add_argument(
        "--skip-agents-rules",
        action="store_true",
        help="Skip writing the Project Memory Rules block into AGENTS.md.",
    )
    return parser.parse_args()


def load_agents_snippet() -> str:
    snippet_path = Path(__file__).resolve().parents[1] / "references" / "AGENTS-snippet.md"
    text = snippet_path.read_text(encoding="utf-8")
    marker = "```md"
    start = text.find(marker)
    end = text.rfind("```")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not parse AGENTS snippet.")
    return text[start + len(marker):end].strip() + "\n"


def inject_agents_rules(project_root: Path) -> None:
    agents_path = project_root / "AGENTS.md"
    snippet = load_agents_snippet()
    content = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    if "## Project Memory Rules" in content:
        return
    separator = "\n\n" if content and not content.endswith("\n\n") else ""
    agents_path.write_text(content + separator + snippet, encoding="utf-8")


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    memory_dir, _ = ensure_directories(project_root)

    project_name = args.project_name or project_root.name
    memory = build_memory(project_name, args.project_type)
    profile = build_profile(args.project_type)

    write_json(memory_dir / "memory.json", memory)
    write_json(memory_dir / "profile.json", profile)
    write_json(memory_dir / "inbox.json", {"captures": []})
    refresh_outputs(project_root, memory, profile)
    if not args.skip_agents_rules:
        inject_agents_rules(project_root)

    print(f"Initialized project memory at {memory_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
