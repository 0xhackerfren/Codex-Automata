import copy
from datetime import datetime, timezone
import unittest
from codex_automata.control import ControlError
from codex_automata.qualification import eligible


class QualificationTests(unittest.TestCase):
    def setUp(self):
        self.model = dict(schema_version=1, id='fixture-local', version='test-only', provider='local-operator',
                          execution='local', approved=True, available=True, data_classes=['private'], phases=['cast'],
                          context_limit_bytes=20000, structured_output_rate=.99, tool_call_rate=.98,
                          coding_acceptance_rate=.9, regression_rate=.01, failure_rate=.1,
                          sample_count=20, security_eligible=False, security_sample_count=0,
                          throughput_tokens_per_second=None, resources=dict(ram_gb=16, accelerator=None),
                          measurement=dict(source='synthetic unit fixture, not a real model result', evidence_sha256='0'*64,
                                           measured_at=datetime.now(timezone.utc).isoformat()))
        self.request = dict(phase='cast', data_class='private', context_bytes=10000, security_sensitive=False,
                            minimum_samples=10, minimum_acceptance=.8, minimum_structured=.95, minimum_tool_calls=.9,
                            maximum_regression=.05, maximum_measurement_age_days=30, available_ram_gb=48, local_only=True)

    def test_eligible_is_not_dispatch(self):
        result = eligible([self.model], self.request)
        self.assertEqual(result['eligible'], ['fixture-local'])
        self.assertFalse(result['dispatched'])

    def test_unapproved_unknown_unavailable_and_security_fail_closed(self):
        for field, value in [('approved', False), ('available', False), ('sample_count', 0),
                             ('coding_acceptance_rate', None), ('execution', 'external'),
                             ('context_limit_bytes', 100), ('regression_rate', .5)]:
            with self.subTest(field=field):
                self.assertFalse(eligible([dict(self.model, **{field: value})], self.request)['eligible'])
        self.assertFalse(eligible([self.model], dict(self.request, security_sensitive=True))['eligible'])

    def test_stale_unknown_version_and_duplicate_model(self):
        model = copy.deepcopy(self.model)
        model['measurement']['measured_at'] = '2000-01-01T00:00:00Z'
        self.assertFalse(eligible([model], self.request)['eligible'])
        for models in ([dict(self.model, schema_version=99)], [self.model, self.model]):
            with self.assertRaises(ControlError):
                eligible(models, self.request)
