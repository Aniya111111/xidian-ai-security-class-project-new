# 多 Agent 安全文献综合与论文写作材料（证据边界修订版）

- 修订日期：2026-10-22。
- 原报告：[[ai_researcher_ideation_20261022_220857_897797]]；原文件保留，未覆盖。
- 修订依据：本次运行日志 `log_2026-10-22 22-07-16.log` 中实际发送的 Obsidian 摘录，而非额外补入的全文内容。
- 证据包：`Agent-IFC/30_Projects/AI-Researcher/References/multi-agent-security.reference.md`。
- 证据包 SHA-256：`13e806374faba89dc1116c5b855e38269c7cc3cd81875d7fa87ceaf8a13c6bd6`。
- 本版是对摘录支持范围与引用格式的修订，不是重新核验原论文 PDF，也不是论文审核通过记录。未运行实验，未新增实测结果。

## 1. 文献范围与证据边界

| 来源编号 | 来源笔记 | 完整笔记路径 | 本次材料边界 |
| --- | --- | --- | --- |
| S1 | 多Agent协作的安全防护 | Agent-IFC/20_Themes/多Agent协作的安全防护.md | 二次综合，不能作为与论文卡独立的一份验证证据 |
| S2 | Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks | Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | 研究问题、结论解释与批判性分析摘录；批判性分析不是原作者已证实的结论 |
| S3 | ORBIT: A Framework for Multi-Agent Safety and Security Evaluations | Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | 一句话总结与批判性分析；部分框架背景也见 S1 的二次综合 |
| S4 | MADBench: Benchmarking the Security of Multi-Agent Debate | Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | 主要是研究问题；结果章节在本次摘录中没有内容，不能据此推导实验发现 |

这些材料可用于建立比较框架和写作提纲，但不足以支持系统性综述、统一性能排名或新防护方法有效性的结论。笔记标记为已审核不等于本报告重新验证了原文。下文“原论文结论”均指论文卡转述的原论文结论，仍应在正式引用前回原文核对。

## 2. 文献综合与对比

### 2.1 安全保证能否跨 Agent 边界组合

**C1**：S2 所述结论针对层级式 agent-as-tool 系统：逐个 Agent 部署 CaMeL 并不自动形成系统级控制流完整性保证。笔记将边界洗白解释为：父 Agent 将工具派生的不可信值写入子 Agent 的指令参数，子 Agent 再将其作为可信指令处理。该论证有拓扑、表达能力和工具返回值等前提，不能扩展为“所有多 Agent 系统均不安全”。[Paper: Section III-A; Section III-C; Section VII]

**C2**：S2 记载的修复采用可信 `message` 与不透明 `variables` 双通道，并依靠运行时强制。这支持把信任边界列为文献比较维度，不支持把双通道本身等同于所有数据流风险均已解决。[Paper: Section IV-A; Section IV-B; Section IV-C]

**C7**：S2 同时限定其经验结果与论证范围，包括基准内既有攻击、平凡安全策略、解释器依赖追踪限制，以及树状拓扑等。因此应区分控制流保证、数据流策略与更强信息流性质，不能以低观察攻击成功率替代完整安全保证。[Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2]

### 2.2 攻击类型与评估配置不能混为一谈

**C3**：S3 的总结将“逐动作防御对被攻陷 Agent 攻击的收益”与“共谋条件下未测得保护”加以区分。这里应理解为被测场景、机制和判据下的观察，而不是所有逐动作防御在所有共谋情形下均无效的定理。本版不重复原报告中的数值，以免在尚未核对结果表与条件时进一步传播。[Paper: PDF p. 1, Abstract；PDF p. 8–9, Section 5；PDF p. 9, Section 6]

**C4**：S1 对 ORBIT 的二次综合介绍了固定其他条件、改变拓扑、记忆可见性或威胁模型等因素的受控评估目标。它可支持把配置条件记录进比较表，但不能单凭作者动机认定整个领域已经存在“复现危机”。[Paper: PDF p. 2–3, Section 1；PDF p. 5, Section 3.1–3.2]

**C8**：S3 的批判性分析提示，判定模型差异和样本量可能影响跨条件比较与零结果解释。这是笔记作者提出的解释风险，并非已经验证的偏差大小，也不能据此否定全部原论文结果。[Paper: PDF p. 34, Table 10 caption] [Paper: PDF p. 36–37, Appendix J.4；PDF p. 38, Table 17；PDF p. 39, Table 19]

### 2.3 MADBench 摘录提供的是问题框架，而不是结果答案

**C5**：S4 提出比较攻击层、共谋模式、被攻陷 Agent 数、辩论轮数和底层模型等因素的问题。本次摘录并未提供这些变量的结果表，因此不能写成“它们已被证明会系统性改变传播路径”，也不能判断变化方向或大小。[Paper: PDF p. 2 §1, p. 7 RQ1/RQ2]

