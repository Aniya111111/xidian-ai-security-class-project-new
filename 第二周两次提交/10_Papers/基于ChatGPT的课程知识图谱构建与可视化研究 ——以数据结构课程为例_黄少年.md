---
schema_version: 1
type: paper
paper_id: "local:sha256:f249e49cfd6262b9eb0f0b2b51d9957f7614bc78376afa7d443553db8fa5f01b"
title: "基于ChatGPT的课程知识图谱构建与可视化研究——以数据结构课程为例"
authors: ["黄少年", "李佩霖", "王焕然", "陈知新"]
year: 2024
venue: "电脑知识与技术"
volume: "20"
issue: "31"
pages: "148-151"
doi: ""
arxiv_id: ""
paper_version: "published"
source_url: ""
pdf: "Agent-IFC/90_Attachments/基于ChatGPT的课程知识图谱构建与可视化研究 ——以数据结构课程为例_黄少年.pdf"
source_hash: "f249e49cfd6262b9eb0f0b2b51d9957f7614bc78376afa7d443553db8fa5f01b"
citekey: ""
topics: ["课程知识图谱", "知识抽取", "ChatGPT", "Neo4j", "智慧教育"]
projects: []
tags: [paper, paper/methods, status/reading]
status: reading
source_scope: fulltext
locator_mode: page-grounded
primary_lens: methods
secondary_lens: ""
context_mode: paper-only
imported_from: Codex
created: "2026-10-12"
updated: "2026-10-12"
---

# 基于ChatGPT的课程知识图谱构建与可视化研究——以数据结构课程为例

> Source coverage: Full paper
> Extraction confidence: High
> Locator mode: page-grounded
> Primary analytical lens: methods
> Secondary analytical lens: None
> Context verification: Paper-only
> Card completeness: Complete relative to supplied source

[[Agent-IFC/90_Attachments/基于ChatGPT的课程知识图谱构建与可视化研究 ——以数据结构课程为例_黄少年.pdf|打开论文 PDF]]

## 01 基本信息

| 字段 | 内容 |
| --- | --- |
| 标题 | 基于ChatGPT的课程知识图谱构建与可视化研究——以数据结构课程为例 |
| 作者及机构 | 黄少年、李佩霖、王焕然：湖南工商大学计算机学院；陈知新：湖南师范大学信息化中心 |
| 期刊、年份 | 《电脑知识与技术》，2024，20(31)：148-151 |
| 收稿日期 | 2024-06-30 |
| DOI / arXiv | 未提供 |
| 文章编号 | 1009-3044(2024)31-0148-04 |
| 代码与数据 | 未提供 |
| 阅读日期 | 2026-10-12 |
| 论文类型 | 方法/应用系统论文 |
| 研究领域 | 课程知识图谱、信息抽取、智慧教育 |
| 研究方向定位 | Agent-derived candidate：可作为“大语言模型辅助知识图谱构建”主题中的应用案例；待用户确认项目归属 |

来源：[Paper: PDF p. 1, title and author block]；[Paper: PDF p. 4, references and ending]

### 术语表

| 规范术语 | 首次定义 | 原文变体 | 采用规则 |
| --- | --- | --- | --- |
| 课程知识图谱 | 以课程为核心的系统化、结构化知识网络 | 无 | 全文统一使用“课程知识图谱” |
| ChatGPT | 文中用于零样本信息抽取的大语言模型工具 | 无具体版本 | 不推断模型版本 |
| Neo4j | 用节点和关系组织、存储并查询图数据的数据库 | Neo4j图数据库 | 统一使用“Neo4j” |
| Precision / Recall / F1 | 准确率、召回率及其调和平均 | 大小写混用 | 公式和指标表统一保留英文缩写 |
| CASREL | 关系抽取基线模型 | 正文出现“CASRE”，表6及参考文献对应 CASREL | 卡片统一写 CASREL，并保留原文命名冲突提示 |

## 02 一句话总结

[Paper] 该文先构建数据结构课程本体，再用多轮提示驱动 ChatGPT 分别抽取实体、属性和关系，最后用 Neo4j 存储与可视化；在文内给定但规模与复现实验细节未报告的数据上，ChatGPT 的实体、关系和属性抽取 F1 分别为 79.24%、65.06% 和 62.06%。[Paper: PDF p. 1, Abstract and Figure 1] [Paper: PDF p. 3, Tables 5-6] [Paper: PDF p. 4, Table 7]

## 03 研究问题

