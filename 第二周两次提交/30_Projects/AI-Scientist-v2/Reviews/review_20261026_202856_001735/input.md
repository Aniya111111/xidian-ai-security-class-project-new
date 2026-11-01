输入范围为文献综合、提纲及主张映射。未开展新实验。
证据仅是提供的笔记摘录，不是经重新核验的全文。

<MANUSCRIPT>
# AI-Researcher Obsidian 构思结果

- 运行时间：2026-10-25T20:18:42+08:00
- Reference 补充材料：无

## 本次研究问题

请根据 Reference 中的最终修订稿，生成一篇中文文献综合型论文初稿。

论文主题：多 Agent 系统安全中的边界信任、协议可组合性与评估框架。

要求：
1. 只使用 Reference 中的内容，不补充未经提供的论文事实、实验结果或数字。
2. 区分原论文结论、笔记分析和本文作者的组织性建议。
3. 保留 C1–C10 主张编号及其来源路径。
4. 将 MADBench 写成待核验的问题导向材料，不声称其已完成或缺少系统化评测。
5. 明确说明本文没有开展新实验。
6. 生成标题、摘要、引言、相关工作、文献综合、讨论、局限性、结论和参考文献占位。
7. 单独生成“主张—来源映射表”。
8. 输出两个部分：
   A. 论文正文初稿
   B. 主张—来源映射表

---

Evidence bundle: E:\oblidian\file\safetyAI\Agent-IFC\30_Projects\AI-Researcher\References\multi-agent-security.reference.md
Evidence bundle SHA-256: 13e806374faba89dc1116c5b855e38269c7cc3cd81875d7fa87ceaf8a13c6bd6
Selected evidence: 15,988 chars from 4 sources
- Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks | Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | 5200 chars
- 多Agent协作的安全防护 | Agent-IFC/20_Themes/多Agent协作的安全防护.md | 2206 chars
- ORBIT: A Framework for Multi-Agent Safety and Security Evaluations | Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | 4736 chars
- MADBench: Benchmarking the Security of Multi-Agent Debate | Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | 2804 chars

# A. 论文正文初稿

## 多Agent系统安全中的边界信任、协议可组合性与评估框架：文献综合与写作指引初稿

### 摘要
随着大型语言模型驱动的多Agent协作架构广泛部署于企业编排与自动化工作流中，跨Agent调用的安全属性面临严重的可组合性挑战。本文基于所提供的研究注记素材，系统梳理了边界信任机制、协议层指令通道保护以及多场景安全评估框架的核心发现与分析视角。本综合明确界定：逐Agent部署独立安全护栏并不自动推导至系统级安全；跨边界“洗白”是破坏层级架构控制流完整性的关键失效机制；而现有评估框架在配置空间覆盖、度量标准一致性与非自适应攻击假设等方面仍存在显著的方法论缺口。本文严格限定于所供注记材料的二次综合，**未开展任何新实验**，亦未引入外部验证结果。文中各项主张均标注原始结论、笔记分析与作者组织建议的归属边界，并将基准测评材料定位为待核验的问题导向参考，以期为后续协议设计与系统化评测研究提供清晰的文献合成与写作指引。

### 引言
多Agent系统的典型特征是中心Orchestrator向专业化子Agent委派子任务，并通过自然语言指令、共享记忆或变量通道传递上下文。该架构在提升推理能力与任务覆盖面的同时，也显著扩大了间接提示注入与权限滥用的攻击面。当每个Agent单独配备安全机制时，研究者常预设安全属性具备模块可组合性；然而，边界处的信息流转模式往往打破该假设。

本文聚焦三个交叉维度：(1) 边界信任的维持机制与控制流完整性(CFI)在层级架构中的可组合性；(2) 协议层双通道分离与运行时策略强制的设计逻辑；(3) 面向多Agent协作的安全评估框架的配置口径、度量有效性与局限。本文严格遵循以下原则：(i) 所有论述仅来源于所附Obsidian注记束；(ii) 区分原论文结论、笔记作者的批判性分析与本文的组织性写作建议；(iii) 将基准评测材料视为待核验的问题导向素材，不提前推断其已完成或缺失系统化验证；(iv) **明确声明本文没有开展任何新实验**。下文首先划定文献范围，随后进行主题综合，讨论测量与协议设计的交叉挑战，最后归纳局限与后续写作方向。

### 一、 相关工作与文献范围界定
本文综合素材来自四个选定注记（S1–S4），覆盖单一协议扩展、主题级综述、跨场景评估框架与辩论基准测评四类材料。各素材角色如下：
- **S1** 针对CaMeL系架构在多Agent层级调用中的安全性质验证，涵盖边界洗白反例、解释器隐式依赖漏检、策略选择与效用代价等关键议题。
- **S2** 为二级综合主题笔记，提炼S1的研究问题、方法输入输出、正确结论解释与边界修复方案，属元综述而非独立复现。
- **S3** 提出ORBIT评估框架，记录攻击注册表构造、威胁模型四维参数、Judge模型一致性、共谋证据强度不对称等实现细节与已知局限。
- **S4** 介绍MADBench基准，围绕对抗性影响在辩论系统中的吸收/放大机制设定研究问题，指出指标口径（如相对放大率分母为清洁对答任务）、任务类型混合与防御机制空白等方法学特征。

本综合不涉及对上述论文原文的新检索、代码审计或实证复现。注记中的批判性观察仅代表笔记作者的推演与检验设想，不构成对原论文结论的替代验证。

