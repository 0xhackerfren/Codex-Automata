from pathlib import Path
import tempfile
import unittest
from codex_automata.benchmark import prepare, evaluate, corpus, ARMS
from codex_automata.control import ControlError


class BenchmarkTests(unittest.TestCase):
    def test_oracles_accept_solutions_and_reject_baselines_across_all_arms(self):
        with tempfile.TemporaryDirectory() as tmp:
            for task in corpus():
                for arm in ARMS:
                    with self.subTest(task=task['id'], arm=arm):
                        root = Path(tmp) / (task['id'] + arm)
                        run = prepare(task['id'], arm, root, 16000)
                        baseline = evaluate(root)
                        self.assertFalse(baseline['correct'])
                        self.assertEqual(baseline['model_results'], 'pending')
                        for name, content in task['solution'].items():
                            (root / 'candidate' / name).write_text(content)
                        result = evaluate(root)
                        self.assertTrue(result['correct'], result)
                        self.assertIsNone(result['first_pass_acceptance'])
                        self.assertLessEqual(run['context_bytes'], 16000)

    def test_unauthorized_change_and_budget_cannot_be_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            prepare('trivial', 'bare', root, 16000)
            (root / 'candidate/message.txt').write_text('Hello, world!\n')
            (root / 'candidate/unauthorized.py').write_text('pass')
            result = evaluate(root)
            self.assertFalse(result['correct'])
            self.assertEqual(result['unauthorized_changes'], ['unauthorized.py'])
            with self.assertRaises(ControlError):
                prepare('feature', 'automata', Path(tmp) / 'tiny', 1024)

    def test_telemetry_must_pair_task_arm_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            prepare('trivial', 'bare', root, 16000)
            with self.assertRaises(ControlError):
                evaluate(root, {'schema_version': 99})
