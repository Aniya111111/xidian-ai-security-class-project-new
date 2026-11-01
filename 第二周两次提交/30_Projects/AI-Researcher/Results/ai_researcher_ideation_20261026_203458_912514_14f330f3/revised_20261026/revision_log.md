# 定向修订记录

原稿与模型审阅结果保留。此次按 nature-writing 的证据边界与术语一致性要求修订，没有调用模型或开展实验。

## 已处理审阅意见

- R1-M1：已修改，仍待作者确认。
- R1-m1：已修改，仍待作者确认。
- R1-m2：已修改，仍待作者确认。

## 术语记录

| 术语 | 本轮用法 | 处理 |
| --- | --- | --- |
| CFI | 控制流完整性 | 保留来源用法，不与更强信息流性质等同 |
| PD | 传播深度 | 修正“防御有效性”误译 |
| ASR / AF | 翻转率 / 相对放大率（S4 语境） | 区分定义和分母 |

## R1-M1 — body

限定协议保证的拓扑、运行时与上下文前提，不把设计方案写成普遍必要条件。

修改前：

为此，协议层将调用边界显式双通道化被提出为必要修复路径：`message` 通道仅承载可信指令（不得依赖任何工具输出），`variables` 通道携带受限且不透明值，配合运行时 `get_variable` 取用与策略强制，可在假设拓扑为有根树的前提下恢复控制流预期 **[S1; S2]**。

修改后：

S1 提出的 multi-CaMeL 将调用边界划分为两个通道：`message` 承载可信指令，`variables` 传递对规划模型不透明的数据，子 Agent 经 `get_variable` 在运行时取用。其控制流完整性论证适用于有根树式层级调用，并以运行时确实强制指令通道完整性为前提；跨调用的历史上下文也需避免将不可信输出提升为可信指令。这是该设定下的一种协议修复方案，不等于一般多 Agent 架构的必要条件或当前实现已满足全部保证 **[S1; S2]**。

## R1-m1 — body

逐段区分笔记分析与本文建议；修正 PD 释义，并保留扫描覆盖未核实的边界。

修改前：

面向多Agent系统的横向比较日益依赖统一评测栈。评估框架的价值在于将拓扑、记忆可见性、威胁模型与防御机制解耦为可调自变量。然而，实践报告呈现多重口径错位。**[笔记分析]** 攻击类型注册表宣称支持多维威胁能力，但实证扫描往往局限于防御策略、模型与拓扑，缺乏对知识水平、预算与持久化维度的因子遍历 **[S3]**。成功判定标准并存语法匹配与LLM judge语义赋值，同一轮交互可能出现判据触发但judge评分中性，或反之，导致攻击成功率(ASR)与防御有效性(PD)的语义映射发生偏移 **[S3]**。此外，Judge模型的跨条件切换（如防御格使用高版本模型评判而基线格使用另一模型）可能引入评分漂移，使低ASR区间的组间差异对Judge配置高度敏感 **[S3]**。

记忆可见性的默认配置同样构成隐性混杂因素。多数共享标志默认关闭，仅在特定拓扑或场景下开启，使得“共享记忆污染”传播路径的实际覆盖率可能被低估 **[S3]**。这些观测共同指向一个方法论要求：评估框架必须公开配置种子、Judge一致性阈值与等价性检验预案，否则“某防御在XX拓扑最强”类结论仅反映该切片的经验噪声。


修改后：

本节限定于 ORBIT 注记所描述的评估配置。框架将拓扑、记忆可见性、威胁模型与防御机制作为可配置维度，但能力声明与结果覆盖需要分别核对。**[笔记分析]** 所供注记列出了攻击类型计数及 ThreatModel 参数的口径问题；结果片段主要报告防御、攻击类型、拓扑与模型变化。知识水平、预算与持久化是否已在其他附录中被充分扫描，本次材料不足以确认 **[S3; C4]**。

**[笔记分析]** 注记提示，机器可判定的攻击成功判据与 LLM judge 对受影响程度的赋值不一定一致。若同一实例在两套判定下出现差异，攻击成功率（ASR）与传播深度（PD）的解释便需分别说明；这里的 PD 不是“防御有效性”。上述内容是需核查的判定一致性问题，不是本文测得的结果 **[S3; C5]**。同理，注记指出部分单元格采用不同 judge 模型，这可能构成跨条件比较的混杂因素，但本次综合没有测量其影响大小 **[S3; C10]**。