### 二、 文献综合：边界信任、协议可组合性与评估框架
#### 2.1 边界信任与协议可组合性
在层级式 `agent-as-tool` 架构中，安全属性的模块化部署面临结构性断裂。**[原论文结论]** 逐Agent部署独立机制无法保证系统级控制流完整性；当父Agent将工具派生的不可信值直接写入子Agent的自然语言指令参数时，子Agent将调用者默认为可信用户，导致“边界洗白” **[S1; S2]**。该现象表明，仅依靠局部解释器或策略检查不足以阻断跨边界的数据流/指令流篡改。为此，协议层将调用边界显式双通道化被提出为必要修复路径：`message` 通道仅承载可信指令（不得依赖任何工具输出），`variables` 通道携带受限且不透明值，配合运行时 `get_variable` 取用与策略强制，可在假设拓扑为有根树的前提下恢复控制流预期 **[S1; S2]**。

然而，协议论证与实现保障之间存在断层。解释器的依赖追踪可能遗漏隐式流（如条件分支外的变量赋值），导致污染值仍被标记为可信；同时，会话历史跨调用保留会模糊“新episode”的可信边界 **[S1]**。此外，分支选择权本身构成低影响力攻击面：不可信数据虽不能新增执行路径，但可在既定分支内引导外部可见输出，违反某些更强安全性质 **[S1]**。因此，边界信任并非单纯依赖提示增强或模板隔离，而需形式化刻画指令通道完整性(CFI)与分支中立性(TIPNI)的相对强度与适用范围 **[S1]**。

#### 2.2 评估框架的配置空间与度量有效性
面向多Agent系统的横向比较日益依赖统一评测栈。评估框架的价值在于将拓扑、记忆可见性、威胁模型与防御机制解耦为可调自变量。然而，实践报告呈现多重口径错位。**[笔记分析]** 攻击类型注册表宣称支持多维威胁能力，但实证扫描往往局限于防御策略、模型与拓扑，缺乏对知识水平、预算与持久化维度的因子遍历 **[S3]**。成功判定标准并存语法匹配与LLM judge语义赋值，同一轮交互可能出现判据触发但judge评分中性，或反之，导致攻击成功率(ASR)与防御有效性(PD)的语义映射发生偏移 **[S3]**。此外，Judge模型的跨条件切换（如防御格使用高版本模型评判而基线格使用另一模型）可能引入评分漂移，使低ASR区间的组间差异对Judge配置高度敏感 **[S3]**。

记忆可见性的默认配置同样构成隐性混杂因素。多数共享标志默认关闭，仅在特定拓扑或场景下开启，使得“共享记忆污染”传播路径的实际覆盖率可能被低估 **[S3]**。这些观测共同指向一个方法论要求：评估框架必须公开配置种子、Judge一致性阈值与等价性检验预案，否则“某防御在XX拓扑最强”类结论仅反映该切片的经验噪声。

#### 2.3 辩论系统与基准测评的问题导向定位
MADBench将对抗性影响在多Agent辩论(MAD)中的流向拆解为准确率、成本、越权读/写的相对放大率(AF)与翻转率(ASR)。其核心价值在于提供分层视角的对照协议。但相关指标需置于待核验语境下审慎解读：**[笔记分析]** AF以基线正确任务数为分母，当基线绝对错误率高或出现零除情况时，比值趋于无穷或掩盖真实危害；ASR本质为翻转率而非总体错误率，二者结合使用方可还原风险全貌 **[S4]**。此外，辩论聚合器同时承担错误吸收源与单点信任枢纽的双重角色，其架构张力决定了防护应优先加固聚合节点还是重构投票/核验范式 **[S4]**。目前该基准尚未接入过滤、来源标记或写白名单等防御机制，其研究问题本身属于待验证的前提假设，不应直接外推为“现有防护无效”或“MAD结构固有脆弱”的定论 **[S4]**。

### 三、 讨论：测量有效性与协议设计的交叉挑战
上述文献片段揭示了多Agent安全研究中反复出现的三组张力：
1. **协议可组合性与实现可靠性的落差**：边界双通道分离在形式论证中成立，但实际执行受限于解释器隐式依赖追踪精度、会话历史管理规则与隐蔽通道容量估算。安全性质的强度对比（CFI vs TIPNI）需在具体拓扑与任务分布上形式化刻画，而非停留在定性断言 **[S1]**。
2. **评估配置的暴露度与统计功效**：框架的模块化设计理想与现实算力/时延预算相冲突。Judge延迟、小样本区间宽度、跨场景异构导入以及非自适应固定载荷，共同削弱了“某设置泛化至全空间”的主张力度。报告方向性结果时必须同步披露功效分析或预设定价边界检验 **[S3]**。
3. **指标语义与归因归责**：相对放大率、翻转率、Judge评分与工具调用日志需保持同构映射。任务类型（纯推理含工具 vs 不含）、授权集预言机是否可写、并行度与阶段token消耗等混杂变量若未分层剥离，将导致结论在跨架构迁移时失效 **[S4]**。

本文作者建议后续写作优先采用“场景切片×度量正交”的叙述结构：先明确协议边界的可达形式性质，再对齐对应评估框架的配置矩阵，最后标注指标口径与统计功效的对应关系。避免将单一基准的负结果泛化为全局防御盲区。

