from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from memory_model import project_memory_dir, slugify_lane, utc_now


ACTIVE_STATUSES = {"ready", "active"}
FINAL_STATUSES = {"released", "completed", "blocked", "expired"}
REGISTRY_NAME = "agent-claims.json"
LOCK_NAME = ".agent-claims.lock"


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def registry_path(project_root: Path) -> Path:
    return project_memory_dir(project_root) / REGISTRY_NAME


def lock_path(project_root: Path) -> Path:
    return project_memory_dir(project_root) / LOCK_NAME


def require_memory_dir(project_root: Path) -> Path:
    memory_dir = project_memory_dir(project_root)
    if not memory_dir.exists():
        raise SystemExit(
            f"Project memory not found at {memory_dir}. Run init_project_memory.py before using the work guard."
        )
    return memory_dir


def load_registry(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "updatedAt": utc_now(), "claims": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("version", 1)
    data.setdefault("updatedAt", utc_now())
    data.setdefault("claims", [])
    return data


def write_registry(path: Path, data: dict) -> None:
    data["updatedAt"] = utc_now()
    tmp_path = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp_path, path)


class RegistryLock:
    def __init__(self, path: Path, timeout_seconds: float = 8.0, stale_seconds: float = 120.0) -> None:
        self.path = path
        self.timeout_seconds = timeout_seconds
        self.stale_seconds = stale_seconds
        self.acquired = False

    def __enter__(self) -> "RegistryLock":
        deadline = time.time() + self.timeout_seconds
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(json.dumps({"createdAt": utc_now(), "pid": os.getpid()}))
                self.acquired = True
                return self
            except FileExistsError:
                if self._is_stale():
                    try:
                        self.path.unlink()
                        continue
                    except OSError:
                        pass
                if time.time() >= deadline:
                    raise SystemExit(f"Could not acquire registry lock at {self.path}")
                time.sleep(0.2)

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.acquired:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass

    def _is_stale(self) -> bool:
        try:
            return time.time() - self.path.stat().st_mtime > self.stale_seconds
        except FileNotFoundError:
            return False


def normalize_scope(value: str) -> str:
    normalized = value.strip().replace("\\", "/").strip("/")
    return normalized.lower() or "."


def normalize_scopes(scopes: list[str] | None) -> list[str]:
    values = [normalize_scope(scope) for scope in (scopes or []) if scope.strip()]
    return sorted(set(values))


def is_repository_scope(scope: str) -> bool:
    return scope in {"*", ".", "repo", "repository", "project", "project-root"}


def scope_overlaps(left: str, right: str) -> bool:
    left = normalize_scope(left)
    right = normalize_scope(right)
    if is_repository_scope(left) or is_repository_scope(right):
        return True
    if left == right:
        return True
    return left.startswith(f"{right}/") or right.startswith(f"{left}/")


def claim_is_expired(claim: dict, now: datetime | None = None) -> bool:
    status = claim.get("status")
    if status not in ACTIVE_STATUSES:
        return False
    expires_at = parse_utc(claim.get("expiresAt"))
    if expires_at is None:
        return False
    return expires_at <= (now or datetime.now(timezone.utc))


def mark_expired_claims(registry: dict) -> int:
    now = datetime.now(timezone.utc)
    changed = 0
    for claim in registry.get("claims", []):
        if claim_is_expired(claim, now):
            claim["status"] = "expired"
            claim["updatedAt"] = utc_now()
            changed += 1
    return changed


def active_claims(registry: dict, include_expired: bool = False) -> list[dict]:
    claims = []
    for claim in registry.get("claims", []):
        expired = claim_is_expired(claim)
        if claim.get("status") in ACTIVE_STATUSES and (include_expired or not expired):
            claims.append(claim)
    claims.sort(key=lambda item: item.get("updatedAt", ""), reverse=True)
    return claims


def format_claim(claim: dict) -> str:
    scopes = ", ".join(claim.get("scopes", [])) or "-"
    return (
        f"{claim.get('id')} [{claim.get('status')}] lane={claim.get('laneId', '-')}"
        f" agent={claim.get('agent', '-')} expires={claim.get('expiresAt', '-')}"
        f" scopes={scopes} task={claim.get('task', '-')}"
    )


