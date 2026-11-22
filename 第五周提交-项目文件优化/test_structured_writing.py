import json
from copy import deepcopy

import pytest

from research_agent.structured_writing import atomize, check_claims, check_review, run_pipeline, render


def fixture():
    text='The tested monitor reduced attack success in this benchmark. Collusion showed no measurable protection in the same experiment.'
    evidence='[Evidence E1 | source S1 | kind primary_pdf_excerpt]\n'+text+'\n[Paper: PDF p. 8]'
    atoms=atomize(evidence)
    claims=[dict(claim_id='C1',atom_id='E1.R1',text='在所测基准中，监控降低了攻击成功率。',
        conditions='该基准的被测配置',quote=text.split('. ')[0]+'.',topic='效果',type='finding'),
        dict(claim_id='C2',atom_id='E1.R1',text='同一实验的共谋条件下未见可测保护效果。',
        conditions='被测共谋条件；不作一般不可能性判断',quote=text.split('. ')[1],topic='边界',type='finding')]
    return dict(selected_text=evidence,selected_sources=[{'title':'Test paper','path':'a.md'}]),atoms,claims


def review(claims,verdict='supported'):
    return {'reviews':[dict(claim_id=c['claim_id'],verdict=verdict,reason='依据给定原文及所测条件',evidence_quote=c['quote']) for c in claims]}


def test_unmatched_quote_and_unbound_number_block_claim():
    _,atoms,claims=fixture()
    c=deepcopy(claims[0]);c['quote']='A fabricated long sentence that is nowhere in the evidence.';c['text']='成功率90%'
    issues=check_claims([c],atoms)
    assert any('连续原文' in s for s in issues)
    assert any('90%' in s for s in issues)


def test_pdf_page_locator_never_becomes_an_independent_evidence_atom():
    text='[Evidence E1 | source S1 | kind primary_pdf_excerpt]\nThis is the complete evidence fragment.\n\n[Paper: PDF p. 12]'
    atoms=atomize(text)
    assert len(atoms)==1
    assert atoms[0]['locators']==['[Paper: PDF p. 12]']
    assert 'complete evidence' in atoms[0]['text']


def test_review_cannot_omit_or_duplicate_claims_or_fabricate_quote():
    _,atoms,claims=fixture()
    for data in ({'reviews':[]},{'reviews':review(claims)['reviews']*2}):
        with pytest.raises(ValueError):check_review(data,claims,atoms)
    r=review(claims);r['reviews'][0]['evidence_quote']='fabricated support that is not in this source'
    with pytest.raises(ValueError):check_review(r,claims,atoms)


def test_conflicting_first_pass_is_repaired_before_readiness():
    inputs,_,claims=fixture()
    replies=iter([{'claims':claims},review(claims,'conflict'),{'claims':claims},review(claims)])
    result=run_pipeline(inputs,lambda *_:json.dumps(next(replies)),max_attempts=2)
    assert result['ready_for_drafting']
    assert not result['author_approved']
    assert len(result['history'])==2
    assert result['history'][0]['reviews'][0]['verdict']=='conflict'


def test_failed_review_never_silently_approves_or_renders_rejected_claim():
    inputs,_,claims=fixture()
    replies=iter([{'claims':claims},review(claims,'insufficient')])
    result=run_pipeline(inputs,lambda *_:json.dumps(next(replies)),max_attempts=1)
    assert not result['ready_for_drafting']
    assert result['claims']==[]
    output=render(result,inputs['selected_sources'])
    assert claims[0]['text'] not in output
    assert '尚不可进入整稿生成' in output


def test_note_only_sources_cannot_gain_pdf_readiness():
    inputs,_,claims=fixture();inputs['selected_text']=inputs['selected_text'].replace('primary_pdf_excerpt','paper_note_excerpt')
    replies=iter([{'claims':claims},review(claims)])
    result=run_pipeline(inputs,lambda *_:json.dumps(next(replies)),max_attempts=1)
    assert not result['ready_for_drafting']


def test_selected_quote_ids_are_expanded_from_evidence_without_model_copying():
    inputs,atoms,claims=fixture()
    for c in claims:
        del c['quote'];c['quote_id']=c['atom_id']
    reviews={'reviews':[dict(claim_id=c['claim_id'],verdict='supported',reason='命题与条件均有原文依据',evidence_quote_id=c['atom_id']) for c in claims]}
    replies=iter([{'claims':claims},reviews])
    result=run_pipeline(inputs,lambda *_:json.dumps(next(replies)),max_attempts=1)
    assert result['ready_for_drafting']
    assert all(c['quote']==atoms[0]['text'] for c in result['claims'])


def test_wrong_quote_id_cannot_forge_supported_review():
    _,atoms,claims=fixture()
    data={'reviews':[dict(claim_id=c['claim_id'],verdict='supported',reason='unsupported',evidence_quote_id='E99.R1') for c in claims]}
    with pytest.raises(ValueError):check_review(data,claims,atoms)


def test_each_source_requires_two_supported_claims():
    inputs,_,claims=fixture()
    inputs['selected_sources'].append({'title':'Second','path':'b.md'})
    inputs['selected_text']+='\n[Evidence E2 | source S2 | kind primary_pdf_excerpt]\n'+claims[0]['quote']+'\n[Paper: PDF p. 2]'
    extra=deepcopy(claims[0]);extra.update(claim_id='C3',atom_id='E2.R1')
    claims.append(extra)
    extra=deepcopy(claims[0]);extra.update(claim_id='C4');claims.append(extra)
    replies=iter([{'claims':claims},review(claims)])
    result=run_pipeline(inputs,lambda *_:json.dumps(next(replies)),max_attempts=1)
    assert not result['ready_for_drafting']
