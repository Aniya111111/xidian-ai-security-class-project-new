逐条评估 REVIEW 中所有主要及局部意见，返回以下结构。
{
 "edits": [{"id":"E1", "issue_ids":["R1-M1"],
            "old":"原稿中唯一、逐字存在的一段文本", "new":"替换文本"}],
 "decisions": [{"issue_id":"R1-M1", "status":"revised|pending_verification|not_adopted",
                "reason":"处理依据及修改说明", "remaining":"仍需核验的事项；没有则写无"}]
}
每条审阅意见必须且只能有一条 decision。每个 edit 可以处理多条意见。
revised 必须关联 edit，pending_verification 可先降调措辞但保留待核验状态。
not_adopted 需说明拒绝理由，不关联修改。不得修改不相关章节或整篇重写。
old 必须是原稿中的唯一连续文本，不得省略、改标点或重叠；不替换整个长文。
new 保留原文结构、表格列、C/S编号、路径和 [Paper: ...] 定位，不能引入新定位或新来源。
新数字只能来自被修改的原文。不要补写未核实的指标全称、区间上限或其他数字。
对置信区间、原论文归因、指标定义等缺乏原文的问题，用待核验说明替代猜测。
若审阅意见有误，可 not_adopted；原稿与审阅都不能作为重新核验原论文的证明。
所有修改应是局部且可追溯的文本替换。只输出 JSON。


<REVIEW>
{
  "summary": "该材料作为文献综合与写作规划较克制，已区分原论文结论、笔记分析与建议；潜在读者为多Agent安全、协议设计、评估基准研究者。主要风险是跨论文综合仍可能过度，以及部分数值/归因表述需弱化。",
  "strengths": [
    "明确区分原论文结论、研究问题、笔记分析与本次建议。",
    "对S4方法与结果缺失保持证据边界，未强行总结。",
    "已提示横向比较限制、指标口径差异和术语映射待补。"
  ],
  "major_concerns": [
    {
      "id": "R1-M1",
      "blocking": false,
      "claim_pointer": "第4节论文提纲：引言（第2行）",
      "claim_quote": "引出单Agent安全到多Agent系统安全的范式迁移",
      "evidence_pointer": "S2笔记03研究问题；S3笔记03研究问题；S4笔记03研究问题；范式迁移为文稿第4节建议",
      "concern": "将S2/S3/S4并列成“范式迁移”可能暗示共同演进，但S4仅有研究问题摘录，S3侧重评估基础设施，证据不足以支撑跨论文范式史或统一迁移结论。",
      "why_it_matters": "影响原创性定位与文献综合可信度，易被读成三篇论文共同得出系统级安全演进。",
      "resolution_test": "明确标注为作者提出的组织线索，或改写为“三类互补问题：协议可组合性、评估基础设施、辩论交互安全”。"
    },
    {
      "id": "R1-M2",
      "blocking": false,
      "claim_pointer": "第5节主张映射 C4",
      "claim_quote": "multi-CaMeL将平均ASR降至0.0%",
      "evidence_pointer": "S2笔记11结论正确解释；S2笔记13批判性分析（Wilson上界约0.4%）",
      "concern": "0.0%是点估计，证据同时提示置信上界；当前表述可能让读者误读为安全攻击已被完全解决。",
      "why_it_matters": "影响安全主张强度和统计表述准确性，尤其在摘要、结论或比较表中易过度。",
      "resolution_test": "改为“观测到0.0%点估计，需核对原文置信上界/区间”，并在正文避免“已解决”语气。"
    },
    {
      "id": "R1-M3",
      "blocking": false,
      "claim_pointer": "第4节论文提纲：辩论交互与对抗传播展望（第6行）",
      "claim_quote": "基于S4的问题设定，推导结构化交互范式的评测缺口",
      "evidence_pointer": "S4笔记03研究问题；S4笔记10实验设计与证据链为空",
      "concern": "仅凭S4研究问题摘录推导“结构化交互范式”的评测缺口，可能把单篇问题导向扩展为跨范式结论。",
      "why_it_matters": "影响第6节可写性和跨论文总结边界；若写成实证缺口会证据不足。",
      "resolution_test": "降为“开放问题/待核验方向”，或补齐S4方法、结果与评测协议后再推导。"
    },
    {
      "id": "R1-M4",
      "blocking": false,
      "claim_pointer": "第5节主张映射 C8",
      "claim_quote": "实验全部使用平凡策略$S=\\emptyset$，结论仅覆盖控制流劫持",
      "evidence_pointer": "S2笔记11结论正确解释（作者自述边界）；S2笔记13批判性分析（同一观察）",
      "concern": "文稿将C8标为“笔记分析”，但摘录显示这可能是原论文自述适用边界；归因类型可能不准确。",
      "why_it_matters": "影响事实、笔记分析与建议的分离，以及后续写作中责任归属。",
      "resolution_test": "核对原文Section II-B/VI-B；若为作者明确声明，改证据类型为原论文结论/边界；否则保留笔记分析并说明推断依据。"
    }
  ],
  "minor_comments": [
    {
      "id": "R1-m1",
      "blocking": false,
      "claim_pointer": "第5节主张映射 C9",
      "claim_quote": "限制了结论对共谋、拜占庭鲁棒与隐蔽信道控制的解释力",
      "evidence_pointer": "S2笔记13批判性分析（未纳入恶意Agent属[Analysis]；Rose et al.仅作动机引用）",
      "concern": "“隐蔽信道控制”是否被原文覆盖无法从摘录确认，可能过度延伸。",
      "why_it_matters": "避免把笔记推断写成原论文明确限制。",
      "resolution_test": "改为“内部Agent背叛/共谋场景”，隐蔽信道表述待原文核验。"
    },
    {
      "id": "R1-m2",
      "blocking": false,
      "claim_pointer": "第4节论文提纲：第6行原有证据定位",
      "claim_quote": "`[Paper: PDF p. 4–6 §3.1–3.3]`",
      "evidence_pointer": "S4笔记03研究问题含该定位；SOURCE_EXCERPTS中S4“10 实验设计与证据链”为空",
      "concern": "该定位看似具体方法证据，但输入未提供对应方法/结果内容。",
      "why_it_matters": "易让读者误以为已有S4方法证据。",
      "resolution_test": "标注“仅研究问题摘录，方法/结果定位待补”。"
    },
    {
      "id": "R1-m3",
      "blocking": false,
      "claim_pointer": "第2.4节分歧与局限",
      "claim_quote": "指标定义(如ASR、PD、BTCR、regret)与判据逻辑亦不相同",
      "evidence_pointer": "S3方法摘录列出ASR/PD/BTCR/regret；文稿P5待补术语映射",
      "concern": "跨领域读者可能无法理解这些缩写和判据差异。",
      "why_it_matters": "影响提纲和正文可读性。",
      "resolution_test": "首次出现给全称，并增加指标对照表。"
    }
  ],
  "revision_order": [
    "弱化“范式迁移/统整主线”，明确为作者组织线索。",
    "修正C4的ASR=0.0%表述，加入置信区间或待核验说明。",
    "将S4相关章节降为开放问题，或补齐方法/结果摘录。",
    "核对C8归因类型，区分原论文边界与笔记分析。",
    "补充术语表、指标对照和S4定位缺失说明。"
  ],
  "not_assessable": [
    "原论文全文真实性、页码、表格内容、DOI与出版信息。",
    "S4是否实际提供方法、数据集、攻击层实现与结果。",
    "C4置信上界、C6 Judge漂移、C8原文边界声明等细节。",
    "恶意Agent、隐蔽信道、共谋收益结构是否被原论文正式覆盖。",
    "三篇工作是否存在可比较的统一威胁模型或共同缺口。"
  ],
  "limitations": [
    "本次只审阅文献综合与写作材料，不判断可投稿性或录用。",
    "仅基于输入摘录，不是全文核验。",
    "输入缺失不证明原论文未做相应研究。",
    "不要求开展新实验，也不核验外部链接或来源真实性。"
  ]
}
</REVIEW>

