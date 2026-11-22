"""Retrieve local PDF text with immutable page/file provenance, never web guesses."""
import hashlib
import re
from pathlib import Path


def primary_fingerprints(inputs, vault):
    """Include actual primary files in cache identity, not just note hashes."""
    root=Path(vault).resolve()
    hashes=[]
    for s in inputs.get('selected_sources',[]):
        note=(root/s['path']).resolve()
        if not note.is_relative_to(root) or not note.is_file():
            raise ValueError('主来源笔记不存在或越界')
        m=re.search(r'^pdf:\s*[\'"]?([^\r\n\'"]+)',note.read_text(encoding='utf-8-sig'),re.M)
        if not m:
            raise ValueError('主来源缺少本地PDF')
        pdf=(root/m[1].strip()).resolve()
        if not pdf.is_relative_to(root):
            raise ValueError('主来源PDF越界')
        hashes.append(hashlib.sha256(pdf.read_bytes()).hexdigest())
    return hashes


def verify_provenance(proof):
    from pypdf import PdfReader
    documents={}
    for item in proof:
        path=item['pdf_path']
        if path not in documents:
            p=Path(path)
            if hashlib.sha256(p.read_bytes()).hexdigest()!=item['pdf_sha256']:
                raise ValueError('PDF已变化，当前主张核验失效')
            documents[path]=PdfReader(p)
        text=documents[path].pages[item['pdf_page']-1].extract_text() or ''
        quote=item['excerpt']
        if hashlib.sha256(quote.encode()).hexdigest()!=item['excerpt_sha256'] or quote not in text:
            raise ValueError('PDF页码或原文摘录不匹配，禁止准入')
    if not proof:
        raise ValueError('缺少PDF溯源记录')


def primary_inputs(inputs, vault, max_chars=22000):
    from pypdf import PdfReader
    from research_agent.claim_evidence import evidence_units
    vault=Path(vault).resolve()
    units=evidence_units(inputs['selected_text'])
    per_source=max_chars//max(1,len(inputs['selected_sources']))
    import copy
    import yaml
    selected_sources=copy.deepcopy(inputs['selected_sources'])
    blocks=[]; proof=[]; index=0
    for n,source in enumerate(selected_sources,1):
        sid=f'S{n}'
        note=(vault/source['path']).resolve(strict=True)
        if not note.is_relative_to(vault):
            raise ValueError('来源笔记超出知识库')
        note_text=note.read_text(encoding='utf-8-sig')
        m=re.search(r'^pdf:\s*[\'"]?([^\r\n\'"]+)',note_text,re.M)
        if not m:
            raise ValueError(f'{sid} 没有本地PDF路径，不能授予原文核验准入')
        pdf=(vault/m[1].strip()).resolve(strict=True)
        if not pdf.is_relative_to(vault):
            raise ValueError('PDF超出知识库')
        texts=[p.extract_text() or '' for p in PdfReader(pdf).pages]
        front=re.match(r'^---\s*\n(.*?)\n---',note_text,re.S)
        metadata=yaml.safe_load(front[1]) if front else {}
        authors=metadata.get('authors') or []
        if isinstance(authors,str):authors=[authors]
        if len(authors)==1 and ',' in authors[0]:authors=[x.strip() for x in authors[0].split(',')]
        year=metadata.get('year')
        if not year:
            date=re.search(r'arXiv:[^\n]+\n?[^\n]{0,50}\b(20\d{2})\b',texts[0])
            if date:year=int(date[1])
        source['bibliographic']={'title':source['title'],'authors':authors,'year':year,
            'arxiv_id':metadata.get('arxiv_id') or None,'doi':metadata.get('doi') or None,
            'source_url':metadata.get('source_url') or None,'local_pdf':str(pdf),
            'metadata_basis':'source_note_and_local_pdf_title_page; DOI not invented'}
        selected='\n'.join(u['excerpt'] for u in units if u['source_id']==sid)
        pages=set()
        for ref in re.finditer(r'PDF p\.\s*(\d+)(?:[–—-](\d+))?',selected):
            lo=int(ref[1]);hi=int(ref[2] or lo)
            pages.update(range(lo,min(hi,lo+3)+1))
        candidates=[]
        for page,t in enumerate(texts,1):
            if 'Guidelines:' in t or re.search(r'\bReferences\b|\bREFERENCES\b',t[:500]):
                continue
            # Prefer results and limitations over citation lists and title pages.
            score=(30 if page in pages else 0)+(0 if page>1 else -25)
            score+=sum(t.lower().count(word)*weight for word,weight in (
                ('average',3),('table iii',12),('table 2',4),('limitations',5),
                ('experiment results',12),('conclusion',5),('collusion',2),
                ('response rates',2),('implicit dependencies',7)))
            if re.search(r'\bREFERENCES\b|^References',t,re.M):score-=20
            # Respect PDF text order. Preserve full chunks including table labels.
            start=0
            while start<len(t):
                end=t.find('\n',min(start+1650,len(t)))
                end=len(t) if end<0 else end+1
                chunk=t[start:end]
                if len(chunk)>=400:
                    local=score+sum(chunk.lower().count(w)*2 for w in ('average','table','baseline','limitations','monotonically','no measurable','compromised','vaccine'))
                    local+=sum(20 for w in ('bidirectional chain topology','implementation limitation','analysis is limited','six configurable','implicit depen') if w in chunk.lower())
                    if 'TABLE III:' in chunk:
                        local+=50
                    candidates.append((local,page,start,chunk))
                start=end
        chosen=[];used=0;page_count={}
        for _,page,start,chunk in sorted(candidates,reverse=True):
            if page_count.get(page,0)>=3 or used+len(chunk)>per_source:
                continue
            chosen.append((page,start,chunk));used+=len(chunk);page_count[page]=page_count.get(page,0)+1
        if not chosen:
            raise ValueError(f'{sid} 没有足够PDF文本，需OCR或人工摘录')
        header=f"Source note: {source['path']}\nSource note SHA-256: {source.get('note_sha256','not recorded')}\n"
        entries=[]
        digest=hashlib.sha256(pdf.read_bytes()).hexdigest()
        for page,start,chunk in sorted(chosen):
            index+=1
            entries.append(f'[Evidence E{index} | source {sid} | kind primary_pdf_excerpt]\n'+chunk+f'\n[Paper: PDF p. {page}]')
            proof.append(dict(evidence_id=f'E{index}',source_id=sid,pdf_path=str(pdf),pdf_sha256=digest,
                pdf_page=page,char_offset=start,excerpt_sha256=hashlib.sha256(chunk.encode()).hexdigest(),excerpt=chunk))
        blocks.append(header+'\n'+'\n\n'.join(entries))
    result=dict(inputs)
    result['selected_sources']=selected_sources
    result['selected_text']='\n\n---\n\n'.join(blocks)
    result['primary_provenance']=proof
    return result