- [Paper] 具体问题：如何减少课程知识图谱构建对人工数据标注和专家知识的依赖，同时完成课程实体、属性、关系抽取和图谱可视化。[Paper: PDF p. 1, Abstract]
- [Paper] 研究意义：课程知识图谱可支持教学内容组织、知识理解和个性化教学；数据结构课程是电子信息类专业的重要核心课程。[Paper: PDF p. 1, Introduction]
- [Paper] 现有方法不足：课程知识图谱构建依赖人工标注和专家知识，知识点之间的复杂关系也给零样本抽取带来可靠性问题。[Paper: PDF p. 1, Abstract] [Paper: PDF p. 4, limitations]
- 核心问题：能否以课程本体约束多轮提示，让 ChatGPT 在不训练专用抽取模型的情况下生成可存储、可查询、可视化的课程知识图谱，并达到可接受的实体、关系和属性抽取效果？

## 04 研究背景与发展路径

> [Paper-framed; external verification not performed]

1. [Paper] 课程知识图谱将课程实体、概念、理论及其关系组织为结构化网络，用于教学内容组织和知识体系理解。[Paper: PDF p. 1, Introduction]
2. [Paper] 生成式预训练语言模型在中文命名实体识别、关系抽取和事件抽取中的应用，为知识图谱自动构建提供了新工具。[Paper: PDF p. 1, Introduction]
3. [Paper] 本文将课程本体、多轮提示式信息抽取与 Neo4j 串联，形成“资料—本体—抽取—图数据库—查询/展示”的流程。[Paper: PDF p. 1, Figure 1]

未对该发展路径、技术首创性或领域位置进行外部文献核验。

## 05 论文识别的核心痛点

| 痛点 | 表现 | 原因或作者解释 | 论文证据 |
| --- | --- | --- | --- |
| 构建成本高 | 传统流程需要数据标注、专家知识或专门模型训练 | 课程知识需先识别实体、属性和关系 | [Paper: PDF p. 1, Abstract] [Paper: PDF p. 4, Section 3] |
| 抽取输出不稳定 | 简单提示未必覆盖实体类型、属性类型和关系类型 | 提示模板不同会影响抽取效果；作者主张多轮问答有助于提高准确性和完整性 | [Paper: PDF p. 2, Sections 1.2.1-1.2.2] [Paper: PDF p. 3, Section 1.2.3] |
| 复杂关系可靠性不足 | 关系抽取的 Precision 仅为 51.92%，低于 CASREL 和 GPLinker | 作者归因于课程知识点之间关系复杂 | [Paper: PDF p. 3, Table 6] [Paper: PDF p. 4, Section 2.3] |
| 图谱需要可浏览和查询 | 抽取结果本身不等于可用知识系统 | 需要图数据库管理节点、关系、属性并支持查询 | [Paper: PDF p. 4, Section 3, Figures 3-4] |

## 06 核心思想

1. [Paper] 表层方法：收集并预处理课程资料，构建课程本体，分别提示 ChatGPT 抽取实体、属性和关系，再写入 Neo4j 展示与查询。[Paper: PDF p. 1, Figure 1]
2. [Paper] 核心洞见：先定义实体类别、属性和关系集合，再在多轮提示中显式给出这些类型及输出格式，以约束大语言模型的抽取空间。[Paper: PDF p. 2, Sections 1.1-1.2.2] [Paper: PDF p. 3, Section 1.2.3]
3. [Analysis] 可迁移启示：对开放式大模型抽取任务，先建立领域模式层，再让模型按模式输出结构化记录，比仅要求“提取知识点”更便于验证和入库；本文给出示例，但未用消融实验单独证明多轮模板的增益。[Paper: PDF p. 2, Tables 1-2] [Paper: PDF p. 3, Tables 3-4]

## 07 方法概览

- [Paper] 输入：课程教案、教材、习题、科研文献、网络资源及电子文档；文中还提到百度百科、维基百科、百度文库资料和两本教材。[Paper: PDF p. 1, Figure 1] [Paper: PDF p. 2, Section 1.2]
- [Paper] 模式层：定义章节实体、概念实体、法则实体，以及属性和包含、属于、基本概念、存储方式、应用、依赖、同义等关系。[Paper: PDF p. 1, Section 1.1] [Paper: PDF p. 2, Table 1]
- [Paper] 抽取层：通过逐步明确类型和输出格式的多轮问答模板，分别进行实体、属性和关系抽取。[Paper: PDF p. 2, Sections 1.2.1-1.2.2] [Paper: PDF p. 3, Section 1.2.3]
- [Paper] 输出：实体二元组、属性二元组、关系三元组，以及写入 Neo4j 后的可查询图谱。[Paper: PDF p. 2, Table 2] [Paper: PDF p. 3, Tables 3-4] [Paper: PDF p. 4, Figures 3-4]
- 未提供：ChatGPT 具体版本、系统提示、采样参数、API/网页端、运行次数、数据划分和完整标注协议。