**[笔记分析]** ORBIT 的记忆可见性默认设置提示，应区分框架支持的共享方式与具体实验实际启用的方式，不能仅从默认值推定全部实验的覆盖情况 **[S3; C10]**。**[本文建议]** 比较这些结果时，应一并列出实际配置、成功判据、judge 设置与样本量；这些建议来自对特定材料的综合，不代表所有评估框架均存在相同问题。


## R1-m2 — body

摘要与结论采用相同的、限于本次来源的归纳范围。

修改前：

而现有评估框架在配置空间覆盖、度量标准一致性与非自适应攻击假设等方面仍存在显著的方法论缺口。

修改后：

对 ORBIT 与 MADBench 注记的分析则提示，配置覆盖、判定口径与任务类型差异需要分别核对，不能直接归纳为所有评估框架的共同缺陷。

## R1-m2 — body

分别限定协议方案、ORBIT 配置问题与 MADBench 指标问题，移除普遍化归纳。

修改前：

本文系统梳理了多Agent系统安全中边界信任维持、协议可组合性修复路径以及评估框架配置与度量有效性的核心文献线索。综合表明：逐Agent安全机制的简单叠加无法抵御跨边界洗白；显式双通道分离与运行时策略强制是恢复控制流预期的必要条件，但其落地受限于隐式依赖追踪、会话管理与隐蔽通道约束。评估框架的理论模块化优势在实践中遭遇统计功效、Judge漂移、指标口径错位与非自适应攻击假设的多重掣肘。未来写作与研究工作应优先建立协议性质到评估指标的严格映射字典，并在公开配置前提下补充自适应红队、功效分析与等价边界检验。本研究仅作文献综合与写作指引，未开展实证验证，所有主张均可追溯至所供注记及其标注的原始定位。


修改后：

本文依据三篇论文卡及一份主题笔记，围绕边界信任、协议可组合性与评估口径组织了文献综合。S1 所述反例说明，在其层级式 agent-as-tool 设定下，逐 Agent 安全机制不能自动保证系统级控制流完整性；multi-CaMeL 提供了该设定下的修复方案，但论证以前述运行时性质被强制为前提，且不能消除已记录的实现与上下文管理限制 **[S1; S2; C1–C3]**。

对于评估材料，ORBIT 注记提示应核对具体配置、judge 设置及成功判据，MADBench 注记则提示应区分相对放大率、翻转率与不同任务的工具权限条件。这些是针对本次材料的分析线索，不构成对所有多 Agent 评估框架的统一判断 **[S3; S4; C4–C10]**。下一轮写作应优先回到原文核对这些定义及适用边界。本稿未开展新实验，也未据此声称任何新防御有效。


## CONSISTENCY-AF — body

去掉将 ASR 条件分母误写为 AF 分母的表述。

修改前：

指出指标口径（如相对放大率分母为清洁对答任务）、任务类型混合与防御机制空白等方法学特征。

修改后：

所供笔记进一步讨论了指标口径、任务类型差异及防御评估的适用边界；这些批判性分析不作为原论文已验证的额外结论。

## CONSISTENCY-AF — body

AF 与 ASR 的解释分别对齐 S4 批判性分析原有条目，不补造公式或数字。

修改前：

AF以基线正确任务数为分母，当基线绝对错误率高或出现零除情况时，比值趋于无穷或掩盖真实危害；ASR本质为翻转率而非总体错误率，二者结合使用方可还原风险全貌 **[S4]**。

修改后：

AF 是相对量，需说明对应基线；当相应基线为零时，笔记记录其记为 ∞，不宜将这类单元格直接排序。ASR 在该笔记所述定义下以 clean run 答对的任务为条件分母，是翻转率而非总体错误率；这一条件分母不能套用于 AF。比较时还需区分 QA 与工作区任务的工具权限条件 **[S4; C9]**。

## CONSISTENCY-SCOPE — body

不将聚合器的分析性观察提升为已验证的防护部署结论。

修改前：

其架构张力决定了防护应优先加固聚合节点还是重构投票/核验范式 **[S4]**。

修改后：

这一笔记分析为后续讨论聚合节点权限提供了问题线索，但本稿没有验证哪种防护部署方式更优 **[S4; C6]**。

## CONSISTENCY-SCOPE — body

区分笔记记录、原论文研究问题与本文尚未完成的原文核验。

修改前：

目前该基准尚未接入过滤、来源标记或写白名单等防御机制，其研究问题本身属于待验证的前提假设，不应直接外推为“现有防护无效”或“MAD结构固有脆弱”的定论 **[S4]**。

修改后：

S4 注记明确将原工作定位为攻击与基准评估，并记录其未评测防护机制。该记录不能被解释为某种防护无效，也不能把论文研究问题直接当作已证实的普遍结论；原文方法与结果仍需逐项核验 **[S4]**。

