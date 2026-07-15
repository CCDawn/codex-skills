import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_brt_routing_eval.py"
SPEC = importlib.util.spec_from_file_location("run_brt_routing_eval", SCRIPT_PATH)
ROUTING_EVAL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ROUTING_EVAL)


class RoutingEvalTests(unittest.TestCase):
    def test_parse_events_counts_unique_commands_and_skill_reads(self) -> None:
        stream = "\n".join(
            [
                'warning that is not JSON',
                '{"type":"item.started","item":{"id":"cmd-1","type":"command_execution","command":"Get-Content C:\\\\Users\\\\me\\\\.codex\\\\skills\\\\ccdawn-brt\\\\SKILL.md"}}',
                '{"type":"item.completed","item":{"id":"cmd-1","type":"command_execution","command":"Get-Content C:\\\\Users\\\\me\\\\.codex\\\\skills\\\\ccdawn-brt\\\\SKILL.md"}}',
                '{"type":"item.completed","item":{"id":"msg-1","type":"agent_message","text":"当前理解与建议"}}',
            ]
        )

        events, skill_reads, last_message = ROUTING_EVAL.parse_events(stream)

        self.assertEqual(len(events), 3)
        self.assertEqual(skill_reads, ["ccdawn-brt"])
        self.assertEqual(last_message, "当前理解与建议")

    def test_parse_events_accepts_codex_double_escaped_windows_paths(self) -> None:
        stream = (
            '{"type":"item.started","item":{"id":"cmd-1","type":"command_execution",'
            '"command":"Get-Content C:\\\\\\\\Users\\\\\\\\me\\\\\\\\.codex\\\\\\\\skills'
            '\\\\\\\\ccdawn-project-review\\\\\\\\SKILL.md"}}'
        )

        _, skill_reads, _ = ROUTING_EVAL.parse_events(stream)

        self.assertEqual(skill_reads, ["ccdawn-project-review"])

    def test_find_codex_cli_prefers_explicit_environment_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            executable = Path(temp_dir) / "codex.exe"
            executable.touch()
            with mock.patch.dict(os.environ, {"CODEX_CLI_PATH": str(executable)}):
                self.assertEqual(ROUTING_EVAL.find_codex_cli(), executable)


if __name__ == "__main__":
    unittest.main()
