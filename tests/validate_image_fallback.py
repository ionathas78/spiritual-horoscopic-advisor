"""Validate image fallback contracts and golden cases. Run with Python + PyYAML."""
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def valid_surface(state, surface, source):
    """Check a proposed image surface against the acquisition/display contract."""
    search = state.get('search', 'not_attempted')
    generation = state.get('generation', 'not_attempted')
    skipped = (not state.get('images_enabled', True)
               or state.get('render_target') == 'pdf'
               or state.get('artifact_type') == 'study_guide')
    if skipped:
        return (surface == 'omitted' and source is None
                and search == generation == 'not_attempted')
    if state.get('user_objects') and generation not in {'not_attempted', 'user_declined'}:
        return False
    if state.get('renderer') == 'markdown_image':
        if state.get('native_renderer_available', True) or not state.get('asset_accessible'):
            return False
    failed_search = search in {'no_suitable_result', 'inaccessible', 'tool_unavailable',
                               'failed', 'alt_text_only', 'undisplayable'}
    if surface == 'image':
        if source == 'search':
            return search == 'displayed' and generation == 'not_attempted'
        return (source == 'generated' and failed_search and generation == 'displayed'
                and not state.get('user_objects'))
    if surface == 'italic_image_cue':
        generation_resolved = generation in {'failed', 'tool_unavailable', 'undisplayable'}
        generation_declined = (state.get('user_objects')
                              and generation in {'user_declined', 'not_attempted'})
        return source is None and failed_search and (generation_resolved or generation_declined)
    return False


def main():
    # Parse all stack assets, including untouched ones, to catch accidental corruption.
    yamls = {p.name: yaml.safe_load(p.read_text()) for p in ROOT.glob('*.yaml')}
    jsons = {p.name: json.loads(p.read_text()) for p in ROOT.glob('*.json')}
    policy = yamls['engine_core.v2.10.4.yaml']['engine_core']['image_selection']['acquisition_fallback']
    image_stage = yamls['process.v4.2.4.yaml']['process']['stage_breakdown']['image']
    render = yamls['render.v3.12.2.yaml']['render']
    lint = yamls['lint.v4.4.2.yaml']['lint']
    order = ['search_similar_image', 'generate_image_unless_user_objects', 'italic_image_cue']
    assert policy['order'] == image_stage['acquisition_order'] == order
    assert policy['generation']['skip_when_user_objects']
    assert policy['execution']['skip_entire_chain_when_images_disabled_or_pdf_or_study_guide']
    assert render['image_rendering']['supported_renderer_fallbacks'] == ['native_image_display', 'markdown_image']
    assert render['image_rendering']['prohibit_markdown_images'] is False
    assert render['degraded_fallback']['image_behavior']['emit_single_italic_image_cue_only_after_acquisition_chain_exhausted']
    assert 'generation_attempted_despite_user_objection' in lint['image_fallback_checks']['reject']

    bundle = jsons['json_bundle.v3.7.1.json']
    template = next(d for d in bundle['documents']
                    if d['source_path'] == 'devotional_render_template_v1.1.1.json')
    embedded = template['doc']['special_rules']['image_fallback']
    assert embedded['acquisition_order'] == order
    assert embedded['generation_skip_when_user_objects']
    assert embedded['cue_only_after_search_and_generation_resolved']
    canonical = json.dumps(template['doc'], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    assert template['sha256'] == hashlib.sha256(canonical.encode()).hexdigest()
    for name in jsons['manifest.v4.4.0.json']['files']:
        assert (ROOT / name).is_file(), name

    tests = jsons['ui_golden_tests.v0.9.9.json']['ui_golden_render_tests']
    ids = [f['id'] for f in tests['fixtures']]
    assert len(ids) == len(set(ids)), 'Duplicate golden fixture IDs'
    count = 0
    for fixture in tests['fixtures']:
        if not fixture['id'].startswith('golden_image_fallback_'):
            continue
        expected = fixture['expected_shape']
        result = valid_surface(fixture['input']['image_attempts'],
                               expected['image_surface'], expected['image_source'])
        assert result == expected['valid'], fixture['id']
        count += 1
    forbidden = ['markdown_images_are_forbidden', 'images_must_always_render_as_image_group_entities',
                 'if_images_enabled_then_image_entity_required', 'images_must_use_entity_renderer',
                 'switch_to_italic_cue_without_retry_loop', 'emit_single_italic_image_cue_when_image_entity_fails']
    active = json.dumps(tests) + json.dumps(template['doc'])
    active += ''.join((ROOT / name).read_text() for name in
                     ['process.v4.2.4.yaml', 'render.v3.12.2.yaml', 'lint.v4.4.2.yaml'])
    for rule in forbidden:
        assert rule not in active, f'Obsolete rule still active: {rule}'
    print(f'PASS: {count} image fallback cases; stack syntax, manifest paths, and cross-file contracts.')


if __name__ == '__main__':
    main()