## CONSISTENCY-SCOPE — body

纠正“只有研究问题”的材料范围描述，避免把缺少摘录写成原论文缺陷。

修改前：

- MADBench等基准材料仅记录研究问题与初步指标定义，未提供防御实施或大规模自适应红队结果，现阶段不宜作为安全性定论依据；

修改后：

- MADBench 摘录包含研究问题及笔记作者对指标和任务的分析，不等于完整方法、结果或原文核验；本稿不能据此推断原论文没有系统评测，也不把它当作防御有效性的证据；

## CONSISTENCY-SCOPE — body

去掉误写的统计术语与过强义务表述。

修改前：

报告方向性结果时必须同步披露功效分析或预设定价边界检验 **[S3]**。

修改后：

**[本文建议]** 讨论 ORBIT 的这些切片时，应区分原文标注的方向性结果与笔记提出的功效或等价性检验建议；本稿未完成这些额外检验 **[S3]**。

## R1-M1 — map

主张表与正文同步限定。

修改前：

| C3 | 双通道分离（message为可信指令，variables为受限变量）及运行时策略强制可在假设拓扑中恢复边界信任。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | [Paper: Sec…]; [Paper: Section VI-A; Section VII] | 原论文结论 | 有根树拓扑；插件式解释器扩展；完整返回schema增补前提 | 2.1节、结论 | 缺失返回schema时的效用代价定量分解；多模型版本的稳定性检验 |

修改后：

| C3 | multi-CaMeL 通过双通道与运行时强制提供层级调用下的协议修复方案；控制流完整性论证以指令通道性质确被强制为前提，不等于当前实现已满足该保证。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | [Paper: Sec…]; [Paper: Section VI-A; Section VII] | 原论文结论 | 有根树拓扑；插件式解释器扩展；完整返回schema增补前提 | 2.1节、结论 | 缺失返回schema时的效用代价定量分解；多模型版本的稳定性检验 |

## C3-LOCATOR — map

从 S1 全文论文卡找到完整协议定位，并补列其实现限制；保留 S2 的拓扑边界定位。

修改前：

| C3 | multi-CaMeL 通过双通道与运行时强制提供层级调用下的协议修复方案；控制流完整性论证以指令通道性质确被强制为前提，不等于当前实现已满足该保证。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | [Paper: Sec…]; [Paper: Section VI-A; Section VII] | 原论文结论 | 有根树拓扑；插件式解释器扩展；完整返回schema增补前提 | 2.1节、结论 | 缺失返回schema时的效用代价定量分解；多模型版本的稳定性检验 |

修改后：

| C3 | multi-CaMeL 通过双通道与运行时强制提供层级调用下的协议修复方案；控制流完整性论证以指令通道性质确被强制为前提，不等于当前实现已满足该保证。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | S1：[Paper: Section IV-A; Section IV-B; Section IV-C]；[Paper: Section VI-B1]；S2：[Paper: Section VI-A; Section VII] | 原论文结论 | 有根树拓扑；插件式解释器扩展；完整返回schema增补前提 | 2.1节、结论 | 缺失返回schema时的效用代价定量分解；多模型版本的稳定性检验 |

## R1-M1 — map

明确设计保证的适用前提。

修改前：

| C3 | multi-CaMeL 通过双通道与运行时强制提供层级调用下的协议修复方案；控制流完整性论证以指令通道性质确被强制为前提，不等于当前实现已满足该保证。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | S1：[Paper: Section IV-A; Section IV-B; Section IV-C]；[Paper: Section VI-B1]；S2：[Paper: Section VI-A; Section VII] | 原论文结论 | 有根树拓扑；插件式解释器扩展；完整返回schema增补前提 | 2.1节、结论 | 缺失返回schema时的效用代价定量分解；多模型版本的稳定性检验 |

修改后：

| C3 | multi-CaMeL 通过双通道与运行时强制提供层级调用下的协议修复方案；控制流完整性论证以指令通道性质确被强制为前提，不等于当前实现已满足该保证。 | S1: Agent-IFC/10_Papers/2026_James Peters-Gill_Can CaMeLs Talk_ Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.md<br>S2: Agent-IFC/20_Themes/多Agent协作的安全防护.md | S1：[Paper: Section IV-A; Section IV-B; Section IV-C]；[Paper: Section VI-B1]；S2：[Paper: Section VI-A; Section VII] | 原论文结论 | 有根树式层级调用；运行时强制指令通道完整性并保留跨边界来源；跨调用历史不可将不可信输出提升为可信上下文。 | 2.1节、结论 | 缺失返回schema时的效用代价定量分解；多模型版本的稳定性检验 |