~~~text
课程资料
  -> 数据采集与预处理
  -> 课程本体（实体/属性/关系类型）
  -> ChatGPT 多轮提示抽取
  -> 实体/属性/关系结构化结果
  -> Neo4j 存储、查询与可视化
~~~

## 08 核心模块拆解

| 模块 | 功能 | 为什么需要 | 输入与输出 | 支撑证据 | 移除后的已知或预期影响 |
| --- | --- | --- | --- | --- | --- |
| 数据采集与预处理 | 汇总课程资料并清洗、整理 | 为本体和抽取提供文本来源 | 多源课程资料 -> 课程文本 | [Paper: PDF p. 1, Figure 1] [Paper: PDF p. 2, Section 1.2] | 未做消融；[Analysis] 数据覆盖与噪声会影响后续实体和关系范围 |
| 课程本体 | 规定实体类别、属性和关系 | 缩小抽取空间并统一表示 | 教学要求/教材/专家意见 -> 模式定义 | [Paper: PDF p. 1, Section 1.1] [Paper: PDF p. 2, Figure 2 and Table 1] | 未做消融；作者将其作为提示中类型约束的来源 |
| 实体抽取 | 识别章节、概念和法则实体 | 生成图谱节点 | 文本 -> 实体类型—实体值 | [Paper: PDF p. 2, Section 1.2.1 and Table 2] | 未报告模块移除实验 |
| 属性抽取 | 提取顶点集合、边集合、方向性、权重等属性 | 丰富节点描述 | 文本 -> 属性—属性值 | [Paper: PDF p. 2, Section 1.2.2] [Paper: PDF p. 3, Table 3] | 未报告模块移除实验 |
| 关系抽取 | 生成实体间三元组 | 构成知识图谱的边 | 文本 -> 主体—关系—客体 | [Paper: PDF p. 3, Section 1.2.3 and Table 4] | 关系 Precision 较低，说明该模块是当前瓶颈 [Paper: PDF p. 3, Table 6] |
| Neo4j 展示层 | 存储节点/关系并支持查询和可视化 | 将抽取结果转为可浏览图谱 | 结构化抽取结果 -> 图数据库界面 | [Paper: PDF p. 4, Section 3 and Figures 3-4] | 未做用户实验；移除后仍有抽取结果但无本文展示与查询界面 |

## 09 关键公式与符号

### Precision

\[
Precision = \frac{TP}{TP + FP}
\]

- TP：正确预测为正例的数量。
- FP：错误预测为正例的数量。
- 用途：衡量模型输出中正确结果所占比例。
- 来源：[Paper: PDF p. 3, Equation 1]

### Recall

\[
Recall = \frac{TP}{TP + FN}
\]

- FN：未被模型识别的真实正例数量。
- 用途：衡量真实目标中被识别出来的比例。
- 来源：[Paper: PDF p. 3, Equation 2]

### F1

\[
F1 = \frac{2 \times Precision \times Recall}{Precision + Recall}
\]

- 用途：Precision 与 Recall 的调和平均。
- 来源：[Paper: PDF p. 3, Equation 3]

## 10 实验设计与证据链

### 实验设置

- [Paper] 任务：课程实体抽取、实体关系抽取和实体属性抽取。[Paper: PDF p. 3, Section 2]
- [Paper] 指标：Precision、Recall 和 F1。[Paper: PDF p. 3, Section 2.1]
- [Paper] 实体抽取基线：Bi-LSTM、Bi-LSTM-CRF、BERT-CRF、HMM、阿里通义千问。[Paper: PDF p. 3, Section 2.2]
- [Paper] 关系抽取基线：CASREL、GPLinker、阿里通义千问。[Paper: PDF p. 3, Section 2.3 and Table 6]
- [Paper] 属性抽取对照：阿里通义千问。[Paper: PDF p. 4, Section 2.4 and Table 7]
- 未提供：语料条目数、训练/验证/测试划分、标注者与一致性、ChatGPT/通义千问版本、提示执行次数、解码参数、置信区间、显著性检验、计算预算和失败样本统计。