### 四、 局限性
本综合受限于所供注记束的范围与方法属性：
- 仅依据已导出注记进行文本综合，未经过原始论文全文精读或代码仓库比对；
- 主题笔记(S2)为二次综合，其推论依赖S1的原始论证链条；
- MADBench等基准材料仅记录研究问题与初步指标定义，未提供防御实施或大规模自适应红队结果，现阶段不宜作为安全性定论依据；
- 文中所有关于效用代价、模型性能趋势、攻击成功率与Judge一致性问题的讨论，均标注为笔记作者的分析视角或待检验假说，不代表已建立的因果规律；
- 未涉及任何实验设计或新数据采集，仅服务于文献合成与写作大纲构建。

### 五、 结论
本文系统梳理了多Agent系统安全中边界信任维持、协议可组合性修复路径以及评估框架配置与度量有效性的核心文献线索。综合表明：逐Agent安全机制的简单叠加无法抵御跨边界洗白；显式双通道分离与运行时策略强制是恢复控制流预期的必要条件，但其落地受限于隐式依赖追踪、会话管理与隐蔽通道约束。评估框架的理论模块化优势在实践中遭遇统计功效、Judge漂移、指标口径错位与非自适应攻击假设的多重掣肘。未来写作与研究工作应优先建立协议性质到评估指标的严格映射字典，并在公开配置前提下补充自适应红队、功效分析与等价边界检验。本研究仅作文献综合与写作指引，未开展实证验证，所有主张均可追溯至所供注记及其标注的原始定位。

### 参考文献
[S1] Peters-Gill, J. (2026). Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks. [笔记路径: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md]  
[S2] 多Agent协作的安全防护. [笔记路径: Agent-IFC/20_Themes/多Agent协作的安全防护.md]  
[S3] Hagag, B. ORBIT: A Framework for Multi-Agent Safety and Security Evaluations. [笔记路径: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md]  
[S4] Liu, Y. MADBench: Benchmarking the Security of Multi-Agent Debate. [笔记路径: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md]  

---

# B. 主张—来源映射表

| 主张编号 | 主张内容 | 来源编号及笔记路径 | 原有证据定位 | 证据类型 | 适用边界 | 拟用于章节 | 待补材料 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| C1 | 逐Agent部署独立安全机制不自动保证层级多Agent系统的控制流完整性与指令通道完整性。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | [Paper: Abstract; Section I 末段; Section III]; [Paper: Section III-A; Section III-C; Section VII] | 原论文结论 | 层级式 agent-as-tool 拓扑；假设子Agent无跨调用状态保留 | 引言、2.1节、结论 | 一般拓扑（DAG/点对点）下的形式化证明；跨调用会话管理的实证基线 |
| C2 | 跨边界“洗白”源于父Agent将工具派生不可信值写入子Agent自然语言指令参数，破坏子Agent对调用者的可信假设。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | [Paper: Section I; Section I 相关工作段; Section III-A 末段]; [Paper: Section III-A; Section III-B; Table III–V] | 原论文结论 | 开放数据源注入；平凡安全策略 $S=\emptyset$ 配置 | 2.1节、讨论 | 非平凡策略下的洗白发生率与误报率消融实验数据 |
| C3 | 双通道分离（message为可信指令，variables为受限变量）及运行时策略强制可在假设拓扑中恢复边界信任。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | [Paper: Sec…]; [Paper: Section VI-A; Section VII] | 原论文结论 | 有根树拓扑；插件式解释器扩展；完整返回schema增补前提 | 2.1节、结论 | 缺失返回schema时的效用代价定量分解；多模型版本的稳定性检验 |
| C4 | 现有评估框架在攻击类型分类、威胁模型参数设定与实证覆盖维度间存在口径不一致，影响自变量定位。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 5, Section 3.2 Layer 3；PDF p. 28, Table 5]; [Paper: PDF p. 28, Appendix G；PDF p. 8, Section 5] | 笔记分析 | ORBIT框架 v1 版本；注册键与Table条目对照周期 | 2.2节、讨论 | 代码仓库注册键清单核对；knowledge level × persistence 因子扫描结果 |
| C5 | 成功判据的语法判定与LLM judge语义赋值存在映射断裂，可能导致ASR与PD指标语义偏移。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 28, Appendix G「Success criteria」；PDF p. 6, Section 3.4] | 笔记分析 | 多判定标准并行的评测管线；跨条件Judge切换场景 | 2.2节、讨论 | 判据成功 vs Judge分类的一致率交叉列联表；Judge模型交换测试报告 |
| C6 | 辩论聚合器同时承担主要吸收来源与单点信任角色，其设计张力决定防护部署的关键瓶颈位置。 | S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 8 §4.1, p. 9 §4.2 M6] | 笔记分析 | MAD任务设置；聚合器保留工具权限前提 | 2.3节、讨论 | 聚合改为无工具权限纯投票/证据核验的对照ASR/IRW/cost数据 |
| C7 | 当前对抗性评测普遍依赖固定载荷与非自适应攻击，可能高估静态防御效果，且未充分扫描知识水平与持久化等维度。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 10, Section 7] | 原论文结论 / 笔记分析 | 框架支持的自适应后续预留；现实算力限制下的代表性切片 | 2.2节、局限性 | 自适应红队对照实验；不同Knowledge Level下的边际效应曲线 |
| C8 | 隐蔽通道容量削减与传统confinement机制在多Agent复杂通信下可能失效，需建立系统级约束保证。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md | [Paper: Section VI-B2] | 原论文结论 | Agent具策略性、渠道复杂度递增场景；排除外部重试循环特例 | 2.1节、讨论 | 系统级confinement形式化规约；隐蔽通道枚举与容量削减的实测报告 |
| C9 | MADBench提供的相对放大率(AF)与翻转率(ASR)指标需结合基线错误率与任务类型分层解读，防止∞值或分母偏差导致风险低估。 | S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 6 Eq.7, p. 7 Table 2, p. 25 脚注]; [Paper: PDF p. 6 Eq.5, p. 25 Table 9a]; [Paper: PDF p. 6–7 §4 Tasks, p. 7 Table 2] | 笔记分析 | QA类任务与工作区任务混合场景；授权预言机固定前提 | 2.3节、讨论 | 绝对差值+置信区间替代方案；清洗错误率与攻击错误率联合报告基线 |
| C10 | 评估框架的默认配置（如记忆可见性标志、Judge模型选择）若未在报告中显式控制，可能成为未被识别的混杂因素。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 33, Appendix I, Table 9；PDF p. 38, Table 17 仅含 Star+SharedMem]; [Paper: PDF p. 34, Table 10 caption] | 笔记分析 | 低共享默认运行态；跨格子Judge模型不一致配置 | 2.2节、讨论 | 六标志扫描的PD/ASR变化报告；Judge双向一致性检验与漂移幅度量化 |