## R1-m2 — map

避免从单一框架及有限摘录推导一般性覆盖缺口。

修改前：

| C4 | 现有评估框架在攻击类型分类、威胁模型参数设定与实证覆盖维度间存在口径不一致，影响自变量定位。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 5, Section 3.2 Layer 3；PDF p. 28, Table 5]; [Paper: PDF p. 28, Appendix G；PDF p. 8, Section 5] | 笔记分析 | ORBIT框架 v1 版本；注册键与Table条目对照周期 | 2.2节、讨论 | 代码仓库注册键清单核对；knowledge level × persistence 因子扫描结果 |

修改后：

| C4 | ORBIT 注记记录了攻击类型与威胁模型参数的口径问题；本次结果摘录不足以确认全部攻击者能力维度是否被充分扫描。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 5, Section 3.2 Layer 3；PDF p. 28, Table 5]; [Paper: PDF p. 28, Appendix G；PDF p. 8, Section 5] | 笔记分析 | ORBIT框架 v1 版本；注册键与Table条目对照周期 | 2.2节、讨论 | 代码仓库注册键清单核对；knowledge level × persistence 因子扫描结果 |

## R1-m1 — map

修正 PD 定义；明确观察属于笔记分析。

修改前：

| C5 | 成功判据的语法判定与LLM judge语义赋值存在映射断裂，可能导致ASR与PD指标语义偏移。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 28, Appendix G「Success criteria」；PDF p. 6, Section 3.4] | 笔记分析 | 多判定标准并行的评测管线；跨条件Judge切换场景 | 2.2节、讨论 | 判据成功 vs Judge分类的一致率交叉列联表；Judge模型交换测试报告 |

修改后：

| C5 | ORBIT 笔记分析提示：攻击成功判据与 judge 赋值可能不一致，解释 ASR 与传播深度（PD）时应分别说明，实际差异仍待核验。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 28, Appendix G「Success criteria」；PDF p. 6, Section 3.4] | 笔记分析 | 多判定标准并行的评测管线；跨条件Judge切换场景 | 2.2节、讨论 | 判据成功 vs Judge分类的一致率交叉列联表；Judge模型交换测试报告 |

## CONSISTENCY-SCOPE — map

与正文对齐，不外推防护效果。

修改前：

| C6 | 辩论聚合器同时承担主要吸收来源与单点信任角色，其设计张力决定防护部署的关键瓶颈位置。 | S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 8 §4.1, p. 9 §4.2 M6] | 笔记分析 | MAD任务设置；聚合器保留工具权限前提 | 2.3节、讨论 | 聚合改为无工具权限纯投票/证据核验的对照ASR/IRW/cost数据 |

修改后：

| C6 | MADBench 笔记将聚合器的吸收作用与权限攻击面并置，形成需要核验的防护部署问题，而非已验证的防护优劣结论。 | S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 8 §4.1, p. 9 §4.2 M6] | 笔记分析 | MAD任务设置；聚合器保留工具权限前提 | 2.3节、讨论 | 聚合改为无工具权限纯投票/证据核验的对照ASR/IRW/cost数据 |

## R1-m2 — map

去掉“当前评测普遍”的外推与另一条主张的混入。

修改前：

| C7 | 当前对抗性评测普遍依赖固定载荷与非自适应攻击，可能高估静态防御效果，且未充分扫描知识水平与持久化等维度。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 10, Section 7] | 原论文结论 / 笔记分析 | 框架支持的自适应后续预留；现实算力限制下的代表性切片 | 2.2节、局限性 | 自适应红队对照实验；不同Knowledge Level下的边际效应曲线 |

修改后：

| C7 | ORBIT 原文局限在笔记中被记录为使用固定载荷、未采用自适应红队，并警告可能高估静态防御效果；不据此推断其他评测采用相同设置。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 10, Section 7] | 原论文结论 / 笔记分析 | 框架支持的自适应后续预留；现实算力限制下的代表性切片 | 2.2节、局限性 | 自适应红队对照实验；不同Knowledge Level下的边际效应曲线 |

## R1-m2 — map

限定来源与推断范围。

修改前：

| C10 | 评估框架的默认配置（如记忆可见性标志、Judge模型选择）若未在报告中显式控制，可能成为未被识别的混杂因素。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 33, Appendix I, Table 9；PDF p. 38, Table 17 仅含 Star+SharedMem]; [Paper: PDF p. 34, Table 10 caption] | 笔记分析 | 低共享默认运行态；跨格子Judge模型不一致配置 | 2.2节、讨论 | 六标志扫描的PD/ASR变化报告；Judge双向一致性检验与漂移幅度量化 |