def find_conflicts(
    registry: dict,
    lane_id: str | None,
    scopes: list[str],
    ignore_claim_id: str | None = None,
) -> list[dict]:
    conflicts = []
    for claim in active_claims(registry):
        if ignore_claim_id and claim.get("id") == ignore_claim_id:
            continue
        reasons = []
        claim_lane = claim.get("laneId")
        if lane_id and claim_lane and claim_lane == lane_id:
            reasons.append("same lane")
        claim_scopes = normalize_scopes(claim.get("scopes", []))
        for requested_scope in scopes:
            for claim_scope in claim_scopes:
                if scope_overlaps(requested_scope, claim_scope):
                    reasons.append(f"scope overlap: {requested_scope} <-> {claim_scope}")
                    break
            if reasons and reasons[-1].startswith("scope overlap:"):
                break
        if reasons:
            conflicts.append({"claim": claim, "reasons": reasons})
    return conflicts


def print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def build_claim(args: argparse.Namespace, lane_id: str, scopes: list[str]) -> dict:
    now = datetime.now(timezone.utc)
    ttl_minutes = max(1, args.ttl_minutes)
    expires_at = now + timedelta(minutes=ttl_minutes)
    return {
        "id": f"claim-{uuid4().hex[:12]}",
        "laneId": lane_id,
        "agent": args.agent,
        "task": args.task,
        "status": args.status,
        "scopes": scopes,
        "createdAt": utc_now(),
        "updatedAt": utc_now(),
        "expiresAt": expires_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "notes": args.note or "",
    }


def command_status(project_root: Path, args: argparse.Namespace) -> int:
    memory_dir = require_memory_dir(project_root)
    path = registry_path(project_root)
    registry = load_registry(path)
    claims = active_claims(registry, include_expired=args.include_expired)
    payload = {
        "memoryDir": str(memory_dir),
        "registry": str(path),
        "activeCount": len([claim for claim in claims if not claim_is_expired(claim)]),
        "claims": claims,
    }
    if args.json:
        print_json(payload)
        return 0

    print(f"Project memory: {memory_dir}")
    print(f"Registry: {path}")
    if not claims:
        print("No active or ready claims.")
        return 0
    print(f"Active/ready claims: {len(claims)}")
    for claim in claims:
        print(f"- {format_claim(claim)}")
    return 0


def command_check(project_root: Path, args: argparse.Namespace) -> int:
    require_memory_dir(project_root)
    lane_id = slugify_lane(args.lane) if args.lane else None
    scopes = normalize_scopes(args.scope)
    path = registry_path(project_root)
    registry = load_registry(path)
    conflicts = find_conflicts(registry, lane_id, scopes)
    payload = {
        "ok": not conflicts,
        "laneId": lane_id,
        "scopes": scopes,
        "conflicts": conflicts,
    }
    if args.json:
        print_json(payload)
    elif conflicts:
        print("Blocked: active or ready claim overlaps requested work.")
        for item in conflicts:
            print(f"- {format_claim(item['claim'])} ({'; '.join(item['reasons'])})")
    else:
        print("No overlapping active or ready claims.")
    return 1 if conflicts else 0


def command_claim(project_root: Path, args: argparse.Namespace) -> int:
    require_memory_dir(project_root)
    lane_id = slugify_lane(args.lane)
    scopes = normalize_scopes(args.scope) or [lane_id]
    path = registry_path(project_root)
    with RegistryLock(lock_path(project_root)):
        registry = load_registry(path)
        expired_count = mark_expired_claims(registry)
        conflicts = find_conflicts(registry, lane_id, scopes)
        if conflicts and not args.force:
            if expired_count:
                write_registry(path, registry)
            payload = {"ok": False, "laneId": lane_id, "scopes": scopes, "conflicts": conflicts}
            if args.json:
                print_json(payload)
            else:
                print("Blocked: active or ready claim overlaps requested work.")
                for item in conflicts:
                    print(f"- {format_claim(item['claim'])} ({'; '.join(item['reasons'])})")
                print("Release the stale claim or rerun with --force after verifying it is safe.")
            return 1

        claim = build_claim(args, lane_id, scopes)
        registry.setdefault("claims", []).insert(0, claim)
        write_registry(path, registry)

    if args.json:
        print_json({"ok": True, "claim": claim, "forced": bool(args.force)})
    else:
        print(f"Created {claim['id']} [{claim['status']}] for lane {lane_id}; expires {claim['expiresAt']}.")
    return 0


