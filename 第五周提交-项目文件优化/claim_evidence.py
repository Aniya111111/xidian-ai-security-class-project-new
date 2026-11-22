"""Deterministic evidence ledger. Links are not semantic verification."""
import re
from research_agent.obsidian_traceability import split_mapping_row, ROW

VERSION = 'claim-evidence-v5.1'

def annotate_evidence(text, sources):
    lines, source, section, index = [], '', '', 0
    paths = {s['path']:f'S{i}' for i,s in enumerate(sources,1)}
    theme = False
    for paragraph in re.split(r'(\n\s*\n)', text):
        if not paragraph.strip():
            lines.append(paragraph); continue
        found = re.search(r'^Source note: (.+)$', paragraph, re.M)
        if found:
            path = found[1].strip(); source = paths.get(path, '')
            theme = '/20_Themes/' in path.replace('\\','/')
            section = ''
            lines.append(paragraph); continue
        if re.match(r'^#{2,4} ', paragraph):
            section = paragraph.splitlines()[0]
        if not source or paragraph.strip() == '---':
            lines.append(paragraph); continue
        # Keep section context; headings and short transition labels are not evidence.
        if not substantive(paragraph.strip()):
            lines.append(paragraph)
            continue
        # Keep section context, but never assign an evidence ID to a bare heading.
        if not re.sub(r'^#{1,6}[^\n]*(?:\n|$)', '', paragraph.strip(), flags=re.M).strip():
            lines.append(paragraph)
            continue
        index += 1
        kind = 'theme_secondary' if theme else 'hypothesis' if '[Hypothesis]' in paragraph or '研究想法' in section else 'note_analysis' if ('批判' in section or '[Analysis]' in paragraph) else 'paper_note_excerpt'
        lines.append(f'[Evidence E{index} | source {source} | kind {kind}]\n' + paragraph)
    return ''.join(lines)

def clean_excerpt(text):
    """Remove extraction scaffolding, never invent or rewrite evidence facts."""
    text = re.split(r'\n\s*---\s*\n|\nSource note:', text, maxsplit=1)[0].strip()
    lines, seen_headers = [], set()
    for line in text.splitlines():
        # A damaged matrix may repeat its row identifier halfway through a line.
        # Keep the complete later row only when its prefix repeats verbatim.
        row = re.match(r'^\|\s*((?:S\d+:)?C\d+)\s*\|', line)
        if row:
            repeats = list(re.finditer(r'\|\s*' + re.escape(row[1]) + r'\s*\|', line))
            if len(repeats) > 1:
                later = line[repeats[-1].start():]
                prefix = line[:repeats[-1].start()]
                if later.startswith(prefix) and later.count('|') >= 10:
                    line = later
        if line.startswith('| 核查-C') and '| 编号 | 实验 |' in line:
            continue  # corrupt duplicated matrix prefix; complete row follows
        if line.startswith('| 编号 | 实验 |') or re.match(r'^\|\s*---', line):
            if line in seen_headers:
                continue
            seen_headers.add(line)
        lines.append(line)
    while lines and (not lines[-1].strip() or re.match(r'^#{1,6} ', lines[-1])):
        lines.pop()
    return '\n'.join(lines).strip()


def evidence_cautions(excerpt):
    """Quarantine contradictory note interpretations without rewriting quotations."""
    cautions = []
    if '变体' in excerpt and re.search(r'未统计|未计数', excerpt):
        cautions.append('消息改写实例不等于变体数量统计；不得据此断言数量显著更多，变体总量未知。')
    if 'no CaMeL → multi-CaMeL' in excerpt and '增量' in excerpt:
        cautions.append('图示 no CaMeL → multi-CaMeL 是总体差值；individual → multi 的增量须有独立比较，不可互换。各基准的样本数和差值分别报告。')
    if '90.0%' in excerpt and '主动疫苗' in excerpt:
        cautions.append('90.0% 仅归属主动疫苗；被动疫苗单列。均值提升不等于统计显著，模型差异不证明规模、年份或供应商的因果作用。')
    return cautions


