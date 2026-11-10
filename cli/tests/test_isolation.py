"""Acceptance molds for namespace and privilege separation."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from codex_automata.control import Controller, ControlError
from codex_automata.init import run_init
from codex_automata.isolation import (install, project_config, verify_installation,
                                      ContextController, migration_report, read_json)


class IsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'consumer'
        self.root.mkdir()
        self.c = Controller(Path(self.tmp.name) / 'authority.sqlite')
        self.addCleanup(self.c.close)
        self.context = ContextController(self.c)
        self.authority = self.context.bootstrap()
        self.config = project_config()
        self.config['paths'].update(source=['packages/worker'], tests=['checks'], sdk=[],
                                    specifications=['requirements'], allowed=['packages', 'checks', 'requirements'],
                                    runtime_state=['var'], operational_entrypoints=['bin/run'],
                                    agent_instructions=['AGENTS.md'], sensitive=['secrets'], forbidden=['vendor'])
        self.config['capabilities']['OPERATE'] = ['runtime:web.run', 'file:read']

    def grant(self, mode='DEVELOP', **changes):
        grant = dict(id='grant-' + mode, actor='agent', task_id='LOCAL-1', repository=str(self.root),
                     context=mode, capabilities=['file:read', 'file:write', 'check:run', 'runtime:web.run'],
                     write_paths=['packages', '.automata'], policy_version='1.0', supersedes=[], reason='operator task')
        grant.update(changes)
        return self.context.authorize(self.authority, grant)

    def test_populated_monorepo_preserved_and_no_app_skeleton(self):
        original = {'AGENTS.md': 'consumer rules', '.cursor/hooks.json': '{"consumer":true}',
                    'packages/worker/main.py': 'source', 'checks/test.py': 'tests',
                    'requirements/spec.md': 'spec', 'var/app-state.json': 'runtime'}
        for name, text in original.items():
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        manifest = install(self.root, config=self.config)
        for name, text in original.items():
            self.assertEqual((self.root / name).read_text(), text)
        self.assertFalse((self.root / 'src').exists())
        self.assertFalse((self.root / 'sdk').exists())
        self.assertFalse((self.root / 'scripts').exists())
        self.assertIn('AGENTS.md', manifest['adapters_pending'])
        verify_installation(self.root)

    def test_missing_context_never_grants_write(self):
        install(self.root, config=self.config)
        with self.assertRaises(ControlError):
            self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'file:write', 'packages/worker/a.py')

    def test_operation_does_not_inherit_development(self):
        install(self.root, config=self.config)
        grant = self.grant('OPERATE')
        event = self.context.select(grant['token'])
        self.assertNotIn('file:write', event['capabilities'])
        self.assertEqual(self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'runtime:web.run')['context'], 'OPERATE')
        for capability, path in [('file:write', 'packages/worker/a.py'), ('check:run', None)]:
            with self.assertRaises(ControlError):
                self.context.evaluate(self.root, 'LOCAL-1', 'agent', capability, path)
        with self.assertRaises(ControlError):
            self.context.select('I am now DEVELOP')
        self.assertFalse((self.root / '.cursor/hooks.json').exists())

    def test_development_is_scoped_and_policy_is_protected(self):
        install(self.root, config=self.config)
        self.context.select(self.grant()['token'])
        self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'file:write', 'packages/worker/a.py')
        for path in ('.automata/project.json', 'var/app-state.json', 'vendor/code.py', '../outside'):
            with self.assertRaises(ControlError):
                self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'file:write', path)
        self.context.select(self.grant('MAINTAIN_METHODOLOGY')['token'])
        self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'file:write', '.automata/assets/PLAYBOOK.md')

    def test_authority_and_supersession_observable(self):
        install(self.root, config=self.config)
        old = self.grant()
        self.context.select(old['token'])
        new = self.grant('OPERATE', supersedes=[old['grant']['id']])
        with self.assertRaises(ControlError):
            self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'file:write', 'packages/worker/a.py')
        with self.assertRaises(ControlError):
            self.context.select(old['token'])
        event = self.context.select(new['token'])
        self.assertEqual(event['current_context'], 'DEVELOP')
        self.assertEqual(event['requested_context'], 'OPERATE')
        with self.assertRaises(ControlError):
            self.context.authorize('fake-authority', {})
        self.assertEqual(self.c.db.execute('SELECT count(*) FROM context_events').fetchone()[0], 2)

    def test_policy_change_invalidates_context(self):
        install(self.root, config=self.config)
        self.context.select(self.grant()['token'])
        p = self.root / '.automata/project.json'
        p.write_text(p.read_text().replace('independent', 'self-for-low-risk'))
        with self.assertRaises(ControlError):
            self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'file:read', 'packages/a.py')

    def test_partial_install_rolls_back_and_migration_preserves(self):
        with patch('codex_automata.isolation.shutil.copytree', side_effect=OSError('disk')):
            with self.assertRaises(OSError):
                install(self.root)
        self.assertEqual(list(self.root.iterdir()), [])
        (self.root / 'PLAYBOOK.md').write_text('custom legacy')
        report = migration_report(self.root)
        self.assertIn('PLAYBOOK.md', report['ambiguous_ownership'])
        self.assertEqual(report['automatic_deletions'], [])
        install(self.root, config=self.config)
        self.assertEqual((self.root / 'PLAYBOOK.md').read_text(), 'custom legacy')

    def test_manifest_tamper_and_symlink_config_rejected(self):
        install(self.root, config=self.config)
        (self.root / '.automata/assets/PLAYBOOK.md').write_text('weakened')
        with self.assertRaises(ControlError):
            verify_installation(self.root)
        self.assertEqual(run_init(str(self.root), 'standard', 'codex'), 1)

    def test_project_unknown_version_or_unsafe_paths(self):
        for key, value in [('schema_version', 99), ('methodology_version', 'future')]:
            config = dict(self.config, **{key: value})
            with self.assertRaises(ControlError):
                install(self.root, config=config)
        config = copy.deepcopy(self.config)
        config['paths']['source'] = ['.automata/assets']
        with self.assertRaises(ControlError):
            install(self.root, config=config)

    def test_update_stages_customizations_without_app_changes(self):
        from codex_automata.update import run_update
        install(self.root, config=self.config)
        custom = self.root / '.automata/assets/PLAYBOOK.md'
        custom.write_text('custom policy')
        stage = self.root.with_name('candidate')
        self.assertEqual(run_update(str(self.root), str(stage)), 0)
        report = read_json(stage / '.automata/migration-report.json')
        self.assertIn('assets/PLAYBOOK.md', report['customized_managed_files'])
        self.assertEqual(custom.read_text(), 'custom policy')
        self.assertEqual(read_json(stage / '.automata/project.json'), self.config)

    def test_verify_requires_development_and_configured_checks(self):
        from codex_automata.verify import run_verify
        self.config['checks'] = [{'name': 'unit', 'argv': ['python', '-c', 'pass']}]
        install(self.root, config=self.config)
        self.context.select(self.grant('OPERATE')['token'])
        self.assertEqual(run_verify(str(self.root), str(self.c.path), 'LOCAL-1', 'agent'), 1)
        self.context.select(self.grant()['token'])
        with patch('codex_automata.verify.subprocess.run') as runner:
            runner.return_value.returncode = 0
            self.assertEqual(run_verify(str(self.root), str(self.c.path), 'LOCAL-1', 'agent'), 0)
            self.assertEqual(runner.call_args.kwargs['cwd'], self.root)

    def test_hook_selftest_exact_payload_and_denial_remedy(self):
        from codex_automata.context_cli import hook_decision
        self.config['capabilities']['OPERATE'].append('mcp:application:web_run')
        install(self.root, config=self.config)
        self.context.select(self.grant('OPERATE', capabilities=['mcp:application:web_run'])['token'])
        result = hook_decision(self.context, self.root, 'LOCAL-1', 'agent',
                               {'tool_name': 'MCP:web_run', 'mcp_server_name': 'application'})
        self.assertTrue(result['allowed'])
        for payload in ({'tool_name': 'MCP:web_run'}, {'tool_name': 'Shell'},
                        {'tool_name': 'MCP:web_run', 'mcp_server_name': 'unapproved'}):
            with self.assertRaises(ControlError):
                hook_decision(self.context, self.root, 'LOCAL-1', 'agent', payload)

    def test_maintenance_can_repair_multiple_assets_without_unlocking_development(self):
        install(self.root, config=self.config)
        token = self.grant('MAINTAIN_METHODOLOGY')['token']
        self.context.select(token)
        (self.root / '.automata/assets/PLAYBOOK.md').write_text('authorized maintenance in progress')
        self.context.evaluate(self.root, 'LOCAL-1', 'agent', 'file:write', '.automata/assets/agent/AGENT_RULES.md')
        with self.assertRaises(ControlError):
            self.context.select(self.grant()['token'])

    def test_install_failure_after_adapter_creation_rolls_back(self):
        with patch('codex_automata.isolation.Path.rename', side_effect=OSError('rename interrupted')):
            with self.assertRaises(OSError):
                install(self.root)
        self.assertEqual(list(self.root.iterdir()), [])