**C9**：S4 将准确率、成本、未授权读和未授权写纳入问题拆分，并提出相对单 Agent 基线的比较视角。这支持区分答案质量与权限安全两个层面；不支持声称 MADBench 已验证某项防御，或已经证明多 Agent 在某一指标上更安全。[Paper: PDF p. 4–6 §3.1–3.3]

### 2.4 联系与不可直接合并之处

**C6**：S1 与 S2 存在转述关系，不能把相同结论出现两次当成两项独立研究的相互印证。S2 的跨边界信任原则可以作为组织讨论的线索，但不能据此认为 ORBIT 的所有共谋现象或 MADBench 的全部攻击目标具有同一失效原因。[Paper: Section VI-A 末段; Section VII]

**C10**：本报告建议以“协作拓扑—攻击者控制范围—信任边界—安全目标—评估判据—效用代价”为共同字段整理文献。该分类是写作建议，不是原论文共同确认的新理论。各来源的任务、攻击和指标不一致，目前不进行统一优劣排名。

## 3. 候选写作方向与材料缺口

| 候选方向 | 已有材料能支持的内容 | 尚缺材料 | 写作边界 |
| --- | --- | --- | --- |
| 多 Agent 安全中的信任边界与权限风险 | C1、C2、C7、C9 可组织控制流与权限目标的对照 | MADBench 结果摘录、各文献权限定义与具体失败案例 | 文献比较，不宣称提出并验证了新防护 |
| 多 Agent 安全评估的配置差异与比较边界 | C3、C4、C8 可讨论攻击类型、配置与判据 | ORBIT 原始表格、完整设置及其他同类文献 | 不使用“复现危机”等超出材料的判断 |
| 从答案质量到权限安全的文献分类 | C5、C9 提供问题轴，C1、C7 提供安全性质边界 | MADBench 对应目标的原文定义和结果，更多已审核论文 | 只能提出分类视角，不能证明该分类具有创新性 |

现有材料更适合先形成范围明确的文献比较文章或研究现状分析。尚不具备新方法实验论文的结果基础；候选方向的创新性也未经过独立检索确认。

## 4. 论文提纲与章节材料

暂定标题：**多 Agent 系统安全中的信任边界、攻击目标与评估条件：基于已有论文卡的比较分析**。

| 章节 | 写作任务与子节 | 主张与来源 | 可用原有定位 | 待补材料 |
| --- | --- | --- | --- | --- |
| 摘要 | 交代比较对象、范围和主要边界，不预写有效性结论 | C1、C4、C9；S1、S2、S4 | [Paper: Section III-A; Section III-C; Section VII]；[Paper: PDF p. 4–6 §3.1–3.3] | 正文与来源核对完成后再定稿 |
| 1 引言 | 1.1 协作与信任边界；1.2 答案质量和权限安全的区别 | C1、C9；S2、S4 | [Paper: Section III-A; Section III-C; Section VII]；[Paper: PDF p. 4–6 §3.1–3.3] | 更完整的问题背景与引用 |
| 2 范围与材料组织 | 2.1 纳入笔记；2.2 摘录限制；2.3 主张分级 | C6、C10；S1、S2、S3、S4 | 不适用（本次材料组织建议） | 纳入排除标准；不将其冒称系统检索 |
| 3 安全性质与分类 | 3.1 控制流及数据流；3.2 权限目标；3.3 攻击者控制范围 | C2、C7、C9；S2、S4 | [Paper: Section IV-A; Section IV-B; Section IV-C]；[Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2]；[Paper: PDF p. 4–6 §3.1–3.3] | 对齐术语，核对各自威胁模型 |
| 4 跨文献比较 | 4.1 单体保证的组合；4.2 共谋与逐动作防御；4.3 辩论变量 | C1、C3、C4、C5；S1、S2、S3、S4 | [Paper: Section III-A; Section III-C; Section VII]；[Paper: PDF p. 1, Abstract；PDF p. 8–9, Section 5；PDF p. 9, Section 6]；[Paper: PDF p. 2 §1, p. 7 RQ1/RQ2] | 补 MADBench 结果；补各实验设置；不统一排名 |
| 5 讨论 | 5.1 可迁移原则；5.2 观察与解释；5.3 测量不确定性 | C6、C7、C8、C10；S1、S2、S3 | [Paper: Section VI-A 末段; Section VII]；[Paper: PDF p. 34, Table 10 caption] | 区分原作者讨论与笔记批评，补反例与反对观点 |
| 6 局限性 | 摘录选择、样本文献有限、二次来源依赖及未核对项目 | C5、C6、C8；S1、S2、S3、S4 | 不适用（本次报告范围说明） | 明列尚未完成的原文与文献覆盖核验 |
| 7 结论 | 只归纳已支持的比较，不宣布新防护有效 | C1、C7、C9、C10；S2、S4 | [Paper: Section III-A; Section III-C; Section VII]；[Paper: PDF p. 4–6 §3.1–3.3] | 随正文证据核对结果收窄结论 |
| 参考文献 | 完整书目信息及版本 | S2、S3、S4；S1 作为笔记来源另记 | 定位缺失（书目信息需单独核验） | 作者、年份、版本、入口与发表状态 |

