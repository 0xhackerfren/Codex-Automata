"""Regression molds derived from the reproduced adversarial findings."""
from datetime import datetime, timedelta, timezone
import json
import os
import sys
import unittest
from unittest.mock import patch

from codex_automata.control import Controller, ControlError
from codex_automata.snapshot import committed_snapshot, verify_worktree


class AdversarialFixTests(unittest.TestCase):
    def setUp(self):
        import test_workflow
        self.t = test_workflow.WorkflowTests()
        self.t.setUp()
        self.addCleanup(self.t.doCleanups)

    def reviewed_ready(self):
        t = self.t
        t.plan.update(profile='standard', impacts=['feature'])
        t.plan['checks'].append(dict(name='integration', argv=[sys.executable, '-B', 'check.py'],
                                    role='integration', tier='T1', timeout=10))
        t.to_cast(); t.fix(); t.checks(); t.advance('cast')
        token = t.grant('reviewer')
        artifact = t.artifact('review', review=dict(kind='independent', reviewer='reviewer', approved=True, unresolved=0))
        t.w.attest_review('LOCAL-1', token, artifact)
        return token, artifact

    def test_hidden_dirty_worktree_cannot_complete(self):
        t = self.t
        t.to_cast(); t.fix(); t.checks()
        t.git('update-index', '--assume-unchanged', 'app.txt')
        (t.repo / 'app.txt').write_text('broken after verification')
        with self.assertRaises(ControlError):
            t.advance('cast')

    def test_approved_spec_revision_and_later_freeze(self):
        t = self.t
        t.job['write_paths'].append('spec.md')
        t.plan['approved_changes'] = ['spec.md']
        t.plan['packet_digest'] = Controller.digest(t.job)
        t.start(); t.advance('intake')
        (t.repo / 'spec.md').write_text('Rule 1: clarified approved requirement.\n')
        t.commit('write specification')
        t.advance('specify')
        (t.repo / 'spec.md').write_text('Unauthorized later drift.\n')
        t.commit('drift after specification freeze')
        with self.assertRaises(ControlError):
            t.w.context_packet('LOCAL-1', 'coder', t.token)

    def test_new_sdk_and_mold_full_workflow(self):
        t = self.t
        t.git('rm', 'contract.py', 'check.py'); t.commit('greenfield baseline')
        t.job.update(phase='discover', base_sha=t.head(), write_paths=['app.txt', 'contract.py', 'check.py'])
        t.plan.update(profile='standard', impacts=['feature'], packet_digest=Controller.digest(t.job),
                      planned_outputs={'sdk': ['contract.py'], 'mold': ['check.py']})
        t.plan['checks'].append(dict(name='integration', argv=[sys.executable, '-B', 'check.py'],
                                    role='integration', tier='T1', timeout=10))
        t.start()
        packet = t.w.context_packet('LOCAL-1', 'coder', t.token)
        self.assertTrue(any(s.get('status') == 'planned-output' for s in packet['sources']))
        t.advance('intake'); t.advance('specify')
        (t.repo / 'contract.py').write_text('VALUE = "fixed"\n'); t.commit('create SDK')
        t.advance('sdk')
        (t.repo / 'check.py').write_text('from pathlib import Path\nassert Path("app.txt").read_text() == "fixed"\n')
        t.commit('create mold'); t.checks(red=True); t.advance('mold')
        t.fix(); t.checks(); t.advance('cast')
        reviewer = t.grant('reviewer')
        artifact = t.artifact('review', review=dict(kind='independent', reviewer='reviewer', approved=True, unresolved=0))
        t.w.attest_review('LOCAL-1', reviewer, artifact)
        t.w.advance('LOCAL-1', 'coder', t.token, artifact)
        self.assertEqual(t.advance('observe')['status'], 'completed-local')

    def test_old_attestation_cannot_be_accepted_as_fresh(self):
        t = self.t
        _, artifact = self.reviewed_ready()
        class Later(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime.now(tz) + timedelta(hours=48)
        with patch('codex_automata.workflow.datetime', Later):
            with self.assertRaisesRegex(ControlError, 'expired'):
                t.w.advance('LOCAL-1', 'coder', t.token, artifact)

    def test_rewind_requires_new_reviewer_attestation(self):
        t = self.t
        reviewer, artifact = self.reviewed_ready()
        t.w.advance('LOCAL-1', 'coder', t.token, artifact)
        t.w.rewind('LOCAL-1', 'coder', t.token, 'review', 'renew review')
        with self.assertRaises(ControlError):
            t.w.advance('LOCAL-1', 'coder', t.token, artifact)
        t.w.attest_review('LOCAL-1', reviewer, artifact)
        t.w.advance('LOCAL-1', 'coder', t.token, artifact)
        self.assertEqual(t.advance('observe')['status'], 'completed-local')

    def test_snapshot_excludes_ignored_files_and_inherited_import_settings(self):
        t = self.t
        (t.repo / '.git/info/exclude').write_text('ignored-source.txt\n')
        (t.repo / 'ignored-source.txt').write_text('uncommitted poison')
        t.plan['checks'][0]['argv'] = [sys.executable, '-B', '-c',
            'import os; from pathlib import Path; assert not Path("ignored-source.txt").exists(); '
            'assert "AUTOMATA_TEST_SECRET" not in os.environ; assert "PYTHONPATH" not in os.environ']
        t.start()
        with patch.dict(os.environ, {'AUTOMATA_TEST_SECRET': 'test sentinel'}):
            result = t.w.execute('LOCAL-1', 'coder', t.token, 'static')
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(result['execution_mode'], 'committed-snapshot')

    def test_snapshot_mutation_is_failed_evidence(self):
        t = self.t
        t.plan['checks'][0]['argv'] = [sys.executable, '-B', '-c',
            'from pathlib import Path; Path("app.txt").write_text("mutated snapshot")']
        t.start()
        result = t.w.execute('LOCAL-1', 'coder', t.token, 'static')
        self.assertFalse(result['unchanged'])
        self.assertEqual((t.repo / 'app.txt').read_text(), 'broken')
        self.assertEqual(t.c.state('LOCAL-1')['attempts'], 1)

    def test_hidden_file_content_rejected_without_index_hint(self):
        t = self.t
        before = (t.repo / 'app.txt').stat()
        (t.repo / 'app.txt').write_bytes(b'BROKEN')
        os.utime(t.repo / 'app.txt', ns=(before.st_atime_ns, before.st_mtime_ns))
        with self.assertRaisesRegex(ControlError, 'content differs'):
            verify_worktree(t.repo, t.head())

    def test_snapshot_ignores_export_attributes_and_preserves_blob_bytes(self):
        t = self.t
        (t.repo / '.gitattributes').write_text('app.txt export-ignore\nnotes.md export-subst\n')
        (t.repo / 'notes.md').write_text('$Format:%H$\n')
        t.commit('export attributes cannot change evidence')
        with committed_snapshot(t.repo, t.head(), t.root) as (root, _):
            self.assertEqual((root / 'app.txt').read_bytes(), b'broken')
            self.assertEqual((root / 'notes.md').read_bytes(), b'$Format:%H$\n')

    def test_git_declared_crlf_allowed_but_binary_changes_rejected(self):
        t = self.t
        (t.repo / '.gitattributes').write_text('notes.md text eol=crlf\n')
        (t.repo / 'notes.md').write_bytes(b'line\n')
        t.commit('declared newline behavior')
        (t.repo / 'notes.md').write_bytes(b'line\r\n')
        verify_worktree(t.repo, t.head())
        (t.repo / 'notes.md').write_bytes(b'other\r\n')
        with self.assertRaises(ControlError):
            verify_worktree(t.repo, t.head())

    def test_planned_output_scope_and_legacy_validation_fail_closed(self):
        from codex_automata.control import validate_job
        t = self.t
        t.git('rm', 'contract.py'); t.commit('future SDK')
        t.job.update(phase='discover', base_sha=t.head())
        t.plan.update(profile='standard', packet_digest=Controller.digest(t.job),
                      planned_outputs={'sdk': ['contract.py']})
        with self.assertRaises(ControlError):
            validate_job(t.job)
        with self.assertRaises(ControlError):
            t.w.approve(t.authority, t.job, t.plan)

    def test_rewind_allows_authorized_spec_amendment(self):
        t = self.t
        t.job['write_paths'].append('spec.md')
        t.plan.update(approved_changes=['spec.md'], packet_digest=Controller.digest(t.job))
        t.to_cast()
        t.w.rewind('LOCAL-1', 'coder', t.token, 'specify', 'Operator-approved requirement clarification')
        (t.repo / 'spec.md').write_text('Rule 1: amended before recasting.\n')
        t.commit('amend requirement')
        t.advance('specify')

    def test_attestation_expiry_at_downstream_gate_and_renewal(self):
        t = self.t
        reviewer, artifact = self.reviewed_ready()
        t.w.advance('LOCAL-1', 'coder', t.token, artifact)
        class Later(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime.now(tz) + timedelta(hours=48)
        # A fresh coder-side acceptance timestamp cannot refresh reviewer time.
        row = t.c.db.execute('SELECT artifacts FROM workflows WHERE id=?', ('LOCAL-1',)).fetchone()
        artifacts = json.loads(row[0])
        artifacts[-1]['recorded_at'] = Later.now(timezone.utc).isoformat()
        t.c.db.execute('UPDATE workflows SET artifacts=? WHERE id=?', (json.dumps(artifacts), 'LOCAL-1'))
        with patch('codex_automata.workflow.datetime', Later):
            with self.assertRaisesRegex(ControlError, 'expired'):
                t.advance('observe')
            t.w.attest_review('LOCAL-1', reviewer, artifact)
            self.assertEqual(t.advance('observe')['status'], 'completed-local')
        self.assertEqual(t.c.db.execute('SELECT count(*) FROM review_attestation_history').fetchone()[0], 2)

    def test_missing_and_future_attestation_times_fail_closed(self):
        t = self.t
        _, artifact = self.reviewed_ready()
        for timestamp in (None, 'invalid', datetime.now().isoformat(),
                          (datetime.now(timezone.utc) + timedelta(hours=48)).isoformat()):
            with self.subTest(timestamp=timestamp):
                t.c.db.execute('UPDATE review_attestations SET issued_at=?', (timestamp,))
                with self.assertRaises(ControlError):
                    t.w.advance('LOCAL-1', 'coder', t.token, artifact)

    def test_explicit_worktree_mode_supports_git_and_labels_receipt(self):
        t = self.t
        t.plan['execution_mode'] = 'verified-worktree'
        t.plan['checks'][0]['argv'] = [sys.executable, '-B', '-c',
            'from pathlib import Path; assert Path(".git").is_dir()']
        t.start()
        receipt = t.w.execute('LOCAL-1', 'coder', t.token, 'static')
        self.assertEqual(receipt['execution_mode'], 'verified-worktree')
        self.assertEqual(receipt['exit_code'], 0)
        t.git('update-index', '--skip-worktree', 'app.txt')
        with self.assertRaises(ControlError):
            t.w.execute('LOCAL-1', 'coder', t.token, 'static')

    def test_execution_mode_cannot_change_after_approval(self):
        import copy
        t = self.t
        t.w.approve(t.authority, t.job, t.plan)
        changed = copy.deepcopy(t.plan)
        changed['execution_mode'] = 'verified-worktree'
        with self.assertRaisesRegex(ControlError, 'prior operator approval'):
            t.w.start(t.job, changed, 'coder')

    @unittest.skipUnless(os.name == 'posix', 'POSIX symlink creation')
    def test_committed_symlink_is_explicitly_rejected(self):
        t = self.t
        (t.repo / 'link').symlink_to('app.txt')
        t.commit('symlink requires adapter')
        with self.assertRaisesRegex(ControlError, 'symlinks/submodules'):
            with committed_snapshot(t.repo, t.head(), t.root):
                self.fail('symlink snapshot unexpectedly accepted')

    @unittest.skipUnless(os.name == 'posix', 'POSIX executable modes')
    def test_snapshot_executable_mode_mutation_is_failed_evidence(self):
        t = self.t
        t.plan['checks'][0]['argv'] = [sys.executable, '-B', '-c',
            'import os; os.chmod("app.txt", 0o755)']
        t.start()
        receipt = t.w.execute('LOCAL-1', 'coder', t.token, 'static')
        self.assertFalse(receipt['unchanged'])
        self.assertEqual(t.c.state('LOCAL-1')['attempts'], 1)