**使用说明与边界声明**：
- 本表严格遵循“主张—来源映射”规范，每行均包含指定列顺序与完整笔记路径。
- `[证据类型]` 区分“原论文结论”、“笔记分析”与“待补材料/不适用”。凡标注“笔记分析”者均为注记作者的批判性推演或检验设想，非原论文已验证发现。
- `[原有证据定位]` 字段逐字复制自注记束 `[Paper: ...]` 字符串，未作缩写、翻译或标点规范化。
- MADBench相关材料(S4)仅用于表征指标口径争议与研究问题导向，不视为已完成防御评估或系统性评测定论。
- 本文仅为文献综合初稿与写作大纲，**未开展任何新实验**，未引入外部数字或示例测量。后续写作需按“待补材料”列逐项核证或替换为公开可用基线。

## 本地来源格式检查

- 定位未在本次摘录中原样出现：[Paper: Sec…]
- 定位未在本次摘录中原样出现：[Paper: ...]

此检查仅核对定位字符串、来源编号与路径，不核验主张语义、原论文真实性或证据充分性。不会自动重试模型，也不代表学术审核通过。

</MANUSCRIPT>

<SOURCE_EXCERPTS>
# Selected evidence

### MADBench: Benchmarking the Security of Multi-Agent Debate
Source note: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md
Source note SHA-256: d5910beb563fdc571b36b17c91930791e4430efa0228ea8db7440548a2e055c8

### 结论—证据矩阵