def quantity_in_excerpt(quantity, excerpt):
    """Allow percentage-point notation for explicitly labelled success-rate deltas.

    This confirms a value occurs in the bound text; it does not validate which
    configuration it belongs to or replace semantic review.
    """
    normalized = re.sub(r'\s+', '', quantity)
    if normalized in re.sub(r'\s+', '', excerpt):
        return True
    match = re.fullmatch(r'(\d+(?:\.\d+)?)(?:pp|个百分点)', normalized)
    if not match:
        return False
    if re.search(r'(?<![\d.])'+re.escape(match[1])+r'\s*(?:pp\b|pts\b|percentage\s+points\b|个百分点)',excerpt,re.I):
        return True
    if re.search(r'percentage[\s-]*point\s+change',excerpt,re.I) and re.search(
            r'[−-]'+re.escape(match[1])+r'\s*%',excerpt):
        return True
    for line in excerpt.splitlines():
        if '任务成功率' in line and ('Δ' in line or r'\Delta' in line) and ('→' in line or '差值' in line):
            if re.search(r'(?<![\d.])' + re.escape(match[1]) + r'(?![\d.])', line):
                return True
    return False


def substantive(text):
    body = re.sub(r'^#{1,6}[^\n]*(?:\n|$)', '', text, flags=re.M).strip()
    return bool(body) and not (len(body) < 50 and body.endswith(('：', ':')) and '[Paper:' not in body)


def qualify_note_claims(excerpt, source_id):
    # Paper locators are immutable source strings, not local claim labels.
    parts = re.split(r'(\[Paper:[^\]\r\n]*\])', excerpt)
    return ''.join(part if i % 2 else re.sub(
        r'(?<![:\w-])C(\d+)\b', lambda m: f'{source_id}:C{m[1]}', part)
        for i, part in enumerate(parts))


def evidence_units(evidence):
    markers = list(re.finditer(r'^\[Evidence (E\d+) \| source (S\d+) \| kind (\w+)\]\n', evidence, re.M))
    return [{'id':m[1], 'source_id':m[2], 'kind':m[3],
             'excerpt':clean_excerpt(evidence[m.end():markers[i+1].start() if i+1<len(markers) else len(evidence)])}
            for i,m in enumerate(markers)]


def clean_evidence(evidence, sources):
    """Preserve existing E IDs in revisions; discard non-evidence transition units."""
    blocks, changes = [], []
    if not sources:
        return evidence, changes
    units = evidence_units(evidence)
    raw_markers = list(re.finditer(r'^\[Evidence (E\d+) \| source S\d+ \| kind \w+\]\n', evidence, re.M))
    raw_units = {m[1]: evidence[m.end():raw_markers[i+1].start() if i+1<len(raw_markers) else len(evidence)].strip() for i,m in enumerate(raw_markers)}
    for index, source in enumerate(sources, 1):
        chosen = []
        for unit in units:
            if unit['source_id'] != f'S{index}': continue
            if not substantive(unit['excerpt']):
                changes.append({'evidence_id':unit['id'],'action':'exclude_non_substantive'})
                continue
            unit['excerpt'] = qualify_note_claims(unit['excerpt'], unit['source_id'])
            for caution in evidence_cautions(unit['excerpt']):
                annotation = '[Evidence caution / 编者核查限制] ' + caution
                if annotation not in unit['excerpt']:
                    unit['excerpt'] += '\n\n' + annotation
            if unit['excerpt'] != raw_units.get(unit['id']):
                changes.append({'evidence_id':unit['id'],'action':'clean_scaffolding_and_qualify_local_claim_ids'})
            chosen.append(f"[Evidence {unit['id']} | source {unit['source_id']} | kind {unit['kind']}]\n{unit['excerpt']}")
        if chosen:
            blocks.append(f"### {source.get('title', source['path'])}\nSource note: {source['path']}\nSource note SHA-256: {source.get('note_sha256', 'not recorded')}\n\n" + '\n\n'.join(chosen))
    return '\n\n---\n\n'.join(blocks), changes


