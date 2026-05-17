from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path


SECTION_TITLES = {
    "summary": "Current Status",
    "progress": "Progress",
    "modules": "Modules",
    "decisions": "Key Decisions",
    "issues": "Issues",
    "todos": "Next Actions",
    "techNotes": "Technical Notes",
    "recentUpdates": "Recent Updates",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_index(memory: dict, profile: dict) -> str:
    project = memory.get("project", {})
    summary = memory.get("summary", {})
    modules = len(memory.get("modules", []))
    open_issues = len([item for item in memory.get("issues", []) if item.get("status") != "resolved"])
    decisions = len(memory.get("decisions", []))
    todos = len([item for item in memory.get("todos", []) if item.get("status") != "done"])
    updates = len(memory.get("recentUpdates", []))
    return f"""# Project Memory Index

## Overview

- Project: {project.get("name", "Unknown")}
- Type: {project.get("type", profile.get("projectType", "general"))}
- Last updated: {summary.get("lastUpdated", "Unknown")}

## Files

- [overview.html](./overview.html)
- [memory.json](./memory.json)
- [profile.json](./profile.json)
- [inbox.json](./inbox.json)
- [archive/](./archive/)

## Active Counts

| Section | Count |
|---|---:|
| Modules | {modules} |
| Open issues | {open_issues} |
| Decisions | {decisions} |
| Open todos | {todos} |
| Recent updates | {updates} |

## Focus

- Current phase: {summary.get("currentPhase", "Unknown")}
- Current focus: {summary.get("focus", "Unknown")}
- Health: {summary.get("health", "unknown")}
"""


def label_for(section: str, profile: dict) -> str:
    return profile.get("labels", {}).get(section, SECTION_TITLES.get(section, section))


def html_page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f172a;
      --panel: #111827;
      --panel-2: #1f2937;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --accent: #38bdf8;
      --good: #22c55e;
      --warn: #f59e0b;
      --bad: #ef4444;
      --border: #334155;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", Arial, sans-serif;
      background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
      color: var(--text);
    }}
    .page {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }}
    .hero {{
      display: grid;
      gap: 16px;
      padding: 24px;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 24px;
    }}
    .hero h1 {{
      margin: 0;
      font-size: 32px;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      color: var(--muted);
      font-size: 14px;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .chip {{
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.28);
      color: #bae6fd;
      font-size: 13px;
    }}
    .grid {{
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }}
    section {{
      background: rgba(17, 24, 39, 0.88);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px;
    }}
    section h2 {{
      margin: 0 0 14px 0;
      font-size: 18px;
    }}
    .muted {{
      color: var(--muted);
    }}
    .status {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 12px;
      border: 1px solid var(--border);
      background: rgba(148, 163, 184, 0.12);
    }}
    .status.green {{ color: #86efac; border-color: rgba(34, 197, 94, 0.4); }}
    .status.yellow {{ color: #fcd34d; border-color: rgba(245, 158, 11, 0.4); }}
    .status.red {{ color: #fca5a5; border-color: rgba(239, 68, 68, 0.4); }}
    .list {{
      display: grid;
      gap: 12px;
    }}
    .item {{
      padding: 12px;
      border-radius: 8px;
      background: rgba(31, 41, 55, 0.7);
      border: 1px solid rgba(51, 65, 85, 0.9);
    }}
    .item h3 {{
      margin: 0 0 8px 0;
      font-size: 15px;
    }}
    .item p {{
      margin: 0;
      line-height: 1.5;
    }}
    .kv {{
      display: grid;
      gap: 10px;
    }}
    .kv div {{
      display: grid;
      gap: 4px;
    }}
    .kv strong {{
      font-size: 13px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .progress-bar {{
      height: 10px;
      border-radius: 999px;
      overflow: hidden;
      background: rgba(51, 65, 85, 0.9);
      margin-top: 8px;
    }}
    .progress-bar span {{
      display: block;
      height: 100%;
      background: linear-gradient(90deg, #22d3ee 0%, #3b82f6 100%);
    }}
    .footer {{
      margin-top: 24px;
      color: var(--muted);
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <main class="page">
    {body}
  </main>
</body>
</html>
"""


def render_summary(memory: dict) -> str:
    summary = memory.get("summary", {})
    phase = escape(summary.get("currentPhase", "Unknown"))
    focus = escape(summary.get("focus", ""))
    health = escape(summary.get("health", "unknown"))
    updated = escape(summary.get("lastUpdated", ""))
    return f"""
    <section>
      <h2>Current Status</h2>
      <div class="kv">
        <div><strong>Phase</strong><span>{phase}</span></div>
        <div><strong>Focus</strong><span>{focus}</span></div>
        <div><strong>Health</strong><span class="status {health}">{health}</span></div>
        <div><strong>Last Updated</strong><span>{updated}</span></div>
      </div>
    </section>
    """


def render_progress(memory: dict) -> str:
    progress = memory.get("progress", {})
    percent = int(progress.get("percent", 0))
    status = escape(progress.get("status", "Unknown"))
    milestones = progress.get("milestones", [])
    milestone_items = "".join(
        f'<div class="item"><h3>{escape(item.get("title", "Milestone"))}</h3>'
        f'<p>{escape(item.get("status", ""))}'
        + (
            f' <span class="muted">- {escape(item.get("note", ""))}</span></p></div>'
            if item.get("note")
            else "</p></div>"
        )
        for item in milestones
    ) or '<p class="muted">No milestones recorded.</p>'
    return f"""
    <section>
      <h2>Progress</h2>
      <div class="kv">
        <div><strong>Status</strong><span>{status}</span></div>
        <div><strong>Completion</strong><span>{percent}%</span></div>
      </div>
      <div class="progress-bar"><span style="width: {percent}%"></span></div>
      <div class="list" style="margin-top: 14px;">{milestone_items}</div>
    </section>
    """


def render_named_items(items: list[dict], empty_text: str, fields: list[tuple[str, str]]) -> str:
    if not items:
        return f'<p class="muted">{escape(empty_text)}</p>'
    rendered = []
    for item in items:
        title = escape(item.get("title") or item.get("name") or "Untitled")
        details = []
        for key, label in fields:
            value = item.get(key)
            if value:
                details.append(f"<strong>{escape(label)}</strong><span>{escape(str(value))}</span>")
        detail_html = "".join(f"<div>{part}</div>" for part in details)
        related_bits = []
        for key, label in [
            ("relatedModules", "Modules"),
            ("relatedIssues", "Issues"),
            ("relatedDecisions", "Decisions"),
            ("relatedFiles", "Files"),
        ]:
            value = item.get(key)
            if value:
                joined = ", ".join(str(part) for part in value)
                related_bits.append(f"<div><strong>{escape(label)}</strong><span>{escape(joined)}</span></div>")
        related_html = "".join(related_bits)
        rendered.append(f'<div class="item"><h3>{title}</h3><div class="kv">{detail_html}{related_html}</div></div>')
    return "".join(rendered)


def render_section(section: str, memory: dict, profile: dict) -> str:
    title = escape(label_for(section, profile))
    if section == "summary":
        return render_summary(memory)
    if section == "progress":
        return render_progress(memory)
    mapping = {
        "modules": ("No modules recorded.", [("status", "Status"), ("summary", "Summary"), ("notes", "Notes")]),
        "decisions": ("No decisions recorded.", [("context", "Context"), ("decision", "Decision"), ("impact", "Impact")]),
        "issues": ("No issues recorded.", [("status", "Status"), ("severity", "Severity"), ("impact", "Impact"), ("nextStep", "Next Step")]),
        "todos": ("No todos recorded.", [("status", "Status"), ("owner", "Owner"), ("notes", "Notes")]),
        "techNotes": ("No technical notes recorded.", [("body", "Note")]),
        "recentUpdates": ("No updates recorded.", [("timestamp", "Time"), ("details", "Details")]),
    }
    empty_text, fields = mapping[section]
    content = render_named_items(memory.get(section, []), empty_text, fields)
    return f"""
    <section>
      <h2>{title}</h2>
      <div class="list">{content}</div>
    </section>
    """


def render_html(memory: dict, profile: dict) -> str:
    project = memory.get("project", {})
    summary = memory.get("summary", {})
    title = project.get("name", "Project Memory")
    project_type = project.get("type", profile.get("projectType", "general"))
    focus = escape(summary.get("focus", ""))
    hero = f"""
    <header class="hero">
      <div>
        <h1>{escape(title)}</h1>
        <div class="meta">
          <span>Project type: {escape(str(project_type))}</span>
          <span>Memory version: {escape(str(project.get("memoryVersion", 1)))}</span>
        </div>
      </div>
      <div class="chips">
        <span class="chip">Static HTML overview</span>
        <span class="chip">Structured agent memory</span>
        <span class="chip">Current focus: {focus or "Unspecified"}</span>
      </div>
    </header>
    """
    sections = profile.get("sections", list(SECTION_TITLES))
    body_sections = "".join(render_section(section, memory, profile) for section in sections if section in SECTION_TITLES)
    footer = """
    <div class="footer">
      Generated from .docs/project-memory/memory.json and profile.json.
    </div>
    """
    return html_page(title, hero + f'<div class="grid">{body_sections}</div>' + footer)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the static overview HTML for a project memory dashboard.")
    parser.add_argument("project_root", help="Path to the target project root.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    memory_dir = project_root / ".docs" / "project-memory"
    memory = load_json(memory_dir / "memory.json")
    profile = load_json(memory_dir / "profile.json")
    output = render_html(memory, profile)
    (memory_dir / "overview.html").write_text(output, encoding="utf-8")
    (memory_dir / "INDEX.md").write_text(render_index(memory, profile), encoding="utf-8")
    print(f"Rendered {memory_dir / 'overview.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
