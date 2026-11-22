"""Production adapter for bounded, tool-free structured literature writing."""
import asyncio
import hashlib
import json
import os
from pathlib import Path

from research_agent.structured_writing import VERSION, run_pipeline, render


def model_call(instructions, content):
    if len(instructions)+len(content)>int(os.getenv('OBSIDIAN_MAX_PROMPT_CHARS','36000')):
        raise ValueError('结构化核验请求超出上下文预算，不能截断证据后继续')
    from research_agent.constant import COMPLETION_MODEL
    from research_agent.inno.core import MetaChain
    from research_agent.inno.types import Agent
    agent=Agent(name='Evidence Claim Auditor',model=COMPLETION_MODEL,instructions=instructions,
        functions=[],tool_choice='none')
    response=asyncio.run(MetaChain().run_async(agent,[{'role':'user','content':content}],
        context_variables={},debug=False,max_turns=1,execute_tools=False))
    if not response.messages or response.messages[-1].get('role')=='error':
        raise RuntimeError('结构化模型调用失败；不授予整稿准入')
    answer=response.messages[-1].get('content','')
    if not isinstance(answer,str) or not answer.strip():
        raise RuntimeError('结构化模型响应为空')
    return answer


def save_result(result, inputs, question, model, signature='', supplemental_reference=''):
    from research_agent.obsidian_ideation import save_ideation_report, audit_writing_output
    from research_agent.obsidian_traceability import process_mapping
    from research_agent.claim_evidence import build_ledger
    if result['ready_for_drafting']:
        from research_agent.primary_sources import verify_provenance
        from research_agent.structured_writing import check_claims,check_review
        problems=check_claims(result['claims'],result['atoms'])
        if problems or not result['history']:
            raise ValueError('准入主张结构或审核记录无效')
        last=result['history'][-1]
        expected={c['claim_id']:c for c in last.get('claims',[])}
        if any(expected.get(c['claim_id'])!=c for c in result['claims']):
            raise ValueError('主张在审核后被修改，禁止准入')
        accepted_ids={c['claim_id'] for c in result['claims']}
        reviewed=check_review({'reviews':[r for r in last.get('reviews',[]) if r['claim_id'] in accepted_ids]},result['claims'],result['atoms'])
        if any(r['verdict']!='supported' for r in reviewed):
            raise ValueError('有未获支持的主张，禁止准入')
        registry={a['atom_id']:a for a in result['atoms']}
        for i in range(1,len(inputs['selected_sources'])+1):
            if sum(registry[c['atom_id']]['source_id']==f'S{i}' for c in result['claims'])<2:
                raise ValueError('来源覆盖不足，禁止准入')
        proof_ids={p['evidence_id'] for p in inputs.get('primary_provenance',[])}
        if any(registry[c['atom_id']]['kind']!='primary_pdf_excerpt'
               or registry[c['atom_id']]['evidence_id'] not in proof_ids for c in result['claims']):
            raise ValueError('主张未绑定PDF溯源记录')
        verify_provenance(inputs.get('primary_provenance',[]))
    answer=render(result,inputs['selected_sources'])
    answer,corrections,issues=process_mapping(answer,inputs['selected_text'],inputs['selected_sources'])
    _,links=build_ledger(answer,inputs['selected_text'],inputs['selected_sources'])
    issues+=links+audit_writing_output(answer,inputs['selected_text'],inputs['selected_sources'],output_kind='synthesis')
    if issues:
        result['ready_for_drafting']=False
        result['blocking_issues'].extend(issues)
        answer=render(result,inputs['selected_sources'])
        answer,corrections,_=process_mapping(answer,inputs['selected_text'],inputs['selected_sources'])
    if not result['ready_for_drafting']:
        issues.append('逐条证据核验或来源覆盖尚未通过，禁止进入整稿生成')
    report=save_ideation_report(answer,question,supplemental_reference,answer=answer,
        source_path=str(inputs['source_path']),source_hash=inputs['source_hash'],model=model,
        audit_warnings=list(dict.fromkeys(issues)),generation_key=signature,
        selected_evidence=inputs['selected_text'],selected_sources=inputs['selected_sources'],
        raw_answer=answer,path_corrections=corrections)
    root=report.parent
    proof=inputs.get('primary_provenance',[])
    report_hash=hashlib.sha256(report.read_bytes()).hexdigest()
    readiness=dict(version=VERSION,ready_for_drafting=result['ready_for_drafting'],
        scope=result.get('scope','evidence_bounded_literature_review_draft'),author_approved=False,
        report_sha256=report_hash,claim_count=len(result['claims']),
        blocking_issues=result['blocking_issues'],review_method='quoted_primary_evidence_and_separate_model_review',
        next_action='draft_from_verified_claims' if result['ready_for_drafting'] else 'repair_evidence_or_claims')
    attachments={'structured_review.json':result,'draft_readiness.json':readiness,'primary_provenance.json':proof}
    mpath=root/'manifest.json';meta=json.loads(mpath.read_text(encoding='utf-8'))
    for name,data in attachments.items():
        p=root/name;p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        meta['outputs'][name.removesuffix('.json')]=name
        meta['output_sha256'][name]=hashlib.sha256(p.read_bytes()).hexdigest()
    meta['structured_writing_version']=VERSION
    meta['ready_for_drafting']=readiness['ready_for_drafting']
    meta['next_action']=readiness['next_action']
    # Record machine review honestly; the author remains pending. Existing
    # chapter mode checks the reviewer's stated scope instead of inventing approval.
    if result['ready_for_drafting']:
        from research_agent.verified_claims import record_review
        catalog_path=root/'verified_claims.json'
        catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
        last=result['history'][-1]['reviews']
        for claim in result['claims']:
            review=next(r for r in last if r['claim_id']==claim['claim_id'])
            record_review(catalog,claim['claim_id'],'supported','independent_model_review',review['reason'],
                '本地PDF逐字摘录及文件1起始页码的机器核验；不是人工认可，不代表全文逐页视觉审查或投稿就绪')
        catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
        meta['output_sha256']['verified_claims.json']=hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    mpath.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def validate_readiness(root):
    """Recheck saved files and live PDFs before using a ready packet for chapters."""
    from research_agent.primary_sources import verify_provenance
    root=Path(root).resolve(strict=True)
    meta=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    ready=json.loads((root/'draft_readiness.json').read_text(encoding='utf-8'))
    if not ready.get('ready_for_drafting') or not meta.get('ready_for_drafting'):
        raise ValueError('本版本未通过整稿准入')
    for key in ('report','structured_review','primary_provenance','draft_readiness','verified_claims'):
        name=meta['outputs'].get(key)
        if not name or Path(name).name!=name:
            raise ValueError('核验附件缺失或路径异常')
        p=root/name
        if hashlib.sha256(p.read_bytes()).hexdigest()!=meta['output_sha256'].get(name):
            raise ValueError('核验文件已变化，需重新核验')
    if ready['report_sha256']!=meta['output_sha256']['report.md']:
        raise ValueError('报告版本与准入版本不一致')
    proof=json.loads((root/'primary_provenance.json').read_text(encoding='utf-8'))
    verify_provenance(proof)
    return ready


