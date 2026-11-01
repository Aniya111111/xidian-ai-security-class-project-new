输入范围为文献综合、提纲及主张映射。未开展新实验。
证据仅是提供的笔记摘录，不是经重新核验的全文。

<MANUSCRIPT>
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

# 主张—来源映射表

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

</MANUSCRIPT>

<SOURCE_EXCERPTS>
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

---

### 多Agent协作的安全防护
Source note: Agent-IFC/20_Themes/多Agent协作的安全防护.md
Source note SHA-256: f69c2638cddcd6ac96421f8a1c8752f705c2919a64cd2661b3e9d63a8cde0c48

#### Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks

- 研究问题摘录：- **具体问题**：CaMeL 为单个 Agent 提供的安全保证（控制流完整性 + 基于 capability 的策略强制），在 Agent 互相调用的层级多 Agent 系统中是否仍然成立？若不成立，失效发生在哪里、能否在协议层修复、修复的效用代价多大？[Paper: Abstract; Section I 末段; Section III] - **研究意义**：随着 Agent 被授予外部数据源、工具与服务访问权，间接提示注入的攻击面显著扩大；同时多 Agent orchestrator 模式（中心 Agent 向专门子 Agent 委派子任务）日益常见，因此"逐 Agent 加固是否等于系统安全"成为部署前的关键问题。作者称其结果为"安全必须在系统层面强制"的既有论点提供经验支持 [25, 26]。[Paper: Section I; Section I 相关工作段; Section III-A 末段] - **现有方… [[Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks#03 研究问题|卡片来源]]

- 方法摘录：- **输入**：用户指令（仅交给根 Agent $A_0$）；工具与环境描述（本文实验中均增补完整返回 schema）；不可信工具输出（数据库、网页、邮件、文件等）；跨 Agent 调用时父 Agent 提供的 `message`（可信）与 `variables`（不透明）。 - **输出**：各 Agent PLLM 生成的 Python 控制流程序；递归展开后得到的系统级控制流计划；实际工具调用及其结果；子 Agent 经 `variables` 通道接收并在运行时取用的值；最终返回给用户的答案。 - **训练/外部工具**：无模型训练或微调。依赖既有 CaMeL 的自定义 Python 解释器（追踪运行时值的来源与依赖、在工具调用处检查策略），本文对其做两项扩展；依赖 PLLM/QLLM 双模型（实验中同一后端模型兼任）；新增 `get_variable` 运行时工具；评测依赖 AssetOpsBench（LLM judge 评分）、AgentDojo/MultiAgentDojo 环境与注入任务，模型经 OpenRouter API 访问。 - **关键假设**： - 拓扑为以 $A_0$ 为根的有向树，每个非根 Agent 有唯一父 Agent，所有 Agent 间通信都经父→子调用与返回；子 Agent 被"新启动"而非跨调用保留状态或会话历史。[Paper: Sec… [[Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks#07 方法概览|卡片来源]]

- 正确解释摘录：论文可以支持的、边界明确的主结论是：**在层级式 agent-as-tool 多 Agent 系统中，"逐 Agent 部署 CaMeL"不等于系统安全。** 失效机制是边界洗白——父 Agent 把工具派生的不可信值写入子 Agent 的自然语言指令参数，而子 Agent 把调用它的父 Agent 当作用户，于是该值以可信输入身份进入子 Agent 的 PLLM 并改写其控制流计划。作者既给出构造性反例（三 Agent、注入置于 SQL 数据库、GPT-5.2、平凡策略），又在温和的表达能力假设下证明：只要系统非平凡且存在返回值不可信的工具，系统级 CFI 必然被违反，即使每个 Agent 各自满足 CFI。[Paper: Section III-A; Section III-C; Section VII] 修复方式是把边界显式双通道化并在运行时强制：`message`（可信指令，不得依赖任何工具输出）与 `variables… [[Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks#11 结论的正确解释|卡片来源]]

## 已审核文献综合

来源：3 篇 `reviewed` 卡片。以下内容为卡片原文摘录与整理，尚需本次综合审核；不代表重新验证了原论文。

比较边界：不同协作拓扑、威胁模型、权限配置、任务与评估协议下的安全结果不能直接排名；未明确的字段保留待确认，不从论文标题推断安全性。

### 研究问题与方法证据

# 多Agent协作的安全防护

### 多Agent协作的安全防护对比表

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

### 结论—证据矩阵

---

### MADBench: Benchmarking the Security of Multi-Agent Debate
Source note: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md
Source note SHA-256: d5910beb563fdc571b36b17c91930791e4430efa0228ea8db7440548a2e055c8

## 13 批判性分析

| `[Analysis]` 观察 | 潜在问题或替代解释 | 为什么重要 | 如何检验 | 依据 |
| --- | --- | --- | --- | --- |
| AF 用比值定义，基线为 0 时记为 ∞ | M3/M4 在 accuracy 与 cost 目标下的 IRW 全为 ∞，实际含义是「单 Agent 从不越权、MAD 越权」，但数值不可比较；作者又对极小样本自标噪声 | 主结论「放大权限攻击」有相当部分依赖不可量化的单元格 | 改报绝对差值 + 置信区间，或按任务数加权；对 ∞ 单元格单独列表并标注分母 | [Paper: PDF p. 6 Eq.7, p. 7 Table 2, p. 25 脚注] |
| ASR 分母是 clean run 答对的任务 | ASR 是「翻转率」而非总体错误率；M2 工作区 ASR=100.00 而 AF 仅 1.05，说明单 Agent 也几乎全错 | 高绝对危害与低相对放大并存时，单看 AF 会低估风险 | 同时报告 clean 错误率、attacked 错误率与 AF 三列 | [Paper: PDF p. 6 Eq.5, p. 25 Table 9a] |
| 「吸收准确率攻击」与「放大越权」来自不同任务类型 | M3/M4 主要在 QA 上测，M2 在工作区任务上测；跨任务类型合并成「MAD 安全性」结论存在混淆变量（任务是否含可执行写工具） | 影响结论可迁移性：纯推理型 MAD（无工具）可能只有吸收一列 | 在同一任务集上同时测两类指标（论文 QA 上的 IRW 已部分做到），并报告 workspace 上的 ASR | [Paper: PDF p. 6–7 §4 Tasks, p. 7 Table 2] |
| 授权集 $R^\star_s/W^\star_s$ 被设定为攻击者不可操纵 | 真实系统中授权本身可被污染（工具配置、任务描述、策略文件）；固定预言机会系统性低估 IRW | 直接关系到「最小权限/委托边界」类防护的可评估性 | 增加「授权面也可写」的攻击族（如 M4 扩展为改写策略/权限声明），并测 IRW 是否失真 | [Paper: PDF p. 6 Eq.6 说明, p. 5 §3.2 M4] |
| 吸收效应来自编排器聚合，而同一组件是 M6 的 100% 攻击面 | 聚合器既是主要吸收来源也是最大单点信任；论文未把这一张力作为设计结论提出 | 决定防护应部署在何处：加固聚合器 vs 移除聚合器特权 | 对比「聚合改为无工具权限的纯投票/证据核验」与现状的 ASR/IRW/cost | [Paper: PDF p. 8 §4.1, p. 9 §4.2 M6] |
| cost 的 AF 混合了并行度与攻击影响 | MAD 本身消耗 $n$ 倍 token，受攻击/干净比值虽为相对量，但工作流阶段差异（如 finalize 额外写文件）会同时影响 cost 与 IRW | 影响「成本攻击」结论的解释 | 报告每阶段 token 分解（Propose/Debate/Decide）与工具调用次数 | [Paper: PDF p. 5 §3.3, p. 9 §4.2 case study] |
| 未评测任何防护机制（YAML `defense_mechanism` 留空） | 论文是攻击/基准工作，标题为 benchmarking；不能从中推出「现有防护无效」或「MAD 不可防护」 | 防止把基准误引为防御评估结论 | 在 MADBench 上接入过滤、来源标记、写白名单等防护并复用同一配对协议 | [Paper: PDF p. 2 §1, p. 6–7 §4] |
| 消融维度不含 $n$（Agent 数量）与拓扑 | 只变 $f$、$R$、模型；「多数被攻陷」与不同拓扑下的吸收/放大未知 | 与画像中「自适应攻击、动态成员、拓扑」的评测空白直接相关 | 扩展 $n\in\{3,5,7\}$、$f/n$ 比例与全连通/星型拓扑 | [Paper: PDF p. 6–7 §4, p. 18 §D.2–D.3] |
| 数据集计数口径不一致 | 摘要与引言称 three datasets，§4 Tasks 列出 SealQA、StrategyQA、AgentDojo、JailbreakBench 四个（100+100+56+100=356），§4.1 又称 four datasets | 影响引用与复现时的任务集界定 | 人工核对 PDF 原文措辞与 §4 表格；必要时向作者确认 | [Paper: PDF p. 1 Abstract, p. 6–7 §4, p. 7 §4.1] |
| 同一 AF 单元格在两处读数疑似不同 | Table 2 中 M4 cost 行 AF_Cost 读作 0.89，Table 9b 同格读作 0.92（可能为检索片段解析所致） | 若为真则是排版/取整不一致；若为解析误差则本卡片该值需更正 | 在 PDF 第 7 页与第 25 页并排核对 Table 2 与 Table 9b | [Paper: PDF p. 7 Table 2, p. 25 Table 9b] |

## 03 研究问题

- **具体问题**：对抗性影响在 MAD 中被吸收还是被放大？不同攻击层、共谋模式、被攻陷 Agent 数 $f$、辩论轮数 $R$、底层模型如何改变结果？[Paper: PDF p. 2 §1, p. 7 RQ1/RQ2]
- **研究意义**：MAD 被用于提升推理与事实性，且常用于 ground truth 不可得的领域；使 Agent 纠错的交互同样会传播对抗性错误，因此需要系统化安全评测 [Paper: PDF p. 1 Abstract, p. 1–2 §1]
- **现有方法不足**：现有安全基准主要面向单个 Agent 的 prompt、observation、memory、tools 与 action execution；针对 MAD 的工作要么假设全员诚实，要么只分析某类攻击；作者声明「据我们所知，尚不存在从分层视角系统分析 MAD 安全性的基准」[Paper: PDF p. 1–2 §1, p. 2 §1]
- **核心问题**：把「辩论是否更安全」拆成按攻击层 × 按攻击目标（准确率 / 成本 / 未授权读 / 未授权写）× 相对单 Agent 基线的可量化比较 [Paper: PDF p. 4–6 §3.1–3.3]

## 10 实验设计与证据链

## 16 研究想法

### Agent-derived research candidates

</SOURCE_EXCERPTS>