"""Validate image fallback contracts and golden cases. Run with Python + PyYAML."""
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def valid_composer_behavior(state, surface, source):
    """Check composer behavior independently of delivered-product validation."""
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


def valid_delivery(surface, supported_renderers):
    """Validate the delivered product without access to acquisition history."""
    excluded = (surface.get('render_target') == 'pdf'
                or surface.get('artifact_type') == 'study_guide'
                or not surface.get('images_enabled', True))
    if excluded:
        return surface['type'] == 'omitted'
    if surface['type'] == 'displayed_image':
        return (surface.get('renderer') in supported_renderers
                and surface.get('asset_displays') is True)
    if surface['type'] == 'italic_image_cue':
        return (surface.get('from_composer') is True and surface.get('italic') is True
                and surface.get('count') == 1)
    return False


def main():
    yamls = {p.name: yaml.safe_load(p.read_text()) for p in ROOT.glob('*.yaml')}
    jsons = {p.name: json.loads(p.read_text()) for p in ROOT.glob('*.json')}
    policy = yamls['engine_core.v2.10.4.yaml']['engine_core']['image_selection']['acquisition_fallback']
    image_stage = yamls['process.v4.2.4.yaml']['process']['stage_breakdown']['image']
    render = yamls['render.v3.12.2.yaml']['render']
    lint = yamls['lint.v4.4.2.yaml']['lint']
    assert policy['owner'] == image_stage['owner'] == 'image_composer'
    assert policy['sole_authority_for_acquisition_and_fallback_precedence']
    assert policy['generation']['skip_when_user_objects']
    assert 'acquisition_order' not in image_stage
    assert render['image_rendering']['assembly']['on_delivery_failure'] == 'return_failure_details_to_image_composer'
    assert render['image_rendering']['assembly']['acquisition_or_fallback_selection'] == 'forbidden'
    assert lint['image_delivery_checks']['inspect'] == 'delivered_surface_only'
    assert lint['image_delivery_checks']['acquisition_history_required'] is False
    assert 'image_fallback_checks' not in lint

    template = next(d for d in jsons['json_bundle.v3.7.1.json']['documents']
                    if d['source_path'] == 'devotional_render_template_v1.1.1.json')
    assert 'image_fallback' not in template['doc']['special_rules']
    assert template['doc']['special_rules']['image_delivery']['inspect'] == 'delivered_surface_only'
    canonical = json.dumps(template['doc'], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    assert template['sha256'] == hashlib.sha256(canonical.encode()).hexdigest()
    for name in jsons['manifest.v4.4.0.json']['files']:
        assert (ROOT / name).is_file(), name

    golden = jsons['ui_golden_tests.v0.9.9.json']
    composer_count = 0
    for fixture in golden['image_composer_behavior_tests']['fixtures']:
        expected = fixture['expected_shape']
        actual = valid_composer_behavior(fixture['input']['image_attempts'],
                                         expected['image_surface'], expected['image_source'])
        assert actual == expected['valid'], fixture['id']
        composer_count += 1
    fixtures = golden['ui_golden_render_tests']['fixtures']
    assert len({f['id'] for f in fixtures}) == len(fixtures)
    delivery_count = 0
    for fixture in fixtures:
        assert 'image_attempts' not in fixture.get('input', {})
        if not fixture['id'].startswith('golden_image_delivery_'):
            continue
        actual = valid_delivery(fixture['input']['image_surface'],
                                render['image_rendering']['supported_renderers'])
        assert actual == fixture['expected_shape']['valid'], fixture['id']
        delivery_count += 1
    checker_text = json.dumps(lint) + json.dumps(render) + json.dumps(template['doc'])
    checker_text += json.dumps(golden['ui_golden_render_tests'])
    for acquisition_detail in ['search_similar_image', 'generate_image_unless_user_objects',
                               'acquisition_order', 'cue_requires_exhausted_acquisition_chain',
                               'cue_only_after_search_and_generation_resolved']:
        assert acquisition_detail not in checker_text, acquisition_detail
    print(f'PASS: {composer_count} composer cases, {delivery_count} delivery cases; ownership and stack contracts.')


if __name__ == '__main__':
    main()
