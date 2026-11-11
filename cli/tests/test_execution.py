"""Real child processes exercise bounded output and cleanup behavior."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

from codex_automata.execution import run_check
from codex_automata.workflow import validate_schema
from codex_automata.control import ControlError


class ExecutionTests(unittest.TestCase):
    def run_python(self, code, limit=1024, timeout=3):
        return run_check([sys.executable, '-B', '-c', code], Path.cwd(), timeout, limit)

    def test_exact_limit_and_merged_stderr(self):
        result = self.run_python('import os; os.write(1, b"a" * 512); os.write(2, b"b" * 512)')
        self.assertEqual(result['exit_code'], 0)
        self.assertIsNone(result['failure'])
        self.assertEqual(result['output_bytes'], 1024)
        self.assertEqual(result['output_sha256'], hashlib.sha256(b'a' * 512 + b'b' * 512).hexdigest())

    def test_zero_exit_overflow_is_failure_with_prefix_hash(self):
        result = self.run_python('import os; os.write(1, b"x" * 1025)')
        self.assertEqual(result['failure'], 'output-limit')
        self.assertEqual(result['output_bytes'], 1024)
        self.assertEqual(result['output_sha256'], hashlib.sha256(b'x' * 1024).hexdigest())
        self.assertEqual(result['output_excerpt'], 'x' * 1024)

    def test_continuous_output_stops_and_excerpt_is_bounded(self):
        start = time.monotonic()
        result = self.run_python('import os\nwhile True: os.write(1, b"x" * 65536)', limit=10000)
        self.assertEqual(result['failure'], 'output-limit')
        self.assertEqual(result['output_bytes'], 10000)
        self.assertEqual(len(result['output_excerpt']), 8192)
        self.assertLess(time.monotonic() - start, 3)

    def test_silent_timeout_and_spawn_failure(self):
        self.assertEqual(self.run_python('import time; time.sleep(30)', timeout=0.15)['failure'], 'timeout')
        result = run_check(['automata-nonexistent-test-command'], Path.cwd(), 1, 1024)
        self.assertEqual(result['failure'], 'FileNotFoundError')
        self.assertEqual(result['output_bytes'], 0)

    def test_limit_schema_rejects_invalid_values(self):
        from test_workflow import WorkflowTests
        fixture = WorkflowTests()
        fixture.setUp()
        try:
            for value in (0, -1, 16777217, True, '1024'):
                fixture.plan['checks'][0]['output_limit_bytes'] = value
                with self.assertRaises(ControlError):
                    validate_schema('plan', fixture.plan)
        finally:
            fixture.doCleanups()

    @unittest.skipUnless(os.name == 'posix', 'POSIX process groups')
    def test_descendants_stopped_after_timeout_and_parent_exit(self):
        for parent in ('time.sleep(30)', 'pass'):
            with self.subTest(parent=parent), tempfile.TemporaryDirectory() as tmp:
                marker = Path(tmp) / 'escaped'
                child = 'import time; from pathlib import Path; time.sleep(0.7); Path(' + repr(str(marker)) + ').write_text("escaped")'
                code = 'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",' + repr(child) + ']); ' + parent
                result = self.run_python(code, timeout=0.25)
                self.assertEqual(result['failure'], 'timeout' if parent != 'pass' else None)
                time.sleep(0.8)
                self.assertFalse(marker.exists(), 'descendant survived process-group cleanup')