| 编号 | 实验 | 被检验的结论 | 比较与条件 | 结果 | 可支持的结论 | 不可支持的更强结论 | 来源 | 人工核查 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 分层攻击分类 | MAD 攻击面可按编排/Agent/资源三层组织，6 个攻击族中 M1–M4 迁移自单 Agent、M5–M6 为多 Agent 特有 | 设计性论断，非实验 | 6 族 × 3 层的形式化定义与相关工作对应 | 该分类是本基准的组织框架，M5/M6 是新增面 | 「这 6 族已覆盖 MAD 全部攻击面」——论文未主张穷尽 | [Paper: PDF p. 2 Fig.1, p. 5–6 §3.2 Table 1] | AI 预审支持；用户最终确认 |
| C02 | 基准规模 | 356 源任务展开为 3,958 个安全测试用例 | 4 个公开数据集 | 100+100+56+100=356 | 规模与来源可核对 | 「覆盖真实部署任务分布」 | [Paper: PDF p. 1 Abstract, p. 6–7 §4 Tasks, p. 24 Table 7–8] | AI 预审支持；用户最终确认 |
| C03 | RQ1 准确率吸收 | 相对单 Agent，MAD 在问答任务上吸收针对准确率的攻击 | M3、M4 在 QA(fact) 上的 AF_ASR | M3 AF_ASR=0.74，M4 AF_ASR=0.87（均 <1） | 在 QA 任务与这两个攻击族上，MAD 降低了攻击对答案的影响 | 「MAD 总体上让系统更安全」；「任何攻击族都被吸收」（M2 的 AF_ASR=1.05 >1） | [Paper: PDF p. 7 Table 2, p. 8 §4.1] | AI 预审支持；用户最终确认 |
| C04 | RQ1 权限放大 | MAD 放大未授权读/写，且在工作区任务上放大多数指标 | M2（workspace）4 个目标 × 3 个指标的 AF | 作者称 M2 在 12 项比较中 11 项放大；AF_IRW 最高 3.00、AF_ASR 最高 3.09 | 注入信息可经 Agent 响应传播并诱发越权操作，工作区任务放大明显 | 「放大幅度稳定可外推」——部分单元格样本极少 | [Paper: PDF p. 7 Table 2, p. 8 §4.1] | AI 预审支持；用户最终确认 |
| C05 | RQ1 QA 任务上的 IRW | 即使 MAD 吸收 M3/M4 的 ASR 与 cost，仍放大未授权读/写 | M3/M4 在 QA 上的 AF_IRW | M3 未授权读 1.05、未授权写 1.41；M4 未授权读 1.02 | 准确率吸收与权限放大可在同一攻击族内并存 | 「IRW 数值差异都显著」——M3/M4 accuracy/cost 行的 IRW 为 ∞（基线为 0） | [Paper: PDF p. 7 Table 2, p. 8 §4.1] | AI 预审支持；用户最终确认 |
| C06 | Case B 案例 | 单 Agent 只越权读、不越权写| C06 | Case B 案例（M2 + workspace） | 单 Agent 只越权读、不越权写；MAD 把它变成执行未授权付款 | 同一 payload、同一入口，AgentDojo 地址更新任务 | 单 Agent：读 `bill-december-2023.txt` 但只执行授权地址更新；MAD：两名 Agent 初时主张付款，辩论后 5/5 支持，编排器输出「update the address, send money(98.70)」并产生 UR+UW | 辩论可把「未导致越权写的越权读」升级为「已执行的越权写」 | 「此类升级在全部工作区任务上普遍发生」——这是单个案例 | [Paper: PDF p. 8 §4.1 Case study, p. 8 Table 3] | AI 预审支持；用户最终确认 |
| C07 | Case A 案例（M3 + SealQA） | 3/5 Agent 的 RAG 被投毒仍答对 | 编排器聚合时比较答案与 supporting evidence | 两名干净 RAG 的 Agent 提出 Clauser，编排器返回正确答案，攻击被吸收 | 聚合器可基于证据质量否决多数错误提案 | 「聚合器总能识别伪造证据」；「多数投票也会吸收」 | [Paper: PDF p. 8 §4.1 Case study, p. 8 Table 3, p. 21 §D.5] | AI 预审支持；用户最终确认 |
| C08 | RQ2 M5 共谋强度 | 共谋模式对准确率的冲击最大，且随被攻陷数 $f$ 上升 | 100 个 QA 任务，$f\in\{1,2,3\}$，三模式 | colluding ASR 14.81 → 16.98 → 28.30；independent 7.55 → 11.32 → 11.32；inconsistent（$f=3$）5.66 | 指向同一错误目标的协同提案比互相竞争的错误提案更能左右编排器决策 | 「$f$ 越大必然越危险」——$f$ 上限为 3（$n=5$），未测多数被攻陷情形 | [Paper: PDF p. 9 Table 4a, p. 9 §4.2] | AI 预审支持；用户最终确认 |
| C09 | RQ2 M5 模式—目标反转 | 不一致模式（equivocation）ASR 最低但 IRW 最高 | $f=3$ 三模式对比 | IRW：inconsistent 74.00 > independent 52.00 > colluding 49.00（作者正文以 49.00/52.00 对比 74.00）；ASR：5.66 最低 | 相互矛盾的提案削弱单一错误答案的支持，却更易引入多种越权动作 | 「equivocation 是最危险的攻击族」——仅在其 IRW 维度成立 | [Paper: PDF p. 9 Table 4a, p. 9 §4.2] | AI 预审支持；用户最终确认 |
| C10 | RQ2 未授权写的来源 | 最终输出答对也不阻止越权写：编排器在 finalize 时自行创建文件 | $y^\star=$ Avatar 的 QA 任务，M5 三模式 | colluding 输出错误答案但无越权写；independent/inconsistent 均答对却各执行一次 create file（`box office ranking analysis.txt`、`highest grossing film 2024.json`）；三运行均无越权读 | 准确率指标会漏掉由编排器自发产生的越权动作 | 「该越权写是协作特有现象」——单 Agent 是否同样自发写文件未在此案例中报告 | [Paper: PDF p. 9 §4.2 case study, p. 21–22 §D.6 logs] | AI 预审支持；用户最终确认 |
| C11 | RQ2 底层模型消融 | 更强的底层模型同时降低 ASR、IRW 与 cost | M5 colluding $f=3$，100 QA 任务 | gpt-4o 28.30/49.00/73.08；GPT-5 6.90/12.00/62.19；GPT-6 Astra 3.28/7.00/50.57 | 在该配置下模型能力与三项攻击指标同向改善 | 「换更强模型即安全」——未测开源/本地模型，也未测 M1–M4 的模型消融 | [Paper: PDF p. 9 Table 4b, p. 9 §4.2] | AI 预审支持；用户最终确认 |
| C12 | RQ2 M6 | 被攻陷编排器可轻易使 MAD 偏离正常行为 | 每个安全目标构造一个 goal-specific 变体 | ASR 100.00、IRW 100.00、cost 180.94 | 控制派发、聚合与写工具的组件是单点信任，可覆盖辩论 Agent 的建议 | 「这是一项发现」——作者自述「not surprisingly」，且结果由攻击构造方式直接决定 | [Paper: PDF p. 9 Table 4c, p. 9 §4.2] | AI 预审支持；用户最终确认 |
| C13 | 附录 D.4 C2W | 输出被翻转主要不是靠说服诚实 Agent | M5 三模式 × $f$，诚实 Agent 的 Propose→Debate 答案变化 | C2W 在所有模式下都低，最高为 colluding $f=3$ 的 3.26% | 攻击影响集中在编排器聚合环节，而非诚实 Agent 的信念改变 | 「诚实 Agent 不可被说服」——作者明示更精心设计的提案与证据可能提高 C2W，留待研究 | [Paper: PDF p. 19 §D.4, Table 11] | AI 预审支持；用户最终确认 |
| C14 | 附录 D.2 轮数消融 | 增加辩论轮数不改变结果 | $R\in\{1,2,3\}$，$f=3$ colluding | ASR 28.30/26.92/33.33；IRW 49.00/55.00/47.00；cost 73.08/74.61/77.44 | 「更多轮 Debate 进一步吸收异常行为」的先前假设在本设置下未获支持 | 「轮数永远无用」——$R>3$ 与不同 $n$ 未测 | [Paper: PDF p. 18 §D.2, Table 10] | AI 预审支持；用户最终确认 |
| C15 | 附录 D.3 目标切换 | 同一被攻陷预算下，「要答案」难、「要动作」易 | M5 参考配置固定，只改 payload 所求目标 | 答案目标 ASR 28.30，其余三目标 1.89–3.77；动作目标 IRW 读 100.00、写 96.00 | 群体对错误答案有抵抗，对越权调用几乎无抵抗；该现象在资源层（§4.1）与 Agent 层同时成立 | 「动作类攻击恒为 100%」——依赖 $R^\star_s/W^\star_s$ 的评测设定 | [Paper: PDF p. 18 §D.3] | AI 预审支持；用户最终确认 |
| C16 | RQ1 M1 | 直接提示注入（越狱）在 MAD 下被吸收且绝对成功率低 | JailbreakBench 100 条有害请求，只报 ASR | MAD 下 ASR 2.38，AF 0.88 | 三 Agent 辩论未放大越狱类攻击 | 「MAD 对内容安全有效」——单一攻击族、单一指标 | [Paper: PDF p. 8 §4.1, p. 7 Table 2, p. 25 Table 9] | AI 预审支持；用户最终确认 |

