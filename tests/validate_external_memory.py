"""Validate prompt-stack wiring and a temporary local memory fixture, not an LLM run."""
import hashlib
import json
from pathlib import Path
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    engine = yaml.safe_load((ROOT / 'engine_core.v2.10.4.yaml').read_text())
    process = yaml.safe_load((ROOT / 'process.v4.2.4.yaml').read_text())['process']
    prefs = yaml.safe_load((ROOT / 'preferences.v3.3.0.yaml').read_text())
    policy = engine['engine_core']['external_memory']
    steps = process['pipeline']
    assert steps.index('memory_load_context') < steps.index('seed_resolve_daily_reuse') < steps.index('horoscope_identify_daily_issue')
    reuse = engine['engine_core']['same_day_seed_reuse']
    assert process['stage_breakdown']['seed_resolution']['authority'] == 'engine_core.same_day_seed_reuse'
    assert 'new_subject' in reuse['default']
    assert engine['engine_core']['source_cycling']['cross_run_review']['applies_when'] == 'selecting_a_new_seed'
    assert engine['engine_core']['freshness_controls']['applies_when'] == 'selecting_a_new_seed'
    assert steps.index('memory_update_context') > steps.index('render_create_output')
    for stage in ('memory_load', 'memory_update'):
        node = engine
        for key in process['stage_breakdown'][stage]['authority'].split('.'):
            node = node[key]
        assert node == policy
    assert prefs['reader_contract_preferences']['external_memory']['location']['default'] is None
    assert policy['write_only_with'] == 'user_authorized_write_access'
    assert 'current_explicit_request_then' in policy['precedence']
    seed_policy = policy['seed_history']
    assert seed_policy['retain_latest_seeds'] == 5
    assert 'stable_across_same_day_reuse_retries_and_repairs' in seed_policy['run_identity']
    assert any('tarot_card' in field for field in seed_policy['seed_fields'])
    assert any('primary_quote' in field for field in seed_policy['seed_fields'])
    assert any('supporting_authors' in field for field in seed_policy['seed_fields'])
    assert engine['engine_core']['source_cycling']['cross_run_review']['history_authority'] == 'engine_core.external_memory.seed_history'
    assert engine['engine_core']['freshness_controls']['daily_theme_freshness']['cross_run_history_authority'] == 'engine_core.external_memory.seed_history'
    assert any('unverified' in rule for rule in policy['unavailable'])
    assert any('without_confirmation' in rule for rule in policy['unavailable'])
    assert any('other_readers' in rule for rule in policy['maintenance'])

    # Real file I/O exercises a user-chosen JSON-shaped memory space. These
    # fixtures supply relevant history and permissions without a service adapter.
    with tempfile.TemporaryDirectory(prefix='devotional-memory-') as folder:
        path = Path(folder) / 'memory.json'
        memory = {'readers': {
            'reader_a': {'preferences': {'content_length': 'standard'},
                         'history': [{'id': 'previous', 'date': '2026-10-19',
                                      'theme_cluster': 'gratitude', 'author': 'Corrie ten Boom'}]},
            'reader_b': {'preferences': {'content_length': 'expanded'}, 'history': []}},
            'unrelated_notes': 'Preserve me.'}
        path.write_text(json.dumps(memory))
        loaded = json.loads(path.read_text())
        reader = loaded['readers']['reader_a']
        request = {'content_length': 'condensed'}
        resolved = reader['preferences'] | request
        assert resolved['content_length'] == 'condensed'
        assert reader['history'][0]['theme_cluster'] == 'gratitude'
        untouched = loaded['readers']['reader_b'].copy()
        record = {'id': 'run-2026-10-20-a', 'date': '2026-10-20',
                  'thesis': 'Attend to the task within reach.', 'theme_cluster': 'attention'}
        # Upsert the same completed run twice, representing a retry.
        for _ in range(2):
            reader['history'] = [v for v in reader['history'] if v['id'] != record['id']] + [record]
            path.write_text(json.dumps(loaded))
        saved = json.loads(path.read_text())
        assert len(saved['readers']['reader_a']['history']) == 2
        assert saved['readers']['reader_b'] == untouched
        assert saved['unrelated_notes'] == 'Preserve me.'
        # Explicit new subjects on the same date must survive as distinct seeds.
        for run in range(7):
            next_seed = {'id': f'run-{run}', 'date': '2026-10-20', 'theme_cluster': f'new-subject-{run}'}
            reader['history'] = (reader['history'] + [next_seed])[-seed_policy['retain_latest_seeds']:]
        path.write_text(json.dumps(loaded))
        saved = json.loads(path.read_text())
        assert [v['id'] for v in saved['readers']['reader_a']['history']] == ['run-2', 'run-3', 'run-4', 'run-5', 'run-6']
        assert saved['readers']['reader_b'] == untouched
        assert saved['unrelated_notes'] == 'Preserve me.'


    bundle = json.loads((ROOT / 'json_bundle.v3.7.1.json').read_text())
    for doc in bundle['documents']:
        if 'doc' in doc:
            canonical = json.dumps(doc['doc'], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            assert doc['sha256'] == hashlib.sha256(canonical.encode()).hexdigest()
    print('PASS: memory stage wiring, authority, missing-history safeguards, and local fixture read/update/retry and same-day rolling-seed checks.')


if __name__ == '__main__':
    main()