### 结论—证据矩阵

| 编号 | 实验 | 被检验的结论 | 比较与条件 | 结果 | 可支持的结论 | 不可支持的更强结论 | 来源 | 人工核查 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 课程实体抽取 | ChatGPT 在给定测试中的实体抽取效果优于所列基线 | 与4个序列标注模型及通义千问比较；数据划分与预算未提供 | ChatGPT P=80.76%、R=77.77%、F1=79.24%，表列 F1 最高 | 在本文表5报告的设置中，ChatGPT 取得最高 F1 | 不能据此证明跨课程、跨模型版本或统计显著的普遍优势 | [Paper: PDF p. 3, Table 5] | 待核查；表5部分基线 F1 与 P/R 不一致 |
| C02 | 课程关系抽取 | ChatGPT 倾向于较高覆盖率，并在表列结果中取得最高 F1 | 与 CASREL、GPLinker、通义千问比较；预算未提供 | ChatGPT P=51.92%、R=87.09%、F1=65.06% | 在本文设置中，ChatGPT 的 Recall 和 F1 为表列最高，但 Precision 低于 CASREL 和 GPLinker | 不能声称关系抽取全面优于所有基线，也不能证明生成关系足够可靠 | [Paper: PDF p. 3, Table 6] [Paper: PDF p. 4, Section 2.3] | 待核查 |
| C03 | 课程属性抽取 | ChatGPT 在表列三项指标上高于通义千问 | 两种大语言模型比较；版本和运行条件未提供 | ChatGPT P=52.94%、R=75.00%、F1=62.06%；通义千问为 50.00%、66.66%、57.14% | 在本文表7的测试中，ChatGPT 指标均高于该对照 | 不能证明对其他课程、属性模式或现代模型仍然优越 | [Paper: PDF p. 4, Table 7] | 待核查 |
| C04 | 图谱展示 | Neo4j 可以呈现已抽取的课程节点、关系和属性 | 论文给出部分图谱与单知识点界面截图 | 图3、图4展示节点关系与属性界面 | 论文实现了展示性原型 | 截图不能证明可用性、学习效果、性能、完整性或部署价值 | [Paper: PDF p. 4, Figures 3-4] | 待核查 |

### 图表与公式清单

| 项目 | 论证作用 | 来源 |
| --- | --- | --- |
| 图1 课程知识图谱构建与可视化流程 | 给出数据层、模式层、抽取层和展示层的端到端流程 | [Paper: PDF p. 1, Figure 1] |
| 图2 “图”概念体系 | 示例化课程本体的层级结构 | [Paper: PDF p. 2, Figure 2] |
| 表1 部分实体关系 | 说明本体中关系类型及实例 | [Paper: PDF p. 2, Table 1] |
| 表2 实体抽取测试样例 | 展示 ChatGPT 输出与标注结果的差异 | [Paper: PDF p. 2, Table 2] |
| 表3 属性抽取测试样例 | 展示属性二元组输出及标注对照 | [Paper: PDF p. 3, Table 3] |
| 表4 关系抽取测试样例 | 展示关系三元组输出及标注对照 | [Paper: PDF p. 3, Table 4] |
| 公式1-3 | 定义 Precision、Recall 和 F1 | [Paper: PDF p. 3, Equations 1-3] |
| 表5 实体抽取结果 | 支撑 C01，同时暴露部分 F1 数值一致性问题 | [Paper: PDF p. 3, Table 5] |
| 表6 关系抽取结果 | 支撑 C02，显示高 Recall 与相对低 Precision | [Paper: PDF p. 3, Table 6] |
| 表7 属性抽取结果 | 支撑 C03 | [Paper: PDF p. 4, Table 7] |
| 图3 部分知识图谱界面 | 支撑系统已生成可视化原型 | [Paper: PDF p. 4, Figure 3] |
| 图4 单个知识点界面 | 展示局部关系和属性查看方式 | [Paper: PDF p. 4, Figure 4] |

## 11 结论的正确解释