修改后：

| C10 | ORBIT 注记中的记忆可见性与 judge 设置提示潜在混杂因素；影响大小及其他框架的情况不能由这些摘录确定。 | S3: Agent-IFC/10_Papers/unknown_Ben Hagag_ORBIT_ A Framework for Multi-Agent Safety and Security Evaluations.md | [Paper: PDF p. 33, Appendix I, Table 9；PDF p. 38, Table 17 仅含 Star+SharedMem]; [Paper: PDF p. 34, Table 10 caption] | 笔记分析 | 低共享默认运行态；跨格子Judge模型不一致配置 | 2.2节、讨论 | 六标志扫描的PD/ASR变化报告；Judge双向一致性检验与漂移幅度量化 |

## CONSISTENCY-AF — map

避免把本轮修订变成强制新增实验。

修改前：

| C9 | MADBench提供的相对放大率(AF)与翻转率(ASR)指标需结合基线错误率与任务类型分层解读，防止∞值或分母偏差导致风险低估。 | S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 6 Eq.7, p. 7 Table 2, p. 25 脚注]; [Paper: PDF p. 6 Eq.5, p. 25 Table 9a]; [Paper: PDF p. 6–7 §4 Tasks, p. 7 Table 2] | 笔记分析 | QA类任务与工作区任务混合场景；授权预言机固定前提 | 2.3节、讨论 | 绝对差值+置信区间替代方案；清洗错误率与攻击错误率联合报告基线 |

修改后：

| C9 | MADBench提供的相对放大率(AF)与翻转率(ASR)指标需结合基线错误率与任务类型分层解读，防止∞值或分母偏差导致风险低估。 | S4: Agent-IFC/10_Papers/unknown_Yuwan Liu_MADBench_ Benchmarking the Security of Multi-Agent Debate.md | [Paper: PDF p. 6 Eq.7, p. 7 Table 2, p. 25 脚注]; [Paper: PDF p. 6 Eq.5, p. 25 Table 9a]; [Paper: PDF p. 6–7 §4 Tasks, p. 7 Table 2] | 笔记分析 | QA类任务与工作区任务混合场景；授权预言机固定前提 | 2.3节、讨论 | 核对原文 AF 与 ASR 定义；按任务类型核对基线和翻转率口径；如需引用定量结果，先核对原表与不确定性报告。 |

## C3-LOCATOR — map

去掉已被截断定位否定的“全部逐字复制”绝对声明和模板占位。

修改前：

- `[原有证据定位]` 字段逐字复制自注记束 `[Paper: ...]` 字符串，未作缩写、翻译或标点规范化。

修改后：

- 原有证据定位逐字沿用已保存的摘录或论文卡。C3 本次从 S1 完整论文卡补回协议定位；定位存在仅证明可追溯，不等于已核验原始 PDF 或证明主张成立。

## 验证与局限

C1–C10 共10行，每行8列；各定位可在该行声明的来源笔记中找到，路径未缩写，输入哈希未变化。上述检查不是原始 PDF 核验，也不代表审阅意见均已得到独立验证。

## CONSISTENCY-TERMS

区分 CFI 与指令通道完整性，按 S1 术语记录恢复 TIPNI 含义。

修改前：

然而，协议论证与实现保障之间存在断层。解释器的依赖追踪可能遗漏隐式流（如条件分支外的变量赋值），导致污染值仍被标记为可信；同时，会话历史跨调用保留会模糊“新episode”的可信边界 **[S1]**。此外，分支选择权本身构成低影响力攻击面：不可信数据虽不能新增执行路径，但可在既定分支内引导外部可见输出，违反某些更强安全性质 **[S1]**。因此，边界信任并非单纯依赖提示增强或模板隔离，而需形式化刻画指令通道完整性(CFI)与分支中立性(TIPNI)的相对强度与适用范围 **[S1]**。

修改后：

然而，协议论证与实现保障之间存在断层。解释器的依赖追踪可能遗漏隐式流（如条件分支外的变量赋值），导致污染值仍被标记为可信；同时，会话历史跨调用保留会模糊“新episode”的可信边界 **[S1]**。此外，不可信数据仍可在既有分支间引导执行并改变外部可见输出，影响范围取决于预先设定的分支 **[S1]**。本文将控制流完整性（CFI）与指令通道完整性分别使用，前者是系统级论证的目标，后者是运行时需强制的性质。S1 注记还区分了 CFI 与更强的终止不敏感概率非干扰（TIPNI）：分支引导可能不违反 CFI，却违反 TIPNI，不能把这些性质等同 **[S1]**。
