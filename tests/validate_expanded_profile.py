"""Contract and specimen checks, not a live devotional-generation test."""
from pathlib import Path
import json,re
import yaml
R=Path(__file__).resolve().parents[1]
def main():
    e=yaml.safe_load((R/'engine_core.v2.10.4.yaml').read_text())['engine_core']
    x=e['output_profiles']['expanded']
    assert e['writing_constraints']['devotional_length_guidance']['preferred_word_bands']['expanded']==[550,1200]
    target=x['paragraph_target']
    assert target['preferred']==7
    bounds=re.fullmatch(r'\[(\d+)-(\d+)\]',target['acceptable_inclusive_range'])
    assert bounds, target
    lower,upper=map(int,bounds.groups())
    assert lower <= target['preferred'] <= upper
    for count,expected in [(3,False),(4,True),(5,True),(6,True),(7,True),(8,True),(9,False)]:
        assert (lower <= count <= upper)==expected, count
    sources=x['study_pass']['sources_target']
    assert [sources[k] for k in ('minimum','recommended','maximum')]==[5,7,10]
    refs=x['surface_contract']['additional_references']
    assert refs['supporting_scripture']=={'minimum':2,'maximum':3}
    assert refs['other_influential_sources']=={'minimum':2,'maximum':3}
    assert refs['primary_anchor_and_primary_quote_source_excluded']
    assert x['study_pass']['source_diversity_authority']=='engine_core.study_pass.source_diversity_balance'
    assert 'extend' in x['study_pass']['method'] and 'cross-reference' in x['study_pass']['method']
    assert 'second passage' in x['scriptural_development'] and 'third' in x['scriptural_development']
    assert 'extending_the_pool' in e['same_day_seed_reuse']['reuse'][0]
    assert e['output_profiles']['standard']['paragraph_target']=={'preferred':2,'acceptable':[2,3]}
    assert e['writing_constraints']['devotional_length_guidance']['preferred_word_bands']['standard']==[180,270]
    assert e['output_profiles']['condensed']['body_contract']['sentence_count']=={'minimum':4,'maximum':6}
    authority='engine_core.output_profiles.expanded.surface_contract.additional_references'
    render=yaml.safe_load((R/'render.v3.12.2.yaml').read_text())['render']
    assert render['additional_references_rendering']['required_composition']['expanded_override_authority']==authority
    lint=yaml.safe_load((R/'lint.v4.4.2.yaml').read_text())['lint']
    assert lint['expanded_profile_checks']['authority']=='engine_core.output_profiles.expanded'
    assert lint['payoff_anchor_checks']['applies_to']==['standard']
    process=yaml.safe_load((R/'process.v4.2.4.yaml').read_text())['process']
    finalization=process['stage_breakdown']['reference_lineage']
    assert finalization['reference_contract']['expanded_override_authority']==authority
    assert finalization['reference_contract']['derive_eligibility_counts_order_and_deduplication_from_selected_contract']
    assert 'supporting_scripture_contract' not in finalization
    assert 'patristic_contract' not in finalization
    assert render['additional_references_rendering']['source_eligibility_authority']=='engine_core.study_transparency.additional_references'
    assert render['output_targets']['pdf']['additional_references']['body_cited_sources_remain_eligible']
    # Reference cases driven by the actual profile bounds, not a live LLM writer.
    def valid_reference_counts(scriptures,others):
        return all(refs[k]['minimum'] <= n <= refs[k]['maximum'] for k,n in [('supporting_scripture',scriptures),('other_influential_sources',others)])
    cases=[(2,2,True),(3,3,True),(1,3,False),(4,2,False),(3,1,False),(2,4,False)]
    for scriptures,others,expected in cases:
        assert valid_reference_counts(scriptures,others)==expected
    bundle=json.loads((R/'json_bundle.v3.7.1.json').read_text())
    for d in bundle['documents']:
        if d['source_path'] in ('devotional_render_template_v1.1.1.json','devotional_pdf_render_template_v1.0.0.json'):
            assert d['doc']['field_contracts']['additional_references']['expanded_override_authority']==authority
            assert d['doc']['field_contracts']['additional_references']['body_cited_sources_remain_eligible']
    fixture=next(f for f in json.loads((R/'ui_golden_tests.v0.9.9.json').read_text())['ui_golden_render_tests']['fixtures'] if f['id']=='golden_expanded_body_quoted_sources_remain_eligible')
    case=fixture['input']
    assert case['all_quoted_in_body'] and case['all_attributed_in_footnotes'] and case['all_materially_influential']
    assert valid_reference_counts(case['supporting_scriptures'],case['other_influential_sources'])==fixture['expected_shape']['valid']
    assert case['supporting_scriptures']+case['other_influential_sources']==fixture['expected_shape']['additional_reference_count']
    text=(R/'surface_examples.v1.1.0.md').read_text().split('## EX-UI-EXPANDED',1)[1].split('## EX-UI-GENERATED-PRAYER',1)[0]
    body=text.split('There is a particular weariness',1)[1].split('\n[Colossians 3:17',1)[0]
    body='There is a particular weariness'+body
    words=len(re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',body).split())
    paragraphs=len(body.strip().split('\n\n'))
    assert 550<=words<=1200 and paragraphs==7,(words,paragraphs)
    refs=text.split('Additional References',1)[1].strip().splitlines()
    entries=[r for r in refs if r.startswith('- ')]
    assert len(entries)==6 and all('(NIV)' in r for r in entries[:3])
    print(f'PASS: expanded study, reference overrides, same-day continuity, unchanged shorter profiles, and {words}-word/seven-paragraph specimen.')
if __name__=='__main__':main()
