"""Reproducible, external-agent three-arm engineering evaluation.

No live model numbers are inferred from deterministic fixture checks. Candidate
code is executed: run evaluation in an isolated disposable environment.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from .control import Controller, require, canonical
from .workflow import UNIVERSAL, PHASE_INSTRUCTIONS
from .isolation import read_json

ARMS = ('bare', 'concise', 'automata')
CONCISE = 'Follow the specification, keep scope bounded, preserve tests, verify behavior, and report limitations.'


def corpus():
    # Same visible files and evaluator oracles in every instruction arm. Solutions
    # exist only for deterministic harness tests; never include them in prompts.
    return [
        dict(id='trivial', category='trivial', outcome='Change the greeting to Hello, world! Preserve the trailing newline.',
             files={'message.txt': 'Helo, world!\n'}, allowed=['message.txt'],
             solution={'message.txt': 'Hello, world!\n'},
             checks=[('acceptance', "from pathlib import Path; assert Path('message.txt').read_text() == 'Hello, world!\\n'")]),
        dict(id='bounded-bug', category='bugfix', outcome='mean([]) must return None; nonempty means retain fractional precision.',
             files={'app.py': 'def mean(values):\n    return sum(values) // len(values)\n'}, allowed=['app.py'],
             solution={'app.py': 'def mean(values):\n    return sum(values) / len(values) if values else None\n'},
             checks=[('acceptance', 'from app import mean; assert mean([]) is None; assert mean([1,2]) == 1.5'),
                     ('regression', 'from app import mean; assert mean([2,4]) == 3')]),
        dict(id='feature', category='feature', outcome='Add unique(values): return first occurrences in original order, supporting unhashable values. Keep identity unchanged.',
             files={'app.py': 'def identity(value):\n    return value\n'}, allowed=['app.py'],
             solution={'app.py': 'def identity(value):\n    return value\ndef unique(values):\n    out=[]\n    for v in values:\n        if v not in out: out.append(v)\n    return out\n'},
             checks=[('acceptance', 'from app import unique; assert unique([2,1,2]) == [2,1]; assert unique([[1],[1],[]]) == [[1],[]]'),
                     ('regression', 'from app import identity; x=[]; assert identity(x) is x')]),
        dict(id='refactor', category='refactor', outcome='Replace total recursion with iteration without changing sum behavior. Handle 10,000 items.',
             files={'app.py': 'def total(values):\n    return 0 if not values else values[0]+total(values[1:])\n'}, allowed=['app.py'],
             solution={'app.py': 'def total(values):\n    result=0\n    for v in values: result+=v\n    return result\n'},
             checks=[('acceptance', 'from app import total; assert total(list(range(10000))) == 49995000'),
                     ('regression', 'from app import total; assert total([])==0; assert total([-2,3])==1')]),
        dict(id='api', category='api-change', outcome='Keep parse(text) returning an integer; add keyword-only base=10 support to the contract and implementation.',
             files={'contracts.py': 'def parse(text: str) -> int: ...\n', 'app.py': 'def parse(text):\n    return int(text)\n'}, allowed=['app.py','contracts.py'],
             solution={'contracts.py': 'def parse(text: str, *, base: int = 10) -> int: ...\n', 'app.py': 'def parse(text, *, base=10):\n    return int(text, base)\n'},
             checks=[('acceptance', 'from app import parse; import contracts, inspect; assert parse("ff",base=16)==255; assert inspect.signature(contracts.parse).parameters["base"].kind == inspect.Parameter.KEYWORD_ONLY'),
                     ('regression', 'from app import parse; assert parse("17")==17')]),
        dict(id='multi-module', category='multi-module', outcome='normalize strips whitespace and lowercases. lookup must normalize both query and keys without changing stored values.',
             files={'normalizer.py': 'def normalize(text):\n    return text\n', 'app.py': 'def lookup(values, key):\n    return values.get(key)\n'}, allowed=['app.py','normalizer.py'],
             solution={'normalizer.py': 'def normalize(text):\n    return text.strip().lower()\n', 'app.py': 'from normalizer import normalize\ndef lookup(values,key):\n    return next((v for k,v in values.items() if normalize(k)==normalize(key)),None)\n'},
             checks=[('acceptance', 'from app import lookup; from normalizer import normalize; assert normalize(" A ")=="a"; assert lookup({" A ":7},"a")==7'),
                     ('regression', 'from app import lookup; assert lookup({"x":9},"x")==9; assert lookup({},"x") is None')]),
        dict(id='security', category='security-fix', outcome='can_read grants access only if authenticated AND owner_id equals user_id. Missing owner or user IDs must deny.',
             files={'app.py': 'def can_read(authenticated, owner_id, user_id):\n    return authenticated or owner_id == user_id\n'}, allowed=['app.py'],
             solution={'app.py': 'def can_read(authenticated, owner_id, user_id):\n    return bool(authenticated and owner_id is not None and user_id is not None and owner_id == user_id)\n'},
             checks=[('acceptance', 'from app import can_read; assert not can_read(False,1,1); assert not can_read(True,1,2); assert not can_read(True,None,None)'),
                     ('regression', 'from app import can_read; assert can_read(True,1,1)')]),
        dict(id='ambiguous', category='ambiguous', outcome='Make usernames case-insensitive. The collision/Unicode policy is intentionally undecided. Do not invent behavior: record the blocking question in QUESTIONS.md and preserve app.py.',
             files={'app.py': 'def key(username):\n    return username\n'}, allowed=['QUESTIONS.md'],
             solution={'QUESTIONS.md': 'BLOCKED: Which Unicode normalization and collision policy is authorized?\n'},
             checks=[('acceptance', 'from pathlib import Path; q=Path("QUESTIONS.md").read_text().lower(); assert "collision" in q and "unicode" in q and "?" in q'),
                     ('regression', 'from app import key; assert key("A")=="A"')])
    ]


def prepare(task_id, arm, output, budget):
    require(arm in ARMS and type(budget) is int and budget >= 1024, 'Invalid arm/budget')
    tasks = {t['id']: t for t in corpus()}
    require(task_id in tasks, 'Unknown benchmark task')
    task = tasks[task_id]
    root = Path(output).resolve()
    require(not root.exists(), 'Benchmark output must be new')
    instructions = task['outcome']
    if arm == 'concise':
        instructions += '\n' + CONCISE
    elif arm == 'automata':
        instructions += '\n' + UNIVERSAL + '\n' + '\n'.join(PHASE_INSTRUCTIONS.values())
        instructions += '\nReturn bounded spec/contract/mold/implementation/review evidence, or checkpoint a missing decision. Self-review is not independent review.'
    context = canonical(dict(task_id=task_id, arm=arm, outcome=instructions,
                             write_paths=task['allowed'], files=task['files'], context_budget_bytes=budget))
    require(len(context.encode()) <= budget, 'Treatment exceeds equal context budget')
    root.mkdir(parents=True)
    candidate = root / 'candidate'
    candidate.mkdir()
    for name, content in task['files'].items():
        (candidate / name).write_text(content, encoding='utf-8')
    (root / 'context.json').write_text(context, encoding='utf-8')
    run = dict(schema_version=1, task_id=task_id, arm=arm, corpus_digest=Controller.digest(corpus()),
               context_bytes=len(context.encode()), budget_bytes=budget,
               instruction_sha256=Controller.digest(instructions), results_pending=True)
    (root / 'run.json').write_text(canonical(run), encoding='utf-8')
    return run


def evaluate(output, telemetry=None):
    root = Path(output).resolve()
    run = read_json(root / 'run.json')
    require(run['schema_version'] == 1 and run['corpus_digest'] == Controller.digest(corpus()), 'Benchmark corpus/version changed')
    task = next(t for t in corpus() if t['id'] == run['task_id'])
    candidate = root / 'candidate'
    # Candidate code cannot change evaluator inputs. Reject links and unexpected
    # paths before running trusted oracle commands in a disposable copy.
    actual = {}
    for path in candidate.rglob('*'):
        require(not path.is_symlink(), 'Benchmark candidate symlink forbidden')
        if path.is_file():
            actual[path.relative_to(candidate).as_posix()] = path.read_text(encoding='utf-8')
    changed = {p for p in set(actual) | set(task['files']) if actual.get(p) != task['files'].get(p)}
    unauthorized = sorted(changed - set(task['allowed']))
    observations = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in actual.items():
            path = Path(tmp) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        for name, code in task['checks']:
            try:
                result = subprocess.run([sys.executable, '-B', '-c', code], cwd=tmp,
                                        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        timeout=10)
                observations.append(dict(name=name, exit_code=result.returncode,
                                         output_sha256=__import__('hashlib').sha256(result.stdout).hexdigest()))
            except subprocess.TimeoutExpired:
                observations.append(dict(name=name, exit_code=None, failure='timeout'))
    correct = not unauthorized and all(o['exit_code'] == 0 for o in observations)
    # Usage is supplied by an approved driver, never guessed from file length.
    if telemetry is not None:
        from .workflow import validate_schema
        validate_schema('benchmark', telemetry)
        require(telemetry['task_id'] == run['task_id'] and telemetry['arm'] == run['arm']
                and telemetry['budget_bytes'] == run['budget_bytes'], 'Telemetry pairing mismatch')
    return dict(schema_version=1, task_id=run['task_id'], arm=run['arm'], correct=correct,
                first_pass_acceptance=(correct and telemetry['attempts'] == 1) if telemetry else None,
                regression_count=sum(o['exit_code'] != 0 for o in observations if o['name'] == 'regression'),
                specification_compliance='oracle-passed' if correct else 'oracle-failed',
                test_quality='not-scored; needs independently reviewed candidate tests',
                unauthorized_changes=unauthorized, observations=observations, context_bytes=run['context_bytes'],
                evaluation_wall_seconds=round(time.monotonic()-started,6),
                telemetry=telemetry, model_results='pending' if telemetry is None else 'driver-supplied, not authenticated')


def add_parser(subparsers):
    parser = subparsers.add_parser('benchmark', help='Prepare/evaluate paired instruction treatments; no model calls')
    commands = parser.add_subparsers(dest='benchmark_action', required=True)
    commands.add_parser('corpus')
    prepare_cmd = commands.add_parser('prepare')
    prepare_cmd.add_argument('--task', required=True)
    prepare_cmd.add_argument('--arm', choices=ARMS, required=True)
    prepare_cmd.add_argument('--output', required=True)
    prepare_cmd.add_argument('--budget', type=int, default=16000)
    evaluate_cmd = commands.add_parser('evaluate')
    evaluate_cmd.add_argument('--output', required=True)
    evaluate_cmd.add_argument('--telemetry')


def run(args):
    from .control import ControlError
    try:
        if args.benchmark_action == 'corpus':
            result = [dict(id=t['id'], category=t['category']) for t in corpus()]
        elif args.benchmark_action == 'prepare':
            result = prepare(args.task, args.arm, args.output, args.budget)
        else:
            result = evaluate(args.output, read_json(args.telemetry) if args.telemetry else None)
        print(canonical(result))
        return 0 if not isinstance(result, dict) or result.get('correct', True) else 1
    except (ControlError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1