def export_draft_inputs(root):
    from research_agent.verified_claims import chapter_material
    root=Path(root)
    ready=validate_readiness(root)
    catalog=json.loads((root/'verified_claims.json').read_text(encoding='utf-8'))
    ids=[c['claim_id'] for c in catalog['claims']]
    material=chapter_material(catalog,ids,catalog['bundle_sha256'])
    instruction=('请基于以下已核验材料起草中文文献综述整稿，定位为草稿。'
        '结构为摘要、引言、文献范围、机制与防御比较、协作与效用、局限与研究问题、结论、参考文献。'
        '每段标注C/E编号，引用表保留S编号、原文PDF页码。不要增添材料外的数字、实验证据或创新性判断。'
        '必须区分主动与被动疫苗、individual与multi CaMeL、各基准总体损失与增量。'
        '固定术语：潜隐提示、问题解决率、不透明数据通道。研究问题另列待验证，不写成结果。'
        '整稿生成后仍需逐段核验，不能自行宣布作者认可或投稿就绪。\n\n')
    prompt=instruction+material
    budget=int(os.getenv('OBSIDIAN_MAX_PROMPT_CHARS','36000'))
    if len(prompt)>budget:
        raise ValueError(f'整稿输入{len(prompt)}字符超预算，需按章拆分而非截断证据')
    files={'chapter_input.md':prompt,
        'manuscript_plan.json':json.dumps({'claim_ids':ids,'scope':ready['scope'],
            'catalog':str(root/'verified_claims.json'),'prompt_chars':len(prompt),
            'requires_post_generation_paragraph_review':True,'author_approved':False},ensure_ascii=False,indent=2)}
    meta_path=root/'manifest.json';meta=json.loads(meta_path.read_text(encoding='utf-8'))
    for name,content in files.items():
        p=root/name
        if p.exists() and p.read_text(encoding='utf-8')!=content:
            raise ValueError('已导出的整稿任务包内容不一致，需创建新版本')
        if not p.exists():p.write_text(content,encoding='utf-8')
        meta['outputs'][name.split('.')[0]]=name
        meta['output_sha256'][name]=hashlib.sha256(p.read_bytes()).hexdigest()
    meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    return dict(prompt_path=str(root/'chapter_input.md'),prompt_chars=len(prompt),claim_count=len(ids))


def run_structured(inputs, question, reference, model, signature):
    from research_agent.primary_sources import primary_inputs
    prepared=primary_inputs(inputs,os.environ['OBSIDIAN_VAULT_PATH'])
    prepared['question']=question
    result=run_pipeline(prepared,model_call,max_attempts=3)
    path=save_result(result,prepared,question,model,signature,reference)
    if result['ready_for_drafting']:
        export_draft_inputs(path.parent)
    state='可进入有证据约束的综述整稿起草（作者待确认）' if result['ready_for_drafting'] else '证据核验未通过，暂不进入整稿'
    return f'结果已保存：{path.parent}\n状态：{state}\n\n'+path.read_text(encoding='utf-8')