<IMMUTABLE_REVIEW_PACKET>
输入范围为文献综合、提纲及主张映射。未开展新实验。
证据仅是提供的笔记摘录，不是经重新核验的全文。

<MANUSCRIPT>
# AI-Researcher Obsidian 构思结果

- 运行时间：2026-10-23T21:34:33+08:00
- Reference 补充材料：无

## 本次研究问题

根据已加载的 Obsidian 证据包，整理多 Agent 系统安全相关文献，生成中文文献综合、论文提纲和主张—来源映射。严格区分原论文结论、原论文研究问题、笔记分析与本次建议；保留来源笔记完整路径和原有证据定位。证据不足时明确说明，不要推断或编造结果。本次只整理写作材料，不设计或运行实验。

---

Evidence bundle: E:\oblidian\file\safetyAI\Agent-IFC\30_Projects\AI-Researcher\References\multi-agent-security.reference.md
Evidence bundle SHA-256: 13e806374faba89dc1116c5b855e38269c7cc3cd81875d7fa87ceaf8a13c6bd6
Selected evidence: 15,935 chars from 4 sources
- 多Agent协作的安全防护 | Agent-IFC/20_Themes/多Agent协作的安全防护.md | 4336 chars
- Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks | Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | 5997 chars
- ORBIT: A Framework for Multi-Agent Safety and Security Evaluations | Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | 3990 chars
- MADBench: Benchmarking the Security of Multi-Agent Debate | Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | 570 chars

# 1. 文献范围与证据边界

| 来源编号 | 完整路径 | 标题 | 覆盖主题 | 证据性质说明 |
|---|---|---|---|---|
| **S1** | `Agent-IFC/20_Themes/多Agent协作的安全防护.md` | 多Agent协作的安全防护 | 主题级二次综述，整合S2/S3/S4的摘录、批判性分析与框架对比 | 为笔记作者的合成笔记，非独立验证或原文复现；其标注为`[Analysis]`的内容属于笔记作者推断，不代表原论文结论 |
| **S2** | `Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md` | Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks | 层级式agent-as-tool系统的控制流完整性(CFI)、间接提示注入(Indirect Prompt Injection)、边界洗白机制与双通道协议修复 | 包含原论文研究问题、方法设定、明确结论与经验数据；附笔记作者批判性分析表 |
| **S3** | `Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md` | ORBIT: A Framework for Multi-Agent Safety and Security Evaluations | 多Agent安全评估框架、YAML参数化配置、受控比较设计、共谋防御盲区 | 包含原论文研究问题、方法架构、自分类结论（1项经验发现+2项演示）；附笔记作者实证设计缺陷分析 |
| **S4** | `Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md` | MADBench: Benchmarking the Security of Multi-Agent Debate | 多智能体辩论(MAD)系统的对抗影响吸收/放大机制、分层攻击评测基准 | **仅提供研究问题与意义摘录**。方法、实验设置与结论部分在本次证据包中**缺失**，任何关于MADBench结果的主张均属证据不足 |

**证据边界说明：**
- 主题笔记(S1)为二次整理，其引用的原文定位仅限辅助追踪，不构成独立验证。
- 不同论文的威胁模型、数据集、评测指标与拓扑假设存在差异，不可直接交叉排名性能。
- 摘录中标注的`[Analysis]`观察表由笔记作者撰写，属于**笔记分析**，需在写作材料中与原论文结论严格剥离。
- S4的方法与结果段落未在证据包中提供，遵循“缺失摘录不证明原论文未研究”原则，对应主张统一标记为`证据不足`。

---

# 2. 文献综合与对比

### 2.1 研究问题与核心关切
- **S2** 聚焦单Agent安全协议(CaMeL的CFI与控制流约束)在层级委托架构下的可组合性，追问“逐Agent加固是否等于系统安全”。
- **S3** 指出当前多Agent安全研究的瓶颈在于“可复用评估基础设施不足”，提出通过解耦拓扑、记忆可见性、威胁模型、攻击与防御维度实现受控比较的研究问题。
- **S4** 针对辩论范式(MAD)常被用于事实核查与推理提升的背景，提出核心问题：对抗性影响在多轮辩论交互中是被吸收还是放大？其结果如何受攻击层、共谋模式、被攻陷Agent数与模型能力的影响。

### 2.2 方法与机制对比
- **S2** 采用树状层级拓扑，引入双通道协议分离`message`(可信指令)与`variables`(不透明数据)，依赖自定义Python解释器进行运行时值源追踪与策略强制，无模型微调。
- **S3** 基于UK AISI Inspect框架构建YAML驱动的配置层栈，支持API托管模型运行，输出三层指标(per-agent/per-sample/per-experiment)，具备框架级扩展能力。
- **S4** 目前仅披露基准构建意图与分层评测视角，具体基线设计、数据流构造、判别判据与训练/运行环境在已供材料中未展开。

### 2.3 结论与适用范围
- **S2** 的经验与理论结合指出：在层级多Agent系统中，即使每个Agent满足CFI，不可信工具返回值仍可能通过自然语言参数渠道“边界洗白”子Agent的控制流；显式双通道化可在不改变既有分支选择权的前提下阻止路径新增，但代价是效用损失与隐式依赖漏检风险。该结论严格限于树状拓扑、诚实Agent、平凡安全策略($S=\emptyset$)与控制流劫持场景。
- **S3** 作者自我界定为一项经验发现与两项演示：逐动作防御可将单一被攻陷Agent的ASR压低约60个百分点，但对共谋行为无可测保护；安全成本因机制而异。该发现依赖于特定任务集(SWE-Bench MI)与默认低共享记忆配置，且成功判据与机器评判(LLM judge)存在语义对齐问题。
- **S4** 尚无法提取有效结论。其研究问题明确了MAD安全性评测的空缺，但未见对抗鲁棒性、吸收/放大效应或分层攻击结果的支撑证据。