def build_ledger(answer, evidence, sources):
    units = evidence_units(evidence)
    by_id = {u['id']:u for u in units}
    claims, warnings, seen = [], [], set()
    for line in answer.splitlines():
        if re.match(r'^\s*\[Evidence caution', line):
            continue
        if 'multi-CaMeL' in line and '0.0%' in line and re.search(r'0\.0%[–—~-]0\.2%', line):
            warnings.append('配置核验：不可将 individual CaMeL 与 multi-CaMeL 的 ASR 合成一个配置结果')
        if '单次模拟运行' in line:
            warnings.append('实验条件核验：单次运行表述需与重复次数及统计口径核对')
        if re.search(r'当前主流协议|现有协议均|所有协议都', line):
            warnings.append('范围核验：单篇协议的拓扑假设不能外推为整个领域的共同限制')
        if '疫苗' in line and re.search(r'示例训练|显著提升', line):
            warnings.append('干预核验：区分上下文示例与参数训练，统计显著性须有检验依据')
        if not re.match(ROW,line): continue
        cells = split_mapping_row(line)
        if len(cells) != 10:
            warnings.append('主张行必须为八列'); continue
        cid = cells[1].strip().replace('**','')
        source_ids = re.findall(r'\bS\d+\b',cells[3])
        unit_ids = list(dict.fromkeys(re.findall(r'\bE\d+\b',cells[4])))
        problems = []
        if cid in seen: problems.append('主张编号重复')
        seen.add(cid)
        suggestion = cells[5].strip() == '本次建议'
        if not suggestion and not unit_ids: problems.append('未绑定证据编号，需逐条建立证据链')
        for uid in unit_ids:
            unit = by_id.get(uid)
            if not unit: problems.append(f'{uid}不存在'); continue
            if not substantive(unit['excerpt']):
                problems.append(f'{uid}只有标题或过渡文字，不能作为支持证据')
            if unit['source_id'] not in source_ids: problems.append(f'{uid}与声明来源不匹配')
            if '原论文' in cells[5] and unit['kind'] in ('note_analysis','theme_secondary','hypothesis'):
                problems.append(f'{uid}为分析或二手转引，不能直接标为原论文已验证结论')
        if '原论文' in cells[5]:
            for sid in source_ids:
                index = int(sid[1:]) - 1
                if 0 <= index < len(sources) and '/20_Themes/' in sources[index]['path'].replace('\\', '/'):
                    problems.append(f'{sid}为主题二手来源，不能标为原论文结论；需绑定一手论文摘录')
        bound = [by_id[uid]['excerpt'] for uid in unit_ids if uid in by_id and by_id[uid]['source_id'] in source_ids]
        if bound:
            excerpt = '\n'.join(bound)
            # Numbers are checked only against the declared evidence, not other papers.
            numbers = re.findall(r'(?<![A-Za-z0-9])\d+(?:\.\d+)?\s*(?:%|pp|×|个百分点)', cells[2])
            absent = [n for n in numbers if not quantity_in_excerpt(n, excerpt)]
            if absent:
                problems.append('数值未在绑定摘录中找到（计算值需说明公式与基线）：' + ', '.join(absent))
            if any(by_id[uid]['kind'] == 'hypothesis' for uid in unit_ids if uid in by_id) and '假设' not in cells[5] and not suggestion:
                problems.append('研究假设被归入非假设类型，需区分待验证推测与已验证发现')
            for locator in re.findall(r'\[Paper:[^\]\r\n]+\]', cells[4]):
                if locator not in excerpt:
                    problems.append('定位未在绑定证据中出现：' + locator)
        claims.append({'claim_id':cid,'claim':cells[2].strip(),'source_ids':source_ids,
                       'evidence_ids':unit_ids,'evidence_type':cells[5].strip(),
                       'conditions':cells[6].strip(),'section':cells[7].strip(),'missing':cells[8].strip(),
                       'link_issues':problems,'semantic_status':'pending_review'})
        warnings.extend(f'{cid}：{p}' for p in problems)
    report_text = re.sub(r'\bS\d+:C\d+\b', '', answer)
    referenced = set(re.findall(r'\bC\d+\b', report_text))
    for cid in sorted(referenced - seen):
        warnings.append(f'{cid}：正文或提纲使用了未定义的主张编号')
    # Conservative review flags, not automatic factual corrections.
    for line in answer.splitlines():
        if re.search(r'(?:含环|有环)[^。\n]{0,18}DAG|DAG[^。\n]{0,18}(?:属于|是)含环', line):
            warnings.append('术语核验：DAG 是有向无环图，不能归入含环拓扑')
        if re.search(r'PD\s*[（(]\s*Prompt Denial', line, re.I):
            warnings.append('指标核验：PD 的展开未核实，需绑定来源中的指标定义')
        if re.search(r'(?:全部|所有|固有)[^。\n]{0,55}(?:语言层|提示|记忆|协作税|协作度)', line):
            warnings.append('范围核验：检查全称或固有代价表述，需保留不同防御与模型的例外')
    if not claims: warnings.append('缺少可逐条审核的主张表')
    return {'version':VERSION,'sources':sources,'evidence_units':units,'claims':claims,
            'semantic_verified':False}, list(dict.fromkeys(warnings))