- [Paper] 任务范围限于数据结构课程的实体、关系和属性抽取，以及 Neo4j 展示。[Paper: PDF pp. 1-4]
- [Analysis] 文中没有给出测试集规模、划分、标注一致性、模型版本或多次运行结果，因此无法判断结果的不确定性、复现性和数据泄漏风险。[Paper: PDF p. 3, Section 2]
- [Analysis] 实体抽取中，ChatGPT 的三项指标较均衡；关系抽取的 Recall 很高但 Precision 仅 51.92%，意味着更全面地找出关系的同时可能产生较多错误关系。[Paper: PDF p. 3, Tables 5-6]
- [Analysis] 该流程不是完全自动可信的端到端系统：本体构建仍使用教学要求、教材和名师意见，且作者承认零样本关系抽取可靠性仍需提高。[Paper: PDF p. 1, Section 1.1] [Paper: PDF p. 4, limitations]
- [Analysis] 图3和图4证明存在展示原型，但没有用户研究、教学效果、查询性能或图谱完整性评估。[Paper: PDF p. 4, Figures 3-4]

边界明确的主结论：本文提供了一个“课程本体 + ChatGPT 多轮提示 + Neo4j”的数据结构课程知识图谱原型，并报告了三类抽取任务的单次比较结果；这些结果支持该路线具有可行性，但不足以证明其可复现性、跨课程泛化能力或实际教学效益。

## 12 作者明确承认的局限

| 局限 | 具体表现 | 作者提出的未来方向 | 来源 |
| --- | --- | --- | --- |
| 零样本知识抽取可靠性不足 | 不同课程知识点之间关系复杂，纯依赖大语言模型的可靠性仍需提高 | 探索更有效的知识表示和关联方法，提高图谱质量与准确性 | [Paper: PDF p. 4, Section 3 ending] |
| 知识问答模板仍需完善 | 现有模板需要进一步提炼和优化 | 继续挖掘 ChatGPT 在课程知识图谱构建中的潜力 | [Paper: PDF p. 4, Section 3 ending] |
| 可视化功能仍可改进 | 当前界面只展示基本浏览、查询与属性查看 | 优化可视化工具并增加交互功能，以适配不同用户群体 | [Paper: PDF p. 4, Section 3 ending] |

## 13 批判性分析

| [Analysis] 观察 | 潜在问题或替代解释 | 为什么重要 | 如何检验 | 依据 |
| --- | --- | --- | --- | --- |
| 表5有三项 F1 与对应 P/R 不一致 | 按公式3重算，Bi-LSTM、Bi-LSTM-CRF、HMM 的 F1 约为 71.09%、71.73%、76.24%，而表中为 66.16%、69.45%、74.05%；可能是排版、转录或评估口径问题 | 会影响基线排序和“优越性”判断 | 获取原始预测与评估脚本，按统一公式重算全部指标 | [Paper: PDF p. 3, Equation 3 and Table 5] |
| 数据与评估协议缺失 | 不清楚样本规模、划分、标注过程和是否重复运行 | 无法估计方差、复现结果或排除样本选择偏差 | 公布数据说明、标注规范、固定划分、运行种子和置信区间 | [Paper: PDF p. 3, Section 2] |
| 模型与预算不透明 | ChatGPT 和通义千问的版本、参数、调用日期、提示上下文长度、重试规则均未给出 | 大模型行为会随版本和随机性变化，且与专门训练基线的预算未必可比 | 锁定模型快照和参数，固定调用次数与 token 预算，在相同测试集重复评估 | [Paper: PDF pp. 2-4, Sections 1.2-2.4] |
| “多轮提示更可靠”缺少消融 | 论文展示三种模板，但没有报告模板1/2/3的量化对比 | 不能判断增益来自多轮结构、类型枚举还是其他因素 | 在相同数据与模型上逐项比较单轮、类型约束、多轮、输出格式约束 | [Paper: PDF p. 2, Sections 1.2.1-1.2.2] [Paper: PDF p. 3, Section 1.2.3] |
| 可视化价值仅由截图支撑 | 未测试任务完成率、学习增益、查询延迟或用户满意度 | “直观”“便捷”和教学价值尚未被实证 | 与传统目录/静态图对照，开展教师和学生任务实验及可用性评估 | [Paper: PDF p. 4, Section 3 and Figures 3-4] |

## 14 学到的知识

### Agent-derived knowledge candidates

- [Paper] 课程知识图谱可拆为数据层、模式层和展示层；模式层先规定实体、属性与关系，再驱动抽取。[Paper: PDF p. 1, Figure 1]
- [Analysis] 本体不仅是最终图谱的数据模式，也可以作为提示约束，缩小大语言模型的输出空间。[Paper: PDF pp. 1-3, Sections 1.1-1.2]
- [Paper] 实体、属性和关系应分别设计输出结构：实体/属性用二元组，关系用三元组。[Paper: PDF p. 2, Table 2] [Paper: PDF p. 3, Tables 3-4]
- [Analysis] 单看 F1 会遮蔽错误类型：本文关系抽取的高 Recall 与低 Precision 表明，图谱入库前需要验证或纠错环节。[Paper: PDF p. 3, Table 6]
- [Paper] Neo4j 将实体表示为节点、关系表示为连接，并通过 Cypher 支持图查询。[Paper: PDF p. 4, Section 3]