### 2.4 分歧与局限
- 三篇工作的关注点并不相同；本次摘录不足以证明它们共同主张“安全需在系统/协议层面强制”。目前可分别概括为：S2讨论**信息信任级别跨越边界的隐式提升**；S3讨论**评估维度的正交化与受控比较**；S4提出**交互范式中的对抗传播问题**。这些是研究焦点的并列，不应写成三篇论文共同得出的结论。
- 直接横向比较受限：S2的Tree-Of-Delegation架构与S3的任意有向通信拓扑、S4的多轮辩论协议不在同一交互契约下；指标定义(如ASR、PD、BTCR、regret)与判据逻辑亦不相同。
- 尚不能从当前摘录归纳三篇工作的“共同缺口”。S2摘录明确讨论树状层级拓扑、诚实Agent及数据流性质等适用边界；S3的笔记分析提出共谋判据、配置覆盖与运行时开销等待核查问题；S4在本次材料中主要是研究问题摘录，不能据此判断其对恶意Agent、异步调用或时延开销的覆盖情况。应逐篇补齐原文后再做跨论文缺口总结。

---

# 3. 候选写作方向与材料缺口

| 写作方向 | 支撑依据 | 适用形态 | 材料缺口 |
|---|---|---|---|
| **D1. 系统级安全保证的可组合性**：从单Agent硬约束到多Agent边界协议的转换条件 | S2的双通道修复与CFI可组合性讨论；S3的拓扑/记忆解耦设计；S1的综述线索 | 综述/立场型论文主线，侧重协议设计与形式性质 | 缺少统一威胁模型下的跨协议属性对比；S4在MAD中的信任传递机制待补充 |
| **D2. 多Agent安全评测基础设施演进**：从单次定制到参数化受控基准 | S3的YAML配置栈与三层指标体系；S2的工具调用环境依赖 | 方法论评述/基准综述 | 现有基准的判据一致性、Judge漂移、小样本功效、非对抗失效底噪等实证规范细节待核验 |
| **D3. 结构化交互范式中的对抗传播**：委派、辩论与链式调用的安全差异 | S4的RQ设定；S2的分支引导(branch steering)风险；S3的共谋脆弱性 | 对比分析/概念框架论文 | MAD的具体攻击层设计、轮数敏感性、模型规模效应数据缺失；需对齐S2/S3的评价口径以便类比 |

**注意区分：** D1-D3为本报告基于已有摘录提出的写作规划建议。原论文并未宣称自身填补了所有领域空白；笔记作者的分析（如效用公平性、共谋证据不对称、默认配置偏向）属于批判性审视，应在正文中作为局限性讨论或未来研究方向引用。

---

# 4. 论文提纲与章节材料

**候选标题：** 《多Agent系统安全：从逐层加固到系统级协议与受控评估》

| 序号 | 章节/小节 | 写作目的 | 主要主张(ID) | 可用来源 | 原有证据定位 | 缺失/待补材料 |
|---|---|---|---|---|---|---|
| **1** | 摘要(Abstract) | 概括研究背景、核心问题、主要发现与写作贡献 | 无新主张 | 全文 | 不适用（本次建议） | 成稿后按实际字数精简提炼 |
| **2** | 引言(Introduction) | 引出单Agent安全到多Agent系统安全的范式迁移，界定本文范围与结构 | C1, C3, C5, C9 | S2, S3, S1 | `[Paper: Section I; Section I 相关工作段; Section III-A 末段]` (S2)<br>`[Paper: PDF p. 2–3, Section 1；PDF p. 5, Section 3.1–3.2]` (S3) | 补充最新部署案例与行业安全白皮书引用 |
| **3** | 相关工作/分类 (Related Work) | 按“单Agent协议→层级委托→辩论交互→评估基准”四维归类 | C1, C3, C5, C7 | S2, S3, S4, S1 | `[Paper: Section I 防御分类段]` (S2)<br>`[Paper: PDF p. 1, Abstract；PDF p. 8–9, Section 5；PDF p. 9, Section 6]` (S3)<br>`[Paper: PDF p. 1–2 §1, p. 2 §1]` (S4) | 核对S4原始相关工作的完整引用链 |
| **4** | 层级委托与协议可组合性 (Cross-Paper Comparison I) | 剖析边界洗白机制与双通道修复的有效性/代价 | C1, C2, C3, C4 | S2 | `[Paper: Section III-A; Section III-C; Section VII]`<br>`[Paper: Section IV-A; Section IV-B; Section IV-C]`<br>`[Paper: Table III; Section V-C1; Section V-A2; Fig. 5; Fig. 6; Table IV; Table V]` | 验证书面概率区间上限([0.0, 0.4])；确认基线效用增强是否一致 |
| **5** | 受控评估框架与共谋盲区 (Cross-Paper Comparison II) | 梳理参数化解耦思想，指出防御机制在非共谋/共谋场景的效能断层 | C5, C6 | S3 | `[Paper: PDF p. 2–3, Section 1；PDF p. 5, Section 3.1–3.2]`<br>`[Paper: PDF p. 8–9, Section 5 (1)；PDF p. 36, Table 14 与 Appendix J.2]` | 核对ORBIT注册攻击键清单；检验Judge模型跨单元格一致性 |
| **6** | 辩论交互与对抗传播展望 (Cross-Paper Comparison III) | 基于S4的问题设定，推导结构化交互范式的评测缺口 | C7 | S4 | `[Paper: PDF p. 2 §1, p. 7 RQ1/RQ2]`<br>`[Paper: PDF p. 4–6 §3.1–3.3]` | **本方向需补齐方法/结果摘录方可展开** |
| **7** | 讨论：局限性与未决问题 (Discussion) | 汇总统计强度、默认配置偏向、恶意Agent覆盖、判据对齐等批判点 | C8, C9, D2延伸 | S2, S3 | `[Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2]` (S2)<br>`[Paper: PDF p. 36–37, Appendix J.4；PDF p. 38, Table 17；PDF p. 39, Table 19]` (S3) | 需补充等价性检验(TOST)与小样本功效的通用写作指引 |
| **8** | 结论 (Conclusion) | 收束于“跨越Agent边界不应隐式提升信息信任级别”的原则 | C3, C4, D1 | S2, S1 | `[Paper: Section VI-A 末段; Section VII]` | 保持与原论文声明一致的弱化语气 |
| **9** | 参考文献 (References) | 规范列出所涉论文、基准文档与外部引用 | — | 全文 | 不适用（本次建议） | 依目标期刊格式排版 |

> 注：本提纲为写作结构规划，不含实验计划或代码实现指导。第6节暂保留问题设定，待MADBench补充材料后再决定是否扩展为实证对比小节。

---

# 5. 主张与来源映射

