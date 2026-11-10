"""Specification-derived negative molds for delivery control plane."""
import copy
import json
import os
import sqlite3
from pathlib import Path
import subprocess
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor

from codex_automata.control import Controller, ControlError, validate_job


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-b', 'main')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Test')
        for path in ('spec.md', 'sdk.py', 'test_app.py', 'app.py'):
            (self.repo / path).write_text('initial\n')
        self.git('add', '.')
        self.git('commit', '-m', 'initial')
        self.sha = self.git('rev-parse', 'HEAD')
        self.job = dict(schema_version=1, id='JOB-1', repository=str(self.repo),
                        branch='main', base_sha=self.sha, phase='cast',
                        outcome='Deliver bounded change', risk='routine', write_paths=['app.py'],
                        acceptance=['Expected behavior'], dependencies=[],
                        specs=['spec.md'], contracts=['sdk.py'], molds=['test_app.py'],
                        policy_id='client-approved', data_class='private', max_attempts=3)
        self.policy = dict(schema_version=1, id='client-approved', models=[
            dict(id='cheap', tier='economical', available=True, phases=['cast'],
                 data_classes=['private']),
            dict(id='strong', tier='frontier', available=True,
                 phases=['cast', 'architect'], data_classes=['private'])])
        self.db = self.root / 'control.sqlite'
        self.c = Controller(self.db)
        self.addCleanup(lambda: self.c.close())

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args],
                                       stderr=subprocess.DEVNULL, text=True).strip()

    def claim(self):
        return self.c.claim(self.job, 'worker-1')

    def evidence(self):
        return dict(packet_digest=self.c.digest(self.job), head_sha=self.sha,
                    checks=[dict(name='unit', head_sha=self.sha, status='passed')],
                    review=dict(head_sha=self.sha, reviewer='reviewer-2', approved=True,
                                unresolved=0), required_checks=['unit'],
                    integration_sha=self.sha)

    def test_schema_and_phase_gates(self):
        for key, value in [('schema_version', 99), ('phase', 'mystery'),
                           ('write_paths', ['../escape']), ('max_attempts', True),
                           ('acceptance', []), ('specs', ['missing.md']),
                           ('contracts', []), ('molds', [])]:
            with self.subTest(key=key):
                job = dict(self.job, **{key: value})
                with self.assertRaises(ControlError):
                    validate_job(job)
        research = dict(self.job, phase='discover', contracts=[], molds=[])
        validate_job(research)

    def test_untracked_reference_rejected(self):
        (self.repo / 'untracked.md').write_text('not versioned')
        with self.assertRaises(ControlError):
            validate_job(dict(self.job, specs=['untracked.md']))

    def test_routing_denies_policy_dependency_and_stale_base(self):
        self.assertEqual(self.c.route(self.job, self.policy)['model'], 'cheap')
        for job, policy in [(dict(self.job, dependencies=['MISSING']), self.policy),
                            (self.job, dict(self.policy, id='other')),
                            (self.job, dict(self.policy, models=[])),
                            (dict(self.job, base_sha='0' * 40), self.policy)]:
            with self.assertRaises(ControlError):
                self.c.route(job, policy)

    def test_attempts_survive_restart_and_model_change(self):
        claim = self.claim()
        self.c.attempt('JOB-1', 'worker-1', claim['token'], 'capability', 'failure')
        self.assertEqual(self.c.route(self.job, self.policy)['model'], 'strong')
        self.c.close()
        self.c = Controller(self.db)
        for _ in range(2):
            self.c.attempt('JOB-1', 'worker-1', claim['token'], 'capability', 'failure')
        with self.assertRaises(ControlError):
            self.c.route(self.job, self.policy)

    def test_environment_failure_does_not_escalate(self):
        claim = self.claim()
        self.c.attempt('JOB-1', 'worker-1', claim['token'], 'environment', 'missing runner')
        with self.assertRaises(ControlError):
            self.c.route(self.job, self.policy)

    def test_risk_routes_up_without_changing_approval(self):
        high = dict(self.job, risk='critical')
        self.assertEqual(self.c.route(high, self.policy)['model'], 'strong')
        denied = copy.deepcopy(self.policy)
        denied['models'][1]['data_classes'] = ['public']
        with self.assertRaises(ControlError):
            self.c.route(high, denied)

    def test_resolution_records_repair_without_resetting_budget(self):
        claim = self.claim()
        self.c.attempt('JOB-1', 'worker-1', claim['token'], 'environment', 'missing runner')
        self.c.resolve('JOB-1', 'worker-1', claim['token'], 'runner repaired and verified')
        self.assertEqual(self.c.route(self.job, self.policy)['attempts'], 1)
        self.c.release('JOB-1', 'worker-1', claim['token'], 'handoff')
        self.c.claim(self.job, 'worker-2')

    def test_completion_checks_actual_changed_paths(self):
        claim = self.claim()
        (self.repo / 'sdk.py').write_text('unauthorized change')
        self.git('add', '.')
        self.git('commit', '-m', 'outside assigned scope')
        self.sha = self.git('rev-parse', 'HEAD')
        with self.assertRaises(ControlError):
            self.c.complete(self.job, 'worker-1', claim['token'], self.evidence(), ['unit'])

    def test_valid_vertical_slice_and_cli_validate(self):
        from codex_automata.cli import main
        packet = self.root / 'packet.json'
        packet.write_text(json.dumps(self.job))
        self.assertEqual(main(['job', 'validate', str(packet)]), 0)
        route = self.c.route(self.job, self.policy)
        self.assertEqual(route['model'], 'cheap')
        claim = self.claim()
        self.git('checkout', '-b', 'job-1')
        (self.repo / 'app.py').write_text('delivered behavior')
        self.git('add', 'app.py')
        self.git('commit', '-m', 'implement bounded change')
        self.sha = self.git('rev-parse', 'HEAD')
        evidence = self.evidence()
        # A reviewed but unintegrated branch cannot be declared completed.
        with self.assertRaises(ControlError):
            self.c.complete(self.job, 'worker-1', claim['token'], evidence, ['unit'])
        self.git('checkout', 'main')
        self.git('merge', '--ff-only', 'job-1')
        self.c.complete(self.job, 'worker-1', claim['token'], evidence, ['unit'])
        self.assertEqual(self.c.state('JOB-1')['status'], 'completed')
        dependent = dict(self.job, id='JOB-2', base_sha=self.sha, dependencies=['JOB-1'])
        self.assertEqual(self.c.route(dependent, self.policy)['model'], 'cheap')

    def test_claim_token_checkpoint_and_packet_immutability(self):
        claim = self.claim()
        with self.assertRaises(ControlError):
            self.c.checkpoint('JOB-1', 'worker-1', 'wrong', 'resume')
        self.c.checkpoint('JOB-1', 'worker-1', claim['token'], 'resume here')
        with self.assertRaises(ControlError):
            self.c.route(dict(self.job, outcome='changed intent'), self.policy)
        self.c.release('JOB-1', 'worker-1', claim['token'], 'paused')
        self.assertEqual(self.c.state('JOB-1')['checkpoint'], 'paused')

    def test_concurrent_claims_allow_only_one_writer(self):
        def compete(n):
            c = Controller(self.db)
            try:
                job = dict(self.job, id='JOB-' + str(n))
                return c.claim(job, 'worker-' + str(n))['token']
            except ControlError:
                return None
            finally:
                c.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(compete, [2, 3]))
        self.assertEqual(sum(result is not None for result in results), 1)

    def test_evidence_rejects_stale_self_review_failed_duplicate_and_missing(self):
        claim = self.claim()
        baseline = self.evidence()
        mutations = []
        for field in ('head_sha', 'packet_digest', 'integration_sha'):
            e = copy.deepcopy(baseline)
            e[field] = '0' * 40
            mutations.append(e)
        for field, value in [('reviewer', 'worker-1'), ('approved', False),
                             ('unresolved', 1), ('head_sha', '0' * 40)]:
            e = copy.deepcopy(baseline)
            e['review'][field] = value
            mutations.append(e)
        for status in ('failed', 'skipped'):
            e = copy.deepcopy(baseline)
            e['checks'][0]['status'] = status
            mutations.append(e)
        e = copy.deepcopy(baseline)
        e['checks'] *= 2
        mutations.append(e)
        e = copy.deepcopy(baseline)
        e['checks'] = []
        mutations.append(e)
        for evidence in mutations:
            with self.subTest(evidence=evidence):
                with self.assertRaises(ControlError):
                    self.c.complete(self.job, 'worker-1', claim['token'], evidence,
                                    required_checks=['unit'])
        self.assertEqual(self.c.state('JOB-1')['status'], 'active')
        self.c.complete(self.job, 'worker-1', claim['token'], baseline,
                        required_checks=['unit'])
        self.assertEqual(self.c.state('JOB-1')['status'], 'completed')

    def test_dependent_job_waits_for_completed_evidence(self):
        with self.assertRaises(ControlError):
            self.c.route(dict(self.job, id='JOB-2', dependencies=['JOB-1']), self.policy)
        claim = self.claim()
        self.c.complete(self.job, 'worker-1', claim['token'], self.evidence(),
                        required_checks=['unit'])
        self.assertEqual(self.c.route(dict(self.job, id='JOB-2', dependencies=['JOB-1']),
                                      self.policy)['model'], 'cheap')

    def test_journal_replay_and_uncertain_reconciliation(self):
        payload = dict(entity='JOB-1', revision='v1', desired='review')
        self.c.prepare_operation('op-1', payload)
        self.c.uncertain_operation('op-1')
        self.assertEqual(self.c.prepare_operation('op-1', payload)['status'], 'uncertain')
        with self.assertRaises(ControlError):
            self.c.prepare_operation('op-1', dict(payload, desired='done'))
        with self.assertRaises(ControlError):
            self.c.reconcile_operation('op-1', dict(payload, revision='v2'))
        self.c.reconcile_operation('op-1', payload)
        self.assertEqual(self.c.prepare_operation('op-1', payload)['status'], 'confirmed')

    def test_rejects_unknown_database_version(self):
        other = self.root / 'future.sqlite'
        db = sqlite3.connect(other)
        db.execute('PRAGMA user_version=99')
        db.close()
        with self.assertRaises(ControlError):
            Controller(other)

    @unittest.skipIf(os.name == 'nt', 'POSIX permissions')
    def test_new_state_database_is_private(self):
        self.assertEqual(self.db.stat().st_mode & 0o777, 0o600)

    def test_cli_rejects_duplicate_json_fields(self):
        from codex_automata.cli import main
        bad = self.root / 'duplicate.json'
        bad.write_text('{"schema_version":1,"schema_version":99}')
        self.assertEqual(main(['job', 'validate', str(bad)]), 1)

    def test_cli_rejects_bad_json(self):
        from codex_automata.cli import main
        bad = self.root / 'bad.json'
        bad.write_text('{')
        self.assertEqual(main(['job', 'validate', str(bad)]), 1)


if __name__ == '__main__':
    unittest.main()