## 15 与已有知识的联系

当前为 paper-only 模式，以下仅为论文内部可见的联系，未独立核验外部文献：

- [Analysis] 该流程连接了三个常见层次：领域本体负责模式约束，信息抽取负责实例生成，图数据库负责存储与交互。[Paper: PDF p. 1, Figure 1]
- [Analysis] 多轮提示在这里承担了“任务分解 + 标签集合约束 + 输出格式约束”的作用，可与结构化输出、模式校验和人工复核组合。[Paper: PDF pp. 2-3, Sections 1.2.1-1.2.3]
- [Analysis] 关系抽取的 Precision/Recall 失衡提示：若系统目标是直接写入知识库，优化目标不应只有覆盖率，还应考虑错误边对下游查询的影响。[Paper: PDF p. 3, Table 6]

## 16 研究想法

### Agent-derived research candidates

#### 候选想法 1：本体约束的关系验证闭环

- 起点：关系抽取 Recall 为 87.09%，但 Precision 为 51.92%，且作者承认复杂关系降低零样本可靠性。[Paper: PDF p. 3, Table 6] [Paper: PDF p. 4, limitations]
- [Hypothesis] 核心假设：在 ChatGPT 输出后增加基于本体的类型约束、反向证据检索和低置信关系人工复核，可以在保持 Recall 不低于基线一定容差的同时显著提高 Precision。
- 相对本文的变化：从“一次提示后直接入库”改为“候选生成—约束校验—证据回溯—选择性人工确认”。
- 初步方法：为每种关系定义允许的主客体类型；要求输出证据句；自动拒绝类型冲突；对剩余候选执行二次判别。
- Validation / 验证方案：在同一固定测试集、同一模型版本与 token 预算下比较原提示、仅类型约束、完整闭环；报告 P/R/F1、人工复核量和单位正确三元组成本。
- 证伪条件：Precision 未提升，或提升完全由大幅牺牲 Recall/增加人工成本造成。
- 可能失败原因：本体定义不完整；二次判别与生成模型共享同类偏差；人工复核成本过高。
- 创新状态：unverified，需检索现有技术。

#### 候选想法 2：版本化、可复现的课程知识抽取基准

- 起点：论文未报告数据规模、划分、模型版本、参数和重复运行结果，表5还存在指标一致性问题。[Paper: PDF p. 3, Section 2, Equation 3 and Table 5]
- [Hypothesis] 核心假设：固定数据划分、标注规范、提示版本、模型快照和评估脚本后，不同抽取策略的相对排名会比单次网页交互结果更稳定，并能揭示模型版本漂移。
- 相对本文的变化：重点从构建单个课程原型转为建立可审计的评估协议和版本账本。
- 初步方法：发布脱敏语料、金标准、标签本体、提示文件、原始输出、评估脚本和每次调用元数据。
- Validation / 验证方案：在多个模型版本上重复运行多个随机种子或采样批次，报告均值、区间、成本和错误类型；对指标脚本进行单元测试。
- 证伪条件：固定协议后结果仍不可重复，或版本化信息不能解释主要波动。
- 可能失败原因：闭源 API 无法锁定快照；公开课程材料受版权限制；数据集太小导致区间过宽。
- 创新状态：unverified，需检索现有技术。

## 关联笔记

- 主题：[[Agent-IFC/20_Themes/课程知识图谱|课程知识图谱]]
- 项目：待关联
- 相关论文：待关联

## 待解决的问题

- [ ] 人工核查 C01-C04 与 PDF 图表。
- [ ] 查明表5中 F1 不一致是排版错误还是评估口径差异。
- [ ] 补充数据规模、划分、ChatGPT 版本和提示执行参数（如作者材料可获得）。
- [ ] 确认该论文归属的具体研究项目后，再填写 projects 与项目链接。
- [ ] 如需判断创新性或研究脉络，另行执行外部文献检索。

## 阅读记录

- 2026-10-12｜Codex｜根据本地完整 PDF 建立 page-grounded 论文卡片；所有核心结论保持“待核查”，状态为 reading。