| 主张编号 | 主张内容 | 来源编号及笔记路径 | 原有证据定位 | 证据类型 | 适用边界 | 拟用于章节 | 待补材料 |
|---|---|---|---|---|---|---|---|
| **C1** | 在层级式agent-as-tool多Agent系统中，“逐Agent部署单Agent安全协议(CaMeL)”不等于系统安全。 | S2: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section III-A; Section III-C; Section VII] | 原论文结论 | 树状拓扑、CFI性质、诚实Agent、存在返回值不可信的工具 | 2, 4, 7 | 确认拓扑变体(DAG/异步)下的适用性外推 |
| **C2** | “边界洗白”(父Agent将工具派生的不可信值写入子Agent自然语言指令参数)是控制流被改写的主要失效机制。 | S2: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section III-A; Section III-C; Section VII] | 原论文结论 | 指令通道混合输入、自然语言参数承载不可信上下文 | 4 | 验证其他协议下类似洗白路径的普遍性 |
| **C3** | 协议层修复需显式双通道化并运行时强制：`message`隔离可信指令，`variables`携带provenance供子Agent按需取用。 | S2: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section IV-A; Section IV-B; Section IV-C] | 原论文结论 | 不透明数据不直接进入PLL决策流、依赖解释器规则 | 2, 4, 8 | 形式化证明与符号执行审计记录 |
| **C4** | 经验结果表明multi-CaMeL将平均ASR降至0.0%，但相对no CaMeL存在8.0–37.5点的效用损失。 | S2: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Table III; Section V-C1; Section V-A2; Fig. 5; Fig. 6; Table IV; Table V] | 原论文结论 | 限定于MultiAgentDojo/AssetOpsBench基准与给定模型池 | 4, 7 | 自适应红队测试与置信上界报告 |
| **C5** | 多Agent安全评估的主要瓶颈是“可复用评估基础设施不足”，而非威胁假设匮乏。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 2–3, Section 1；PDF p. 5, Section 3.1–3.2] | 原论文研究问题/意义 | 适用于需快速切换拓扑/记忆/威胁模型的比较研究 | 2, 3, 5 | 与其他基准(如MASpi, ASB)的能力矩阵复核 |
| **C6** | 逐动作防御能将单一被攻陷Agent的ASR压低约60个百分点，但对共谋行为无可测保护。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 8–9, Section 5 (1)；PDF p. 36, Table 14 与 Appendix J.2] | 原论文结论 | SWE-Bench MI、GPT-5.4、Star设定、$\tau=0.5$、N=50 | 5, 7 | 共谋收益结构对齐检验与门控防御时延测量 |
| **C7** | 辩论系统中对抗性影响是被吸收还是放大，及其随攻击层、轮数、模型与$f$变化的量化规律，尚无系统化评测。 | S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 2 §1, p. 7 RQ1/RQ2]<br>[Paper: PDF p. 4–6 §3.1–3.3] | 原论文研究问题 | 仅限MAD范式预设，尚未给出实证结果 | 3, 6 | 获取S4方法/结果完整摘录以转为实证主张 |
| **C8** | 实验全部使用平凡策略$S=\emptyset$，结论仅覆盖控制流劫持，不覆盖数据流攻击、越权动作或策略误报率。 | S2: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2] | 笔记分析 | 笔记作者基于原文Section II-B与Section IV-B第2点的推断 | 7 | 原文作者对数据流攻击范围的明确声明核对 |
| **C9** | 威胁模型未纳入恶意/被攻陷Agent，限制了结论对共谋、拜占庭鲁棒与隐蔽信道控制的解释力。 | S2: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section I（Rose et al. 引用）; Section III-A（攻击者设定）; Section II-A] | 笔记分析 | 笔记作者指出原文仅考虑外部数据源注入，未建模内部Agent背叛 | 7 | 原文附录对恶意Agent覆盖的正式声明检索 |
| **C10** | 建议以“跨越Agent边界的信息信任级别管理”为线索统整多层委托、辩论与评估框架的演进脉络。 | S1: Agent-IFC/20_Themes/多Agent协作的安全防护.md；S2: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md；S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md；S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | 不适用（本次建议） | 本次建议 | 面向综述/立场型写作结构规划 | 根据目标期刊偏好调整章节权重 |

---

# 6. 后续写作清单

| 优先级 | 任务描述 | 涉及主张/章节 | 缺失材料/待办 |
|---|---|---|---|
| **P1** | 核实S2中ASR=0.0%的Wilson置信上限([0.0, 0.4])表述位置，并在正文中使用“≤X%”或带区间写法，避免绝对化断言。 | C4 / 章4, 7 | 原文Table III注释页码确认；统计措辞模板准备 |
| **P2** | 核对S2效用比较公平性：检查no-CaMeL基线是否同样获得完整工具返回schema的提示增强，若否则修正“效用损失”归因。 | C4, C8 / 章7 | 原文Section V开头段交叉比对；撰写消融对比段 |
| **P3** | 审查S3 Judge模型漂移问题：确认Table 10中defended cells(GPT-4.1)与baseline(GPT-4o)的差异幅度，在讨论中注明跨格比较的潜在偏差。 | C5, C6 / 章5, 7 | 原文Table 10 caption逐字核对；撰写判据一致性备注 |
| **P4** | 检索并补充S4(MADBench)的方法设定、数据集划分、攻击层实现与初步结果摘录，以便将C7转化为实证对比主张或维持为问题导向文献。 | C7 / 章3, 6 | S4原文Method/Setup/Results段提取；若仍缺则降为“开放问题”叙述 |
| **P5** | 对齐三篇论文的术语与指标映射表（ASR/PD/BTCR/regret/coalition advantage），避免读者混淆不同基准下的同类指标定义。 | C1~C9 / 章3, 4, 5 | 编制统一缩写与判定逻辑对照表（仅做描述性整理） |
| **P6** | 撰写“局限性与未决问题”段落，明确区分原论文声明的边界与笔记作者指出的实证缺陷，采用弱化语气(e.g., “当前证据表明…”“仍需进一步验证”)。 | C8, C9, D2延伸 / 章7 | 收集原文Limitations/Future Work段原句；完成段落草稿 |
| **P7** | 按目标投稿格式整理参考文献元数据，核对S1/S2/S3/S4的DOI、出版 venue 与年份，确保引用路径可追溯。 | 全篇 | 文献管理软件批量导入；交叉校验SHA-256对应的版本快照 |

> 本清单仅含阅读核对、文献整理与文本起草任务，不涉及任何实验设计、代码实现或算力调度。所有后续步骤均以完善写作材料与证据链闭环为目标。

## 本地来源格式检查

- 已识别 10 行 C 编号主张映射，并检查来源编号、完整路径和定位格式；主张与证据是否实质匹配仍需人工核对。

此检查仅核对定位字符串、来源编号与路径，不核验主张语义、原论文真实性或证据充分性。不会自动重试模型，也不代表学术审核通过。

</MANUSCRIPT>

<SOURCE_EXCERPTS>
### 多Agent协作的安全防护
Source note: Agent-IFC/20_Themes/多Agent协作的安全防护.md
Source note SHA-256: f69c2638cddcd6ac96421f8a1c8752f705c2919a64cd2661b3e9d63a8cde0c48

#### Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks

