"""Run a complete offline single-agent workflow in a disposable repository.

Run: PYTHONPATH=cli python examples/standalone_workflow_demo.py
No network, LLM, Linear, service, GitHub API or second agent is used. The explicit
operator bootstrap is demonstrated in-process; production adapters must separate
that authority from model tools.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from codex_automata.control import Controller
from codex_automata.isolation import ContextController, install, project_config
from codex_automata.workflow import Workflow, blob


def demonstrate():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        repo = root / 'application'
        repo.mkdir()
        def git(*args):
            return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.DEVNULL, text=True).strip()
        git('init', '-b', 'main')
        git('config', 'user.name', 'Offline demo')
        git('config', 'user.email', 'demo@example.invalid')
        config = project_config('essential')
        config['paths'].update(source=['app.py'], specifications=['requirements.md'], tests=['test_mean.py'],
                               allowed=['app.py'])
        install(repo, profile='essential', agent='codex', config=config)
        files = {'requirements.md': 'R1: mean([]) returns None; mean([1,2]) returns 1.5.\n',
                 'app.py': 'def mean(values):\n    return sum(values) // len(values)\n',
                 'test_mean.py': 'from app import mean\nassert mean([]) is None\nassert mean([1,2]) == 1.5\n'}
        for name, content in files.items():
            (repo / name).write_text(content, encoding='utf-8')
        git('add', '.')
        git('commit', '-m', 'spec and molds baseline')
        job = dict(schema_version=1, id='DEMO-1', repository=str(repo), branch='main', base_sha=git('rev-parse','HEAD'),
                   phase='discover', outcome='Fix mean under R1', risk='routine', write_paths=['app.py'],
                   acceptance=['R1'], dependencies=[], specs=['requirements.md'], contracts=[], molds=['test_mean.py'],
                   policy_id='local-manual', data_class='private', max_attempts=3)
        checks = [dict(name='static', argv=[sys.executable,'-B','-c','import ast; ast.parse(open("test_mean.py").read())'], role='static',tier='T0',timeout=10),
                  dict(name='fixture', argv=[sys.executable,'-B','-c','assert sum([1,2])/len([1,2]) == 1.5'], role='fixture',tier='T0',timeout=10),
                  dict(name='behavior', argv=[sys.executable,'-B','test_mean.py'],role='behavior',tier='T1',timeout=10)]
        plan = dict(schema_version=1, methodology_version='1.0', packet_digest=Controller.digest(job),
                    profile='small', impacts=['bugfix'], checks=checks, traceability={'R1':['behavior']},
                    context_paths=['app.py'], context_budget=16000, review_policy='self-for-low-risk',
                    review_max_age_hours=24, approved_changes=[])
        c = Controller(root / 'control.sqlite')
        try:
            context = ContextController(c)
            authority = context.bootstrap()
            grant = dict(id='demo-development', actor='coder', task_id=job['id'], repository=str(repo),
                         context='DEVELOP', capabilities=['file:read','file:write','check:run'], write_paths=['app.py'],
                         policy_version='1.0', supersedes=[], reason='Explicit offline demo operator authorization')
            context.select(context.authorize(authority, grant)['token'])
            workflow = Workflow(c)
            workflow.approve(authority, job, plan)
            token = workflow.start(job, plan, 'coder')['token']
            context_sizes = []
            for phase in ('intake','specify','mold','cast','review','observe'):
                packet = workflow.context_packet(job['id'], 'coder', token)
                context_sizes.append(packet['context_bytes'])
                if phase == 'mold':
                    for check in checks:
                        receipt = workflow.execute(job['id'],'coder',token,check['name'],'fail' if check['role']=='behavior' else 'pass')
                        assert receipt['failure'] is None
                if phase == 'cast':
                    checkpoint = workflow.snapshot(job['id'])
                    workflow.resume(job['id'], 'coder', token, checkpoint)
                    (repo / 'app.py').write_text('def mean(values):\n    return sum(values) / len(values) if values else None\n')
                    git('add','app.py')
                    git('commit','-m','fix R1')
                    for check in checks:
                        receipt = workflow.execute(job['id'],'coder',token,check['name'])
                        assert receipt['exit_code'] == 0
                head = git('rev-parse','HEAD')
                outputs = ['test_mean.py'] if phase == 'mold' else ['app.py'] if phase == 'cast' else ['requirements.md']
                artifact = dict(schema_version=1, methodology_version='1.0', task_id=job['id'],
                                packet_digest=Controller.digest(job), phase=phase, head_sha=head, inputs=[],
                                outputs=[dict(path=p,blob=blob(repo,head,p)) for p in outputs],
                                summary='Observed ' + phase + '; local only, no deployment',
                                review=dict(kind='self',reviewer='coder',approved=True,unresolved=0) if phase=='review' else None)
                result = workflow.advance(job['id'],'coder',token,artifact)
            snapshot = workflow.snapshot(job['id'])
            return dict(status=result['status'], deployed=result['deployed'], review=result['review']['kind'],
                        phases_completed=len(snapshot['artifacts']), observed_commands=len(snapshot['verified_results']),
                        attempts=snapshot['attempts'], context_max_bytes=max(context_sizes), context_budget_bytes=16000,
                        checkpoint_resumed=True, external_services_used=False)
        finally:
            c.close()


if __name__ == '__main__':
    print(json.dumps(demonstrate(), sort_keys=True))