## 5. 主张与来源映射

| 主张编号 | 主张内容 | 来源编号及笔记路径 | 原有证据定位 | 证据类型 | 适用边界 | 拟用于章节 | 待补材料 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | 层级系统内个体 CaMeL 保证不自动组合为系统级 CFI，存在边界洗白机制 | S2：Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section III-A; Section III-C; Section VII] | 原论文结论（笔记转述） | 仅在论文所述架构与论证前提内 | 1、4 | 核对原文假设与反例 |
| C2 | message/variables 双通道与运行时强制用于处理该控制流边界问题 | S2：Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section IV-A; Section IV-B; Section IV-C] | 原论文结论（笔记转述） | 不等于数据流与所有权限风险均已解决 | 3 | 原文机制及形式化条件 |
| C3 | ORBIT 笔记区分逐动作防御的被攻陷 Agent 收益与被测共谋条件下的零测得收益 | S3：Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 1, Abstract；PDF p. 8–9, Section 5；PDF p. 9, Section 6] | 原论文结论（笔记转述） | 不外推为所有共谋均无防护 | 4 | 具体表格、配置、样本与不确定性 |
| C4 | 受控比较需记录拓扑、记忆、威胁模型与防御配置 | S1：Agent-IFC/20_Themes/多Agent协作的安全防护.md | [Paper: PDF p. 2–3, Section 1；PDF p. 5, Section 3.1–3.2] | 笔记分析（二次综合） | 框架目标不证明全领域存在复现危机 | 4 | 回溯 ORBIT 对应原文与配置 |
| C5 | MADBench 摘录提出 R、f、模型与攻击层的影响问题，尚不足以陈述影响结果 | S4：Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 2 §1, p. 7 RQ1/RQ2] | 原论文研究问题 | 本次摘录未提供结果，不等于原论文未研究 | 4、6 | 原文结果与完整证据链 |
| C6 | 主题笔记与论文卡不构成独立验证；跨边界信任原则不能替代跨论文机制证明 | S1：Agent-IFC/20_Themes/多Agent协作的安全防护.md；S2：Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section VI-A 末段; Section VII] | 本次建议（引用 S2 原则，说明来源依赖） | 不是多种攻击的统一因果解释 | 2、5、6 | 标记每项二次引用的上游来源 |
| C7 | CaMeL 结果受既有攻击、平凡策略、实现假设与拓扑限制 | S2：Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2] | 原论文结论（笔记转述的局限） | 不扩展为全面系统安全保证 | 3、5、7 | 原文局限及保证范围 |
| C8 | judge 与样本量差异构成比较和零结果解释时应检查的风险 | S3：Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 34, Table 10 caption]；[Paper: PDF p. 36–37, Appendix J.4；PDF p. 38, Table 17；PDF p. 39, Table 19] | 笔记分析 | 不代表已测出偏差大小，不据此否定整项研究 | 5、6 | 核对 caption 与样本口径 |
| C9 | MADBench 研究问题区分准确率、成本及未授权读写目标 | S4：Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 4–6 §3.1–3.3] | 原论文研究问题 | 不包含本次摘录未给出的结果或防御效果 | 1、3、7 | 各目标定义及结果出处 |
| C10 | 用共同字段组织文献比较，不进行不可比设置下的性能排名 | S1：Agent-IFC/20_Themes/多Agent协作的安全防护.md；S2：Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md；S3：Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md；S4：Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | 不适用（本次建议） | 本次建议 | 未建立新理论或创新性结论 | 2、5、7 | 补充文献并核对字段可比性 |

## 6. 后续写作清单

1. 优先补齐 MADBench 的结果段与表格到论文卡，再更新本次可用摘录；主要影响 C5、C9 与第 4 章。当前不猜测结果方向。
2. 对 C1、C2、C3、C7 的原文位置、条件与术语逐项核对；特别区分定理、经验观察、演示和作者解释。
3. 将 C8 的批判性分析保留为待核对项目，不把潜在测量问题写成已经证实的结果错误。
4. 核对 S2、S3、S4 的作者、版本和发表信息。路径中的 unknown 不是可靠的书目年份。
5. 用上述共同字段补充可比文献；记录纳入范围，不在缺乏检索依据时宣称“首次”或“填补空白”。
6. 先起草第 2 章材料范围和第 3 章分类，再写第 4 章比较；摘要和结论最后根据证据核对结果定稿。本阶段不要求开展实验。

## 本次修订记录

- 把 MADBench 变量效应从已证实结果改为研究问题，明确本次没有可用结果摘录。
- 补齐映射表中的完整笔记路径，保留实际输入中的完整定位字符串。
- 将 ORBIT 的观察限定到被测条件，区分笔记批评和原论文结论。
- 将“复现危机”等超范围表达改为配置差异和比较边界；不声称已经验证创新性或形成可投稿论文。
