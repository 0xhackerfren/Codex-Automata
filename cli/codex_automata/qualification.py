"""Capability-based eligibility; inventory and measurements are operator inputs."""
from datetime import datetime, timezone
from .control import require, PHASES, nonempty
from .workflow import validate_schema


def eligible(models, request):
    fields = {'phase', 'data_class', 'context_bytes', 'security_sensitive', 'minimum_samples',
              'minimum_acceptance', 'minimum_structured', 'minimum_tool_calls', 'maximum_regression',
              'maximum_measurement_age_days', 'available_ram_gb', 'local_only'}
    require(isinstance(request, dict) and set(request) == fields, 'Unknown or missing qualification requirements')
    require(request['phase'] in PHASES and nonempty(request['data_class']), 'Invalid qualification job')
    for key in ('context_bytes', 'minimum_samples', 'maximum_measurement_age_days'):
        require(type(request[key]) is int and request[key] > 0, 'Positive integer required: ' + key)
    for key in ('minimum_acceptance', 'minimum_structured', 'minimum_tool_calls', 'maximum_regression'):
        require(type(request[key]) in (float, int) and 0 <= request[key] <= 1, 'Invalid threshold: ' + key)
    require(type(request['security_sensitive']) is bool and type(request['local_only']) is bool
            and type(request['available_ram_gb']) in (int, float) and request['available_ram_gb'] >= 0,
            'Explicit runtime capacity and security requirements needed')
    require(isinstance(models, list), 'Model inventory must be a list')
    seen, accepted, rejected = set(), [], []
    for model in models:
        validate_schema('model', model)
        require(set(model['phases']) <= PHASES, 'Unknown model phase')
        require(model['id'] not in seen, 'Duplicate model identity')
        seen.add(model['id'])
        reasons = []
        if not model['approved']:
            reasons.append('provider/model not approved')
        if not model['available']:
            reasons.append('runtime reports unavailable')
        if request['phase'] not in model['phases'] or request['data_class'] not in model['data_classes']:
            reasons.append('phase or data classification not approved')
        if request['local_only'] and model['execution'] != 'local':
            reasons.append('local execution required')
        if model['context_limit_bytes'] < request['context_bytes']:
            reasons.append('insufficient context capacity')
        if model['resources']['ram_gb'] > request['available_ram_gb']:
            reasons.append('insufficient reported RAM')
        if model['sample_count'] < request['minimum_samples']:
            reasons.append('insufficient measured samples')
        for field, threshold in [('coding_acceptance_rate', 'minimum_acceptance'),
                                 ('structured_output_rate', 'minimum_structured'), ('tool_call_rate', 'minimum_tool_calls')]:
            if model[field] is None or model[field] < request[threshold]:
                reasons.append('unqualified ' + field)
        if model['regression_rate'] is None or model['regression_rate'] > request['maximum_regression']:
            reasons.append('unqualified regression rate')
        if request['security_sensitive'] and (not model['security_eligible'] or model['security_sample_count'] < request['minimum_samples']):
            reasons.append('security-sensitive qualification missing')
        try:
            measured = datetime.fromisoformat(model['measurement']['measured_at'].replace('Z', '+00:00'))
            age = (datetime.now(timezone.utc) - measured).total_seconds() / 86400
            if not 0 <= age <= request['maximum_measurement_age_days']:
                reasons.append('measurement stale or future dated')
        except (ValueError, TypeError):
            reasons.append('measurement date invalid')
        (rejected if reasons else accepted).append(dict(id=model['id'], reasons=reasons) if reasons else model['id'])
    return dict(schema_version=1, eligible=accepted, rejected=rejected, recommendation_only=True,
                dispatched=False, trust='operator-supplied approval, measurements and runtime capacity; not authenticated by this API')


def add_parser(subparsers):
    parser = subparsers.add_parser('model', help='Capability-based eligibility without compute scheduling')
    parser.add_argument('action', choices=['eligible'])
    parser.add_argument('--inventory', required=True)
    parser.add_argument('--request', required=True)


def run(args):
    import json
    import sys
    from .isolation import read_json
    from .control import ControlError
    try:
        result = eligible(read_json(args.inventory), read_json(args.request))
        print(json.dumps(result, sort_keys=True))
        return 0 if result['eligible'] else 1
    except (ControlError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1
