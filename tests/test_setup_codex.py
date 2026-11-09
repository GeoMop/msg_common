"""Offline setup checks; all copies stay in temporary directories."""

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import shlex
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "setup_codex", Path(__file__).parents[1] / "scripts/setup_codex.py"
)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repository = Path(self.temporary.name) / "repository"
        self.home = Path(self.temporary.name) / "codex"
        self.agent = self.repository / "skills/review/agent-definitions/reviewer.toml"
        self.put(self.agent, 'name = "reviewer"\r\n')
        self.put(self.repository / "skills/review/agents/openai.yaml", "interface: {}\n")
        self.put(
            self.repository / "config/github/README.md",
            "GitHub setup instructions; no machine-readable configuration here.",
        )
        self.put(self.repository / "config/another/README.md", "Another MCP guide")
        template = Path(__file__).parents[1] / "config/github/github-review.toml"
        self.put(self.repository / "config/github/github-review.toml", template.read_text())

    def put(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode())

    def run_setup(self, token="fake-setup-token"):
        with patch.object(setup, "__file__", str(self.repository / "scripts/setup_codex.py")):
            with patch.dict("os.environ", {"CODEX_HOME": str(self.home)}):
                with patch("builtins.input", return_value=token), patch.object(setup.subprocess, "run") as run, redirect_stdout(io.StringIO()) as output:
                    run.return_value = setup.subprocess.CompletedProcess([], 0)
                    setup.main()
                    self.assertEqual(run.call_count, 2 if token else 1)
                    if token:
                        run.assert_any_call(
                            [setup.sys.executable, str(self.repository / "config/github/credentials.py"),
                             "store", str(self.home / "github-credentials")],
                            input=token, text=True, check=True,
                        )
                    run.assert_any_call(
                        [setup.sys.executable, str(self.repository / "config/github/check_access.py"),
                         str(self.home / "github-credentials")],
                    )
        return output.getvalue()

    def test_default_copies_all_agents_and_shows_all_mcps(self):
        self.put(self.repository / "skills/writer/agent-definitions/writer.toml", 'name = "writer"\n')
        self.put(self.repository / "skills/review/agents/metadata.toml", "metadata only")
        output = self.run_setup()
        self.assertEqual(
            sorted(path.name for path in (self.home / "agents").iterdir()),
            ["reviewer.toml", "writer.toml"],
        )
        self.assertEqual((self.home / "agents/reviewer.toml").read_bytes(), self.agent.read_bytes())
        self.assertIn("MCP github", output)
        self.assertIn("MCP another", output)
        self.assertIn("expires_in=365", output)
        config = (self.home / "config.toml").read_text()
        self.assertIn("http_headers_helper", config)
        self.assertIn(str(self.repository / "config/github/credentials.py"), config)
        self.assertNotIn("/absolute/path/to/", config)

    def test_empty_prompt_reuses_token_without_storing(self):
        output = self.run_setup(token="")
        self.assertIn("Using the saved GitHub token", output)

    def test_rerun_replaces_team_agents_and_keeps_other_files(self):
        self.run_setup()
        self.put(self.agent, 'name = "reviewer"\nmodel = "new"\n')
        self.put(self.home / "agents/personal.toml", 'name = "personal"\n')
        personal = 'model = "personal-model"\n# Private settings left untouched\n'
        self.put(self.home / "config.toml", personal)
        output = self.run_setup()
        self.assertEqual((self.home / "agents/reviewer.toml").read_bytes(), self.agent.read_bytes())
        self.assertTrue((self.home / "agents/personal.toml").exists())
        self.assertTrue((self.home / "config.toml").read_text().startswith(personal))
        self.assertEqual((self.home / "config.toml.bak").read_text(), personal)
        self.assertNotIn("personal-model", output)

    def test_template_rerun_is_idempotent_and_updates_only_its_block(self):
        self.run_setup()
        config_file = self.home / "config.toml"
        current = config_file.read_text()
        modified = config_file.stat().st_mtime_ns
        self.run_setup()
        self.assertEqual(config_file.stat().st_mtime_ns, modified)
        suffix = '\n[mcp_servers.other]\nurl = "https://example.test/mcp"\n'
        config_file.write_text(current + suffix)
        cmd_escaped = setup.format_command_for_toml(
            ["python", "/path with spaces/credentials.py", "headers", "/private/store"],
        )
        setup.apply_github_template(
            self.repository / "config/github/github-review.toml", config_file, cmd_escaped,
        )
        updated = config_file.read_text()
        self.assertTrue(updated.endswith(suffix))
        self.assertEqual(updated.count("[mcp_servers.github_review]"), 1)
        self.assertEqual(updated.count("# BEGIN MSG GitHub MCP"), 1)
        self.assertIn(f"http_headers_helper = {cmd_escaped}", updated)
        self.assertEqual((self.home / "config.toml.bak").read_text(), current + suffix)

    def test_unmanaged_conflict_and_broken_markers_preserve_config(self):
        config_file = self.home / "config.toml"
        for existing in [
            '[mcp_servers.github_review]\nurl = "https://personal.test"\n',
            '[apps."connector_76869538009648d5b282a4bb21c3d157"]\nenabled = true\n',
            '# BEGIN MSG GitHub MCP\nmissing end\n',
            '# END MSG GitHub MCP\n',
            '# END MSG GitHub MCP\n# BEGIN MSG GitHub MCP\n',
            '# BEGIN MSG GitHub MCP\n# END MSG GitHub MCP\n' * 2,
            '# END MSG GitHub MCP\n# BEGIN MSG GitHub MCP\n# END MSG GitHub MCP\n',
            '# BEGIN MSG GitHub MCP\n# END MSG GitHub MCP\n# BEGIN MSG GitHub MCP\n',
        ]:
            with self.subTest(existing=existing):
                self.put(config_file, existing)
                with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
                    setup.apply_github_template(
                        self.repository / "config/github/github-review.toml", config_file, '"helper"',
                    )
                self.assertEqual(config_file.read_text(), existing)
                self.assertFalse((self.home / "config.toml.bak").exists())

    def test_duplicate_filenames_raise_before_copying(self):
        self.put(self.repository / "skills/another/agent-definitions/reviewer.toml", 'name = "reviewer"\n')
        with self.assertRaisesRegex(AssertionError, "Duplicate"):
            self.run_setup()
        self.assertFalse(self.home.exists())

    def test_conflicts_outside_existing_block_print_proposal_without_writing(self):
        config_file = self.home / "config.toml"
        managed = '# BEGIN MSG GitHub MCP\nold settings\n# END MSG GitHub MCP\n'
        conflicts = [
            '[mcp_servers.github_review.tools]\n',
            '[apps.connector_76869538009648d5b282a4bb21c3d157]\n',
        ]
        for conflict in conflicts:
            for existing in [conflict, conflict + managed, managed + conflict]:
                with self.subTest(existing=existing):
                    self.put(config_file, existing)
                    with redirect_stdout(io.StringIO()) as output:
                        with self.assertRaisesRegex(SystemExit, "reconcile"):
                            setup.apply_github_template(
                                self.repository / "config/github/github-review.toml",
                                config_file, '"proposed helper"',
                            )
                    self.assertIn('# BEGIN MSG GitHub MCP', output.getvalue())
                    self.assertIn('http_headers_helper = "proposed helper"', output.getvalue())
                    self.assertEqual(config_file.read_text(), existing)
                    self.assertFalse((self.home / "config.toml.bak").exists())

    def test_generic_mcp_help_is_independent_of_agents_and_github(self):
        guide = self.repository / "config/another/README.md"
        with redirect_stdout(io.StringIO()) as output:
            setup.setup_mcps([guide], self.home / "config.toml", {"github": setup.setup_github})
        self.assertIn("MCP another", output.getvalue())
        self.assertNotIn("GITHUB_PAT_TOKEN", output.getvalue())
        self.assertFalse(self.home.exists())

    def test_errors_propagate(self):
        with patch.object(setup.shutil, "copy2", side_effect=OSError("copy failed")):
            with self.assertRaisesRegex(OSError, "copy failed"):
                self.run_setup()

    def test_access_check_failure_stops_setup(self):
        failure = setup.subprocess.CompletedProcess(["check_access.py"], 1)
        with patch.object(setup, "__file__", str(self.repository / "scripts/setup_codex.py")):
            with patch.dict("os.environ", {"CODEX_HOME": str(self.home)}):
                with patch("builtins.input", return_value="fake-token"), patch.object(setup.subprocess, "run", side_effect=[None, failure]):
                    with redirect_stdout(io.StringIO()):
                        with self.assertRaises(SystemExit) as stopped:
                            setup.main()
        self.assertEqual(stopped.exception.code, 1)

    def test_posix_command_survives_string_and_shell_decoding(self):
        args = ["/path with spaces/python", "helper's$name`file.py", 'quote"back\\slash']
        with patch.object(setup.os, "name", "posix"):
            cmd_escaped = setup.format_command_for_toml(args)
        self.assertEqual(shlex.split(json.loads(cmd_escaped)), args)

    def test_windows_command_preserves_paths_with_spaces_and_backslashes(self):
        args = [r"C:\Program Files\Python\python.exe", r"C:\MSG\helper.py", "headers",
                r"C:\private folder\store"]
        with patch.object(setup.os, "name", "nt"):
            cmd_escaped = setup.format_command_for_toml(args)
        self.assertEqual(
            json.loads(cmd_escaped),
            r'"C:\Program Files\Python\python.exe" C:\MSG\helper.py headers "C:\private folder\store"',
        )


if __name__ == "__main__":
    unittest.main()