def command_activate(project_root: Path, args: argparse.Namespace) -> int:
    require_memory_dir(project_root)
    path = registry_path(project_root)
    with RegistryLock(lock_path(project_root)):
        registry = load_registry(path)
        mark_expired_claims(registry)
        claim = next((item for item in registry.get("claims", []) if item.get("id") == args.claim_id), None)
        if claim is None:
            raise SystemExit(f"Claim not found: {args.claim_id}")
        conflicts = find_conflicts(
            registry,
            claim.get("laneId"),
            normalize_scopes(claim.get("scopes", [])),
            ignore_claim_id=args.claim_id,
        )
        if conflicts and not args.force:
            if args.json:
                print_json({"ok": False, "claim": claim, "conflicts": conflicts})
            else:
                print("Blocked: activating this claim would overlap active work.")
                for item in conflicts:
                    print(f"- {format_claim(item['claim'])} ({'; '.join(item['reasons'])})")
            return 1
        claim["status"] = "active"
        claim["updatedAt"] = utc_now()
        write_registry(path, registry)
    if args.json:
        print_json({"ok": True, "claim": claim})
    else:
        print(f"Activated {args.claim_id}.")
    return 0


def command_release(project_root: Path, args: argparse.Namespace) -> int:
    require_memory_dir(project_root)
    path = registry_path(project_root)
    with RegistryLock(lock_path(project_root)):
        registry = load_registry(path)
        claim = next((item for item in registry.get("claims", []) if item.get("id") == args.claim_id), None)
        if claim is None:
            raise SystemExit(f"Claim not found: {args.claim_id}")
        claim["status"] = args.status
        claim["updatedAt"] = utc_now()
        if args.reason:
            claim["releaseReason"] = args.reason
        write_registry(path, registry)
    if args.json:
        print_json({"ok": True, "claim": claim})
    else:
        print(f"Marked {args.claim_id} as {args.status}.")
    return 0


def command_prune(project_root: Path, args: argparse.Namespace) -> int:
    require_memory_dir(project_root)
    path = registry_path(project_root)
    with RegistryLock(lock_path(project_root)):
        registry = load_registry(path)
        before = len(registry.get("claims", []))
        mark_expired_claims(registry)
        keep_statuses = ACTIVE_STATUSES | {"blocked"}
        registry["claims"] = [claim for claim in registry.get("claims", []) if claim.get("status") in keep_statuses]
        after = len(registry.get("claims", []))
        write_registry(path, registry)
    removed = before - after
    if args.json:
        print_json({"ok": True, "removed": removed, "remaining": after})
    else:
        print(f"Pruned {removed} inactive claims; {after} claims remain.")
    return 0


def add_target_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--lane", help="Stable lane or responsibility id, such as backend-auth.")
    parser.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Optional file/module scope. Repeat for multiple scopes. Use repo for repository-wide work.",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Guard project-memory lane work with lightweight agent claims.")
    parser.add_argument("project_root", help="Path to the target project root.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Show active and ready work claims.")
    status.add_argument("--include-expired", action="store_true", help="Include active claims that are past expiry.")
    status.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    check = subparsers.add_parser("check", help="Check whether requested work overlaps an active claim.")
    add_target_args(check)
    check.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    claim = subparsers.add_parser("claim", help="Create a ready or active work claim if no overlap exists.")
    add_target_args(claim)
    claim.add_argument("--agent", default="codex-session", help="Agent/session label.")
    claim.add_argument("--task", required=True, help="Short description of the intended work.")
    claim.add_argument("--status", default="active", choices=sorted(ACTIVE_STATUSES), help="Initial claim status.")
    claim.add_argument("--ttl-minutes", type=int, default=240, help="Minutes before the claim is considered stale.")
    claim.add_argument("--note", default="", help="Optional extra note.")
    claim.add_argument("--force", action="store_true", help="Create the claim despite conflicts after manual review.")
    claim.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    activate = subparsers.add_parser("activate", help="Promote a ready claim to active.")
    activate.add_argument("--claim-id", required=True, help="Claim id to activate.")
    activate.add_argument("--force", action="store_true", help="Activate despite conflicts after manual review.")
    activate.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    release = subparsers.add_parser("release", help="Release or close a claim.")
    release.add_argument("--claim-id", required=True, help="Claim id to release.")
    release.add_argument("--status", default="released", choices=sorted(FINAL_STATUSES - {"expired"}), help="Final status.")
    release.add_argument("--reason", default="", help="Optional release reason.")
    release.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    prune = subparsers.add_parser("prune", help="Remove inactive released/completed/expired claims.")
    prune.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    commands = {
        "status": command_status,
        "check": command_check,
        "claim": command_claim,
        "activate": command_activate,
        "release": command_release,
        "prune": command_prune,
    }
    return commands[args.command](project_root, args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)