## 02 一句话总结

MADBench 用「编排层—Agent 层—资源层」分层威胁模型组织 6 个攻击族（M1–M4 迁移自单 Agent，M5–M6 为多 Agent 特有），在 356 个源任务、3,958 个测试用例上与单 Agent 基线配对比较，结论是：MAD 在问答任务上**吸收**针对答案准确率的攻击，却**放大**未授权读与写；即便 5 个 Agent 中 3 个共谋，也只翻转 28.30% 原本答对的任务，且仅 3.26% 初始答对的诚实 Agent 在辩论中被说服改错 [Paper: PDF p. 1 Abstract, p. 7–8 §4.1, p. 9 §4.2]。

## 16 研究想法

## 10 实验设计与证据链

### Agent-derived research candidates

---

### Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks
Source note: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md
Source note SHA-256: 59775e74afeb2756e97b54189f34ebfaf3cb9eac1c1d5d618b49ed72cbf8ba88

## 11 结论的正确解释

论文可以支持的、边界明确的主结论是：**在层级式 agent-as-tool 多 Agent 系统中，"逐 Agent 部署 CaMeL"不等于系统安全。** 失效机制是边界洗白——父 Agent 把工具派生的不可信值写入子 Agent 的自然语言指令参数，而子 Agent 把调用它的父 Agent 当作用户，于是该值以可信输入身份进入子 Agent 的 PLLM 并改写其控制流计划。作者既给出构造性反例（三 Agent、注入置于 SQL 数据库、GPT-5.2、平凡策略），又在温和的表达能力假设下证明：只要系统非平凡且存在返回值不可信的工具，系统级 CFI 必然被违反，即使每个 Agent 各自满足 CFI。[Paper: Section III-A; Section III-C; Section VII]

修复方式是把边界显式双通道化并在运行时强制：`message`（可信指令，不得依赖任何工具输出）与 `variables`（不透明数据，携带 capabilities 与 provenance，子 Agent 经 `get_variable` 在运行时取用）。由此从根 Agent 计划递归展开得到的系统级控制流计划仅由用户指令与可信信息决定；不可信数据仍可在既有分支间"分支引导"，但不能新增路径。作者强调，与单 Agent CaMeL 不同，multi-CaMeL 的解释器即使不配置任何安全策略也是保证 CFI 所必需的。[Paper: Section IV-A; Section IV-B; Section IV-C]

经验结果的适用范围必须与其条件一起读：在 MultiAgentDojo（n = 949 注入任务实例/模型/配置）上，平均 ASR 从 no CaMeL 的 12.9% 降到 individual CaMeL 的 0.2%、multi-CaMeL 的 0.0%，且 individual CaMeL 的每一例残留成功攻击都是边界洗白；效用方面，AssetOpsBench 上 multi-CaMeL 相对 individual CaMeL 平均仅额外下降 3.2 点（两个最强模型 0.85 点，各模型区间重叠），但相对 no CaMeL 的整体损失仍达 8.0–37.5 点，MultiAgentDojo 上更大（GPT-4.1 −53.7、Gemini 2.5 Pro −49.5）。[Paper: Table III; Section V-C1; Section V-A2; Fig. 5; Fig. 6; Table IV; Table V]

因此**不应**把结论读成："multi-CaMeL 使多 Agent 系统安全"。作者自己划出的边界包括：0% ASR 只针对基准内既有攻击，未做自适应攻击评测，且大规模自适应红队对所有前沿模型都发现非零成功率；实验全部使用平凡安全策略 $S=\emptyset$，因此结果只覆盖控制流劫持，不覆盖数据流攻击；协议层论证以"指令通道完整性被强制"为前提，而当前实现继承了 CaMeL 解释器漏检隐式依赖的限制；分析仅限树状层级拓扑与 CFI/CaMeL-安全性质，DAG、循环、异步、共享内存、点对点架构与更强信息流性质（如 TIPNI，branch steering 会违反它）留待未来工作。[Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2]

