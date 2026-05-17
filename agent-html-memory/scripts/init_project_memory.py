from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from render_overview import render_html, render_index


SECTION_PRESETS = {
    "general": [
        "summary",
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_memory(project_name: str, project_type: str) -> dict:
    now = utc_now()
    return {
        "project": {
            "name": project_name,
            "type": project_type,
            "root": ".",
            "memoryVersion": 1,
        },
        "summary": {
            "currentPhase": "Setup",
            "health": "green",
            "focus": "Initialize project memory",
            "lastUpdated": now,
        },
        "progress": {
            "percent": 0,
            "status": "Not started",
            "milestones": [
                {
                    "title": "Project memory initialized",
                    "status": "done",
                    "note": "Base dashboard and structured files created.",
                }
            ],
        },
        "modules": [],
        "decisions": [],
        "issues": [],
        "todos": [
            {
                "title": "Fill in project summary",
                "status": "open",
                "owner": "agent",
                "notes": "Replace setup placeholders after first real task.",
            }
        ],
        "techNotes": [
            {
                "title": "Memory system",
                "body": "Source of truth lives in memory.json. overview.html is generated and should be refreshed after updates.",
            }
        ],
        "recentUpdates": [
            {
                "timestamp": now,
                "title": "Initialized project memory",
                "details": "Created memory.json, profile.json, overview.html, INDEX.md, inbox.json, and archive scaffolding.",
            }
        ],
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
    memory_dir = project_root / ".docs" / "project-memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = memory_dir / "archive"
    archive_dir.mkdir(exist_ok=True)

    project_name = args.project_name or project_root.name
    memory = build_memory(project_name, args.project_type)
    profile = build_profile(args.project_type)

    memory_path = memory_dir / "memory.json"
    profile_path = memory_dir / "profile.json"
    overview_path = memory_dir / "overview.html"
    inbox_path = memory_dir / "inbox.json"
    index_path = memory_dir / "INDEX.md"

    memory_path.write_text(json.dumps(memory, indent=2) + "\n", encoding="utf-8")
    profile_path.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    inbox_path.write_text(json.dumps({"captures": []}, indent=2) + "\n", encoding="utf-8")
    overview_path.write_text(render_html(memory, profile), encoding="utf-8")
    index_path.write_text(render_index(memory, profile), encoding="utf-8")
    if not args.skip_agents_rules:
        inject_agents_rules(project_root)

    print(f"Initialized project memory at {memory_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
