from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from coordination_model import (  # noqa: E402
    CoordinationConflict,
    coordination_root,
    create_claim,
    load_registry,
    mutate_registry,
    open_coordination,
    pause_agent,
    public_snapshot,
    prune_registry,
    register_agent,
    release_claim,
    resolve_coordination,
    respond_coordination,
    resume_agent,
    slugify,
    update_agent,
)


def run_git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


class AgentCoordinationTests(unittest.TestCase):
    def test_git_worktrees_share_one_coordination_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            worktree = Path(temp) / "worker"
            root.mkdir()
            run_git("init", cwd=root)
            run_git("config", "user.email", "test@example.com", cwd=root)
            run_git("config", "user.name", "Test User", cwd=root)
            (root / "README.md").write_text("test\n", encoding="utf-8")
            run_git("add", "README.md", cwd=root)
            run_git("commit", "-m", "init", cwd=root)
            run_git("worktree", "add", "-b", "worker", str(worktree), cwd=root)

            self.assertEqual(coordination_root(root), coordination_root(worktree))

    def test_concurrent_agent_registration_keeps_every_agent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            project.mkdir()
            codex_home = Path(temp) / "codex-home"

            def join(index: int) -> None:
                mutate_registry(
                    project,
                    lambda registry: register_agent(
                        registry,
                        agent_id=f"agent-{index}",
                        label=f"Agent {index}",
                        task=f"Task {index}",
                        scopes=[f"scope/{index}"],
                    ),
                    codex_home=codex_home,
                )

            with ThreadPoolExecutor(max_workers=6) as executor:
                list(executor.map(join, range(12)))

            registry = load_registry(project, codex_home=codex_home)
            self.assertEqual(12, len(registry["agents"]))
            self.assertEqual(12, registry["revision"])

    def test_pause_yields_claim_and_resume_rechecks_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            project.mkdir()
            codex_home = Path(temp) / "codex-home"

            def setup(registry: dict) -> None:
                register_agent(registry, "agent-a", "Agent A", task="Integrator")
                register_agent(registry, "agent-b", "Agent B", task="Frontend")
                create_claim(registry, "agent-b", "ui", ["web/src"], "Frontend work")
                open_coordination(
                    registry,
                    kind="conflict",
                    owner_agent_id="agent-a",
                    participants=["agent-a", "agent-b"],
                    topic="Resolve overlapping UI changes",
                    surfaces=["web/src"],
                )

            mutate_registry(project, setup, codex_home=codex_home)
            registry = load_registry(project, codex_home=codex_home)
            coordination_id = registry["coordinations"][0]["id"]

            mutate_registry(
                project,
                lambda value: pause_agent(value, "agent-b", coordination_id, "Yield UI scope"),
                codex_home=codex_home,
            )
            mutate_registry(
                project,
                lambda value: create_claim(value, "agent-a", "ui", ["web/src"], "Conflict repair"),
                codex_home=codex_home,
            )

            with self.assertRaises(CoordinationConflict):
                mutate_registry(
                    project,
                    lambda value: resume_agent(value, "agent-b", coordination_id),
                    codex_home=codex_home,
                )

            registry = load_registry(project, codex_home=codex_home)
            active_claim = next(item for item in registry["claims"] if item["agentId"] == "agent-a")
            mutate_registry(
                project,
                lambda value: release_claim(value, active_claim["id"], "completed"),
                codex_home=codex_home,
            )
            mutate_registry(
                project,
                lambda value: resume_agent(value, "agent-b", coordination_id),
                codex_home=codex_home,
            )

            registry = load_registry(project, codex_home=codex_home)
            agent_b = next(item for item in registry["agents"] if item["id"] == "agent-b")
            claim_b = next(item for item in registry["claims"] if item["agentId"] == "agent-b")
            self.assertEqual("active", agent_b["state"])
            self.assertEqual("active", claim_b["status"])

    def test_join_or_update_cannot_bypass_paused_resume_check(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(registry, "agent-a", "Agent A")
        coordination = open_coordination(
            registry,
            kind="conflict",
            owner_agent_id="agent-a",
            participants=["agent-a"],
            topic="Pause for shared scope",
        )
        pause_agent(registry, "agent-a", coordination["id"], "Wait for integration")

        refreshed = register_agent(registry, "agent-a", "Agent A", task="Same task")
        self.assertEqual("paused", refreshed["state"])
        with self.assertRaises(CoordinationConflict):
            register_agent(registry, "agent-a", "Agent A", state="active")
        with self.assertRaises(CoordinationConflict):
            update_agent(registry, "agent-a", state="active")

    def test_reclaim_by_same_agent_is_idempotent(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(registry, "agent-a", "Agent A")
        first = create_claim(registry, "agent-a", "api", ["core/api"], "Build API")
        second = create_claim(registry, "agent-a", "api", ["core/api"], "Build API")

        self.assertEqual(first["id"], second["id"])
        self.assertEqual(1, len(registry["claims"]))

    def test_expired_claim_does_not_block_new_owner(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(registry, "agent-a", "Agent A")
        register_agent(registry, "agent-b", "Agent B")
        expired = create_claim(registry, "agent-a", "api", ["core/api"], "Old API work")
        expired["expiresAt"] = (
            datetime.now(timezone.utc) - timedelta(minutes=1)
        ).replace(microsecond=0).isoformat().replace("+00:00", "Z")

        current = create_claim(registry, "agent-b", "api", ["core/api"], "Current API work")

        self.assertEqual("agent-b", current["agentId"])
        self.assertEqual("expired", expired["status"])

    def test_repository_scope_blocks_every_nested_scope(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(registry, "agent-a", "Agent A")
        register_agent(registry, "agent-b", "Agent B")
        create_claim(registry, "agent-a", "whole-project", ["repo"], "Repository migration")

        with self.assertRaises(CoordinationConflict):
            create_claim(registry, "agent-b", "ui", ["web/src"], "Frontend work")

    def test_non_ascii_labels_get_stable_distinct_ids(self) -> None:
        self.assertEqual(slugify("前端 Agent"), slugify("前端 Agent"))
        self.assertNotEqual(slugify("前端"), slugify("后端"))

    def test_prune_removes_closed_claim_history(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(registry, "agent-a", "Agent A")
        closed = create_claim(registry, "agent-a", "api", ["core/api"], "Finished API")
        release_claim(registry, closed["id"], "completed")

        prune_registry(registry)

        self.assertEqual([], registry["claims"])

    def test_discussion_keeps_positions_and_one_decision(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(registry, "agent-a", "Agent A")
        register_agent(registry, "agent-b", "Agent B")
        coordination = open_coordination(
            registry,
            kind="discussion",
            owner_agent_id="agent-a",
            participants=["agent-a", "agent-b"],
            topic="Fast merge order",
            surfaces=["core", "web"],
        )
        respond_coordination(
            registry,
            coordination["id"],
            "agent-b",
            "position",
            "Merge shared contract before UI",
            ["UI depends on the contract"],
        )
        resolve_coordination(
            registry,
            coordination["id"],
            "agent-a",
            "Merge core first, then UI",
            "Dependency order accepted",
        )

        self.assertEqual("resolved", coordination["state"])
        self.assertEqual(1, len(coordination["responses"]))
        self.assertEqual("Merge core first, then UI", coordination["decision"])

    def test_only_participants_respond_and_only_owner_resolves(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(registry, "agent-a", "Agent A")
        register_agent(registry, "agent-b", "Agent B")
        register_agent(registry, "agent-c", "Agent C")
        coordination = open_coordination(
            registry,
            kind="discussion",
            owner_agent_id="agent-a",
            participants=["agent-a", "agent-b"],
            topic="Choose merge order",
        )

        with self.assertRaises(CoordinationConflict):
            respond_coordination(registry, coordination["id"], "agent-c", "position", "Uninvited", [])
        with self.assertRaises(CoordinationConflict):
            resolve_coordination(registry, coordination["id"], "agent-b", "Decision", "Not owner")

    def test_legacy_claims_migrate_without_deleting_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            memory_dir = project / ".docs" / "project-memory"
            memory_dir.mkdir(parents=True)
            legacy_path = memory_dir / "agent-claims.json"
            legacy_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "claims": [
                            {
                                "id": "claim-old",
                                "laneId": "api",
                                "agent": "legacy-agent",
                                "task": "Legacy task",
                                "status": "active",
                                "scopes": ["core/api"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            registry = load_registry(project, codex_home=Path(temp) / "codex-home")

            self.assertEqual("claim-old", registry["claims"][0]["id"])
            self.assertEqual("legacy-agent", registry["agents"][0]["label"])
            self.assertTrue(legacy_path.exists())
            self.assertIn("agent-claims.json", registry["migration"]["source"])

    def test_public_snapshot_redacts_thread_and_absolute_worktree(self) -> None:
        registry: dict = {"agents": [], "claims": [], "coordinations": [], "recentEvents": []}
        register_agent(
            registry,
            "agent-a",
            "Agent A",
            thread_id="thread-secret",
            worktree="C:/secret/worktree",
            task="Visible task",
        )

        snapshot = public_snapshot(registry)
        encoded = json.dumps(snapshot)
        self.assertNotIn("thread-secret", encoded)
        self.assertNotIn("C:/secret/worktree", encoded)
        self.assertIn("Visible task", encoded)

    def test_resolved_coordination_syncs_decision_and_redacted_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            codex_home = Path(temp) / "codex-home"
            project.mkdir()
            environment = dict(os.environ)
            environment["CODEX_HOME"] = str(codex_home)
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "init_project_memory.py"),
                    str(project),
                    "--project-type",
                    "general",
                    "--dashboard-preset",
                    "default",
                    "--skip-agents-rules",
                ],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )

            def setup(registry: dict) -> str:
                register_agent(
                    registry,
                    "agent-a",
                    "Agent A",
                    thread_id="thread-secret",
                    worktree="C:/secret/worktree",
                    task="Integrate branches",
                    stage="merging",
                )
                coordination = open_coordination(
                    registry,
                    kind="merge",
                    owner_agent_id="agent-a",
                    participants=["agent-a"],
                    topic="Merge API before UI",
                    surfaces=["core/api", "web/src"],
                    target_branch="main",
                )
                resolve_coordination(
                    registry,
                    coordination["id"],
                    "agent-a",
                    "Merge API first, then UI",
                    "UI consumes the new contract",
                )
                return coordination["id"]

            coordination_id = mutate_registry(project, setup, codex_home=codex_home)
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "sync_project_memory.py"),
                    str(project),
                    "--lane",
                    "integration",
                    "--coordination-id",
                    coordination_id,
                ],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )

            lane = json.loads(
                (project / ".docs" / "project-memory" / "lanes" / "integration.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(coordination_id, lane["decisions"][0]["coordinationId"])
            dashboard = (project / ".docs" / "project-memory" / "overview.html").read_text(encoding="utf-8")
            index = (project / ".docs" / "project-memory" / "INDEX.md").read_text(encoding="utf-8")
            self.assertIn("Active Agents", dashboard)
            self.assertIn("Agent A", dashboard)
            self.assertIn("Active agents: 1", index)
            self.assertNotIn("thread-secret", dashboard)
            self.assertNotIn("C:/secret/worktree", dashboard)


if __name__ == "__main__":
    unittest.main()