作者提炼出的、比具体协议更宽的原则是：**跨越 Agent 边界不应隐式提升信息的信任级别**；随着能力更强的 Agent 被组合成更大更复杂的系统，在其接口上保留这一区分将是让安全保证可组合的重要部分。[Paper: Section VI-A 末段; Section VII]

## 12 作者明确承认的局限

| 局限 | 具体表现 | 作者提出的未来方向 | 来源 |
| --- | --- | --- | --- |
| 拓扑受限 | 分析仅限层级 agent-as-tool（有根树）设置；更一般架构中可能没有单一根 Agent、没有唯一信息流方向、没有清晰的 agent-as-tool 边界可供强制协议 | 把"边界不得隐式升级信任"的原则形式化扩展到 DAG、循环图、共享内存系统与点对点 Agent 架构，并证明相应的系统级 CFI 与 CaMeL-安全 | [Paper: Section VI-A; Section VII] |
| 会话历史与"新 episode"处理 | 协议可在每个调用边界独立应用：Agent 被新父首次调用时，该父可被视为新 episode 的可信用户；但若跨调用保留会话历史则需额外小心，因为先前交互可能含源自不可信数据的输出，不应并入后续调用的上下文 | 明确跨调用上下文管理规则（作者作为设计注意事项提出） | [Paper: Section VI-A] |
| 安全性质强度受限 | 本文只定义并证明 CFI 与 CaMeL-安全；并发工作 LLMbda [28] 的 TIPNI 更强——multi-CaMeL 允许的 branch steering（不可信数据在既有分支间引导执行、改变外部可见输出）会违反 TIPNI，作者承认"TIPNI 排除了 CFI 允许的一些行为" | 形式化刻画 CFI 与 TIPNI 的相对强度与适用范围 | [Paper: Section VI-B; Section IV-C] |
| 解释器漏检隐式依赖 | CaMeL 解释器的依赖追踪可能漏掉经控制流的隐式流：变量的值依赖不可信条件（尤其是未走分支上的赋值）时仍可能被标记为可信；multi-CaMeL 因扩展该解释器而继承此限制，故当前实现在涉及此类隐式依赖时可能无法强制指令通道完整性（协议层论证不受影响，因其假设该性质已被强制） | 强化 CaMeL 解释器以可靠（soundly）追踪此类依赖，作者称之为重要未来工作 | [Paper: Section VI-B1] |
| Confinement 与隐蔽通道 | 信息流保证依赖 Agent 被适当 confinement [30]；随着 Agent 更具策略性、通过日益复杂的渠道通信，传统的隐蔽通道枚举与容量削减可能不足 [31]。（CaMeL 的外部重试循环被 Garby et al. 指为泄漏通道；multi-CaMeL 实现不重试失败执行，故不继承该具体问题） | 为 multi-CaMeL 建立适当的 confinement 保证 | [Paper: Section VI-B2] |
| 评测中的策略选择 | 实验全部使用平凡安全策略（$S=\emptyset$）：一是因为证明 CFI 不可组合已足以说明 CaMeL-安全不可组合，二是配置非平凡策略需在众多可能中做任意选择，结果会依赖所选策略 | 在 Section IV 说明 multi-CaMeL 如何自然扩展到需要非平凡安全策略的情形（保留跨边界 provenance 即可全局强制 $S$） | [Paper: Section II-B; Section IV-B] |
| 基准攻击的代表性 | GPT-5.5 在无 CaMeL 时 ASR 亦为 0%；作者明确这不应被解读为对间接提示注入的普遍鲁棒性——MultiAgentDojo 上的 0% 可能只反映基准所代表的攻击，而非对更强自适应攻击的免疫，并引大规模自适应红队对所有受评前沿模型都发现非零攻击成功 [29] | （作为解释边界提出；未给出具体后续实验计划） | [Paper: Table III 说明文字] |
| 效用依赖提示增强与预先承诺的计划 | 两个基准上都必须为工具描述增补完整返回 schema 才能获得合理效用（作者视其为协议必要组成而非固有局限）；多数良性失效源于在观察运行时数据前承诺控制流计划，另有未经检查的范围替换失效 | 作者将其作为观察到的失效模式记录，未提出具体解决方案 | [Paper: Section V 开头; Section V-C2] |
| 复现性受模型访问限制 | 模型经 OpenRouter API 访问，底层推理硬件不受作者控制，精确复现可能依赖对相同模型版本的持续访问 | （在 LLM 使用说明中披露） | [Paper: Section IX] |

## 03 研究问题

