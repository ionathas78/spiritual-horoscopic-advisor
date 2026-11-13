"""Check contract alignment; these checks do not execute an LLM writer."""
from pathlib import Path
import json
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    docs={p.name:yaml.safe_load(p.read_text()) for p in ROOT.glob('*.yaml')}
    policy=docs['engine_core.v2.10.4.yaml']['engine_core']['writing_constraints']['body_quote_policy']
    authority='engine_core.writing_constraints.body_quote_policy'
    forbidden_eligibility_rules=('candidate_source_is_not_already_reserved_only_as_body_quote_footnote','source_is_not_duplicate_of_body_quote_footnote_unless_it_had_separate_nonquotation_influence','include_footnote_citations: false')
    for name in ('process.v4.2.4.yaml','render.v3.12.2.yaml'):
        text=(ROOT/name).read_text()
        assert not any(rule in text for rule in forbidden_eligibility_rules),name
    assert 'primary anchor' in policy['scripture']['default']
    assert 'expanded' in policy['scripture']['default']
    assert 'condensed (short) and standard' in policy['scripture']['compact_profiles']
    assert 'fully legitimate' in policy['scripture']['compact_profiles']
    assert 'paraphrase' in policy['scripture']['rhythm_exception']
    assert 'faithful attributed paraphrase' in policy['other_sources']['requirement']
    assert 'qualifications' in policy['selection']
    assert 'inline or in a footer' in policy['attribution']
    assert 'must not be counted' in policy['primary_anchor']['supporting_reference_count']
    assert docs['process.v4.2.4.yaml']['process']['stage_breakdown']['write']['body_quote_rules']['authority']==authority
    render=docs['render.v3.12.2.yaml']['render']
    assert render['body_quote_rendering']['authority']==authority
    assert render['output_targets']['pdf']['devotional']['direct_body_quote_citation_mode']=='inline_or_footer'
    assert docs['lint.v4.4.2.yaml']['lint']['body_quote_checks']['authority']==authority
    for path in ROOT.iterdir():
        if path.suffix not in ('.yaml','.json'):continue
        text=path.read_text()
        for obsolete in ('forbid_direct_quote_of_primary_scripture_reference','inline_attribution_forbidden','primary_scripture_reference_must_appear_exactly_once_in_surface_output','forbid_primary_scripture_equivalence_in_footnotes','must_not_contain_primary_anchor_reference','no_equivalent_primary_range_in_body_or_footnotes','overlapping_primary_ranges_must_not_appear_as_secondary_citations','forbid_overlapping_primary_range_as_secondary_reference'):
            assert obsolete not in text,(path.name,obsolete)
    bundle=json.loads((ROOT/'json_bundle.v3.7.1.json').read_text())
    pdf=next(d['doc'] for d in bundle['documents'] if d['source_path']=='devotional_pdf_render_template_v1.0.0.json')
    assert pdf['field_contracts']['devotional_body']['inline_attribution_allowed']
    assert pdf['field_contracts']['footnotes']['primary_anchor_body_attribution_allowed']
    checks=docs['process.v4.2.4.yaml']['process']['stage_breakdown']['lint']['render_surface_lock']['required_checks']
    assert 'primary_anchor_slot_and_supporting_reference_deduplication_verified' in checks
    assert pdf['field_contracts']['additional_references']['include_primary_anchor'] is False
    ui=next(d['doc'] for d in bundle['documents'] if d['source_path']=='devotional_render_template_v1.1.1.json')
    assert ui['lint']['rules']['primary_and_overlapping_ranges_excluded_from_additional_references']
    fixtures=json.loads((ROOT/'ui_golden_tests.v0.9.9.json').read_text())['ui_golden_render_tests']['fixtures']
    cases={f['id']:f for f in fixtures}
    assert cases['golden_scripture_paraphrase_preserves_rhythm']['expected_shape']['valid']
    assert not cases['regression_author_name_without_supporting_material']['expected_shape']['valid']
    print('PASS: source policy ownership, body/primary quotations, paraphrase exception, attribution, and obsolete-rule removal.')

if __name__=='__main__':main()
