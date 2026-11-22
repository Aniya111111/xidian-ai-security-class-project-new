import json
import hashlib
from pathlib import Path
from unittest.mock import patch
import pytest
from research_agent.claim_evidence import annotate_evidence, build_ledger
from research_agent.obsidian_ideation import save_ideation_report
from revise_obsidian_report import revise

SOURCES = [{'path':'Agent-IFC/10_Papers/a.md','note_sha256':'hash'}]
EVIDENCE = '### A\nSource note: Agent-IFC/10_Papers/a.md\nSource note SHA-256: hash\n\n## 13 批判性分析\n\n可能共变 [Paper: A]\n'

def row(kind='笔记分析',unit='E1'):
    return f'| C1 | 可能共变 | S1 | {unit} [Paper: A] | {kind} | 限定条件 | 讨论 | 待验证 |'

def test_context_and_analysis_are_preserved():
    evidence = annotate_evidence(EVIDENCE,SOURCES)
    assert '[Evidence E1 | source S1 | kind note_analysis]' in evidence
    ledger, issues = build_ledger(row(),evidence,SOURCES)
    assert not issues and not ledger['semantic_verified']
    assert ledger['claims'][0]['semantic_status'] == 'pending_review'
    assert any('可能共变' in unit['excerpt'] for unit in ledger['evidence_units'])

@pytest.mark.parametrize('mapping',[row('原论文结论'),row(unit='E99'),row(unit=''),row()+'\n'+row()])
def test_bad_links_never_mark_verified(mapping):
    ledger, issues = build_ledger(mapping,annotate_evidence(EVIDENCE,SOURCES),SOURCES)
    assert issues and not ledger['semantic_verified']

def test_theme_stays_secondary():
    sources = [{'path':'Agent-IFC/20_Themes/a.md'}]
    evidence = annotate_evidence(EVIDENCE.replace('10_Papers','20_Themes'),sources)
    assert 'kind theme_secondary' in evidence
    assert build_ledger(row('原论文结论'),evidence,sources)[1]

def test_revision_preserves_parent_and_cannot_reuse_review(tmp_path):
    with patch.dict('os.environ',{'OBSIDIAN_VAULT_PATH':str(tmp_path),'OBSIDIAN_RESULT_OUTPUT_DIR':'results'}):
        parent = save_ideation_report(row(),'q',answer=row(),selected_evidence=annotate_evidence(EVIDENCE,SOURCES),selected_sources=SOURCES)
        before = {p.name:p.read_bytes() for p in parent.parent.iterdir()}
        child = revise(parent.parent,row(),'收窄C1')
    assert {p.name:p.read_bytes() for p in parent.parent.iterdir()} == before
    meta = json.loads((child/'manifest.json').read_text(encoding='utf-8'))
    assert meta['revision_of'] == parent.parent.name
    assert meta['author_status'] == 'pending_human_review'
    assert meta['generation_signature'] is None
    assert meta['claim_ids'] == ['C1']
    assert not (child/'author_confirmation.json').exists()
    assert 'claim_evidence.json' in meta['output_sha256']

def test_revision_inherits_verified_pdf_sidecar_and_rejects_tampering(tmp_path):
    with patch.dict('os.environ',{'OBSIDIAN_VAULT_PATH':str(tmp_path),'OBSIDIAN_RESULT_OUTPUT_DIR':'results'}):
        report = save_ideation_report(row(),'q',answer=row(),selected_evidence=annotate_evidence(EVIDENCE,SOURCES),selected_sources=SOURCES)
        parent=report.parent
        attachment=parent/'pdf_verification.json'
        attachment.write_text('{"excerpts":[]}',encoding='utf-8')
        meta=json.loads((parent/'manifest.json').read_text(encoding='utf-8'))
        meta['outputs']['pdf_verification']=attachment.name
        meta['output_sha256'][attachment.name]=hashlib.sha256(attachment.read_bytes()).hexdigest()
        (parent/'manifest.json').write_text(json.dumps(meta),encoding='utf-8')
        child=revise(parent,row(),'保留附件')
        assert (child/attachment.name).read_bytes()==attachment.read_bytes()
        assert not (child/'author_confirmation.json').exists()
        attachment.write_text('tampered',encoding='utf-8')
        with pytest.raises(ValueError,match='PDF'):
            revise(parent,row(),'应拒绝')
