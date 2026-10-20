"""Contract and routing-reference checks; this does not run an LLM generator."""
import hashlib
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]


def values(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from values(child)
    elif isinstance(value, list):
        for child in value:
            yield from values(child)
    else:
        yield value


def main():
    yamls = {p.name: yaml.safe_load(p.read_text()) for p in ROOT.glob('*.yaml')}
    jsons = {p.name: json.loads(p.read_text()) for p in ROOT.glob('*.json')}
    roots = {}
    for doc in yamls.values():
        roots.update(doc)
    roots['preferences'] = yamls['preferences.v3.3.0.yaml']
    for name, doc in (yamls | jsons).items():
        for value in values(doc):
            if isinstance(value, str) and not value.endswith(('.yaml', '.json', '.md')) and re.fullmatch(r'(engine_core|preferences|render)\.[A-Za-z0-9_.]+', value):
                node = roots
                for key in value.split('.'):
                    assert key in node, (name, value)
                    node = node[key]
    manifest = jsons['manifest.v4.4.0.json']
    for name in manifest['files'] + manifest['updated_files']:
        assert (ROOT / name).is_file(), name
    for name in ('render.v3.12.2.yaml', 'lint.v4.4.2.yaml'):
        doc = yamls[name]
        key = 'render' if name.startswith('render') else 'lint'
        examples = doc[key]['normative_examples' if key == 'render' else 'normative_example_checks']
        assert examples['source_file'] in manifest['files']
    process = roots['process']
    stage_aliases = {v['alias'] for v in process['stage_breakdown'].values()}
    assert set(process['pipeline']) <= stage_aliases
    engine = roots['engine_core']
    assert engine['problem_selection']['explicit_subject']['preserve']
    assert engine['source_cycling']['cross_run_review']['applies_when'] == 'selecting_a_new_seed'
    freshness = roots['lint']['freshness_checks']['daily_theme_freshness']
    assert freshness['derive_checks_and_failure_actions_from_authority']
    assert freshness['applies_when'] == 'selecting_a_new_seed'
    assert engine['freshness_controls']['freshness_entropy']['applies_when'] == 'selecting_a_new_seed'
    assert roots['render']['additional_references_rendering']['omit_when_empty'] is False
    fields = engine['external_memory']['seed_history']['seed_fields']
    assert any('local_civil_date_and_timezone' in field for field in fields)
    assert any('compact_study_brief' in field for field in fields)

    bundle = jsons['json_bundle.v3.7.1.json']
    docs = {d['source_path']: d['doc'] for d in bundle['documents'] if 'doc' in d}
    for entry in bundle['documents']:
        if 'doc' in entry:
            canonical = json.dumps(entry['doc'], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            assert entry['sha256'] == hashlib.sha256(canonical.encode()).hexdigest()
    ui = docs['devotional_render_template_v1.1.1.json']['field_contracts']
    assert docs['user_prefs_devotional_v1.1.2.json']['formatting']['show_date']['default_by_render_target'] == {'ui': False, 'pdf': True}
    assert ui['date']['render']['enabled'] is False
    assert ui['week_theme']['render']['enabled'] is False
    assert ui['additional_references']['behavior']['allow_empty'] is False
    pdf = docs['devotional_pdf_render_template_v1.0.0.json']['field_contracts']
    assert pdf['anchor_scripture']['expanded_text_by_content_length']['condensed'] is False

    # A small decision-table reference model exercises the boundary cases for
    # prompt routing. It is deliberately not presented as the production engine.
    cases = jsons['ui_golden_tests.v0.9.9.json']['seed_routing_reference_cases']
    for case in cases['fixtures']:
        request, seed = case['request'], case.get('seed')
        match = (seed is not None and seed['reader_scope'] == request['reader_scope']
                 and seed['local_date'] == request['local_date'])
        decision = 'reuse' if match and not request.get('new_subject', False) else 'new_seed'
        assert decision == case['expected_route'], case['id']
    print(f'PASS: stack paths, stage aliases, hashes, UI/PDF contracts, and {len(cases["fixtures"])} routing-reference cases.')


if __name__ == '__main__':
    main()
