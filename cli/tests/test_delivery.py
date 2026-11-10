"""Behavioral regression molds for safe adoption and truthful gate evidence."""
import contextlib
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from codex_automata.init import run_init as _run_init

def run_init(*args, **kwargs):
    return _run_init(*args, **kwargs, layout="legacy")

from codex_automata.update import run_update as _run_update

def run_update(*args, **kwargs):
    return _run_update(*args, **kwargs, layout="legacy")

from codex_automata.verify import run_verify

ROOT = Path(__file__).resolve().parents[2]


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def test_every_profile_agent_ships_portable_workflow(self):
        for profile in ('essential', 'standard', 'complete'):
            for agent in ('cursor', 'codex', 'claude', 'copilot', 'generic'):
                with self.subTest(profile=profile, agent=agent):
                    target = self.base / (profile + agent)
                    self.assertEqual(run_init(str(target), profile, agent), 0)
                    for name in ('AGENTS.md', 'agent/LINEAR_FIRST.md', 'agent/MODEL_ROUTING.md',
                                 'templates/linear-issue-template.md',
                                 'templates/linear-project-brief-template.md',
                                 'templates/execution-queue-template.md',
                                 'prompts/plan.md', 'prompts/execute.md',
                                 'prompts/reconcile.md', '.github/workflows/codex-gates.yml'):
                        self.assertTrue((target / name).is_file(), name)
                    self.assertEqual((target / '.cursor').exists(),
                                     agent in ('cursor', 'generic'))

    def test_init_collision_fails_before_any_write(self):
        target = self.base / 'consumer'
        target.mkdir()
        (target / 'AGENTS.md').write_text('custom policy')
        self.assertEqual(run_init(str(target), 'standard', 'cursor'), 1)
        self.assertEqual(list(target.iterdir()), [target / 'AGENTS.md'])
        self.assertEqual((target / 'AGENTS.md').read_text(), 'custom policy')

    def test_unrelated_source_is_preserved(self):
        target = self.base / 'consumer'
        target.mkdir()
        (target / 'application.py').write_text('original')
        self.assertEqual(run_init(str(target), 'essential', 'codex'), 0)
        self.assertEqual((target / 'application.py').read_text(), 'original')

    def test_update_stages_without_touching_customizations(self):
        target = self.base / 'consumer'
        target.mkdir()
        (target / 'AGENTS.md').write_text('custom policy')
        self.assertEqual(run_update(str(target), profile='essential', agent='codex'), 0)
        self.assertEqual((target / 'AGENTS.md').read_text(), 'custom policy')
        stage = self.base / 'consumer-automata-update'
        self.assertTrue((stage / 'agent/LINEAR_FIRST.md').is_file())
        self.assertFalse((stage / '.cursor').exists())
        self.assertEqual(run_update(str(target)), 1)
        self.assertEqual(run_update(str(target), str(target / 'nested')), 1)

    @unittest.skipIf(os.name == 'nt', 'Symlink privileges vary on Windows')
    def test_broken_destination_symlink_is_not_followed(self):
        target = self.base / 'consumer'
        target.mkdir()
        (target / 'AGENTS.md').symlink_to(self.base / 'missing')
        self.assertEqual(run_init(str(target), 'standard', 'cursor'), 1)
        self.assertTrue((target / 'AGENTS.md').is_symlink())
        self.assertFalse((target / 'agent').exists())

    def test_update_cannot_stage_in_an_ancestor(self):
        target = self.base / 'consumer'
        target.mkdir()
        (target / 'AGENTS.md').write_text('custom')
        self.assertEqual(run_update(str(target), str(self.base)), 1)
        self.assertEqual((target / 'AGENTS.md').read_text(), 'custom')

    def test_missing_gates_fail(self):
        (self.base / 'AGENTS.md').touch()
        self.assertEqual(run_verify(str(self.base)), 1)

    def test_failing_gate_and_missing_runner_fail(self):
        target = self.base / 'consumer'
        run_init(str(target), 'essential', 'codex')
        with patch('codex_automata.verify.subprocess.run') as run:
            run.return_value.returncode = 7
            self.assertEqual(run_verify(str(target)), 1)
        with patch('codex_automata.verify.subprocess.run', side_effect=FileNotFoundError('runner')):
            self.assertEqual(run_verify(str(target)), 1)

    @unittest.skipIf(os.name == 'nt', 'Bash entrypoint tested on Linux')
    def test_bash_initializer_ships_hidden_files(self):
        target = self.base / 'shell'
        result = subprocess.run(['bash', str(ROOT / 'scripts/init.sh'),
                                 '--profile', 'essential', str(target)], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((target / '.automata/adapters/automata-context.mdc').is_file())
        self.assertTrue((target / '.automata/assets/agent/LINEAR_FIRST.md').is_file())
        self.assertFalse((target / '.github/workflows/codex-gates.yml').exists())

    @unittest.skipIf(os.name == 'nt', 'Bash CI command tested on Linux')
    def test_shipped_ci_does_not_swallow_python_failures(self):
        workflow = (ROOT / 'harness/.github/workflows/codex-gates.yml').read_text()
        block = workflow.split('      - name: Detect and run tests\n        run: |\n')[1]
        block = block.split('\n  spec-check-windows:')[0]
        script = '\n'.join(line[10:] for line in block.splitlines())
        bin_dir = self.base / 'bin'
        bin_dir.mkdir()
        fake = bin_dir / 'python'
        fake.write_text('#!/bin/sh\ncase "$*" in\n *pytest*tests/*) exit 23;;\n *) exit 0;;\nesac\n')
        fake.chmod(0o755)
        (self.base / 'requirements.txt').touch()
        env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'])
        result = subprocess.run(['bash', '-e', '-c', script], cwd=self.base, env=env,
                                capture_output=True)
        self.assertEqual(result.returncode, 23, result.stderr)
        fake.write_text('#!/bin/sh\nexit 19\n')
        result = subprocess.run(['bash', '-e', '-c', script], cwd=self.base, env=env,
                                capture_output=True)
        self.assertEqual(result.returncode, 19)


if __name__ == '__main__':
    unittest.main()
