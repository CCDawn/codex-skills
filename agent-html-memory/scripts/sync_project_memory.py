from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from render_overview import load_json, render_html, render_index


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync project memory after meaningful development work.")
    parser.add_argument("project_root", help="Path to the target project root.")
    parser.add_argument("--focus", default=None, help="Optional current focus to store in summary.focus.")
    parser.add_argument("--phase", default=None, help="Optional current phase to store in summary.currentPhase.")
    parser.add_argument("--health", default=None, choices=["green", "yellow", "red"], help="Optional summary health.")
    parser.add_argument("--update", default=None, help="Short recent update summary for this task.")
    parser.add_argument("--capture-title", default=None, help="Optional inbox capture title to promote.")
    parser.add_argument("--promote-captures", action="store_true", help="Promote all inbox captures into recent updates and clear inbox.")
    return parser.parse_args()


def promote_capture_to_update(capture: dict) -> dict:
    timestamp = capture.get("timestamp") or utc_now()
    title = capture.get("title") or "Promoted inbox capture"
    details = capture.get("details") or capture.get("body") or ""
    promoted = {
        "timestamp": timestamp,
        "title": title,
        "details": details,
    }
    for key in ("relatedModules", "relatedIssues", "relatedDecisions", "relatedFiles"):
        if capture.get(key):
            promoted[key] = capture[key]
    return promoted


def sync_memory(project_root: Path, args: argparse.Namespace) -> None:
    memory_dir = project_root / ".docs" / "project-memory"
    memory_path = memory_dir / "memory.json"
    profile_path = memory_dir / "profile.json"
    inbox_path = memory_dir / "inbox.json"
    overview_path = memory_dir / "overview.html"
    index_path = memory_dir / "INDEX.md"

    memory = load_json(memory_path)
    profile = load_json(profile_path)
    inbox = load_json(inbox_path) if inbox_path.exists() else {"captures": []}

    summary = memory.setdefault("summary", {})
    now = utc_now()
    summary["lastUpdated"] = now
    if args.focus:
        summary["focus"] = args.focus
    if args.phase:
        summary["currentPhase"] = args.phase
    if args.health:
        summary["health"] = args.health

    recent_updates = memory.setdefault("recentUpdates", [])
    if args.update:
        recent_updates.insert(
            0,
            {
                "timestamp": now,
                "title": args.update,
                "details": args.update,
            },
        )

    captures = inbox.get("captures", [])
    remaining_captures = []
    for capture in captures:
        should_promote = args.promote_captures or (
            args.capture_title is not None and capture.get("title") == args.capture_title
        )
        if should_promote:
            recent_updates.insert(0, promote_capture_to_update(capture))
        else:
            remaining_captures.append(capture)

    inbox["captures"] = remaining_captures

    overview_path.write_text(render_html(memory, profile), encoding="utf-8")
    index_path.write_text(render_index(memory, profile), encoding="utf-8")
    write_json(memory_path, memory)
    write_json(inbox_path, inbox)


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    sync_memory(project_root, args)
    print(f"Synced project memory at {project_root / '.docs' / 'project-memory'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