- 研究问题摘录：- **具体问题**：CaMeL 为单个 Agent 提供的安全保证（控制流完整性 + 基于 capability 的策略强制），在 Agent 互相调用的层级多 Agent 系统中是否仍然成立？若不成立，失效发生在哪里、能否在协议层修复、修复的效用代价多大？[Paper: Abstract; Section I 末段; Section III] - **研究意义**：随着 Agent 被授予外部数据源、工具与服务访问权，间接提示注入的攻击面显著扩大；同时多 Agent orchestrator 模式（中心 Agent 向专门子 Agent 委派子任务）日益常见，因此"逐 Agent 加固是否等于系统安全"成为部署前的关键问题。作者称其结果为"安全必须在系统层面强制"的既有论点提供经验支持 [25, 26]。[Paper: Section I; Section I 相关工作段; Section III-A 末段] - **现有方… [[Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks#03 研究问题|卡片来源]]

- 方法摘录：- **输入**：用户指令（仅交给根 Agent $A_0$）；工具与环境描述（本文实验中均增补完整返回 schema）；不可信工具输出（数据库、网页、邮件、文件等）；跨 Agent 调用时父 Agent 提供的 `message`（可信）与 `variables`（不透明）。 - **输出**：各 Agent PLLM 生成的 Python 控制流程序；递归展开后得到的系统级控制流计划；实际工具调用及其结果；子 Agent 经 `variables` 通道接收并在运行时取用的值；最终返回给用户的答案。 - **训练/外部工具**：无模型训练或微调。依赖既有 CaMeL 的自定义 Python 解释器（追踪运行时值的来源与依赖、在工具调用处检查策略），本文对其做两项扩展；依赖 PLLM/QLLM 双模型（实验中同一后端模型兼任）；新增 `get_variable` 运行时工具；评测依赖 AssetOpsBench（LLM judge 评分）、AgentDojo/MultiAgentDojo 环境与注入任务，模型经 OpenRouter API 访问。 - **关键假设**： - 拓扑为以 $A_0$ 为根的有向树，每个非根 Agent 有唯一父 Agent，所有 Agent 间通信都经父→子调用与返回；子 Agent 被"新启动"而非跨调用保留状态或会话历史。[Paper: Sec… [[Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks#07 方法概览|卡片来源]]

- 正确解释摘录：论文可以支持的、边界明确的主结论是：**在层级式 agent-as-tool 多 Agent 系统中，"逐 Agent 部署 CaMeL"不等于系统安全。** 失效机制是边界洗白——父 Agent 把工具派生的不可信值写入子 Agent 的自然语言指令参数，而子 Agent 把调用它的父 Agent 当作用户，于是该值以可信输入身份进入子 Agent 的 PLLM 并改写其控制流计划。作者既给出构造性反例（三 Agent、注入置于 SQL 数据库、GPT-5.2、平凡策略），又在温和的表达能力假设下证明：只要系统非平凡且存在返回值不可信的工具，系统级 CFI 必然被违反，即使每个 Agent 各自满足 CFI。[Paper: Section III-A; Section III-C; Section VII] 修复方式是把边界显式双通道化并在运行时强制：`message`（可信指令，不得依赖任何工具输出）与 `variables… [[Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks#11 结论的正确解释|卡片来源]]

#### ORBIT: A Framework for Multi-Agent Safety and Security Evaluations

- 研究问题摘录：- 具体问题：如何在不为每项研究重建整套基础设施的前提下做**受控**多 Agent 安全评估——固定其余维度、单独改变拓扑/记忆可见性/威胁模型参数/攻击类型/防御机制，并同时测量攻击成功率与良性效用？[Paper: PDF p. 2–3, Section 1；PDF p. 5, Section 3.1–3.2] - 研究意义：作者认为主要瓶颈"不是威胁假设不足，而是可复用评估基础设施不足"；该固定成本对防御工作的负担重于攻击工作（攻击比防御更易跨基底迁移）[Paper: PDF p. 10, Section 6；PDF p. 15, Appendix A]。 - 现有方法不足：多数防御研究只在自建环境评估单一机制对单一攻击类型；现有多 Agent 框架缺少可配置拓扑、威胁模型参数化或与防御的集成；单 Agent 基准不改变交互 Agent 数量、不参数化威胁模型、不在同一协议下联合评估攻击与防御 [Paper: PDF p.… [[Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations#03 研究问题|卡片来源]]

- 方法摘录：- 输入：一份 YAML 实验配置，指定 Setup（Agent 角色/模型/系统提示/工具、有向通信拓扑、记忆可见性策略）、Scenario（`@task` 任务与 Docker 沙箱环境）、Attack（类型、ThreatModel 四参数、注入时机、成功判据）、Defense（type / invocation mode / scope / fail mode，可跨层组合）[Paper: PDF p. 5, Section 3.2 Layer 1–4]。 - 输出：Inspect eval log，以及三层指标——per-agent（compromise score）、per-sample（PD、AS、PR/ER/HA/HT）、per-experiment（ASR、mean PD、BTCR、ΔBTCR、defense bypass rate、false positive rate）；DCOP 场景另输出 ground-truth 的 regret 与 coalition advantage [Paper: PDF p. 6, Section 3.4 与 Figure 2；PDF p. 7, Section 4]。 - 训练/外部工具：**不训练或微调任何模型**，全部使用 API 托管模型（无需 GPU）；运行时为 Inspect AI（MIT 许可），ORBIT 运行时扩展… [[Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations#07 方法概览|卡片来源]]

- 正确解释摘录：论文自己把结论分档，这一分层必须原样保留：**一项作为经验发现辩护的结果**、**两项作为框架能力的演示而非主张** [Paper: PDF p. 8, Section 5「We report one empirical finding (1) and two demonstrations (2–3)」；PDF p. 9, Section 6]。 - 可作为经验发现接受：在 SWE-Bench MI（GPT-5.4，Star，$N=50$，$\tau=0.5$）上，逐动作防御把被攻陷 Agent 的 ASR 压低 60 个百分点，却对共谋无可测保护，且四种防御在共谋上互相不可区分；机制解释是共谋的脆弱性只存在于"各自良性动作的组合"之中 [Paper: PDF p. 8–9, Section 5 (1)；PDF p. 36, Table 14 与 Appendix J.2]。 - 只能作为演示接受：安全成本依机制而异（Dual-… [[Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations#11 结论的正确解释|卡片来源]]

## 已审核文献综合

来源：3 篇 `reviewed` 卡片。以下内容为卡片原文摘录与整理，尚需本次综合审核；不代表重新验证了原论文。

### 后续比较需要补齐的材料

- 扩充覆盖消息注入、恶意 Agent、记忆污染、权限越界、工具滥用和级联攻击的已审核论文，再按统一威胁模型比较。

- 对可比实验核对共同数据集、模型、指标与预算；暂不汇总成统一性能排名。

- 回原文核对卡片中的待确认字段，区分作者结论、分析与研究假设。

### 研究问题与方法证据

比较边界：不同协作拓扑、威胁模型、权限配置、任务与评估协议下的安全结果不能直接排名；未明确的字段保留待确认，不从论文标题推断安全性。

# 多Agent协作的安全防护

### 多Agent协作的安全防护对比表

## 手写笔记

<!-- Agent-IFC:multi-agent-security-synthesis:begin -->

---

### Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks
Source note: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md
Source note SHA-256: 59775e74afeb2756e97b54189f34ebfaf3cb9eac1c1d5d618b49ed72cbf8ba88

## 13 批判性分析

| `[Analysis]` 观察 | 潜在问题或替代解释 | 为什么重要 | 如何检验 | 依据 |
| --- | --- | --- | --- | --- |
| "ASR 降到 0.0%"的统计强度有限 | n = 949 下 0 次成功的 Wilson 95% 上界约 0.4%（论文表中即 [0.0, 0.4]），因此结果与"低到 0.4% 的真实 ASR"在统计上不可区分；且注入攻击集合固定、非自适应 | 若把 0.0% 当作"已解决"，会低估针对 `variables` 通道、`get_variable` 语义或 QLLM 输出的定向攻击风险 | 设计自适应攻击：让注入内容显式诱导父 Agent 把不可信文本写入 `message`（测试解释器是否拦截）、或诱导子 Agent 以特定变量名调用 `get_variable`；报告 ASR 的置信上界而非点估计 | [Paper: Table III 及其说明]（作者已部分承认，见 C12） |
| 全部实验使用平凡策略 $S=\emptyset$，安全结论只覆盖控制流劫持 | 论文明确区分控制流攻击与数据流攻击：即使控制流不变，攻击者仍可能影响 QLLM 在合法计划内产出的数据，导致越权动作（如外发敏感信息）。跨边界保留 provenance 的机制（解释器性质 2）在实验中**未被实际行使** | 研究画像关注的"共享记忆污染、上下文污染、数据外泄"多属数据流层面；仅凭本文不能推断 multi-CaMeL 对这类攻击有效 | 配置非平凡策略（如禁止 `send_email` 携带源自私有数据的参数发给未授权收件人），测量攻击成功率、策略误报率与效用三者；并做"仅性质 1 / 仅性质 2 / 两者"的消融 | [Paper: Section II-B（Definition 4 与数据流攻击说明）; Section IV-B 第 2 点; Section II-B 平凡策略理由] |
| 协议层保证与实现层保证之间存在缺口 | 作者承认解释器可能漏检隐式依赖（未走分支上的赋值等），使变量在被污染时仍标记为可信；而 Section IV-C 的论证以"指令通道完整性被强制"为前提 | 这意味着 0% ASR 是经验观察，不等于实现满足协议性质；真实系统中一次漏检就可能重新打开边界洗白 | 构造隐式依赖测试用例（如 `if untrusted_flag: msg = trusted_text`，其中 `untrusted_flag` 源自工具输出），检查解释器是否阻止该 `msg` 进入 `message`；或用形式化/符号执行审计解释器的依赖追踪规则 | [Paper: Section VI-B1; Section IV-C] |
| 效用比较的公平性存疑 | CaMeL 系配置获得"所有工具描述增补完整返回 schema"的提示增强；检索到的正文未说明 no-CaMeL 基线是否也获得同等增强 | 若基线未获增强，则 no CaMeL 的效用被低估，从而夸大 CaMeL 系的相对代价；反之若基线也获增强，则比较公平——这一点直接影响 21.6 点与 3.2 点这两个数字的解释 | 交叉消融：{增强, 未增强} × {no CaMeL, individual, multi}，报告 2×3 网格 | [Paper: Section V 开头段]（增强必要性明确，基线是否同享增强未明确记录） |
| MultiAgentDojo 由本文作者构造，工具划分方式可能天然利于 multi-CaMeL | 子 Agent 按工具相似度划分（Email/Calendar/Drive、Transactions/Files/Account、Slack/Web、Hotels/Restaurants/Car Rental/Assistant），跨边界通信因此多为"传值"而非"传需要下游据此改变计划的指令" | 若真实系统的委派是"把检索到的不可信内容交给子 Agent 并让它自行决定动作"，双通道分离的效用代价可能远高于本文测得的 3.2 点 | 增设一类任务：子 Agent 必须依据不可信内容选择不同工具序列（即需要 branch steering 之外的计划调整），测量 multi-CaMeL 的成功率与 ASR | [Paper: Section V-B; Table I]（划分为论文自述设计，属 `[Analysis]` 推断） |
| "能力越强、代价越小"缺乏机制解释与定量支撑 | 趋势非单调（Flash-Lite 在 AssetOpsBench 上 multi-CaMeL 26.8% 反而高于 individual 20.5%），仅 5 个模型，未做能力度量回归；模型名（Claude Fable 5、GPT-5.5 等）经 OpenRouter 访问，版本可能漂移 | 该趋势是论文对"系统级防御终将变得可负担"的核心乐观论据；若只是样本噪声，则部署建议需重估 | 增加模型数量并纳入公开能力分数做回归；对同一模型固定版本重复运行以估计运行间方差；报告 per-task 配对检验而非仅区间重叠 | [Paper: Section V-A2; Section V-B1; Table IV; Table V; Section IX] |
| branch steering 本身可能是可利用的攻击面 | 作者承认不可信数据可在既有分支间引导执行并改变外部可见输出，且这违反 TIPNI。若父 Agent 的计划包含"若工具返回 X 则调用 `child_agent(query_1)` 否则 `query_2`"，攻击者可通过操纵工具输出选择分支 | 对研究画像中的"级联失效/攻击传播"而言，分支选择权就是一种低成本影响力，即使不新增路径 | 构造仅通过分支选择达成危害的任务（如两个分支中一个含敏感工具调用），测量 multi-CaMeL 下的成功率；并把 CFI 与 TIPNI 的差集形式化为可测属性 | [Paper: Section IV-C; Section VI-B] |
| 威胁模型未覆盖恶意/被攻陷 Agent 与共谋 | 本文的对手是把注入植入外部数据源的外部攻击者，所有 Agent 本体均诚实且运行 CaMeL；论文在引言中引用 Rose et al. 的隐蔽共谋工作 [19] 作为动机，但未把恶意 Agent 纳入模型 | 研究画像的 B 簇（恶意成员、共谋、拜占庭鲁棒）与 D 簇（权限委托）无法由本文结论覆盖：一个恶意子 Agent 可在 `variables` 中返回任意内容，而父 Agent 的 PLLM 恰恰看不见它 | 扩展威胁模型：允许某个子 Agent 被攻陷（返回伪造/污染数据），检验 provenance 保留是否足以让父 Agent 的策略拦截；或与拜占庭鲁棒聚合机制组合评测 | [Paper: Section I（Rose et al. 引用）; Section III-A（攻击者设定）; Section II-A]（未纳入恶意 Agent 属 `[Analysis]` 判断） |
| 案例研究与主实验使用不同模型（GPT-5.2 vs 五个评测模型） | Section III-A/III-B 的演示与 OMNI-Leak 验证用 GPT-5.2，而 Table III–V 用另外五个模型；GPT-5.2 未出现在主结果表中 | 反例的可复现性与主实验结论之间存在模型不一致，读者难以判断边界洗白的发生率是否依赖特定模型的拼接习惯 | 在五个评测模型上重跑 Section III-A 的三 Agent 演示，报告各模型下 Program 4 型改写（新增外发调用）的出现率 | [Paper: Section III-A; Section III-B; Table III–V] |

## 11 结论的正确解释

论文可以支持的、边界明确的主结论是：**在层级式 agent-as-tool 多 Agent 系统中，"逐 Agent 部署 CaMeL"不等于系统安全。** 失效机制是边界洗白——父 Agent 把工具派生的不可信值写入子 Agent 的自然语言指令参数，而子 Agent 把调用它的父 Agent 当作用户，于是该值以可信输入身份进入子 Agent 的 PLLM 并改写其控制流计划。作者既给出构造性反例（三 Agent、注入置于 SQL 数据库、GPT-5.2、平凡策略），又在温和的表达能力假设下证明：只要系统非平凡且存在返回值不可信的工具，系统级 CFI 必然被违反，即使每个 Agent 各自满足 CFI。[Paper: Section III-A; Section III-C; Section VII]

修复方式是把边界显式双通道化并在运行时强制：`message`（可信指令，不得依赖任何工具输出）与 `variables`（不透明数据，携带 capabilities 与 provenance，子 Agent 经 `get_variable` 在运行时取用）。由此从根 Agent 计划递归展开得到的系统级控制流计划仅由用户指令与可信信息决定；不可信数据仍可在既有分支间"分支引导"，但不能新增路径。作者强调，与单 Agent CaMeL 不同，multi-CaMeL 的解释器即使不配置任何安全策略也是保证 CFI 所必需的。[Paper: Section IV-A; Section IV-B; Section IV-C]

经验结果的适用范围必须与其条件一起读：在 MultiAgentDojo（n = 949 注入任务实例/模型/配置）上，平均 ASR 从 no CaMeL 的 12.9% 降到 individual CaMeL 的 0.2%、multi-CaMeL 的 0.0%，且 individual CaMeL 的每一例残留成功攻击都是边界洗白；效用方面，AssetOpsBench 上 multi-CaMeL 相对 individual CaMeL 平均仅额外下降 3.2 点（两个最强模型 0.85 点，各模型区间重叠），但相对 no CaMeL 的整体损失仍达 8.0–37.5 点，MultiAgentDojo 上更大（GPT-4.1 −53.7、Gemini 2.5 Pro −49.5）。[Paper: Table III; Section V-C1; Section V-A2; Fig. 5; Fig. 6; Table IV; Table V]

因此**不应**把结论读成："multi-CaMeL 使多 Agent 系统安全"。作者自己划出的边界包括：0% ASR 只针对基准内既有攻击，未做自适应攻击评测，且大规模自适应红队对所有前沿模型都发现非零成功率；实验全部使用平凡安全策略 $S=\emptyset$，因此结果只覆盖控制流劫持，不覆盖数据流攻击；协议层论证以"指令通道完整性被强制"为前提，而当前实现继承了 CaMeL 解释器漏检隐式依赖的限制；分析仅限树状层级拓扑与 CFI/CaMeL-安全性质，DAG、循环、异步、共享内存、点对点架构与更强信息流性质（如 TIPNI，branch steering 会违反它）留待未来工作。[Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2]

作者提炼出的、比具体协议更宽的原则是：**跨越 Agent 边界不应隐式提升信息的信任级别**；随着能力更强的 Agent 被组合成更大更复杂的系统，在其接口上保留这一区分将是让安全保证可组合的重要部分。[Paper: Section VI-A 末段; Section VII]

## 03 研究问题

- **具体问题**：CaMeL 为单个 Agent 提供的安全保证（控制流完整性 + 基于 capability 的策略强制），在 Agent 互相调用的层级多 Agent 系统中是否仍然成立？若不成立，失效发生在哪里、能否在协议层修复、修复的效用代价多大？[Paper: Abstract; Section I 末段; Section III]
- **研究意义**：随着 Agent 被授予外部数据源、工具与服务访问权，间接提示注入的攻击面显著扩大；同时多 Agent orchestrator 模式（中心 Agent 向专门子 Agent 委派子任务）日益常见，因此"逐 Agent 加固是否等于系统安全"成为部署前的关键问题。作者称其结果为"安全必须在系统层面强制"的既有论点提供经验支持 [25, 26]。[Paper: Section I; Section I 相关工作段; Section III-A 末段]
- **现有方法不足**：
  - 模型级防御（微调/偏好优化让模型区分特权指令与低权限内容）与输入级防御（DataFilter 过滤模型、提示净化、sandwich prompting、spotlighting）"通常依赖习得的模型行为，不提供硬安全保证" [10]。[Paper: Section I 防御分类段]
  - 系统级防御（Dual LLM 模式、CaMeL、信息流控制 [13,14]、细粒度权限强制 [15]）中，CaMeL 明确"是为单 Agent 与其环境交互而formulated 的"，多 Agent 设置留白。[Paper: Section I 系统级防御段; Section I "CaMeL is formulated for a single agent" 段]
  - 已有工作已把层级 agent-as-tool 架构当作攻击面研究（如 OMNI-Leak [22]、Triedman et al. [24]），但缺少"个体安全何时可组合到系统级"的刻画与可运行的防护协议。[Paper: Section II-A; Section III-B]
- **核心问题**：跨越 Agent 边界时，信息的信任级别是否被隐式提升？如何在保留跨边界数据可用性的同时，阻止不可信数据进入下游 Agent 的指令通道？[Paper: Section VI-A 末段; Section VII]

## 10 实验设计与证据链

---

### ORBIT: A Framework for Multi-Agent Safety and Security Evaluations
Source note: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md
Source note SHA-256: 41ee328c301d418c7eb20e9df0c3f58ff2e443b5b5b4713283c57d26bc8e2747

## 13 批判性分析

| `[Analysis]` 观察 | 潜在问题或替代解释 | 为什么重要 | 如何检验 | 依据 |
| --- | --- | --- | --- | --- |
| 攻击类型口径不一致：Section 3.2 称"四种攻击类型"，Table 5 列十个内置条目且 misuse / misbehavior 标为 scenario-level | 读者可能把"四种"当作可用攻击实现总数，或把 misuse 当作注册表内可配置攻击 | 直接影响复现时的配置写法与"攻击面覆盖度"的判断；也影响 C08 中"框架支持哪些自变量"的边界 | 对照代码仓库的 `register_attack()` 注册键清单，逐条核对 Table 5 条目是否都有注册实现 | [Paper: PDF p. 5, Section 3.2 Layer 3；PDF p. 28, Table 5] |
| ThreatModel 四参数是能力声明，实证覆盖未跟上 | 支持 black/gray/white-box、budget、persistence、attack surface 四维，但检索到的结果章节报告的变化维度是防御、攻击类型、拓扑与模型 | 研究关注配置要求"定位攻击者能力"；若 knowledge level 未被扫描，"某防御在某攻击者能力下有效"仍缺少自变量维度 | 在固定载荷下做 knowledge level × persistence 因子扫描，报告 ASR 与 PD 的边际效应（是否已在其他附录出现：未核实） | [Paper: PDF p. 28, Appendix G；PDF p. 8, Section 5] |
| 成功判据的机器可判定性与"有害性"不等价 | 子串/正则/特定工具调用属语法判据，否定判据属可用性判据；而 $C_i$ 由 LLM judge 赋值，两套判定并存 | 同一实验可能出现"判据成功但 judge 判 0.5"或反之，使 ASR 与 PD 的语义不完全一致 | 交叉列联表统计判据成功 vs judge 分类的一致率，报告不一致样本 | [Paper: PDF p. 28, Appendix G「Success criteria」；PDF p. 6, Section 3.4] |
| Table 10 中 defended cells 用 GPT-4.1 judge、无防御基线用 GPT-4o judge（caption 明示） | 跨条件 ASR 差异可能部分来自 judge 模型差异；当基线 ASR 低至 3%、区间重叠时判断对 judge 敏感 | 直接影响 C04 中"系统提示在 BrowserART 上最强"这类跨格比较的可信度 | 用同一 judge 重跑 defended 与 baseline 单元，或交换 judge 做双向一致性检验，报告 ASR 漂移幅度 | [Paper: PDF p. 34, Table 10 caption] |
| 共谋证据两侧强度不对称 | SWE-Bench 共谋 ASR 30%（无防御）被用作核心证据，但 JiraTicket 共谋中联盟优势为负或近零、无 defended cell 可区分 | "没有防御能降低共谋 ASR"可能部分源于攻击强度不足或收益结构缺失，而非防御机制的固有盲区；且 secret_channel 对监控防御不可见，意味着门控在原理上无从判定 | 在 SWE-Bench 共谋上同时报告联盟方收益指标，确认攻击确实带来可测收益；再检验门控型防御 | [Paper: PDF p. 9, Table 2；PDF p. 35, Table 11；PDF p. 27, Appendix G「Collusion」] |
| OS-Harm 跨场景对照的数据来源异质 | Table 18 结果从 Hagag et al. [2026] 导入，模型与技术栈不同，caption 明确"不可跨场景比较" | 但正文用它论证"BrowserART 的 3.8× 放大远大于 OS-Harm"，即以声明不可比的数字支撑场景依赖性论断 | 在 ORBIT 同一栈、同一模型上重跑 OS-Harm 拓扑条件，再做放大倍数比较 | [Paper: PDF p. 38, Table 18 caption；PDF p. 37, Appendix J.5] |
| 样本量与区间宽度 | 多格 $N=42\text{–}52$；Sonnet 4.6 良性列只有 5 个 judged samples（100.0 (5/5)）；作者自标若干结果为 directional | 小样本下"无显著差异"既可能是真无效应也可能是功效不足；C07 的"nothing moves"尤其依赖功效 | 做功效分析或扩大种子数；对关键零结果报告预设等价边界下的等价性检验（如 TOST）而非仅报告区间跨零 | [Paper: PDF p. 36–37, Appendix J.4；PDF p. 38, Table 17；PDF p. 39, Table 19] |
| 前沿模型共谋对照不完整 | Table 12 脚注记录 LLM-monitor 单元因 judge 延迟耗尽 wall-clock 预算被排除，Agent 只剩约 40% 回合 | 既是覆盖缺口，也提示在线 judge 型防御在长回合多 Agent 场景中存在**时延可行性**问题，而该问题未被作为安全结论单独讨论 | 单独测量 monitor/guardian 的每回合时延与 token 成本随 Agent 数、回合数的增长曲线，给出可部署性边界 | [Paper: Appendix J, Table 12 脚注（页码未核实）；PDF p. 16–17, Appendix D] |
| "首个跨场景受控比较"是优先权主张 | 论文未提供系统性检索协议支撑 "first"；同时自引 MASpi（23 种攻击、7 个框架）与 ASB（27 攻击 × 8 防御 × 10 场景）作为近邻 | 优先权主张若被当作既成事实引用，会掩盖真实差异（差异更可能落在"同一栈内把拓扑/记忆/威胁模型作为一等维度"） | 按研究关注配置的检索策略复核 MASpi、ASB、MASEval、MAESTRO、Terrarium、MASTER 的维度覆盖，独立复核 Table 4 | [Paper: PDF p. 9, Section 6；PDF p. 17–18, Appendix E 及 Table 4] |
| Dual-LLM 的"净化"与"信息损失"未被分离 | Q-LLM 摘要既剥离注入指令也剥离任务信息；RedCode-Gen 上其传播深度 0.12 与无防御 0.14 接近，作者据此说明摘要保留了代码语义 | 若净化与信息损失同源，则该防御的安全收益上限受其效用代价约束；论文未测"更强净化 + 结构化保真摘要"的可行前沿 | 变体化 Q-LLM 提示（字段级结构化摘要 vs 自由摘要），同一场景上同时报告 ASR 与 BTCR，画出前沿曲线 | [Paper: PDF p. 36, Table 15；PDF p. 31–32, Appendix H.5；PDF p. 35, Table 13] |
| 记忆可见性默认值使"默认配置"接近低共享 | 六标志中五个默认 False，只有 `goal_visible` 默认 True | 若多数实验在低共享默认下运行，"共享记忆污染"这一传播路径的实证覆盖可能小于框架能力；`shared_cot` 被标注会暴露含攻击相关推理的内部审议，但未见其被单独扫描 | 固定攻击与防御，只扫描六个标志（尤其 `shared_action_history` 与 `shared_cot`），报告 PD 与 ASR 变化 | [Paper: PDF p. 33, Appendix I, Table 9；PDF p. 38, Table 17 仅含 Star+SharedMem] |
| 非对抗失效设置被声明但未在结果中展开 | 框架支持 misbehavior 与 coordination failure（无攻击者），OS-Harm 的 misbehavior split 提供无攻击者设置 | 研究关注配置关心"级联失效"与"局部失效后的恢复"；若结果章节只报告对抗条件，诚实 Agent 间的协调失败率缺少基线数据 | 检索/补做无攻击条件下各场景的 regret 与 BTCR 分布，作为"正常失效底噪"基线（本卡未在检索到的结果中见到该报告：未核实） | [Paper: PDF p. 3, Contribution 2；PDF p. 28, Table 5 NON-ADVERSARIAL 行；PDF p. 8, Section 4] |

## 10 实验设计与证据链

### 结论—证据矩阵

## 16 研究想法

## 02 一句话总结

ORBIT 是建立在 UK AISI Inspect 之上、把"拓扑—记忆可见性—威胁模型—防御—执行—评估"拆成六个可组合配置层的多 Agent 安全评估框架与基准套件；其核心经验发现是：能把被攻陷 Agent 攻击成功率压低 60 个百分点的逐动作防御，对共谋没有任何可测保护，且没有一种被测防御覆盖全部被测攻击类型 [Paper: PDF p. 1, Abstract；PDF p. 8–9, Section 5；PDF p. 9, Section 6]。

---

### MADBench: Benchmarking the Security of Multi-Agent Debate
Source note: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md
Source note SHA-256: d5910beb563fdc571b36b17c91930791e4430efa0228ea8db7440548a2e055c8

## 03 研究问题

- **具体问题**：对抗性影响在 MAD 中被吸收还是被放大？不同攻击层、共谋模式、被攻陷 Agent 数 $f$、辩论轮数 $R$、底层模型如何改变结果？[Paper: PDF p. 2 §1, p. 7 RQ1/RQ2]
- **研究意义**：MAD 被用于提升推理与事实性，且常用于 ground truth 不可得的领域；使 Agent 纠错的交互同样会传播对抗性错误，因此需要系统化安全评测 [Paper: PDF p. 1 Abstract, p. 1–2 §1]
- **现有方法不足**：现有安全基准主要面向单个 Agent 的 prompt、observation、memory、tools 与 action execution；针对 MAD 的工作要么假设全员诚实，要么只分析某类攻击；作者声明「据我们所知，尚不存在从分层视角系统分析 MAD 安全性的基准」[Paper: PDF p. 1–2 §1, p. 2 §1]
- **核心问题**：把「辩论是否更安全」拆成按攻击层 × 按攻击目标（准确率 / 成本 / 未授权读 / 未授权写）× 相对单 Agent 基线的可量化比较 [Paper: PDF p. 4–6 §3.1–3.3]

## 10 实验设计与证据链

## 16 研究想法
</SOURCE_EXCERPTS>
</IMMUTABLE_REVIEW_PACKET>