- **具体问题**：CaMeL 为单个 Agent 提供的安全保证（控制流完整性 + 基于 capability 的策略强制），在 Agent 互相调用的层级多 Agent 系统中是否仍然成立？若不成立，失效发生在哪里、能否在协议层修复、修复的效用代价多大？[Paper: Abstract; Section I 末段; Section III]
- **研究意义**：随着 Agent 被授予外部数据源、工具与服务访问权，间接提示注入的攻击面显著扩大；同时多 Agent orchestrator 模式（中心 Agent 向专门子 Agent 委派子任务）日益常见，因此"逐 Agent 加固是否等于系统安全"成为部署前的关键问题。作者称其结果为"安全必须在系统层面强制"的既有论点提供经验支持 [25, 26]。[Paper: Section I; Section I 相关工作段; Section III-A 末段]
- **现有方法不足**：
  - 模型级防御（微调/偏好优化让模型区分特权指令与低权限内容）与输入级防御（DataFilter 过滤模型、提示净化、sandwich prompting、spotlighting）"通常依赖习得的模型行为，不提供硬安全保证" [10]。[Paper: Section I 防御分类段]
  - 系统级防御（Dual LLM 模式、CaMeL、信息流控制 [13,14]、细粒度权限强制 [15]）中，CaMeL 明确"是为单 Agent 与其环境交互而formulated 的"，多 Agent 设置留白。[Paper: Section I 系统级防御段; Section I "CaMeL is formulated for a single agent" 段]
  - 已有工作已把层级 agent-as-tool 架构当作攻击面研究（如 OMNI-Leak [22]、Triedman et al. [24]），但缺少"个体安全何时可组合到系统级"的刻画与可运行的防护协议。[Paper: Section II-A; Section III-B]
- **核心问题**：跨越 Agent 边界时，信息的信任级别是否被隐式提升？如何在保留跨边界数据可用性的同时，阻止不可信数据进入下游 Agent 的指令通道？[Paper: Section VI-A 末段; Section VII]

---

### ORBIT: A Framework for Multi-Agent Safety and Security Evaluations
Source note: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md
Source note SHA-256: 41ee328c301d418c7eb20e9df0c3f58ff2e443b5b5b4713283c57d26bc8e2747

## 12 作者明确承认的局限

| 局限 | 具体表现 | 作者提出的未来方向 | 来源 |
| --- | --- | --- | --- |
| 配置空间覆盖不足 | 配置空间组合式巨大，评估只覆盖代表性切片；因子式评估计算成本快速增长 | 依靠框架的可组合性扩展覆盖 | [Paper: PDF p. 10, Section 7] |
| 攻击非自适应 | 攻击使用固定载荷模板而非自适应红队，"可能高估静态防御的效果"，并使与控制评估的对应只是部分的 | 攻击注册表支持自适应后续；未来工作含自适应红队（"会把监控实验变成完整的控制评估"） | [Paper: PDF p. 10, Section 7；PDF p. 9–10, Section 6] |
| 不主张全空间泛化 | 明确声明"我们不能主张我们的发现泛化到配置空间的所有点" | 未提供 | [Paper: PDF p. 10, Section 7] |
| 执行模型假设 | 假设回合制执行与离散消息传递；连续通信、共享梯度信号或学习式通信协议的系统不在范围内 | 未提供（列为范围外） | [Paper: PDF p. 10, Section 7] |
| judge 残余问题 | 自一致 95.4%、双 judge 92.5%、人类 91%，但人类核查只用单一评分者、未做评分者间一致性分析，"残余 judge 问题不能被完全排除" | 未提供 | [Paper: PDF p. 10, Section 7] |
| 构造效度 | 明确不主张改造保留了源基准所测的构念 | 以良性基线列作为常设合理性检查 | [Paper: PDF p. 26, Appendix F.6] |
| 双重使用风险与基准过拟合 | 标准化攻击实现原则上可被改造用于攻击已部署系统；标准化指标可能诱使优化被测维度而牺牲未测维度 | 两项设计选择约束风险（攻击只实例化文献已有威胁类、不引入新攻击能力；攻击作用于编排层而非模型级越狱，其可迁移性取决于匹配特定架构选择）；可扩展注册表允许社区添加场景/攻击/防御而无需改编排器 | [Paper: PDF p. 15–16, Appendix A] |
| 附录结果的性质 | 附录 J 多数结果是演示框架能力的初步调查，而非严格研究 | 未提供 | [Paper: PDF p. 33–34, Appendix J 开篇] |

## 02 一句话总结

ORBIT 是建立在 UK AISI Inspect 之上、把"拓扑—记忆可见性—威胁模型—防御—执行—评估"拆成六个可组合配置层的多 Agent 安全评估框架与基准套件；其核心经验发现是：能把被攻陷 Agent 攻击成功率压低 60 个百分点的逐动作防御，对共谋没有任何可测保护，且没有一种被测防御覆盖全部被测攻击类型 [Paper: PDF p. 1, Abstract；PDF p. 8–9, Section 5；PDF p. 9, Section 6]。

---

### 多Agent协作的安全防护
Source note: Agent-IFC/20_Themes/多Agent协作的安全防护.md
Source note SHA-256: f69c2638cddcd6ac96421f8a1c8752f705c2919a64cd2661b3e9d63a8cde0c48

比较边界：不同协作拓扑、威胁模型、权限配置、任务与评估协议下的安全结果不能直接排名；未明确的字段保留待确认，不从论文标题推断安全性。

# 多Agent协作的安全防护

### 多Agent协作的安全防护对比表

### 研究问题与方法证据

## Selection manifest
- MADBench: Benchmarking the Security of Multi-Agent Debate | Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md
- Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks | Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md
- ORBIT: A Framework for Multi-Agent Safety and Security Evaluations | Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md
- 多Agent协作的安全防护 | Agent-IFC/20_Themes/多Agent协作的安全防护.md

</SOURCE_EXCERPTS>