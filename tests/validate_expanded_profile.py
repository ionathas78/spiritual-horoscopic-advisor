"""Contract and specimen checks, not a live devotional-generation test."""
from pathlib import Path
import json,re
import yaml
R=Path(__file__).resolve().parents[1]
def main():
    e=yaml.safe_load((R/'engine_core.v2.10.4.yaml').read_text())['engine_core']
    x=e['output_profiles']['expanded']
    assert e['writing_constraints']['devotional_length_guidance']['preferred_word_bands']['expanded']==[550,1200]
    assert x['paragraph_target']=={'preferred':7,'acceptable':[4,8]}
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
    bundle=json.loads((R/'json_bundle.v3.7.1.json').read_text())
    for d in bundle['documents']:
        if d['source_path'] in ('devotional_render_template_v1.1.1.json','devotional_pdf_render_template_v1.0.0.json'):
            assert d['doc']['field_contracts']['additional_references']['expanded_override_authority']==authority
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
